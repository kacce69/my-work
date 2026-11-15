// ── Outils communs : couleurs, thèmes, courbes, heures, icônes ─────────────────────────────────────
const D = window.DATA, C = D.coul, O = D.opt || {};
const FONCE = "#3D1030", NOIR = "#2A0A20", ENCRE = "#1d0a18", ROSE = "#E8879B", VERT = "#2F8F5B", ROUGE = "#D4374A";
window.ALERTES = []; window.SONS = []; window.JOURNAL = [];
window.onerror = (m, f, l) => { window.ALERTES.push(`erreur de la page : ${m} (ligne ${l})`); window.PRET = true; };

const THEME = {
  creme: {titre: C.prune, tagF: C.or, tagT: FONCE, subF: C.prune, subT: C.creme, disque: false, deco: "rgba(235,190,114,.28)", puceF: C.prune, puceT: C.creme,
          accT: FONCE, accF: C.or, carte: "#fff", carteT: FONCE, doux: "rgba(61,16,48,.62)", trait: C.prune, voile: "rgba(90,31,74,.10)"},
  prune: {titre: C.creme, tagF: C.or, tagT: FONCE, subF: C.creme, subT: FONCE, disque: true, deco: "rgba(255,255,255,.06)", puceF: C.or, puceT: FONCE,
          accT: C.or, accF: "", carte: C.creme, carteT: FONCE, doux: "rgba(251,243,236,.74)", trait: C.or, voile: "rgba(255,255,255,.12)"},
  or:    {titre: FONCE, tagF: C.prune, tagT: C.creme, subF: C.prune, subT: C.creme, disque: true, deco: "rgba(255,255,255,.24)", puceF: C.prune, puceT: C.creme,
          accT: C.creme, accF: C.prune, carte: C.creme, carteT: FONCE, doux: "rgba(61,16,48,.7)", trait: C.prune, voile: "rgba(90,31,74,.14)"},
  nuit:  {titre: C.creme, tagF: C.or, tagT: FONCE, subF: C.creme, subT: FONCE, disque: true, deco: "rgba(255,255,255,.05)", puceF: C.or, puceT: FONCE,
          accT: C.or, accF: "", carte: C.creme, carteT: FONCE, doux: "rgba(251,243,236,.7)", trait: C.or, voile: "rgba(255,255,255,.10)"}
};

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const sortie = x => 1 - Math.pow(1 - clamp(x), 3);
const rebond = x => { x = clamp(x); const c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const douce = x => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const mel = (a, b, k) => a + (b - a) * k;
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const coul = (c, defaut) => c ? (C[c] || {vert: VERT, rouge: ROUGE, rose: ROSE, fonce: FONCE, blanc: "#fff"}[c] || c) : defaut;
const E = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
function alea(g) { let a = g >>> 0; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

// Texte enrichi : *mot* = mot mis en valeur (couleur d'accent du thème).
const accent = th => `color:${th.accT};${th.accF ? "background:" + th.accF + ";" : ""}`;
const riche = (s, th) => esc(s).replace(/\*([^*]+)\*/g, (_, m) => `<span class="acc" style="${accent(th)}">${m}</span>`);
function motsRiches(l, th) {                               // chaque mot dans son <span class="m">, l'accent peut couvrir plusieurs mots
  let on = false;
  return String(l).split(" ").filter(Boolean).map(w => {
    if (w.startsWith("*")) { on = true; w = w.slice(1); }
    const a = on;
    if (/\*[.,!?:;…»]*$/.test(w)) { w = w.replace("*", ""); on = false; }
    return `<span class="m"${a ? ` style="${accent(th)}"` : ""}>${esc(w)}</span>`;
  }).join(" ");
}

// ── Heures : « quand » d'un élément, en secondes depuis le début de la scène ────────────────────────
// nombre | "voix" (début de la voix) | "fin-voix" | "@mot dit" | {mot, n, decale} | {part: 0..1 de la voix} | {avant_fin: s}
const simple = s => String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/œ/g, "oe");
const parties = s => simple(s).split(/[^a-z0-9]+/).filter(Boolean);
function rangMot(sc, q, n = 1) {
  const plat = []; (sc.mots || []).forEach((m, j) => parties(m[2]).forEach(p => plat.push([p, j])));
  const ch = parties(q); if (!ch.length) return -1;
  for (let i = 0; i + ch.length <= plat.length; i++)
    if (ch.every((c, k) => plat[i + k][0] === c) && --n === 0) return plat[i][1];
  return -1;
}
function heure(q, sc, defaut, x) {
  if (q == null) q = defaut;
  if (q == null) return 0;
  if (typeof q === "number") return q;
  const p0 = sc.parle0 - sc.debut, p1 = sc.parle1 - sc.debut;
  if (q === "voix") return p0;
  if (q === "fin-voix") return p1;
  if (typeof q === "string") q = {mot: q.replace(/^@/, "")};
  let t = 0;
  if (q.mot != null) {
    const r = typeof q.mot === "number" ? q.mot - 1 : rangMot(sc, q.mot, q.n || 1);
    if (r < 0 || !(sc.mots || [])[r]) { window.ALERTES.push(`scène ${x ? x.i + 1 : "?"} : « ${q.mot} » n'est pas dans la voix de cette scène`); t = p0; }
    else { t = sc.mots[r][q.fin ? 1 : 0] - sc.debut; window.JOURNAL.push(`scène ${x ? x.i + 1 : "?"} : « ${q.mot} » dit à ${t.toFixed(2)} s`); }
  } else if (q.part != null) t = p0 + q.part * (p1 - p0);
  else if (q.avant_fin != null) t = sc.fin - sc.debut - q.avant_fin;
  return t + (q.decale || 0);
}
// Heure d'apparition de chaque mot d'un titre, d'après la voix (les mots absents de la voix suivent le précédent).
function heuresVoix(mots, sc, t0) {
  const toks = (sc.mots || []).map(m => parties(m[2])); let p = 0, prec = t0; const out = [];
  mots.forEach(w => {
    const c = parties(w).sort((a, b) => b.length - a.length)[0]; let r = -1;
    if (c) for (let j = p; j < toks.length; j++) if (toks[j].includes(c)) { r = j; break; }
    if (r >= 0) { prec = Math.max(prec, sc.mots[r][0] - sc.debut - 0.05); p = r; } else prec += 0.08;
    out.push(prec);
  });
  return out;
}

// ── Entrées, boucles, position ─────────────────────────────────────────────────────────────────────
const ENTREES = {
  pop: k => ({o: clamp(k * 3), s: k <= 0 ? 0.6 : 0.6 + 0.4 * rebond(k)}),
  monte: k => ({o: sortie(k), ty: (1 - sortie(k)) * 56}),
  descend: k => ({o: sortie(k), ty: -(1 - sortie(k)) * 56}),
  "de-gauche": k => ({o: clamp(k * 3), tx: -(1 - sortie(k)) * 220}),
  "de-droite": k => ({o: clamp(k * 3), tx: (1 - sortie(k)) * 220}),
  "de-bas": k => ({o: clamp(k * 4), ty: (1 - sortie(k)) * 620}),
  fondu: k => ({o: k}),
  zoom: k => ({o: clamp(k * 4), s: 1 + (1 - sortie(k)) * 1.3}),
  tombe: k => ({o: clamp(k * 5), ty: -(1 - rebond(k)) * 520}),
  tourne: k => ({o: clamp(k * 3), r: -(1 - rebond(k)) * 16, s: 0.7 + 0.3 * rebond(k)}),
  aucune: () => ({o: 1})
};
const BOUCLES = {
  flotte: a => ({ty: 9 * Math.sin(2 * Math.PI * a / 2.4)}),
  pulse: a => ({s: 1 + 0.045 * Math.sin(2 * Math.PI * a / 1.1)}),
  balance: a => ({r: 4 * Math.sin(2 * Math.PI * a / 1.8)}),
  tourne: a => ({r: a * 90}),
  tremble: a => ({tx: 3 * Math.sin(a * 47), ty: 3 * Math.cos(a * 53)})
};
// État d'un élément à l'instant u (secondes depuis le début de la scène) : null s'il n'est pas à l'écran.
function cycle(def, x, dq = 0.2, de = "pop", dd = 0.45) {
  const sc = x.sc, t0 = heure(def.quand, sc, dq, x), t1 = def.jusqu != null ? heure(def.jusqu, sc, null, x) : null;
  const en = typeof def.entree === "object" && def.entree ? def.entree : {type: def.entree || de};
  const f = ENTREES[en.type] || ENTREES.pop, dur = en.duree || dd, bo = BOUCLES[def.boucle];
  x.t0 = t0;                                              // l'heure d'arrivée, pour que Margot puisse y jeter un œil (jeu fin)
  if (def.entree && !ENTREES[en.type]) window.ALERTES.push(`scène ${x.i + 1} : entrée inconnue « ${en.type} »`);
  return {t0, t1, etat(u) {
    const a = u - t0;
    if (a < 0) return null;
    const st = {o: 1, tx: 0, ty: 0, s: 1, r: 0, age: a, k: clamp(a / dur), ...f(clamp(a / dur))};
    if (bo) { const b = bo(a); st.tx += b.tx || 0; st.ty += b.ty || 0; st.r += b.r || 0; st.s *= b.s || 1; }
    if (t1 != null && u > t1) { const q = (u - t1) / 0.25; if (q >= 1) return null; st.o *= 1 - q; st.s *= 1 - 0.15 * q; }
    return st;
  }};
}
function applique(el, st, base = "") {
  if (!st) { el.style.display = "none"; return false; }
  el.style.display = ""; el.style.opacity = st.o;
  el.style.transform = `${base} translate(${st.tx.toFixed(1)}px,${st.ty.toFixed(1)}px) rotate(${st.r.toFixed(2)}deg) scale(${st.s.toFixed(4)})`;
  return true;
}
// Place un élément : x, y = son centre ; ou haut / bas / gauche / droite = le bord correspondant ; l = largeur.
function pose(el, def, d = {}) {
  const g = k => def[k] ?? d[k];
  let bx = "-50%", by = "-50%";
  if (g("gauche") != null && def.x == null) { el.style.left = g("gauche") + "px"; bx = "0"; }
  else if (g("droite") != null && def.x == null) { el.style.left = g("droite") + "px"; bx = "-100%"; }
  else el.style.left = (g("x") ?? 540) + "px";
  if (g("haut") != null && def.y == null) { el.style.top = g("haut") + "px"; by = "0"; }
  else if (g("bas") != null && def.y == null) { el.style.top = g("bas") + "px"; by = "-100%"; }
  else el.style.top = (g("y") ?? 960) + "px";
  if (g("l")) el.style.width = g("l") + "px";
  if (def.z != null) el.style.zIndex = def.z;
  const base = `translate(${bx},${by})` + (def.rot ? ` rotate(${def.rot}deg)` : "");
  el.style.transform = base;
  return base;
}

// ── Icônes (traits arrondis, boîte 100 × 100) ──────────────────────────────────────────────────────
const ICONES = {
  coche: '<path d="M20 54 L42 74 L82 28"/>',
  croix: '<path d="M26 26 L74 74 M74 26 L26 74"/>',
  plus: '<path d="M50 18 V82 M18 50 H82"/>',
  fleche: '<path d="M14 50 H82 M58 26 L84 50 L58 74"/>',
  etoile: '<path d="M50 12 L61.8 36.6 L88 40.6 L69 59.4 L73.5 86 L50 73.4 L26.5 86 L31 59.4 L12 40.6 L38.2 36.6 Z" fill="currentColor"/>',
  coeur: '<path d="M50 84 C14 60 10 34 28 24 C40 18 48 26 50 34 C52 26 60 18 72 24 C90 34 86 60 50 84 Z" fill="currentColor"/>',
  eclair: '<path d="M58 8 L24 56 H48 L40 92 L76 42 H52 Z" fill="currentColor"/>',
  horloge: '<circle cx="50" cy="50" r="36"/><path d="M50 28 V50 L66 60"/>',
  loupe: '<circle cx="43" cy="43" r="25"/><path d="M62 62 L86 86"/>',
  telephone: '<rect x="30" y="10" width="40" height="80" rx="9"/><path d="M44 78 H56"/>',
  epingle: '<path d="M50 90 C30 62 24 50 24 38 A26 26 0 1 1 76 38 C76 50 70 62 50 90 Z"/><circle cx="50" cy="38" r="9"/>',
  calendrier: '<rect x="16" y="22" width="68" height="62" rx="9"/><path d="M16 42 H84 M34 12 V30 M66 12 V30"/>',
  euro: '<path d="M72 26 A30 30 0 1 0 72 74 M18 43 H56 M18 58 H52"/>',
  assiette: '<circle cx="50" cy="50" r="36"/><circle cx="50" cy="50" r="20"/>',
  couverts: '<path d="M30 12 V40 M20 12 V32 Q20 42 30 42 Q40 42 40 32 V12 M30 42 V88 M70 12 C84 30 82 50 70 56 M70 12 V88"/>',
  verre: '<path d="M30 12 H70 C70 40 62 52 50 52 C38 52 30 40 30 12 Z M50 52 V84 M34 86 H66"/>',
  toque: '<path d="M30 62 C8 62 8 32 30 34 C32 12 68 12 70 34 C92 32 92 62 70 62 V84 H30 Z M30 72 H70"/>',
  cloche: '<path d="M18 72 H82 M28 72 C28 30 72 30 72 72 M50 40 V30 M42 30 H58"/>',
  ardoise: '<path d="M14 16 H86 V66 H14 Z M30 66 L22 88 M70 66 L78 88 M30 34 H62 M30 48 H52"/>',
  carte: '<rect x="24" y="12" width="52" height="76" rx="8"/><path d="M36 34 H64 M36 50 H58 M36 66 H62"/>',
  boutique: '<path d="M18 46 V86 H82 V46 M10 46 L20 18 H80 L90 46 Z M40 86 V62 H60 V86"/>',
  maison: '<path d="M12 50 L50 16 L88 50 M22 42 V86 H78 V42 M42 86 V62 H58 V86"/>',
  photo: '<rect x="12" y="30" width="76" height="52" rx="9"/><circle cx="50" cy="56" r="15"/><path d="M36 30 L42 18 H58 L64 30"/>',
  qr: '<rect x="14" y="14" width="28" height="28" rx="4"/><rect x="58" y="14" width="28" height="28" rx="4"/><rect x="14" y="58" width="28" height="28" rx="4"/><path d="M58 58 H70 V70 M86 58 V72 M58 84 H72 M84 86 H86"/>',
  lien: '<path d="M42 58 L58 42 M36 48 L26 58 A14 14 0 0 0 46 78 L52 72 M64 52 L74 42 A14 14 0 0 0 54 22 L48 28"/>',
  avion: '<path d="M10 46 L90 12 L64 88 L46 58 Z M46 58 L90 12"/>',
  signet: '<path d="M26 12 H74 V88 L50 68 L26 88 Z"/>',
  commentaire: '<path d="M50 14 C74 14 88 30 88 48 C88 66 74 80 50 80 C44 80 39 79 34 77 L14 86 L21 68 C15 62 12 56 12 48 C12 30 26 14 50 14 Z"/>',
  message: '<path d="M14 20 H86 V66 H46 L28 84 V66 H14 Z"/>',
  personne: '<circle cx="50" cy="34" r="17"/><path d="M16 88 C16 62 84 62 84 88"/>',
  pouce: '<path d="M14 46 H32 V86 H14 Z M32 50 L46 16 C56 16 60 24 58 34 L55 44 H76 C86 44 88 54 85 62 L79 80 C77 85 73 86 68 86 H32"/>',
  oeil: '<path d="M8 50 C28 20 72 20 92 50 C72 80 28 80 8 50 Z"/><circle cx="50" cy="50" r="13"/>',
  ampoule: '<path d="M38 64 C22 52 24 20 50 20 C76 20 78 52 62 64 V74 H38 Z M40 86 H60"/>',
  billet: '<rect x="10" y="28" width="80" height="44" rx="7"/><circle cx="50" cy="50" r="11"/>',
  graphique: '<path d="M14 86 H88 M22 72 L42 50 L56 60 L82 26 M64 26 H82 V44"/>',
  cible: '<circle cx="50" cy="50" r="38"/><circle cx="50" cy="50" r="23"/><circle cx="50" cy="50" r="7" fill="currentColor"/>',
  cadenas: '<rect x="22" y="44" width="56" height="42" rx="8"/><path d="M34 44 V32 A16 16 0 0 1 66 32 V44"/>',
  cadeau: '<path d="M18 44 H82 V86 H18 Z M10 28 H90 V44 H10 Z M50 28 V86 M50 28 C40 6 22 14 32 28 M50 28 C60 6 78 14 68 28"/>',
  feuille: '<path d="M18 82 C18 40 46 18 84 16 C82 54 60 82 18 82 Z M18 82 L60 40"/>',
  flocon: '<path d="M50 10 V90 M15.4 30 L84.6 70 M15.4 70 L84.6 30 M40 18 L50 28 L60 18 M40 82 L50 72 L60 82"/>',
  interdit: '<circle cx="50" cy="50" r="36"/><path d="M25 25 L75 75"/>',
  question: '<path d="M34 36 C34 16 66 16 66 36 C66 50 50 50 50 64"/><circle cx="50" cy="82" r="4" fill="currentColor"/>',
  exclamation: '<path d="M50 14 V62"/><circle cx="50" cy="82" r="4" fill="currentColor"/>',
  soleil: '<circle cx="50" cy="50" r="18"/><path d="M50 8 V20 M50 80 V92 M8 50 H20 M80 50 H92 M20.3 20.3 L28.8 28.8 M71.2 71.2 L79.7 79.7 M20.3 79.7 L28.8 71.2 M71.2 28.8 L79.7 20.3"/>',
  liste: '<rect x="20" y="12" width="60" height="76" rx="8"/><path d="M33 34 L39 40 L49 28 M58 36 H68 M33 60 L39 66 L49 54 M58 62 H68"/>',
  calculette: '<rect x="22" y="10" width="56" height="80" rx="9"/><path d="M34 28 H66 M35 50 H36 M49.5 50 H50.5 M64 50 H65 M35 68 H36 M49.5 68 H50.5 M64 68 H65"/>',
  balance: '<path d="M50 16 V84 M30 86 H70 M18 30 H82 M18 30 L7 58 H29 Z M82 30 L71 58 H93 Z"/>',
  megaphone: '<path d="M14 42 V58 H30 L66 78 V22 L30 42 Z M32 60 L38 84 H48 L43 66 M78 38 C85 44 85 56 78 62"/>',
  flamme: '<path d="M50 90 C28 90 20 70 28 54 C34 44 40 40 40 24 C52 30 57 42 56 52 C61 47 63 40 62 32 C77 46 81 60 76 73 C72 84 62 90 50 90 Z"/>',
  poubelle: '<path d="M20 28 H80 M40 28 V17 H60 V28 M28 28 L33 88 H67 L72 28 M43 43 V73 M57 43 V73"/>',
  rafraichir: '<path d="M82 50 A32 32 0 1 1 71 26 M72 8 V27 H53"/>'
};
const ico = (nom, taille = 100, c = "currentColor", ep = 8) =>
  `<svg class="ico" viewBox="0 0 100 100" width="${taille}" height="${taille}" fill="none" stroke="currentColor" stroke-width="${ep}" stroke-linecap="round" stroke-linejoin="round" style="color:${c};display:block">${ICONES[nom] || ICONES.question}</svg>`;

const FAB = {};                                            // les fabriques d'éléments, par type
