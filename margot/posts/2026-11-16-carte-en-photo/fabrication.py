#!/usr/bin/env python3
"""Carrousel « Retaper votre carte ? Une photo suffit. » du 16/11/2026 : 5 images 1080 × 1350 qui annoncent la nouveauté du site
— le restaurateur importe une photo, une image ou un PDF de sa carte, le site la lit en quelques secondes, il relit et publie.
Faits donnés par Owen le 16/11/2026 ; offre lue le même jour sur /tarifs (« Gratuit pendant le lancement, sans carte bancaire »).

python3 fabrication.py   →   1.jpg … 5.jpg et planche.jpg, dans ce dossier.
Les illustrations sont celles des Reels : ../../kit/illustration.py les fabrique (dossier img/, refait s'il manque).
La carte en papier et l'écran du téléphone sont des exemples dessinés (ils portent le mot « Exemple ») : l'espace du restaurateur
n'est pas public, on ne montre donc pas de capture de l'outil.
"""
import base64, pathlib, subprocess, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
KIT = ICI.parent.parent / "kit"
ILLUSTRATIONS = {                                                          # nom du fichier → options de illustration.py
    "tel-carte": ["--telephone", "carte", "--largeur", "640"],
    "tel-corrige": ["--element", '{"type": "telephone", "son": false, "ecran": {"type": "carte", "defile": false, "change": {"plat": "Bavette", "prix": "19 €", "quand": 0.5}}}', "--largeur", "640"],
    "chef-tel": ["--personnage", "chef", "--expression", "joie", "--objet", "telephone", "--fond", "prune", "--largeur", "480"],
    "m-pointe": ["--margot", "--pose", "pointe", "--expression", "joie", "--regard", "droite", "--largeur", "640"],
    "m-pouce": ["--margot", "--pose", "pouce", "--expression", "joie", "--largeur", "640"],
    "m-fete-disque": ["--margot", "--pose", "fete", "--expression", "joie", "--disque", "creme", "--largeur", "640"],
    "photo": ["--icone", "photo", "--disque", "or", "--couleur", "fonce", "--largeur", "300"],
    "eclair": ["--icone", "eclair", "--disque", "prune", "--couleur", "creme", "--largeur", "300"],
    "coche": ["--icone", "coche", "--disque", "prune", "--couleur", "creme", "--largeur", "300"],
}
_polices = [KIT / "node_modules/@fontsource/fraunces/files/fraunces-latin-900-normal.woff2", pathlib.Path("/home/claude/insta/node_modules/@fontsource/fraunces/files/fraunces-latin-900-normal.woff2")]
_police = next((p for p in _polices if p.exists()), None)                  # sans Fraunces (npm i @fontsource/fraunces dans kit/), les titres passent en Georgia
POLICE = base64.b64encode(_police.read_bytes()).decode() if _police else ""
TH = {
    "creme": dict(fond="#FBF3EC", titre="#5A1F4A", acc="color:#3D1030;background:#EBBE72", tagf="#EBBE72", tagt="#3D1030", texte="rgba(61,16,48,.84)", deco="rgba(235,190,114,.28)", trait="#5A1F4A"),
    "prune": dict(fond="#5A1F4A", titre="#FBF3EC", acc="color:#EBBE72", tagf="#EBBE72", tagt="#3D1030", texte="rgba(251,243,236,.9)", deco="rgba(255,255,255,.06)", trait="#EBBE72"),
    "or": dict(fond="#EBBE72", titre="#3D1030", acc="color:#FBF3EC;background:#5A1F4A", tagf="#5A1F4A", tagt="#FBF3EC", texte="rgba(61,16,48,.88)", deco="rgba(255,255,255,.24)", trait="#5A1F4A"),
}
N = 5


def page(th, titre, corps="", rang=None, taille=108, haut_texte=424):
    t = TH[th]
    tag = "Nouveau" + (f" · {rang}/{N}" if rang else "")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:900;src:url(data:font/woff2;base64,{POLICE})}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;background:{t['fond']};font-family:Inter,"Helvetica Neue",Arial,sans-serif}}
