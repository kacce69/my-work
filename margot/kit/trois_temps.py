#!/usr/bin/env python3
"""Récrit les scénarios « en trois temps », à la demande d'Owen (19/11/2026) :
  1. l'accroche : une première phrase de moins de 12 mots, puis une question (ou une annonce vraie)
     dont la réponse n'arrive qu'au dernier conseil ;
  2. la valeur : trois conseils, le plus utile en dernier, et la réponse à la question de l'accroche ;
  3. le bénéfice : une scène « À retenir » (les trois points à l'écran, une phrase dite), puis l'appel, raccourci.
Les faits et les conseils ne changent pas : seule l'écriture change. Chaque Reel demande donc une nouvelle prise de voix.

    python3 trois_temps.py <dossier des scénarios d'avant> [codes…]

Lit <dossier>/<code>.json, écrit specs/<code>.json. Les textes sont dans la table T ci-dessous.
Clés de T[code] : s1 (voix de la scène 1), t1 (son titre, si l'accroche change), v {n° de scène d'origine: voix},
t {n°: titre}, ordre (ordre des scènes de conseils, par n° d'origine), r (phrase « À retenir »), items (les trois points
affichés, sinon les titres des conseils), apres (n° d'origine de la scène après laquelle vient « À retenir » ; par défaut le
dernier conseil), fin (voix de la dernière scène), q {n°: {ancien déclencheur: nouveau}}.
"""
import json, pathlib, re, sys

ICI = pathlib.Path(__file__).resolve().parent
FIN_IMPAIR = "Enregistrez cette vidéo, et envoyez-la à un collègue restaurateur."
FIN_PAIR = "Écrivez menu en commentaire, et nous vous recontactons."

