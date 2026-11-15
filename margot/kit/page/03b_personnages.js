// ── Personnages (le restaurateur, le serveur, les clients) et plats illustrés ───────────────────────
// Dans le même trait que Margot. Un personnage ne parle que si « parle » est vrai (sa bouche suit alors la voix).
const TEINTS = {clair: "#F6D7BC", mat: "#E8B48A", fonce: "#9A6444"};
const PEX0 = {mw: 18, my: 148, mb: 157, ey: 9, sgA: 0, sdA: 0, sgY: 0, sdY: 0, rond: 0};
const PEXPR = {
  neutre: {}, joie: {mb: 168, mw: 22, sgY: -4, sdY: -4}, doute: {mb: 148, mw: 14, sgA: 9, sdA: -11, sdY: -7},
  surprise: {ey: 12, rond: 1, sgY: -8, sdY: -8}, triste: {mb: 138, mw: 16, sgA: -12, sdA: -12}, colere: {mb: 140, mw: 16, sgA: 14, sdA: 14, ey: 7}
};
const pexpr = n => ({...PEX0, ...(PEXPR[n] || {})});
const ROLES = ["chef", "cheffe", "serveur", "client", "cliente"];
const assombri = (hex, k = 0.16) => "#" + [1, 3, 5].map(j => Math.round(parseInt(hex.slice(j, j + 2), 16) * (1 - k)).toString(16).padStart(2, "0")).join("");

