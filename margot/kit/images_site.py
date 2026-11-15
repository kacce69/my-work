#!/usr/bin/env python3
"""Récupère les images publiques de restaurant-site-internet.fr pour les montrer dans un Reel, un post ou un carrousel.

Usage :
  python3 images_site.py /exemples                                   liste les images de la page
  python3 images_site.py /exemples --prendre 1,3 --vers /tmp/images  télécharge les images n° 1 et 3 (ou --prendre tout)
  python3 images_site.py /exemples --capture /tmp/images/page.png    capture de la page entière, largeur d'un téléphone
                                                                      (--largeur 390 par défaut, 1200 pour un écran d'ordinateur ;
                                                                      --hauteur 2400 ne garde que le haut de la page)

Tout passe par le lecteur de veille du site (curl -A "rcs-veille (monitor)") : il ne compte pas dans les statistiques de
visites. La capture ne visite pas la page avec un navigateur : la page est reconstituée ici, à partir de son code et de sa
feuille de style, sans ses scripts (donc sans bandeau ni fenêtre surgissante) ; ce qu'un script ajoute à la page n'y figure pas.

Les pages de démonstration du site (/exemples et /exemple/…) sont les siennes : ce sont elles qu'on montre de préférence.
Sur la page d'un vrai restaurant, les images du dossier /uploads/ sont les photos déposées par le restaurateur : elles lui
appartiennent. Avant d'en montrer une dans une publication, ou de montrer sa page, il faut son accord ; et jamais de photo
où l'on reconnaît une personne.
Dans un scénario : {"plan": "image", "image": {"src": "/tmp/images/photo.jpg"}} ou, dans le téléphone,
{"ecran": {"type": "image", "src": "/tmp/images/page.png"}}.
"""
import argparse, html, os, pathlib, re, subprocess, sys, urllib.parse

SITE = "https://restaurant-site-internet.fr"
LECTEUR = "rcs-veille (monitor)"


def lire(url, vers):
    """Télécharge une adresse du site avec le lecteur de veille. Renvoie le code de réponse."""
    if urllib.parse.urlparse(url).netloc != urllib.parse.urlparse(SITE).netloc:
        raise SystemExit(f"Adresse hors du site, non lue : {url}")
    r = subprocess.run(["curl", "-sS", "-m", "40", "-A", LECTEUR, "-o", str(vers), "-w", "%{http_code}", url], capture_output=True, text=True)
    return r.stdout.strip() or r.stderr.strip()[:80]


def images(page_html, base):
    """Les images d'une page, dans l'ordre : [(adresse, texte de remplacement)]."""
    vues, out = set(), []

    def ajoute(u, alt=""):
        u = urllib.parse.urljoin(base, html.unescape(u.strip()))
        if not u.startswith("data:") and u not in vues and urllib.parse.urlparse(u).netloc == urllib.parse.urlparse(SITE).netloc:
            vues.add(u); out.append((u, html.unescape(alt)))

    for m in re.finditer(r"<img\b[^>]*>", page_html):
        src, alt = re.search(r'\bsrc=["\']([^"\']+)', m.group()), re.search(r'\balt=["\']([^"\']*)', m.group())
        if src:
            ajoute(src.group(1), alt.group(1) if alt else "")
    for u in re.findall(r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page_html):
        ajoute(u, "image de partage")
    for u in re.findall(r'url\(["\']?([^"\')]+\.(?:png|jpe?g|webp|svg|gif)[^"\')]*)', page_html):
        ajoute(u)
    return out


def nom_local(url):
    return re.sub(r"[^A-Za-z0-9._-]", "_", pathlib.PurePosixPath(urllib.parse.urlparse(url).path).name) or "image"


