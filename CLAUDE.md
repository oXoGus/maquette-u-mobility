# CLAUDE.md — U-Mobility (maquette)

Contexte complet pour reprendre le projet dans Claude Code. À lire avant toute modification.

## 1. Le projet

- **U-Mobility** : application de covoiturage pour les étudiants et personnels de l'**Université Gustave Eiffel** (campus Cité Descartes, Champs-sur-Marne).
- Projet de **SAÉ de BUT Informatique** (2e année) de Mathis. Livrables finaux : un **site web** et une **application mobile cross-platform** qui partagent le plus possible le front.
- Ce dépôt contient la **maquette interactive** (HTML/CSS/JS statique, versions ordinateur et mobile) qui sert :
  1. à valider le design et les parcours ;
  2. à être **importée dans Figma** avec le plugin **html.to.design** (import par URL) ;
  3. de référence visuelle pour le futur code (React + Tailwind envisagé côté web).
- Langue de l'interface et de la documentation : **français**. On **tutoie** l'utilisateur.

## 2. Arborescence

```
src/                    ← SOURCE (c'est ici qu'on modifie)
  build.py              générateur : contient TOUTES les pages (HTML en f-strings Python) + helpers
  styles.css            tokens (variables CSS) + tous les composants
  app.js                interactions (popups, onglets, étoiles, tags, loader, routeur de l'aperçu)
  fonts.css             @font-face des polices auto-hébergées
  assets/               logos (PNG + SVG), loader SVG animé, polices woff2 (licence OFL)
dist/                   ← GÉNÉRÉ par build.py (ignoré par git, ne jamais éditer)
scripts/
  dev.py                dev local sans Docker : rebuild auto + serveur http://localhost:8080
  charte/               génération de docs/charte-graphique-u-mobility.pdf (Playwright)
nginx/nginx.dev.conf    nginx du conteneur de dev
Dockerfile.dev          image de dev (nginx + Python, rebuild à chaud)
docker-compose.dev.yml  lance le conteneur de dev
.github/workflows/deploy.yml   CD : build + publication GitHub Pages à chaque push sur main
docs/
  charte-graphique-u-mobility.pdf       charte du projet (15 pages)
  charte-officielle-uge-couverture.png  couverture de la charte officielle UGE V2.4 (source des couleurs)
  product-backlog-initial.xlsx          Product Backlog (source des écrans)
  design-system/                        tokens.json (6 pistes de couleurs), README, palettes
```

## 3. Commandes

```bash
python3 src/build.py                          # génère dist/ (Python 3.10+, aucune dépendance)
python3 scripts/dev.py                        # dev sans Docker → http://localhost:8080
docker compose -f docker-compose.dev.yml up --build   # dev avec Docker → http://localhost:8080
```