function personnageSVG(role, def, th) {
  const peau = TEINTS[def.teint] || TEINTS.mat, sombre = th.titre === C.creme, cuisine = role === "chef" || role === "cheffe", blanc = cuisine || role === "serveur";
  const haut = coul(def.couleur, blanc ? "#FFFDF8" : role === "cliente" ? ROSE : "#3E8E86"), manche = blanc ? "#E9DFD4" : assombri(haut);
  const jambe = cuisine || role === "serveur" ? (sombre ? "#8E7F96" : FONCE) : "#4A5A78", pied = sombre ? "#C9BBCB" : FONCE;
  const chev = def.cheveux || (role === "cliente" || role === "cheffe" ? "#6B2E1E" : "#3D2416");
  const bras = (d, c = manche) => `<path d="${d}" fill="none" stroke="${c}" stroke-width="30" stroke-linecap="round"/>`, mainP = (x, y) => `<circle cx="${x}" cy="${y}" r="17" fill="${peau}"/>`;
  const gauche = bras("M94 222 C62 242 56 282 66 312") + mainP(67, 324), ob = def.objet;
  // Le bras à droite de l'image : au repos, ou tenant un téléphone, un plateau, une carte
  const droit = ob === "telephone" || ob === "carte" ? bras("M206 226 C240 250 236 276 212 266") : ob === "plateau" ? bras("M206 222 C236 232 250 204 248 176") : bras("M206 222 C238 242 244 282 234 312") + mainP(233, 324);
  const tenu = ob === "telephone" ? `<rect x="182" y="210" width="42" height="70" rx="9" fill="${ENCRE}"/><rect x="187" y="217" width="32" height="52" rx="4" fill="${C.creme}"/>` + mainP(207, 270)
    : ob === "carte" ? `<rect x="168" y="196" width="66" height="88" rx="8" fill="${C.creme}" stroke="${C.or}" stroke-width="5"/><g stroke="${P}" stroke-width="5" stroke-linecap="round"><path d="M180 218H222M180 236H214M180 254H218"/></g>` + mainP(207, 272)
    : ob === "plateau" ? mainP(248, 170) + `<ellipse cx="250" cy="152" rx="58" ry="8" fill="${C.or}"/><path d="M208 148 C208 100 292 100 292 148 Z" fill="${C.creme}" stroke="${C.or}" stroke-width="5" stroke-linejoin="round"/><circle cx="250" cy="107" r="7" fill="${C.or}"/>` : "";
  if (ob && !tenu) window.ALERTES.push(`objet de personnage inconnu « ${ob} » (telephone, carte, plateau)`);
  const torse = cuisine ? `<rect x="84" y="184" width="132" height="172" rx="34" fill="${haut}" stroke="#E6D8CC" stroke-width="5"/><path d="M150 200 V300" stroke="#E6D8CC" stroke-width="4"/>
      <g fill="${P}"><circle cx="131" cy="230" r="6"/><circle cx="169" cy="230" r="6"/><circle cx="131" cy="264" r="6"/><circle cx="169" cy="264" r="6"/></g>
      <path d="M88 298 H212 V338 Q212 356 190 356 H110 Q88 356 88 338 Z" fill="${P}"/><path d="M122 180 L150 204 L178 180 Z" fill="${C.or}"/>`
    : role === "serveur" ? `<rect x="84" y="184" width="132" height="172" rx="34" fill="${haut}" stroke="#E6D8CC" stroke-width="5"/>
      <path d="M86 220 Q86 186 118 186 L150 262 L182 186 Q214 186 214 220 V300 H86 Z" fill="${P}"/><path d="M88 296 H212 V338 Q212 356 190 356 H110 Q88 356 88 338 Z" fill="${FONCE}"/><path d="M88 296 H212" stroke="${C.or}" stroke-width="5"/>
      <path d="M150 196 L132 186 V206 Z M150 196 L168 186 V206 Z" fill="${C.or}"/><circle cx="150" cy="196" r="5" fill="${C.or}"/>`
    : `<rect x="84" y="184" width="132" height="172" rx="34" fill="${haut}"/><path d="M128 184 Q150 204 172 184" fill="none" stroke="${manche}" stroke-width="6" stroke-linecap="round"/>`;
  const coiffe = cuisine ? (role === "cheffe" ? `<path d="M94 122 C82 96 92 76 104 72 V118 Z M206 122 C218 96 208 76 196 72 V118 Z" fill="${chev}"/><circle cx="150" cy="176" r="0"/>` : "")
      + `<path d="M100 82 V56 C68 50 70 8 106 12 C116 -16 184 -16 194 12 C230 8 232 50 200 56 V82 Z" fill="#fff" stroke="#E6D8CC" stroke-width="5" stroke-linejoin="round"/><path d="M100 64 H200" stroke="#E6D8CC" stroke-width="4"/>`
    : role === "cliente" ? `<path d="M90 156 C68 60 130 40 150 50 C170 40 232 60 210 156 C212 112 196 86 150 84 C104 86 88 112 90 156 Z" fill="${chev}"/>`
    : `<path d="M92 106 C86 44 214 44 208 106 C196 78 104 78 92 106 Z" fill="${chev}"/>`;
  const visage = `<g class="py"><ellipse class="po" cx="130" cy="116" rx="7" ry="9" fill="${NOIR}"/><ellipse class="po" cx="170" cy="116" rx="7" ry="9" fill="${NOIR}"/></g>
    <g stroke="${NOIR}" stroke-width="5" stroke-linecap="round"><path class="psg" d="M118 98 H140"/><path class="psd" d="M160 98 H182"/></g>
    <ellipse cx="112" cy="136" rx="10" ry="6" fill="${ROSE}" opacity=".55"/><ellipse cx="188" cy="136" rx="10" ry="6" fill="${ROSE}" opacity=".55"/>
    <path class="pb" d="M132 148 Q150 157 168 148" fill="${NOIR}" stroke="${NOIR}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    ${role === "chef" && def.moustache !== false ? `<path d="M122 136 Q137 124 150 133 Q163 124 178 136 Q163 147 150 138 Q137 147 122 136 Z" fill="${assombri(chev, 0)}"/>` : ""}`;
  return `<svg class="perso" viewBox="0 -24 300 464" xmlns="http://www.w3.org/2000/svg" style="display:block;overflow:visible">
    <ellipse cx="150" cy="426" rx="${sombre ? 118 : 98}" ry="${sombre ? 15 : 10}" fill="${sombre ? "rgba(251,243,236,.13)" : "rgba(61,16,48,.13)"}"/>
    <rect x="112" y="336" width="26" height="76" fill="${jambe}"/><rect x="162" y="336" width="26" height="76" fill="${jambe}"/><ellipse cx="119" cy="415" rx="27" ry="11" fill="${pied}"/><ellipse cx="181" cy="415" rx="27" ry="11" fill="${pied}"/>
    <g class="ph">${gauche}${droit}<rect x="136" y="150" width="28" height="48" fill="${peau}"/>${torse}${tenu}<g class="pt"><circle cx="150" cy="114" r="58" fill="${peau}"/>${coiffe}${visage}</g></g></svg>`;
}

