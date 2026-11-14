#!/usr/bin/env python3
"""Écrit les 30 scénarios de Reels (specs/J01.json … J30.json) de la campagne « Margot, 30 jours ».
Jours impairs : conseil pur. Jours pairs : la dernière scène parle de Restaurant Site Internet
et invite à commenter MENU. Chaque Reel reprend le thème de l'article du même jour."""
import json, pathlib

ICI = pathlib.Path(__file__).resolve().parent
FONDS = ["creme", "prune", "or", "creme", "prune"]
POSES = ["bonjour", "pouce", "carte", "pouce"]
FIN_IMPAIR = "Enregistrez cette vidéo, et envoyez-la à un collègue restaurateur. À demain !"
FIN_PAIR = " Écrivez menu en commentaire, et nous vous recontactons pour mettre votre carte en ligne."

R = {}


def reel(j, accroche, voix, conseils, sol=None, fin=None, puces=None):
    """puces : {numéro de scène (0 = accroche): [textes]}"""
    R[j] = dict(accroche=accroche, voix=voix, conseils=conseils, sol=sol, fin=fin, puces=puces or {})


reel(1, ["Votre fiche Google", "est-elle à jour ?"], "Votre fiche Google est-elle vraiment à jour ? Voici trois points à vérifier aujourd'hui.", [
    (["1. Les horaires", "exceptionnels"], "Un : vos horaires exceptionnels. Jours fériés, congés : annoncez-les avant, pas après."),
    (["2. Le lien", "vers la carte"], "Deux : le lien vers votre carte. Il doit mener à la carte du moment, avec les prix."),
    (["3. Des photos", "récentes"], "Trois : des photos récentes. La devanture, la salle, et quelques plats de la carte actuelle.")])

reel(2, ["Vos photos de plats", "donnent-elles faim ?"], "Vos photos de plats donnent-elles vraiment faim ? Trois gestes simples, avec un téléphone.", [
    (["1. La lumière", "du jour"], "Un : la lumière du jour. Posez l'assiette près d'une fenêtre, sans flash."),
    (["2. Un objectif", "propre"], "Deux : essuyez l'objectif du téléphone, et le bord de l'assiette."),
    (["3. Un seul plat", "bien cadré"], "Trois : un seul plat par photo, cadré de près, sur une table dégagée.")],
    sol="Sur Restaurant Site Internet, vos photos s'affichent sur la page de votre restaurant, avec votre carte.")

reel(3, ["Allergènes :", "savez-vous répondre ?"], "Un client vous demande s'il y a des fruits à coque dans un plat. Savez-vous répondre tout de suite ?", [
    (["1. Quatorze", "allergènes"], "Un : il existe quatorze allergènes à déclaration obligatoire. Gardez la liste sous la main."),
    (["2. Par écrit,", "plat par plat"], "Deux : l'information doit être disponible par écrit. Notez les allergènes plat par plat."),
    (["3. À jour à chaque", "changement"], "Trois : mettez-la à jour à chaque changement de recette ou de fournisseur.")])

reel(4, ["Combien vous coûte", "ce plat ?"], "Savez-vous combien vous coûte vraiment votre plat du jour ? Le calcul tient en trois étapes.", [
    (["1. Les ingrédients", "et les quantités"], "Un : listez chaque ingrédient, avec la quantité pour une portion."),
    (["2. Le coût", "de la portion"], "Deux : multipliez par le prix d'achat, puis additionnez. C'est votre coût matière."),
    (["3. Comparez au", "prix de vente"], "Trois : comparez ce coût à votre prix de vente hors taxes.")],
    sol="Et si un prix doit changer, sur Restaurant Site Internet, vous le modifiez en quelques secondes depuis votre téléphone.")

reel(5, ["Un avis négatif ?", "Pas de panique"], "Un avis négatif vient de tomber ? Ne répondez pas à chaud. Voici comment faire.", [
    (["1. Remerciez"], "Un : remerciez la personne d'avoir pris le temps d'écrire."),
    (["2. Reconnaissez", "les faits"], "Deux : reconnaissez ce qui s'est mal passé, sans vous justifier longuement."),
    (["3. Proposez", "d'en parler"], "Trois : dites ce que vous avez changé, et proposez d'en reparler par téléphone.")])

