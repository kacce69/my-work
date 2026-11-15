// ── Scènes : construction, rendu d'une image à l'instant t, contrôles ──────────────────────────────
const root = document.getElementById("root"), S = [];
const TRANSITIONS = ["cercle", "fondu", "coupe", "zoom", "rideau", "volet", "glisse-gauche", "glisse-droite", "glisse-haut", "glisse-bas", "pousse-gauche", "pousse-droite", "pousse-haut"];
const karaoke = O.soustitres === "karaoke", sansSub = O.soustitres === "aucun";

D.scenes.forEach((sc, i) => {
  const th = THEME[sc.fond] || THEME.creme, d = E("div", "scene"), cam = E("div", "cam");
  d.style.background = C[sc.fond] || C.creme; d.style.zIndex = i + 1;
  const s = {sc, i, th, d, cam, acteurs: [], secousses: [], camT: ""};
  const x = {sc, i, th,
    son(t, nom, vol) { if (nom && O.bruitages !== false && sc.bruitages !== false) window.SONS.push({t: +(sc.debut + t).toFixed(3), son: nom, vol: vol ?? 1}); },
    secousse(t) { s.secousses.push(t); }};
  if (sc.fond && !THEME[sc.fond]) window.ALERTES.push(`scène ${i + 1} : fond inconnu « ${sc.fond} »`);
  cam.innerHTML = sc.cercles === false ? "" : `<div class="deco" style="width:760px;height:760px;left:-300px;top:-240px;background:${th.deco}"></div>
  <div class="deco" style="width:560px;height:560px;right:-220px;top:1480px;background:${th.deco}"></div>`;
  if (sc.decor) {
    const f = DECORS[sc.decor];
    if (!f) window.ALERTES.push(`scène ${i + 1} : décor inconnu « ${sc.decor} »`);
    else { const r = f(sc.fond); cam.insertAdjacentHTML("beforeend", typeof r === "string" ? r : r.html); if (r.anim) { const el = cam.lastElementChild; s.acteurs.push({type: "decor", zone: false, def: {}, anim: u => r.anim(u, el)}); } }
  }
  let plan = PLANS[sc.plan || "margot"], premier = null;
  if (!plan) { window.ALERTES.push(`scène ${i + 1} : plan inconnu « ${sc.plan} »`); plan = PLANS.margot; }
  plan(sc, x).concat(sc.elements || []).forEach(def => {
    const f = FAB[def.type];
    if (!f) { window.ALERTES.push(`scène ${i + 1} : type d'élément inconnu « ${def.type} »`); return; }
    const a = f(def, x); a.def = def;
    if (a.el) { if (a.derriere && premier) cam.insertBefore(a.el, premier); else cam.appendChild(a.el); premier = premier || a.el; }
    s.acteurs.push(a);
  });
  d.appendChild(cam);
  if (O.progression) {
    const p = E("div", "prog", D.scenes.map(z => `<i style="flex:${(z.fin - z.debut).toFixed(2)};background:${th.voile}"><b style="background:${th.titre}"></b></i>`).join(""));
    d.appendChild(p); s.prog = [...p.querySelectorAll("b")];
  }
  const sub = E("div", "sub", `<span style="background:${th.subF};color:${th.subT}"></span>`);
  d.appendChild(sub); s.sub = sub.firstChild; s.avecSub = !sansSub && sc.soustitres !== false && !s.acteurs.some(a => a.type === "grosmots");
  (sc.secousses || []).forEach(q => s.secousses.push(heure(q, sc, 0, x)));
  root.appendChild(d); S.push(s);
  // Bruitages : le changement de scène, puis ceux demandés dans le scénario
  if (i > 0) {
    const tr = sc.transition || "cercle";
    if (!TRANSITIONS.includes(tr)) window.ALERTES.push(`scène ${i + 1} : transition inconnue « ${tr} »`);
    const defaut = tr === "cercle" ? "pop" : tr === "fondu" || tr === "coupe" ? null : tr === "zoom" ? "impact" : "whoosh";
    const sn = sc.son_transition !== undefined ? sc.son_transition : defaut;
    if (sn && O.bruitages !== false) window.SONS.push({t: sn === "pop" ? sc.debut : Math.max(0, +(sc.debut - 0.1).toFixed(3)), son: sn, vol: 1});
  }
  (sc.sons || []).forEach(e => window.SONS.push({t: +(sc.debut + heure(e.quand, sc, 0, x)).toFixed(3), son: e.son, vol: e.volume ?? 1}));
});

