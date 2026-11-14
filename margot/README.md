# Margot — Reels avec son

- `kit/` : de quoi fabriquer un Reel vertical (1080 × 1920) où Margot parle : `sh kit/preparer.sh`, puis `python3 kit/reel.py kit/specs/J01.json sortie.mp4`.
- `reels/` : les vidéos publiées sur Instagram (une par jour de campagne, plus les hors-série `HS…`), avec leur image de couverture et une image carrée pour Facebook.

## La voix

Depuis le 14/11/2026, Margot a la voix « Amélie » (ElevenLabs, modèle `eleven_v3_conversational`, identifiant de voix `sQfOhaIRbFZ7R8bP1x9f`), obtenue par le compte Speko d'Owen. Chaque Reel a sa prise dans `kit/voix/` :

- `kit/voix/<code>.flac` : la prise, faite en une seule fois pour tout le Reel (24 000 Hz, mono) ;
- `kit/voix/<code>.json` : le calage de cette prise sur le scénario (où couper entre deux scènes, heure de chaque mot pour les sous-titres, contrôle de ce qui a été entendu).

`reel.py` utilise la prise quand ces deux fichiers existent. Sans eux, il fabrique la voix sur place avec Kokoro (voix française `ff_siwis`, gratuite) : c'est la voix de secours. Avec `--prise`, il s'arrête plutôt que de passer à Kokoro.

### Refaire ou ajouter une prise

1. Synthèse Speko (`audio.synthesize`) : le texte = les lignes `voix` du scénario, **séparées par une ligne vide**, dans l'ordre ; `intent.language` = `fr-FR` ; `voice` = `sQfOhaIRbFZ7R8bP1x9f` ; `constraints.allowedProviders.tts` = `["elevenlabs:eleven_v3_conversational"]`. Coût constaté le 14/11/2026 : environ 0,04 $ pour 1 000 caractères (0,02 $ par Reel).
2. Convertir le fichier reçu : `ffmpeg -i prise.wav -ar 24000 -ac 1 -c:a flac kit/voix/<code>.flac`.
3. Caler : `python3 kit/caler_voix.py <code>` (transcription locale, `pip install faster-whisper`). La ligne affichée doit donner un ratio proche de 1 et aucune alerte ; un écart entre deux mots qui se prononcent pareil (« faim » / « fin ») est sans importance.
4. Fabriquer : `python3 kit/reel.py kit/specs/<code>.json reels/<code>.mp4 --prise`.

Deux prises du même texte ne sont jamais identiques : on garde le fichier plutôt que de le refaire. Si le texte d'une scène change, il faut une nouvelle prise du Reel entier.

À savoir (constaté le 14/11/2026 sur une cinquantaine de prises) :

- en début de scène, « Un : … », « Deux : … », « Trois : … » sont parfois sautés par la voix. Dans le texte envoyé à la synthèse, écrire « Un, … », « Deux, … », « Trois, … » (le scénario, lui, garde les deux-points pour les sous-titres) ;
- une prise sur cinq environ a un défaut (mot avalé, syllabe en trop). `caler_voix.py` le signale dans « écarts » : on refait alors la prise, c'est l'affaire de quelques centimes ;
- si le même mot résiste à deux prises (« tombe sur » était entendu « tourne sur »), on reformule la phrase dans le scénario plutôt que d'insister ;
- en cas de doute sur un mot, une troisième écoute indépendante tranche : la transcription Speko (`audio.transcribe`) du lien de téléchargement de la prise.