reel(6, ["Table réservée,", "personne ne vient ?"], "Une table réservée, et personne ne vient ? Trois habitudes pour limiter les réservations non honorées.", [
    (["1. Un numéro", "de téléphone"], "Un : prenez toujours un numéro de téléphone avec la réservation."),
    (["2. Un rappel", "la veille"], "Deux : envoyez un petit message de rappel la veille, ou le matin même."),
    (["3. Une annulation", "facile"], "Trois : dites clairement comment annuler. Un client qui sait comment prévenir a moins d'excuses.")],
    sol="Sur Restaurant Site Internet, vous pouvez activer la réservation de table en ligne, avec une confirmation par e-mail.")

reel(7, ["Votre ardoise", "se lit-elle vite ?"], "Votre ardoise du jour se lit-elle en cinq secondes ? Sinon, voici comment la simplifier.", [
    (["1. Peu de plats"], "Un : peu de choix. Deux ou trois plats du jour suffisent."),
    (["2. Le plat,", "puis le prix"], "Deux : le nom du plat d'abord, en gros, puis le prix bien aligné."),
    (["3. Des mots", "simples"], "Trois : des mots simples. Le produit, la cuisson, la garniture.")])

reel(8, ["Vos plats stars", "sont-ils rentables ?"], "Vos plats les plus commandés sont-ils aussi ceux qui vous rapportent ?", [
    (["1. Comptez", "les ventes"], "Un : comptez les ventes de chaque plat sur un mois."),
    (["2. Calculez", "la marge"], "Deux : calculez la marge de chaque plat. Prix de vente, moins coût matière."),
    (["3. Classez", "vos plats"], "Trois : classez. Un plat populaire et rentable se met en avant. Un plat ni l'un ni l'autre se discute.")],
    sol="Sur Restaurant Site Internet, vous modifiez votre carte en ligne quand vous voulez, depuis votre téléphone.")

reel(9, ["Votre QR code", "est-il bien placé ?"], "Un QR code que personne ne scanne ne sert à rien. Voici où le mettre.", [
    (["1. Sur la table"], "Un : sur chaque table, bien visible, avec une phrase simple : scannez pour voir la carte."),
    (["2. En vitrine"], "Deux : en vitrine, pour ceux qui hésitent à entrer."),
    (["3. Jamais seul"], "Trois : gardez une carte papier et l'affichage des prix. Le QR code seul ne suffit pas.")])

reel(10, ["Fermé un jour férié ?", "Dites-le avant"], "Vous fermez un jour férié ? Vos clients doivent le savoir avant de se déplacer.", [
    (["1. Votre fiche", "Google"], "Un : saisissez vos horaires exceptionnels sur votre fiche Google."),
    (["2. Réseaux", "et répondeur"], "Deux : annoncez-le sur vos réseaux, et changez le message du répondeur."),
    (["3. Sur la porte"], "Trois : une affichette sur la porte, avec la date de réouverture.")],
    sol="Sur Restaurant Site Internet, vos horaires figurent sur la page de votre restaurant, et vous pouvez y afficher une annonce.")

reel(11, ["Votre carte est-elle", "trop longue ?"], "Trop de plats sur la carte ? Trois questions pour savoir lesquels retirer.", [
    (["1. Se vend-il ?"], "Un : ce plat se vend-il encore ? Regardez vos ventes du mois."),
    (["2. Est-il", "rentable ?"], "Deux : vous laisse-t-il une marge correcte ?"),
    (["3. Complique-t-il", "le service ?"], "Trois : complique-t-il la cuisine ou les stocks ? S'il se vend peu, rapporte peu et complique le service, il peut quitter la carte.")])

