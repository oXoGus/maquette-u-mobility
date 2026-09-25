U-Mobility est le service de covoiturage des étudiants de l'Université Gustave Eiffel (Cité Descartes, Champs-sur-Marne, et les autres sites), disponible en application mobile et en site web : la même charte s'applique aux deux. La marque est proche, pratique et rassurante : on partage un trajet avec quelqu'un de sa fac, pas avec un inconnu. L'indigo est la couleur de l'université ; il reste la couleur dominante quelle que soit la piste retenue.

## Choisir une piste de couleurs

Ce système propose **5 alternatives** de couleurs secondaires autour de l'indigo `brand` (#282284), suivies de la **charte officielle de l'université** (piste 6). Chaque alternative est un thème : basculer de thème montre toute la charte (tokens, composants, couverture) dans cette piste. La planche **Comparatif** les montre côte à côte sur le même écran. Le détail de chaque piste est dans la section « Les pistes de couleurs ».

| Thème | Secondaire | Accent | Intention |
| --- | --- | --- | --- |
| `eco` | Vert #2DB273 | Ciel #5EC8F2 | Écologie, nature, trajet vertueux |
| `corail` | Corail #FF6F59 | Beurre #FFD55A | Chaleureux, convivial, social |
| `route` | Turquoise #00A6A6 | Orange #FF8A00 | Mobilité, signalétique routière |
| `electrique` | Lime #C8F03C | Rose #FF5C9A | Énergique, soirée, génération étudiante |
| `campus` | Ciel #8FB8FF | Ambre #F5A300 | Sobre, institutionnel, proche de l'université |
| `officielle` | Lavande #535995 | Lavande claire #C7C9DB (provisoire) | Charte officielle UGE V2.4, indigo #282F7A |

## Ton et contenus

- Tutoyer l'étudiant (« Où vas-tu ? », « Ta place est réservée »). Phrases courtes, verbes d'action.
- Nommer les vrais lieux du campus : « Bâtiment Copernic », « Gare de Noisy-Champs », « Bienvenüe ».
- Boutons à l'infinitif ou à la 1re personne : « Proposer un trajet », « Réserver ma place ».
- Heures au format français `8 h 10`, prix `2,50 €`, CO₂ `−1,2 kg CO₂`.
- Pas d'emoji dans l'interface ; pas de points d'exclamation en série ; pas de majuscules pleines sauf dans `caption`.

## Couleur

- Règle 60 / 30 / 10 : `brand` et `surface` portent l'écran, `secondary` marque l'action et les informations clés, `accent` n'est qu'une touche (notification, note, « Nouveau »).
- `brand` : barre d'app, bouton principal, liens, onglet actif, titres d'accueil. Texte dessus : `on-brand`.
- `secondary` est un **aplat**, jamais une couleur de texte sur fond clair. Pour du texte dans la teinte secondaire, utiliser `secondary-ink`. Texte sur l'aplat : `on-secondary` (indigo foncé dans les pistes 1 à 5, blanc dans la piste officielle).
- Un seul bouton `secondary` par écran : l'appel à l'action (Rechercher, Réserver, Proposer).
- Texte courant `ink`, texte secondaire `ink-muted`, cartes `surface-raised` sur fond `surface`, séparateurs `line`.
- Statuts : `success` et `danger` en texte + icône + mot, jamais la couleur seule.
- Tous les couples texte/fond cités dans les notes des tokens atteignent 4,5:1 dans les 6 thèmes.

## Typographie

- Titres en **Outfit** (famille `display`), géométrique et arrondie comme le logo : `display` pour l'accueil, `title-lg` pour le titre d'écran, `title-md` pour les cartes et sections.
- Texte en **Figtree** (famille `sans`) : `body` par défaut, `body-lg` pour les introductions et le chat, `label` pour boutons et onglets, `caption` pour badges et métadonnées.
- Deux polices Google Fonts, chargées par `components/bundle.css`.

## Espacement, formes, ombres

- Grille de 4 px : `space-4` (16 px) de marge latérale sur mobile et de padding de carte, `space-3` entre cartes, `space-6` entre sections.
- Formes généreusement arrondies, en écho au logo : `radius-md` (boutons, cartes), `radius-lg` (feuilles modales), `radius-pill` (badges, avatars), `radius-sm` (champs).
- `shadow-card` pour les cartes de trajet posées sur `surface` ; `shadow-sheet` pour la feuille qui remonte du bas.
- Motif graphique : la route pointillée du logo. Elle relie départ et arrivée dans `TripCard` et peut rythmer les illustrations (tirets arrondis `radius-sm`).

## Focus et accessibilité

- Focus clavier : contour 2 px `focus-ring` décalé de 2 px, visible sur toutes les surfaces.
- Cibles tactiles de 48 px minimum (`cc-btn`).

## Logo et iconographie

- Logo : `assets/Logos` — `logo-indigo.png` sur fond clair, `logo-blanc.png` sur `brand` ou `ink`. Le logo ne prend jamais la couleur secondaire.
- Icônes : pictogrammes pleins aux angles arrondis, dans le même esprit que le logo (formes pleines, pas de trait fin). Proposition : Material Symbols Rounded, style rempli — à valider, aucune bibliothèque d'icônes n'a encore été fournie.
- Icônes en `fill: currentColor`, 18 px dans les boutons, 12 px dans les badges, 24 px dans la barre d'onglets.
