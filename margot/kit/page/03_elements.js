// ── Éléments : chaque fabrique renvoie {el, anim(u, t, ouv), ajuste?()} ───────────────────────────
// u = secondes depuis le début de la scène, t = secondes depuis le début du Reel, ouv = ouverture de la bouche (0..1).

FAB.etiquette = (def, x) => {
  const el = E("div", "tag", `<span style="background:${x.th.tagF};color:${x.th.tagT}">${esc(def.texte ?? D.etiquette)}</span>`);
  return {el, type: "etiquette", anim(u) { el.style.opacity = clamp((u - 0.1) / 0.3); }};
};

FAB.titre = (def, x) => {
  const th = x.th, sc = x.sc, lignes = [].concat(def.lignes ?? def.texte ?? []).filter(l => l != null && l !== "").map(String);
  const anime = def.anime || "lignes", parMots = anime === "mots" || anime === "voix", textes = lignes.map(l => l.replace(/\*/g, ""));
  const el = E("div", def.legacy ? "titre" + (def.petit ? " petit" : "") : "el tt");
  el.style.color = coul(def.couleur, th.titre);
  if (!def.legacy) { pose(el, def, {haut: 312, l: 952}); el.style.fontSize = (def.taille || 104) + "px"; if (def.aligne) el.style.textAlign = def.aligne; }
  el.innerHTML = lignes.map((l, j) => `<div>${anime === "machine" ? `<span class="vu"></span><span class="cache">${esc(textes[j])}</span>` : parMots ? motsRiches(l, th) : riche(l, th)}</div>`).join("");
  const divs = [...el.children], t0 = heure(def.quand, sc, 0.16, x), t1 = def.jusqu != null ? heure(def.jusqu, sc, null, x) : null;
  let ms = [], hm = [];
  if (parMots) { ms = [...el.querySelectorAll(".m")]; hm = anime === "voix" ? heuresVoix(ms.map(m => m.textContent), sc, t0) : ms.map((_, j) => t0 + (def.pas || 0.09) * j); }
  return {el, type: "titre", t0,
    ajuste() {                                             // réduit un titre trop large jusqu'à ce que chaque ligne tienne
      let taille = parseFloat(getComputedStyle(el).fontSize);
      divs.forEach(l => { l.style.whiteSpace = "nowrap"; });
      while (taille > (def.mini || 60) && divs.some(l => l.scrollWidth > el.clientWidth)) { taille -= 4; el.style.fontSize = taille + "px"; }
      if (divs.some(l => l.scrollWidth > el.clientWidth)) window.ALERTES.push(`scène ${x.i + 1} : titre trop long`);
      if (def.legacy && el.getBoundingClientRect().bottom > 700) window.ALERTES.push(`scène ${x.i + 1} : titre trop haut (${divs.length} lignes)`);
    },
    anim(u) {
      if (t1 != null) { const q = (u - t1) / 0.25; if (q >= 1) { el.style.display = "none"; return; } el.style.display = ""; el.style.opacity = q > 0 ? 1 - q : 1; }
      if (parMots) ms.forEach((m, j) => { const k = (u - hm[j]) / 0.3; m.style.opacity = clamp(k * 3); m.style.transform = `translateY(${((1 - sortie(k)) * 34).toFixed(1)}px) scale(${k <= 0 ? 0.7 : (0.7 + 0.3 * rebond(k)).toFixed(3)})`; });
      else if (anime === "machine") { let n = Math.max(0, Math.floor((u - t0) * (def.vitesse || 26))); divs.forEach((l, j) => { const v = Math.min(textes[j].length, n); n -= v; l.firstChild.textContent = textes[j].slice(0, v); l.lastChild.textContent = textes[j].slice(v); }); }
      else if (anime !== "fixe") divs.forEach((l, j) => { const k = sortie((u - t0 - 0.12 * j) / 0.4); l.style.opacity = k; l.style.transform = `translateY(${(1 - k) * 56}px)`; });   // "fixe" : là dès la première image
    }};
};

FAB.texte = (def, x) => {
  const th = x.th, st = def.style || "simple", el = E("div", "el"), base = pose(el, def, {l: st === "pastille" ? null : 900});
  const c = coul(def.couleur, st === "carton" ? th.carteT : st === "pastille" ? th.puceT : st === "doux" ? th.doux : th.titre);
  const fond = st === "pastille" ? `background:${coul(def.fond, th.puceF)};` : st === "carton" ? `background:${coul(def.fond, th.carte)};` : "";
  el.innerHTML = `<div class="tx ${st}" style="font-size:${def.taille || 48}px;color:${c};${fond}${def.aligne ? `text-align:${def.aligne};` : ""}${def.leger ? "font-weight:500;" : ""}">${[].concat(def.texte ?? "").map(l => riche(l, st === "carton" ? THEME.creme : th)).join("<br>")}</div>`;
  const cy = cycle(def, x, 0.3, "monte"); x.son(cy.t0, def.son);
  return {el, type: "texte", anim(u) { applique(el, cy.etat(u), base); }};
};