reel(12, ["« Poisson du jour »,", "c'est un peu court"], "Poisson du jour, ça ne dit pas grand-chose. Voici une formule simple pour nommer un plat.", [
    (["1. Le produit"], "Un : le produit précis. Dos de cabillaud, plutôt que poisson."),
    (["2. La cuisson"], "Deux : la cuisson. Rôti, poêlé, confit : on imagine déjà l'assiette."),
    (["3. La garniture", "ou l'origine"], "Trois : la garniture ou l'origine. Purée maison, légumes du marché.")],
    sol="Sur Restaurant Site Internet, chaque plat de votre carte s'affiche avec son nom et son prix, lisible sur un téléphone.")

reel(13, ["Vos prix sont-ils", "bien affichés ?"], "L'affichage des prix est obligatoire, à l'intérieur comme à l'extérieur. Trois points à vérifier.", [
    (["1. La carte", "à l'extérieur"], "Un : dehors, votre menu ou votre carte du jour doit être visible pendant tout le service."),
    (["2. Les mêmes", "à l'intérieur"], "Deux : à l'intérieur, les cartes et les menus doivent être identiques à ceux de l'extérieur."),
    (["3. Taxes et", "service compris"], "Trois : le prix affiché s'entend taxes et service compris.")],
    puces={0: ["Source : DGCCRF"]})

reel(14, ["Vous trouve-t-on", "sur Google ?"], "Quand on cherche un restaurant dans votre ville, apparaissez-vous ?", [
    (["1. Une fiche Google", "complète"], "Un : une fiche Google complète. Catégorie, horaires, photos."),
    (["2. Les mêmes infos", "partout"], "Deux : le même nom, la même adresse et le même téléphone partout où vous apparaissez."),
    (["3. Des avis", "avec réponse"], "Trois : répondez à vos avis. Une fiche vivante inspire confiance.")],
    sol="Sur Restaurant Site Internet, votre restaurant a sa page dans un répertoire, classée par ville et par type de cuisine.")

reel(15, ["Instagram :", "quoi publier ?"], "Pas d'idée pour Instagram ? Voici trois publications faciles à refaire chaque semaine.", [
    (["1. Le plat", "du moment"], "Un : le plat du moment, en photo, à la lumière du jour."),
    (["2. Les coulisses"], "Deux : les coulisses. La mise en place, le marché, l'équipe qui prépare."),
    (["3. Les infos", "pratiques"], "Trois : les infos pratiques. Horaires, fermeture, soirée à venir.")])

reel(16, ["Menu de fêtes :", "c'est le moment"], "Votre menu de fêtes est-il prêt ? Mieux vaut l'annoncer tôt.", [
    (["1. Le menu", "et son prix"], "Un : fixez le menu et son prix, en précisant si la boisson est comprise."),
    (["2. Annoncez-le", "partout"], "Deux : annoncez-le partout. En salle, sur vos réseaux, sur votre fiche Google."),
    (["3. Une date", "limite"], "Trois : donnez une date limite de réservation, et un moyen simple de réserver.")],
    sol="Sur Restaurant Site Internet, vous ajoutez votre menu de fêtes à votre carte en ligne en quelques minutes.")

reel(17, ["Que jetez-vous", "chaque semaine ?"], "Savez-vous ce que vous jetez chaque semaine ? Trois habitudes pour le réduire.", [
    (["1. Notez", "ce qui part"], "Un : pendant une semaine, notez ce qui part à la poubelle."),
    (["2. Repérez", "ce qui revient"], "Deux : repérez les produits qui reviennent le plus souvent."),
    (["3. Ajustez"], "Trois : commandez-en moins, ou faites-en un plat du jour.")])

reel(18, ["Comment faire", "revenir un client ?"], "Un client content ne revient pas toujours. Trois gestes qui aident.", [
    (["1. Reconnaissez-le"], "Un : reconnaissez-le. Un bonjour par son nom, sa table préférée."),
    (["2. Une attention"], "Deux : une petite attention. Un mot sur le plat qu'il aime, une nouveauté à goûter."),
    (["3. Des nouvelles"], "Trois : donnez des nouvelles. La carte qui change, une soirée à venir.")],
    sol="Sur Restaurant Site Internet, vos habitués retrouvent votre carte du moment, avec sa date de mise à jour.")

