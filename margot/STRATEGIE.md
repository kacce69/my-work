# La stratégie de Margot

Mise à jour le 15/11/2026. À relire avant de proposer un plan de contenu, un essai ou un compte rendu. Les chiffres cités sont ceux lus ce jour-là dans Windsor.ai et sur le site ; ils se relisent, ils ne se recopient pas.

## 1. Le but : des restaurateurs inscrits

Les vues ne sont qu'un moyen. Ce qui compte : le nombre de restaurants dont la carte est en ligne, puis les commentaires « MENU » (un restaurateur à recontacter).

- **Mesure** : les pages du répertoire, `curl -sS -A "rcs-veille (monitor)" https://restaurant-site-internet.fr/restaurants`, liens qui commencent par `/restaurant/`. Une page ne compte que si sa carte est publiée : on lit chaque page de la même façon, et celle qui affiche « La carte n'a pas encore été publiée » ne compte pas.
- **Repère** : le 15/11/2026, 7 pages, dont 5 avec une carte publiée (dav-chawarma-cotonou, ftiechoka974-gol, maison-dimelly-lyon, okimono-agen, pizza-rega-agen) et 2 sans carte (le-bistrot-conde-sur-sarthe, pizza-a-marcinelle-marcinelle).
- **Objectif de départ** : 10 cartes publiées le 14/12/2026, puis 5 de plus chaque mois. Owen peut le changer.
- **Le plus court chemin** : un restaurateur qui a créé sa page sans publier sa carte est à une photo du but. Le signaler à Owen à chaque point, pour qu'il le relance.
- **Limite** : une page en ligne n'est pas forcément un restaurateur inscrit de lui-même (Owen peut en créer). Le nombre de comptes créés n'est lisible que par lui : le lui demander à chaque point.
- **Le point de la semaine** : la tâche planifiée « Margot – point de la semaine » (chaque lundi, 8 h 37, heure de Paris) refait ces mesures et écrit à Owen en 180 mots.

## 2. Le constat du 15/11/2026

12 abonnés, 15 publications en deux jours, aucun enregistrement, aucun envoi, aucun commentaire. Portée de 0 à 16 comptes, sauf un Reel vu par 139 comptes.

Ce Reel est le seul à avoir été montré à des inconnus, et il dit l'essentiel : 95 % des vues ont été abandonnées avant 3 secondes, pour 1,9 seconde regardée en moyenne. Les autres Reels (6 à 16 comptes, donc surtout des proches) : 62 à 83 % d'abandons, 4,5 à 9,7 secondes en moyenne.

Deux problèmes distincts, donc : presque personne ne voit les vidéos (§ 4), et ceux qui les voient ne restent pas (§ 3). Avec si peu de vues, ces chiffres indiquent une direction, pas une certitude.

## 3. La première seconde

Un restaurateur décide en deux ou trois secondes. Dans les nouveaux Reels :

- l'accroche est **lisible en entier dès la première image** : en scène 1, titre `"anime": "fixe"`, personnages déjà en place (`"entree": "aucune"`, `"quand": 0`), jamais un fond vide ;
- **quelque chose bouge dans la première demi-seconde** (une bulle, un sursaut, un « non » de la tête) et la voix démarre aussitôt ;
- huit mots au plus, qui disent le problème du restaurateur avec ses mots à lui (« Un site ? Pas le temps. ») plutôt que le nom du produit ;
- `"jeu": "fin"` : Margot joue plus finement, pour le même travail d'écriture.

Le modèle : `kit/specs/PRO1.json`.

**Les Reels déjà programmés suivent cette règle depuis le 16/11/2026.** Le 15/11 au soir, à la demande d'Owen, l'image des 37 Reels à venir (J02 à J30, HS1 à HS8) a été refaite sans toucher aux mots ni à la voix : accroche lisible dès la première image, une illustration par conseil (icône, plat, personnage ou téléphone) calée sur la voix, la vraie page de démonstration du site dans le téléphone avant « Commentez MENU », appel animé en dernière scène. Modèle : `kit/specs/J02.json` ; la transformation est dans `kit/mettre_a_niveau.py`.

Ce n'est pas un essai propre (tout a changé d'un coup), mais c'est une première mesure : comparer la part des vues abandonnées avant 3 secondes des Reels publiés à partir du 16/11 à celle des Reels du 14 et du 15/11 (62 à 95 %), sans rien conclure en dessous de 50 comptes touchés. Le point du jour et le point de la semaine relèvent ce chiffre.

**Premier relevé, le 19/11/2026** (Instagram, lu par Windsor ; seulement les Reels vus par plus de 50 comptes) :

