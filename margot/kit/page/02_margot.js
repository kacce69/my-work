// ── Margot : poses, expressions, accessoires, gestes ───────────────────────────────────────────────
const P = C.prune;
const bras = (d, w = 32) => `<path d="${d}" fill="none" stroke="${P}" stroke-width="${w}" stroke-linecap="round"/>`;
const main = (cx, cy, r = 30) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${P}"/>`;
const balance = (amp, per) => u => amp * Math.sin(2 * Math.PI * u / per);

// Bras droit (à droite de l'image). b = bras, dessiné derrière le corps ; o = main et objet, dessinés devant ;
// piv = épaule ; a(u) = petit mouvement d'attente, en degrés.
const POSES = {
  bonjour: {b: bras("M650 446 C705 428 742 384 746 320") + main(746, 302, 31), o: "", piv: [655, 446], a: u => (u < 1.6 ? 15 : 5) * Math.sin(2 * Math.PI * (u < 1.6 ? 2.6 : 0.8) * u)},
  pouce: {b: bras("M650 470 C690 474 730 468 760 452"), o: `<rect x="752" y="356" width="24" height="90" rx="12" fill="${P}"/>` + main(766, 449, 34), piv: [655, 472], a: u => -4 + 4 * Math.sin(2 * Math.PI * u / 1.1)},
  carte: {b: bras("M650 478 C690 486 725 490 757 487", 30), o: `<rect x="737" y="307" width="160" height="208" rx="20" fill="${C.creme}" stroke="${C.or}" stroke-width="9"/><g stroke="${P}" stroke-width="9" stroke-linecap="round"><path d="M766 363H866"/><path d="M766 404H846"/><path d="M766 440H858"/></g>` + main(759, 487, 29), piv: [655, 472], a: balance(3, 1.6)},
  repos: {b: bras("M650 474 C700 490 722 520 716 566") + main(714, 581, 29), o: "", piv: [655, 474], a: null},
  index: {b: bras("M650 446 C705 428 742 384 746 320") + main(746, 302, 31) + `<rect x="735" y="214" width="22" height="82" rx="11" fill="${P}"/>`, o: "", piv: [655, 446], a: balance(5, 0.9)},
  pointe: {b: bras("M650 466 C700 472 750 464 798 452"), o: main(812, 449, 31) + `<rect x="832" y="438" width="72" height="22" rx="11" fill="${P}" transform="rotate(-5 812 449)"/>`, piv: [655, 466], a: balance(2.5, 1.2)},
  hanche: {b: bras("M650 442 C742 452 752 544 672 566"), o: main(664, 566, 29), piv: [655, 442], a: balance(1.2, 2)},
  leve: {b: bras("M650 440 C712 412 742 340 732 264") + main(732, 246, 31), o: "", piv: [655, 440], a: balance(5, 0.6)},
  hausse: {b: bras("M650 468 C700 500 750 482 778 440"), o: `<ellipse cx="786" cy="428" rx="36" ry="21" fill="${P}" transform="rotate(-15 786 428)"/>`, piv: [655, 468], a: balance(2, 1.4)},
  reflechit: {b: bras("M650 446 C722 426 726 306 668 262"), o: main(656, 252, 29), piv: [655, 446], a: balance(2.5, 0.55)},
  stop: {b: bras("M650 470 C700 474 742 452 770 424"), o: [-22, -8, 8, 22].map(r => `<rect x="778" y="330" width="16" height="62" rx="8" fill="${P}" transform="rotate(${r} 786 402)"/>`).join("") + main(786, 402, 42), piv: [655, 470], a: balance(1.5, 1.5)},
  telephone: {b: bras("M650 478 C690 486 725 490 757 487", 30), o: `<rect x="740" y="290" width="128" height="226" rx="24" fill="${ENCRE}"/><rect x="750" y="304" width="108" height="190" rx="12" fill="${C.creme}"/><g stroke="${P}" stroke-width="8" stroke-linecap="round"><path d="M768 336H838"/><path d="M768 366H824"/><path d="M768 396H834"/></g><rect x="768" y="430" width="72" height="34" rx="17" fill="${C.or}"/>` + main(759, 493, 29), piv: [655, 472], a: balance(3, 1.6)},
  loupe: {b: bras("M650 478 C690 486 725 490 757 487", 30), o: `<path d="M776 428 L760 484" stroke="${FONCE}" stroke-width="18" stroke-linecap="round"/><circle cx="806" cy="372" r="62" fill="rgba(255,255,255,.32)" stroke="${C.or}" stroke-width="16"/><path d="M772 356 A40 40 0 0 1 800 328" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".85"/>` + main(759, 487, 29), piv: [655, 472], a: balance(4, 1.4)},
  plateau: {b: bras("M650 470 C700 484 748 452 770 406"), o: main(772, 398, 29) + `<ellipse cx="792" cy="366" rx="106" ry="14" fill="${C.or}"/><path d="M714 360 C714 274 870 274 870 360 Z" fill="${C.creme}" stroke="${C.or}" stroke-width="8" stroke-linejoin="round"/><circle cx="792" cy="286" r="11" fill="${C.or}"/>`, piv: [655, 470], a: balance(1.5, 1.8)},
  panneau: {b: bras("M650 478 C690 486 725 490 772 487", 30), o: d => {
    const t = String(d.panneau || "").split("\n").slice(0, 2), n = Math.max(...t.map(l => l.length), 1), fs = Math.min(70, Math.floor(330 / n));
    return `<path d="M802 396 L790 484" stroke="${FONCE}" stroke-width="14" stroke-linecap="round"/><rect x="684" y="232" width="236" height="166" rx="18" fill="${C.creme}" stroke="${C.or}" stroke-width="9"/>`
      + t.map((l, k) => `<text x="802" y="${(315 + (k - (t.length - 1) / 2) * fs * 1.05).toFixed(0)}" text-anchor="middle" dominant-baseline="central" font-family="Fraunces,Georgia,serif" font-weight="900" font-size="${fs}" fill="${FONCE}">${esc(l)}</text>`).join("") + main(788, 487, 29);
  }, piv: [655, 472], a: balance(3, 1.6)}
};
// Bras gauche (à gauche de l'image).
const BRASG = {
  repos: {b: bras("M300 474 C250 490 228 520 234 566") + main(236, 581, 29), o: "", piv: [295, 474], a: null},
  leve: {b: bras("M300 440 C238 412 208 340 218 264") + main(218, 246, 31), o: "", piv: [295, 440], a: balance(-5, 0.6)},
  hausse: {b: bras("M300 468 C250 500 200 482 172 440"), o: `<ellipse cx="164" cy="428" rx="36" ry="21" fill="${P}" transform="rotate(15 164 428)"/>`, piv: [295, 468], a: balance(-2, 1.4)},
  hanche: {b: bras("M300 442 C208 452 198 544 278 566"), o: main(286, 566, 29), piv: [295, 442], a: balance(-1.2, 2)},
  pointe: {b: bras("M300 466 C250 472 200 464 152 452"), o: main(138, 449, 31) + `<rect x="46" y="438" width="72" height="22" rx="11" fill="${P}" transform="rotate(5 138 449)"/>`, piv: [295, 466], a: balance(-2.5, 1.2)}
};
const DOUBLE = {fete: {droite: "leve", gauche: "leve"}, hausse: {droite: "hausse", gauche: "hausse"}, hanches: {droite: "hanche", gauche: "hanche"}};
function normPose(p, x) {
  const n = !p ? {droite: "bonjour", gauche: "repos"} : typeof p === "string" ? {...(DOUBLE[p] || {droite: p, gauche: "repos"})} : {droite: p.droite || "repos", gauche: p.gauche || "repos"};
  if (!POSES[n.droite]) { window.ALERTES.push(`scène ${x.i + 1} : pose inconnue « ${n.droite} »`); n.droite = "bonjour"; }
  if (!BRASG[n.gauche]) { window.ALERTES.push(`scène ${x.i + 1} : pose du bras gauche inconnue « ${n.gauche} »`); n.gauche = "repos"; }
  return n;
}