FAB.puces = (def, x) => {
  const th = x.th, sc = x.sc, el = E("div", "puces", (def.items || []).map(p => `<span style="background:${th.puceF};color:${th.puceT}">${esc(p)}</span>`).join(""));
  if (def.haut != null) el.style.top = def.haut + "px";
  const ps = [...el.children], n = ps.length, t0 = def.quand != null ? heure(def.quand, sc, null, x) : null;
  return {el, type: "puces",
    ajuste() { if (def.legacy && n && el.getBoundingClientRect().bottom > 760) window.ALERTES.push(`scène ${x.i + 1} : puces sur plus d'une ligne`); },
    anim(u, t) {
      const span = sc.parle1 - sc.parle0;
      ps.forEach((p, j) => { const k = t0 != null ? (u - t0 - 0.18 * j) / 0.3 : (t - (sc.parle0 + span * j / n + 0.05)) / 0.3; p.style.opacity = clamp(k * 2); p.style.transform = `scale(${k <= 0 ? 0.6 : 0.6 + 0.4 * rebond(k)})`; });
    }};
};

FAB.liste = (def, x) => {
  const th = x.th, sc = x.sc, el = E("div", "el liste"), base = pose(el, def, {haut: 560, l: 880});
  const items = (def.items || []).map(it => typeof it === "string" ? {texte: it} : it), n = items.length, p0 = sc.parle0 - sc.debut, span = sc.parle1 - sc.parle0;
  el.innerHTML = items.map((it, j) => {
    const pu = it.puce || def.puce || "coche";
    const [f, c, dedans] = pu === "numero" ? [th.puceF, th.puceT, j + 1] : pu === "croix" ? [ROUGE, "#fff", ico("croix", 50, "#fff", 13)] : pu === "coche" ? [VERT, "#fff", ico("coche", 50, "#fff", 13)]
      : pu === "point" ? [th.puceF, th.puceT, ""] : [th.puceF, th.puceT, ico(pu, 52, th.puceT, 9)];
    return `<div class="it"><div class="pu" style="background:${f};color:${c}">${dedans}</div><div class="lt" style="color:${th.titre};font-size:${def.taille || 56}px">${riche(it.texte, th)}</div></div>`;
  }).join("");
  const rangs = [...el.children], ts = items.map((it, j) => it.quand != null ? heure(it.quand, sc, null, x) : p0 + span * j / n + 0.05);
  ts.forEach(t => x.son(t, def.son === undefined ? "tic" : def.son));
  return {el, type: "liste", instants: ts.map((t, j) => ({t, el: rangs[j]})), anim(u) {
    rangs.forEach((r, j) => { const k = (u - ts[j]) / 0.35; r.style.opacity = clamp(k * 2.5); r.style.transform = `translateX(${((1 - sortie(k)) * -70).toFixed(1)}px)`; r.firstChild.style.transform = `scale(${k <= 0 ? 0 : rebond(k).toFixed(3)})`; });
  }};
};

FAB.chiffre = (def, x) => {
  const th = x.th, el = E("div", "el chf"), base = pose(el, def, {haut: 330, l: 980});
  const v1 = +def.valeur, v0 = +(def.depuis ?? 0), dec = def.decimales || 0, dur = def.duree || 1.1;
  const fmt = v => v.toLocaleString("fr-FR", {minimumFractionDigits: dec, maximumFractionDigits: dec}).replace(/[  ]/g, " ");
  el.innerHTML = `<div class="nb" style="color:${coul(def.couleur, th.titre)};font-size:${def.taille || 300}px"><span class="pre">${esc(def.prefixe || "")}</span><span class="v">${fmt(v0)}</span><span class="suf">${esc(def.suffixe || "")}</span></div>`
    + (def.jauge ? `<div class="jg" style="background:${th.voile}"><div style="background:${th.trait};width:0"></div></div>` : "")
    + (def.legende ? `<div class="lg" style="color:${th.titre}">${riche(def.legende, th)}</div>` : "")
    + (def.source ? `<div class="src" style="color:${th.doux}">Source : ${esc(def.source)}</div>` : def.exemple ? `<div class="src" style="color:${th.doux}">Exemple</div>` : "");
  if (!def.source && !def.exemple) window.ALERTES.push(`scène ${x.i + 1} : chiffre sans source (ajoutez "source", ou "exemple": true si c'est un exemple présenté comme tel)`);
  const v = el.querySelector(".v"), jg = el.querySelector(".jg div"), lg = el.querySelector(".lg"), cy = cycle(def, x, 0.3, "pop");
  if (def.son !== false) { x.son(cy.t0 + 0.15, "compte"); x.son(cy.t0 + 0.15 + dur, "ding"); }
  return {el, type: "chiffre", anim(u) {
    if (!applique(el, cy.etat(u), base)) return;
    const k = sortie((u - cy.t0 - 0.15) / dur);
    v.textContent = fmt(mel(v0, v1, k));
    if (jg) jg.style.width = (100 * k * v1 / (def.sur || 100)).toFixed(1) + "%";
    if (lg) { const kl = sortie((u - cy.t0 - 0.35) / 0.4); lg.style.opacity = kl; lg.style.transform = `translateY(${((1 - kl) * 30).toFixed(1)}px)`; }
  }};
};

