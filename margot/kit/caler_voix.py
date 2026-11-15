#!/usr/bin/env python3
"""Cale une prise de voix enregistrée (une seule prise pour tout le Reel) sur son scénario.

Usage : python3 caler_voix.py J01 HS0 …        (sans argument : toutes les prises du dossier voix/)

Pour chaque code, lit specs/<code>.json et voix/<code>.flac (ou .wav, 24 000 Hz mono), puis écrit
voix/<code>.json :
  - où couper la prise pour chaque scène (au milieu du silence qui sépare deux scènes) ;
  - l'heure de chaque mot, pour que les sous-titres suivent la voix ;
  - un contrôle : ce qui a été entendu, comparé au texte prévu (« ratio » et « ecarts »), et des alertes.
reel.py utilise ensuite ces deux fichiers à la place de la voix Kokoro.

La prise se fait en une fois, les textes des scènes séparés par une ligne vide (voir le README).
Transcription locale et gratuite (faster-whisper : pip install faster-whisper).
"""
import difflib, json, pathlib, re, subprocess, sys, tempfile, unicodedata
import numpy as np, soundfile as sf
import reel

ICI = pathlib.Path(__file__).resolve().parent
SR = reel.SR
UNITES = "zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize".split()
DIZAINES = {20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 60: "soixante"}


def nombre(n):
    """Un nombre de 0 à 99 en toutes lettres, mot par mot."""
    if n < 17:
        return [UNITES[n]]
    if n < 20:
        return ["dix", UNITES[n - 10]]
    if n < 70:
        d, u = n // 10 * 10, n % 10
        return [DIZAINES[d]] + ([] if u == 0 else ["et", "un"] if u == 1 else [UNITES[u]])
    if n < 80:
        return ["soixante"] + (["et"] if n == 71 else []) + nombre(n - 60)
    return ["quatre", "vingt"] + ([] if n == 80 else nombre(n - 80))


def norm(t):
    """Texte → mots comparables (minuscules, sans ponctuation, nombres en lettres)."""
    t = re.sub(r"(?<=[a-zà-ÿ])(?=[A-Z])", " ", unicodedata.normalize("NFC", t))      # « RestaurantSite » → deux mots
    t = t.lower().replace("’", "'").replace("œ", "oe")
    t = re.sub(r"(\d+)\s*%", r"\1 pour cent", t)
    t = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿ]", " ", t)
    out = []
    for m in t.split():
        if m == "1er":
            out.append("premier")
        elif m.isdigit() and int(m) < 100:
            out += nombre(int(m))
        else:
            out.append(m)
    return out


def cle(m):
    """Deux mots qui se prononcent pareil (« jours »/« jour », « cherchent »/« cherche ») ont la même clé."""
    if len(m) > 4 and m.endswith("ent"):
        m = m[:-2]
    m = m[:-1] if len(m) > 2 and m[-1] in "sx" else m
    if len(m) > 3 and m[-2:] in ("ez", "er"):                 # « comparez » / « comparer » / « comparé »
        m = m[:-2] + "é"
    elif m.endswith("ée"):
        m = m[:-1]
    for a, b in (("eau", "o"), ("au", "o"), ("aim", "in"), ("ain", "in"), ("ein", "in")):
        m = m.replace(a, b)
    return m


def ecouter(modele, son16):
    """Mots entendus, avec leur heure : [(mot, début, fin)]."""
    segs, _ = modele.transcribe(son16, language="fr", beam_size=5, condition_on_previous_text=False, word_timestamps=True)
    return [(n, float(w.start), float(w.end)) for s in segs for w in (s.words or []) for n in norm(w.word)]


