# Catalogue du moteur de Reels de Margot

Tout ce qu'un scénario (`specs/<code>.json`) peut demander à `reel.py`. Les images du dossier `catalogue/` montrent les poses, les expressions, les accessoires, les icônes, les écrans de téléphone et les décors. `specs/DEMO.json` est un exemple complet qui utilise la plupart de ces possibilités.

L'image fait 1080 × 1920. Les positions sont en pixels depuis le coin haut gauche. Les anciens scénarios (J01 à J30, HS0 à HS8) restent valables tels quels : ils utilisent le plan `margot`.

## 1. Le Reel entier

```json
{ "etiquette": "Les conseils de Margot",
  "soustitres": "karaoke", "progression": true, "musique": "entrain",
  "scenes": [ … ] }
```

| Clé | Valeurs | Effet |
|---|---|---|
| `etiquette` | texte | La pastille en haut de chaque scène (nom de la série, « 3/8 »…). |
| `soustitres` | `"bloc"` (défaut), `"karaoke"`, `"aucun"` | `karaoke` : le mot en cours de prononciation est surligné. |
| `progression` | `true` | Barre de progression en haut, un segment par scène. |
| `musique` | `"entrain"`, `"douce"`, `"suspense"`, `"fete"` ou `{"nom": "douce", "volume": -3}` | Musique de fond ; elle s'efface quand Margot parle. `volume` en décibels. Sans cette clé : pas de musique. |
| `bruitages` | `false` | Coupe les bruitages automatiques (ceux de `sons` restent). |
| `couverture` | `{"scene": 1, "instant": 3.2}` | Image de couverture. Par défaut : la fin de la première scène. |

## 2. Une scène

| Clé | Valeurs | Effet |
|---|---|---|
| `plan` | voir § 3 | Mise en page. Défaut : `margot`. |
| `fond` | `creme`, `prune`, `or`, `nuit` | Couleur de fond ; les couleurs des textes suivent. |
| `decor` | `ville`, `salle`, `rue`, `cuisine`, `nappe`, `points`, `rayons` | Silhouette ou motif discret derrière la scène. `cercles: false` retire les deux grands disques. |
| `voix` | texte | Ce que dit Margot. Sert aussi aux sous-titres. Sans `voix`, la scène est muette et dure `duree` secondes (2 par défaut). |
| `dit` | texte | Texte envoyé à la synthèse quand la prononciation demande une autre écriture ; les sous-titres gardent `voix`. |
| `avant`, `apres`, `duree_min` | secondes | Silence avant et après la voix (0,45 et 0,35 par défaut) ; durée minimale de la scène. |
| `transition` | `cercle` (défaut), `fondu`, `coupe`, `zoom`, `rideau`, `volet`, `glisse-gauche`, `glisse-droite`, `glisse-haut`, `glisse-bas`, `pousse-gauche`, `pousse-droite`, `pousse-haut` | Arrivée de la scène. `son_transition` : un bruitage, ou `false`. |
| `camera` | `avance`, `recule`, `derive` | Mouvement lent de toute la scène. `secousses: ["@mot", 2.4]` : petits tremblements. |
| `titre` | liste de lignes | Titre du plan. `*mot*` met un mot en valeur. `anime` : `lignes` (défaut), `mots`, `voix` (chaque mot arrive quand il est dit), `machine` (se tape lettre à lettre). `taille_titre` en pixels. |
| `pose`, `expression`, `accessoire`, `regard`, `gestes`, `miroir`, `panneau`, `entree` | voir § 4 | Jeu de Margot dans le plan. `margot: {"x": …, "y": …, "taille": …}` la déplace, `margot: false` la retire. |
| `elements` | liste, voir § 5 | Éléments ajoutés par-dessus le plan. |
| `sons` | `[{"quand": "@prix", "son": "caisse", "volume": 0.8}]` | Bruitages placés à la main. |
| `soustitres`, `bruitages`, `etiquette` | `false` | Retire le bandeau de sous-titres, les bruitages automatiques ou la pastille pour cette scène. |

## 3. Les plans