FAB.barres = (def, x) => {
  const th = x.th, el = E("div", "el bar"), base = pose(el, def, {haut: 560, l: 880});
  const ds = def.donnees || [], max = def.max || Math.max(...ds.map(d => d.valeur), 1), dec = def.decimales || 0;
  const ecrit = v => v.toLocaleString("fr-FR", {minimumFractionDigits: dec, maximumFractionDigits: dec}).replace(/[\u202f\u00a0]/g, "\u2009") + (def.unite || ""), lmax = Math.max(...ds.map(d => ecrit(d.valeur).length), 1);
  el.innerHTML = ds.map(d => `<div class="ln"><div class="nm" style="color:${th.titre}">${esc(d.nom)}</div><div class="rg"><div class="pi" style="background:${th.voile}"><div class="re" style="background:${d.accent ? th.trait : th.doux}"></div></div><div class="va" style="color:${th.titre};min-width:${(lmax * 0.56 + 0.3).toFixed(1)}em"></div></div></div>`).join("")
    + (def.source ? `<div class="src" style="color:${th.doux}">Source : ${esc(def.source)}</div>` : def.exemple ? `<div class="src" style="color:${th.doux}">Exemple</div>` : "");
  if (!def.source && !def.exemple) window.ALERTES.push(`scène ${x.i + 1} : barres sans source (ajoutez "source", ou "exemple": true)`);
  const rangs = [...el.querySelectorAll(".ln")].map(r => [r, r.querySelector(".re"), r.querySelector(".va")]), t0 = heure(def.quand, x.sc, 0.4, x);
  ds.forEach((_, j) => x.son(t0 + 0.28 * j, def.son === undefined ? "glisse" : def.son));
  return {el, type: "barres", instants: rangs.map((r, j) => ({t: t0 + 0.28 * j, el: r[0]})), anim(u) {
    rangs.forEach(([r, re, va], j) => {
      const a = u - t0 - 0.28 * j, k = sortie(a / 0.8), w = 100 * k * ds[j].valeur / max;
      r.style.opacity = clamp(a / 0.2); re.style.width = w.toFixed(1) + "%";
      va.textContent = ecrit(k * ds[j].valeur);
    });
  }};
};

// Badge : une petite icône ronde posée sur le coin haut-droit d'une icône ou d'un plat. "badge" : le nom de l'icône ;
// "badge_quand" : l'instant où il arrive (par défaut 0,3 s après l'élément). D = le diamètre de ce qui le porte.
function badgeHTML(def, x, D) {
  if (!def.badge) return "";
  if (!ICONES[def.badge]) window.ALERTES.push(`scène ${x.i + 1} : icône inconnue « ${def.badge} »`);
  const bd = Math.round(Math.max(72, D * 0.3)), k = D / 2 * Math.SQRT1_2, clair = x.sc.fond === "or";
  return `<div class="bdg" style="position:absolute;left:${(D / 2 + k - bd / 2).toFixed(0)}px;top:${(D / 2 - k - bd / 2).toFixed(0)}px;width:${bd}px;height:${bd}px;border-radius:50%;background:${clair ? C.creme : C.or};`
    + `box-shadow:0 6px 14px rgba(42,10,32,.25);display:flex;align-items:center;justify-content:center">${ico(def.badge, Math.round(bd * 0.56), FONCE, 10)}</div>`;
}
function badgeAnim(el, def, x, t0) {
  const b = el.querySelector(".bdg");
  if (!b) return () => {};
  const tb = def.badge_quand != null ? heure(def.badge_quand, x.sc, null, x) : t0 + 0.3;
  if (def.son !== false) x.son(tb, "bulle", 0.6);
  return u => { const k = (u - tb) / 0.3; b.style.transform = `scale(${k <= 0 ? 0 : rebond(k).toFixed(3)})`; };
}
const porte = (dessin, def, x, D) => def.badge ? `<div style="position:relative;width:${D}px;height:${D}px;display:flex;align-items:center;justify-content:center">${dessin}${badgeHTML(def, x, D)}</div>` : dessin;

FAB.icone = (def, x) => {
  const el = E("div", "el"), t = def.taille || 160, base = pose(el, def), c = coul(def.couleur, x.th.trait);
  if (!ICONES[def.nom]) window.ALERTES.push(`scène ${x.i + 1} : icône inconnue « ${def.nom} »`);
  el.innerHTML = porte(def.fond ? `<div style="width:${t * 1.6}px;height:${t * 1.6}px;border-radius:50%;background:${coul(def.fond)};display:flex;align-items:center;justify-content:center">${ico(def.nom, t, c, def.ep)}</div>` : ico(def.nom, t, c, def.ep),
    def, x, def.fond ? t * 1.6 : t);
  const cy = cycle(def, x, 0.3, "pop"); x.son(cy.t0, def.son);
  const ba = badgeAnim(el, def, x, cy.t0);
  return {el, t0: cy.t0, type: "icone", anim(u) { applique(el, cy.etat(u), base); ba(u); }};
};

