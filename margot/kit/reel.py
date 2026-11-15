#!/usr/bin/env python3
"""Reel Margot avec son : voix de Margot, bouche animée sur la voix, sous-titres, bruitages, musique,
1080 x 1920, 30 images/s.

Usage : python3 reel.py spec.json sortie.mp4 [--apercu[=N]] [--kokoro | --prise | --muet] [--sans-musique]
        python3 reel.py spec.json --texte      affiche le texte à envoyer à la synthèse vocale (une prise pour tout le Reel)
  --apercu       : n'écrit que des images JPEG (dossier apercu/ : 3 par scène, ou N avec --apercu=N ; --apercu=1 = la fin de
                   chaque scène) et des planches (apercu/planche-1.jpg…) qui les réunissent, pour contrôler la mise en page
                   avant de fabriquer la vidéo. Affiche aussi les durées, l'heure des mots utilisés et les alertes.
  --kokoro       : ignore la prise enregistrée et fabrique la voix avec Kokoro.
  --prise        : exige la prise enregistrée ; s'arrête si elle manque (au lieu de passer à Kokoro).
  --muet         : aucune voix ; les durées sont estimées d'après la longueur du texte. Pour contrôler une mise en page
                   avec --apercu avant d'avoir la prise (rien à installer, rien à payer).
  --sans-musique : ignore la musique demandée par le scénario.

Voix : si voix/<nom du spec>.flac (ou .wav) et voix/<nom du spec>.json existent, c'est cette prise
enregistrée qui est utilisée (voix « Amélie », voir caler_voix.py et le README). Sinon la voix est
fabriquée sur place par Kokoro (voix française locale et gratuite, installée par « preparer.sh kokoro »).

Scénario le plus simple (tout le reste — plans, éléments, gestes, bruitages, musique — est décrit dans CATALOGUE.md) :
{ "etiquette": "Les conseils de Margot",
  "scenes": [ { "fond": "creme|prune|or|nuit", "pose": "bonjour|pouce|carte|…",
                "titre": ["ligne 1", "ligne 2"], "puces": ["optionnel"],
                "voix": "Texte dit par Margot." } ] }
Prérequis (installés au besoin par preparer.sh) : soundfile, numpy, pillow, playwright, ffmpeg, la police Fraunces
(@fontsource/fraunces) ; pour la voix de secours : kokoro-onnx et les fichiers kokoro-v1.0.onnx / voices-v1.0.bin.
"""
import json, math, os, re, subprocess, sys, pathlib
import numpy as np, soundfile as sf

ICI = pathlib.Path(__file__).resolve().parent
W, H, FPS, SR = 1080, 1920, 30, 24000
VOIX, VITESSE = "ff_siwis", 1.0
COUL = {"creme": "#FBF3EC", "prune": "#5A1F4A", "or": "#EBBE72", "nuit": "#2A0A20"}
NOMBRES = "Un|Deux|Trois|Quatre|Cinq|Six|Sept|Huit|Neuf|Dix"


def trouver(nom, *dossiers):
    for d in dossiers:
        p = pathlib.Path(d) / nom
        if p.exists():
            return p
    raise SystemExit(f"Fichier manquant : {nom} (lancez « sh preparer.sh kokoro » pour la voix de secours, ou utilisez --muet pour un simple aperçu)")


def a_voix(sc):
    return bool((sc.get("voix") or "").strip())


def jetons(voix):
    """Les mots d'une scène, tels que les sous-titres les découpent (« ? », « : »… restent collés au mot)."""
    return [m for m in re.sub(r"\s+([!?:;])", "\xa0\\1", voix.strip()).split(" ") if m]


def texte_prise(spec):
    """Le texte à envoyer à la synthèse vocale : une scène par paragraphe (ligne vide entre deux), dans l'ordre.
    « dit » remplace « voix » quand la prononciation demande une autre écriture ; « Un : » devient « Un, »
    (la voix saute parfois le numéro quand il est suivi de deux-points)."""
    return "\n\n".join(re.sub(rf"^({NOMBRES})\s*:", r"\1,", (sc.get("dit") or sc["voix"]).strip()) for sc in spec["scenes"] if a_voix(sc))