// Expressions : écarts par rapport au visage neutre. sgA / sdA = angle des sourcils (positif = froncés), sgY / sdY = leur hauteur.
const EX0 = {ry: 50, rx: 41, pr: 1, px: 0, py: 0, lid: 0, sv: 0, sgA: 0, sdA: 0, sgY: 0, sdY: 0, mb: 536, my: 464, mw: 51, mt: 0, jo: 0, mmin: 0, arc: 0, coeurs: 0, rond: 0};
const EXPR = {
  neutre: {},
  joie: {sv: 1, sgA: -6, sdA: -6, sgY: -10, sdY: -10, mb: 550, mw: 58, jo: 0.8},
  rire: {arc: 1, sv: 1, sgA: -8, sdA: -8, sgY: -14, sdY: -14, mb: 558, mw: 62, jo: 1, mmin: 1},
  surprise: {ry: 57, rx: 44, pr: 0.72, sv: 1, sgA: -4, sdA: -4, sgY: -26, sdY: -26, rond: 1},
  doute: {lid: 0.36, px: 8, sv: 1, sgA: 12, sdA: -14, sgY: 2, sdY: -20, mb: 488, my: 478, mw: 40, mt: -10},
  triste: {ry: 46, py: 8, sv: 1, sgA: -16, sdA: -16, sgY: -2, sdY: -2, mb: 446, my: 488, mw: 44},
  colere: {ry: 43, lid: 0.22, sv: 1, sgA: 18, sdA: 18, sgY: 8, sdY: 8, mb: 450, my: 482, mw: 46},
  malice: {lid: 0.4, px: 9, py: 2, sv: 1, sgA: 8, sdA: -12, sgY: 0, sdY: -12, mb: 542, mw: 50, mt: -14},
  amour: {coeurs: 1, sv: 1, sgA: -6, sdA: -6, sgY: -12, sdY: -12, mb: 552, mw: 58, jo: 1}
};
const exprDe = nom => ({...EX0, ...(EXPR[nom] || {})});
const melE = (a, b, k) => { const o = {}; for (const c in EX0) o[c] = (c === "arc" || c === "coeurs" || c === "rond") ? (k >= 0.5 ? b[c] : a[c]) : mel(a[c], b[c], k); return o; };