- La **prod** est sur **GitHub Pages** : un push sur `main` lance `.github/workflows/deploy.yml` (build Python puis `actions/deploy-pages`). Activer une fois : Settings → Pages → Source « GitHub Actions ». Sur un compte gratuit, Pages exige un dépôt public (dépôt privé : plan Pro/Team).
- `build.py` produit aussi `dist/404.html` (copie du plan) et `dist/.nojekyll`.
- `dist/preview.html` : **aperçu une page** (toutes les pages dans des `<template>`, routeur par ancre `#page.etat`, sélecteur d'écran + bascule Ordinateur/Mobile). C'est ce fichier qui est publié en **artifact Claude** ; il est autonome (logos en data URI, Google Fonts car l'artifact bloque les fichiers externes). Les pages statiques, elles, utilisent les polices locales.

## 4. Comment les pages sont construites (`src/build.py`)

- Tout est dans `build.py` : un dictionnaire `PAGES[clé] = dict(title, body | app, modals, role, active, sub, mtitle, back, topright, raw)`.
  - `body` : contenu de la page ; `app_page()` l'entoure de la barre latérale, de la barre mobile, du titre et de la barre d'onglets.
  - `raw=True` (connexion, plan) : `app` est le HTML complet, sans gabarit.
  - `role` : `user` (défaut), `mod` (modérateur), `dir` (direction) → change la navigation et le compte en bas de la barre latérale.
  - `modals` : HTML des popups de la page (placés hors du `.frame`, voir §6).
- Helpers à réutiliser plutôt que d'écrire du HTML à la main :
  `i(nom)` icône SVG (dictionnaire `P`) · `trip(...)` carte de trajet · `select(id, valeur)` liste déroulante de zones · `days(on, pick, allowed, mini)` sélecteur de jours · `rate(id)` notation 5 étoiles · `stars(moyenne, n)` · `stars5(k)` · `tagbox(id, tags)` · `tags_static(tags)` · `inp(id, valeur, placeholder, icône)` · `textarea(id, placeholder, maxlength)` · `modal(id, contenu, wide, drawer)` · `dhead(titre, sous-titre, icône, rouge)` · `success(titre, texte)` · `heatmap(seed)` · `bars(data)` · `hbars(data)`.
- Données de démo : zones `ZONES_DEP` / `ZONES_CAMPUS`, personnes fictives (Léa M., Inès N., Thomas K., Yanis B., Hugo P., Amina S., Paul R., Chloé L.), l'utilisateur connecté est « Mathis D. ».
- Attention aux f-strings : pas de `\` dans une expression `{…}` (Python 3.11) ; utiliser une constante (ex. `ACT`).

## 5. Écrans et états (ancres)

Chaque état s'ouvre par une ancre, utile pour l'import Figma (`plan.html` liste tout) :

| Page | États |
|---|---|
| `connexion.html` | comptes démo : étudiant, modérateur, direction |
| `index.html` | `#passager` (défaut), `#conducteur`, `#loader` |
| `recherche.html` | — |
| `trajet.html` | `#demande` (popup de réservation), `#signaler` |
| `publier.html` | `#voiture` |
| `mes-trajets.html` | `#avenir`, `#recues`, `#envoyees`, `#anoter`, `#annuler`, `#annuler-trajet`, `#noter-conducteur`, `#noter-passagers`, `#signaler-compte` |
| `historique.html` | `#noter-passagers` |
| `messages.html` | `#signaler-compte`, `#annuler` (quitter le trajet) |
| `profil.html` | `#creneau`, `#modifier-profil`, `#voiture`, `#export-donnees`, `#supprimer-compte` |
| `moderation.html` (modérateur) | `#signalement` (panneau latéral) |
| `direction.html` (direction) | — |

## 6. CSS et JS : conventions

- **Tokens** dans `:root` de `styles.css` (charte officielle UGE, piste 6) :
  indigo `--brand #282F7A` · `--brand-hover #1E2461` · `--brand-soft #EAEBF3` · lavande `--secondary #535995` · accent provisoire `--accent #C7C9DB` · fond `--surface #F6F6FA` · cartes `--surface-raised #FFF` · `--line #DCDCE8` · encre `--ink #16193F` · `--ink-muted #555A7E` · `--success #1D7A4C` · `--danger #C42B40` · `--warning-ink #8A5A00` · échelle heatmap `--heat-0…4`.
  Espacements `--space-1…12` (4 px), rayons `--radius-sm 8 / md 14 / lg 24 / pill`, ombres `--shadow-card / hover / dialog`.
- **Responsive par container queries** : `.frame { container-type: inline-size }` puis `@container app (max-width: 900px)`. Ça permet la bascule Mobile dans l'aperçu. Les popups/loader/toasts sont **hors** de `.frame` (le containment casserait `position: fixed`) ; leur largeur mobile passe par `.device-m`.
- Utilitaires : `.hide-m` (masqué en mobile), `.hide-d` (masqué en ordinateur), `[hidden]` forcé en `display:none`.
- **API data-attributes de `app.js`** (pas de framework) :
  `data-open="id"` ouvre `#m-id` · `data-close` ferme · `data-next` (+ `data-loading`) passe à l'étape suivante `[data-step]` · `data-tabs="groupe"` + `data-tab="x"` + panneaux `data-panel-of="groupe" data-panel="x"` · `data-toast="msg"` (+ `data-remove="sélecteur"`) · `data-loadtoast="msg"` (loader puis toast) · `.seg[data-single]` + `data-show`/`data-when` · `.chip[data-toggle]` / `.chip[data-radio]` · `.toggle` · `.days button` · `.stepper` (`data-max`) · `.rate` · `.tagbox` (Entrée pour ajouter) · `.suggest button` · `.select` · `data-tip` (infobulle) · `data-logout` · `#del-confirm` / `#del-go` (suppression de compte).
- **Loader** : le logo avec la route prolongée en perspective. Géométrie mesurée sur le logo (coordonnées du PNG d'origine 909×870) : point de fuite y = 495,3 ; demi-largeur = 0,196 × d ; tiret n : début d = 84 × 1,94ⁿ, fin = début × 1,63 (d = y − 495,3) ; animation n → n + s, s ∈ [0,1[ en 0,9 s. Implémenté dans `build.py` (`road_polys`, rendu statique) et `app.js` (`roadPolys`, animation) ; version autonome SMIL dans `src/assets/u-mobility-loader.svg`.

## 7. Décisions de design (demandées par Mathis, à respecter)

- Charte **officielle UGE V2.4** : indigo + lavande relevés sur la couverture (`docs/charte-officielle-uge-couverture.png`). Motif des **arcs** lavande sur indigo, titres d'accueil en Outfit Light + 600.
- **Voiture uniquement** (plus de vélo / RER / marche).
- **Zones de départ et d'arrivée prédéfinies** (liste), pas d'adresse ni de géolocalisation ; le profil permet seulement d'en choisir une.
- **Carte de trajet** : heures libellées « Départ » / « Arrivée estimée » ; **pas** d'avatar du conducteur ; **pas** de pourcentage de compatibilité ; afficher le **nombre de demandes en attente** et les places libres ; la carte entière est cliquable (survol + bouton « Voir le détail »).
- **Tags** facultatifs sur un trajet publié, et **tags libres** écrits par l'utilisateur dans ses préférences ; ils servent à matcher la recherche.
- **Notes sur 5 étoiles sans avis écrit** : le passager note le conducteur, le conducteur note chaque passager, après le trajet. Détail du trajet : répartition des notes, pas de commentaires.
- **Demande de réservation** (popup) : pour un trajet régulier, le passager choisit ses jours parmi ceux du conducteur ; places ; message facultatif (140 caractères).
- Page **« Mes trajets »** (et non « Mes réservations ») : annulation claire (place ou trajet, une date ou tout le régulier) ; les demandes sont **groupées sous leur trajet**.
- **Tableau de bord** : vue Passager **ou** Conducteur (pas les deux) ; activité façon **GitHub** (heatmap 6 mois).
- **Messagerie par trajet** avec tous les membres, **messages système** (a rejoint / a quitté / horaire modifié / trajet créé), **pas de réponses rapides** au-dessus de la saisie, bouton **Signaler** bien visible (en-tête + drapeau par membre).
- **Signalements** : compte (depuis les messages) ou trajet ; traités sur une page **réservée aux modérateurs**.
- **Direction** : tableau de bord de statistiques **anonymisées** (aucun groupe < 10 personnes).
- Barre latérale : **compte collé en bas** (sticky) avec bouton **Se déconnecter** visible (aussi dans le Profil).
- **RGPD** : « Télécharger mes données » (JSON/CSV) et « Supprimer mon compte et mes données » (confirmation en tapant SUPPRIMER) dans Profil → Confidentialité et données ; polices auto-hébergées.
- Interactions dessinées : ajouter un créneau, modifier le profil, ajouter une voiture (sans plaque), survols partout, loader personnalisé.
- Écriture : tutoiement, lieux réels du campus, formats français (`7 h 50`, `2,50 €`), pas d'emoji dans l'interface.

## 8. Règles pour les modifications

1. Modifier **`src/`** uniquement, puis `python3 src/build.py`. Ne jamais éditer `dist/`.
2. Vérifier chaque changement en **1440 px et 390 px** (bascule Mobile de `preview.html` ou navigateur réduit) : pas de débordement horizontal.
3. Réutiliser les helpers et les classes existantes ; nouvelles couleurs = nouveaux tokens dans `:root`.
4. Contrastes AA minimum (texte 4,5:1), focus visible, statuts = couleur + mot + icône, cibles ≥ 44 px.
5. Un nouvel état / popup = une ancre, et l'ajouter à `PLAN` dans `build.py` (pour l'import Figma).
6. Si le design change (couleurs, typo, composants), régénérer la charte : voir `scripts/charte/make_charte.py`.

## 9. Import dans Figma (html.to.design)

1. Pousser sur `main` → site sur `https://<compte>.github.io/<dépôt>/`.
2. Plugin html.to.design → onglet **Web** → coller l'URL d'une page (ou d'un état, ex. `…/trajet.html#demande`).
3. Viewports : **1440** et **390** en même temps · Theme Light.
4. Les liens entre écrans se refont dans l'onglet **Prototype** de Figma ; la barre d'onglets mobile se fixe avec « Fixed (stay in place) ».

## 10. Reste à faire / points ouverts

- Récupérer le **PDF complet de la charte officielle UGE V2.4** : police officielle, couleurs complémentaires (l'accent `#C7C9DB` est **provisoire**), logo vectoriel de l'université, règles d'association des logos.
- Backlog « fonctionnalités avancées » pas encore maquetté : **challenges / gamification** (classement anonymisé, badges), **carte interactive** des zones de rendez-vous (seule une carte fictive existe dans le détail), **export mensuel** (boutons présents dans Historique et Direction, sans écran dédié).
- Écrans possibles ensuite : onboarding (choix de la zone et des horaires au premier lancement), notifications, états vides et erreurs.
- Passage au code : composants React + Tailwind à partir de `styles.css` (tokens → `@theme` Tailwind v4), et version mobile (React Native / Expo : le loader SMIL ne marche pas avec `react-native-svg`, prévoir `Animated` ou Lottie).