def synthese(scenes, prise=None, muet=False):
    """Une voix par scène. Renvoie la piste complète et les repères de temps.
    Sans prise : la voix est fabriquée ici par Kokoro. Avec une prise enregistrée (dossier voix/) :
    chaque scène est découpée dans l'enregistrement et les sous-titres suivent l'heure de chaque mot.
    Une scène sans « voix » est muette : elle dure « duree » secondes (2 par défaut)."""
    if prise is None and not muet and any(a_voix(sc) for sc in scenes):
        from kokoro_onnx import Kokoro
        mod = [ICI / "modeles", ICI, pathlib.Path.cwd(), "/home/claude/tts"]
        k = Kokoro(str(trouver("kokoro-v1.0.onnx", *mod)), str(trouver("voices-v1.0.bin", *mod)))
        import phonemizer
        from kokoro_onnx.tokenizer import Tokenizer

        def sons(texte):
            # Sans cette option, un mot jugé anglais (« Google », « flash », « e-mail ») est entouré de marques
            # « (en) … (fr) » que la voix prononce comme des bruits parasites.
            ph = phonemizer.phonemize(Tokenizer.normalize_text(texte), "fr-fr", preserve_punctuation=True, with_stress=True,
                                      language_switch="remove-flags")
            return "".join(c for c in ph if c in k.tokenizer.vocab).strip()
    elif prise is not None:
        son, sr = sf.read(prise["audio"], dtype="float32")
        son = son.mean(axis=1) if son.ndim > 1 else son
        if sr != SR:
            raise SystemExit(f"{prise['audio']} : {sr} Hz au lieu de {SR} Hz (convertissez avec ffmpeg -ar {SR} -ac 1)")

    piste, t, rang = [], 0.0, 0
    for i, sc in enumerate(scenes):
        parle = a_voix(sc)
        if not parle:
            s = np.zeros(0, dtype=np.float32)
        elif muet:                                                # pas de voix : durée estimée (environ 16 signes par seconde)
            s = np.zeros(int(SR * max(0.8, len(sc["voix"]) / 16.5)), dtype=np.float32)
        elif prise is None:
            s, sr = k.create(sons(sc.get("dit") or sc["voix"]), voice=VOIX, speed=VITESSE, lang="fr-fr", is_phonemes=True)
            assert sr == SR
        else:
            c = prise["scenes"][rang]; rang += 1
            s = son[int(c["debut"] * SR): int(c["fin"] * SR)].copy()
        fort = np.where(np.abs(s) > 0.012)[0]
        d0 = max(0, fort[0] - 900) if len(fort) else 0
        s = s[d0: min(len(s), fort[-1] + 1500)] if len(fort) else s
        if parle and prise is not None and not muet:
            r = min(240, len(s) // 2)                             # fondu de 10 ms aux deux coupes
            s[:r] *= np.linspace(0, 1, r, dtype=np.float32); s[-r:] *= np.linspace(1, 0, r, dtype=np.float32)
            base = c["debut"] + d0 / SR                           # heure, dans la prise, du début de la scène
            sc["_mots"] = [(max(0.0, m0 - base), max(0.0, m1 - base)) for m0, m1 in c["mots"]]
        avant, apres = sc.get("avant", 0.35 if i == 0 else 0.45), sc.get("apres", 0.9 if i == len(scenes) - 1 else 0.35)
        if not parle:                                             # scène muette : une « voix » fictive pour caler les éléments
            duree = float(sc.get("duree", 2.0))
            avant, apres = min(0.3, duree / 4), min(0.3, duree / 4)
            s = np.zeros(int(max(0.0, duree - avant - apres) * SR), dtype=np.float32)
        sc["debut"], sc["parle0"] = t, t + avant
        sc["parle1"] = sc["parle0"] + len(s) / SR
        sc["fin"] = sc["parle1"] + apres
        if sc.get("duree_min"):
            sc["fin"] = max(sc["fin"], sc["debut"] + float(sc["duree_min"]))
        sc["fin"] = math.ceil(sc["fin"] * FPS) / FPS          # durée entière en images
        bloc = np.zeros(int(round((sc["fin"] - sc["debut"]) * SR)), dtype=np.float32)
        d = int(avant * SR)
        bloc[d:d + len(s)] = s[: len(bloc) - d]
        sc["_pauses"] = pauses(s)
        piste.append(bloc)
        t = sc["fin"]
    return np.concatenate(piste)


def enveloppe(piste):
    """Ouverture de la bouche (0..1) pour chaque image, d'après le volume de la voix."""
    n = int(len(piste) / SR * FPS)
    pas = SR // FPS
    rms = np.array([np.sqrt(np.mean(piste[i * pas:(i + 1) * pas] ** 2) + 1e-12) for i in range(n)])
    ref = np.percentile(rms[rms > 0.01], 90) if np.any(rms > 0.01) else 1.0
    o = np.clip((rms - 0.012) / (ref * 0.9), 0, 1) ** 0.7
    lisse = np.zeros(n)
    for i in range(n):                                        # monte vite, redescend doucement
        prec = lisse[i - 1] if i else 0.0
        lisse[i] = o[i] if o[i] > prec else prec * 0.55 + o[i] * 0.45
    return [round(float(x), 3) for x in lisse]


def pauses(s):
    """Silences à l'intérieur d'une prise de voix : liste (milieu en secondes, durée)."""
    pas = SR // 100
    e = np.array([np.sqrt(np.mean(s[i:i + pas] ** 2)) for i in range(0, len(s) - pas, pas)])
    calme, out, i = e < 0.02, [], 0
    while i < len(calme):
        if calme[i]:
            j = i
            while j < len(calme) and calme[j]:
                j += 1
            if 0 < i and j < len(calme) and (j - i) >= 10:
                out.append(((i + j) / 2 / 100, (j - i) / 100))
            i = j
        else:
            i += 1
    return out


def mots_scene(sc):
    """Heure de début et de fin de chaque mot de la scène, en secondes depuis le début du Reel : [début, fin, mot].
    Avec une prise enregistrée, ce sont les heures réelles ; avec Kokoro, une estimation au prorata des lettres."""
    if not a_voix(sc):
        return []
    toks = jetons(sc["voix"])
    if "_mots" in sc:
        h = sc["_mots"]
    else:
        span, poids = sc["parle1"] - sc["parle0"], [len(tk) + 1.5 for tk in toks]
        cumul = np.concatenate([[0.0], np.cumsum(poids)]) / sum(poids)
        h = [(span * cumul[j], span * cumul[j + 1]) for j in range(len(toks))]
    return [[round(sc["parle0"] + a, 3), round(sc["parle0"] + b, 3), tk] for (a, b), tk in zip(h, toks)]


def sous_titres(sc, maxi=30):
    """Sous-titres : une phrase à la fois, coupée en blocs courts, calée sur les pauses de la voix.
    Chaque bloc porte aussi « m » : l'heure de chacun de ses mots (pour les mettre en valeur un à un)."""
    if not a_voix(sc):
        sc.pop("_mots", None); sc.pop("_pauses", None)
        return []
    texte = re.sub(r"\s+([!?:;])", "\xa0\\1", sc["voix"].strip())
    phrases = [p for p in re.split(r"(?<=[.!?…])\s+", texte) if p]
    span = sc["parle1"] - sc["parle0"]
    heures = sc.pop("_mots", None)                            # prise enregistrée : heure de chaque mot
    grandes = sorted(sorted(sc.pop("_pauses", []), key=lambda x: -x[1])[: len(phrases) - 1])
    if len(grandes) == len(phrases) - 1:
        bornes = [0.0] + [m for m, _ in grandes] + [span]
    else:                                                     # pas assez de pauses nettes : au prorata
        poids = [len(p) + 8 for p in phrases]
        bornes = [0.0] + [span * sum(poids[: k + 1]) / sum(poids) for k in range(len(poids))]
    out, rang = [], 0
    for k, ph in enumerate(phrases):
        mots, n = ph.split(" "), max(1, math.ceil(len(ph) / maxi))
        cible, blocs, cur = len(ph) / n, [], ""
        for m in mots:
            essai = (cur + " " + m).strip()
            if cur and (len(essai) > maxi or (len(blocs) < n - 1 and (len(cur) >= cible or (cur.endswith(",") and len(cur) >= 0.55 * cible)))):
                fin = cur.split(" ")
                if len(fin) > 1 and len(fin[-1]) <= 3 and fin[-1].isalpha():   # pas de bloc fini par « je », « par », « de »…
                    cur, m = " ".join(fin[:-1]), fin[-1] + " " + m
                blocs.append(cur); cur = m
            else:
                cur = essai
        blocs.append(cur)
        if heures:                                            # chaque bloc commence quand son premier mot est dit
            for b in blocs:
                nb = len(b.split(" "))
                t = sc["parle0"] + heures[min(rang, len(heures) - 1)][0]
                out.append({"t0": round(t - 0.04, 3), "t1": 0.0, "texte": b,
                            "m": [round(sc["parle0"] + heures[min(rang + j, len(heures) - 1)][0], 3) for j in range(nb)]})
                rang += nb
            continue
        t0, t1 = sc["parle0"] + bornes[k], sc["parle0"] + bornes[k + 1]
        poids, t = [len(b) + 4 for b in blocs], t0
        for b, p in zip(blocs, poids):
            d, nb = (t1 - t0) * p / sum(poids), len(b.split(" "))
            out.append({"t0": round(t - 0.04, 3), "t1": round(t + d - 0.04, 3), "texte": b,
                        "m": [round(t + d * j / nb - 0.04, 3) for j in range(nb)]})
            t += d
    if heures:
        out[0]["t0"] = min(out[0]["t0"], round(sc["parle0"] - 0.04, 3))
        for a, b in zip(out, out[1:]):                        # jamais à rebours, jamais moins de 0,3 s à l'écran
            b["t0"] = max(b["t0"], round(a["t0"] + 0.3, 3))
            a["t1"] = b["t0"]
    out[-1]["t1"] = round(sc["parle1"] + 0.25, 3)
    return out


def page_html(data):
    polices = [ICI / "node_modules/@fontsource/fraunces/files", pathlib.Path("/home/claude/insta/node_modules/@fontsource/fraunces/files")]
    f = next((p for p in polices if p.exists()), None)
    face = (f"@font-face{{font-family:Fraunces;font-weight:900;src:url({f.as_uri()}/fraunces-latin-900-normal.woff2)}}"
            f"@font-face{{font-family:Fraunces;font-weight:600;src:url({f.as_uri()}/fraunces-latin-600-normal.woff2)}}") if f else ""
    inter = ICI / "node_modules/@fontsource/inter/files"
    if inter.exists() and "Inter" not in subprocess.run(["fc-list", ":family"], capture_output=True, text=True).stdout:
        face += "".join(f"@font-face{{font-family:Inter;font-weight:{g};src:url({inter.as_uri()}/inter-latin-{g}-normal.woff2)}}" for g in (300, 500, 600, 700, 800))
    scripts = "\n".join(p.read_text(encoding="utf-8") for p in sorted((ICI / "page").glob("*.js")))
    donnees = "window.DATA=" + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";"
    return (ICI / "reel_page.html").read_text(encoding="utf-8").replace("/*POLICES*/", face).replace("/*SCRIPTS*/", scripts).replace("/*DONNEES*/", donnees)


def chemins(o, base, manquants):
    """Les « src » (images) écrits par rapport au scénario deviennent des adresses de fichiers."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "src" and isinstance(v, str) and not re.match(r"^(https?|file|data):", v):
                p = (base / v).resolve()
                if not p.exists():
                    manquants.append(v)
                o[k] = p.as_uri()
            else:
                chemins(v, base, manquants)
    elif isinstance(o, list):
        for v in o:
            chemins(v, base, manquants)


def planches(dossier, images, par_scene):
    """Réunit les images d'aperçu en planches (une ligne par scène) : un seul coup d'œil pour tout contrôler."""
    from PIL import Image
    larg = 1080 // par_scene
    haut = larg * H // W
    lignes = max(1, 1500 // haut)
    rangs = [images[k:k + par_scene] for k in range(0, len(images), par_scene)]
    sorties = []
    for p in range(0, len(rangs), lignes):
        bloc = rangs[p:p + lignes]
        pl = Image.new("RGB", (larg * par_scene, haut * len(bloc)), "#888888")
        for y, rang in enumerate(bloc):
            for x, f in enumerate(rang):
                with Image.open(f) as im:
                    pl.paste(im.convert("RGB").resize((larg - 4, haut - 4), Image.LANCZOS), (x * larg + 2, y * haut + 2))
        s = dossier / f"planche-{p // lignes + 1}.jpg"
        pl.save(s, quality=88); sorties.append(s)
    return sorties


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args or (len(args) < 2 and "--texte" not in opts):
        raise SystemExit(__doc__)
    chemin = pathlib.Path(args[0])
    spec = json.loads(chemin.read_text(encoding="utf-8"))
    if "--texte" in opts:
        print(texte_prise(spec)); return
    sortie = pathlib.Path(args[1]).resolve()
    apercu = next((a for a in opts if a.startswith("--apercu")), None)
    scenes = spec["scenes"]
    tmp = sortie.parent / (sortie.stem + "_tmp"); tmp.mkdir(parents=True, exist_ok=True)
    manquants = []
    chemins(scenes, chemin.resolve().parent, manquants)

    prise, nom = None, chemin.stem
    parlantes = [sc for sc in scenes if a_voix(sc)]
    cale = ICI / "voix" / f"{nom}.json"
    audio = next((p for p in (ICI / "voix" / f"{nom}.flac", ICI / "voix" / f"{nom}.wav") if p.exists()), None)
    muet = "--muet" in opts
    if muet and not apercu:
        raise SystemExit("--muet ne sert qu'avec --apercu : une vidéo sans voix ne se publie pas.")
    if cale.exists() and audio and "--kokoro" not in opts and not muet:
        prise = json.loads(cale.read_text(encoding="utf-8")); prise["audio"] = str(audio)
        if len(prise["scenes"]) != len(parlantes) or any(len(c["mots"]) != len(jetons(sc["voix"])) for c, sc in zip(prise["scenes"], parlantes)):
            raise SystemExit(f"voix/{nom}.json ne correspond plus au scénario : refaites la prise ou relancez caler_voix.py {nom}")
    if "--prise" in opts and not prise:
        raise SystemExit(f"Pas de prise enregistrée calée pour {nom} (voix/{nom}.flac et voix/{nom}.json) : rien n'est fabriqué.")
    print("Voix :", "aucune (aperçu muet, durées estimées)" if muet else f"prise enregistrée {audio.name}" if prise else "Kokoro (fabriquée sur place)")
    piste = synthese(scenes, prise, muet)
    for sc in scenes:
        sc["mots"] = mots_scene(sc)
        sc["subs"] = sous_titres(sc, 17 if sc.get("plan") == "mots" else 30)
        for k in ("debut", "fin", "parle0", "parle1"):
            sc[k] = round(sc[k], 4)
    duree = scenes[-1]["fin"]
    data = {"W": W, "H": H, "fps": FPS, "etiquette": spec.get("etiquette", "Les conseils de Margot"),
            "scenes": scenes, "env": enveloppe(piste), "coul": COUL, "opt": {k: v for k, v in spec.items() if k != "scenes"}}
    html = tmp / "page.html"; html.write_text(page_html(data), encoding="utf-8")
    print(f"Durée : {duree:.2f} s, {len(scenes)} scènes")
    for v in manquants:
        print("ALERTE : image introuvable :", v)

    from playwright.sync_api import sync_playwright
    chrome = "/usr/bin/google-chrome"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome) if os.path.exists(chrome) else p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.on("pageerror", lambda e: print("ALERTE : erreur de la page :", e))
        pg.goto(html.as_uri()); pg.wait_for_function("window.PRET===true", timeout=30000)
        for a in pg.evaluate("window.ALERTES"):
            print("ALERTE mise en page :", a)
        evenements = pg.evaluate("window.SONS")

        # Son : voix + bruitages (le « pop » des changements de scène, et ceux des éléments), niveau normalisé
        mix, inconnus = piste.copy(), set()
        if evenements:
            import sons as bruits
            for e in evenements:
                try:
                    s = bruits.effet(e["son"])
                except KeyError:
                    inconnus.add(str(e["son"])); continue
                d = int(e["t"] * SR)
                if 0 <= d < len(mix):
                    s = s[: len(mix) - d]
                    mix[d:d + len(s)] += s if e.get("vol", 1) == 1 else (s * float(e["vol"])).astype(np.float32)
        for n in sorted(inconnus):
            print("ALERTE : bruitage inconnu :", n)
        sf.write(tmp / "voix.wav", mix, SR)
        musique = None if "--sans-musique" in opts else spec.get("musique")
        if musique:
            import sons as bruits
            m_nom, m_vol = (musique, 0) if isinstance(musique, str) else (musique.get("nom"), musique.get("volume", 0))
            try:
                sf.write(tmp / "musique.wav", bruits.musique(m_nom, duree) * 10 ** (m_vol / 20), bruits.SRM)
            except KeyError:
                print("ALERTE : musique inconnue :", m_nom); musique = None

        if apercu:
            par_scene = int(apercu.split("=")[1]) if "=" in apercu else 3
            d = sortie.parent / "apercu"; d.mkdir(exist_ok=True)
            for f in d.iterdir():
                if re.fullmatch(r"(s\d+[a-z]|planche-\d+)\.jpg", f.name):
                    f.unlink()
            images = []
            for i, sc in enumerate(scenes):
                if par_scene == 3:
                    instants = [sc["debut"] + 0.12, (sc["parle0"] + sc["parle1"]) / 2, sc["parle1"] - 0.05]
                elif par_scene == 1:                              # une seule image : la fin de la scène, tout est en place
                    instants = [sc["fin"] - 0.05]
                else:
                    a, z = sc["debut"] + 0.12, sc["fin"] - 0.05
                    instants = [a + (z - a) * j / max(1, par_scene - 1) for j in range(par_scene)]
                for j, t in enumerate(instants):
                    pg.evaluate("t=>render(t)", t)
                    f = d / f"s{i + 1}{'abcdefghijklmnop'[j]}.jpg"
                    pg.screenshot(path=str(f), type="jpeg", quality=88); images.append(f)
                print(f"scène {i + 1} : de {sc['debut']:.2f} à {sc['fin']:.2f} s, voix de {sc['parle0']:.2f} à {sc['parle1']:.2f} s")
            for ligne in pg.evaluate("window.JOURNAL"):
                print("  ", ligne)
            print(f"bruitages : {len(evenements)}" + (f", musique : {m_nom}" if musique else ""))
            b.close()
            print("Aperçus dans", d, "- planches :", ", ".join(s.name for s in planches(d, images, 4 if par_scene == 1 else par_scene))); return
        fichiers = []
        for i, sc in enumerate(scenes):
            brut, fini = tmp / f"scene{i + 1}.part.mp4", tmp / f"scene{i + 1}.mp4"
            ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                   "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p",
                                   "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                                   "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(brut)], stdin=subprocess.PIPE)
            n0, n1 = int(round(sc["debut"] * FPS)), int(round(sc["fin"] * FPS))
            for n in range(n0, n1):
                pg.evaluate("t=>render(t)", n / FPS)
                ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
            ff.stdin.close()
            if ff.wait() != 0:
                raise SystemExit(f"ffmpeg a échoué sur la scène {i + 1}")
            brut.rename(fini); fichiers.append(fini); print(f"scène {i + 1} : {n1 - n0} images")
        b.close()
    (tmp / "liste.txt").write_text("".join(f"file '{f}'\n" for f in fichiers))
    muet = tmp / "muet.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "liste.txt"), "-c", "copy", str(muet)], check=True)
    if musique:
        # La voix (et les bruitages) gardent leur niveau ; la musique passe dessous et s'efface quand Margot parle.
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(muet), "-i", str(tmp / "voix.wav"), "-i", str(tmp / "musique.wav"), "-filter_complex",
                        "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v][k];"
                        "[2:a][k]sidechaincompress=threshold=0.03:ratio=6:attack=25:release=450[m];"
                        "[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.9:level=disabled[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", str(sortie)], check=True)
    else:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(muet), "-i", str(tmp / "voix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ac", "2", "-c:a", "aac", "-b:a", "160k",
                        "-movflags", "+faststart", "-shortest", str(sortie)], check=True)
    # Couverture (image d'accroche) pour cover_url : par défaut la fin de la première scène (titre complet, plus de sous-titre)
    cv = spec.get("couverture") or {}
    sc0 = scenes[min(len(scenes), max(1, int(cv.get("scene", 1)))) - 1]
    t0 = f"{(sc0['debut'] + cv['instant']) if 'instant' in cv else (sc0['fin'] - 0.05):.2f}"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", t0, "-i", str(sortie), "-frames:v", "1", "-q:v", "2",
                    str(sortie.with_suffix(".jpg"))], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", t0, "-i", str(sortie), "-frames:v", "1", "-vf", "crop=1080:1080:0:285", "-q:v", "2",
                    str(sortie.with_name(sortie.stem + "-carre.jpg"))], check=True)
    print("Vidéo :", sortie, f"({sortie.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