const CHAPEAUX = {
  toque: `<path d="M372 190 V132 C318 128 310 58 372 60 C386 22 452 12 475 46 C498 12 564 22 578 60 C640 58 632 128 578 132 V190 Z" fill="#fff" stroke="#E6D8CC" stroke-width="7" stroke-linejoin="round"/><path d="M372 152 H578" stroke="#E6D8CC" stroke-width="7"/>`,
  couronne: `<path d="M372 190 L352 92 L420 138 L475 70 L530 138 L598 92 L578 190 Z" fill="#F4CF7E" stroke="#B9862F" stroke-width="8" stroke-linejoin="round"/><circle cx="352" cy="88" r="13" fill="#B9862F"/><circle cx="475" cy="64" r="13" fill="#B9862F"/><circle cx="598" cy="88" r="13" fill="#B9862F"/><circle cx="475" cy="154" r="12" fill="${ROUGE}"/>`,
  bonnet: `<path d="M318 192 C330 96 430 44 520 62 C600 78 660 130 690 214 C650 190 628 168 604 160 C596 170 596 180 596 192 Z" fill="#C8323C"/><rect x="302" y="158" width="312" height="52" rx="26" fill="#fff"/><circle cx="694" cy="226" r="27" fill="#fff"/>`,
  fete: `<path d="M392 188 L475 30 L558 188 Z" fill="${ROSE}" stroke="#C96078" stroke-width="6" stroke-linejoin="round"/><path d="M420 140 L530 140 M442 98 L508 98" stroke="${C.creme}" stroke-width="10"/><circle cx="475" cy="30" r="20" fill="${C.or}"/>`
};
const CASQUE = `<path d="M282 356 V300 C282 118 668 118 668 300 V356" fill="none" stroke="${ENCRE}" stroke-width="18" stroke-linecap="round"/><rect x="262" y="330" width="40" height="96" rx="16" fill="${ENCRE}"/><rect x="648" y="330" width="40" height="96" rx="16" fill="${ENCRE}"/><path d="M282 426 C282 500 330 524 392 514" fill="none" stroke="${ENCRE}" stroke-width="10" stroke-linecap="round"/><circle cx="402" cy="512" r="14" fill="${ENCRE}"/>`;

