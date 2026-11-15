#!/usr/bin/env python3
"""Bruitages et musiques de fond des Reels de Margot, fabriqués par calcul : aucun fichier son, aucun droit à payer.

  effet(nom)            → un bruitage (mono, 24 000 Hz)        noms : voir EFFETS
  musique(nom, duree)   → une musique de fond (stéréo, 48 000 Hz) noms : voir MUSIQUES
  python3 sons.py       → écrit un échantillon de chaque son dans echantillons/ pour les écouter
"""
import numpy as np

SR, SRM = 24000, 48000                                        # bruitages (comme la voix) ; musique


def _t(d, sr=SR):
    return np.arange(int(d * sr)) / sr


def _bruit(n, bas, haut, sr, graine):
    """Bruit limité à une bande de fréquences, toujours le même pour une graine donnée."""
    s = np.fft.rfft(np.random.default_rng(graine).standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / sr)
    s[(f < bas) | (f > haut)] = 0
    y = np.fft.irfft(s, n)
    return y / (np.max(np.abs(y)) + 1e-9)


def _note(f, d, sr=SR, harm=((1, 1.0, 6), (2, 0.4, 9), (3, 0.15, 13))):
    """Une note qui s'éteint : harm = (rang de l'harmonique, force, vitesse d'extinction)."""
    tt = _t(d, sr)
    y = sum(a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * c) for h, a, c in harm)
    n, m = min(len(y), int(0.004 * sr)), min(len(y), int(0.02 * sr))
    y[:n] *= np.linspace(0, 1, n); y[-m:] *= np.linspace(1, 0, m)
    return y


def _suite(freqs, pas, tenue, harm=((1, 1.0, 7), (2.76, 0.4, 11), (5.4, 0.15, 16))):
    y = np.zeros(int((pas * (len(freqs) - 1) + tenue) * SR) + 1)
    for k, f in enumerate(freqs):
        n = _note(f, tenue if k == len(freqs) - 1 else max(pas * 2.5, 0.2), SR, harm)
        i = int(k * pas * SR); y[i:i + len(n)] += n[: len(y) - i]
    return y


def _glisse_freq(f, sr=SR):
    return 2 * np.pi * np.cumsum(f) / sr


# ── Bruitages ────────────────────────────────────────────────────────────────────────────────────
def _pop():                                                   # le « pop » d'origine des changements de scène
    tt = np.arange(int(0.07 * SR)) / SR
    return 0.07 * np.sin(2 * np.pi * (520 * tt - 1800 * tt ** 2)) * np.exp(-tt * 55)


def _whoosh(d=0.36, g=0.10, graine=3):
    n = int(d * SR); k = np.arange(n) / n
    y = _bruit(n, 300, 1200, SR, graine) * (1 - k) + _bruit(n, 1200, 3500, SR, graine + 1) * np.sin(np.pi * k) + 0.7 * _bruit(n, 3500, 9000, SR, graine + 2) * k
    return g * np.sin(np.pi * k) ** 2 * y


def _ding(f=1320, d=0.7, g=0.085):
    tt = _t(d)
    return g * (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) + 0.45 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 11) + 0.2 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 16))


def _tic():
    tt = _t(0.035)
    return 0.05 * np.sin(2 * np.pi * 2100 * tt) * np.exp(-tt * 160) + 0.02 * _bruit(len(tt), 3000, 9000, SR, 5) * np.exp(-tt * 300)


def _clic():
    tt = _t(0.05)
    return 0.07 * (np.sin(2 * np.pi * 1300 * tt) + 0.5 * np.sin(2 * np.pi * 820 * tt)) * np.exp(-tt * 120)


def _bulle():
    tt = _t(0.11)
    return 0.06 * np.sin(_glisse_freq(520 + 520 * tt / 0.11)) * np.sin(np.pi * tt / 0.11) ** 1.5


def _impact(g=0.22, grave=50, aigu=120, graine=7):
    tt = _t(0.3)
    return g * np.sin(_glisse_freq(grave + aigu * np.exp(-tt * 32))) * np.exp(-tt * 12) + 0.3 * g * _bruit(len(tt), 250, 3500, SR, graine) * np.exp(-tt * 55)


def _compte():                                                # petits tics de plus en plus aigus et rapprochés
    y = np.zeros(int(1.0 * SR))
    for k in range(10):
        t0, f = 0.95 * (1 - (1 - k / 10) ** 1.7), 900 + 90 * k
        tt = _t(0.03); n = 0.035 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 150)
        i = int(t0 * SR); y[i:i + len(n)] += n[: len(y) - i]
    return y


def _erreur():
    a, b = _note(233.1, 0.16, SR, ((1, 1.0, 9), (3, 0.3, 12))), _note(185.0, 0.26, SR, ((1, 1.0, 8), (3, 0.3, 11)))
    y = np.zeros(int(0.14 * SR) + len(b)); y[:len(a)] += a; y[int(0.14 * SR):] += b
    return 0.09 * y


