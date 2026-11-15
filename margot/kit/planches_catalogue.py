#!/usr/bin/env python3
"""Refait les images du dossier catalogue/ : tout ce que Margot et le moteur savent montrer, en un coup d'œil.

Usage : python3 planches_catalogue.py
Les listes (poses, expressions, icônes, écrans…) sont lues dans les fichiers du moteur : une possibilité ajoutée
apparaît d'elle-même sur sa planche. À relancer après chaque ajout, puis regarder les images.
"""
import json, pathlib, re, subprocess, sys, tempfile
from PIL import Image

ICI = pathlib.Path(__file__).resolve().parent
lire = lambda f: (ICI / "page" / f).read_text(encoding="utf-8")


def cles(source, nom):
    """Les clés d'un objet « const NOM = { … } » écrit sur plusieurs lignes."""
    bloc = re.search(rf"const {nom} = \{{\n(.*?)\n\}};", source, re.S).group(1)
    return re.findall(r"^  ([a-z_]+)[:(]", bloc, re.M)


def grille(noms, cols, fabrique, y0, dy, taille, etiquettes=None):
    els = []
    for k, n in enumerate(noms):
        x, y = 1080 * (k % cols + 0.5) / cols, y0 + dy * (k // cols)
        els.append(dict(type="margot", x=x + 71 * taille, y=y, taille=taille, entree="aucune", disque=False, **fabrique(n)))
        els.append(dict(type="texte", x=x, y=y + 330 * taille + 26, taille=28, l=1080 // cols, texte=(etiquettes or noms)[k], quand=0, entree="aucune", zone=False))
    return els


def titre(t):
    return dict(type="texte", x=540, y=210, taille=44, texte=t, quand=0, entree="aucune", zone=False)


def main():
    m, o, tel, plans = lire("02_margot.js"), lire("01_outils.js"), lire("04_telephone.js"), lire("05_plans.js")
    poses, gauches, exprs = cles(m, "POSES"), [g for g in cles(m, "BRASG") if g != "repos"], cles(m, "EXPR")
    accs = ["masque", "lunettes", "casque"] + cles(m, "CHAPEAUX")
    icones, ecrans, decors = cles(o, "ICONES"), cles(tel, "ECRANS"), ["ville"] + [d for d in cles(plans, "DECORS") if d != "ville"]
    doubles = re.findall(r"(\w+): \{droite", re.search(r"const DOUBLE = \{(.*?)\};", m).group(1))
    libre = dict(plan="libre", fond="creme", duree=1.2, cercles=False)
    scenes, noms = [], []

    def planche(nom, elements, **plus):
        scenes.append({**libre, **plus, "elements": elements}); noms.append(nom)

    lp = poses + [d for d in doubles if d not in poses] + [f"gauche-{g}" for g in gauches]
    planche("poses", [titre("Poses de Margot")] + grille(
        lp, 4, lambda n: dict(pose={"gauche": n[7:], "droite": "repos"} if n.startswith("gauche-") else n, panneau="-10 %"), 400, 250, 0.3,
        [n.replace("gauche-", "gauche : ") for n in lp]))
    planche("expressions", [titre("Expressions")] + grille(exprs, 3, lambda n: dict(expression=n, pose="repos"), 470, 400, 0.42))
    planche("accessoires", [titre("Accessoires")] + grille(accs, 3, lambda n: dict(accessoire=n, pose="repos"), 500, 420, 0.42))
    els = [titre("Icônes")]
    for k, n in enumerate(icones):
        x, y = 1080 * (k % 6 + 0.5) / 6, 340 + 168 * (k // 6)
        els += [dict(type="icone", nom=n, x=x, y=y, taille=88, quand=0, entree="aucune"), dict(type="texte", x=x, y=y + 68, taille=20, l=180, texte=n, quand=0, entree="aucune", zone=False)]
    planche("icones", els)
    for p in range(0, len(ecrans), 3):
        els = [titre("Écrans du téléphone")]
        for k, n in enumerate(ecrans[p:p + 3]):
            x = 1080 * (k + 0.5) / 3
            ec = dict(type=n, defile=False, **({"note": 4.6, "avis": 128, "manque": "Carte"} if n == "fiche" else {}), **({"src": str(ICI / "catalogue" / "poses.jpg")} if n == "image" else {}))
            els += [dict(type="telephone", x=x, y=900, taille=0.7, quand=0, entree="aucune", ecran=ec, zone=False, son=False),
                    dict(type="texte", x=x, y=1270, taille=30, l=330, texte=n, couleur="creme", quand=0, entree="aucune", zone=False)]
        planche(f"ecrans-{p // 3 + 1}", els, fond="prune", duree=3.2)
    # Personnages et plats
    pp = lire("03b_personnages.js")
    roles, plats = re.findall(r'"(\w+)"', re.search(r"const ROLES = \[(.*?)\];", pp).group(1)), cles(pp, "PLATS")
    pex = re.findall(r"(\w+): \{", re.search(r"const PEXPR = \{\n(.*?)\n\};", pp, re.S).group(1))
    els = [titre("Personnages")]

    def rang(liste, y, taille, fabrique, etiquettes):
        for k, n in enumerate(liste):
            x = 1080 * (k + 0.5) / len(liste)
            els.append(dict(type="personnage", x=x, y=y, taille=taille, quand=0, entree="aucune", zone=False, **fabrique(n)))
            els.append(dict(type="texte", x=x, y=y + 0.78 * taille + 34, taille=26, l=1080 // len(liste), texte=etiquettes[k], quand=0, entree="aucune", zone=False))

    rang(roles, 500, 186, lambda n: dict(role=n), roles)
    rang(pex, 890, 150, lambda n: dict(role="client", expression=n), [f"expression : {n}" for n in pex])
    rang(["telephone", "carte", "plateau", "clair", "mat", "fonce"], 1250, 150,
         lambda n: dict(role="serveur" if n == "plateau" else "cliente", objet=n) if n in ("telephone", "carte", "plateau") else dict(role="chef", teint=n),
         ["objet : telephone", "objet : carte", "objet : plateau", "teint : clair", "teint : mat", "teint : fonce"])
    planche("personnages", els)
    els = [titre("Plats illustrés")]
    for k, n in enumerate(plats):
        x, y = 1080 * (k % 3 + 0.5) / 3, 440 + 300 * (k // 3)
        els += [dict(type="plat", nom=n, x=x, y=y, taille=210, quand=0, entree="aucune", zone=False), dict(type="texte", x=x, y=y + 138, taille=28, l=340, texte=n, quand=0, entree="aucune", zone=False)]
    planche("plats", els)
    for d in decors:
        planche(f"decor-{d}", [dict(type="texte", x=540, y=900, taille=90, texte=d, quand=0, entree="aucune", zone=False)], decor=d, cercles=True, fond="creme" if len(noms) % 2 else "prune")

    sortie = ICI / "catalogue"; sortie.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "PLANCHES.json").write_text(json.dumps({"etiquette": "", "bruitages": False, "soustitres": "aucun", "scenes": scenes}, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ICI / "reel.py"), str(tmp / "PLANCHES.json"), str(tmp / "x.mp4"), "--apercu=1"], capture_output=True, text=True)
        for ligne in r.stdout.splitlines():
            if "ALERTE" in ligne and "dépasse" not in ligne and "trop " not in ligne:
                print(ligne)
        if r.returncode:
            raise SystemExit(r.stderr[-800:])
        vues = {n: Image.open(tmp / "apercu" / f"s{k + 1}a.jpg").convert("RGB") for k, n in enumerate(noms)}
    for n, im in vues.items():
        if not n.startswith("decor-"):
            im.resize((720, 1280), Image.LANCZOS).save(sortie / f"{n}.jpg", quality=86)
    dd = [n for n in vues if n.startswith("decor-")]
    w, h, cols = 270, 480, 4
    pl = Image.new("RGB", (w * cols, h * -(-len(dd) // cols)), "#FBF3EC")
    for k, n in enumerate(dd):
        pl.paste(vues[n].resize((w - 4, h - 4), Image.LANCZOS), ((k % cols) * w + 2, (k // cols) * h + 2))
    pl.save(sortie / "decors.jpg", quality=86)
    print("Images dans", sortie, ":", ", ".join(sorted(p.name for p in sortie.glob("*.jpg"))))


if __name__ == "__main__":
    main()