function margotSVG(id, dD, dG, acc, def) {
  const a = n => acc.includes(n), corps = a("masque") ? NOIR : P, obj = (reg, p) => typeof reg[p].o === "function" ? reg[p].o(def) : reg[p].o;
  return `<svg class="margot" viewBox="190 160 730 630" xmlns="http://www.w3.org/2000/svg"><g class="corps">
  <ellipse cx="475" cy="752" rx="200" ry="16" fill="rgba(61,16,48,.13)"/>
  <g class="jg"><rect x="390" y="620" width="36" height="102" fill="${FONCE}"/><ellipse cx="398" cy="737" rx="45" ry="19" fill="${FONCE}"/></g>
  <g class="jd"><rect x="524" y="620" width="36" height="102" fill="${FONCE}"/><ellipse cx="552" cy="737" rx="45" ry="19" fill="${FONCE}"/></g>
  <g class="haut">
  ${dG.map(p => `<g class="bg" data-p="${p}">${BRASG[p].b}</g>`).join("")}
  ${dD.map(p => `<g class="bras" data-p="${p}">${POSES[p].b}</g>`).join("")}
  <clipPath id="${id}"><rect x="293" y="178" width="364" height="484" rx="45"/></clipPath>
  <g clip-path="url(#${id})"><rect x="293" y="178" width="364" height="484" fill="${P}"/><rect x="293" y="178" width="364" height="92" fill="${C.or}"/></g>
  ${a("masque") ? `<g clip-path="url(#${id})"><rect x="293" y="324" width="364" height="112" fill="${NOIR}"/></g>` : ""}
  ${Object.keys(CHAPEAUX).filter(a).map(n => `<g>${CHAPEAUX[n]}</g>`).join("")}
  <g class="yeux"><ellipse class="oeil" cx="414" cy="380" rx="41" ry="50" fill="#fff"/><ellipse class="oeil" cx="536" cy="380" rx="41" ry="50" fill="#fff"/></g>
  <g class="pupilles"><g class="pg"><circle class="pu" cx="422" cy="388" r="21" fill="${NOIR}"/><circle class="re" cx="430" cy="378" r="7" fill="#fff"/></g><g class="pd"><circle class="pu" cx="544" cy="388" r="21" fill="${NOIR}"/><circle class="re" cx="552" cy="378" r="7" fill="#fff"/></g></g>
  <g class="coeurs" display="none" fill="${ROUGE}"><g transform="translate(388 354) scale(.56)">${ICONES.coeur.replace('fill="currentColor"', "")}</g><g transform="translate(510 354) scale(.56)">${ICONES.coeur.replace('fill="currentColor"', "")}</g></g>
  <g class="arcs" display="none" fill="none" stroke="#fff" stroke-width="15" stroke-linecap="round"><path d="M376 396 Q414 344 452 396"/><path d="M498 396 Q536 344 574 396"/></g>
  <rect class="pauG" x="368" y="328" width="92" height="0" fill="${corps}"/><rect class="pauD" x="490" y="328" width="92" height="0" fill="${corps}"/>
  <g class="sourcils" display="none" stroke="${C.creme}" stroke-width="12" stroke-linecap="round"><path class="sg" d="M380 306 H448"/><path class="sd" d="M502 306 H570"/></g>
  ${a("lunettes") ? `<g><rect x="360" y="336" width="108" height="78" rx="24" fill="#1d0a18"/><rect x="482" y="336" width="108" height="78" rx="24" fill="#1d0a18"/><rect x="462" y="352" width="26" height="13" fill="#1d0a18"/><path d="M293 356H362M588 356H657" stroke="#1d0a18" stroke-width="11"/><path d="M380 356l22 -8M502 356l22 -8" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".7"/></g>` : ""}
  <g class="joues" opacity="0"><ellipse cx="350" cy="454" rx="27" ry="15" fill="${ROSE}"/><ellipse cx="600" cy="454" rx="27" ry="15" fill="${ROSE}"/></g>
  <path class="bouche" d="M424 464 Q475 536 526 464" fill="${NOIR}" stroke="${C.creme}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
  <g stroke-width="13" stroke-linecap="round"><path d="M352 558H516" stroke="${C.creme}"/><path d="M554 558H598" stroke="${C.or}"/><path d="M352 606H476" stroke="${C.creme}"/><path d="M554 606H598" stroke="${C.or}"/></g>
  ${a("casque") ? `<g>${CASQUE}</g>` : ""}
  ${dG.map(p => obj(BRASG, p) ? `<g class="og" data-p="${p}">${obj(BRASG, p)}</g>` : "").join("")}
  ${dD.map(p => obj(POSES, p) ? `<g class="objet" data-p="${p}">${obj(POSES, p)}</g>` : "").join("")}
  </g></g></svg>`;
}

