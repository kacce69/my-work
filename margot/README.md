# Margot — Reels avec son

- `kit/` : de quoi fabriquer un Reel vertical (1080 × 1920) où Margot parle.
- `reels/` : les vidéos publiées sur Instagram (une par jour de campagne, plus les hors-série `HS…`), avec leur image de couverture et une image carrée pour Facebook.

## Le kit

| Fichier | Rôle |
|---|---|
| `kit/preparer.sh` | Installe ce qu'il faut (`sh kit/preparer.sh` ; ajouter `kokoro` pour la voix de secours). |
| `kit/reel.py` | Fabrique un Reel à partir d'un scénario : `python3 kit/reel.py kit/specs/<code>.json reels/<code>.mp4 --prise`. |
| `kit/specs/<code>.json` | Les scénarios. `DEMO.json` montre le moteur élargi ; `J01`…`J30` et `HS0`…`HS8` sont ceux de la campagne. |
| `kit/CATALOGUE.md` | Tout ce qu'un scénario peut demander : plans, éléments, jeu de Margot, sons, contrôles. |
| `kit/catalogue/*.jpg` | Les poses, expressions, accessoires, icônes, écrans de téléphone et décors, en images. |
| `kit/page/*.js`, `kit/reel_page.html` | Le moteur d'animation (une page web dessinée image par image). |
| `kit/sons.py` | Bruitages et musiques de fond, fabriqués par calcul. |
| `kit/caler_voix.py`, `kit/voix/` | Les prises de voix et leur calage sur le scénario. |
| `kit/planches_catalogue.py` | Refait les images de `kit/catalogue/` après un ajout au moteur. |
| `kit/generer_specs.py` | A écrit les 30 scénarios de la campagne « Margot, 30 jours ». |

## Fabriquer un Reel

1. Écrire `kit/specs/<code>.json` (voir `kit/CATALOGUE.md` et `kit/specs/DEMO.json`).
2. Contrôler la mise en page sans voix : `python3 kit/reel.py kit/specs/<code>.json /tmp/<code>/x.mp4 --apercu=4 --muet`, corriger jusqu'à ce qu'il n'y ait plus d'alerte, regarder les planches.
3. Faire la prise de voix (ci-dessous), la caler.
4. Refaire l'aperçu avec `--prise` (les heures des mots sont alors exactes), regarder les planches.
5. Fabriquer : `python3 kit/reel.py kit/specs/<code>.json reels/<code>.mp4 --prise`. Trois fichiers sortent : `<code>.mp4`, `<code>.jpg` (couverture) et `<code>-carre.jpg` (Facebook).

Le moteur élargi (15/11/2026) rend les anciens scénarios comme avant : les 40 passent sans alerte, le son est identique et les images aussi (60 images comparées point par point : une seule diffère, d'un niveau sur 255 dans un carré de 8 pixels).

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
- ne jamais lancer deux transcriptions à la fois, ni une transcription pendant un rendu : la mémoire n'y suffit pas.