| Reel | Comptes touchés | Abandons avant 3 s | Durée regardée en moyenne | Durée du Reel |
|---|---|---|---|---|
| Avant la refonte, 14/11 (« Votre carte est sur Facebook… ») | 147 | 94,5 % | 2,0 s | — |
| J03, allergènes (17/11) | 136 | 47,1 % | 7,5 s | 27,5 s |
| HS1, le repérage (16/11) | 77 | 48,6 % | 5,1 s | 26,3 s |
| J04, coût matière (18/11) | 90 | 64,4 % | 4,2 s | 31,2 s |

Le début retient mieux. Le point faible s'est déplacé : ceux qui passent les 3 secondes regardent ensuite 6 à 14 secondes sur une trentaine (calcul fait à partir des deux chiffres d'Instagram), donc partent en moyenne pendant le premier ou le deuxième conseil. Les deux accroches qui retiennent le mieux ouvrent sur une scène ou une phrase inattendue ; la moins bonne annonce « le calcul tient en trois étapes ». Trois Reels : une tendance, pas une preuve.

## 3 bis. L'écriture en trois temps (depuis le 19/11/2026)

Le 19/11/2026, Owen a demandé que les Reels à venir suivent la règle « accroche, valeur, bénéfice » d'une vidéo de conseils qu'il a vue : les trois endroits où un Reel perd son public sont le début, le milieu et la fin. Les 32 Reels restants (J05 à J30, HS3 à HS8) ont été récrits ainsi, avec une nouvelle prise de voix ; les faits et les conseils n'ont pas changé.

1. **L'accroche** : une première phrase de moins de 12 mots (8 au plus à l'écran), une scène vécue ou une phrase inattendue plutôt qu'une annonce de plan. Elle est suivie d'une **question ouverte** ou d'une annonce dont la réponse n'arrive qu'au dernier conseil (« Faut-il tout régler par écrit ? Réponse à la troisième étape. »).
2. **La valeur** : trois conseils, le plus utile en dernier ; c'est lui qui répond à la question de l'accroche, et il le dit (« Trois, au contraire : … »).
3. **Le bénéfice** : une scène « À retenir » (les trois points cochés à l'écran, une phrase dite), puis l'appel, raccourci.

**L'annonce doit être vraie.** Elle porte sur ce que la vidéo donne vraiment : une question à laquelle le dernier conseil répond, ou une propriété vérifiable de ce conseil (« le dernier se fait quand il n'est pas là »). Jamais « presque personne ne le fait », « le plus efficace » ni aucune promesse qu'on ne peut pas vérifier.

La transformation est dans `kit/trois_temps.py` (les textes y sont, Reel par Reel) ; le modèle est `kit/specs/J05.json`. Les Reels durent maintenant 27 à 39 secondes (33 en moyenne), contre 22 à 34 (27 en moyenne) : 6 secondes de plus en moyenne, c'est le prix de la question ouverte et de la scène « À retenir ».

**Ce qu'on mesure**, toujours sur les Reels vus par plus de 50 comptes : la durée regardée en moyenne (elle doit monter au-dessus des 4 à 8 secondes du tableau ci-dessus) et la part d'abandons avant 3 secondes (elle ne doit pas remonter). La courbe complète, seconde par seconde, ne se lit que dans l'application Instagram (statistiques du Reel) : c'est elle qui dit si la fin retient. Là encore, ce n'est pas un essai propre : les sujets changent chaque jour. On juge sur plusieurs Reels, pas sur un seul.

## 4. Faire voir les vidéos aux restaurateurs

Par ordre de coût. Claude prépare ; il ne contacte personne et ne dépense rien.