let NM = 0;
const GD = {saut: 0.55, hoche: 0.7, non: 0.75, sursaut: 0.45, penche: 1.2, tourne: 0.6, tremble: 0.6, rebond: 0.5, clin: 0.35, danse: 1.6};
const REGARDS = {face: [0, 0], gauche: [-13, 0], droite: [13, 0], haut: [0, -12], bas: [0, 12]};

FAB.margot = (def, x) => {
  const sc = x.sc, th = x.th, id = "b" + (NM++), acc = [].concat(def.accessoire || []);
  acc.forEach(n => { if (!["masque", "lunettes", "casque"].includes(n) && !CHAPEAUX[n]) window.ALERTES.push(`scène ${x.i + 1} : accessoire inconnu « ${n} »`); });
  const gs = (def.gestes || []).map(g => ({...g, t: heure(g.quand, sc, 0, x)})).sort((a, b) => a.t - b.t);
  gs.forEach(g => { if (g.geste && !GD[g.geste]) window.ALERTES.push(`scène ${x.i + 1} : geste inconnu « ${g.geste} »`); if (g.expression && !EXPR[g.expression]) window.ALERTES.push(`scène ${x.i + 1} : expression inconnue « ${g.expression} »`); });
  if (def.expression && !EXPR[def.expression]) window.ALERTES.push(`scène ${x.i + 1} : expression inconnue « ${def.expression} »`);
  const tq = heure(def.quand, sc, 0, x), t1 = def.jusqu != null ? heure(def.jusqu, sc, null, x) : null;
  const p0 = normPose(def.pose, x), suiteD = [{t: -1e9, p: p0.droite}], suiteG = [{t: -1e9, p: p0.gauche}];
  gs.filter(g => g.pose).forEach(g => {
    const n = normPose(g.pose, x);
    if (n.droite !== suiteD[suiteD.length - 1].p) suiteD.push({t: g.t, p: n.droite});
    if (n.gauche !== suiteG[suiteG.length - 1].p) suiteG.push({t: g.t, p: n.gauche});
  });
  const dD = [...new Set(suiteD.map(s => s.p))], dG = [...new Set(suiteG.map(s => s.p))];
  const wrap = E("div", "mg", ((def.disque ?? th.disque) ? '<div class="disque"></div>' : "") + margotSVG(id, dD, dG, acc, def));
  const q = s => wrap.querySelector(s), qa = s => [...wrap.querySelectorAll(s)];
  const R = {disque: q(".disque"), svg: q(".margot"), haut: q(".haut"), yeux: qa(".oeil"), yeuxG: q(".yeux"), pup: q(".pupilles"), pg: q(".pg"), pd: q(".pd"), pus: qa(".pu"), res: qa(".re"),
             coeurs: q(".coeurs"), arcs: q(".arcs"), pauG: q(".pauG"), pauD: q(".pauD"), sour: q(".sourcils"), sg: q(".sg"), sd: q(".sd"), joues: q(".joues"), bouche: q(".bouche"), jg: q(".jg"), jd: q(".jd")};
  const grp = {}; ["bg", "bras", "og", "objet"].forEach(c => qa("." + c).forEach(g => { grp[c + ":" + g.dataset.p] = g; }));

  const X0 = 540, Y0 = 1070.5, dep = [{t: -1e9, x: def.x ?? X0, y: def.y ?? Y0, s: def.taille ?? 1, d: 0}];
  gs.filter(g => g.deplace).forEach(g => { const pr = dep[dep.length - 1], d = g.deplace; dep.push({t: g.t, x: d.x ?? pr.x, y: d.y ?? pr.y, s: d.taille ?? pr.s, d: d.duree || 0.6}); });
  const perso = dep.length > 1 || def.x != null || def.y != null || def.taille != null || def.miroir;
  if (perso) wrap.style.transformOrigin = `${X0}px ${Y0}px`;
  const exs = [{t: -1e9, e: exprDe(def.expression)}].concat(gs.filter(g => g.expression).map(g => ({t: g.t, e: exprDe(g.expression)})));
  const regs = [{t: -1e9, r: def.regard || "face"}].concat(gs.filter(g => g.regard).map(g => ({t: g.t, r: g.regard})));
  const vec = (r, cx, cy, cs) => { if (typeof r === "string") return REGARDS[r] || [0, 0]; const dx = r.x - cx, dy = r.y - (cy - 150 * cs), n = Math.hypot(dx, dy) || 1; return [13 * dx / n, 12 * dy / n]; };
  const en = def.entree || "pop";
  let marchait = false;

  const brasAnim = (suite, reg, clsB, clsO, u) => {
    let j = suite.length - 1; while (j > 0 && suite[j].t > u) j--;
    const cur = suite[j], age = u - Math.max(cur.t, tq), prec = j > 0 ? suite[j - 1] : null;
    for (const p of new Set(suite.map(s => s.p))) {
      const pz = reg[p];
      let s = p === cur.p ? 1 : 0;
      if (prec && age < 0.36) { if (p === cur.p) s = age < 0.08 ? 0 : rebond((age - 0.08) / 0.28); else if (p === prec.p) s = clamp(1 - age / 0.12); }
      for (const g of [grp[clsB + ":" + p], grp[clsO + ":" + p]]) {
        if (!g) continue;
        if (s <= 0.001) { g.setAttribute("display", "none"); continue; }
        g.removeAttribute("display");
        const [px, py] = pz.piv;
        if (!pz.a && s === 1) { g.removeAttribute("transform"); continue; }
        const a = pz.a ? pz.a(p === cur.p ? age : 0) : 0;
        g.setAttribute("transform", (s === 1 ? "" : `translate(${px} ${py}) scale(${s.toFixed(3)}) translate(${-px} ${-py}) `) + `rotate(${a.toFixed(2)} ${px} ${py})`);
      }
    }
  };

  return {el: wrap, type: "margot", boite: () => R.svg.getBoundingClientRect(),
    anim(u, t, ouv) {
      const ue = u - tq;
      if (ue < 0 || (t1 != null && u > t1 + 0.3)) { wrap.style.display = "none"; return; }
      wrap.style.display = "";
      // Position et taille (déplacements)
      let k = dep.length - 1; while (k > 0 && dep[k].t > u) k--;
      let cx = dep[k].x, cy = dep[k].y, cs = dep[k].s, marche = 0;
      if (k > 0) { const a = dep[k - 1], b = dep[k], kk = douce((u - b.t) / b.d); cx = mel(a.x, b.x, kk); cy = mel(a.y, b.y, kk); cs = mel(a.s, b.s, kk); if (kk < 1) marche = u - b.t + 0.001; }
      if (perso) wrap.style.transform = `translate(${(cx - X0).toFixed(1)}px,${(cy - Y0).toFixed(1)}px) scale(${def.miroir ? -cs : cs},${cs})`;
      // Entrée
      let tf = "", op = 1;
      if (en === "pop") {
        const ent = rebond((ue - 0.05) / 0.5);
        tf = `translateY(${(1 - ent) * 90}px) scale(${0.82 + 0.18 * ent})`; op = clamp(ue / 0.15);
        if (R.disque) R.disque.style.transform = `scale(${sortie((ue - 0.02) / 0.4)})`;
      } else {
        const d = 1 - sortie(ue / 0.5);
        tf = en === "de-gauche" ? `translateX(${-d * 900}px)` : en === "de-droite" ? `translateX(${d * 900}px)` : en === "de-bas" ? `translateY(${d * 900}px)` : en === "tombe" ? `translateY(${-(1 - rebond(ue / 0.6)) * 1100}px)` : "";
        if (en === "fondu") op = clamp(ue / 0.3);
        if (R.disque) R.disque.style.transform = en === "aucune" ? "" : `scale(${sortie(ue / 0.4)})`;
      }
      if (t1 != null && u > t1) { const qf = (u - t1) / 0.3; op *= 1 - clamp(qf); tf += ` translateY(${(qf * 80).toFixed(1)}px)`; }
      // Gestes
      let gx = 0, gy = 0, gr = 0, gsx = 1, gsy = 1, clin = false, actif = false;
      for (const g of gs) {
        const a = u - g.t, ge = g.geste; if (!ge || a < 0) continue;
        const kk = a / (g.duree || GD[ge] || 0.6), f = g.force || 1; if (kk > 1) continue;
        actif = true;
        if (ge === "saut") { gy -= 150 * f * Math.sin(Math.PI * kk); gsy *= 1 + 0.07 * Math.sin(2 * Math.PI * kk); gsx *= 1 - 0.05 * Math.sin(2 * Math.PI * kk); }
        else if (ge === "hoche") { gy += 18 * f * Math.sin(4 * Math.PI * kk) * (1 - kk); gsy *= 1 - 0.03 * Math.sin(4 * Math.PI * kk) * (1 - kk); }
        else if (ge === "non") gr += 7 * f * Math.sin(5 * Math.PI * kk) * (1 - 0.5 * kk);
        else if (ge === "sursaut") { const h = Math.sin(Math.PI * kk); gy -= 44 * f * h; gsx *= 1 + 0.1 * h; gsy *= 1 + 0.1 * h; }
        else if (ge === "penche") gr += (g.cote === "gauche" ? -9 : 9) * f * Math.min(1, kk * 6, (1 - kk) * 6);
        else if (ge === "tourne") gr += 360 * douce(kk);
        else if (ge === "tremble") gx += 8 * f * Math.sin(a * 60) * (1 - kk);
        else if (ge === "rebond") gy -= 48 * f * Math.abs(Math.sin(2 * Math.PI * kk)) * (1 - kk);
        else if (ge === "danse") { gr += 7 * f * Math.sin(2 * Math.PI * 2 * kk); gy -= 30 * f * Math.abs(Math.sin(2 * Math.PI * 2 * kk)); }
        else if (ge === "clin") clin = true;
      }
      if (actif && (gx || gy || gr || gsx !== 1 || gsy !== 1))
        tf += ` translate(${gx.toFixed(1)}px,${gy.toFixed(1)}px) translateY(250px) rotate(${gr.toFixed(2)}deg) scale(${gsx.toFixed(4)},${gsy.toFixed(4)}) translateY(-250px)`;
      R.svg.style.transform = tf; R.svg.style.opacity = op;
      // Corps, bras
      const parle = def.parle !== false && t >= sc.parle0 - 0.1 && t <= sc.parle1 + 0.1 ? ouv : 0;
      const bob = 5 * Math.sin(2 * Math.PI * t / 1.7), rot = 1.2 * Math.sin(2 * Math.PI * t / 2.3);
      R.haut.setAttribute("transform", `translate(0 ${(bob - parle * 3).toFixed(2)}) rotate(${rot.toFixed(2)} 475 640)`);
      brasAnim(suiteD, POSES, "bras", "objet", u); brasAnim(suiteG, BRASG, "bg", "og", u);
      if (marche || marchait) {
        const w = marche ? 22 * Math.sin(2 * Math.PI * 3.2 * marche) : 0;
        R.jg.setAttribute("transform", `translate(0 ${(-Math.max(0, w)).toFixed(1)})`); R.jd.setAttribute("transform", `translate(0 ${(-Math.max(0, -w)).toFixed(1)})`);
        marchait = !!marche;
      }
      // Visage
      let je = exs.length - 1; while (je > 0 && exs[je].t > u) je--;
      let e = exs[je].e;
      if (je > 0) { const kk = (u - exs[je].t) / 0.16; if (kk < 1) e = melE(exs[je - 1].e, e, clamp(kk)); }
      const cl = (t + 0.4 * x.i) % 2.9, ferme = cl > 1.1 && cl < 1.24 && !(x.i === 0 && t > sc.fin - 0.6);   // pas de clin d'œil sur l'image de couverture
      R.yeux.forEach((o, j) => { o.setAttribute("ry", ferme || (clin && j === 1) ? 5 : e.ry); o.setAttribute("rx", e.rx); });
      R.pup.setAttribute("opacity", ferme ? 0 : 1);
      let jr = regs.length - 1; while (jr > 0 && regs[jr].t > u) jr--;
      let [vx, vy] = vec(regs[jr].r, cx, cy, cs);
      if (jr > 0) { const kk = sortie((u - regs[jr].t) / 0.18); if (kk < 1) { const [ax, ay] = vec(regs[jr - 1].r, cx, cy, cs); vx = mel(ax, vx, kk); vy = mel(ay, vy, kk); } }
      if (def.miroir) vx = -vx;
      R.pup.setAttribute("transform", `translate(${(3 * Math.sin(t * 0.9) + vx + e.px).toFixed(2)} ${(2 * Math.cos(t * 0.7) + vy + e.py).toFixed(2)})`);
      R.pus.forEach(p => p.setAttribute("r", 21 * e.pr)); R.res.forEach(p => p.setAttribute("r", 7 * e.pr));
      if (e.arc) { R.yeuxG.setAttribute("display", "none"); R.arcs.removeAttribute("display"); } else { R.yeuxG.removeAttribute("display"); R.arcs.setAttribute("display", "none"); }
      const sansPup = e.arc || e.coeurs;
      if (sansPup) R.pg.setAttribute("display", "none"); else R.pg.removeAttribute("display");
      if (sansPup || clin) R.pd.setAttribute("display", "none"); else R.pd.removeAttribute("display");
      if (e.coeurs && !ferme) R.coeurs.removeAttribute("display"); else R.coeurs.setAttribute("display", "none");
      const hp = e.lid > 0.01 ? e.lid * 2 * e.ry + 2 : 0;
      R.pauG.setAttribute("y", 378 - e.ry); R.pauG.setAttribute("height", hp); R.pauD.setAttribute("y", 378 - e.ry); R.pauD.setAttribute("height", hp);
      if (e.sv > 0.05) {
        R.sour.removeAttribute("display"); R.sour.setAttribute("opacity", e.sv);
        R.sg.setAttribute("transform", `translate(0 ${e.sgY.toFixed(1)}) rotate(${e.sgA.toFixed(1)} 414 306)`); R.sd.setAttribute("transform", `translate(0 ${e.sdY.toFixed(1)}) rotate(${(-e.sdA).toFixed(1)} 536 306)`);
      } else R.sour.setAttribute("display", "none");
      R.joues.setAttribute("opacity", (e.jo * 0.62).toFixed(2));
      const pb = Math.max(parle, e.mmin * 0.3);
      if (e.rond) R.bouche.setAttribute("d", `M449 492 Q475 ${(466 - 8 * pb).toFixed(1)} 501 492 Q475 ${(522 + 26 * pb).toFixed(1)} 449 492 Z`);
      else {
        const sm = e.mb >= e.my, haut = e.mb - (sm ? 70 : 28) * pb, bas = e.mb + (sm ? 30 : 62) * pb, r1 = v => +v.toFixed(1);
        R.bouche.setAttribute("d", `M${r1(475 - e.mw)} ${r1(e.my)} Q475 ${haut.toFixed(1)} ${r1(475 + e.mw)} ${r1(e.my + e.mt)} Q475 ${bas.toFixed(1)} ${r1(475 - e.mw)} ${r1(e.my)} Z`);
      }
    }};
};
