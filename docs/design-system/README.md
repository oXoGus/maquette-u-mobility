U-Mobility est le service de covoiturage des étudiants et personnels de l'Université Gustave Eiffel (Cité Descartes, Champs-sur-Marne, et les autres sites), disponible en application mobile et en site web : la même charte s'applique aux deux. La marque est proche, pratique et rassurante : on partage un trajet avec quelqu'un de sa fac, pas avec un inconnu.

Le design system suit **un seul thème : la charte graphique officielle de l'université, V2.4** (`docs/Charte_Gustave_Eiffel_V2-4.pdf`). Les valeurs de référence sont dans `tokens.json` et appliquées dans le bloc `:root` de `src/styles.css` ; la palette complète est détaillée dans `palettes.md`.

## Ton et contenus

- Tutoyer l'étudiant (« Où vas-tu ? », « Ta place est réservée »). Phrases courtes, verbes d'action.
- Nommer les vrais lieux du campus : « Bâtiment Copernic », « Gare de Noisy-Champs », « Bienvenüe ».
- Boutons = l'action exacte, à l'infinitif ou à la 1re personne : « Demander à rejoindre ce trajet », « Annuler ma place ». Jamais « Valider » ou « OK ».
- Heures libellées et au format français : « Départ 7 h 50 », « Arrivée estimée 8 h 20 » ; prix `2,50 €` ; CO₂ `1,4 kg de CO₂`.
- Pas d'emoji dans l'interface, pas de points d'exclamation en série, pas de capitales pleines (seule exception : le titre de l'écran de connexion, voir Typographie).

## Couleur

