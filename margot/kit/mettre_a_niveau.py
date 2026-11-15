#!/usr/bin/env python3
"""Met les scénarios de la campagne au niveau du moteur du 15/11/2026, sans toucher à un seul mot dit par Margot :
les prises de voix enregistrées restent donc valables (seul leur découpage en scènes change).

Usage : python3 mettre_a_niveau.py <dossier d'origine> [codes…]          (sans code : J02…J30 et HS1…HS8)
Lit <dossier>/<code>.json (le scénario d'origine : plan « margot » partout) et <dossier>/voix/<code>.json (son calage d'origine),
écrit specs/<code>.json et, quand la dernière scène est partagée en deux, voix/<code>.json.
Les scénarios d'origine sont dans l'historique du dépôt (avant le 15/11/2026 au soir).

Ce qui change dans chaque Reel :
- le Reel entier : jeu fin, sous-titres karaoké, barre de progression ;
- scène 1 : l'accroche se lit dès la première image (titre fixe, Margot déjà en place), une illustration arrive aussitôt ;
- scènes de conseil : Margot montre une illustration calée sur un mot de la voix — plan « montre » (icône ou plat),
  « duo » (personnage), « telephone » (écran) ou « liste » (les pastilles deviennent des points qui se cochent) ;
- la phrase qui présente le site devient une scène à part, où le téléphone montre la vraie page de démonstration du site
  (ou un écran d'exemple animé) ; la prise de voix est coupée en deux dans le silence entre les deux phrases ;
- dernière scène : plan « fin », avec l'appel animé (commenter MENU, ou enregistrer et envoyer).
Les illustrations sont choisies à la main, scène par scène, dans les tables ci-dessous.
"""
import json, pathlib, re, sys, unicodedata

import numpy as np
import soundfile as sf

from reel import jetons

ICI = pathlib.Path(__file__).resolve().parent