FAB.personnage = (def, x) => {
  const sc = x.sc, role = def.role || "chef", el = E("div", "el"), base = pose(el, def, {x: 540, y: 1100}) + (def.miroir ? " scaleX(-1)" : "");
  if (!ROLES.includes(role)) window.ALERTES.push(`scène ${x.i + 1} : personnage inconnu « ${role} » (${ROLES.join(", ")})`);
  el.innerHTML = personnageSVG(ROLES.includes(role) ? role : "client", def, x.th); el.firstChild.setAttribute("width", def.taille || 320);
  const q = s => el.querySelector(s), yeux = [...el.querySelectorAll(".po")], py = q(".py"), sg = q(".psg"), sd = q(".psd"), bouche = q(".pb"), haut = q(".ph"), tete = q(".pt"), svg = el.firstChild;
  const gs = (def.gestes || []).map(g => ({...g, t: heure(g.quand, sc, 0, x)})).sort((a, b) => a.t - b.t);
  const exs = [{t: -1e9, e: pexpr(def.expression)}].concat(gs.filter(g => g.expression).map(g => ({t: g.t, e: pexpr(g.expression)})));
  [def.expression, ...gs.map(g => g.expression)].forEach(n => { if (n && !PEXPR[n]) window.ALERTES.push(`scène ${x.i + 1} : expression de personnage inconnue « ${n} » (${Object.keys(PEXPR).join(", ")})`); });
  gs.forEach(g => { if (g.geste && !["saut", "non", "hoche"].includes(g.geste)) window.ALERTES.push(`scène ${x.i + 1} : geste de personnage inconnu « ${g.geste} » (saut, non, hoche)`); });
  const rg = {gauche: -4, droite: 4}[def.regard] || 0, cy = cycle(def, x, 0.2, "pop"), dec = 0.7 * (x.i + 1) + (def.x || 0) / 300;
  x.son(cy.t0, def.son);
  return {el, t0: cy.t0, type: "personnage", anim(u, t, ouv) {
    if (!applique(el, cy.etat(u), base)) return;
    let je = exs.length - 1; while (je > 0 && exs[je].t > u) je--;
    let e = exs[je].e;
    if (je > 0) { const k = (u - exs[je].t) / 0.16; if (k < 1) { const a = exs[je - 1].e, o = {}; for (const c in PEX0) o[c] = c === "rond" ? (k >= 0.5 ? e[c] : a[c]) : mel(a[c], e[c], clamp(k)); e = o; } }
    let gy = 0, gr = 0;
    for (const g of gs) { const a = u - g.t, k = a / (g.duree || 0.6); if (!g.geste || a < 0 || k > 1) continue;
      if (g.geste === "saut") gy -= 90 * Math.sin(Math.PI * k); else if (g.geste === "non") gr += 7 * Math.sin(5 * Math.PI * k) * (1 - 0.5 * k); else if (g.geste === "hoche") gy += 12 * Math.sin(4 * Math.PI * k) * (1 - k); }
    svg.style.transform = gy ? `translateY(${gy.toFixed(1)}px)` : "";
    const parle = def.parle && t >= sc.parle0 - 0.1 && t <= sc.parle1 + 0.1 ? ouv : 0;
    haut.setAttribute("transform", `translate(0 ${(3 * Math.sin(2 * Math.PI * (t + dec) / 1.9) - parle * 2).toFixed(2)})`);
    tete.setAttribute("transform", `rotate(${(1.5 * Math.sin(2 * Math.PI * (t + dec) / 2.7) + gr).toFixed(2)} 150 172)`);
    const cl = (t + dec) % 3.3, ferme = cl > 1.4 && cl < 1.53;
    yeux.forEach(o => o.setAttribute("ry", ferme ? 1.5 : e.ey)); py.setAttribute("transform", `translate(${rg} 0)`);
    sg.setAttribute("transform", `translate(0 ${e.sgY.toFixed(1)}) rotate(${e.sgA.toFixed(1)} 129 98)`); sd.setAttribute("transform", `translate(0 ${e.sdY.toFixed(1)}) rotate(${(-e.sdA).toFixed(1)} 171 98)`);
    if (e.rond) bouche.setAttribute("d", `M141 152 Q150 ${(144 - 3 * parle).toFixed(1)} 159 152 Q150 ${(162 + 10 * parle).toFixed(1)} 141 152 Z`);
    else { const sm = e.mb >= e.my; bouche.setAttribute("d", `M${150 - e.mw} ${e.my} Q150 ${(e.mb - (sm ? 16 : 6) * parle).toFixed(1)} ${150 + e.mw} ${e.my} Q150 ${(e.mb + (sm ? 12 : 16) * parle).toFixed(1)} ${150 - e.mw} ${e.my} Z`); }
  }};
};