- Couleur principale : **bleu UGE `brand` #2F2A85** (Pantone 2746C). Barre latérale, en-tête mobile, bandeaux d'accueil, bouton principal, liens, onglet actif, logo. Texte dessus : `on-brand` (blanc) ou `on-brand-muted`.
- Règle 60 / 30 / 10 : `brand` et `surface` portent l'écran ; le texte bleu nuit, le blanc des cartes et les teintes `brand-soft` font la structure ; `secondary` et `accent` ne sont que des touches.
- `secondary` = **violet UGE #8B4A97** : boutons d'engagement (« Demander à rejoindre », « Envoyer la demande », « Publier le trajet ») et avatars, texte blanc dessus. Un seul bouton violet par écran.
- `accent` = **jaune UGE #FBBA00** : pastilles de compteur de la barre latérale et marques « Nouveau », toujours avec `on-accent` (bleu nuit). Jamais une couleur de texte.
- Texte courant `ink` (**bleu nuit UGE #0F273B**), texte secondaire `ink-muted` #52606E, cartes `surface-raised` sur le gris `surface` #F2F2F3, filets `line`.
- Statuts : `success` #007A5A (vert UGE assombri), `danger` #D2213C (rouge UGE), `warning-ink` #9A4F00 (orange UGE assombri), chacun avec son fond `*-soft`. Toujours couleur + mot + icône, jamais la couleur seule.
- Les couleurs officielles ne sont pas retouchées ; quand l'une d'elles n'atteint pas 4,5:1 en texte (vert, orange), une variante assombrie sert au texte et l'officielle reste pour les aplats non textuels.
- Magenta, vert clair, turquoise et bleu ne sont pas utilisés pour l'instant (réserve pour graphiques et illustrations).

## Typographie

- La charte impose **TT Norms®** pour toutes les communications, titres comme texte : **une seule famille**. Sa licence est payante, donc **Figtree** (SIL OFL, auto-hébergée dans `src/assets/fonts`, graisses 300 à 800) la remplace. Pile : `"TT Norms Pro", "TT Norms", "Figtree", "Segoe UI", system-ui, sans-serif` ; si la licence est fournie, il suffit d'ajouter ses `@font-face`.
- Titres en **gras 800, casse de phrase**, comme les affiches de la charte : `display` 40/44 pour le bandeau d'accueil, `title-lg` 30/36 (h1, −0,02 em), `title-md` 20/26 en 700 (h2), `title-sm` 16/22 en 700 (h3).
- Exception : le titre de l'écran de connexion reprend la couverture de la charte (« CHARTE GRAPHIQUE ») en **Light 300 et capitales**, 56/60.
- Texte : `body` 15/22 par défaut, `body-lg` 16/24 pour les introductions, `label` 14/18 en 700 pour les boutons, `caption` 12/16 en 600 pour badges et métadonnées, **en casse de phrase, sans espacement de lettres**.
- Chiffres alignés (prix, heures, statistiques) : `font-variant-numeric: tabular-nums`.
- Polices auto-hébergées : aucun appel à Google Fonts (RGPD).

## Formes, espacement, ombres

- Principe : **« ce qui contient est droit, ce qui se touche est rond »**. Cartes, champs, panneaux et popups ont des angles à peine adoucis (`radius-sm` 4 px, `radius-md` 6 px, `radius-lg` 8 px) ; boutons, puces, badges, contrôles segmentés, sélecteur de jours et avatars sont en pilule ou en cercle (`radius-pill`).
- **Aplats sans ombre** : `shadow-card` est un filet de 1 px `line` ; au survol, `shadow-hover` passe à un filet bleu de 1,5 px. Les ombres portées sont réservées à ce qui passe au-dessus de la page : `shadow-pop` (listes déroulantes, infobulles) et `shadow-dialog` (popups, panneaux latéraux).
- Grille de 4 px : `space-4` (16 px) de marge latérale sur mobile, `space-6` (24 px) de padding de carte et entre sections, `space-8` (32 px) de marge du contenu sur ordinateur.

## Principe graphique et motif

- **Principe graphique UGE** (charte p. 24-25), construit à partir du symbole du logotype : de grands **demi-anneaux de la couleur du fond** entaillent les aplats bleus (bandeau d'accueil), un **anneau blanc translucide** fait écho au symbole, et une **bande du motif** (le symbole répété, charte p. 6) borde le côté gauche.
- Anneaux toujours coupés par les bords du bloc, jamais plus de deux par bloc. Le motif reste discret (opacité 16 à 20 %).
- Motif propre à U-Mobility : la **route pointillée** du logo, qui relie départ et arrivée dans la carte de trajet et défile dans le loader.

## Logos

- **Logotype Université Gustave Eiffel** : vectorisé depuis le PDF officiel, `src/assets/uge-logo.svg` (bleu) et `uge-logo-blanc.svg` (blanc) ; symbole seul : `uge-symbole.svg`.
  - Le symbole peut servir d'élément graphique (motif, avatar de réseau social) mais **ne remplace jamais le logotype**.
  - Taille minimale : **25 mm de large** à l'impression (≈ 96 px à l'écran) ; zone de protection = la largeur du demi-cercle du symbole, tout autour.
  - Bleu sur fond blanc ; noir sur fonds de couleur claire ; blanc sur fonds plus foncés (bleu UGE, bleu nuit) ; bleu dans un cartouche blanc sur fond complexe.
  - Interdits : incliner, modifier les proportions, modifier les couleurs, retirer des éléments, utiliser une autre typographie, inventer un autre principe d'endossement, utiliser une version illisible.
- **Pictogramme U-Mobility** (`src/assets/logo-indigo.svg` / `.png`, recoloré en #2F2A85, et `logo-blanc`) : bleu UGE sur fond clair, blanc sur `brand` ou `ink`. Jamais dans une autre couleur ni sur le violet. Il est présenté à côté du logotype de l'université (ex. écran de connexion), sans être fusionné avec lui dans un même bloc.

## Focus et accessibilité

- Contrastes AA minimum (4,5:1 pour le texte courant) ; les couples utilisés sont listés dans la charte PDF (`docs/charte-graphique-u-mobility.pdf`) et dans les notes de `tokens.json`.
- Focus clavier : contour 2 px `focus-ring` (bleu UGE) décalé de 2 px, visible sur toutes les surfaces.
- Cibles tactiles de 44 px minimum. Échap ferme les popups. Animations coupées si l'utilisateur demande moins d'animations.

## Iconographie

- Icônes au trait (2 px, extrémités arrondies), `stroke: currentColor`, 20 px par défaut, 16 px dans les badges, 24 px dans la barre d'onglets.
