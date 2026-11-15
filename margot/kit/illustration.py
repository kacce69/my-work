#!/usr/bin/env python3
"""Une illustration du moteur en image fixe, à fond transparent, pour les posts, carrousels et stories :
Margot, un personnage, un plat, une icône, un téléphone et son écran — exactement ceux des Reels.

Usage :
  python3 illustration.py margot.png  --margot [--pose pouce] [--expression joie] [--accessoire toque,lunettes] [--regard droite] [--panneau "-10 %"]
                                      [--disque creme]            (Margot posée sur son disque crème, pour un fond or ou prune)
  python3 illustration.py chef.png    --personnage chef [--expression joie] [--objet telephone] [--teint mat] [--regard gauche]
  python3 illustration.py pizza.png   --plat pizza [--disque prune]
  python3 illustration.py euro.png    --icone euro [--disque prune] [--couleur creme] [--badge coche]
  python3 illustration.py ecran.png   --telephone carte           (un écran du téléphone : carte, recherche, fiche, reservation, qr, ardoise…)
  python3 illustration.py x.png       --element '{"type": "plat", "nom": "soupe", "badge": "euro"}'      (tout élément du catalogue)
Options communes :
  --largeur 600    largeur de l'image, en pixels (600 par défaut)
  --fond creme     le fond sur lequel l'image sera posée (creme, prune, or, nuit) : il choisit les couleurs par défaut des traits ;
                   l'image, elle, reste transparente. Sur un fond or ou prune, Margot se pose sur un disque crème (--disque creme) :
                   son en-tête est doré et son corps prune.
Les noms acceptés sont ceux de CATALOGUE.md (§ 4 à 7) ; un nom inconnu est signalé par une ALERTE.
Il ne faut que Python, Playwright et Chrome : pip install playwright ; python3 -m playwright install chromium (si /usr/bin/google-chrome manque).
Une image se regarde avant de servir.
"""
import argparse, json, os, pathlib, subprocess

ICI = pathlib.Path(__file__).resolve().parent


def polices():
    f = ICI / "node_modules/@fontsource/fraunces/files"
    face = (f"@font-face{{font-family:Fraunces;font-weight:900;src:url({f.as_uri()}/fraunces-latin-900-normal.woff2)}}"
            f"@font-face{{font-family:Fraunces;font-weight:600;src:url({f.as_uri()}/fraunces-latin-600-normal.woff2)}}") if f.exists() else ""
    inter = ICI / "node_modules/@fontsource/inter/files"
    try:
        connues = subprocess.run(["fc-list", ":family"], capture_output=True, text=True).stdout
    except OSError:
        connues = ""
    if inter.exists() and "Inter" not in connues:
        face += "".join(f"@font-face{{font-family:Inter;font-weight:{g};src:url({inter.as_uri()}/inter-latin-{g}-normal.woff2)}}" for g in (300, 500, 600, 700, 800))
    return face