T = {
 "J05": {"s1": "Un avis négatif vient de tomber ? Faut-il tout régler par écrit ? Réponse à la troisième étape.",
         "v": {4: "Trois : dites ce que vous avez changé, et proposez d'en reparler par téléphone. Tout ne se règle pas par écrit."},
         "r": "À retenir : on répond à froid, et on propose d'en reparler."},
 "J06": {"s1": "Une table réservée, et personne ne vient ? Faut-il compliquer l'annulation ? Réponse à la troisième habitude.",
         "v": {4: "Trois, au contraire : dites clairement comment annuler. Un client qui sait comment prévenir a moins d'excuses."},
         "r": "À retenir : un numéro, un rappel, et une annulation facile.",
         "items": ["Un numéro de téléphone", "Un rappel la veille", "Une annulation facile"]},
 "J07": {"s1": "Votre ardoise du jour se lit-elle en cinq secondes ? Et le prix, où le mettre ? Réponse au troisième conseil.",
         "ordre": [2, 4, 3],
         "v": {4: "Deux : des mots simples. Le produit, la cuisson, la garniture.",
               3: "Trois, le prix : le nom du plat d'abord, en gros, puis le prix bien aligné."},
         "r": "À retenir : peu de plats, des mots simples, et le prix bien aligné.",
         "items": ["Peu de plats", "Des mots simples", "Le plat, puis le prix"]},
 "J08": {"s1": "Vos plats les plus commandés vous rapportent-ils vraiment ? Et que faire des autres ? Réponse à la troisième étape.",
         "r": "À retenir : comptez, calculez, classez, puis décidez plat par plat.",
         "items": ["Comptez les ventes", "Calculez la marge", "Classez vos plats"]},
 "J09": {"s1": "Un QR code que personne ne scanne ne sert à rien. Et peut-il remplacer la carte papier ? Réponse au troisième point.",
         "v": {4: "Trois : non, il ne remplace pas tout. Gardez une carte papier et l'affichage des prix : le QR code seul ne suffit pas."},
         "r": "À retenir : sur la table, en vitrine, mais jamais tout seul.",
         "items": ["Sur chaque table", "En vitrine", "Jamais seul"]},
 "J10": {"s1": "Vous fermez un jour férié ? Trois endroits où le dire, et un détail à ne pas oublier.",
         "v": {4: "Trois : une affichette sur la porte. Et le détail à ne pas oublier : la date de réouverture."},
         "r": "À retenir : prévenez avant, partout où vos clients vous cherchent.",
         "items": ["Votre fiche Google", "Réseaux et répondeur", "Sur la porte"]},
 "J11": {"s1": "Trop de plats sur votre carte ? Quand un plat doit-il la quitter ? Réponse en trois questions.",
         "r": "À retenir : peu vendu, peu rentable, compliqué à servir : le plat peut partir.",
         "items": ["Se vend-il ?", "Est-il rentable ?", "Simple à servir ?"]},
 "J12": {"s1": "Poisson du jour, ça ne dit pas grand-chose. Trois précisions, et à la fin, le nom complet du plat.",
         "r": "À retenir : filet de cabillaud rôti, purée maison. Le produit, la cuisson, la garniture.",
         "items": ["Le produit", "La cuisson", "Garniture ou origine"]},
 "J13": {"s1": "L'affichage des prix est obligatoire, à l'intérieur comme à l'extérieur. Et le service, est-il compris ? Réponse au troisième point.",
         "v": {4: "Trois : oui, le prix affiché comprend les taxes et le service."},
         "r": "À retenir : affichés dehors, identiques dedans, taxes et service compris.",
         "items": ["Affichés dehors", "Identiques dedans", "Taxes et service compris"]},
 "J14": {"s1": "Quand on cherche un restaurant dans votre ville, apparaissez-vous ? Trois réglages, et un détail qui doit être identique partout.",
         "ordre": [2, 4, 3],
         "v": {4: "Deux : répondez à vos avis. Une fiche vivante inspire confiance.",
               3: "Trois, le détail : le même nom, la même adresse et le même téléphone partout où vous apparaissez."},
         "r": "À retenir : une fiche complète, des avis avec réponse, les mêmes infos partout.",
         "items": ["Fiche Google complète", "Des avis avec réponse", "Les mêmes infos partout"]},
 "J15": {"s1": "Pas d'idée pour Instagram ? Trois publications à refaire chaque semaine, dont une pour les semaines sans nouveauté.",
         "v": {4: "Trois, pour les semaines sans nouveauté : les infos pratiques. Horaires, fermeture, soirée à venir."},
         "r": "À retenir : un plat, les coulisses, les infos pratiques. Chaque semaine.",
         "items": ["Le plat du moment", "Les coulisses", "Les infos pratiques"]},
 "J16": {"s1": "Votre menu de fêtes est-il prêt ? Trois étapes pour l'annoncer, et une date à ne pas oublier.",
         "v": {4: "Trois, la date à ne pas oublier : donnez une date limite de réservation, et un moyen simple de réserver."},
         "r": "À retenir : un menu, un prix, une annonce, et une date limite.",
         "items": ["Le menu et son prix", "Annoncez-le partout", "Une date limite"]},
 "J17": {"s1": "Savez-vous ce que vous jetez chaque semaine ? Et que faire d'un produit qui revient ? Réponse à la troisième étape.",
         "r": "À retenir : notez, repérez, ajustez. Une semaine suffit pour commencer.",
         "items": ["Notez ce qui part", "Repérez ce qui revient", "Ajustez"]},
 "J18": {"s1": "Un client content ne revient pas toujours. Trois gestes qui aident, et le dernier se fait quand il n'est pas là.",
         "v": {4: "Trois, quand il n'est pas là : donnez des nouvelles. La carte qui change, une soirée à venir."},
         "r": "À retenir : le reconnaître, une attention, et des nouvelles entre deux visites.",
         "items": ["Reconnaissez-le", "Une attention", "Des nouvelles"]},
 "J19": {"s1": "On se perd parfois dans une carte. Trois règles pour ranger la vôtre, et un nom de rubrique à éviter.",
         "ordre": [2, 4, 3],
         "v": {4: "Deux : peu de plats par rubrique. La carte se lit plus vite.",
               3: "Trois : des noms de rubrique simples. Écrivez plats, plutôt que nos créations gourmandes."},
         "r": "À retenir : l'ordre du repas, peu de plats, des noms simples.",
         "items": ["L'ordre du repas", "Peu de plats", "Des noms simples"]},
 "J20": {"s1": "Une réservation notée trop vite, et c'est l'erreur. Trois choses à demander, dont une juste avant de raccrocher.",
         "v": {4: "Trois, avant de raccrocher : les demandes particulières. Allergie, chaise haute, anniversaire."},
         "r": "À retenir : qui, quand, combien, et les demandes particulières.",
         "items": ["Nom, date et heure", "Couverts et téléphone", "Demandes particulières"]},
 "J21": {"s1": "Votre formule du midi est-elle rentable ? Et combien de choix proposer ? Réponse au troisième point.",
         "r": "À retenir : un coût connu, un prix comparé, et peu de choix.",
         "items": ["Le coût de chaque plat", "Le total face au prix", "Peu de choix"]},
 "J22": {"s1": "On soigne la carte des plats, on oublie celle des boissons. Trois idées, et ce qu'il faut écrire à côté de chaque prix.",
         "ordre": [2, 4, 3],
         "v": {4: "Deux : proposez quelques vins au verre, bien visibles.",
               3: "Trois, à côté de chaque prix : indiquez la contenance de chaque boisson."},
         "r": "À retenir : des familles, des vins au verre, la contenance et le prix.",
         "items": ["Par familles", "Des vins au verre", "La contenance et le prix"]},
 "J23": {"s1": "Un passant ne regarde votre vitrine que quelques secondes. Trois choses à lui montrer, dont une quand vous êtes fermé.",
         "v": {4: "Trois, même fermé : une vitrine propre et éclairée, y compris en dehors du service."},
         "r": "À retenir : la carte, les horaires, et la lumière, même fermé.",
         "items": ["La carte et les prix", "Les horaires", "Propre et éclairée"]},
 "J24": {"s1": "Votre carte est-elle passée à l'hiver ? Trois idées simples, et la dernière consiste à enlever.",
         "v": {4: "Trois, ce qu'on enlève : retirez les plats d'été. Une carte courte, et de saison."},
         "r": "À retenir : de saison, qui réchauffe, et sans les plats d'été.",
         "items": ["Des produits de saison", "Un plat qui réchauffe", "Sans les plats d'été"]},
 "J25": {"s1": "Proposez-vous des bons cadeaux pour Noël ? Trois étapes, et le bon moment pour en parler à vos clients.",
         "v": {4: "Trois : faites-le savoir. En salle, sur vos réseaux, et au bon moment : avec l'addition."},
         "r": "À retenir : une formule, une date de validité, et un mot avec l'addition.",
         "items": ["Un montant ou un menu", "Une date de validité", "Faites-le savoir"]},
 "J26": {"s1": "Vous ouvrez pour le réveillon ? Dites-le dès maintenant. Trois informations, et sans la dernière, personne ne peut venir.",
         "v": {4: "Trois, l'indispensable : comment réserver, et jusqu'à quelle date."},
         "r": "À retenir : le menu, le prix, les horaires, et comment réserver.",
         "items": ["Le menu et le prix", "Les horaires", "Comment réserver"]},
 "J27": {"s1": "Beaucoup de clients aiment savoir d'où vient ce qu'ils mangent. Et pour quatre viandes, c'est une obligation. Lesquelles ? Réponse à la fin.",
         "ordre": [2, 4, 3],
         "v": {4: "Deux : restez exact. Si le fournisseur change, la carte change aussi.",
               3: "Trois, l'obligation : pour le bœuf, le porc, le mouton et la volaille, l'origine doit être indiquée."},
         "r": "À retenir : dites d'où ça vient, restez exact, et indiquez l'origine des viandes.",
         "items": ["Producteur ou région", "Restez exact", "L'origine des viandes"]},
 "J28": {"s1": "Vous voulez plus d'avis ? Trois règles, dont une chose à ne jamais faire.",
         "v": {4: "Trois, à ne jamais faire : pas de cadeau en échange d'un avis. Un avis doit rester libre."},
         "r": "À retenir : demandez au bon moment, facilitez, et n'achetez jamais un avis.",
         "items": ["Au moment de l'addition", "Un QR code vers la fiche", "Jamais de contrepartie"]},
 "J29": {"s1": "Vous pilotez votre restaurant au ressenti ? Cinq chiffres, une fois par semaine. Le dernier se compte en tables vides.",
         "v": {4: "Et le dernier, celui des tables vides : les réservations non honorées."},
         "r": "À retenir : notez ces cinq chiffres chaque lundi, dans un simple tableau.",
         "items": ["Couverts", "Ticket moyen", "Coût matière", "Pertes", "Réservations non honorées"]},
 "J30": {"s1": "Trente jours de conseils. S'il ne fallait en garder que trois ? Le dernier ne coûte que du temps.",
         "v": {4: "Trois, celui qui ne coûte que du temps : des réponses à vos avis, et des nouvelles régulières sur vos réseaux."},
         "r": "À retenir : une fiche à jour, une carte en ligne, des réponses aux avis.",
         "items": ["Une fiche Google à jour", "Votre carte en ligne", "Des réponses aux avis"],
         "fin": "Écrivez menu en commentaire, et nous vous recontactons. Merci de m'avoir suivie pendant ces trente jours !"},
 "HS3": {"s1": "Entre deux missions, même le meilleur joueur finit par avoir faim. Et là, votre restaurant a une partie à jouer.",
         "r": "À retenir : une carte visible en ligne, c'est une chance d'être choisi.",
         "items": ["Votre carte", "Vos prix", "Vos horaires"]},
 "HS4": {"s1": "Dans un braquage, la bonne planque, personne ne la trouve. Et votre restaurant, est-il bien caché, lui aussi ?",
         "v": {4: "À retenir : sortez de la planque. Montrez votre carte, vos prix et vos horaires."}, "sans_r": True},
 "HS5": {"s1": "Personne ne braque un coffre sans savoir ce qu'il contient. Vos clients ont la même exigence, devinez pour quoi.",
         "r": "À retenir : montrez les plats et les prix avant qu'on vous les demande.",
         "items": ["Des plats", "Des prix", "Pas de surprise"], "apres": 3, "fin": None},
 "HS6": {"s1": "Vous cherchez un code de triche pour votre restaurant ? Il n'y en a pas. Mais j'ai trois raccourcis.",
         "v": {2: "Trois raccourcis simples, pour être trouvé sur internet.",
               4: "À retenir : aucune triche. Trois choses concrètes, à mettre en place puis à tenir à jour."}, "sans_r": True},
 "HS7": {"s1": "Dans le jeu, le GPS vous mène partout en un instant. Jusqu'à votre restaurant, il suffit de deux boutons. Lesquels ?",
         "v": {3: "Il faut deux boutons bien visibles : appeler, et itinéraire. C'est tout ce qu'il y a à retenir."}, "sans_r": True, "fin": None},
 "HS8": {"s1": "Même les plus gros jeux reçoivent des mises à jour. Et votre carte, de quand date la dernière ?",
         "v": {2: "Un prix qui change, un plat retiré : est-elle encore juste ?"},
         "r": "À retenir : une carte datée et à jour évite un client déçu.",
         "items": ["Un prix qui change", "Un plat retiré", "La date de mise à jour"], "apres": 3, "fin": None},
}

