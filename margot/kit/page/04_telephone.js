// ── Téléphone : une maquette de téléphone et ses écrans ────────────────────────────────────────────
// Chaque écran reçoit ses réglages (ec) et un contexte (c.h = heure d'un « quand », c.son = bruitage)
// et renvoie {html, init?(page) → fonction appelée à chaque image}.
const ECRANS = {
  carte(ec, c) {
    const d = {nom: "Chez Margot", sous: "Exemple de carte", info: "Ouvert · 12 h – 14 h", pied: "Carte mise à jour aujourd'hui", rubriques: [
      {titre: "Entrées", plats: [["Œuf mayonnaise", "6 €"], ["Soupe du jour", "7 €"]]},
      {titre: "Plats", plats: [["Bavette, frites maison", "18 €"], ["Poisson du marché", "19 €"], ["Risotto aux champignons", "16 €"]]},
      {titre: "Desserts", plats: [["Tarte du jour", "7 €"], ["Mousse au chocolat", "7 €"]]},
      {titre: "Boissons", plats: [["Café", "2 €"], ["Verre de vin", "5 €"], ["Jus de pomme", "4 €"]]}], ...ec};
    return {html: `<div class="ph-tete"><b>${esc(d.nom)}</b><i>${esc(d.sous)}</i></div><div class="ph-chips"><span>${esc(d.info)}</span><span class="pl">Réserver</span></div>`
      + d.rubriques.map(r => `<div class="ph-rub">${esc(r.titre)}</div>` + r.plats.map(p => `<div class="ph-plat"><span>${esc(p[0])}${p[2] ? `<small>${esc(p[2])}</small>` : ""}</span><b>${esc(p[1])}</b></div>`).join("")).join("")
      + `<div class="ph-pied">${esc(d.pied)}</div>`,
      // "change": {plat, prix, quand} : le prix de ce plat est remplacé à cet instant (un appui, puis le nouveau prix).
      init(page) {
        const ch = d.change; if (!ch) return null;
        const rg = [...page.querySelectorAll(".ph-plat")].find(p => p.firstChild.textContent.startsWith(ch.plat)), b = rg && rg.querySelector("b");
        if (!b) { window.ALERTES.push(`écran carte : plat « ${ch.plat} » introuvable pour "change"`); return null; }
        const avant = b.textContent, tq = c.h(ch.quand, {part: 0.5});
        c.son(tq, "clic"); c.son(tq + 0.3, "succes", 0.7);
        return u => {
          const a = u - tq - 0.3, k = a / 0.45;
          rg.style.background = u >= tq - 0.05 ? "rgba(235,190,114,.38)" : ""; rg.style.borderRadius = "10px";
          b.textContent = a >= 0 ? ch.prix : avant; b.style.display = "inline-block"; b.style.color = a >= 0 ? "#2F8F5B" : "";
          b.style.transform = `scale(${a > 0 && k < 1 ? (1 + 0.45 * Math.sin(Math.PI * k)).toFixed(3) : 1})`;
        };
      }};
  },
  recherche(ec, c) {
    const d = {requete: "restaurant ouvert ce midi", resultats: [{titre: "Chez Margot", sous: "Exemple · 350 m", badge: "Carte en ligne", ok: true},
      {titre: "Le Bistrot Exemple", sous: "Exemple · 500 m", badge: "Pas de carte", ok: false}, {titre: "La Table Modèle", sous: "Exemple · 800 m", badge: "Carte en ligne", ok: true}], ...ec};
    const tq = c.h(d.quand, 0.5), vit = d.vitesse || 20, tf = tq + d.requete.length / vit + 0.3;
    return {html: `<div class="ph-rech"><div class="ph-bar">${ico("loupe", 30, "#5A1F4A", 11)}<span class="rq"></span><span class="cu"></span></div>`
      + d.resultats.map(r => `<div class="ph-res"><div class="ph-vig">${ico("couverts", 44, "#5A1F4A", 8)}</div><div><b>${esc(r.titre)}</b><i>${esc(r.sous || "")}</i>${r.badge ? `<span class="${r.ok ? "oui" : "non"}">${esc(r.badge)}</span>` : ""}</div></div>`).join("") + `</div>`,
      init(page) {
        const rq = page.querySelector(".rq"), cu = page.querySelector(".cu"), rs = [...page.querySelectorAll(".ph-res")];
        for (let j = 0; j < d.requete.length; j += 3) c.son(tq + j / vit, "tic", 0.5);
        rs.forEach((_, j) => c.son(tf + 0.2 * j, "bulle", 0.6));
        return u => {
          rq.textContent = d.requete.slice(0, clamp(Math.floor((u - tq) * vit), 0, d.requete.length)); cu.style.opacity = u < tf && Math.floor(u * 2.5) % 2 ? 1 : 0;
          rs.forEach((r, j) => { const k = (u - tf - 0.2 * j) / 0.3; r.style.opacity = clamp(k * 2); r.style.transform = `translateY(${((1 - sortie(k)) * 30).toFixed(1)}px)`; });
        };
      }};
  },
  fiche(ec, c) {
    const d = {nom: "Le Bistrot Exemple", sous: "Exemple · Restaurant", horaires: "Ouvert · ferme à 22 h", adresse: "12 rue de l'Exemple", boutons: ["Appeler", "Itinéraire", "Carte"], ...ec};
    const et = d.note != null ? `<div class="ph-et">${[1, 2, 3, 4, 5].map(n => ico("etoile", 26, n <= Math.round(d.note) ? "#E0A93B" : "#E6D8CC")).join("")}<span>${String(d.note).replace(".", ",")}${d.avis ? ` · ${d.avis} avis` : ""}</span></div>` : "";
    return {html: `<div class="ph-couv">${ico("assiette", 110, "#EBBE72", 6)}</div><div class="ph-fi"><b>${esc(d.nom)}</b><i>${esc(d.sous)}</i>${et}<p>${ico("horloge", 26, "#5A1F4A", 10)}${esc(d.horaires)}</p><p>${ico("epingle", 26, "#5A1F4A", 10)}${esc(d.adresse)}</p>`
      + `<div class="ph-bts">${d.boutons.map(b => `<span class="${b === d.accent ? "ac" : b === d.manque ? "mq" : ""}">${esc(b)}</span>`).join("")}</div>`
      + (d.manque ? `<div class="ph-mq">${ico("interdit", 30, "#D4374A", 10)}<span>${esc(d.message || "Pas de carte en ligne")}</span></div>` : "") + `</div>`,
      init(page) {
        const ac = page.querySelector(".ac"), mq = page.querySelector(".ph-mq"), tm = c.h(d.quand, {part: 0.5});
        if (mq) c.son(tm, "erreur", 0.7);
        return u => {
          if (ac) ac.style.transform = `scale(${(1 + 0.07 * Math.sin(2 * Math.PI * u / 0.9)).toFixed(3)})`;
          if (mq) { const k = (u - tm) / 0.3; mq.style.opacity = clamp(k * 3); mq.style.transform = `scale(${k <= 0 ? 0.6 : (0.6 + 0.4 * rebond(k)).toFixed(3)})`; }
        };
      }};
  },
  messages(ec, c) {
    const d = {titre: "Messages", messages: [{de: "client", texte: "Bonjour, vous avez la carte ?"}, {de: "moi", texte: "Oui ! Voici le lien."}], ...ec}, n = d.messages.length;
    const ts = d.messages.map((m, j) => m.quand != null ? c.h(m.quand) : c.h({part: j / n}));
    return {html: `<div class="ph-entete">${esc(d.titre)}</div><div class="ph-fil">${d.messages.map(m => `<div class="ph-msg${m.de === "moi" ? " moi" : ""}">${esc(m.texte)}</div>`).join("")}</div>`,
      init(page) {
        const ms = [...page.querySelectorAll(".ph-msg")]; ts.forEach(t => c.son(t, "bulle", 0.7));
        return u => ms.forEach((m, j) => { const k = (u - ts[j]) / 0.3; m.style.opacity = clamp(k * 3); m.style.transform = `scale(${k <= 0 ? 0.7 : (0.7 + 0.3 * rebond(k)).toFixed(3)})`; });
      }};
  },
  vide(ec) {
    const d = {titre: "Aucune carte trouvée", sous: "Ce restaurant n'a pas mis sa carte en ligne.", ...ec};
    return {html: `<div class="ph-vide">${ico("loupe", 150, "#C9B8AA", 7)}<b>${esc(d.titre)}</b><i>${esc(d.sous)}</i></div>`,
      init(page) { const ic = page.querySelector(".ico"); return u => { ic.style.transform = `rotate(${(8 * Math.sin(2 * Math.PI * u / 1.6)).toFixed(1)}deg)`; }; }};
  },
  reservation(ec, c) {
    const d = {titre: "Réserver une table", champs: [["Date", "Samedi"], ["Heure", "20 h"], ["Personnes", "4"]], bouton: "Réserver", fait: "Table réservée", ...ec}, n = d.champs.length;
    const ts = d.champs.map((_, j) => c.h({part: 0.1 + 0.6 * j / n})), tb = c.h(d.quand, {part: 0.85});
    return {html: `<div class="ph-entete">${esc(d.titre)}</div><div class="ph-form">${d.champs.map(ch => `<div class="ph-ch"><i>${esc(ch[0])}</i><b>${esc(ch[1])}</b></div>`).join("")}<div class="ph-btn">${esc(d.bouton)}</div><div class="ph-ok">${ico("coche", 70, "#fff", 13)}<b>${esc(d.fait)}</b></div></div>`,
      init(page) {
        const bs = [...page.querySelectorAll(".ph-ch b")], bt = page.querySelector(".ph-btn"), ok = page.querySelector(".ph-ok");
        ts.forEach(t => c.son(t, "tic", 0.7)); c.son(tb, "clic"); c.son(tb + 0.25, "succes");
        return u => {
          bs.forEach((b, j) => { const k = (u - ts[j]) / 0.25; b.style.opacity = clamp(k * 3); b.style.transform = `scale(${k <= 0 ? 0.6 : (0.6 + 0.4 * rebond(k)).toFixed(3)})`; });
          const a = u - tb, k = (a - 0.2) / 0.35;
          bt.style.transform = `scale(${a > 0 && a < 0.2 ? 0.93 : 1})`; ok.style.opacity = clamp(k * 3); ok.style.transform = `scale(${k <= 0 ? 0.5 : (0.5 + 0.5 * rebond(k)).toFixed(3)})`;
        };
      }};
  },
  notification(ec, c) {
    const d = {heure: "19:42", jour: "samedi", app: "Restaurant Site Internet", titre: "Nouvelle réservation", texte: "Samedi, 20 h · 4 personnes", ...ec}, tn = c.h(d.quand, {part: 0.3});
    return {html: `<div class="ph-verrou"><b>${esc(d.heure)}</b><i>${esc(d.jour)}</i><div class="ph-notif"><div class="ph-ni">${ico("cloche", 40, "#5A1F4A", 9)}</div><div><em>${esc(d.app)}</em><b>${esc(d.titre)}</b><span>${esc(d.texte)}</span></div></div></div>`,
      init(page) {
        const nf = page.querySelector(".ph-notif"); c.son(tn, "ding");
        return u => { const k = (u - tn) / 0.4; nf.style.opacity = clamp(k * 3); nf.style.transform = `translateY(${(-(1 - rebond(k)) * 160).toFixed(1)}px)`; };
      }};
  },
  ardoise(ec, c) {
    const d = {titre: "Ardoise du jour", lignes: [["Velouté de potimarron", "7 €"], ["Blanquette de veau", "15 €"], ["Tarte tatin", "7 €"]], pied: "Exemple", ...ec}, n = d.lignes.length;
    const ts = d.lignes.map((_, j) => c.h({part: 0.15 + 0.7 * j / n}));
    return {html: `<div class="ph-ard"><b>${esc(d.titre)}</b>${d.lignes.map(l => `<p><span>${esc(l[0])}</span><em>${esc(l[1] || "")}</em></p>`).join("")}<i>${esc(d.pied)}</i></div>`,
      init(page) {
        const ps = [...page.querySelectorAll("p")]; ts.forEach(t => c.son(t, "glisse", 0.6));
        return u => ps.forEach((p, j) => { p.style.clipPath = `inset(0 ${(100 - 100 * sortie((u - ts[j]) / 0.5)).toFixed(1)}% 0 0)`; });
      }};
  },
  qr(ec) {
    const d = {titre: "Scannez pour voir la carte", sous: "Exemple", ...ec}, g = alea(77), N = 21; let cs = "";
    const coin = (a, b) => (a < 8 && b < 8) || (a >= N - 8 && b < 8) || (a < 8 && b >= N - 8);
    for (let b = 0; b < N; b++) for (let a = 0; a < N; a++) if (!coin(a, b) && g() < 0.48) cs += `<rect x="${a}" y="${b}" width="1.02" height="1.02"/>`;
    const rep = (a, b) => `<rect x="${a}" y="${b}" width="7" height="7"/><rect x="${a + 1}" y="${b + 1}" width="5" height="5" fill="#fff"/><rect x="${a + 2}" y="${b + 2}" width="3" height="3"/>`;
    return {html: `<div class="ph-qr"><b>${esc(d.titre)}</b><div class="ph-qc"><svg viewBox="-1 -1 23 23" width="330" height="330" fill="#3D1030">${cs}${rep(0, 0)}${rep(N - 7, 0)}${rep(0, N - 7)}</svg><div class="ph-scan"></div></div><i>${esc(d.sous)}</i></div>`,
      init(page) { const s = page.querySelector(".ph-scan"); return u => { s.style.top = (6 + 86 * (0.5 - 0.5 * Math.cos(2 * Math.PI * u / 2.2))).toFixed(1) + "%"; }; }};
  },
  image(ec) { return {html: `<img class="ph-img" src="${esc(ec.src || "")}">`}; }
};