# T : une entrée par scène (1 à 4). i = icône, p = plat, c = personnage, t = écran du téléphone, l = True (les pastilles deviennent une liste).
# b = badge (petite icône sur le coin), q = quand (un mot de la voix), e = expression du personnage, o = objet en main, bulle = ce qu'il dit,
# ecran = réglages de l'écran, d = décor de la scène, acc = accessoire de Margot pour tout le Reel, neige = flocons en scène 1.
T = {
    "J02": [dict(p="pates", b="photo", d="cuisine"), dict(i="soleil", q="@lumière"), dict(c="chef", o="telephone", e="joie", q="@essuyez"), dict(p="steak", b="photo", q="@plat")],
    "J03": [dict(c="cliente", e="doute", bulle="Il y a des fruits à coque ?", d="salle"), dict(i="liste", b="exclamation", q="@quatorze"), dict(i="carte", q="@écrit"), dict(i="toque", b="rafraichir", q="@changement")],
    "J04": [dict(p="steak", b="euro", d="cuisine"), dict(i="liste", q="@listez"), dict(i="calculette", q="@multipliez"), dict(i="balance", q="@comparez")],
    "J05": [dict(i="etoile", b="exclamation", d="salle"), dict(i="coeur", q="@remerciez"), dict(i="coche", q="@reconnaissez"), dict(i="telephone", q="@téléphone")],
    "J06": [dict(i="assiette", b="question", d="salle"), dict(i="telephone", q="@numéro"),
            dict(t="messages", ecran=dict(titre="Rappel (exemple)", messages=[dict(de="moi", texte="Bonjour, nous vous attendons demain à 20 h. À demain !", quand="@rappel")])),
            dict(i="calendrier", b="croix", q="@annuler")],
    "J07": [dict(i="ardoise", b="horloge", d="rue"), dict(t="ardoise"), dict(i="euro", q="@prix"), dict(i="commentaire", q="@mots")],
    "J08": [dict(p="burger", b="etoile", d="cuisine"), dict(i="graphique", q="@comptez"), dict(i="calculette", q="@calculez"), dict(i="cible", q="@classez")],
    "J09": [dict(i="qr", b="question", d="salle"), dict(i="qr", b="couverts", q="@table"), dict(i="boutique", q="@vitrine"), dict(i="carte", b="euro", q="@carte")],
    "J10": [dict(i="calendrier", b="croix", d="rue"), dict(i="epingle", b="horloge", q="@horaires"), dict(i="megaphone", q="@annoncez-le"), dict(i="boutique", q="@porte")],
    "J11": [dict(i="carte", b="question", d="cuisine"), dict(i="graphique", q="@ventes"), dict(i="euro", q="@marge"), dict(c="chef", e="doute", q="@cuisine")],
    "J12": [dict(p="poisson", b="question", d="cuisine"), dict(p="poisson", q="@produit"), dict(i="flamme", q="@cuisson"), dict(p="salade", q="@garniture")],
    "J13": [dict(i="euro", b="oeil", d="rue"), dict(i="boutique", q="@dehors"), dict(i="carte", q="@intérieur"), dict(i="billet", b="coche", q="@prix")],
    "J14": [dict(t="recherche", ecran=dict(requete="restaurant près de moi", quand=0.4), d="rue"), dict(t="fiche"), dict(i="epingle", b="coche", q="@adresse"), dict(i="etoile", b="commentaire", q="@avis")],
    "J15": [dict(i="photo", b="question", d="salle"), dict(p="pizza", b="photo", q="@plat"), dict(c="cheffe", e="joie", q="@coulisses"), dict(i="horloge", q="@infos")],
    "J16": [dict(i="cadeau", b="etoile", acc="bonnet", neige=True, d="salle"), dict(i="carte", b="euro", q="@menu"), dict(i="megaphone", q="@annoncez-le"), dict(i="calendrier", q="@date")],
    "J17": [dict(i="poubelle", b="question", d="cuisine"), dict(i="liste", q="@notez"), dict(i="loupe", q="@repérez"), dict(p="soupe", q="@plat")],
    "J18": [dict(c="client", e="joie", d="salle"), dict(c="serveur", e="joie", bulle="Bonjour ! Votre table préférée ?", q="@bonjour"), dict(p="dessert", b="coeur", q="@attention"), dict(i="message", q="@nouvelles")],
    "J19": [dict(i="carte", b="loupe", d="salle"), dict(t="carte"), dict(i="commentaire", q="@noms"), dict(i="coche", q="@peu")],
    "J20": [dict(c="serveur", o="telephone", e="doute", d="salle"), dict(i="calendrier", b="horloge", q="@date"), dict(i="couverts", b="telephone", q="@couverts"), dict(i="exclamation", q="@demandes")],
    "J21": [dict(p="pates", b="euro", d="cuisine"), dict(i="calculette", q="@calculez"), dict(i="balance", q="@comparez"), dict(i="coche", q="@limitez")],
    "J22": [dict(p="vin", b="question", d="salle"), dict(p="cafe", q="@familles"), dict(i="verre", b="euro", q="@contenance"), dict(p="vin", q="@vins")],
    "J23": [dict(i="boutique", b="oeil", d="rue"), dict(i="carte", b="euro", q="@carte"), dict(i="horloge", q="@horaires"), dict(i="ampoule", q="@éclairée")],
    "J24": [dict(i="flocon", acc="bonnet", neige=True, d="rue"), dict(i="feuille", q="@saison"), dict(p="soupe", q="@soupe"), dict(p="salade", b="croix", q="@été")],
    "J25": [dict(i="cadeau", acc="bonnet", neige=True, d="salle"), dict(i="billet", q="@montant"), dict(i="calendrier", q="@date"), dict(i="megaphone", q="@savoir")],
    "J26": [dict(p="dessert", b="etoile", acc="fete", d="salle"), dict(i="carte", b="euro", q="@menu"), dict(i="horloge", q="@heure"), dict(i="calendrier", q="@réserver")],
    "J27": [dict(i="epingle", b="question", d="cuisine"), dict(i="feuille", q="@producteur"), dict(p="steak", q="@bœuf"), dict(i="coche", q="@exact")],
    "J28": [dict(i="etoile", b="plus", d="salle"), dict(i="billet", q="@addition"), dict(i="qr", q="@QR"), dict(i="cadeau", b="interdit", q="@cadeau")],
    "J29": [dict(i="graphique", d="cuisine"), dict(i="couverts", b="billet", q="@couverts"), dict(i="euro", b="poubelle", q="@coût"), dict(i="calendrier", b="croix", q="@réservations")],
    "J30": [dict(i="loupe", b="coche", d="rue"), dict(t="fiche"), dict(t="carte"), dict(i="etoile", b="commentaire", q="@avis")],
    "HS1": [dict(i="loupe"), dict(i="epingle", b="horloge", q="@lieux"), dict(l=True, q=["@carte", "@prix", "@horaires"]), dict(t="vide")],
    "HS2": [dict(i="epingle"), dict(i="loupe", q="@recoin"), dict(i="boutique", b="question", q="@restaurant"), dict(l=True, q=["@plats", "@prix", "@mise à jour"])],
    "HS3": [dict(p="burger"), dict(t="recherche", ecran=dict(requete="où manger près de moi", quand="@cherche")), dict(t="fiche", ecran=dict(manque="Carte", quand="@rien")),
            dict(c="client", o="telephone", e="doute", q="@rien")],
    "HS4": [dict(i="cadenas"), dict(i="boutique", b="epingle", q="@inverse"), dict(t="vide"), dict(l=True, q=["@carte", "@prix", "@horaires"])],
    "HS5": [dict(i="cadenas", b="question"), dict(p="steak", b="euro", q="@assiette"), dict(i="billet", b="coche", q="@prix"),
            dict(t="carte", ecran=dict(defile=False, change=dict(plat="Bavette", prix="19 €", quand="@modifiez")))],
    "HS6": [dict(i="eclair", b="question"), dict(i="loupe", q="@raccourcis"), dict(l=True, q=["@fiche", "@carte", "@QR"]), dict(i="coche", q="@concrètes")],
    "HS7": [dict(i="epingle"), dict(i="boutique", b="question", q="@restaurant"), dict(l=True, q=["@appeler", "@itinéraire"], puces=["telephone", "epingle"]), dict(i="telephone", b="epingle", q="@boutons")],
    "HS8": [dict(i="rafraichir"), dict(i="carte", b="question", q="@carte"), dict(c="cliente", e="triste", q="@client"), dict(i="calendrier", b="coche", q="@date")],
}


