#!/usr/bin/env python3
"""Carrousel « Je ne suis plus seule ! » du 16/11/2026 : 7 images 1080 × 1350 qui présentent la nouvelle image des vidéos de Margot
(personnages, une illustration par conseil, la page d'exemple du site dans le téléphone, la série « Margot vous répond »).

python3 fabrication.py   →   1.jpg … 7.jpg et planche.jpg, dans ce dossier.
Les illustrations sont celles des Reels : elles sont fabriquées par ../../kit/illustration.py (dossier img/, refait s'il manque).
Ce fichier sert aussi de modèle pour un carrousel fait à la main : une page HTML par image, capturée avec Playwright.
"""
import base64, pathlib, subprocess, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
KIT = ICI.parent.parent / "kit"
PAGE_SITE = (KIT / "specs" / "images" / "page-haut.png").as_uri()          # la page de démonstration du site, lue le 15/11/2026
ILLUSTRATIONS = {                                                          # nom du fichier → options de illustration.py
    "m-fete": ["--margot", "--pose", "fete", "--expression", "joie", "--largeur", "760"],
    "m-pointe": ["--margot", "--pose", "pointe", "--expression", "joie", "--regard", "droite", "--largeur", "640"],
    "m-pointe-disque": ["--margot", "--pose", "pointe", "--expression", "joie", "--regard", "droite", "--disque", "creme", "--largeur", "560"],
    "m-surprise-disque": ["--margot", "--pose", "hanche", "--expression", "surprise", "--regard", "droite", "--disque", "creme", "--largeur", "560"],
    "m-bonjour": ["--margot", "--pose", "bonjour", "--expression", "joie", "--largeur", "760"],
    "c-chef": ["--personnage", "chef", "--expression", "joie", "--largeur", "440"],
    "c-cheffe": ["--personnage", "cheffe", "--expression", "joie", "--objet", "carte", "--largeur", "440"],
    "p-chef": ["--personnage", "chef", "--expression", "doute", "--fond", "prune", "--largeur", "460"],
    "p-cheffe": ["--personnage", "cheffe", "--expression", "joie", "--objet", "telephone", "--fond", "prune", "--largeur", "460"],
    "p-serveur": ["--personnage", "serveur", "--expression", "joie", "--objet", "plateau", "--fond", "prune", "--largeur", "480"],
    "o-client": ["--personnage", "client", "--expression", "joie", "--objet", "telephone", "--fond", "or", "--largeur", "460"],
    "o-cliente": ["--personnage", "cliente", "--expression", "doute", "--fond", "or", "--regard", "gauche", "--largeur", "460"],
    "o-chef-colere": ["--personnage", "chef", "--expression", "colere", "--fond", "or", "--regard", "gauche", "--largeur", "500"],
    "pates": ["--plat", "pates", "--disque", "prune", "--badge", "photo", "--largeur", "420"],
    "euro": ["--icone", "euro", "--disque", "prune", "--couleur", "creme", "--largeur", "380"],
    "qr": ["--icone", "qr", "--disque", "prune", "--couleur", "creme", "--largeur", "380"],
    "tel": ["--element", '{"type": "telephone", "son": false, "ecran": {"type": "image", "src": "%s", "defile": false}}' % PAGE_SITE, "--fond", "prune", "--largeur", "620"],
}
_polices = [KIT / "node_modules/@fontsource/fraunces/files/fraunces-latin-900-normal.woff2", pathlib.Path("/home/claude/insta/node_modules/@fontsource/fraunces/files/fraunces-latin-900-normal.woff2")]
_police = next((p for p in _polices if p.exists()), None)                  # sans Fraunces (npm i @fontsource/fraunces dans kit/), les titres passent en Georgia
POLICE = base64.b64encode(_police.read_bytes()).decode() if _police else ""
TH = {
    "creme": dict(fond="#FBF3EC", titre="#5A1F4A", acc="color:#3D1030;background:#EBBE72", tagf="#EBBE72", tagt="#3D1030", texte="rgba(61,16,48,.84)", deco="rgba(235,190,114,.28)"),
    "prune": dict(fond="#5A1F4A", titre="#FBF3EC", acc="color:#EBBE72", tagf="#EBBE72", tagt="#3D1030", texte="rgba(251,243,236,.9)", deco="rgba(255,255,255,.06)"),
    "or": dict(fond="#EBBE72", titre="#3D1030", acc="color:#FBF3EC;background:#5A1F4A", tagf="#5A1F4A", tagt="#FBF3EC", texte="rgba(61,16,48,.88)", deco="rgba(255,255,255,.24)"),
}
N = 7


