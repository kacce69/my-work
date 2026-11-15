#!/usr/bin/env python3
"""Margot en image fixe, pour les posts, carrousels, stories et documents : un SVG (et, au besoin, un PNG à fond
transparent) avec la pose, l'expression et les accessoires du moteur de Reels — donc la même Margot partout.

Usage : python3 margot_svg.py sortie.svg [--pose pouce] [--gauche pointe] [--expression joie] [--accessoire toque,lunettes]
                                         [--regard droite] [--panneau "-10 %"] [--bouche 0.6] [--miroir] [--png 1200]
  --pose        bras droit, ou les deux bras (fete, hausse, hanches) ; --gauche : bras gauche seul
  --bouche      ouverture de la bouche, de 0 (sourire fermé) à 1
  --png LARGEUR écrit aussi sortie.png, à fond transparent, de cette largeur en pixels
Les noms acceptés sont ceux de CATALOGUE.md (§ 4) ; un nom inconnu est signalé.
Le texte d'un panneau est en Fraunces : dans une page HTML qui charge cette police, le SVG suffit ; ailleurs, prendre le PNG.
Sur un fond or ou prune, poser Margot sur un disque crème (#FBF3EC), comme dans les Reels : son en-tête est doré.
"""
import argparse, json, os, pathlib, re

ICI = pathlib.Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sortie"); p.add_argument("--pose", default="bonjour"); p.add_argument("--gauche"); p.add_argument("--expression", default="neutre")
    p.add_argument("--accessoire", default=""); p.add_argument("--regard", default="face"); p.add_argument("--panneau", default="")
    p.add_argument("--bouche", type=float, default=0.0); p.add_argument("--miroir", action="store_true"); p.add_argument("--png", type=int)
    a = p.parse_args()
    import reel
    pose = {"droite": a.pose, "gauche": a.gauche} if a.gauche else a.pose
    definition = {"type": "margot", "pose": pose, "expression": a.expression, "accessoire": [x for x in a.accessoire.split(",") if x],
                  "regard": a.regard, "panneau": a.panneau.replace("\\n", "\n"), "miroir": a.miroir, "entree": "aucune", "disque": False}
    data = {"W": reel.W, "H": reel.H, "fps": reel.FPS, "etiquette": "", "scenes": [], "env": [0], "coul": reel.COUL, "opt": {}}
    scripts = "\n".join((ICI / "page" / f).read_text(encoding="utf-8") for f in ("01_outils.js", "02_margot.js"))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{reel.page_html(data).split('<style>')[1].split('*{box-sizing')[0]}
    html,body{{margin:0;background:transparent}} .margot{{overflow:visible}}</style></head><body><script>
    window.DATA={json.dumps(data)};
    {scripts}
    const sc = {{debut: 0, fin: 100, parle0: 0, parle1: 100}}, x = {{sc, i: 1, th: THEME.creme, son() {{}}, secousse() {{}}}};
    const acteur = FAB.margot({json.dumps(definition, ensure_ascii=False)}, x);
    document.body.appendChild(acteur.el);
    document.fonts.load('900 60px Fraunces').catch(() => 0).then(() => document.fonts.ready).then(() => {{
      acteur.anim(0, 0, {a.bouche});
      const svg = acteur.el.querySelector("svg"), b = svg.querySelector(".corps").getBBox(), m = 26;   // la boîte ignore l'épaisseur des traits
      svg.removeAttribute("style"); svg.removeAttribute("class");
      const vb = [b.x - m, b.y - m, b.width + 2 * m, b.height + 2 * m].map(v => +v.toFixed(1));
      svg.setAttribute("viewBox", vb.join(" ")); svg.setAttribute("width", vb[2]); svg.setAttribute("height", vb[3]);
      {"svg.setAttribute('transform', 'scale(-1 1)');" if a.miroir else ""}
      window.SVG = svg.outerHTML;
      const largeur = {a.png or 0};
      if (largeur) {{ svg.setAttribute("width", "100%"); svg.removeAttribute("height"); document.body.innerHTML = `<div id="m" style="width:${{largeur}}px">${{svg.outerHTML}}</div>`; }}
      requestAnimationFrame(() => requestAnimationFrame(() => {{ window.PRET = true; }}));
    }});
    </script></body></html>"""
    sortie = pathlib.Path(a.sortie).resolve(); sortie.parent.mkdir(parents=True, exist_ok=True)
    tmp = sortie.with_suffix(".page.html"); tmp.write_text(page, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    chrome = "/usr/bin/google-chrome"
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome) if os.path.exists(chrome) else pw.chromium.launch()
        pg = b.new_page(viewport={"width": max(1200, (a.png or 0) + 40), "height": max(1400, int((a.png or 0) * 1.5))})
        pg.goto(tmp.as_uri()); pg.wait_for_function("window.PRET===true", timeout=20000)
        for al in pg.evaluate("window.ALERTES"):
            print("ALERTE :", re.sub(r"^scène \d+ : ", "", al))
        svg = pg.evaluate("window.SVG")
        sortie.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n", encoding="utf-8")
        if a.png:
            pg.locator("#m svg").screenshot(path=str(sortie.with_suffix(".png")), omit_background=True)
        b.close()
    tmp.unlink()
    print("Margot :", sortie, ("et " + sortie.with_suffix(".png").name) if a.png else "")


if __name__ == "__main__":
    main()
