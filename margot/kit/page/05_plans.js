// ── Décors (silhouettes discrètes derrière la scène) ───────────────────────────────────────────────
const teinte = f => f === "prune" || f === "nuit" ? "rgba(255,255,255,.09)" : "rgba(90,31,74,.13)";
const cadre = s => `<svg style="position:absolute;left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">${s}</svg>`;
function ville(fond) {
  const c = teinte(fond);
  const larg = [150, 110, 190, 130, 90, 170, 120, 160], haut = [300, 210, 380, 250, 170, 330, 230, 290];
  let x = -20, s = "";
  larg.forEach((w, k) => {
    const hh = haut[k], y = 1920 - hh;
    s += `<rect x="${x}" y="${y}" width="${w - 14}" height="${hh}" fill="${c}"/>`;
    for (let fy = y + 34; fy < 1900; fy += 56) for (let fx = x + 22; fx < x + w - 44; fx += 44) s += `<rect x="${fx}" y="${fy}" width="16" height="22" fill="${c}"/>`;
    x += w;
  });
  return cadre(s);
}
const DECORS = {
  ville,
  salle(fond) {
    const c = teinte(fond), r = (x, y, w, h, rx = 0) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${c}"/>`;
    const table = (x, y) => r(x - 150, y, 300, 22, 11) + r(x - 10, y + 22, 20, 1920 - y) + r(x - 250, y - 90, 16, 1920 - y + 90, 8) + r(x - 250, y + 40, 84, 16, 8) + r(x - 182, y + 40, 16, 1920 - y)
      + r(x + 234, y - 90, 16, 1920 - y + 90, 8) + r(x + 166, y + 40, 84, 16, 8) + r(x + 166, y + 40, 16, 1920 - y) + r(x - 40, y - 54, 14, 54, 5) + `<circle cx="${x - 33}" cy="${y - 68}" r="20" fill="${c}"/>` + r(x + 30, y - 40, 34, 40, 6);
    return cadre(table(290, 1700) + table(820, 1745));
  },
  rue(fond) {
    const c = teinte(fond), r = (x, y, w, h, rx = 0) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${c}"/>`;
    const boutique = (x, w, h) => {
      const y = 1920 - h; let s = r(x, y, w, h) + r(x - 12, y, w + 24, 56, 8);
      for (let k = 0; k < Math.floor((w + 24) / 48); k++) s += `<circle cx="${x + 12 + 48 * k}" cy="${y + 56}" r="24" fill="${c}"/>`;
      return s + r(x + 30, y + 120, w * 0.42, h - 190, 6) + r(x + w * 0.62, y + 120, w * 0.26, h - 120, 6) + r(x + w * 0.2, y - 64, w * 0.6, 46, 10);
    };
    const lampadaire = x => r(x - 5, 1560, 10, 360) + r(x - 40, 1548, 80, 14, 7) + `<circle cx="${x}" cy="1530" r="22" fill="${c}"/>`;
    return cadre(boutique(40, 300, 330) + boutique(400, 280, 390) + boutique(740, 300, 310) + lampadaire(376) + lampadaire(716));
  },
  cuisine(fond) {
    const c = teinte(fond), r = (x, y, w, h, rx = 0) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${c}"/>`;
    const marmite = x => r(x - 80, 1660, 160, 100, 14) + r(x - 106, 1682, 26, 16, 8) + r(x + 80, 1682, 26, 16, 8) + r(x - 90, 1638, 180, 20, 10) + r(x - 14, 1618, 28, 20, 8);
    const poele = x => r(x - 70, 1726, 140, 34, 12) + r(x + 70, 1736, 124, 14, 7);
    const bouteille = x => r(x - 22, 1650, 44, 110, 10) + r(x - 9, 1598, 18, 56, 6);
    return cadre(r(0, 1760, 1080, 160) + r(0, 1760, 1080, 18) + marmite(210) + poele(520) + bouteille(800) + bouteille(868) + bouteille(936));
  },
  nappe(fond) {
    const c = fond === "prune" || fond === "nuit" ? "rgba(255,255,255,.045)" : "rgba(90,31,74,.06)";
    return `<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(0deg,${c} 0 60px,transparent 60px 120px),repeating-linear-gradient(90deg,${c} 0 60px,transparent 60px 120px)"></div>`;
  },
  points(fond) {
    const c = fond === "prune" || fond === "nuit" ? "rgba(255,255,255,.08)" : "rgba(90,31,74,.10)";
    return `<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;background-image:radial-gradient(${c} 7px,transparent 8px);background-size:72px 72px"></div>`;
  },
  rayons(fond) {
    const c = fond === "prune" || fond === "nuit" ? "rgba(255,255,255,.05)" : "rgba(90,31,74,.06)";
    return {html: `<div style="position:absolute;left:-760px;top:-230px;width:2600px;height:2600px;background:repeating-conic-gradient(${c} 0deg 9deg,transparent 9deg 18deg)"></div>`,
      anim: (u, el) => { el.style.transform = `rotate(${(u * 5).toFixed(2)}deg)`; }};
  }
};