1. **La prospection d'Owen, avec une vidéo.** Il écrit déjà aux restaurants par Facebook et par e-mail : le message gagne à tenir en trois phrases et à porter le lien d'un Reel qui répond à l'objection du restaurateur. Sur Instagram, une première prise de contact avec quelqu'un qui ne vous suit pas ne passe que du texte : la vidéo part après sa réponse. Peu de messages, écrits un par un : des envois en série identiques font restreindre un compte.
2. **Les groupes de restaurateurs** (Facebook). Lire le règlement de chaque groupe ; y apporter un conseil complet, utile sans le site ; ne mettre un lien que si le règlement le permet, sinon répondre à ceux qui demandent.
3. **La mise en avant payante** du Reel qui retient le mieux (le moins d'abandons avant 3 secondes). C'est une dépense : Owen la décide, la règle et la paie lui-même depuis Instagram. Petit budget, une seule audience, une semaine, puis on lit les abandons avant 3 secondes, les visites du profil et les commentaires « MENU ». Conditions d'après le guide cité plus bas : compte professionnel, Reel de 60 secondes au plus, sans musique d'un tiers, non partagé sur Facebook. Proposition de départ remise à Owen le 15/11/2026 : `PRO1`, objectif « visites du profil », France, 25 à 60 ans, centres d'intérêt de la restauration, 5 € par jour pendant 6 jours.

Les « Reels d'essai » d'Instagram (montrés d'abord aux seuls non-abonnés) demandent un compte public, éligible aux recommandations, d'au moins 200 abonnés pour un compte professionnel, d'après l'aide de Metricool (un autre outil, Publer, écrit encore 1 000) : pas pour ce compte aujourd'hui, mais c'est un palier à viser. Un Reel d'essai ne peut pas être mis en avant.

## 5. La preuve

Rien ne convainc un restaurateur comme un autre restaurateur. Les candidats sont ceux dont la page est en ligne.

- Avant de montrer une page, un nom, une photo ou une phrase d'un restaurateur : son accord écrit, demandé par Owen, gardé avec le scénario.
- Jamais de témoignage inventé, de chiffre arrangé, ni de photo où l'on reconnaît une personne.
- L'accord obtenu : un Reel « Démonstration » avec sa vraie page (`images_site.py /restaurant/<adresse> --capture`), son nom à l'écran, et une phrase de lui citée telle quelle.
- En attendant : les pages de démonstration du site, toujours présentées comme des exemples.

## 6. Après les 30 jours : moins de volume, plus d'essais

Trois publications par jour ne servent à rien si la première seconde ne retient pas. À partir du 15/12/2026, proposition : cinq publications par semaine (trois Reels, deux carrousels), dont chaque semaine un essai.

**Un essai d'accroche.** Un seul sujet, un seul corps de vidéo, deux scènes 1 différentes (A et B).

- Soit en publication normale : A et B le même jour de la semaine, à la même heure, à une semaine d'écart ; l'ordre s'inverse à l'essai suivant.
- Soit, si Owen le décide, en mise en avant : A et B avec la même audience, le même budget, la même durée. C'est la seule comparaison propre tant que le compte est petit.
- Ce qu'on lit (Windsor, connecteur `instagram`) : `media_reel_skip_rate` (part des vues abandonnées avant 3 secondes : le juge de l'accroche), `media_reel_avg_watch_time`, `media_reach`, puis `media_saved` et `media_shares`.
- La règle, écrite avant de publier : en dessous de 50 comptes touchés de chaque côté, pas de conclusion. Au-dessus, l'accroche qui a le moins d'abandons gagne si l'écart dépasse 10 points ; sinon, égalité, et on essaie autre chose.
- On reprend la forme qui gagne, pas le sujet. Un essai par semaine, une seule chose changée à la fois.

**Dans l'ordre** : le type d'accroche (l'objection du restaurateur, une question, un chiffre sourcé) ; la première image (Margot et un personnage, Margot seule, le téléphone) ; la durée (20 ou 35 secondes) ; l'appel (commenter MENU, enregistrer).

**Le journal des essais** (à compléter ici) :

| Date | Sujet | Accroche A | Accroche B | Comptes touchés A / B | Abandons avant 3 s A / B | Décision |
|---|---|---|---|---|---|---|
| | | | | | | |

## 7. La série « Margot vous répond »

Une objection de restaurateur par épisode, la réponse montrée plutôt que dite. Chaque fait se relit sur le site le jour de la fabrication.

| N° | L'objection | La réponse à montrer | État |
|---|---|---|---|
| 1 | « Un site ? Pas le temps. » | Une photo de la carte suffit : elle est saisie pour lui. | `PRO1`, fait le 15/11/2026 |
| 2 | « Ma carte est déjà sur Facebook. » | Tous les clients n'y ont pas de compte ; un lien s'ouvre partout. | à faire |
| 3 | « Ma carte change tout le temps. » | Un prix se change en quelques secondes ; l'ardoise du jour s'efface le soir. | à faire |
| 4 | « Gratuit ? Il y a un piège. » | Ce que dit la page des tarifs, mot pour mot. | à faire |
| 5 | « Je ne suis pas doué avec les ordinateurs. » | Tout se fait depuis un téléphone ; ou l'on est rappelé. | à faire |

## Sources des règles citées (lues le 15/11/2026)

- Première prise de contact en message privé limitée à une invitation en texte (article du 4 août 2023) : https://www.blogdumoderateur.com/instagram-nouvelle-option-limiter-spams-dm/
- Reels d'essai, conditions : https://help.metricool.com/fr/how-to-publish-instagram-trial-reels-in-metricool-q27tj (200 abonnés) et https://publer.com/help/fr/article/comment-programmer-des-reels-dessai-sur-instagram-p8brtq/ (1 000 abonnés)
- Mettre un Reel en avant (objectif, audience, budget, durée, conditions) : https://blog.hootsuite.com/boost-instagram-reels/
- Le plan d'action remis à Owen (messages de prospection, publication pour un groupe, réglages de mise en avant, demande d'accord) : https://claude.ai/artifact/JN9YdASGuqfoP3M9BSCKmY
- Offre et fonctions du site : https://restaurant-site-internet.fr/tarifs et https://restaurant-site-internet.fr/restaurateurs