// Trait dessiné à la main : flèche, cercle, soulignement, trait, croix (coordonnées de la scène, 1080 × 1920).
FAB.forme = (def, x) => {
  const el = E("div", "el plein"), c = coul(def.couleur, x.th.trait), [x0, y0] = def.de || [300, 900], [x1, y1] = def.a || [780, 900];
  let d, tete = "";
  if (def.forme === "fleche") {
    const cb = def.courbe ?? 0.25, mx = (x0 + x1) / 2 + cb * (y1 - y0), my = (y0 + y1) / 2 - cb * (x1 - x0), a = Math.atan2(y1 - my, x1 - mx), L = def.pointe || 46;
    d = `M${x0} ${y0} Q${mx} ${my} ${x1} ${y1}`;
    tete = `M${(x1 - L * Math.cos(a - 0.5)).toFixed(1)} ${(y1 - L * Math.sin(a - 0.5)).toFixed(1)} L${x1} ${y1} L${(x1 - L * Math.cos(a + 0.5)).toFixed(1)} ${(y1 - L * Math.sin(a + 0.5)).toFixed(1)}`;
  } else if (def.forme === "cercle") {
    const cx = def.x ?? 540, cy = def.y ?? 960, rx = def.rx || 220, ry = def.ry || 90;
    d = `M${cx - rx} ${cy} C${cx - rx} ${cy - ry * 1.32} ${cx + rx} ${cy - ry * 1.32} ${cx + rx} ${cy} C${cx + rx} ${cy + ry * 1.32} ${cx - rx} ${cy + ry * 1.32} ${cx - rx * 1.05} ${cy - 16}`;
  } else if (def.forme === "soulignement") d = `M${x0} ${y0} Q${(3 * x0 + x1) / 4} ${y0 - 18} ${(x0 + x1) / 2} ${(y0 + y1) / 2} T${x1} ${y1}`;
  else if (def.forme === "croix") { const cx = def.x ?? 540, cy = def.y ?? 960, r = def.r || 80; d = `M${cx - r} ${cy - r} L${cx + r} ${cy + r} M${cx + r} ${cy - r} L${cx - r} ${cy + r}`; }
  else d = `M${x0} ${y0} L${x1} ${y1}`;
  el.innerHTML = `<svg width="1080" height="1920" viewBox="0 0 1080 1920" fill="none" stroke="${c}" stroke-width="${def.ep || 12}" stroke-linecap="round" stroke-linejoin="round"><path class="p" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="${d}"/>${tete ? `<path class="h" d="${tete}"/>` : ""}</svg>`;
  const p = el.querySelector(".p"), h = el.querySelector(".h"), t0 = heure(def.quand, x.sc, 0.4, x), dur = def.duree || 0.5, t1 = def.jusqu != null ? heure(def.jusqu, x.sc, null, x) : null;
  x.son(t0, def.son);
  return {el, type: "forme", zone: false, anim(u) {
    const k = (u - t0) / dur;
    if (k <= 0 || (t1 != null && u > t1 + 0.25)) { el.style.display = "none"; return; }
    el.style.display = ""; el.style.opacity = t1 != null && u > t1 ? 1 - (u - t1) / 0.25 : 1;
    p.setAttribute("stroke-dashoffset", (1 - sortie(k)).toFixed(4)); if (h) h.style.opacity = k > 0.8 ? 1 : 0;
  }};
};

FAB.image = (def, x) => {
  const el = E("div", "el"), base = pose(el, def, {l: 800}), z = def.zoom || [1, 1.08];
  el.innerHTML = `<div class="img ${def.cadre || "arrondi"}" style="height:${def.h || 600}px"><img src="${esc(def.src || "")}" style="object-fit:${def.ajuste || "cover"};object-position:${def.position || "50% 50%"}"></div>${def.legende ? `<div class="imgl" style="color:${x.th.titre}">${esc(def.legende)}</div>` : ""}`;
  const im = el.querySelector("img"), cy = cycle(def, x, 0.25, "pop"); x.son(cy.t0, def.son);
  im.onerror = () => window.ALERTES.push(`scène ${x.i + 1} : image introuvable (${def.src})`);
  return {el, type: "image", anim(u) {
    if (!applique(el, cy.etat(u), base)) return;
    im.style.transform = `scale(${mel(z[0], z[1], clamp((u - cy.t0) / Math.max(1, x.sc.fin - x.sc.debut - cy.t0))).toFixed(4)})`;
  }};
};

FAB.bulle = (def, x) => {
  const th = x.th, el = E("div", "el"), base = pose(el, def), f = coul(def.fond, th.carte), txt = String(def.texte || "");
  el.style.width = "max-content"; el.style.maxWidth = (def.l || 640) + "px";
  el.innerHTML = `<div class="bul q-${def.queue || "bas-gauche"}" style="background:${f};color:${coul(def.couleur, th.carteT)};font-size:${def.taille || 46}px;--f:${f}"><span class="vu"></span><span class="cache"></span></div>`;
  const vu = el.querySelector(".vu"), ca = el.querySelector(".cache"), cy = cycle(def, x, 0.3, "pop");
  x.son(cy.t0, def.son === undefined ? "bulle" : def.son);
  return {el, type: "bulle", anim(u) {
    if (!applique(el, cy.etat(u), base)) return;
    const n = def.machine ? clamp(Math.floor((u - cy.t0 - 0.2) * (def.vitesse || 30)), 0, txt.length) : txt.length;
    vu.textContent = txt.slice(0, n); ca.textContent = txt.slice(n);
  }};
};

let NAV = 0;
function avatarSVG(role, t, th) {
  const id = "av" + (NAV++), f = th.puceF, c = th.puceT;
  return `<svg width="${t}" height="${t}" viewBox="0 0 100 100" style="display:block"><clipPath id="${id}"><circle cx="50" cy="50" r="50"/></clipPath><g clip-path="url(#${id})"><rect width="100" height="100" fill="${f}"/><circle cx="50" cy="42" r="18" fill="${c}"/><path d="M14 104 C14 62 86 62 86 104 Z" fill="${c}"/>`
    + (role === "chef" ? `<path d="M34 30 C22 30 22 13 35 15 C38 3 62 3 65 15 C78 13 78 30 66 30 V37 H34 Z" fill="#fff" stroke="${c}" stroke-width="2"/>` : "") + `</g></svg>`;
}
FAB.avatar = (def, x) => {
  const el = E("div", "el"), base = pose(el, def); el.innerHTML = avatarSVG(def.role || "client", def.taille || 150, x.th);
  const cy = cycle(def, x, 0.25, "pop");
  return {el, type: "avatar", anim(u) { applique(el, cy.etat(u), base); }};
};