def capture(url, page_html, sortie, largeur, hauteur=None):
    """Reconstitue la page dans un dossier (code, feuilles de style, polices, images) et la photographie sans réseau."""
    dossier = sortie.parent / (sortie.stem + "_page"); dossier.mkdir(parents=True, exist_ok=True)
    pris = {}

    def local(u, base):
        u = urllib.parse.urljoin(base, html.unescape(u.strip()))
        if u.startswith("data:") or urllib.parse.urlparse(u).netloc != urllib.parse.urlparse(SITE).netloc:
            return None
        if u not in pris:
            f = dossier / f"{len(pris):03d}_{nom_local(u)}"
            pris[u] = f.name if lire(u, f) == "200" else None
        return pris[u]

    def styles(css, base):                                    # les adresses d'une feuille de style (polices, fonds)
        return re.sub(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', lambda m: f'url("{local(m.group(1), base) or ""}")', css)

    t = re.sub(r"<script\b.*?</script>", "", page_html, flags=re.S | re.I)
    t = re.sub(r'\s(?:loading|srcset|sizes)=["\'][^"\']*["\']', "", t)

    def feuille(m):
        href = re.search(r'href=["\']([^"\']+)', m.group())
        if not href or "stylesheet" not in m.group():
            return "" if "preload" in m.group() or "preconnect" in m.group() else m.group()
        u = urllib.parse.urljoin(url, html.unescape(href.group(1))); f = local(u, url)
        if not f:
            return ""
        (dossier / f).write_text(styles((dossier / f).read_text(encoding="utf-8", errors="replace"), u), encoding="utf-8")
        return f'<link rel="stylesheet" href="{f}">'

    t = re.sub(r"<link\b[^>]*>", feuille, t)
    t = re.sub(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)', lambda m: m.group(1) + (local(m.group(2), url) or ""), t)
    t = re.sub(r'(style=["\'][^"\']*)', lambda m: styles(m.group(1), url), t)
    (dossier / "page.html").write_text(t, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    chrome = "/usr/bin/google-chrome"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome) if os.path.exists(chrome) else p.chromium.launch()
        ctx = b.new_context(viewport={"width": largeur, "height": 844}, device_scale_factor=2, java_script_enabled=False)
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith("file:") else r.abort())   # rien ne part vers le site
        pg = ctx.new_page(); pg.goto((dossier / "page.html").as_uri()); pg.wait_for_load_state("load")
        if hauteur:
            pg.set_viewport_size({"width": largeur, "height": hauteur}); pg.screenshot(path=str(sortie))
        else:
            pg.screenshot(path=str(sortie), full_page=True)
        b.close()
    from PIL import Image
    with Image.open(sortie) as im:
        print(f"Capture : {sortie} ({im.width} × {im.height} px), page reconstituée dans {dossier}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("page"); p.add_argument("--prendre"); p.add_argument("--vers", default="images_site")
    p.add_argument("--capture"); p.add_argument("--largeur", type=int, default=390); p.add_argument("--hauteur", type=int)
    a = p.parse_args()
    url = urllib.parse.urljoin(SITE + "/", a.page.lstrip("/")) if not a.page.startswith("http") else a.page
    vers = pathlib.Path(a.vers).resolve() if not a.capture else pathlib.Path(a.capture).resolve().parent
    vers.mkdir(parents=True, exist_ok=True)
    f = vers / "_page.html"
    code = lire(url, f)
    if code != "200":
        raise SystemExit(f"{url} : réponse {code}")
    t = f.read_text(encoding="utf-8", errors="replace"); f.unlink()
    if a.capture:
        capture(url, t, pathlib.Path(a.capture).resolve(), a.largeur, a.hauteur); return
    liste = images(t, url)
    print(f"{url} : {len(liste)} images")
    for k, (u, alt) in enumerate(liste, 1):
        genre = "photo déposée sur une page de restaurant" if "/uploads/" in u else "visuel du site"
        print(f"  {k:2d}. {u}  [{genre}]" + (f"  « {alt} »" if alt else ""))
    if a.prendre:
        choix = range(1, len(liste) + 1) if a.prendre == "tout" else [int(n) for n in a.prendre.split(",")]
        from PIL import Image
        for n in choix:
            u = liste[n - 1][0]; g = vers / nom_local(u)
            code = lire(u, g)
            if code != "200":
                print(f"  n° {n} : réponse {code}"); continue
            try:
                with Image.open(g) as im:
                    print(f"  n° {n} → {g} ({im.width} × {im.height} px)")
            except Exception:
                print(f"  n° {n} → {g}")


if __name__ == "__main__":
    main()
