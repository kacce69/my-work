# Margot — Reels avec son

- `kit/` : de quoi fabriquer un Reel vertical (1080 × 1920) où Margot parle.
- `reels/` : les vidéos publiées sur Instagram (une par jour de campagne, plus les hors-série `HS…`), avec leur image de couverture et une image carrée pour Facebook.
- `PUBLIER.md` : les comptes, les actions de publication, la procédure Canva pour les images, la trame d'une tâche planifiée.
- `STRATEGIE.md` : le but (des restaurateurs inscrits), le constat chiffré, la règle de la première seconde, les moyens de faire voir les vidéos, la preuve, la méthode d'essais, la série « Margot vous répond ».

## Le kit

| Fichier | Rôle |
|---|---|
| `kit/preparer.sh` | Installe ce qu'il faut (`sh kit/preparer.sh` ; ajouter `kokoro` pour la voix de secours). |
| `kit/reel.py` | Fabrique un Reel à partir d'un scénario : `python3 kit/reel.py kit/specs/<code>.json reels/<code>.mp4 --prise`. |
| `kit/specs/<code>.json` | Les scénarios. `PRO1.json` est le modèle des nouveaux Reels (accroche lisible dès la première image, jeu fin, un personnage, une vraie page du site) ; `DEMO.json` fait le tour du moteur ; `J01`…`J30` et `HS0`…`HS8` sont ceux de la campagne (`J02`…`J30` et `HS1`…`HS8` ont été mis à niveau le 15/11/2026 : mêmes mots, nouvelle image). `specs/images/` : les captures utilisées par un scénario, dont quatre vues de la page de démonstration du site (`page-haut`, `page-carte`, `page-plats`, `page-boissons`). |
| `kit/CATALOGUE.md` | Tout ce qu'un scénario peut demander : plans, éléments, jeu de Margot, sons, contrôles. |
| `kit/catalogue/*.jpg` | Les poses, expressions, accessoires, personnages, plats, icônes, écrans de téléphone et décors, en images. |
| `kit/page/*.js`, `kit/reel_page.html` | Le moteur d'animation (une page web dessinée image par image). |
| `kit/sons.py` | Bruitages et musiques de fond, fabriqués par calcul. |
| `kit/caler_voix.py`, `kit/voix/` | Les prises de voix et leur calage sur le scénario. |
| `kit/ecouter.py` | Contrôle final : transcrit le son d'une vidéo terminée et le compare au scénario. |
| `kit/images_site.py` | Les vraies images du site : liste et télécharge les images publiques d'une page, ou photographie la page entière (`--capture`), avec le lecteur de veille qui ne fausse pas les statistiques. |
| `kit/margot_svg.py` | Margot en image fixe (SVG, PNG à fond transparent) pour les posts et les carrousels : `python3 kit/margot_svg.py margot.svg --pose plateau --expression joie --accessoire toque --png 900`. |
| `kit/illustration.py` | Toutes les illustrations du moteur en image fixe à fond transparent (Margot, personnages, plats, icônes, téléphone), pour les posts et les carrousels : `python3 kit/illustration.py chef.png --personnage chef --expression joie`. Ne demande que Python, Playwright et Chrome. |
| `kit/planches_catalogue.py` | Refait les images de `kit/catalogue/` après un ajout au moteur. |
| `posts/<date>-<sujet>/` | Les images d'un post ou d'un carrousel fait à la main, à l'adresse où une tâche planifiée les lit, avec sa légende (`legende.md`) et le fichier qui les fabrique. Modèle : `posts/2026-11-16-nouveaute/fabrication.py`. |
| `kit/mettre_a_niveau.py` | A mis les 37 Reels de la campagne (J02 à J30, HS1 à HS8) au niveau du moteur le 15/11/2026, sans changer un mot dit : ses tables disent quelle illustration montre chaque scène. À relire avant de retoucher l'un de ces scénarios. |
| `kit/trois_temps.py` | A récrit le 19/11/2026 les 32 Reels restants (J05 à J30, HS3 à HS8) « en trois temps », à la demande d'Owen : accroche de moins de 12 mots suivie d'une question dont la réponse n'arrive qu'au dernier conseil, meilleur conseil en dernier, scène « À retenir », appel raccourci. Ses textes sont dans sa table ; chaque Reel a une nouvelle prise de voix. La règle est expliquée dans `STRATEGIE.md` § 3 bis. |
| `kit/generer_specs.py` | A écrit les 30 scénarios d'origine de la campagne « Margot, 30 jours » (plan `margot` partout) ; `mettre_a_niveau.py` les a transformés depuis. |

## Fabriquer un Reel