FAB.tampon = (def, x) => {
  const el = E("div", "el"), base = pose(el, def), c = coul(def.couleur, /faux|non|stop|erreur/i.test(def.texte || "") ? ROUGE : VERT);
  el.innerHTML = `<div class="tamp" style="color:${c};border-color:${c};font-size:${def.taille || 120}px">${esc(def.texte || "FAUX")}</div>`;
  const t0 = heure(def.quand, x.sc, {part: 0.6}, x);
  x.son(t0 + 0.1, def.son === undefined ? "tampon" : def.son); if (def.secousse !== false) x.secousse(t0 + 0.12);
  return {el, type: "tampon", anim(u) {
    const a = u - t0; if (a < 0) { el.style.display = "none"; return; }
    const k = clamp(a / 0.16); el.style.display = ""; el.style.opacity = clamp(k * 3);
    el.style.transform = `${base} rotate(${def.angle ?? -9}deg) scale(${(1 + (1 - k * k) * 1.8).toFixed(3)})`;
  }};
};

FAB.carton = (def, x) => {
  const th = x.th, el = E("div", "el"), base = pose(el, def, {l: 452}), ton = def.ton || "neutre", cb = ton === "plus" ? VERT : ton === "moins" ? ROUGE : th.puceF;
  el.innerHTML = `<div class="crt" style="background:${th.carte};color:${th.carteT};border-color:${ton === "neutre" ? "transparent" : cb}${def.icone ? "" : ";padding-top:34px"}">`
    + (def.icone ? `<div class="ci" style="background:${cb}">${ico(def.icone, 54, ton === "neutre" ? th.puceT : "#fff", 13)}</div>` : "")
    + (def.entete ? `<div class="ce">${riche(def.entete, THEME.creme)}</div>` : "")
    + (def.lignes || []).map(l => `<div class="cl">${riche(l, THEME.creme)}</div>`).join("") + `</div>`;
  const ls = [...el.querySelectorAll(".cl")], cy = cycle(def, x, 0.3, "pop"); x.son(cy.t0, def.son === undefined ? "pop" : def.son);
  return {el, type: "carton", anim(u) {
    if (!applique(el, cy.etat(u), base)) return;
    ls.forEach((l, j) => { const k = sortie((u - cy.t0 - 0.3 - 0.2 * j) / 0.35); l.style.opacity = k; l.style.transform = `translateY(${((1 - k) * 22).toFixed(1)}px)`; });
  }};
};

FAB.citation = (def, x) => {
  const th = x.th, el = E("div", "el"), base = pose(el, def, {haut: 340, l: 920}), tp = def.tampon;
  const ct = tp ? coul(tp.couleur, /faux|non|stop|erreur/i.test(tp.texte || "FAUX") ? ROUGE : VERT) : "";
  el.innerHTML = `<div class="cit${tp ? " avec-tp" : ""}" style="background:${th.carte};color:${th.carteT}"><div class="gm" style="color:${C.or}">“</div><div class="ct" style="font-size:${def.taille || 64}px">${riche(def.texte || "", THEME.creme)}</div>`
    + (def.auteur ? `<div class="ca">${esc(def.auteur)}</div>` : "") + (tp ? `<div class="tp"><div class="tamp" style="color:${ct};border-color:${ct};font-size:${tp.taille || 104}px">${esc(tp.texte || "FAUX")}</div></div>` : "") + `</div>`;
  const cy = cycle(def, x, 0.25, "pop"), st = el.querySelector(".tp"), tt = tp ? heure(tp.quand, x.sc, {part: 0.7}, x) : 0;
  x.son(cy.t0, def.son); if (tp) { x.son(tt + 0.1, tp.son === undefined ? "tampon" : tp.son); x.secousse(tt + 0.12); }
  return {el, type: "citation", anim(u) {
    if (!applique(el, cy.etat(u), base)) return;
    if (st) { const a = u - tt, k = clamp(a / 0.16); st.style.opacity = a < 0 ? 0 : clamp(k * 3); st.style.transform = `rotate(${tp.angle ?? -9}deg) scale(${(1 + (1 - k * k) * 1.8).toFixed(3)})`; }
  }};
};