def page(nom, cercle=None, **k):
    """Une vue de la vraie page de démonstration du site (specs/images/) dans le téléphone. Elle défile ; ou bien, avec
    cercle = (x, y, rx, ry, quand), elle reste en place et un trait entoure à cet instant ce dont parle Margot."""
    if cercle:
        return dict(ecran=dict(type="image", src=f"images/{nom}.png", defile=False, **k), pastille="Page d'exemple", cercle=cercle)
    return dict(ecran=dict(type="image", src=f"images/{nom}.png", **k), pastille="Page d'exemple")


FETES = [{"titre": "Menu de fêtes", "plats": [["Velouté de châtaignes", "9 €"], ["Chapon rôti, purée maison", "24 €"], ["Bûche au chocolat", "8 €"]]},
         {"titre": "Plats", "plats": [["Bavette, frites maison", "18 €"], ["Poisson du marché", "19 €"]]}, {"titre": "Desserts", "plats": [["Tarte du jour", "7 €"]]}]
# DEMO : la phrase qui présente le site (dernière scène d'origine, avant « Écrivez menu… ») devient une scène « telephone ».
# titre = ce que dit la phrase, en deux lignes ; ecran = ce que montre le téléphone ; pastille = la mention posée à côté.
DEMO = {
    "J02": dict(titre=["Vos photos", "sur *votre page*"], **page("page-haut", defile_de="@page")),
    "J04": dict(titre=["Un prix change ?", "*Quelques secondes*"], ecran=dict(type="carte", defile=False, change=dict(plat="Bavette", prix="19 €", quand="@modifiez")), pastille="Exemple"),
    "J06": dict(titre=["La réservation", "*en ligne*"], ecran=dict(type="reservation", quand="@confirmation"), pastille="Exemple"),
    "J08": dict(titre=["Modifiable", "*quand vous voulez*"], **page("page-plats")),
    "J10": dict(titre=["Vos horaires", "*sur votre page*"], **page("page-haut", defile_de=0.3, defile_a="@page"), cercle=(668, 1178, 205, 160, "@votre restaurant")),
    "J12": dict(titre=["Chaque plat,", "*son nom, son prix*"], **page("page-plats")),
    "J14": dict(titre=["Votre page", "*dans le répertoire*"], **page("page-haut", cercle=(642, 1023, 193, 27, "@ville"))),
    "J16": dict(titre=["Votre menu de fêtes", "*en quelques minutes*"], ecran=dict(type="carte", defile=False, rubriques=FETES), pastille="Exemple"),
    "J18": dict(titre=["Votre carte", "*du moment*"], **page("page-carte", cercle=(640, 704, 182, 46, "@date"))),
    "J20": dict(titre=["La réservation", "*en ligne*"], ecran=dict(type="reservation"), pastille="Exemple"),
    "J22": dict(titre=["Vos boissons,", "*comme vos plats*"], **page("page-boissons")),
    "J24": dict(titre=["La date de", "*mise à jour*"], **page("page-carte", cercle=(640, 704, 182, 46, "@date"))),
    "J26": dict(titre=["Menu de réveillon", "*et réservation*"], ecran=dict(type="reservation", champs=[["Date", "31 décembre"], ["Heure", "20 h"], ["Personnes", "4"]]), pastille="Exemple"),
    "J28": dict(titre=["Un QR code", "*et des affichettes*"], ecran=dict(type="qr"), pastille="Exemple"),
    "J30": dict(titre=["Une page", "*à votre nom*"], **page("page-haut", cercle=(585, 955, 150, 60, "@nom"))),
    "HS1": dict(titre=["Votre carte", "*en ligne*"], **page("page-carte", defile_de=0.3)),
    "HS2": dict(titre=["Votre carte", "*en ligne*"], **page("page-carte", defile_de=0.3)),
    "HS3": dict(titre=["Votre carte", "*en ligne*"], **page("page-carte", defile_de=0.3)),
    "HS4": dict(titre=["Une page", "*à votre nom*"], **page("page-haut", cercle=(585, 955, 150, 60, "@nom"))),
    "HS6": dict(titre=["La carte", "*et le QR code*"], ecran=dict(type="qr"), pastille="Exemple"),
}
CODES = [f"J{n:02d}" for n in range(2, 31)] + [f"HS{n}" for n in range(1, 9)]
APPEL = "Écrivez menu"                                            # le début de la phrase d'appel, dans toutes les dernières scènes « MENU »