1. Écrire `kit/specs/<code>.json` (voir `kit/CATALOGUE.md` et `kit/specs/DEMO.json`).
2. Contrôler la mise en page sans voix : `python3 kit/reel.py kit/specs/<code>.json /tmp/<code>/x.mp4 --apercu=4 --muet`, corriger jusqu'à ce qu'il n'y ait plus d'alerte, regarder les planches.
3. Faire la prise de voix (ci-dessous), la caler.
4. Refaire l'aperçu avec `--prise` (les heures des mots sont alors exactes), regarder les planches.
5. Fabriquer : `python3 kit/reel.py kit/specs/<code>.json reels/<code>.mp4 --prise`. Quatre fichiers sortent : `<code>.mp4`, `<code>.jpg` (couverture), `<code>-portrait.jpg` (1080 × 1350, pour Facebook) et `<code>-carre.jpg` (1080 × 1080).
6. Contrôler : `python3 kit/ecouter.py reels/<code>.mp4 kit/specs/<code>.json` (la voix doit rester compréhensible), puis regarder quelques images de la vidéo et sa couverture.

Chaque ajout au moteur laisse les scénarios existants tels quels : vérifié le 15/11/2026 avec les 40 scénarios d'origine de la campagne (597 images d'aperçu comparées point par point avant et après les ajouts, aucune différence).

Les ajouts du 15/11/2026 au soir (jeu fin, personnages, plats, plan `duo`, titre `fixe`, morceau de musique fourni) ne touchent à rien de ce qui existait : les 40 anciens scénarios (597 images d'aperçu) donnent exactement les mêmes images, ainsi que `DEMO` et cinq scénarios d'essai (128 images), rendus par le moteur d'avant et par celui d'après. Le jeu fin ne s'applique qu'aux scénarios qui le demandent (`"jeu": "fin"`).

## La voix

Depuis le 14/11/2026, Margot a la voix « Amélie » (ElevenLabs, modèle `eleven_v3_conversational`, identifiant de voix `sQfOhaIRbFZ7R8bP1x9f`), obtenue par le compte Speko d'Owen. Chaque Reel a sa prise dans `kit/voix/` :

- `kit/voix/<code>.flac` : la prise, faite en une seule fois pour tout le Reel (24 000 Hz, mono) ;
- `kit/voix/<code>.json` : le calage de cette prise sur le scénario (où couper entre deux scènes, heure de chaque mot pour les sous-titres et les animations, contrôle de ce qui a été entendu).

`reel.py` utilise la prise quand ces deux fichiers existent. Sans eux, il fabrique la voix sur place avec Kokoro (voix française `ff_siwis`, gratuite) : c'est la voix de secours. Avec `--prise`, il s'arrête plutôt que de passer à Kokoro.

### Refaire ou ajouter une prise

1. Texte à envoyer : `python3 kit/reel.py kit/specs/<code>.json --texte` (les lignes `voix` du scénario, **séparées par une ligne vide**, dans l'ordre ; les scènes muettes n'y figurent pas ; `dit` remplace `voix` quand la prononciation demande une autre écriture).
2. Synthèse Speko (`audio.synthesize`) : `text` = ce texte ; `intent.language` = `fr-FR` ; `voice` = `sQfOhaIRbFZ7R8bP1x9f` ; `constraints.allowedProviders.tts` = `["elevenlabs:eleven_v3_conversational"]`. Coût constaté : environ 0,04 $ pour 1 000 caractères (0,02 à 0,03 $ par Reel).
3. Convertir le fichier reçu : `ffmpeg -i prise.wav -ar 24000 -ac 1 -c:a flac kit/voix/<code>.flac`.
4. Caler : `python3 kit/caler_voix.py <code>` (transcription locale). La ligne affichée doit donner un ratio proche de 1 et aucune alerte ; un écart entre deux mots qui se prononcent pareil (« faim » / « fin ») est sans importance.
5. Fabriquer : `python3 kit/reel.py kit/specs/<code>.json reels/<code>.mp4 --prise`.

Deux prises du même texte ne sont jamais identiques : on garde le fichier plutôt que de le refaire. Si le texte d'une scène change, il faut une nouvelle prise du Reel entier.

À savoir (constaté le 14/11/2026 sur une cinquantaine de prises) :

- en début de scène, « Un : … », « Deux : … », « Trois : … » sont parfois sautés par la voix. `--texte` les écrit « Un, … », « Deux, … », « Trois, … » (le scénario, lui, garde les deux-points pour les sous-titres) ;
- une prise sur cinq environ a un défaut (mot avalé, syllabe en trop). `caler_voix.py` le signale dans « écarts » : on refait alors la prise, c'est l'affaire de quelques centimes ;
- si le même mot résiste à deux prises (« tombe sur » était entendu « tourne sur »), on reformule la phrase dans le scénario plutôt que d'insister ;
- en cas de doute sur un mot, une troisième écoute indépendante tranche : la transcription Speko (`audio.transcribe`) du lien de téléchargement de la prise ;
- le calage peut laisser passer un petit mot avalé en début de phrase (« Nous la saisissons » entendu « La la saisissons » par le contrôle final et « Ne la saisissons » par Speko) : c'est `ecouter.py`, sur la vidéo terminée, qui le rattrape. On reformule pour que le mot porte l'accent (« Et c'est nous qui la saisissons ») ;
- ne jamais lancer deux transcriptions à la fois, ni une transcription pendant un rendu : la mémoire n'y suffit pas.
