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
  assets/               logos U-Mobility (PNG + SVG), logotype et symbole UGE vectorisés (uge-*.svg), loader SVG animé, polices woff2 (licence OFL)
dist/                   ← GÉNÉRÉ par build.py (ignoré par git, ne jamais éditer)
scripts/
  dev.py                dev local sans Docker : rebuild auto + serveur http://localhost:8080
  charte/               génération de docs/charte-graphique-u-mobility.pdf (Playwright)
nginx/nginx.dev.conf    nginx du conteneur de dev
Dockerfile.dev          image de dev (nginx + Python, rebuild à chaud)
docker-compose.dev.yml  lance le conteneur de dev
.github/workflows/deploy.yml   CD : build + publication GitHub Pages à chaque push sur main
docs/
  Charte_Gustave_Eiffel_V2-4.pdf        charte officielle de l'université (SOURCE de vérité du design, 36 p.)
  charte-graphique-u-mobility.pdf       charte du projet, générée par scripts/charte/
  product-backlog-initial.xlsx          Product Backlog (source des écrans)
  design-system/                        tokens.json, README, palette officielle
```

## 3. Commandes

```bash
python3 src/build.py                          # génère dist/ (Python 3.10+, aucune dépendance)
python3 scripts/dev.py                        # dev sans Docker → http://localhost:8080
docker compose -f docker-compose.dev.yml up --build   # dev avec Docker → http://localhost:8080
```

- La **prod** est sur **GitHub Pages** : un push sur `main` lance `.github/workflows/deploy.yml` (build Python puis `actions/deploy-pages`). Activer une fois : Settings → Pages → Source « GitHub Actions ». Sur un compte gratuit, Pages exige un dépôt public (dépôt privé : plan Pro/Team).
- `build.py` produit aussi `dist/404.html` (copie du plan) et `dist/.nojekyll`.
- `dist/preview.html` : **aperçu une page** (toutes les pages dans des `<template>`, routeur par ancre `#page.etat`, sélecteur d'écran + bascule Ordinateur/Mobile). C'est ce fichier qui est publié en **artifact Claude** ; il est autonome (logos en data URI, logotype UGE en SVG inline, motif en data URI dans le CSS, Google Fonts car l'artifact bloque les fichiers externes). Les pages statiques, elles, utilisent les polices locales.

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
| `index.html` | `#loader` |
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