EFFETS = {
    "pop": _pop,
    "whoosh": _whoosh,
    "glisse": lambda: _whoosh(0.18, 0.07, 9),
    "ding": _ding,
    "cloche": lambda: _ding(1760, 1.1, 0.08),
    "tic": _tic,
    "clic": _clic,
    "bulle": _bulle,
    "impact": _impact,
    "tampon": lambda: _impact(0.26, 60, 160, 11),
    "compte": _compte,
    "succes": lambda: 0.075 * _suite([659.25, 880.0], 0.09, 0.5),
    "tada": lambda: 0.07 * _suite([523.25, 659.25, 783.99, 1046.5], 0.07, 0.7),
    "caisse": lambda: 0.06 * _suite([2093.0, 2637.0], 0.06, 0.6) + np.pad(0.03 * _bruit(int(0.12 * SR), 4000, 10000, SR, 13) * np.exp(-_t(0.12) * 30), (0, int(0.66 * SR) + 1 - int(0.12 * SR))),
    "erreur": _erreur,
}
_CACHE = {}


def effet(nom):
    if nom not in EFFETS:
        raise KeyError(nom)
    if nom not in _CACHE:
        _CACHE[nom] = np.asarray(EFFETS[nom](), dtype=np.float32)
    return _CACHE[nom]


# ── Musiques de fond ─────────────────────────────────────────────────────────────────────────────
DEMI = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
MARIMBA = ((1, 1.0, 9), (4, 0.3, 20), (9.2, 0.08, 34))
PIANO = ((1, 1.0, 3.2), (2, 0.42, 4.5), (3, 0.16, 6.5), (4, 0.06, 9))
BASSE = ((1, 1.0, 5), (2, 0.3, 7))
PIZZ = ((1, 1.0, 11), (2, 0.5, 14), (3, 0.3, 17), (4, 0.15, 21))
ACC = {"C": ("C", "E", "G"), "G": ("G", "B", "D"), "Am": ("A", "C", "E"), "F": ("F", "A", "C"), "Dm": ("D", "F", "A"), "E": ("E", "G#", "B"), "Em": ("E", "G", "B")}


def hz(nom, octave):
    return 440.0 * 2 ** ((DEMI[nom] - 9) / 12 + (octave - 4))


def _pose(buf, y, t0, g=1.0, pan=0.0):
    i = int(t0 * SRM)
    if i >= len(buf) or i < 0:
        return
    y, a = y[: len(buf) - i], (pan + 1) * np.pi / 4
    buf[i:i + len(y), 0] += y * g * np.cos(a); buf[i:i + len(y), 1] += y * g * np.sin(a)


def _kick():
    tt = _t(0.32, SRM)
    return np.sin(_glisse_freq(46 + 100 * np.exp(-tt * 30), SRM)) * np.exp(-tt * 9)


def _grain(d, bas, haut, chute, graine):
    n = int(d * SRM)
    return _bruit(n, bas, haut, SRM, graine) * np.exp(-np.arange(n) / SRM * chute)


def _nappe(noms, octave, d):
    tt = _t(d, SRM)
    y = sum(np.sin(2 * np.pi * hz(n, octave) * (1 + e) * tt) for n in noms for e in (-0.003, 0.003)) / (2 * len(noms))
    a, r = int(0.6 * SRM), int(0.7 * SRM)
    y[:a] *= np.linspace(0, 1, a) ** 2; y[-r:] *= np.linspace(1, 0, r) ** 2
    return y


def _entrain(buf, t0, T, acc, m):
    f, t, q = ACC[acc]
    for k, (n, o) in enumerate([(f, 4), (q, 4), (t, 5), (q, 4), (f, 5), (q, 4), (t, 5), (q, 4)]):
        _pose(buf, _note(hz(n, o), 0.6, SRM, MARIMBA), t0 + k * T / 2, 0.20 if k % 2 == 0 else 0.15, 0.25 if k % 2 == 0 else -0.35)
    for k in (0, 1.5, 2):
        _pose(buf, _note(hz(f, 2), 0.5, SRM, BASSE), t0 + k * T, 0.34)
    for k in (0, 2):
        _pose(buf, _kick(), t0 + k * T, 0.40)
    for k in (1, 3):
        _pose(buf, _grain(0.14, 900, 4200, 38, m * 10 + k), t0 + k * T, 0.09, 0.1)
    for k in range(8):
        _pose(buf, _grain(0.07, 5000, 12000, 70, m * 20 + k), t0 + k * T / 2, 0.03 if k % 2 == 0 else 0.055, 0.5)
    if m % 8 >= 4:
        _pose(buf, _nappe((f, t, q), 4, 4 * T + 0.5), t0, 0.07)