// Question à choix : les réponses apparaissent, une barre de temps se vide, puis la bonne réponse s'allume.
FAB.choix = (def, x) => {
  const th = x.th, sc = x.sc, el = E("div", "el chx"), base = pose(el, def, {haut: 640, l: 880});
  const opts = def.options || [], bonne = (def.bonne || 1) - 1, t0 = heure(def.quand, sc, 0.5, x), tr = heure(def.revele, sc, {part: 0.62}, x);
  el.innerHTML = opts.map((o, j) => `<div class="op"><span class="ol" style="background:${th.puceF};color:${th.puceT}">${"ABCD"[j]}</span><span class="otx">${esc(o)}</span><span class="ok">${ico("coche", 46, "#fff", 14)}</span></div>`).join("")
    + `<div class="tps"><div style="background:${th.trait}"></div></div>`;
  const ops = [...el.querySelectorAll(".op")], barre = el.querySelector(".tps div"), td = t0 + 0.15 * opts.length + 0.3;
  if (def.son !== false) { for (let s = td; s < tr - 0.15; s += 0.5) x.son(s, "tic", 0.7); x.son(tr, "succes"); }
  return {el, type: "choix", anim(u) {
    const rev = u >= tr;
    ops.forEach((o, j) => {
      const k = (u - t0 - 0.15 * j) / 0.35, bon = rev && j === bonne, kr = (u - tr) / 0.3;
      o.style.opacity = clamp(k * 2.5) * (rev && !bon ? 0.45 : 1);
      o.style.transform = `translateY(${((1 - sortie(k)) * 40).toFixed(1)}px) scale(${bon ? (1 + 0.05 * Math.sin(Math.PI * clamp(kr))).toFixed(3) : 1})`;
      o.style.background = bon ? VERT : th.carte; o.style.color = bon ? "#fff" : th.carteT;
      o.lastChild.style.transform = `scale(${bon ? rebond(kr).toFixed(3) : 0})`;
    });
    barre.parentNode.style.opacity = clamp((u - td + 0.2) / 0.2) * (rev ? 1 - clamp((u - tr) / 0.2) : 1);
    barre.style.width = (100 * (1 - clamp((u - td) / Math.max(0.1, tr - td)))).toFixed(1) + "%";
  }};
};

// Appel à l'action animé : commenter (un mot se tape puis s'envoie), abonner, enregistrer, envoyer, lien.
FAB.appel = (def, x) => {
  const th = x.th, g = def.genre || "commenter", el = E("div", "el cta"), base = pose(el, def), cy = cycle(def, x, 0.4, "pop"), t0 = cy.t0;
  let anim;
  if (g === "commenter") {
    const mot = String(def.mot || "MENU"), pas = 0.14, tm = def.mot_quand != null ? heure(def.mot_quand, x.sc, null, x) : t0 + 0.4, te = tm + pas * mot.length + 0.3;
    el.innerHTML = `<div class="pub" style="background:${th.puceF};color:${th.puceT}">${esc(mot)}</div><div class="com"><div class="av" style="background:${C.or}">${ico("personne", 84, FONCE, 8)}</div><div class="champ"><span class="sai"></span><span class="cur"></span></div><div class="env" style="background:${C.prune}">${ico("avion", 46, "#fff", 9)}</div></div>`;
    const sai = el.querySelector(".sai"), cur = el.querySelector(".cur"), env = el.querySelector(".env"), pub = el.querySelector(".pub");
    if (def.son !== false) { for (let j = 0; j < mot.length; j++) x.son(tm + pas * j, "tic", 0.8); x.son(te, "clic"); x.son(te + 0.14, "bulle"); }
    anim = u => {
      const n = clamp(Math.floor((u - tm) / pas) + 1, 0, mot.length), a = u - te, kp = (a - 0.1) / 0.35;
      sai.textContent = a > 0.1 ? "" : mot.slice(0, n); cur.style.opacity = a > 0.1 ? 0 : (Math.floor(u * 2.5) % 2 ? 0.15 : 1);
      env.style.transform = `scale(${a > 0 && a < 0.25 ? (1 - 0.25 * Math.sin(Math.PI * a / 0.25)).toFixed(3) : 1})`;
      pub.style.opacity = clamp(kp * 3); pub.style.transform = `translateY(${((1 - sortie(kp)) * 110).toFixed(1)}px) scale(${kp <= 0 ? 0.5 : (0.5 + 0.5 * rebond(kp)).toFixed(3)})`;
    };
  } else if (g === "abonner") {
    const tc = t0 + (def.delai ?? 0.9); let etat = null;
    el.innerHTML = `<div class="btn"></div>`; const b = el.firstChild; x.son(tc, def.son === undefined ? "clic" : def.son);
    anim = u => {
      const fait = u >= tc, a = u - tc;
      if (fait !== etat) { etat = fait; b.innerHTML = fait ? `<span>Abonné</span>${ico("coche", 54, th.titre, 13)}` : "<span>S'abonner</span>"; b.style.background = fait ? "transparent" : th.puceF; b.style.color = fait ? th.titre : th.puceT; b.style.borderColor = fait ? th.titre : th.puceF; }
      b.style.transform = `scale(${a > 0 && a < 0.3 ? (1 + 0.12 * Math.sin(Math.PI * a / 0.3)).toFixed(3) : a > -0.12 && a <= 0 ? 0.94 : 1})`;
    };
  } else if (g === "enregistrer") {
    const tc = t0 + (def.delai ?? 0.9);
    el.innerHTML = `<div class="ic">${ico("signet", 190, th.trait, 9)}</div><div class="lb" style="color:${th.titre}">${esc(def.texte || "Enregistrez ce conseil")}</div>`;
    const p = el.querySelector(".ico path"); x.son(tc, def.son === undefined ? "clic" : def.son);
    anim = u => { const a = u - tc; p.setAttribute("fill", a >= 0 ? th.trait : "none"); el.firstChild.style.transform = `scale(${a > 0 && a < 0.35 ? (1 + 0.2 * Math.sin(Math.PI * a / 0.35)).toFixed(3) : 1})`; };
  } else if (g === "envoyer") {
    el.innerHTML = `<div class="ic">${ico("avion", 170, th.trait, 8)}</div><div class="lb" style="color:${th.titre}">${esc(def.texte || "Envoyez-la à un collègue")}</div>`;
    x.son(t0 + 0.5, def.son === undefined ? "whoosh" : def.son);
    anim = u => {
      const k = (u - t0 - 0.5) / 0.7, kk = douce(k), r = sortie((u - t0 - 1.4) / 0.5), ic = el.firstChild;
      ic.style.transform = k <= 0 ? "" : k < 1 ? `translate(${(kk * 700).toFixed(0)}px,${(-kk * 240).toFixed(0)}px) rotate(${(-12 * kk).toFixed(1)}deg) scale(${(1 - 0.4 * kk).toFixed(3)})` : `translateX(${(-(1 - r) * 700).toFixed(0)}px)`;
      ic.style.opacity = k >= 1 && u - t0 < 1.4 ? 0 : 1;
    };
  } else {
    el.innerHTML = `<div class="btn lien" style="background:${th.puceF};color:${th.puceT};border-color:${th.puceF};font-size:${def.taille || 46}px">${ico("lien", 56, th.puceT, 10)}<span>${esc(def.texte || "restaurant-site-internet.fr")}</span></div>`;
    anim = u => { el.firstChild.style.transform = `scale(${(1 + 0.03 * Math.sin(2 * Math.PI * u / 1.2)).toFixed(4)})`; };
  }
  return {el, type: "appel", anim(u) { if (applique(el, cy.etat(u), base)) anim(u); }};
};