- **Tokens** dans `:root` de `styles.css`, tirés de la **charte officielle UGE V2.4** (`docs/Charte_Gustave_Eiffel_V2-4.pdf`, p. 7) :
  bleu UGE `--brand #2F2A85` (Pantone 2746C) · `--brand-hover #231F66` · `--brand-soft #EBEAF4` · `--on-brand-muted #D6D5EA` · violet UGE `--secondary #8B4A97` · jaune UGE `--accent #FBBA00` (+ `--on-accent #0F273B`) · fond gris charte `--surface #F2F2F3` · cartes `--surface-raised #FFF` · `--line #DDDEE2` · encre bleu nuit UGE `--ink #0F273B` · `--ink-muted #52606E` · `--success #007A5A` (vert UGE #00936E assombri pour le texte, `--success-fill`) · rouge UGE `--danger #D2213C` · `--warning #EF7D00` / `--warning-ink #9A4F00` · échelle heatmap `--heat-0…4` (teintes du bleu).
  Les 9 autres couleurs secondaires officielles ont chacune 3 tokens `--c-<nom>` (aplat), `--c-<nom>-soft` (fond pâle), `--c-<nom>-ink` (texte ≥ 5:1) : magenta, turquoise, bleu, vertclair, jaune, orange, violet, vert, nuit.
  Polices : `--font-display` = `--font-sans` = TT Norms, remplacée par **Figtree** (300–800) tant qu'on n'a pas la licence.
  Espacements `--space-1…12` (4 px), rayons `--radius-sm 4 / md 6 / lg 8 / pill`, ombres `--shadow-card` (filet 1 px, pas d'ombre) / `--shadow-hover` (filet bleu) / `--shadow-pop` (listes) / `--shadow-dialog`, motif `--pattern` (symbole UGE en data URI).
- **Responsive par container queries** : `.frame { container-type: inline-size }` puis `@container app (max-width: 900px)`. Ça permet la bascule Mobile dans l'aperçu. Les popups/loader/toasts sont **hors** de `.frame` (le containment casserait `position: fixed`) ; leur largeur mobile passe par `.device-m`.
- Utilitaires : `.hide-m` (masqué en mobile), `.hide-d` (masqué en ordinateur), `[hidden]` forcé en `display:none`.
- **API data-attributes de `app.js`** (pas de framework) :
  `data-open="id"` ouvre `#m-id` · `data-close` ferme · `data-next` (+ `data-loading`) passe à l'étape suivante `[data-step]` · `data-tabs="groupe"` + `data-tab="x"` + panneaux `data-panel-of="groupe" data-panel="x"` · `data-toast="msg"` (+ `data-remove="sélecteur"`) · `data-loadtoast="msg"` (loader puis toast) · `.seg[data-single]` + `data-show`/`data-when` · `.chip[data-toggle]` / `.chip[data-radio]` · `.toggle` · `.days button` · `.stepper` (`data-max`) · `.rate` · `.tagbox` (Entrée pour ajouter) · `.suggest button` · `.select` · `data-tip` (infobulle) · `data-logout` · `#del-confirm` / `#del-go` (suppression de compte).
- **Loader** : le logo avec la route prolongée en perspective. Géométrie mesurée sur le logo (coordonnées du PNG d'origine 909×870) : point de fuite y = 495,3 ; demi-largeur = 0,196 × d ; tiret n : début d = 84 × 1,94ⁿ, fin = début × 1,63 (d = y − 495,3) ; animation n → n + s, s ∈ [0,1[ en 0,9 s. Implémenté dans `build.py` (`road_polys`, rendu statique) et `app.js` (`roadPolys`, animation) ; version autonome SMIL dans `src/assets/u-mobility-loader.svg`.

## 7. Décisions de design (demandées par Mathis, à respecter)

- Charte **officielle UGE V2.4** (`docs/Charte_Gustave_Eiffel_V2-4.pdf`, remplace l'ancienne piste « indigo + lavande » qui était fausse) :
  - couleur principale bleu `#2F2A85` ; les couleurs secondaires officielles ont chacune un rôle (demandé par Mathis : « trop monochrome ») :
    - bleu nuit = texte ; violet = boutons d'engagement (rejoindre, envoyer, publier) ; jaune = compteurs ; vert / rouge / orange = statuts ;
    - pastille d'icône des statistiques selon le type d'indicateur, identique partout : CO₂ vert, distance / trajets turquoise, note jaune, personnes violet, voiture / remplissage orange, trajets passager magenta, régularité / horaires bleu, signalements rouge (`.stat .k svg[data-i=…]`, `i()` ajoute `data-i` à chaque icône) ;
    - badge « Régulier » turquoise (`.badge.reg`), rôle « Conducteur » orange (`.badge.drv`) ;
    - tags : couleur stable selon le texte (`tagc()`/`hue()` dans `build.py`, `tagColor()` dans `app.js`, classes `.t0…t5`) ;
    - avatars : couleur stable par personne selon les initiales (`color_avatars()` dans `build.py`, classes `.av0…av6`) ;
    - messages système : a rejoint = vert, a modifié = orange, a quitté = rouge ;
    - anneau plein dans les bandeaux : magenta (tableau de bord, connexion), jaune (plan) ;
    - rôle dans un trajet : turquoise = conducteur, magenta = passager.
  - **une seule famille** pour titres et texte (TT Norms → Figtree) ; titres en gras 800 façon affiche de la charte ; titre de connexion en Light majuscules comme la couverture ; pas de titre « maigre + gras » ni de libellés en majuscules espacées.
  - **« ce qui contient est droit, ce qui se touche est rond »** : cartes, champs, panneaux à petits rayons (4–8 px) et à plat (filet, sans ombre) ; boutons, puces, onglets segmentés, jours, avatars en pilule / cercle.
  - **principe graphique** (charte p. 24-25) : de grands demi-anneaux couleur du fond entaillent les aplats bleus (`.hero .arc.a1`), un anneau blanc translucide (`.arc.a2`), une bande du **motif du symbole** (p. 6) sur le bord gauche (`.hero::before`, `.auth .pattern`).
  - **logotype officiel UGE** (blanc) en signature sur l'écran de connexion (`UGE_BLANC` dans `build.py`) ; règles : jamais le symbole seul à la place du logotype, largeur ≥ 25 mm, zone de protection = largeur du demi-cercle du symbole, ni rotation, ni déformation, ni recoloration.
- **Voiture uniquement** (plus de vélo / RER / marche).
- **Zones de départ et d'arrivée prédéfinies** (liste), pas d'adresse ni de géolocalisation ; le profil permet seulement d'en choisir une.
- **Carte de trajet** (`trip()`) : heures libellées « Départ » / « Arrivée estimée » ; **pas** d'avatar du conducteur mais les **avatars des passagers acceptés** + un cercle pointillé par place vide (`seats()`) ; badge « N place(s) restante(s) » sur fond bleu primaire (`.badge.seats`) ; **pas** de pourcentage de compatibilité ; afficher le **nombre de demandes en attente** ; la carte entière est cliquable (survol + « Voir le détail »). Dans Mes trajets, la carte porte des actions et « Voir le détail » est un lien dans la ligne des boutons (pas de boutons « Messagerie » / « Voir le détail » en double).
- **Rôle dans le trajet** (`role="d"|"p"`, `role_tag()`) : l'utilisateur est **à la fois passager et conducteur** ; chaque trajet affiche son rôle : volant turquoise = Conducteur, siège magenta = Passager (étiquette + liseré gauche de la carte, icône ronde dans les en-têtes de `group_head()`).
- **Prix et commission** : le prix affiché est ce que paie le passager ; U-Mobility prélève une **commission fixe de 0,19 €** par passager et par trajet (`COMMISSION`, `driver_share()`). Elle apparaît sur les cartes (« dont 0,19 € de commission »), en détail dans le trajet et la popup de demande (part reversée au conducteur + commission = prix), et côté conducteur dans Publier (« tu reçois 2,31 € »).
- **Trajet régulier** : le détail l'annonce clairement (badge « Trajet régulier », titre « Chaque lundi, mardi… ») et montre **jours, période et prochain départ** sans ouvrir la popup (`.recur`).
- **Tags** facultatifs sur un trajet publié, et **tags libres** écrits par l'utilisateur dans ses préférences ; ils servent à matcher la recherche.
- **Notes sur 5 étoiles sans avis écrit** : le passager note le conducteur, le conducteur note chaque passager, après le trajet. **Une seule note par utilisateur** (pas de note « conducteur » et « passager » séparées). Détail du trajet : répartition des notes, pas de commentaires ni de phrase d'explication.
- **Demande de réservation** (popup) : pour un trajet régulier, le passager choisit ses jours parmi ceux du conducteur ; places ; message facultatif (140 caractères).
- Page **« Mes trajets »** (et non « Mes réservations ») : annulation claire (place ou trajet, une date ou tout le régulier) ; les demandes sont **groupées sous leur trajet**.
- **Tableau de bord** : **une seule vue** (pas de sélecteur Passager / Conducteur) : trajets à venir des deux rôles mélangés avec leur étiquette de rôle, demandes à traiter et demandes envoyées ; activité façon **GitHub** (heatmap 6 mois, tous rôles).
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

- Charte officielle intégrée (couleurs, logotype et symbole vectorisés depuis le PDF). Reste : obtenir la **licence TT Norms®** (fichiers woff2) pour remplacer Figtree, et faire valider par le service communication l'association du logo U-Mobility avec le logotype UGE (endossement, charte p. 14-16).
- Backlog « fonctionnalités avancées » pas encore maquetté : **challenges / gamification** (classement anonymisé, badges), **carte interactive** des zones de rendez-vous (seule une carte fictive existe dans le détail), **export mensuel** (boutons présents dans Historique et Direction, sans écran dédié).
- Écrans possibles ensuite : onboarding (choix de la zone et des horaires au premier lancement), notifications, états vides et erreurs.
- Passage au code : composants React + Tailwind à partir de `styles.css` (tokens → `@theme` Tailwind v4), et version mobile (React Native / Expo : le loader SMIL ne marche pas avec `react-native-svg`, prévoir `Animated` ou Lottie).