def plus(q, d):
    """Le même « quand », d secondes plus tard."""
    if isinstance(q, (int, float)):
        return round(q + d, 2)
    if isinstance(q, str) and q.startswith("@"):
        return {"mot": q[1:], "decale": d}
    return {**q, "decale": round(q.get("decale", 0) + d, 2)}


def heure(q, voix, mots):
    """À combien de secondes du début de la scène est dit le mot q (« @mot »), d'après le calage. None si q n'est pas un mot."""
    if not (isinstance(q, str) and q.startswith("@")):
        return None
    simple = lambda t: "".join(c for c in unicodedata.normalize("NFD", t.lower().replace("œ", "oe")) if unicodedata.category(c) != "Mn")
    parties = lambda t: [x for x in re.split(r"[^a-z0-9]+", simple(t)) if x]
    plat = [(x, j) for j, m in enumerate(jetons(voix)) for x in parties(m)]
    ch = parties(q)
    for i in range(len(plat) - len(ch) + 1):
        if [x for x, _ in plat[i:i + len(ch)]] == ch:
            return mots[plat[i][1]][0] - mots[0][0] + 0.45
    raise SystemExit(f"« {q} » n'est pas dans : {voix}")


def coupe(code, n_avant, cal):
    """Partage en deux la dernière scène du calage, après son n_avant-ième mot : la coupe tombe au milieu du premier silence
    (au moins 70 ms) qui suit la fin de la première phrase, donc avant la reprise de souffle, qui reste avec la seconde.
    Renvoie la durée de ce silence, ou False (sans rien changer) s'il n'y en a pas."""
    sc = cal["scenes"][-1]
    mots = sc["mots"]
    son, sr = sf.read(str(next(p for p in (ICI / "voix" / f"{code}.flac", ICI / "voix" / f"{code}.wav") if p.exists())), dtype="float32")
    son = son.mean(axis=1) if son.ndim > 1 else son
    a, b = int((mots[n_avant - 1][1] - 0.08) * sr), int(min(sc["fin"], mots[n_avant][0] + 0.45) * sr)
    pas = sr // 100                                               # volume par tranches de 10 ms
    calme = [float(np.abs(son[i:i + pas]).max()) < 0.02 for i in range(a, b, pas)]
    i = 0
    while i < len(calme):
        j = i
        while j < len(calme) and calme[j]:
            j += 1
        if j - i >= 7:
            t = round((a + (i + j) // 2 * pas) / sr, 3)
            cal["scenes"][-1:] = [{"debut": sc["debut"], "fin": t, "mots": mots[:n_avant]}, {"debut": t, "fin": sc["fin"], "mots": mots[n_avant:]}]
            return round((j - i) * pas / sr, 2)
        i = j + 1
    return False


TARD = 1.6                                                        # au-delà, l'illustration n'attend pas son mot : elle arrive avec la voix


def illustre(m, sc, garde, premiere, mots):
    """Une scène d'accroche ou de conseil, d'après son entrée dans la table T.
    L'illustration arrive sur son mot ; si ce mot vient tard, elle arrive dès que Margot parle, et c'est le badge, la bulle
    et le geste de Margot qui tombent sur le mot."""
    titre, pose = sc.get("titre", []), sc.get("pose", "bonjour")
    q = m.get("q")
    t = None if m.get("l") else heure(q, sc["voix"], mots)
    tot = "voix" if t is not None and t > TARD else q                # quand l'illustration arrive
    if m.get("l"):                                                # les pastilles deviennent une liste qui se coche, mot après mot
        puces = m.get("puces") or [None] * len(sc["puces"])
        return {"plan": "liste", **garde, "titre": titre, "pose": pose, "expression": "joie",
                "liste": {"taille": 68, "items": [{"texte": t, "quand": k, **({"puce": p} if p else {})} for t, k, p in zip(sc["puces"], q, puces)]}}
    if "t" in m:                                                  # un écran : le plan « telephone », Margot le montre du doigt
        tel = {"ecran": {"type": m["t"], **m.get("ecran", {})}}
        s = {"plan": "telephone", **garde, "titre": titre, "telephone": tel, "expression": "joie"}
        if premiere:
            tel.update({"quand": 0, "entree": "aucune"})
    elif "c" in m:                                                # un personnage : le plan « duo », côte à côte avec Margot
        d = {"role": m["c"], "expression": m.get("e", "neutre"), **({"objet": m["o"]} if m.get("o") else {})}
        arrive = 0 if premiere else tot if tot is not None else 0.35
        mot = q if tot == "voix" else plus(arrive, 0.3)              # l'instant du geste et de la bulle
        d["quand"] = arrive
        if premiere:
            d["entree"] = "aucune"
        geste = {"joie": "saut", "doute": "non", "colere": "non"}.get(d["expression"])
        if geste:
            d["gestes"] = [{"quand": mot, "geste": geste}]
        if m.get("bulle"):
            d["repliques"] = [{"qui": m["c"], "texte": m["bulle"], "quand": mot}]
        s = {"plan": "duo", **garde, "titre": titre, "duo": d, "pose": pose}
        if not premiere and q is not None:
            s["gestes"] = [{"quand": q, "pose": "pointe"}, {"quand": q, "expression": "joie"}]
    else:                                                         # une icône ou un plat : le plan « montre »
        e = {"type": "icone", "nom": m["i"]} if "i" in m else {"type": "plat", "nom": m["p"]}
        if m.get("b"):
            e["badge"] = m["b"]
        if premiere:
            e["quand"] = 0.25
        elif tot is not None:
            e["quand"] = tot
            if tot == "voix" and e.get("badge"):
                e["badge_quand"] = q
        s = {"plan": "montre", **garde, "titre": titre, "montre": e, "pose": pose}
        if not premiere and q is not None:
            s["gestes"] = [{"quand": q, "pose": "pointe"}, {"quand": q, "expression": "joie"}]
        if sc.get("puces"):
            s["puces"] = sc["puces"]
    if premiere:                                                  # l'accroche : tout est en place dès la première image
        s.update({"anime": "fixe", "taille_titre": 88 if s["plan"] == "telephone" else 100, "entree": "aucune", "expression": "malice"})
        if s["plan"] != "telephone":
            s["gestes"] = [{"quand": {"part": 0.5}, "pose": "pointe"}, {"quand": {"part": 0.5}, "expression": "joie"}]
    return s


def niveau(spec, code, cal):
    """Le scénario mis à niveau. Renvoie (scénario, calage à écrire ou None)."""
    table, scenes, n = T[code], spec["scenes"], len(spec["scenes"])
    acc = next((m["acc"] for m in table if m.get("acc")), None)
    out = {"note": "Mis à niveau le 15/11/2026 par mettre_a_niveau.py : mêmes mots dits, même prise de voix ; plans « montre », « duo », « telephone », « liste » et « fin », "
                   "jeu fin, accroche lisible dès la première image. Les écrans « image » montrent la page de démonstration du site (restaurant fictif, marquée « Exemple fictif »), "
                   "lue le 15/11/2026 ; les autres écrans sont des exemples dessinés.",
           "etiquette": spec.get("etiquette"), "jeu": "fin", "soustitres": "karaoke", "progression": True, "scenes": []}
    nouveau_cal = None
    for i, sc in enumerate(scenes):
        garde = {k: sc[k] for k in ("fond", "decor", "accessoire", "voix") if k in sc}
        if acc:
            garde["accessoire"] = acc
        if i < n - 1:
            m = table[i]
            if m.get("d") and "decor" not in garde:
                garde["decor"] = m["d"]
            s = illustre(m, sc, garde, i == 0, cal["scenes"][i]["mots"])
            if i:
                s["transition"] = "glisse-gauche"
            if m.get("neige"):
                s["elements"] = s.get("elements", []) + [{"type": "particules", "genre": "neige"}]
            out["scenes"].append(s)
            continue
        voix = sc["voix"]
        if "MENU" not in " ".join(sc.get("titre", [])):               # « Enregistrez et partagez »
            out["scenes"].append({"plan": "fin", **garde, "transition": "zoom", "titre": ["Enregistrez", "et *partagez*"],
                                  "appel": {"genre": "enregistrer", "x": 322, "y": 722, "texte": "Enregistrez", "quand": "@Enregistrez", "delai": 0.45},
                                  "elements": [{"type": "appel", "genre": "envoyer", "x": 758, "y": 722, "texte": "Envoyez-la", "quand": "@envoyez-la"}],
                                  "pose": "pouce", "expression": "joie", "gestes": [{"quand": "@envoyez-la", "geste": "hoche"}, {"quand": "@demain", "pose": "bonjour"}]})
            continue
        demo, k = DEMO.get(code), voix.find(APPEL)
        if demo and k > 0:                                           # la phrase sur le site devient une scène à part
            p1, p2 = voix[:k].strip(), voix[k:].strip()
            assert jetons(p1) + jetons(p2) == jetons(voix), code
            silence = coupe(code, len(jetons(p1)), cal)
            if silence:
                nouveau_cal = cal
                print(f"  {code} : dernière scène partagée en deux (silence de {silence} s entre les deux phrases)")
                e = {"plan": "telephone", **garde, "fond": "or", "voix": p1, "apres": 0.25, "transition": "glisse-gauche", "titre": demo["titre"], "telephone": {"ecran": demo["ecran"]}, "expression": "joie",
                     "elements": [{"type": "texte", "style": "pastille", "texte": demo["pastille"], "taille": 32, "x": 205, "y": 1000, "quand": 0.5}]}
                if demo.get("cercle"):
                    x, y, rx, ry, quand = demo["cercle"]
                    e["elements"].append({"type": "forme", "forme": "cercle", "x": x, "y": y, "rx": rx, "ry": ry, "couleur": "rouge", "ep": 9, "quand": quand})
                out["scenes"].append(e)
                voix, garde = p2, {**garde, "avant": 0.2}             # la reprise de souffle ouvre déjà la scène : peu de silence avant
            else:
                print(f"  {code} : silence trop court entre les deux phrases, la dernière scène reste entière")
        fin = {"plan": "fin", **garde, "voix": voix, "transition": "zoom", "titre": ["Commentez", "*MENU*"], "appel": {"genre": "commenter", "mot": "MENU", "mot_quand": "@Écrivez"},
               "puces": sc.get("puces", []), "pose": "telephone", "expression": "joie",
               "gestes": [{"quand": "@recontactons", "pose": "pouce"}, {"quand": "@recontactons", "geste": "saut"}],
               "elements": [{"type": "particules", "genre": "confettis", "quand": {"mot": "Écrivez", "decale": 0.9}}]}
        if "carte en ligne" in voix[voix.find(APPEL):]:
            fin["gestes"].append({"quand": {"mot": "carte", "n": voix[:voix.find("recontactons")].lower().count("carte") + 1}, "pose": "carte"})
        if "Merci" in voix:                                          # le dernier jour : Margot remercie
            fin["gestes"] += [{"quand": "@Merci", "pose": "fete"}, {"quand": "@Merci", "expression": "amour"}, {"quand": "@Merci", "geste": "saut"}]
            fin["elements"].append({"type": "particules", "genre": "coeurs", "quand": "@Merci"})
        out["scenes"].append(fin)
    return out, nouveau_cal


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    source = pathlib.Path(sys.argv[1])
    for code in sys.argv[2:] or CODES:
        spec = json.loads((source / f"{code}.json").read_text(encoding="utf-8"))
        if "jeu" in spec:
            raise SystemExit(f"{code} : ce scénario est déjà mis à niveau ; donnez le dossier des scénarios d'origine.")
        origine = source / "voix" / f"{code}.json"
        texte_cal = (origine if origine.exists() else ICI / "voix" / f"{code}.json").read_text(encoding="utf-8")
        cal = json.loads(texte_cal)
        if len(cal["scenes"]) != len(spec["scenes"]):
            raise SystemExit(f"{code} : le calage n'est pas celui d'origine ; placez-le dans {source}/voix/.")
        neuf, ncal = niveau(spec, code, cal)
        (ICI / "specs" / f"{code}.json").write_text(json.dumps(neuf, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (ICI / "voix" / f"{code}.json").write_text(json.dumps(ncal, ensure_ascii=False, indent=1) + "\n" if ncal else texte_cal, encoding="utf-8")
        print(code, "mis à niveau :", len(neuf["scenes"]), "scènes")


if __name__ == "__main__":
    main()