FAB.telephone = (def, x) => {
  const sc = x.sc, el = E("div", "el"), ec = def.ecran || {type: "carte"}, f = ECRANS[ec.type || "carte"];
  const base = pose(el, def, {x: 668, y: 968}) + (def.incline ? ` rotate(${def.incline}deg)` : "") + (def.taille ? ` scale(${def.taille})` : "");
  if (!f) window.ALERTES.push(`scène ${x.i + 1} : écran de téléphone inconnu « ${ec.type} »`);
  const c = {h: (q, d) => heure(q, sc, d ?? 0, x), son: (t, n, v) => { if (def.son !== false) x.son(t, n, v); }};
  const e = (f || ECRANS.vide)(ec, c);
  el.innerHTML = `<div class="tel"><div class="ecran"><div class="encoche"></div><div class="page">${e.html}</div><div class="tap"></div></div></div>`;
  const page = el.querySelector(".page"), tap = el.querySelector(".tap"), an = e.init ? e.init(page) : null;
  const cy = cycle(def, x, 0.25, "de-bas", 0.55), td0 = heure(ec.defile_de, sc, {part: 0.3}, x), td1 = heure(ec.defile_a, sc, {part: 0.95}, x);
  const touches = (def.touches || []).map(t => ({t: heure(t.quand, sc, 0.5, x), x: t.x ?? 0.5, y: t.y ?? 0.5}));
  touches.forEach(t => c.son(t.t, "clic"));
  let course = 0;
  return {el, type: "telephone",
    ajuste() { course = ec.defile === false ? 0 : Math.max(0, page.scrollHeight - 868); },
    anim(u) {
      if (!applique(el, cy.etat(u), base)) return;
      if (course) page.style.transform = `translateY(${(-course * douce((u - td0) / Math.max(0.3, td1 - td0))).toFixed(1)}px)`;
      if (an) an(u);
      const tc = touches.find(t => u >= t.t && u < t.t + 0.4);
      if (tc) { const k = (u - tc.t) / 0.4; tap.style.display = "block"; tap.style.left = (tc.x * 438) + "px"; tap.style.top = (tc.y * 868) + "px"; tap.style.transform = `scale(${(0.5 + 0.9 * sortie(k)).toFixed(3)})`; tap.style.opacity = 1 - k; }
      else tap.style.display = "none";
    }};
};