def page(th, titre, corps="", rang=None, taille=108, haut_texte=424):
    t = TH[th]
    tag = "Du nouveau chez Margot" + (f" · {rang}/{N}" if rang else "")
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
.bulle{{position:absolute;background:#fff;color:#3D1030;font-weight:600;font-size:38px;line-height:1.25;padding:22px 30px;border-radius:30px;box-shadow:0 10px 24px rgba(42,10,32,.16)}}
.bulle{{white-space:nowrap}}
.bulle:after{{content:"";position:absolute;bottom:-22px;left:var(--q,54px);width:0;height:0;border:24px solid transparent;border-top-color:#fff;border-bottom:0}}
p.g{{position:absolute;font-weight:600;font-size:44px;line-height:1.32;color:{t['texte']}}}
.tagn{{display:none}}
.pastille{{position:absolute;font-weight:700;font-size:30px;padding:10px 26px;border-radius:999px;background:#EBBE72;color:#3D1030}}
.bouton{{position:absolute;left:50%;transform:translateX(-50%);font-weight:800;font-size:54px;padding:24px 70px;border-radius:999px;background:#5A1F4A;color:#FBF3EC;box-shadow:0 12px 26px rgba(42,10,32,.22);white-space:nowrap}}
</style></head><body>
<div class="deco" style="left:-250px;top:-270px;width:620px;height:620px"></div><div class="deco" style="right:-210px;bottom:-230px;width:560px;height:560px"></div>
<div class="tag"><span>{tag}</span></div>
<h1>{titre}</h1>{f'<p class="t">{corps}</p>' if corps else ''}
"""


def img(nom, gauche, largeur, bas=None, haut=None):
    place = f"bottom:{1350 - bas}px" if bas is not None else f"top:{haut}px"
    return f'<img src="img/{nom}.png" style="left:{gauche}px;width:{largeur}px;{place}">'


A = lambda m: f'<span class="acc">{m}</span>'
PAGES = [
    page("creme", f"Je ne suis<br>plus {A('seule')}&nbsp;!", "Du nouveau dans mes vidéos<br>pour les restaurateurs", taille=126, haut_texte=470)
    + img("c-cheffe", 22, 262, bas=1306) + img("c-chef", 800, 262, bas=1306) + img("m-fete", 262, 556, bas=1300),

    page("prune", f"Le chef,<br>{A('c’est vous')}", "Un chef, une cheffe, un serveur&nbsp;: ils jouent vos journées. Le service à préparer, le téléphone qui sonne, la carte à changer.", 2)
    + img("p-chef", 56, 292, bas=1306) + img("p-cheffe", 384, 292, bas=1306) + img("p-serveur", 696, 346, bas=1306),

    page("or", f"Vos clients<br>{A('aussi')}", "Ils cherchent une table, demandent ce qu’il y a dans un plat, regardent votre carte avant de venir.", 3)
    + img("o-client", 120, 300, bas=1306) + img("o-cliente", 650, 300, bas=1306)
    + '<div class="bulle" style="left:392px;top:650px;--q:384px">Il y a des fruits à coque&nbsp;?</div>',

    page("creme", f"Un conseil,<br>{A('une image')}", "Une photo de plat, un prix, un QR code&nbsp;: chaque geste se montre. Vous voyez tout de suite quoi faire.", 4)
    + img("m-pointe", 30, 470, haut=836) + img("pates", 628, 330, haut=660) + img("euro", 524, 250, haut=1012) + img("qr", 796, 250, haut=1012),

    page("prune", f"À quoi ressemble<br>{A('une page&nbsp;?')}", rang=5, taille=100)
    + '<p class="g" style="left:76px;top:436px;width:470px">Quand je parle du site, je vous montre une page d’exemple&nbsp;: la carte, les prix, les horaires.</p>'
    + img("tel", 596, 428, bas=1316) + img("m-pointe-disque", 106, 384, haut=900) + '<div class="pastille" style="left:176px;top:816px">Page d’exemple</div>',

    page("or", f"Nouvelle série&nbsp;:<br>{A('Margot vous répond')}", "Une objection de restaurateur<br>par épisode. Le premier est en ligne&nbsp;:<br>«&nbsp;Un site&nbsp;? Pas le temps.&nbsp;»", 6, taille=92, haut_texte=400)
    + img("m-surprise-disque", 60, 400, haut=884) + img("o-chef-colere", 724, 270, bas=1306)
    + '<div class="bulle" style="left:330px;top:636px;--q:505px">J’ai un service à préparer&nbsp;!</div>',

    page("creme", f"Abonnez-vous<br>pour {A('la suite')}", taille=118)
    + '<div class="bouton" style="top:476px">S’abonner</div>' + img("m-bonjour", 244, 592, bas=1300),
]


def main():
    (ICI / "img").mkdir(exist_ok=True)
    for nom, options in ILLUSTRATIONS.items():
        if not (ICI / "img" / f"{nom}.png").exists():
            subprocess.run([sys.executable, str(KIT / "illustration.py"), str(ICI / "img" / f"{nom}.png"), *options], check=True)
    sortie = ICI
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome"); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, h in enumerate(PAGES, 1):
            f = ICI / f"page{k}.html"; f.write_text(h + "</body></html>", encoding="utf-8")
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(sortie / f"{k}.png")); f.unlink()
            Image.open(sortie / f"{k}.png").convert("RGB").save(sortie / f"{k}.jpg", quality=95)
            (sortie / f"{k}.png").unlink()
        b.close()
    L, H = 432, 540
    pl = Image.new("RGB", (4 * (L + 8), 2 * (H + 8)), "white")
    for k in range(N):
        pl.paste(Image.open(sortie / f"{k + 1}.jpg").resize((L, H), Image.LANCZOS), ((k % 4) * (L + 8), (k // 4) * (H + 8)))
    pl.save(ICI / "planche.jpg", quality=86); print("planche :", pl.size)


if __name__ == "__main__":
    main()