def sans_numero(lignes):
    return re.sub(r"^\d+\.\s*", "", " ".join(lignes)).replace("*", "").strip()

def remplace(o, table):
    """Remplace les déclencheurs « quand » devenus sans objet (mot retiré du texte)."""
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ("quand", "mot_quand") and isinstance(v, (str, dict)):
                cle = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, sort_keys=True)
                if cle in table: o[k] = table[cle]
            else: remplace(v, table)
    elif isinstance(o, list):
        for v in o: remplace(v, table)

def trois_temps(spec, code):
    m = T[code]; sc = spec["scenes"]; n = len(sc)
    pair = sc[-1].get("appel", {}) and (sc[-1]["appel"] if isinstance(sc[-1]["appel"], str) else sc[-1]["appel"].get("genre")) == "commenter"
    # 1. l'accroche
    sc[0]["voix"] = m["s1"]
    if "t1" in m: sc[0]["titre"] = m["t1"]
    # 2. les conseils : textes, titres, ordre
    for k, v in m.get("v", {}).items(): sc[k - 1]["voix"] = v
    for k, t in m.get("t", {}).items(): sc[k - 1]["titre"] = t
    for k, tb in m.get("q", {}).items():
        remplace(sc[k - 1], {(a if a.startswith("@") or not a.startswith("{") else a): b for a, b in tb.items()})
    if "ordre" in m:
        places = sorted(m["ordre"]); fonds = [sc[p - 1].get("fond") for p in places]; trans = [sc[p - 1].get("transition") for p in places]
        nouvelles = [sc[o - 1] for o in m["ordre"]]
        for i, (p, s) in enumerate(zip(places, nouvelles)):
            s = dict(s); s["fond"] = fonds[i]
            if trans[i]: s["transition"] = trans[i]
            if s.get("titre") and re.match(r"^\d+\.\s", s["titre"][0]): s["titre"] = [re.sub(r"^\d+\.", f"{i + 1}.", s["titre"][0])] + s["titre"][1:]
            sc[p - 1] = s
    # 3. « À retenir » (sans_r : la phrase est déjà dans une scène, pas de scène ajoutée)
    if m.get("sans_r"): return fin_de(spec, sc, m, pair)
    apres = m.get("apres", n - 2 if pair and sc[-2].get("plan") == "telephone" else n - 1)
    conseils = [s for s in sc[1:apres] if s.get("titre")][-3:]
    items = m.get("items") or [sans_numero(s["titre"]) for s in conseils]
    suivant = sc[apres].get("fond"); avant = sc[apres - 1].get("fond")
    fond = next(f for f in ("or", "prune", "creme") if f not in (suivant, avant))
    retenir = {"plan": "liste", "fond": fond, "voix": m["r"], "avant": 0.3, "apres": 0.3, "transition": "glisse-gauche",
               "titre": ["À *retenir*"], "pose": "index", "expression": "malice",
               "liste": {"taille": m.get("taille") or max(58, min(74, int(740 / (0.5 * max(len(t) for t in items))))),
                         "items": [{"texte": t, "quand": round(0.35 + 0.45 * i, 2)} for i, t in enumerate(items)]},
               "gestes": [{"quand": {"part": 0.55}, "expression": "joie"}]}
    sc.insert(apres, retenir)
    return fin_de(spec, sc, m, pair)