def aligner(prevus, entendus):
    """Heure de chaque mot prévu, d'après les mots entendus. Renvoie (heures, ratio, écarts).
    Chaque écart : (rangs des mots prévus concernés, description)."""
    sm = difflib.SequenceMatcher(None, [cle(p[0]) for p in prevus], [cle(e[0]) for e in entendus], autojunk=False)
    heures, ecarts = [None] * len(prevus), []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            for k in range(a1 - a0):
                heures[a0 + k] = (entendus[b0 + k][1], entendus[b0 + k][2])
            continue
        ecarts.append((set(range(a0, a1)) or {a0 - 1, a0},
                       f"« {' '.join(p[0] for p in prevus[a0:a1])} » → « {' '.join(e[0] for e in entendus[b0:b1])} »"))
        if op == "replace":                                   # on répartit les mots entendus sur les mots prévus
            na, nb = a1 - a0, b1 - b0
            for k in range(na):
                j0, j1 = b0 + k * nb // na, b0 + max((k + 1) * nb // na - 1, k * nb // na)
                heures[a0 + k] = (entendus[j0][1], entendus[min(j1, b1 - 1)][2])
    # mots prévus restés sans heure : entre leurs voisins
    for i, h in enumerate(heures):
        if h is None:
            avant = next((heures[j][1] for j in range(i - 1, -1, -1) if heures[j]), 0.0)
            apres = next((heures[j][0] for j in range(i + 1, len(heures)) if heures[j]), avant)
            heures[i] = (avant, max(avant, apres))
    return heures, sm.ratio(), ecarts


