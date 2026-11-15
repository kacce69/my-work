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

## 4. Faire voir les vidéos aux restaurateurs

Par ordre de coût. Claude prépare ; il ne contacte personne et ne dépense rien.

1. **La prospection d'Owen, avec une vidéo.** Il écrit déjà aux restaurants par Facebook et par e-mail : le message gagne à tenir en trois phrases et à porter le lien d'un Reel qui répond à l'objection du restaurateur. Sur Instagram, une première prise de contact avec quelqu'un qui ne vous suit pas ne passe que du texte : la vidéo part après sa réponse. Peu de messages, écrits un par un : des envois en série identiques font restreindre un compte.
2. **Les groupes de restaurateurs** (Facebook). Lire le règlement de chaque groupe ; y apporter un conseil complet, utile sans le site ; ne mettre un lien que si le règlement le permet, sinon répondre à ceux qui demandent.
3. **La mise en avant payante** du Reel qui retient le mieux (le moins d'abandons avant 3 secondes). C'est une dépense : Owen la décide, la règle et la paie lui-même depuis Instagram. Petit budget, une seule audience, une semaine, puis on lit le coût d'une visite de profil et les commentaires « MENU ».

Les « Reels d'essai » d'Instagram (montrés d'abord aux seuls non-abonnés) demandent 1 000 abonnés d'après les outils de publication qui les proposent : pas pour ce compte aujourd'hui.

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

- Première prise de contact en message privé limitée au texte : https://www.blogdumoderateur.com/instagram-nouvelle-option-limiter-spams-dm/
- Reels d'essai, seuil de 1 000 abonnés : https://help.metricool.com/fr/how-to-publish-instagram-trial-reels-in-metricool-q27tj et https://publer.com/help/fr/article/comment-programmer-des-reels-dessai-sur-instagram-p8brtq/
- Mettre un Reel en avant (objectif, audience, budget, durée) : https://blog.hootsuite.com/boost-instagram-reels/
- Offre et fonctions du site : https://restaurant-site-internet.fr/tarifs et https://restaurant-site-internet.fr/restaurateurs