def fin_de(spec, sc, m, pair):
    """L'appel, raccourci (fin: None garde la phrase d'origine)."""
    f = sc[-1]; ancienne = f.get("voix", "")
    if not ("fin" in m and m["fin"] is None): f["voix"] = m.get("fin") or (FIN_PAIR if pair else FIN_IMPAIR)
    if f["voix"] != ancienne:
        remplace(f, {"@demain": {"avant_fin": 0.7}, json.dumps({"mot": "carte", "n": 1}, ensure_ascii=False, sort_keys=True): {"avant_fin": 0.6}})
    spec["note"] = (spec.get("note", "") + " Récrit en trois temps le 19/11/2026 par trois_temps.py (accroche et question ouverte, meilleur conseil en dernier, scène « À retenir ») : nouvelle prise de voix.").strip()
    return spec

def main():
    src = pathlib.Path(sys.argv[1]); codes = sys.argv[2:] or sorted(T)
    for c in codes:
        if c not in T: print(f"{c} : pas de texte dans la table"); continue
        spec = trois_temps(json.loads((src / f"{c}.json").read_text(encoding="utf-8")), c)
        (ICI / "specs" / f"{c}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        mots = sum(len(s.get("voix", "").split()) for s in spec["scenes"])
        acc = re.split(r"(?<=[?!.])\s", spec["scenes"][0]["voix"])[0]
        print(f"{c} : {len(spec['scenes'])} scènes, {mots} mots ; accroche de {len(acc.split())} mots")

if __name__ == "__main__":
    main()