// Plats illustrés (boîte 200 × 200) : de quoi donner faim sans photo.
const assiette = '<circle cx="100" cy="104" r="92" fill="#fff" stroke="#E6D8CC" stroke-width="6"/><circle cx="100" cy="104" r="66" fill="none" stroke="#F1E7DD" stroke-width="5"/>';
const PLATS = {
  pates: assiette + '<g transform="translate(100 106) scale(1.3) translate(-100 -106)"><g fill="none" stroke="#F0C55E" stroke-width="10" stroke-linecap="round"><path d="M62 108 C62 70 138 70 138 108 C138 140 62 140 62 108"/><path d="M76 106 C76 84 124 84 124 106 C124 126 76 126 76 106"/><path d="M90 104 C90 94 110 94 110 104"/></g><path d="M82 96 C92 80 118 82 120 100 C122 116 88 118 82 96 Z" fill="#C8452F"/><path d="M96 86 C104 72 120 78 112 92 Z" fill="#5FA052"/></g>',
  burger: '<path d="M30 92 C30 40 170 40 170 92 Z" fill="#E0A04A"/><g fill="#FBF3EC"><ellipse cx="72" cy="66" rx="6" ry="3"/><ellipse cx="104" cy="56" rx="6" ry="3"/><ellipse cx="134" cy="70" rx="6" ry="3"/></g><path d="M24 98 Q40 114 56 100 Q72 116 88 100 Q104 116 120 100 Q136 116 152 100 Q166 114 176 98 Z" fill="#6BAF5A"/><rect x="28" y="106" width="144" height="26" rx="13" fill="#6B3A2A"/><path d="M40 106 H160 L140 124 Z" fill="#F4C542"/><path d="M30 138 H170 C170 168 30 168 30 138 Z" fill="#E0A04A"/>',
  pizza: '<circle cx="100" cy="102" r="90" fill="#E0A04A"/><circle cx="100" cy="102" r="74" fill="#F3D27A"/><g fill="#C8452F"><circle cx="74" cy="76" r="13"/><circle cx="128" cy="84" r="13"/><circle cx="92" cy="128" r="13"/><circle cx="136" cy="134" r="11"/></g><g fill="#5FA052"><path d="M100 96 C108 84 120 92 112 104 Z"/><path d="M62 112 C70 100 82 108 74 120 Z"/><path d="M116 58 C124 46 136 54 128 66 Z"/></g><path d="M100 102 L164 54 M100 102 L188 110" stroke="#E0A04A" stroke-width="4"/>',
  salade: assiette + '<g fill="#6BAF5A"><ellipse cx="78" cy="100" rx="34" ry="24" transform="rotate(-20 78 100)"/><ellipse cx="122" cy="112" rx="34" ry="22" transform="rotate(24 122 112)"/></g><ellipse cx="100" cy="88" rx="30" ry="20" fill="#8CC56E"/><circle cx="84" cy="118" r="13" fill="#C8452F"/><circle cx="124" cy="86" r="11" fill="#C8452F"/><circle cx="106" cy="112" r="12" fill="#fff"/><circle cx="106" cy="112" r="6" fill="#F4C542"/>',
  soupe: '<ellipse cx="100" cy="150" rx="86" ry="14" fill="rgba(61,16,48,.12)"/><path d="M22 96 H178 C178 152 142 164 100 164 C58 164 22 152 22 96 Z" fill="#fff" stroke="#E6D8CC" stroke-width="6"/><ellipse cx="100" cy="96" rx="78" ry="20" fill="#E39A3B" stroke="#E6D8CC" stroke-width="6"/><path d="M84 92 C94 86 106 98 118 92" stroke="#FBF3EC" stroke-width="5" fill="none" stroke-linecap="round"/><g fill="none" stroke="#C9B8AA" stroke-width="6" stroke-linecap="round"><path d="M74 62 C66 50 82 44 74 30"/><path d="M104 60 C96 48 112 42 104 26"/><path d="M134 62 C126 50 142 44 134 30"/></g>',
  steak: assiette + '<path d="M54 94 C52 66 102 60 122 76 C140 90 128 130 96 132 C70 134 56 118 54 94 Z" fill="#7A4630"/><g stroke="#4E2A1C" stroke-width="5" stroke-linecap="round"><path d="M72 90 L96 114"/><path d="M88 80 L114 106"/></g><g fill="#F0C55E"><rect x="120" y="96" width="44" height="11" rx="5" transform="rotate(-24 142 101)"/><rect x="118" y="112" width="46" height="11" rx="5" transform="rotate(8 141 117)"/><rect x="112" y="128" width="42" height="11" rx="5" transform="rotate(-10 133 133)"/></g><circle cx="72" cy="138" r="9" fill="#5FA052"/>',
  poisson: assiette + '<path d="M48 104 C70 70 122 72 142 104 C122 136 70 138 48 104 Z" fill="#E8A27A"/><path d="M138 104 L166 82 V126 Z" fill="#E8A27A"/><circle cx="70" cy="98" r="5" fill="#3D1030"/><path d="M92 86 C100 98 100 110 92 122" stroke="#C97F58" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="118" cy="142" r="17" fill="#F4D24A" stroke="#E0B62E" stroke-width="4"/><path d="M118 126 V158 M102 142 H134" stroke="#E0B62E" stroke-width="3"/>',
  dessert: assiette + '<path d="M58 96 L128 70 L148 96 L74 124 Z" fill="#FFF7EC" stroke="#F1DEC4" stroke-width="3" stroke-linejoin="round"/><path d="M74 124 L148 96 V132 L74 160 Z" fill="#E8B56A"/><path d="M58 96 L74 124 V160 L58 132 Z" fill="#D39B4E"/><path d="M74 142 L148 114" stroke="#FFF7EC" stroke-width="7"/><circle cx="104" cy="88" r="12" fill="#C8452F"/><path d="M104 78 C108 66 118 64 122 70" stroke="#5FA052" stroke-width="4" fill="none" stroke-linecap="round"/>',
  cafe: '<ellipse cx="100" cy="150" rx="84" ry="16" fill="#fff" stroke="#E6D8CC" stroke-width="6"/><path d="M46 84 H154 V112 C154 140 132 150 100 150 C68 150 46 140 46 112 Z" fill="#fff" stroke="#E6D8CC" stroke-width="6"/><path d="M154 94 C182 90 182 128 150 126" fill="none" stroke="#E6D8CC" stroke-width="9"/><ellipse cx="100" cy="86" rx="50" ry="12" fill="#6B3A2A"/><g fill="none" stroke="#C9B8AA" stroke-width="6" stroke-linecap="round"><path d="M84 58 C76 46 92 40 84 26"/><path d="M116 58 C108 46 124 40 116 26"/></g>',
  glace: '<circle cx="78" cy="86" r="25" fill="#F6C9D4"/><circle cx="122" cy="86" r="25" fill="#F3E3B8"/><circle cx="100" cy="62" r="25" fill="#7A4630"/><rect x="126" y="24" width="13" height="58" rx="4" fill="#E0A04A" transform="rotate(24 132 53)"/><path d="M56 98 H144 L120 152 H80 Z" fill="#fff" stroke="#E6D8CC" stroke-width="6" stroke-linejoin="round"/><path d="M100 152 V172" stroke="#E6D8CC" stroke-width="8"/><path d="M72 176 H128" stroke="#E6D8CC" stroke-width="10" stroke-linecap="round"/>',
  fromage: '<ellipse cx="100" cy="150" rx="84" ry="12" fill="rgba(61,16,48,.12)"/><rect x="20" y="120" width="160" height="26" rx="13" fill="#B98552"/><path d="M40 120 H152 V72 Z" fill="#F4C542"/><path d="M40 120 L152 72 V60 Z" fill="#E0A82E"/><g fill="#E0A82E"><circle cx="122" cy="102" r="8"/><circle cx="138" cy="88" r="5"/><circle cx="98" cy="110" r="5"/></g><g fill="#5A1F4A"><circle cx="52" cy="110" r="9"/><circle cx="66" cy="104" r="9"/><circle cx="58" cy="96" r="9"/></g><path d="M58 88 C60 80 66 78 70 80" stroke="#5FA052" stroke-width="4" fill="none" stroke-linecap="round"/>',
  vin: '<path d="M62 24 H138 C142 84 124 108 100 108 C76 108 58 84 62 24 Z" fill="#fff" stroke="#E6D8CC" stroke-width="6"/><path d="M64 60 H136 C134 92 120 104 100 104 C80 104 66 92 64 60 Z" fill="#5A1F4A"/><path d="M100 108 V164" stroke="#E6D8CC" stroke-width="8"/><path d="M66 170 H134" stroke="#E6D8CC" stroke-width="10" stroke-linecap="round"/>'
};
FAB.plat = (def, x) => {
  const el = E("div", "el"), t = def.taille || 240, base = pose(el, def);
  if (!PLATS[def.nom]) window.ALERTES.push(`scène ${x.i + 1} : plat inconnu « ${def.nom} » (${Object.keys(PLATS).join(", ")})`);
  const dessin = `<svg viewBox="0 0 200 200" width="${t}" height="${t}" style="display:block;filter:drop-shadow(0 10px 14px rgba(42,10,32,.18))">${PLATS[def.nom] || assiette}</svg>`;
  // "fond" : un disque de couleur derrière le plat ; "badge" : une petite icône sur son coin.
  el.innerHTML = porte(def.fond ? `<div style="width:${t * 1.22}px;height:${t * 1.22}px;border-radius:50%;background:${coul(def.fond)};display:flex;align-items:center;justify-content:center">${dessin}</div>` : dessin, def, x, def.fond ? t * 1.22 : t * 0.9);
  const cy = cycle(def, x, 0.3, "pop"); x.son(cy.t0, def.son);
  const ba = badgeAnim(el, def, x, cy.t0);
  return {el, t0: cy.t0, type: "plat", anim(u) { applique(el, cy.etat(u), base); ba(u); }};
};