// Dialogue : bulles façon messagerie. de = "client" | "chef" (à gauche, avec un avatar) ou "margot" (à droite).
FAB.chat = (def, x) => {
  const th = x.th, sc = x.sc, el = E("div", "el chat"), base = pose(el, def, {haut: 330, l: 960});
  const rs = def.repliques || [], n = rs.length, p0 = sc.parle0 - sc.debut, span = sc.parle1 - sc.parle0;
  el.innerHTML = rs.map(r => {
    const moi = r.de === "margot" || r.de === "moi", f = moi ? th.puceF : th.carte, c = moi ? th.puceT : th.carteT;
    return `<div class="rg${moi ? " moi" : ""}">${moi ? "" : `<div class="avt">${avatarSVG(r.de, 112, th)}</div>`}<div class="bul q-${moi ? "bas-droite" : "bas-gauche"}" style="background:${f};color:${c};font-size:${def.taille || 47}px;--f:${f}">${esc(r.texte)}</div></div>`;
  }).join("");
  const rangs = [...el.children], ts = rs.map((r, j) => r.quand != null ? heure(r.quand, sc, null, x) : Math.max(0.2, p0 + span * j / n - 0.1));
  ts.forEach(t => x.son(t, def.son === undefined ? "bulle" : def.son));
  return {el, type: "chat", anim(u) {
    rangs.forEach((r, j) => { const k = (u - ts[j]) / 0.35; r.style.opacity = clamp(k * 3); r.style.transformOrigin = r.classList.contains("moi") ? "100% 100%" : "0 100%"; r.style.transform = `translateY(${((1 - sortie(k)) * 30).toFixed(1)}px) scale(${k <= 0 ? 0.8 : (0.8 + 0.2 * rebond(k)).toFixed(3)})`; });
  }};
};

// Particules : confettis, neige, coeurs, bulles, etincelles (toujours les mêmes d'un rendu à l'autre).
FAB.particules = (def, x) => {
  const el = E("div", "el plein part"), genre = def.genre || "confettis", n = def.nombre || (genre === "confettis" ? 90 : 46), g = alea(1000 + x.i * 97 + (def.graine || 0));
  const cs = genre === "neige" ? ["#fff"] : genre === "coeurs" ? [ROSE, ROUGE] : genre === "etincelles" ? [C.or, "#fff"] : genre === "bulles" ? ["#fff", C.or] : [C.or, ROSE, x.sc.fond === "creme" || x.sc.fond === "or" ? C.prune : C.creme, VERT];
  const ps = Array.from({length: n}, () => ({x: g() * 1080, y: g() * 1920, d: g(), v: 0.7 + g() * 0.7, r: g() * 360, vr: (g() - 0.5) * 700, t: 14 + g() * 20, c: cs[Math.floor(g() * cs.length)], ph: g() * 6.28}));
  el.innerHTML = ps.map(p => genre === "confettis" ? `<i style="width:${p.t.toFixed(0)}px;height:${(p.t * 0.55).toFixed(0)}px;background:${p.c}"></i>`
    : genre === "neige" ? `<i style="width:${(p.t * 0.7).toFixed(0)}px;height:${(p.t * 0.7).toFixed(0)}px;border-radius:50%;background:${p.c}"></i>`
    : genre === "bulles" ? `<i style="width:${(p.t * 1.6).toFixed(0)}px;height:${(p.t * 1.6).toFixed(0)}px;border-radius:50%;border:4px solid ${p.c}"></i>`
    : `<i>${ico(genre === "coeurs" ? "coeur" : "etoile", (p.t * 1.7).toFixed(0), p.c)}</i>`).join("");
  const is = [...el.children], t0 = heure(def.quand, x.sc, 0.2, x), dur = def.duree || (genre === "confettis" ? 2.8 : 1e9), op = def.opacite ?? (genre === "confettis" ? 1 : 0.75);
  if (genre === "confettis") x.son(t0, def.son === undefined ? "tada" : def.son); else x.son(t0, def.son);
  return {el, type: "particules", zone: false, derriere: def.derriere ?? (genre !== "confettis" && !def.devant), anim(u) {
    const a = u - t0;
    if (a < 0 || a > dur + 0.6) { el.style.display = "none"; return; }
    el.style.display = ""; el.style.opacity = op * clamp(a / 0.3) * (1 - clamp((a - dur) / 0.6));
    is.forEach((e, j) => {
      const p = ps[j]; let px = p.x, py, rot = 0, s = 1;
      if (genre === "confettis") { const b = a - p.d * 0.45; py = -60 + Math.max(0, b) * p.v * 900 + 140 * Math.max(0, b) * Math.max(0, b); px += 70 * Math.sin(a * 2.2 + p.ph); rot = p.r + p.vr * a; }
      else if (genre === "neige") { py = (p.y + a * p.v * 130) % 1980 - 30; px += 34 * Math.sin(a * 0.9 + p.ph); }
      else if (genre === "coeurs" || genre === "bulles") { py = 1950 - (p.y + a * p.v * 200) % 2000; px += 40 * Math.sin(a * 1.1 + p.ph); }
      else { py = p.y; s = 0.35 + 0.65 * Math.abs(Math.sin(a * p.v * 2.2 + p.ph)); }
      e.style.transform = `translate(${px.toFixed(1)}px,${py.toFixed(1)}px) rotate(${rot.toFixed(0)}deg) scale(${s.toFixed(3)})`;
    });
  }};
};

