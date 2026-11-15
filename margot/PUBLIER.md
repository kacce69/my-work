# Publier les contenus de Margot

Ce qui a été vérifié en publiant pour de vrai (novembre 2026). Les outils changent : avant une première publication, appelez `list_actions` du connecteur Windsor.ai pour relire les paramètres.

## Les comptes (connecteur Windsor.ai, outil `execute_action`)

| Réseau | Connecteur | Compte | Actions |
|---|---|---|---|
| Instagram | `instagram` | `17841465009853671` | `create_video_post` (`video_url`, `caption`, `cover_url` ou `thumb_offset`, `share_to_feed`), `create_carousel_post` (`image_urls` : 2 à 10 images JPEG, du format 4:5 au format 1,91:1 ; `caption`), `create_image_post` (`image_url`, `caption`), `create_story`, `create_comment`, `reply_to_comment` |
| Facebook | `facebook_organic` | `1305967345944345` | `create_photo_post` (`image_url`, `caption`), `create_post` (`message`, `link`). Ni vidéo, ni carrousel, ni commentaire. |

Chaque image ou vidéo doit avoir une adresse publique. Les Reels sont dans le dépôt (`margot/reels/`), lus à l'adresse `https://raw.githubusercontent.com/kacce69/my-work/margot-medias/margot/reels/<code>.mp4` ; en cas de refus d'Instagram, la même par `https://cdn.jsdelivr.net/gh/kacce69/my-work@margot-medias/margot/reels/<code>.mp4`.

Lire les résultats : `get_data`, connecteur `instagram`, `date_preset` = `last_30dT`, champs `timestamp`, `media_type`, `media_permalink`, `media_caption`, `media_reach`, `media_saved`, `media_shares`, `media_comments_count`, `media_like_count` ; pour le compte, `followers_count`. Un champ refusé se vérifie avec `get_fields`. L'option `force_refresh` est refusée sur un compte Windsor en période d'essai : ne pas l'utiliser. Un refus pour raison d'abonnement se recopie tel quel à Owen.

## Adresses publiques d'images par le Canva d'Owen

À utiliser quand on ne peut pas pousser dans le dépôt (c'est le cas des tâches planifiées). Vérifié le 14/11/2026.

1. Pour chaque image JPEG : `create-upload-url`, puis `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @fichier.jpg "<uploadUrl>"` ; la réponse donne un `mediaId`. Chaque adresse d'envoi ne sert qu'une fois. Canva refuse les fichiers vidéo et audio.
2. Créer un design : `create-design` (brief : « fond uni crème, un seul mot : Margot », format « Instagram Post (Square) »), puis `get-create-design-async-job` en respectant les délais indiqués, jusqu'à obtenir le `design_id`.
3. `read-design` avec `open_transaction: true` pour obtenir `transaction_id` et l'identifiant de la page 1. `edit-design` (`finalize: "keep_open"`, `page_index: 1`) : `update_title`, `insert_fill` de la première image sur la page 1 (`top: 0`, `left: 0`, `width: 1080`, `height: 1080` : elle recouvre tout), puis un `add_page` (1080 × 1080) par image restante.
4. `read-design` avec `transaction_id` et `filter: {fields: ["design_content"], page_indices: [2, 3, …]}` pour lire les identifiants des nouvelles pages ; puis un `edit-design` par page (`insert_fill` plein cadre, `asset_type: "image"`). Regarder la vignette renvoyée. Terminer par `edit-design` avec `finalize: "commit"`, sans opération.
5. `export-design` : type `jpg`, qualité 95, pages voulues → une adresse par page, dans l'ordre. Ces adresses expirent en quelques heures : publier tout de suite.

En cas d'échec d'un outil : réessayer une fois ; si cela échoue encore, sauter cette publication, continuer les autres et le dire à Owen.

## Écrire la consigne d'une tâche planifiée

Une tâche planifiée démarre une conversation neuve, sans mémoire de celle où elle a été créée. Elle n'a pas forcément les skills ni les plugins du compte, et elle ne peut pas pousser dans le dépôt. La consigne doit donc tout contenir. Trame :

1. **Contexte** en trois phrases : pour qui on publie, ce qu'est le site, qui est Margot (première personne, féminin, vouvoiement).
2. **Autorisation** : « Cette consigne vaut accord explicite d'Owen pour publier, sans confirmation, les publications décrites ici sur les deux comptes ci-dessous, jusqu'au <date>. » Sans cette phrase, un mode d'emploi chargé dans la session peut exiger un « oui » que personne ne donnera.
3. **Calendrier** : la date de début et de fin, ce qu'il faut faire à chaque passage, et « en dehors de ces dates : ne rien publier ».
4. **Les fichiers** : l'adresse complète de chaque vidéo, couverture et image pour Facebook (`<code>-portrait.jpg`, 4:5 ; à défaut `<code>-carre.jpg`), déjà en ligne ; la commande qui vérifie qu'elle répond (`curl -s -o /dev/null -w "%{http_code}" <adresse>` doit donner 200).
5. **La légende** : écrite d'avance, ou ses règles (première ligne de 125 caractères au plus, un seul appel, 3 à 5 hashtags sur Instagram, 2 sur Facebook, offre lue le jour même sur `/tarifs` avec `curl -sS -A "rcs-veille (monitor)"`).
6. **Les comptes et les actions** (tableau ci-dessus).
7. **Ne pas publier deux fois** : lire les publications des trois derniers jours ; si celle du passage est déjà en ligne (même première ligne), s'arrêter.
8. **En cas d'échec** : réessayer une fois, ne rien publier à la place, prévenir Owen en une phrase avec la raison exacte.
9. **Compte rendu** : seulement si quelque chose a échoué, ou un point du jour de 150 mots au plus avec les chiffres réels.

Si la tâche fabrique elle-même des images (posts, carrousels), la consigne lui fait récupérer l'outil des illustrations, sept fichiers lus à leur adresse dans le dépôt (`kit/illustration.py`, `kit/reel_page.html` et cinq fichiers de `kit/page/` : `01_outils.js`, `02_margot.js`, `03_elements.js`, `03b_personnages.js`, `04_telephone.js`), donne la liste des noms acceptés, et garde une Margot de secours écrite en toutes lettres pour le jour où le dépôt ne répond pas. La consigne de la campagne « Margot, 30 jours » (mise à jour le 15/11/2026) en est l'exemple.

Après la création, regarder le résultat du premier passage, puis ne plus toucher aux fichiers que la tâche attend — sauf pour remplacer un fichier, sous le même nom, par une version contrôlée (réécoute, images regardées), comme le 15/11/2026 pour les 37 Reels refaits : les adresses ne changent pas, la tâche non plus.