// ── Plans : mises en page prêtes à l'emploi. Chaque plan renvoie la liste de ses éléments ; ceux de
// « elements » (dans le scénario) s'ajoutent par-dessus. ─────────────────────────────────────────────
const etq = sc => sc.etiquette === false ? [] : [{type: "etiquette"}];
const ttl = (sc, d) => (sc.titre || []).length ? [{type: "titre", lignes: sc.titre, ...d, anime: sc.anime ?? d.anime, ...(sc.taille_titre ? {taille: sc.taille_titre} : {})}] : [];
const mgt = (sc, d) => sc.margot === false ? [] : [{type: "margot", ...d, pose: sc.pose ?? d.pose, expression: sc.expression ?? d.expression, accessoire: sc.accessoire, regard: sc.regard ?? d.regard,
  gestes: sc.gestes ?? d.gestes, miroir: sc.miroir, panneau: sc.panneau, entree: sc.entree, ...(sc.margot || {})}];
const PLANS = {
  // Le plan d'origine : étiquette, titre, pastilles, Margot en grand au centre.
  margot: sc => [...etq(sc), {type: "titre", legacy: true, petit: !!((sc.titre || []).length > 2 || (sc.puces && sc.puces.length)), lignes: sc.titre || []},
    {type: "puces", legacy: true, items: sc.puces || []},
    ...(sc.margot === false ? [] : [{type: "margot", legacy: true, pose: sc.pose, expression: sc.expression, accessoire: sc.accessoire, regard: sc.regard, gestes: sc.gestes, miroir: sc.miroir, panneau: sc.panneau, entree: sc.entree, ...(sc.margot || {})}])],
  // Accroche : très gros titre dont les mots arrivent avec la voix.
  accroche: sc => [...etq(sc), ...ttl(sc, {haut: 330, taille: 132, anime: "voix"}), ...mgt(sc, {x: 540, y: 1160, taille: 0.8})],
  // Gros sous-titres : le texte dit s'affiche en grand, mot après mot.
  mots: sc => [...etq(sc), {type: "grosmots", haut: 380, ...(sc.taille_titre ? {taille: sc.taille_titre} : {})}, ...mgt(sc, {x: 540, y: 1160, taille: 0.8})],
  telephone: sc => [...etq(sc), ...ttl(sc, {haut: 300, taille: 84}), {type: "telephone", x: 668, y: 968, ...(sc.telephone || {})}, ...mgt(sc, {x: 205, y: 1236, taille: 0.46, pose: "pointe", regard: "droite"})],
  chiffre: sc => [...etq(sc), {type: "chiffre", haut: 320, ...(sc.chiffre || {})}, ...mgt(sc, {x: 540, y: 1215, taille: 0.6})],
  barres: sc => [...etq(sc), ...ttl(sc, {haut: 300, taille: 80}), {type: "barres", haut: 540, ...(sc.barres || {})}, ...mgt(sc, {x: 540, y: 1262, taille: 0.48})],
  liste: sc => {
    const L = Array.isArray(sc.liste) ? {items: sc.liste} : (sc.liste || {}), n = (L.items || []).length, tm = n <= 3 ? 0.56 : n === 4 ? 0.46 : 0.38;
    return [...etq(sc), ...ttl(sc, {haut: 300, taille: 80}), {type: "liste", haut: 530, ...L}, ...mgt(sc, {x: 540, y: 1405 - tm * 300, taille: tm})];
  },
  compare: sc => {
    const c = sc.compare || {};
    return [...etq(sc), ...ttl(sc, {haut: 300, taille: 76}), {type: "carton", x: 286, haut: 560, l: 452, ton: "moins", icone: "croix", quand: 0.4, ...(c.gauche || {})},
      {type: "carton", x: 794, haut: 560, l: 452, ton: "plus", icone: "coche", quand: {part: 0.5}, ...(c.droite || {})}, ...mgt(sc, {x: 540, y: 1262, taille: 0.48})];
  },
  question: sc => {
    const q = sc.question || {}, tr = q.revele ?? {part: 0.62};
    return [...etq(sc), ...ttl(sc, {haut: 300, taille: 80}), {type: "choix", haut: 650, ...q}, ...mgt(sc, {x: 540, y: 1272, taille: 0.46, expression: "doute", gestes: [{quand: tr, expression: "joie"}, {quand: tr, geste: "saut"}]})];
  },
  dialogue: sc => [...etq(sc), {type: "chat", haut: 330, repliques: sc.dialogue || []}, ...mgt(sc, {x: 540, y: 1262, taille: 0.48})],
  // Montre : Margot, à gauche, montre du doigt ce qui apparaît à droite — une icône ou un plat (une chose, ou une liste de choses).
  // Par défaut l'illustration est posée sur un disque, flotte doucement, et accepte "badge" (une petite icône sur son coin).
  montre: sc => {
    const clair = !sc.fond || sc.fond === "creme" || sc.fond === "or";
    const els = [].concat(sc.montre || []).map(m => ({x: 800, y: 972, quand: 0.35, boucle: "flotte",
      ...(m.type === "icone" ? {taille: 250, fond: clair ? "prune" : "creme", couleur: clair ? "creme" : "prune"} : m.type === "plat" ? (clair ? {taille: 340, fond: "prune"} : {taille: 410}) : {}), ...m}));
    return [...etq(sc), ...ttl(sc, {haut: 300, taille: 84}), ...(sc.puces && sc.puces.length ? [{type: "puces", haut: 520, items: sc.puces, quand: 0.5}] : []), ...els,
      ...mgt(sc, {x: 290, y: 1010, taille: 0.78, pose: "pointe", regard: "droite"})];
  },
  // Duo : Margot et un personnage (le restaurateur, un client) côte à côte ; leurs répliques s'affichent en bulles.
  duo: sc => {
    const d = sc.duo || {}, rs = d.repliques || [], moi = r => r.qui === "margot", h = (r, j) => r.quand ?? {part: j / Math.max(1, rs.length)};
    const bulles = rs.map((r, j) => {
      const k = rs.findIndex((z, n) => n > j && moi(z) === moi(r));
      return {type: "bulle", texte: r.texte, taille: r.taille || 44, l: 470, quand: h(r, j), ...(k > 0 ? {jusqu: h(rs[k], k)} : {}), ...(moi(r) ? {gauche: 56, bas: 1084, queue: "bas-gauche"} : {droite: 1024, bas: 840, queue: "bas-droite"})};
    });
    return [...etq(sc), ...ttl(sc, {haut: 300, taille: 76}), {type: "personnage", role: "chef", x: 806, y: 1150, taille: 372, quand: 0.15, regard: "gauche", ...d, repliques: undefined},
      ...mgt(sc, {x: 270, y: 1283, taille: 0.56, regard: "droite"}), ...bulles];
  },
  mythe: sc => {
    const m = sc.mythe || {}, v = m.verdict || "FAUX", tq = m.quand ?? {part: 0.7}, contre = /faux|non|pas/i.test(v);
    return [...etq(sc), {type: "citation", haut: 350, l: 920, texte: m.texte, taille: m.taille, auteur: m.auteur, tampon: {texte: v, quand: tq, couleur: m.couleur ?? (contre ? "rouge" : "vert")}},
      ...mgt(sc, {x: 540, y: 1240, taille: 0.54, expression: "doute", gestes: [{quand: tq, geste: contre ? "non" : "hoche"}, {quand: tq, expression: contre ? "colere" : "joie"}]})];
  },
  image: sc => [...etq(sc), ...ttl(sc, {haut: 300, taille: 76}), {type: "image", x: 540, y: 850, l: 860, h: 600, ...(sc.image || {})}, ...mgt(sc, {x: 190, y: 1292, taille: 0.4})],
  fin: sc => {
    const a = typeof sc.appel === "string" ? {genre: sc.appel} : (sc.appel || {genre: "commenter"});
    return [...etq(sc), ...ttl(sc, {haut: 312, taille: 112}), {type: "appel", x: 540, y: 706, ...a}, ...(sc.puces && sc.puces.length ? [{type: "puces", haut: 868, items: sc.puces, quand: 0.8}] : []), ...mgt(sc, {x: 540, y: 1222, taille: 0.6})];
  },
  // Rien d'imposé : seulement « elements ».
  libre: sc => sc.etiquette === true ? [{type: "etiquette"}] : []
};