.deco{{position:absolute;border-radius:50%;background:{t['deco']}}}
.tag{{position:absolute;left:0;right:0;top:62px;text-align:center}}
.tag span{{display:inline-block;font-weight:700;font-size:30px;padding:10px 28px;border-radius:999px;background:{t['tagf']};color:{t['tagt']}}}
h1{{position:absolute;left:50px;right:50px;top:150px;text-align:center;font-family:Fraunces,Georgia,serif;font-weight:900;font-size:{taille}px;line-height:1.06;letter-spacing:-1.5px;color:{t['titre']}}}
.acc{{padding:0 .12em;border-radius:.14em;{t['acc']}}}
p.t{{position:absolute;left:84px;right:84px;top:{haut_texte}px;text-align:center;font-weight:600;font-size:45px;line-height:1.32;color:{t['texte']}}}
img{{position:absolute;display:block}}
.papier{{position:absolute;width:340px;padding:24px 26px 16px;background:#FFFDF8;border-radius:6px;box-shadow:0 14px 30px rgba(42,10,32,.24);color:#3D1030;font-family:Georgia,"Times New Roman",serif}}
.papier b{{display:block;text-align:center;font-family:Fraunces,Georgia,serif;font-weight:900;font-size:34px;margin-bottom:6px}}
.papier i{{display:block;font-size:20px;margin:12px 0 4px;color:#8A5A2B;border-bottom:1px solid #E8DCCD}}
.papier p{{display:flex;justify-content:space-between;gap:10px;font-size:19px;line-height:1.55}}
.papier small{{display:block;text-align:center;margin-top:10px;font-family:Inter,sans-serif;font-weight:700;font-size:17px;opacity:.7}}
.coin{{position:absolute;width:58px;height:58px;border:10px solid #EBBE72}}
.pastille{{position:absolute;font-weight:700;font-size:30px;padding:10px 26px;border-radius:999px;background:#EBBE72;color:#3D1030;white-space:nowrap}}
.site{{position:absolute;left:0;right:0;bottom:44px;text-align:center;font-weight:600;font-size:30px;color:{t['texte']}}}
.bouton{{position:absolute;left:50%;transform:translateX(-50%);font-weight:800;font-size:50px;padding:22px 64px;border-radius:999px;background:#EBBE72;color:#3D1030;box-shadow:0 12px 26px rgba(42,10,32,.28);white-space:nowrap}}
</style></head><body>
<div class="deco" style="left:-250px;top:-270px;width:620px;height:620px"></div><div class="deco" style="right:-210px;bottom:-230px;width:560px;height:560px"></div>
<div class="tag"><span>{tag}</span></div>
<h1>{titre}</h1>{f'<p class="t">{corps}</p>' if corps else ''}
"""


def img(nom, gauche, largeur, bas=None, haut=None):
    place = f"bottom:{1350 - bas}px" if bas is not None else f"top:{haut}px"
    return f'<img src="img/{nom}.png" style="left:{gauche}px;width:{largeur}px;{place}">'


def papier(gauche, haut, angle=-5, echelle=1.0):
    """La carte en papier du restaurant : un exemple dessiné, avec les mêmes plats que l'écran du téléphone."""
    return f"""<div class="papier" style="left:{gauche}px;top:{haut}px;transform:rotate({angle}deg) scale({echelle});transform-origin:0 0"><b>La carte</b>
<i>Entrées</i><p><span>Œuf mayonnaise</span><em>6 €</em></p><p><span>Soupe du jour</span><em>7 €</em></p>
<i>Plats</i><p><span>Bavette, frites maison</span><em>18 €</em></p><p><span>Poisson du marché</span><em>19 €</em></p><p><span>Risotto aux champignons</span><em>16 €</em></p>
<i>Desserts</i><p><span>Tarte du jour</span><em>7 €</em></p><p><span>Mousse au chocolat</span><em>7 €</em></p>
<small>Exemple</small></div>"""


def viseur(gauche, haut, largeur, hauteur):
    """Les quatre coins d'un cadrage d'appareil photo."""
    c = lambda x, y, bords: f'<div class="coin" style="left:{x}px;top:{y}px;border-{bords[0]}:0;border-{bords[1]}:0"></div>'
    return (c(gauche, haut, ("right", "bottom")) + c(gauche + largeur - 58, haut, ("left", "bottom"))
            + c(gauche, haut + hauteur - 58, ("right", "top")) + c(gauche + largeur - 58, haut + hauteur - 58, ("left", "top")))


def fleche(gauche, haut, largeur, couleur):
    return (f'<svg style="position:absolute;left:{gauche}px;top:{haut}px" width="{largeur}" height="{largeur * 0.6:.0f}" viewBox="0 0 200 120" fill="none" stroke="{couleur}" stroke-width="13" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M12 92 C52 22 128 16 182 62"/><path d="M146 56 L184 64 L180 26"/></svg>')


A = lambda m: f'<span class="acc">{m}</span>'
PAGES = [
    page("creme", f"Retaper<br>votre carte&nbsp;?<br>{A('Une photo suffit')}", "Vous la prenez en photo,<br>le site la remplit pour vous.", taille=104, haut_texte=506)
    + papier(52, 730, -6, 0.9) + fleche(404, 716, 190, "#5A1F4A") + img("photo", 440, 124, haut=846) + img("tel-carte", 640, 336, bas=1314) + img("m-pointe", 356, 280, bas=1316),

    page("prune", f"1. Prenez-la<br>{A('en photo')}", "Avec votre téléphone, depuis votre espace. Une image déjà enregistrée ou un PDF, ça marche aussi.", 2)
    + papier(120, 716, -4, 1.0) + viseur(76, 672, 430, 560) + img("photo", 404, 150, haut=626) + img("chef-tel", 640, 318, bas=1306),

    page("or", f"2. Le site<br>{A('la lit pour vous')}", "En quelques secondes, votre carte<br>se remplit toute seule.", 3)
    + papier(64, 700, -6, 0.92) + fleche(404, 760, 220, "#5A1F4A") + img("eclair", 448, 132, haut=900) + img("tel-carte", 640, 350, bas=1314),

    page("creme", f"3. Vous relisez,<br>{A('vous publiez')}", "Corrigez un nom ou un prix si besoin, puis mettez votre carte en ligne.", 4, taille=100)
    + img("tel-corrige", 612, 372, bas=1318) + img("m-pouce", 70, 440, bas=1306) + img("coche", 468, 134, haut=720)
    + '<div class="pastille" style="left:724px;top:578px">Exemple</div>',

    page("prune", f"Créez<br>{A('votre carte')}", "Gratuit pendant le lancement,<br>sans carte bancaire.", taille=124, haut_texte=440)
    + '<div class="bouton" style="top:596px">Lien en bio</div>' + img("m-fete-disque", 310, 460, haut=770)
    + '<div class="site">restaurant-site-internet.fr</div>',
]


def main():
    (ICI / "img").mkdir(exist_ok=True)
    for nom, options in ILLUSTRATIONS.items():
        if not (ICI / "img" / f"{nom}.png").exists():
            subprocess.run([sys.executable, str(KIT / "illustration.py"), str(ICI / "img" / f"{nom}.png"), *options], check=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome") if pathlib.Path("/usr/bin/google-chrome").exists() else pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, h in enumerate(PAGES, 1):
            f = ICI / f"page{k}.html"; f.write_text(h + "</body></html>", encoding="utf-8")
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(ICI / f"{k}.png")); f.unlink()
            Image.open(ICI / f"{k}.png").convert("RGB").save(ICI / f"{k}.jpg", quality=95)
            (ICI / f"{k}.png").unlink()
        b.close()
    L, H = 432, 540
    pl = Image.new("RGB", (N * (L + 8), H), "white")
    for k in range(N):
        pl.paste(Image.open(ICI / f"{k + 1}.jpg").resize((L, H), Image.LANCZOS), (k * (L + 8), 0))
    pl.save(ICI / "planche.jpg", quality=86); print("planche :", pl.size)


if __name__ == "__main__":
    main()
