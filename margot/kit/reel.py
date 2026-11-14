#!/usr/bin/env python3
"""Reel Margot avec son : voix de Margot (Kokoro, voix française locale et gratuite),
bouche animée sur la voix, sous-titres, 1080 x 1920, 30 images/s.

Usage : python3 reel.py spec.json sortie.mp4 [--apercu]
  --apercu : n'écrit que quelques images JPEG (dossier apercu/) pour contrôler la mise en page.

spec.json :
{ "etiquette": "Les conseils de Margot",
  "scenes": [ { "fond": "creme|prune|or", "pose": "bonjour|pouce|carte",
                "titre": ["ligne 1", "ligne 2"], "puces": ["optionnel"],
                "voix": "Texte dit par Margot." } ] }
Prérequis (installés au besoin par preparer.sh) : kokoro-onnx, soundfile, numpy, playwright,
ffmpeg, la police Fraunces (@fontsource/fraunces) et les fichiers kokoro-v1.0.onnx / voices-v1.0.bin.
"""
import json, math, os, re, subprocess, sys, pathlib
import numpy as np, soundfile as sf

ICI = pathlib.Path(__file__).resolve().parent
W, H, FPS, SR = 1080, 1920, 30, 24000
VOIX, VITESSE = "ff_siwis", 1.0
COUL = {"creme": "#FBF3EC", "prune": "#5A1F4A", "or": "#EBBE72"}


def trouver(nom, *dossiers):
    for d in dossiers:
        p = pathlib.Path(d) / nom
        if p.exists():
            return p
    raise SystemExit(f"Fichier manquant : {nom} (lancez preparer.sh)")


def synthese(scenes):
    """Une prise de voix par scène. Renvoie la piste complète et les repères de temps."""
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

    piste, t = [], 0.0
    for i, sc in enumerate(scenes):
        s, sr = k.create(sons(sc["voix"]), voice=VOIX, speed=VITESSE, lang="fr-fr", is_phonemes=True)
        assert sr == SR
        fort = np.where(np.abs(s) > 0.012)[0]
        s = s[max(0, fort[0] - 900): min(len(s), fort[-1] + 1500)] if len(fort) else s
        avant, apres = (0.35 if i == 0 else 0.45), (0.9 if i == len(scenes) - 1 else 0.35)
        sc["debut"], sc["parle0"] = t, t + avant
        sc["parle1"] = sc["parle0"] + len(s) / SR
        sc["fin"] = sc["parle1"] + apres
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


def sous_titres(sc, maxi=30):
    """Sous-titres : une phrase à la fois, coupée en blocs courts, calée sur les pauses de la voix."""
    texte = re.sub(r"\s+([!?:;])", " \\1", sc["voix"].strip())
    phrases = [p for p in re.split(r"(?<=[.!?…])\s+", texte) if p]
    span = sc["parle1"] - sc["parle0"]
    grandes = sorted(sorted(sc.pop("_pauses", []), key=lambda x: -x[1])[: len(phrases) - 1])
    if len(grandes) == len(phrases) - 1:
        bornes = [0.0] + [m for m, _ in grandes] + [span]
    else:                                                     # pas assez de pauses nettes : au prorata
        poids = [len(p) + 8 for p in phrases]
        bornes = [0.0] + [span * sum(poids[: k + 1]) / sum(poids) for k in range(len(poids))]
    out = []
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
        t0, t1 = sc["parle0"] + bornes[k], sc["parle0"] + bornes[k + 1]
        poids, t = [len(b) + 4 for b in blocs], t0
        for b, p in zip(blocs, poids):
            d = (t1 - t0) * p / sum(poids)
            out.append({"t0": round(t - 0.04, 3), "t1": round(t + d - 0.04, 3), "texte": b})
            t += d
    out[-1]["t1"] = round(sc["parle1"] + 0.25, 3)
    return out


def page_html(data):
    polices = [ICI / "node_modules/@fontsource/fraunces/files", pathlib.Path("/home/claude/insta/node_modules/@fontsource/fraunces/files")]
    f = next((p for p in polices if p.exists()), None)
    face = (f"@font-face{{font-family:Fraunces;font-weight:900;src:url({f.as_uri()}/fraunces-latin-900-normal.woff2)}}"
            f"@font-face{{font-family:Fraunces;font-weight:600;src:url({f.as_uri()}/fraunces-latin-600-normal.woff2)}}") if f else ""
    return (ICI / "reel_page.html").read_text(encoding="utf-8").replace("/*POLICES*/", face).replace("/*DONNEES*/", "window.DATA=" + json.dumps(data, ensure_ascii=False) + ";")


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    apercu = "--apercu" in sys.argv
    scenes = spec["scenes"]
    tmp = sortie.parent / (sortie.stem + "_tmp"); tmp.mkdir(parents=True, exist_ok=True)

    piste = synthese(scenes)
    for sc in scenes:
        sc["subs"] = sous_titres(sc)
        for k in ("debut", "fin", "parle0", "parle1"):
            sc[k] = round(sc[k], 4)
    duree = scenes[-1]["fin"]
    data = {"W": W, "H": H, "fps": FPS, "etiquette": spec.get("etiquette", "Les conseils de Margot"),
            "scenes": scenes, "env": enveloppe(piste), "coul": COUL}
    html = tmp / "page.html"; html.write_text(page_html(data), encoding="utf-8")
    print(f"Durée : {duree:.2f} s, {len(scenes)} scènes")

    # Son : voix + petit « pop » à chaque changement de scène, niveau normalisé
    mix = piste.copy()
    tt = np.arange(int(0.07 * SR)) / SR
    pop = 0.07 * np.sin(2 * np.pi * (520 * tt - 1800 * tt ** 2)) * np.exp(-tt * 55)
    for sc in scenes[1:]:
        d = int(sc["debut"] * SR)
        mix[d:d + len(pop)] += pop.astype(np.float32)
    sf.write(tmp / "voix.wav", mix, SR)

    from playwright.sync_api import sync_playwright
    chrome = "/usr/bin/google-chrome"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome) if os.path.exists(chrome) else p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(html.as_uri()); pg.wait_for_function("window.PRET===true", timeout=20000)
        for a in pg.evaluate("window.ALERTES"):
            print("ALERTE mise en page :", a)
        if apercu:
            d = sortie.parent / "apercu"; d.mkdir(exist_ok=True)
            for i, sc in enumerate(scenes):
                for nom, t in (("a", sc["debut"] + 0.12), ("b", (sc["parle0"] + sc["parle1"]) / 2), ("c", sc["parle1"] - 0.05)):
                    pg.evaluate("t=>render(t)", t)
                    pg.screenshot(path=str(d / f"s{i + 1}{nom}.jpg"), type="jpeg", quality=88)
            b.close(); print("Aperçus dans", d); return
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
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(muet), "-i", str(tmp / "voix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ac", "2", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", "-shortest", str(sortie)], check=True)
    # Couverture (image d'accroche) pour cover_url
    t0 = f"{scenes[0]['fin'] - 0.05:.2f}"                     # fin de l'accroche : titre complet, plus de sous-titre
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", t0, "-i", str(sortie), "-frames:v", "1", "-q:v", "2",
                    str(sortie.with_suffix(".jpg"))], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", t0, "-i", str(sortie), "-frames:v", "1", "-vf", "crop=1080:1080:0:285", "-q:v", "2",
                    str(sortie.with_name(sortie.stem + "-carre.jpg"))], check=True)
    print("Vidéo :", sortie, f"({sortie.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