def page(definition, fond):
    gabarit = (ICI / "reel_page.html").read_text(encoding="utf-8")
    style = gabarit.split("<style>")[1].split("</style>")[0].replace("/*POLICES*/", polices())
    scripts = "\n".join((ICI / "page" / f).read_text(encoding="utf-8") for f in ("01_outils.js", "02_margot.js", "03_elements.js", "03b_personnages.js", "04_telephone.js"))
    data = {"W": 1080, "H": 1920, "fps": 30, "etiquette": "", "scenes": [], "env": [0], "opt": {},
            "coul": {"creme": "#FBF3EC", "prune": "#5A1F4A", "or": "#EBBE72", "nuit": "#2A0A20"}}
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{style}
html,body{{background:transparent!important;overflow:visible}} .margot{{overflow:visible}}</style></head><body><div id="zone" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></div><script>
window.DATA={json.dumps(data)};
{scripts}
const sc = {{debut: 0, fin: 6, parle0: 0, parle1: 4, mots: [], fond: {json.dumps(fond)}}}, x = {{sc, i: 0, th: THEME[{json.dumps(fond)}] || THEME.creme, son() {{}}, secousse() {{}}}};
const def = {json.dumps(definition, ensure_ascii=False)};
if (!FAB[def.type]) window.ALERTES.push(`élément inconnu « ${{def.type}} »`);
const acteur = (FAB[def.type] || FAB.icone)(def, x);
document.getElementById("zone").appendChild(acteur.el);
document.fonts.load('900 60px Fraunces').catch(() => 0).then(() => document.fonts.ready).then(() => {{
  if (acteur.ajuste) acteur.ajuste();
  acteur.anim(5.9, 5.9, 0);
  requestAnimationFrame(() => requestAnimationFrame(() => {{
    // La boîte de l'image : pour Margot, son corps entier (bras et accessoires compris) ; sinon tout ce qui se voit —
    // les formes dessinées, les images, et les blocs qui ont un fond, un bord ou une ombre (un disque, le téléphone).
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    const prend = (r, m) => {{ x0 = Math.min(x0, r.left - m); y0 = Math.min(y0, r.top - m); x1 = Math.max(x1, r.right + m); y1 = Math.max(y1, r.bottom + m); }};
    const corps = acteur.el.querySelector("svg .corps");
    if (corps) {{
      const r = corps.getBoundingClientRect(), dq = acteur.el.querySelector(".disque");
      prend(r, 26 * r.width / corps.getBBox().width);
      if (dq) prend(dq.getBoundingClientRect(), 0);
    }}
    else acteur.el.querySelectorAll("*").forEach(e => {{
      if (e.closest("defs, clipPath")) return;
      for (let p = e; p && p !== acteur.el.parentElement; p = p.parentElement) {{ const s = getComputedStyle(p); if (s.display === "none" || s.visibility === "hidden" || +s.opacity === 0) return; }}
      const st = getComputedStyle(e), svg = e.namespaceURI.includes("svg");
      let r = e.getBoundingClientRect();
      if (!r.width || !r.height) return;
      for (let p = e.parentElement; p && p !== acteur.el.parentElement; p = p.parentElement) {{       // ce qu'un cadre coupe ne compte pas (la page qui dépasse de l'écran du téléphone)
        if (getComputedStyle(p).overflow === "visible") continue;
        const c = p.getBoundingClientRect(), g = Math.max(r.left, c.left), h = Math.max(r.top, c.top), d = Math.min(r.right, c.right), b = Math.min(r.bottom, c.bottom);
        if (d <= g || b <= h) return;
        r = {{left: g, top: h, right: d, bottom: b, width: d - g, height: b - h}};
      }}
      if (svg) {{ if (e.children.length || e.tagName === "svg") return; }}
      else if (e.tagName !== "IMG" && st.backgroundColor === "rgba(0, 0, 0, 0)" && st.backgroundImage === "none" && st.boxShadow === "none" && !parseFloat(st.borderTopWidth) && (e.children.length || !e.textContent.trim())) return;
      prend(r, svg ? (parseFloat(st.strokeWidth) || 0) * 0.6 * r.width / Math.max(1, e.getBBox().width || 1) : st.boxShadow === "none" ? 0 : 26);
    }});
    window.BOITE = [x0 - 14, y0 - 14, x1 - x0 + 28, y1 - y0 + 28];
    window.PRET = true;
  }}));
}});
</script></body></html>"""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sortie")
    p.add_argument("--margot", action="store_true"); p.add_argument("--pose", default="bonjour"); p.add_argument("--accessoire", default=""); p.add_argument("--panneau", default="")
    p.add_argument("--personnage"); p.add_argument("--expression"); p.add_argument("--objet"); p.add_argument("--teint"); p.add_argument("--regard")
    p.add_argument("--plat"); p.add_argument("--icone"); p.add_argument("--disque"); p.add_argument("--couleur"); p.add_argument("--badge")
    p.add_argument("--telephone"); p.add_argument("--element")
    p.add_argument("--largeur", type=int, default=600); p.add_argument("--fond", default="creme")
    a = p.parse_args()
    plus = lambda **k: {c: v for c, v in k.items() if v}
    if a.element:
        d = json.loads(a.element)
    elif a.margot:
        d = {"type": "margot", "pose": a.pose, "disque": bool(a.disque), **plus(expression=a.expression, accessoire=[n for n in a.accessoire.split(",") if n], regard=a.regard, panneau=a.panneau.replace("\\n", "\n"))}
    elif a.personnage:
        d = {"type": "personnage", "role": a.personnage, "taille": 400, **plus(expression=a.expression, objet=a.objet, teint=a.teint, regard=a.regard)}
    elif a.plat:
        d = {"type": "plat", "nom": a.plat, "taille": 400, **plus(fond=a.disque, badge=a.badge)}
    elif a.icone:
        d = {"type": "icone", "nom": a.icone, "taille": 300, **plus(fond=a.disque, couleur=a.couleur, badge=a.badge)}
    elif a.telephone:
        d = {"type": "telephone", "ecran": {"type": a.telephone, "defile": False}, "son": False}
    else:
        raise SystemExit(__doc__)
    d = {"x": 540, "y": 960, "quand": 0, "entree": "aucune", **d}
    sortie = pathlib.Path(a.sortie).resolve(); sortie.parent.mkdir(parents=True, exist_ok=True)
    tmp = sortie.with_suffix(".page.html"); tmp.write_text(page(d, a.fond), encoding="utf-8")
    from playwright.sync_api import sync_playwright
    chrome = "/usr/bin/google-chrome"
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome) if os.path.exists(chrome) else pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(tmp.as_uri()); pg.wait_for_function("window.PRET===true", timeout=20000)
        for al in pg.evaluate("window.ALERTES"):
            print("ALERTE :", al.replace("scène 1 : ", ""))
        x, y, l, h = pg.evaluate("window.BOITE")
        pg.close()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=max(0.25, min(6, a.largeur / l)))
        pg.goto(tmp.as_uri()); pg.wait_for_function("window.PRET===true", timeout=20000)
        pg.screenshot(path=str(sortie), omit_background=True, clip={"x": x, "y": y, "width": l, "height": h})
        b.close()
    tmp.unlink()
    print("Illustration :", sortie, f"(environ {round(a.largeur)} × {round(a.largeur * h / l)} px)")


if __name__ == "__main__":
    main()