// Gros sous-titres : le texte dit s'affiche en grand, mot après mot (remplace le bandeau de sous-titres).
FAB.grosmots = (def, x) => {
  const th = x.th, sc = x.sc, el = E("div", "el gm2"), blocs = sc.subs || [];
  pose(el, def, {haut: 400, l: 968}); el.style.fontSize = (def.taille || 124) + "px"; el.style.color = coul(def.couleur, th.titre);
  let courant = null, ms = [];
  const montre = b => { courant = b; el.innerHTML = b.texte.split(" ").map(w => `<span class="m">${esc(w)}</span>`).join(" "); ms = [...el.children]; };
  return {el, type: "grosmots",
    ajuste() { const lh = parseFloat(getComputedStyle(el).lineHeight) || 130; blocs.forEach(b => { montre(b); if (el.scrollHeight > 3.3 * lh) window.ALERTES.push(`scène ${x.i + 1} : gros sous-titre sur plus de 3 lignes : ${b.texte}`); }); courant = null; el.innerHTML = ""; },
    anim(u, t) {
      const b = blocs.find(s => t >= s.t0 && t < s.t1) || (blocs.length && t >= blocs[blocs.length - 1].t1 ? blocs[blocs.length - 1] : null);
      if (!b) { el.style.display = "none"; return; }
      el.style.display = ""; if (b !== courant) montre(b);
      ms.forEach((m, j) => {
        const tm = b.m && b.m[j] != null ? b.m[j] : b.t0, k = (t - tm) / 0.16, dit = k > 0, enCours = dit && t < b.t1 && (j === ms.length - 1 || t < (b.m ? b.m[j + 1] : 1e9));
        m.style.opacity = dit ? 1 : 0.2; m.style.color = enCours ? th.accT : ""; m.style.background = enCours && th.accF ? th.accF : "";
        m.style.transform = `scale(${dit ? (1 + 0.14 * (1 - sortie(k))).toFixed(3) : 1})`;
      });
    }};
};

// Élément libre : n'importe quel HTML / SVG, animé par des clés ou par une fonction.
//   cles : [{t, opacity, x, y, scale, rot}] (t en secondes depuis « quand ») ; js : corps d'une fonction (u, el, o) appelée à chaque image.
FAB.libre = (def, x) => {
  const el = E("div", "el" + (def.plein ? " plein" : "")), base = def.plein ? "" : pose(el, def);
  if (def.css) { const st = document.createElement("style"); st.textContent = def.css; document.head.appendChild(st); }
  el.innerHTML = def.html || "";
  const cy = cycle(def, x, 0, def.entree || "aucune"), cles = (def.cles || []).slice().sort((a, b) => a.t - b.t);
  let f = null;
  if (def.js) { try { f = new Function("u", "el", "o", def.js); } catch (e) { window.ALERTES.push(`scène ${x.i + 1} : « js » de l'élément libre invalide (${e.message})`); } }
  const o = {clamp, sortie, rebond, douce, mel, ico, C, th: x.th, sc: x.sc, mots: x.sc.mots, heure: q => heure(q, x.sc, 0, x), parle: 0, t: 0};
  x.son(cy.t0, def.son);
  return {el, type: "libre", zone: def.zone ?? !def.plein, anim(u, t, ouv) {
    const st = cy.etat(u); if (!st) { el.style.display = "none"; return; }
    if (cles.length) {
      let i = 0; while (i < cles.length - 1 && cles[i + 1].t <= st.age) i++;
      const A = cles[i], B = cles[Math.min(i + 1, cles.length - 1)], k = B.t > A.t ? douce((st.age - A.t) / (B.t - A.t)) : 0, v = (p, d) => mel(A[p] ?? d, B[p] ?? A[p] ?? d, k);
      st.o *= v("opacity", 1); st.tx += v("x", 0); st.ty += v("y", 0); st.s *= v("scale", 1); st.r += v("rot", 0);
    }
    applique(el, st, base);
    if (f) { o.parle = ouv; o.t = t; try { f(u, el, o); } catch (e) { if (!el._err) { el._err = 1; window.ALERTES.push(`scène ${x.i + 1} : erreur dans « js » (${e.message})`); } } }
  }};
};