reel(19, ["Votre carte est-elle", "bien rangée ?"], "On se perd parfois dans une carte. Trois règles pour bien ranger la vôtre.", [
    (["1. L'ordre", "du repas"], "Un : suivez l'ordre du repas. Entrées, plats, desserts, puis boissons."),
    (["2. Des rubriques", "aux noms simples"], "Deux : des noms de rubrique simples. Plats, plutôt que nos créations gourmandes."),
    (["3. Peu de plats", "par rubrique"], "Trois : peu de plats par rubrique. La carte se lit plus vite.")])

reel(20, ["Réservation", "au téléphone"], "Une réservation notée trop vite, et c'est l'erreur. Voici ce qu'il faut toujours demander.", [
    (["1. Nom, date", "et heure"], "Un : le nom, la date et l'heure. Répétez-les à voix haute."),
    (["2. Couverts", "et téléphone"], "Deux : le nombre de couverts, et un numéro de téléphone."),
    (["3. Les demandes", "particulières"], "Trois : les demandes particulières. Allergie, chaise haute, anniversaire.")],
    sol="Et pour les heures où vous ne pouvez pas décrocher, Restaurant Site Internet propose la réservation de table en ligne.")

reel(21, ["Votre formule du midi", "est-elle rentable ?"], "Votre formule du midi est-elle rentable ? Trois points à vérifier.", [
    (["1. Le coût", "de chaque plat"], "Un : calculez le coût matière de l'entrée, du plat et du dessert."),
    (["2. Le total", "face au prix"], "Deux : comparez le total au prix de la formule, hors taxes."),
    (["3. Peu de choix"], "Trois : limitez les choix. Deux entrées, deux plats, deux desserts suffisent.")])

reel(22, ["Et votre carte", "des boissons ?"], "On soigne la carte des plats, et on oublie celle des boissons. Trois idées pour la rendre lisible.", [
    (["1. Par familles"], "Un : rangez par familles. Sans alcool, bières, vins, boissons chaudes."),
    (["2. La contenance", "et le prix"], "Deux : indiquez la contenance et le prix de chaque boisson."),
    (["3. Des vins", "au verre"], "Trois : proposez quelques vins au verre, bien visibles.")],
    sol="Sur Restaurant Site Internet, vos boissons s'ajoutent à votre carte en ligne, comme vos plats.")

reel(23, ["Que voit-on", "depuis la rue ?"], "Un passant ne regarde votre vitrine que quelques secondes. Que voit-il ?", [
    (["1. La carte", "et les prix"], "Un : la carte et les prix, lisibles sans entrer."),
    (["2. Les horaires"], "Deux : les horaires, et les jours de fermeture."),
    (["3. Propre", "et éclairée"], "Trois : une vitrine propre et éclairée, même en dehors du service.")])

reel(24, ["Votre carte est-elle", "passée à l'hiver ?"], "Votre carte est-elle passée à l'hiver ? Trois idées simples.", [
    (["1. Des produits", "de saison"], "Un : des produits de saison. Courges, poireaux, choux, agrumes."),
    (["2. Un plat", "qui réchauffe"], "Deux : au moins un plat mijoté, et une soupe ou un velouté."),
    (["3. Sans les plats", "d'été"], "Trois : retirez les plats d'été. Une carte courte, et de saison.")],
    sol="Sur Restaurant Site Internet, vous changez votre carte en quelques minutes, et la date de mise à jour s'affiche.")

reel(25, ["Des bons cadeaux", "pour Noël ?"], "Proposez-vous des bons cadeaux pour Noël ? C'est simple à mettre en place.", [
    (["1. Un montant", "ou un menu"], "Un : choisissez la formule. Un montant, ou un menu précis."),
    (["2. Une date", "de validité"], "Deux : indiquez une date de validité, et comment réserver."),
    (["3. Faites-le", "savoir"], "Trois : faites-le savoir. En salle, avec l'addition, sur vos réseaux.")])