| Plan | Ce qu'on voit | Clés propres au plan |
|---|---|---|
| `margot` | Titre, pastilles, Margot en grand au centre (le plan d'origine). | `titre`, `puces` |
| `accroche` | Très gros titre dont les mots arrivent avec la voix, Margot dessous. | `titre` |
| `mots` | Le texte dit s'affiche en très grand, mot après mot (pas de bandeau de sous-titres). | — |
| `telephone` | Un téléphone et son écran, Margot le montre du doigt. | `titre`, `telephone: {"ecran": {…}, "touches": [{"quand": "@prix", "x": 0.8, "y": 0.5}], "incline": -4}` (§ 6) |
| `chiffre` | Un grand nombre qui compte, sa légende, sa source. | `chiffre: {"valeur": 14, "suffixe": " allergènes", "legende": "…", "source": "economie.gouv.fr"}` ; aussi `prefixe`, `depuis`, `decimales`, `duree`, `jauge: true` et `sur`. Sans `source`, mettre `"exemple": true` (le mot « Exemple » s'affiche). |
| `barres` | Barres horizontales qui grandissent. | `titre`, `barres: {"donnees": [{"nom": "Lundi", "valeur": 18, "accent": true}], "unite": " couverts", "source": "…"}` (ou `"exemple": true`) |
| `liste` | Titre et liste qui se coche point par point (5 points au plus). | `titre`, `liste: ["…", {"texte": "…", "quand": "@horaires", "puce": "croix"}]` ou `{"items": […], "puce": "numero"}`. Puces : `coche`, `croix`, `numero`, `point` ou une icône. |
| `compare` | Deux cartons côte à côte : sans / avec, avant / après. | `titre`, `compare: {"gauche": {"entete": "Sans", "lignes": ["…"]}, "droite": {"entete": "Avec", "lignes": ["…"], "quand": "@avec"}}` |
| `question` | Une question, 2 à 4 réponses, une barre de temps, puis la bonne réponse s'allume. | `titre`, `question: {"options": ["…", "…"], "bonne": 2, "revele": "@réponse"}` |
| `dialogue` | Bulles façon messagerie (3 au plus). | `dialogue: [{"de": "client", "texte": "…"}, {"de": "margot", "texte": "…", "quand": "@oui"}]` ; `de` : `client`, `chef`, `margot` |
| `mythe` | Une idée reçue entre guillemets, puis un tampon qui tombe dessus. | `mythe: {"texte": "…", "verdict": "FAUX", "quand": "@faux"}` ; `verdict` libre (`VRAI`, `PAS SÛR`…) |
| `image` | Une image dans un cadre, Margot dans le coin. | `titre`, `image: {"src": "photo.jpg", "legende": "…", "cadre": "polaroid"}` (chemin écrit par rapport au scénario) |
| `fin` | Titre, appel à l'action animé, pastille d'adresse. | `titre`, `puces`, `appel` : `"commenter"`, `"abonner"`, `"enregistrer"`, `"envoyer"`, `"lien"` ou `{"genre": "commenter", "mot": "MENU", "mot_quand": "@menu"}` |
| `libre` | Rien d'imposé : seulement `elements`. | `etiquette: true` pour garder la pastille |

## 4. Margot

Dans un plan, ces clés se mettent sur la scène. Dans `elements`, elles se mettent sur un élément `{"type": "margot", …}` (on peut en mettre plusieurs).

- **`pose`** (bras droit) : `bonjour`, `pouce`, `carte`, `repos`, `index`, `pointe`, `hanche`, `leve`, `hausse`, `reflechit`, `stop`, `telephone`, `loupe`, `plateau`, `panneau` (avec `"panneau": "-10 %"`, deux lignes séparées par `\n`). Les deux bras : `fete`, `hausse`, `hanches`. Bras au choix : `{"droite": "hanche", "gauche": "pointe"}` (bras gauche : `repos`, `leve`, `hausse`, `hanche`, `pointe`).
- **`expression`** : `neutre`, `joie`, `rire`, `surprise`, `doute`, `triste`, `colere`, `malice`, `amour`.
- **`accessoire`** (un nom ou une liste) : `masque`, `lunettes`, `casque`, `toque`, `couronne`, `bonnet` (Noël), `fete` (chapeau pointu).
- **`regard`** : `face`, `gauche`, `droite`, `haut`, `bas` ou `{"x": 700, "y": 600}` (un point de l'image).
- **`entree`** : `pop` (défaut), `de-gauche`, `de-droite`, `de-bas`, `tombe`, `fondu`, `aucune` (elle est déjà là : utile quand elle reste à la même place d'une scène à l'autre).
- **`x`, `y`, `taille`** : centre de sa boîte (540 et 1070 par défaut ; son corps est un peu à gauche du centre pour laisser la place au bras droit) et taille (1 = 650 pixels de large). `miroir: true` la retourne. `disque: false` retire le disque crème posé derrière elle sur les fonds foncés.
- **`quand`, `jusqu`** : moment où elle arrive et où elle part. `parle: false` : sa bouche ne suit pas la voix.
- **`gestes`** : ce qu'elle fait pendant la scène, chacun avec son `quand` :

```json
"gestes": [
  {"quand": "@carte", "geste": "saut"},
  {"quand": "@carte", "expression": "joie"},
  {"quand": "@regardez", "pose": "pointe"},
  {"quand": 2.0, "regard": "droite"},
  {"quand": "@venez", "deplace": {"x": 760, "y": 1150, "taille": 0.7, "duree": 0.9}}
]
```

Gestes : `saut`, `hoche` (oui), `non`, `sursaut`, `penche` (`"cote": "gauche"`), `tourne`, `tremble`, `rebond`, `clin` (clin d'œil), `danse`. Options : `duree`, `force`. Pendant un `deplace`, elle marche.

**Margot en image fixe** (posts, carrousels, stories, documents) : `python3 margot_svg.py margot.svg --pose plateau --expression joie --accessoire toque,lunettes --png 900` écrit un SVG et un PNG à fond transparent, avec les mêmes poses, expressions et accessoires. Autres options : `--gauche`, `--regard`, `--panneau`, `--bouche`, `--miroir`.

## 5. Les éléments

Clés communes : `x`, `y` (centre de l'élément) ou `haut`, `bas`, `gauche`, `droite` (le bord correspondant) ; `l` (largeur) ; `rot` (degrés) ; `z` (ordre d'empilement) ; `quand` ; `jusqu` (moment où il disparaît) ; `entree` : `pop`, `monte`, `descend`, `de-gauche`, `de-droite`, `de-bas`, `fondu`, `zoom`, `tombe`, `tourne`, `aucune` (ou `{"type": "pop", "duree": 0.6}`) ; `boucle` : `flotte`, `pulse`, `balance`, `tourne`, `tremble` ; `son` (un bruitage, ou `false`).

Couleurs : `creme`, `prune`, `or`, `nuit`, `fonce`, `vert`, `rouge`, `rose`, `blanc`, ou une couleur CSS. Dans les textes, `*mot*` met un mot en valeur.

| Type | Clés | Rôle |
|---|---|---|
| `titre` | `lignes`, `taille` (104), `anime`, `quand`, `jusqu`, `couleur`, `aligne` | Titre en Fraunces ; rétrécit seul si une ligne est trop large. |
| `texte` | `texte` (une ligne ou une liste), `taille` (48), `style` : `simple`, `pastille`, `carton`, `doux` ; `couleur`, `fond`, `aligne`, `leger` | Paragraphe, pastille ou encadré. |
| `puces` | `items`, `haut`, `quand` | Rangée de pastilles. |
| `liste` | `items`, `puce`, `taille` (56) | Liste à puces animée. |
| `chiffre`, `barres` | voir § 3 | Nombre qui compte, barres. |
| `icone` | `nom` (§ 7), `taille` (160), `couleur`, `fond` (disque de couleur derrière), `ep` | Une icône. |
| `forme` | `forme` : `fleche` (`de`, `a`, `courbe`), `cercle` (`x`, `y`, `rx`, `ry`), `soulignement` (`de`, `a`), `croix` (`x`, `y`, `r`), `trait` (`de`, `a`) ; `couleur`, `ep`, `quand`, `duree`, `jusqu` | Trait qui se dessine comme à la main, pour désigner ou entourer. |
| `image` | `src`, `l` (800), `h` (600), `cadre` : `arrondi`, `polaroid`, `aucun` ; `legende`, `zoom` (`[1, 1.08]`), `ajuste`, `position` | Photo ou capture d'écran, avec un zoom lent. |
| `bulle` | `texte`, `l` (640 au plus), `taille` (46), `queue` : `bas-gauche`, `bas-droite`, `haut-gauche`, `haut-droite`, `gauche`, `droite`, `aucune` ; `machine: true` (le texte se tape) | Bulle de parole. |
| `avatar` | `role` : `client`, `chef` ; `taille` (150) | Petit personnage rond (un client, un cuisinier). |
| `tampon` | `texte`, `taille` (120), `couleur`, `angle`, `quand` | Tampon qui tombe, avec secousse et bruit. |
| `carton` | `entete`, `lignes`, `icone`, `ton` : `plus`, `moins`, `neutre` | Carte blanche avec en-tête et lignes. |
| `citation` | `texte`, `taille` (64), `auteur`, `tampon: {"texte": "FAUX", "quand": …}` | Phrase entre guillemets. |
| `choix` | `options`, `bonne`, `quand`, `revele` | Réponses d'une question. |
| `appel` | `genre`, `mot`, `mot_quand`, `texte`, `delai` | Appel à l'action animé. |
| `chat` | `repliques`, `taille` (47) | Dialogue en bulles. |
| `particules` | `genre` : `confettis`, `neige`, `coeurs`, `bulles`, `etincelles` ; `nombre`, `duree`, `opacite`, `devant` | Les confettis passent devant, les autres derrière le contenu. |
| `grosmots` | `taille` (124), `haut` | Gros sous-titres mot à mot. |
| `telephone` | § 6 | Maquette de téléphone. |
| `margot` | § 4 | Margot. |
| `etiquette` | `texte` | La pastille du haut. |
| `libre` | `html`, `css`, `plein: true` (toute l'image), `cles`, `js` | Tout ce qu'un navigateur sait dessiner. |

**Élément libre.** `cles` anime l'élément entre des étapes : `[{"t": 0, "opacity": 0, "y": 60}, {"t": 0.4, "opacity": 1, "y": 0}, {"t": 3, "rot": 360, "scale": 1.2}]` (`t` en secondes depuis `quand`). `js` est le corps d'une fonction appelée à chaque image avec `u` (secondes depuis le début de la scène), `el` (l'élément) et `o` (outils : `o.clamp`, `o.sortie`, `o.rebond`, `o.douce`, `o.mel`, `o.heure("@mot")`, `o.parle` = ouverture de la bouche, `o.mots`, `o.ico(nom, taille, couleur)`, `o.C` = couleurs). Exemple : `"js": "el.style.letterSpacing = (2 + 2 * Math.sin(u * 4)) + 'px';"`. L'animation dépend uniquement de `u` : pas de minuterie, pas de hasard, sinon deux images voisines ne se suivent plus.

## 6. Écrans du téléphone

`"telephone": {"ecran": {"type": "carte", …}}`. Chaque écran a des textes par défaut, tous remplaçables. Un restaurant, un plat ou un prix inventé garde le mot « Exemple » à l'écran.

| `type` | Clés | Ce qu'il montre |
|---|---|---|
| `carte` | `nom`, `sous`, `info`, `pied`, `rubriques: [{"titre": "Plats", "plats": [["Bavette", "18 €", "description"]]}]`, `defile_de`, `defile_a`, `defile: false` | Une carte de restaurant qui défile. |
| `recherche` | `requete`, `quand` (début de la frappe), `resultats: [{"titre", "sous", "badge", "ok"}]` | Une recherche qui se tape, puis ses résultats. |
| `fiche` | `nom`, `sous`, `horaires`, `adresse`, `note`, `avis`, `boutons`, `accent` (bouton mis en avant), `manque` (bouton absent), `message`, `quand` | La fiche d'un restaurant, avec ou sans carte. |
| `messages` | `titre`, `messages: [{"de": "client" ou "moi", "texte", "quand"}]` | Une conversation. |
| `vide` | `titre`, `sous` | « Aucune carte trouvée ». |
| `reservation` | `titre`, `champs: [["Date", "Samedi"]]`, `bouton`, `fait`, `quand` (moment de l'appui) | Une réservation qui se remplit puis se confirme. |
| `notification` | `heure`, `jour`, `app`, `titre`, `texte`, `quand` | Écran verrouillé et notification. |
| `ardoise` | `titre`, `lignes: [["Blanquette", "15 €"]]`, `pied` | L'ardoise du jour. |
| `qr` | `titre`, `sous` | Un QR code d'illustration (il ne mène nulle part). |
| `image` | `src`, `defile_de`, `defile_a` | Une vraie capture d'écran, qui défile si elle est haute (voir « Les vraies images du site » ci-dessous). |

**Les vraies images du site.** `python3 images_site.py /exemples` liste les images publiques d'une page de restaurant-site-internet.fr ; `--prendre 1,3 --vers dossier` (ou `--prendre tout`) les télécharge ; `--capture page.png` photographie la page entière telle qu'un téléphone l'affiche (`--largeur 1200` pour un écran d'ordinateur, `--hauteur 1900` pour n'en garder que le haut : une capture plus courte défile plus lentement). Tout passe par le lecteur de veille du site, qui ne compte pas dans ses statistiques ; la page est reconstituée ici, sans ses scripts, sans jamais être visitée par un navigateur. Dans un scénario : `"telephone": {"ecran": {"type": "image", "src": "page.png", "defile_de": "@carte"}}`, ou le plan `image`.

Les pages de démonstration (`/exemples`, `/exemple/…`) sont celles du site : ce sont elles qu'on montre de préférence. La page d'un vrai restaurant et les photos qu'il y a déposées (dossier `/uploads/`) lui appartiennent : pas de publication sans son accord, et jamais de photo où l'on reconnaît une personne.

## 7. Icônes

`coche`, `croix`, `plus`, `fleche`, `etoile`, `coeur`, `eclair`, `horloge`, `loupe`, `telephone`, `epingle`, `calendrier`, `euro`, `assiette`, `couverts`, `verre`, `toque`, `cloche`, `ardoise`, `carte`, `boutique`, `maison`, `photo`, `qr`, `lien`, `avion`, `signet`, `commentaire`, `message`, `personne`, `pouce`, `oeil`, `ampoule`, `billet`, `graphique`, `cible`, `cadenas`, `cadeau`, `feuille`, `flocon`, `interdit`, `question`, `exclamation`.

## 8. Quand : caler sur la voix

`quand` (et `jusqu`, `revele`, `mot_quand`…) accepte :

- un nombre : secondes depuis le début de la scène ;
- `"voix"`, `"fin-voix"` : le début et la fin de la voix ;
- `"@carte"` ou `"@carte en ligne"` : l'instant où ce mot est dit dans la scène ;
- `{"mot": "carte", "n": 2, "decale": -0.1}` : la 2ᵉ fois que le mot est dit, un dixième de seconde plus tôt ; `{"mot": 5}` : le 5ᵉ mot ; `"fin": true` : la fin du mot ;
- `{"part": 0.5}` : la moitié de la voix ; `{"avant_fin": 0.6}` : 0,6 s avant la fin de la scène.

Avec une prise enregistrée et calée, ces heures sont exactes. Avec la voix de secours (Kokoro), elles sont estimées. `--apercu` affiche l'heure trouvée pour chaque mot ; un mot absent de la voix déclenche une alerte.

## 9. Sons

- **Bruitages** : `pop`, `whoosh`, `glisse`, `ding`, `cloche`, `tic`, `clic`, `bulle`, `impact`, `tampon`, `compte`, `succes`, `tada`, `caisse`, `erreur`. Beaucoup d'éléments ont le leur (une liste fait `tic`, un chiffre `compte` puis `ding`, un tampon `tampon`, des confettis `tada`, une transition `pop`, `whoosh` ou `impact`). `"son": false` sur un élément le coupe.
- **Musiques** : `entrain` (enjouée), `douce` (calme), `suspense` (à pas de loup), `fete` (festive).
- Tous sont fabriqués par calcul dans `sons.py` : aucun fichier, aucun droit à payer. `python3 sons.py` écrit un échantillon de chacun dans `echantillons/`.

## 10. Contrôler avant de fabriquer

`python3 reel.py specs/<code>.json sortie.mp4 --apercu=4` écrit quatre images par scène et des planches (`apercu/planche-1.jpg`…). Il affiche aussi les durées, l'heure des mots utilisés par `quand`, et des alertes :

- texte trop long, sous-titre sur trois lignes, pastilles sur deux lignes ;
- élément qui sort de la zone utile (à gauche de 16, à droite de 1064, au-dessus de 170 : boutons d'Instagram ; plus bas que 1446 quand il y a des sous-titres, 1640 sinon) ;
- nom inconnu (plan, pose, geste, expression, accessoire, icône, écran, transition, bruitage), clé inconnue dans une scène ou au niveau du Reel (faute de frappe), mot absent de la voix, chiffre sans source, image introuvable.

`"note": "…"` est accepté partout (Reel ou scène) pour laisser une remarque : le moteur l'ignore.

On ne fabrique la vidéo que lorsqu'il n'y a plus d'alerte et que les planches ont été regardées.

## 11. Ajouter une possibilité

| Pour ajouter… | Fichier | Où |
|---|---|---|
| une pose, une expression, un accessoire, un geste | `page/02_margot.js` | `POSES`, `BRASG`, `EXPR`, `CHAPEAUX`, la boucle des gestes (et `GD` pour sa durée) |
| une icône, une entrée, une boucle | `page/01_outils.js` | `ICONES`, `ENTREES`, `BOUCLES` |
| un type d'élément | `page/03_elements.js` | `FAB.<type> = (def, x) => ({el, type, anim(u, t, ouv)})` |
| un écran de téléphone | `page/04_telephone.js` | `ECRANS` |
| un décor, un plan | `page/05_plans.js` | `DECORS`, `PLANS` |
| une transition, un mouvement de caméra | `page/06_scene.js` | `TRANSITIONS` et `render` |
| un bruitage, une musique | `sons.py` | `EFFETS`, `MUSIQUES` |

Après un changement : `python3 planches_catalogue.py` refait les images de `catalogue/` ; on les regarde, on refait l'aperçu de `specs/DEMO.json` et d'un ancien scénario (`specs/J08.json`), et on complète ce catalogue.