def _douce(buf, t0, T, acc, m):
    f, t, q = ACC[acc]
    _pose(buf, _nappe((f, t, q), 3, 4 * T + 0.6), t0, 0.16)
    for k, (n, o) in enumerate([(f, 4), (q, 4), (t, 5), (q, 4)]):
        _pose(buf, _note(hz(n, o), 1.4, SRM, PIANO), t0 + k * T, 0.17 if k == 0 else 0.12, -0.2 + 0.13 * k)
    _pose(buf, _note(hz(f, 2), 1.6, SRM, BASSE), t0, 0.26)
    for k in (1, 3):
        _pose(buf, _grain(0.08, 5000, 11000, 60, m * 10 + k), t0 + k * T, 0.03, 0.4)


def _suspense(buf, t0, T, acc, m):
    f, t, q = ACC[acc]
    for k, (n, o) in enumerate([(f, 2), None, (f, 2), (q, 2), (f, 2), None, (t, 3), (q, 2)]):
        if n:
            _pose(buf, _note(hz(n, o), 0.3, SRM, PIZZ), t0 + k * T / 2, 0.36, -0.1)
    for k in (1, 3):
        _pose(buf, _grain(0.06, 1800, 6000, 90, m * 10 + k), t0 + k * T, 0.13, 0.2)
    for k in range(8):
        _pose(buf, _grain(0.03, 7000, 12000, 160, m * 20 + k), t0 + k * T / 2, 0.022, 0.5)
    if m % 2 == 1:
        for k, (n, o) in enumerate([(t, 5), (f, 5), (q, 4)]):
            _pose(buf, _note(hz(n, o), 0.5, SRM, MARIMBA), t0 + (2.5 + k * 0.5) * T, 0.13, 0.35)


def _fete(buf, t0, T, acc, m):
    f, t, q = ACC[acc]
    for k, (n, o) in enumerate([(f, 5), (t, 5), (q, 5), (t, 5), (f, 6), (q, 5), (t, 5), (q, 5)]):
        _pose(buf, _note(hz(n, o), 0.5, SRM, MARIMBA), t0 + k * T / 2, 0.17, 0.3 if k % 2 == 0 else -0.3)
    for k in range(4):
        _pose(buf, _kick(), t0 + k * T, 0.34)
        _pose(buf, _note(hz(f, 2), 0.3, SRM, BASSE), t0 + (k + 0.5) * T, 0.28)
    for k in (1, 3):
        _pose(buf, _grain(0.14, 900, 4200, 38, m * 10 + k), t0 + k * T, 0.13, 0.1)
    for k in range(16):
        _pose(buf, _grain(0.05, 6000, 12000, 90, m * 40 + k), t0 + k * T / 4, 0.02 if k % 2 == 0 else 0.035, 0.5)


MUSIQUES = {
    "entrain": {"bpm": 104, "accords": ["C", "G", "Am", "F"], "jeu": _entrain},         # enjouée : marimba, basse, percussions légères
    "douce": {"bpm": 76, "accords": ["F", "Am", "Dm", "C"], "jeu": _douce},             # calme : piano doux et nappe
    "suspense": {"bpm": 100, "accords": ["Am", "Am", "F", "E"], "jeu": _suspense},      # à pas de loup : cordes pincées, claquements de doigts
    "fete": {"bpm": 124, "accords": ["C", "F", "G", "C"], "jeu": _fete},                # festive : rythme marqué, claquements de mains
}


def musique(nom, duree, niveau=0.03):
    """Musique de fond de `duree` secondes, ramenée à un niveau moyen fixe (la voix passera toujours devant)."""
    if nom not in MUSIQUES:
        raise KeyError(nom)
    spec, n = MUSIQUES[nom], int(duree * SRM)
    T = 60 / spec["bpm"]
    buf = np.zeros((n, 2))
    for m in range(int(np.ceil(duree / (4 * T))) + 1):
        spec["jeu"](buf, m * 4 * T, T, spec["accords"][m % len(spec["accords"])], m)
    buf *= niveau / (np.sqrt(np.mean(buf ** 2)) + 1e-9)
    a, r = min(n, int(0.25 * SRM)), min(n, int(1.4 * SRM))
    buf[:a] *= np.linspace(0, 1, a)[:, None]; buf[-r:] *= (np.linspace(1, 0, r) ** 1.5)[:, None]
    return np.clip(buf, -0.95, 0.95).astype(np.float32)


if __name__ == "__main__":
    import pathlib, soundfile as sf
    d = pathlib.Path(__file__).resolve().parent / "echantillons"; d.mkdir(exist_ok=True)
    for nom in EFFETS:
        e = effet(nom); sf.write(d / f"bruitage-{nom}.wav", e, SR)
        print(f"{nom:10s} {len(e) / SR:5.2f} s  crête {np.max(np.abs(e)):.3f}")
    for nom in MUSIQUES:
        m = musique(nom, 20); sf.write(d / f"musique-{nom}.wav", m, SRM)
        print(f"musique {nom:9s} crête {np.max(np.abs(m)):.3f}  moyenne {np.sqrt(np.mean(m ** 2)):.3f}")
    print("Échantillons dans", d)