reel(26, ["Réveillon :", "annoncez-le tôt"], "Vous ouvrez pour le réveillon ? Dites-le dès maintenant.", [
    (["1. Le menu", "et le prix"], "Un : le menu complet et son prix par personne."),
    (["2. Les horaires"], "Deux : l'heure d'arrivée, et si la soirée se prolonge."),
    (["3. Comment", "réserver"], "Trois : comment réserver, et jusqu'à quelle date.")],
    sol="Sur Restaurant Site Internet, votre menu de réveillon s'affiche sur votre page, avec la réservation de table en ligne si vous le souhaitez.")

reel(27, ["D'où viennent", "vos produits ?"], "Beaucoup de clients aiment savoir d'où vient ce qu'ils mangent. Dites-le sur votre carte.", [
    (["1. Le producteur", "ou la région"], "Un : nommez le producteur ou la région, quand c'est vrai et régulier."),
    (["2. L'origine", "des viandes"], "Deux : pour le bœuf, le porc, le mouton et la volaille, l'origine doit être indiquée."),
    (["3. Restez exact"], "Trois : restez exact. Si le fournisseur change, la carte change aussi.")],
    puces={2: ["Source : DGCCRF"]})

reel(28, ["Plus d'avis,", "honnêtement"], "Vous voulez plus d'avis ? Il suffit souvent de demander, au bon moment.", [
    (["1. Au moment", "de l'addition"], "Un : demandez au moment de l'addition, quand le client vous dit que c'était bon."),
    (["2. Un QR code", "vers votre fiche"], "Deux : facilitez-lui la tâche, avec un QR code qui mène à votre fiche Google."),
    (["3. Jamais", "de contrepartie"], "Trois : pas de cadeau en échange d'un avis. Un avis doit rester libre.")],
    sol="Sur Restaurant Site Internet, vous recevez aussi un QR code et des affichettes à imprimer, qui mènent à votre carte.")

reel(29, ["Cinq chiffres", "à suivre"], "Vous pilotez votre restaurant au ressenti ? Cinq chiffres suffisent, une fois par semaine.", [
    (["Couverts et", "ticket moyen"], "Le nombre de couverts, et le ticket moyen."),
    (["Coût matière", "et pertes"], "Le coût matière, et ce que vous avez jeté."),
    (["Réservations", "non honorées"], "Et les réservations non honorées. Notez ces cinq chiffres chaque lundi, dans un simple tableau.")])

reel(30, ["Votre restaurant", "en ligne : le point"], "Dernier conseil de la série : votre présence en ligne tient en trois points.", [
    (["1. Une fiche Google", "à jour"], "Un : une fiche Google à jour, avec vos horaires et vos photos."),
    (["2. Votre carte", "en ligne"], "Deux : votre carte en ligne, avec les prix et la date de mise à jour."),
    (["3. Des réponses", "aux avis"], "Trois : des réponses à vos avis, et des nouvelles régulières sur vos réseaux.")],
    sol="Pour la carte, Restaurant Site Internet vous donne une page à votre nom, avec un QR code.",
    fin=" Merci de m'avoir suivie pendant ces trente jours !")

assert sorted(R) == list(range(1, 31))
(ICI / "specs").mkdir(exist_ok=True)
for j, r in R.items():
    pair = j % 2 == 0
    assert pair == bool(r["sol"]), j
    scenes = [{"fond": FONDS[0], "pose": POSES[0], "titre": r["accroche"], "voix": r["voix"]}]
    for k, (titre, voix) in enumerate(r["conseils"], 1):
        scenes.append({"fond": FONDS[k], "pose": POSES[k], "titre": titre, "voix": voix})
    if pair:
        scenes.append({"fond": FONDS[4], "pose": "carte", "titre": ["Commentez", "MENU"], "puces": ["restaurant-site-internet.fr"],
                       "voix": r["sol"] + FIN_PAIR + (r["fin"] or "")})
    else:
        scenes.append({"fond": FONDS[4], "pose": "bonjour", "titre": ["Enregistrez", "et partagez"], "voix": FIN_IMPAIR})
    for k, p in r["puces"].items():
        scenes[k]["puces"] = p
    spec = {"etiquette": f"Les conseils de Margot · {j}/30", "scenes": scenes}
    (ICI / "specs" / f"J{j:02d}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("30 scénarios écrits dans", ICI / "specs")