def caler(code, modeles):
    spec = json.loads((ICI / "specs" / f"{code}.json").read_text(encoding="utf-8"))
    audio = next(p for p in (ICI / "voix" / f"{code}.flac", ICI / "voix" / f"{code}.wav") if p.exists())
    son, sr = sf.read(audio, dtype="float32")
    son = son.mean(axis=1) if son.ndim > 1 else son
    if sr != SR:
        raise SystemExit(f"{audio} : {sr} Hz au lieu de {SR} Hz")
    duree = len(son) / SR

    # Mots prévus, avec la scène et le rang du mot dans la scène
    listes = [reel.jetons(sc["voix"]) for sc in spec["scenes"] if reel.a_voix(sc)]     # les scènes muettes n'ont pas de prise
    prevus = [(n, si, ti) for si, toks in enumerate(listes) for ti, tok in enumerate(toks) for n in norm(tok)]

    with tempfile.TemporaryDirectory() as tmp:
        w16 = pathlib.Path(tmp) / "a.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(audio), "-ac", "1", "-ar", "16000", str(w16)], check=True)
        son16, _ = sf.read(w16, dtype="float32")
    son16 = np.ascontiguousarray(son16)

    heures, ratio, ecarts = aligner(prevus, ecouter(modeles("small"), son16))
    if ecarts:                                                # doute : on réécoute avec un modèle plus fin
        h2, r2, e2 = aligner(prevus, ecouter(modeles("medium"), son16))
        douteux1, douteux2 = set().union(*(r for r, _ in ecarts)), set().union(*(r for r, _ in e2)) if e2 else set()
        if r2 >= ratio:
            heures, ratio, ecarts = h2, r2, e2
        # un écart ne compte que si les deux écoutes butent au même endroit
        ecarts = [(r, d) for r, d in ecarts if r & douteux1 & douteux2]
    ecarts = [d for _, d in ecarts]

    # Heure de chaque mot du scénario (un mot du scénario peut valoir plusieurs mots dits : « annoncez-les »)
    mots = [[None] * len(toks) for toks in listes]
    for (n, si, ti), (h0, h1) in zip(prevus, heures):
        m = mots[si][ti]
        mots[si][ti] = [h0, h1] if m is None else [min(m[0], h0), max(m[1], h1)]
    for si, lm in enumerate(mots):                            # « ? » isolé, etc. : l'heure du mot d'avant
        for ti, m in enumerate(lm):
            if m is None:
                prec = lm[ti - 1][1] if ti else (mots[si - 1][-1][1] if si else 0.0)
                lm[ti] = [prec, prec]

    # Silences de la prise (pas de 10 ms)
    pas = SR // 100
    e = np.array([np.sqrt(np.mean(son[i:i + pas] ** 2)) for i in range(0, len(son) - pas + 1, pas)])
    seuil = max(0.004, 0.05 * float(np.percentile(e, 95)))
    calme, plages, i = e < seuil, [], 0
    while i < len(calme):
        if calme[i]:
            j = i
            while j < len(calme) and calme[j]:
                j += 1
            plages.append((i / 100, j / 100)); i = j
        else:
            i += 1

    # Après un silence net, le mot le plus proche commence exactement quand la voix reprend
    plat = [m for lm in mots for m in lm]
    for a, b in plages:
        if b - a >= 0.15 and b < duree - 0.05:
            k = min(range(len(plat)), key=lambda j: abs(plat[j][0] - b))
            if abs(plat[k][0] - b) <= 0.35:
                plat[k][0] = b; plat[k][1] = max(plat[k][1], b)
    for j in range(1, len(plat)):                             # les heures ne reculent jamais
        plat[j][0] = max(plat[j][0], plat[j - 1][0])

    alertes, coupes = [], [0.0]
    for si in range(len(mots) - 1):
        ta, tb = mots[si][-1][1], mots[si + 1][0][0]
        f0, f1 = max(coupes[-1] + 0.2, ta - 0.35), min(duree, tb + 0.35)
        cand = [(min(b, f1) - max(a, f0), a, b) for a, b in plages if min(b, f1) - max(a, f0) >= 0.08]
        if cand:
            _, a, b = max(cand)
            coupes.append(round((max(a, f0 - 0.5) + min(b, f1 + 0.5)) / 2, 3))
            if b - a < 0.2:
                alertes.append(f"scènes {si + 1}/{si + 2} : pause de {b - a:.2f} s seulement")
        else:
            coupes.append(round((ta + tb) / 2, 3)); alertes.append(f"scènes {si + 1}/{si + 2} : pas de silence net à la coupe")
    coupes.append(round(duree, 3))

    for a, b in plages:                                       # silence anormal au milieu d'une scène
        if b - a > 1.2 and a > 0.05 and b < duree - 0.05 and not any(abs(c - (a + b) / 2) < (b - a) / 2 for c in coupes[1:-1]):
            alertes.append(f"silence de {b - a:.1f} s à {a:.1f} s")
    bruit = lambda t0, t1: float(np.sum(~calme[int(max(0, t0) * 100): int(max(0, t1) * 100)])) / 100
    if bruit(0, mots[0][0][0] - 0.4) > 0.25:
        alertes.append("du son avant le premier mot")
    if bruit(mots[-1][-1][1] + 0.6, duree) > 0.25:
        alertes.append("du son après le dernier mot")
    if ratio < 0.9:
        alertes.append("texte entendu trop différent du texte prévu")

    out = {"audio": audio.name, "duree": round(duree, 3), "ratio": round(ratio, 3), "ecarts": ecarts, "alertes": alertes,
           "scenes": [{"debut": coupes[si], "fin": coupes[si + 1], "mots": [[round(a, 3), round(b, 3)] for a, b in mots[si]]}
                      for si in range(len(mots))]}
    part = ICI / "voix" / f"{code}.json.part"                 # écrit d'un coup : reel.py ne lit jamais un fichier à moitié fait
    part.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    part.rename(ICI / "voix" / f"{code}.json")
    print(f"{code} : {ratio:.3f} | {duree:.1f} s | coupes {coupes[1:-1]}"
          + ("" if not ecarts else " | écarts : " + " ; ".join(ecarts))
          + ("" if not alertes else " | ALERTES : " + " ; ".join(alertes)), flush=True)


def main():
    from faster_whisper import WhisperModel
    charges = {}

    def modeles(nom):
        if nom not in charges:
            charges[nom] = WhisperModel(nom, device="cpu", compute_type="int8", cpu_threads=2)
        return charges[nom]

    codes = sys.argv[1:] or sorted({p.stem for p in (ICI / "voix").glob("*.flac")} | {p.stem for p in (ICI / "voix").glob("*.wav")})
    for code in codes:
        caler(code, modeles)


if __name__ == "__main__":
    main()