function render(t) {
  const img = Math.max(0, Math.min(D.env.length - 1, Math.round(t * D.fps)));
  const ouv = D.env[img] || 0;
  S.forEach((s, i) => {
    const sc = s.sc, u = t - sc.debut, sv = S[i + 1];
    if (u < 0 || (sv && t >= sv.sc.debut + 0.5)) { s.d.style.display = "none"; return; }
    s.d.style.display = "block";
    // Arrivée de la scène
    const tr = i === 0 ? "aucune" : (sc.transition || "cercle"), k = sortie(u / 0.42);
    let clip = "none", tf = "", op = "";
    if (tr === "cercle") clip = `circle(${Math.round(k * 2300)}px at 540px 1070px)`;
    else if (tr === "fondu") op = clamp(u / 0.42);
    else if (tr === "glisse-gauche" || tr === "pousse-gauche") tf = `translateX(${((1 - k) * 1080).toFixed(1)}px)`;
    else if (tr === "glisse-droite" || tr === "pousse-droite") tf = `translateX(${(-(1 - k) * 1080).toFixed(1)}px)`;
    else if (tr === "glisse-haut" || tr === "pousse-haut") tf = `translateY(${((1 - k) * 1920).toFixed(1)}px)`;
    else if (tr === "glisse-bas") tf = `translateY(${(-(1 - k) * 1920).toFixed(1)}px)`;
    else if (tr === "rideau") clip = `inset(0 ${(100 - 100 * k).toFixed(2)}% 0 0)`;
    else if (tr === "volet") clip = `polygon(0 0, ${(k * 230 - 30).toFixed(1)}% 0, ${(k * 230 - 130).toFixed(1)}% 100%, 0 100%)`;
    else if (tr === "zoom") { tf = `scale(${(1.35 - 0.35 * k).toFixed(4)})`; op = clamp(u / 0.2); }
    if (sv && t >= sv.sc.debut) {                          // la scène suivante pousse celle-ci
      const tn = sv.sc.transition, kn = sortie((t - sv.sc.debut) / 0.42);
      if (tn === "pousse-gauche") tf = `translateX(${(-kn * 1080).toFixed(1)}px)`;
      else if (tn === "pousse-droite") tf = `translateX(${(kn * 1080).toFixed(1)}px)`;
      else if (tn === "pousse-haut") tf = `translateY(${(-kn * 1920).toFixed(1)}px)`;
    }
    s.d.style.clipPath = clip; s.d.style.transform = tf; s.d.style.opacity = op;
    // Caméra
    let ct = "";
    const dur = sc.fin - sc.debut, cm = sc.camera;
    if (cm === "avance") ct = `scale(${(1 + 0.07 * u / dur).toFixed(4)})`;
    else if (cm === "recule") ct = `scale(${(1.07 - 0.07 * u / dur).toFixed(4)})`;
    else if (cm === "derive") ct = `scale(1.05) translateX(${(-24 + 48 * u / dur).toFixed(1)}px)`;
    for (const ts of s.secousses) { const a = u - ts; if (a >= 0 && a < 0.4) { const amp = 18 * (1 - a / 0.4); ct += ` translate(${(amp * Math.sin(a * 95)).toFixed(1)}px,${(amp * Math.cos(a * 71)).toFixed(1)}px)`; } }
    if (ct !== s.camT) { s.cam.style.transform = ct; s.camT = ct; }
    for (const a of s.acteurs) a.anim(u, t, ouv);
    if (s.prog) s.prog.forEach((p, j) => { const z = D.scenes[j]; p.style.width = (100 * clamp((t - z.debut) / (z.fin - z.debut))).toFixed(1) + "%"; });
    // Sous-titres
    const e = s.sub, b = s.avecSub ? (sc.subs || []).find(z => t >= z.t0 && t < z.t1) : null;
    if (b) {
      e.style.display = "inline-block";
      if (karaoke) {
        if (e._b !== b) { e._b = b; e.innerHTML = b.texte.split(" ").map(w => `<b>${esc(w)}</b>`).join(" "); e._m = [...e.children]; }
        e._m.forEach((m, j) => { const tm = b.m && b.m[j] != null ? b.m[j] : b.t0, dit = t >= tm, cours = dit && (j === e._m.length - 1 || t < b.m[j + 1]); m.style.opacity = dit ? 1 : 0.62; m.style.background = cours ? C.or : ""; m.style.color = cours ? FONCE : ""; m.style.boxShadow = cours ? `0 0 0 7px ${C.or}` : ""; });
      } else e.textContent = b.texte;
      e.style.transform = `scale(${0.9 + 0.1 * sortie((t - b.t0) / 0.12)})`;
    } else e.style.display = "none";
  });
}

function ajuster() {
  S.forEach((s, i) => {
    s.d.style.display = "block"; s.d.style.clipPath = "none";
    s.acteurs.forEach(a => a.ajuste && a.ajuste());
    if (s.avecSub) (s.sc.subs || []).forEach(b => { s.sub.style.display = "inline-block"; s.sub.textContent = b.texte; if (s.sub.getBoundingClientRect().height > 190) window.ALERTES.push(`scène ${i + 1} : sous-titre sur 3 lignes : ${b.texte}`); });
    s.sub.style.display = "none"; s.sub._b = null;
  });
}
// Contrôle des débordements : chaque élément, tel qu'il est à la fin de sa scène, doit rester dans la zone utile.
function verifier() {
  S.forEach((s, i) => {
    render(s.sc.fin - 0.04);
    const subs = s.avecSub && (s.sc.subs || []).length;
    s.acteurs.forEach(a => {
      if (a.zone === false || !a.el || a.def.legacy || a.def.zone === false || a.type === "etiquette") return;
      if (getComputedStyle(a.el).display === "none") return;
      const r = a.boite ? a.boite() : a.el.getBoundingClientRect();
      if (!r.width) return;
      if (r.left < 16 || r.right > 1064) window.ALERTES.push(`scène ${i + 1} : ${a.type} dépasse sur le côté (de ${Math.round(r.left)} à ${Math.round(r.right)} px)`);
      if (r.top < 170) window.ALERTES.push(`scène ${i + 1} : ${a.type} trop haut (${Math.round(r.top)} px : zone des boutons d'Instagram)`);
      if (r.bottom > (subs && a.type !== "margot" ? 1446 : 1640)) window.ALERTES.push(`scène ${i + 1} : ${a.type} trop bas (${Math.round(r.bottom)} px${subs ? " : il passe sous les sous-titres" : ""})`);
    });
  });
}
const images = [...document.images].map(im => im.complete ? 0 : new Promise(r => { im.addEventListener("load", r); im.addEventListener("error", r); }));
document.fonts.load('900 104px Fraunces').catch(() => 0).then(() => document.fonts.load('600 64px Fraunces')).catch(() => 0).then(() => document.fonts.ready).then(() => Promise.all(images))
  .then(() => { ajuster(); verifier(); render(0); window.PRET = true; });
