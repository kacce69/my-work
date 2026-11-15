#!/usr/bin/env python3
"""Réécoute une vidéo terminée : transcrit son (voix, bruitages et musique mêlés) et compare au scénario.
Sert de contrôle final quand personne n'a encore écouté le Reel : la voix doit rester compréhensible.

Usage : python3 ecouter.py reels/<code>.mp4 specs/<code>.json
Affiche la ressemblance (1 = tout le texte est entendu) et le texte entendu. En dessous de 0,95, écouter ou refaire.
Un seul appel à la fois, et jamais pendant un rendu : la transcription prend beaucoup de mémoire.
"""
import difflib, json, pathlib, subprocess, sys, tempfile
import numpy as np, soundfile as sf
import caler_voix as cv, reel


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    video, spec = pathlib.Path(sys.argv[1]), json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        w = pathlib.Path(tmp) / "a.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-ac", "1", "-ar", "16000", str(w)], check=True)
        son, _ = sf.read(w, dtype="float32")
    from faster_whisper import WhisperModel
    modele = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    segs, _ = modele.transcribe(np.ascontiguousarray(son), language="fr", beam_size=5, condition_on_previous_text=False)
    entendu = " ".join(s.text.strip() for s in segs)
    prevu = " ".join(sc["voix"] for sc in spec["scenes"] if reel.a_voix(sc))
    a, b = [cv.cle(m) for m in cv.norm(prevu)], [cv.cle(m) for m in cv.norm(entendu)]
    r = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    print(f"ressemblance : {r:.3f}" + ("" if r >= 0.95 else "  ← à écouter ou à refaire"))
    print("entendu :", entendu)


if __name__ == "__main__":
    main()
