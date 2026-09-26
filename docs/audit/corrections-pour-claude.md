# Corrections à appliquer : feuille de route pour Claude Code

> **Statut : ANALYSE SEULEMENT. Ne rien corriger avant que Mathis ait tranché les décisions de la section 0.**
> Audit du 25/09/2026, fait sur le commit `0416f3b`. Les numéros de ligne (`src/build.py:NNN`, `src/styles.css:NNN`, `src/app.js:NNN`) valent pour ce commit. S'il a bougé, **retrouve l'endroit par le contenu cité**, pas par le numéro.
> Rapport lisible pour Mathis : [`rapport-audit.md`](rapport-audit.md). Scripts d'audit à relancer après correction : `docs/audit/scripts/`. Les chemins `BASE` et `D` y sont en dur : adapte-les. Pour les lancer : un venv avec `playwright`, puis `python -m playwright install chromium`. Captures de référence : `docs/audit/captures/`.

**Règles du projet (CLAUDE.md §8), toujours valables :**
- modifier `src/` uniquement, jamais `dist/` ;
- `python3 src/build.py` après chaque lot ;
- vérifier en 1440 et 390 px, **et maintenant aussi en 1024 px** ;
- nouvelles couleurs = tokens dans `:root` ;
- tout nouvel état = une ancre dans `PLAN` ;
- design modifié = régénérer la charte (`scripts/charte/make_charte.py`) ;
- mettre à jour CLAUDE.md §5, §7 et §10 quand une décision change.

Chaque tâche a un identifiant (`CDC-x`, `RWD-x`, `A11Y-x`, `DATA-x`, `NAV-x`, `CODE-x`, `TXT-x`). Gravité : **B** = bloquant, **M** = majeur, **m** = mineur.

---

## 0. Décisions à obtenir de Mathis (elles bloquent les tâches indiquées)

| # | Question | Recommandation | Tâches bloquées |
|---|---|---|---|
| D1 | Supprimer prix et commission ? | Oui, tout supprimer | CDC-1, TXT-3, DATA-13 |
| D2 | Ajouter « modes » au profil ? | Oui (chips), publication en voiture seule conservée | CDC-2 |
| D3 | Rôles : back-office `admin` unique, plus un rôle `asso` ? | Oui | CDC-4, CDC-12 |
| D4 | Dates : décaler les libellés pour 2026, ou tout passer en 2025 ? | 2026 (projet démarré le 26/09/2026) | DATA-1 |
| D5 | Badge qualitatif de compatibilité, sans pourcentage ? | Oui | CDC-10 |
| D6 | Messages prédéfinis dans la messagerie ? | À son choix | CDC-5 (partie) |
| D7 | Barre d'onglets mobile fixe ? | Sticky, avec classe `.figma` pour l'import | RWD-9 |
| D8 | Persona fictif à la place de « Mathis Dintrat » ? | Oui | CDC-8 |

---

## 1. Cahier des charges (`docs/SAE05_u-mobility_cahier_des_charges.pdf`)

### CDC-1 [B] Retirer prix et commission (D1)
- **Cdc :** §4, hors périmètre : « Paiement ou partage de frais réel. Responsabilité contractuelle ».
- **À supprimer :**
  - `COMMISSION = 0.19`, `driver_share()` et peut-être `euros()` (`build.py:145-152`) ;
  - le prix et « dont 0,19 € de commission » dans `trip()` (`build.py:175-176`), ainsi que la classe `.fee` ;
  - le bloc `.recap` du détail du trajet (`build.py:482-487`) et celui de la popup `#demande` (`build.py:500-503`) ;
  - le champ `p-price`, la suggestion et « Tu reçois 2,31 € » dans `publier` (`build.py:538`) ;
  - la stat « Frais partagés 96 € » dans `historique` (`build.py:672`), à remplacer par « Régularité » ou « Km partagés » ;
  - le tri « Prix » dans `recherche` (`build.py:431`).
- **À remplacer :** le motif « Tarif abusif » (`build.py:511`) et le signalement #248 « Tarif abusif (25 €) » (`build.py:871`) deviennent « Demande d'argent / usage commercial ».
- **Carte de trajet :** dans `.trip-side`, mettre à la place « N places restantes » et « ≈ X kg CO₂ évités ».
- **Mention :** ajouter une ligne `.hint` dans `#demande` et `publier` : « U-Mobility met en relation les membres de l'université, sans paiement ni responsabilité sur le trajet. » (couvre aussi CDC-15).
- **Documentation :** CLAUDE.md §7, retirer « Prix et commission ». Retirer aussi les règles CSS mortes (`.fee`, `.recap` si inutilisé).

### CDC-2 [M] Modes de déplacement (D2)
- **Cdc :** §1, et §6 `MobilityProfile(... modes)`.
- **Profil :** dans `profil` (`build.py:813-867`), ajouter une carte « Mes modes de déplacement » avec des `.chip[data-toggle]` : Covoiturage conducteur, Covoiturage passager, Transports en commun, Vélo, Marche.
- **Publier :** remplacer « Seule la voiture est proposée sur U-Mobility. » (`build.py:520`) par « Trajet en voiture partagée ».
- **Plan :** `PLAN` « Voiture uniquement » (`build.py:975`).
- **Direction :** ajouter `hbars()` « Part modale déclarée ».
- **Documentation :** CLAUDE.md §7.

### CDC-3 [M] Séparer campus et point d'arrivée
- **Cdc :** §5 et §6, `User(... campus ...)`.
- **Constat :** `ZONES_CAMPUS` (`build.py:99`) contient des bâtiments.
- **À faire :**
  - créer `CAMPUS = ["Marne-la-Vallée (Cité Descartes)", "Paris", "Lille", "Lyon", "Marseille", ...]` (campus UGE fictivisés si besoin) ;
  - dans `profil`, ajouter un champ « Campus » (nouveau `select` avec un groupe à part) ;
  - renommer le libellé « Campus habituel » (`build.py:778`, `821`) en « Point d'arrivée habituel » ;
  - ajouter un filtre Campus dans `direction`.

### CDC-4 [M] Rôles back-office (D3)
- **Cdc :** §3 « Administrateurs », « Associations ou services campus » ; §4 « Back-office : modération, signalements, statistiques ».
- **`ROLES` (`build.py:201-205`) :**
  - `dir` devient `admin`, avec le libellé « Administrateur · Vie étudiante » ;
  - corriger les initiales (DATA-14).
- **`nav_html()` (`build.py:208-223`) :**
  - navigation admin unique : Signalements, Trajets (CDC-7), Statistiques, Challenges (CDC-12), Journal (CDC-16) ;
  - `mod` reste un sous-rôle, limité aux signalements et aux trajets.
- **Connexion (`build.py:350-351`) :** comptes démo Étudiant, Modérateur, Administrateur et Association.
- **Documentation :** PLAN (`build.py:995-996`), CLAUDE.md §5 et §7.

### CDC-5 [M] Messagerie limitée
- **Constat :** conversation « Bienvenüe → Torcy · demande en attente » (`build.py:701`), en contradiction avec `build.py:489`.
- **Conversation verrouillée :** la rendre verrouillée (icône `i("lock")`, « Disponible après acceptation par Yanis ») et ajouter une ancre `messages.html#verrouillee` dans PLAN.
- **Signaler un message :** ajouter « Signaler ce message » sur chaque `.bubble`, avec un `iconbtn` au survol ou au focus, à côté de `small`.
- **Note sous la saisie (`build.py:725`) :** ajouter « 30 messages par jour maximum ».
- **Messages prédéfinis (D6) :** si validé, une rangée de `.chip` « J'arrive », « 5 min de retard », « Je suis au point de RDV ». Mettre à jour CLAUDE.md §7, qui l'interdit aujourd'hui.

### CDC-6 [M] Régularité dans le tableau de bord
- **Cdc :** §5 « trajets effectués, estimation CO2 évitée, régularité ».
- **Stats de `index` (`build.py:367-370`) :** remplacer « Personnes rencontrées » par « Régularité », avec l'icône `repeat` (pastille bleue, convention `.stat .k svg[data-i=…]`). Valeur : `3,2 trajets / semaine` et sous-ligne « 8 semaines actives sur 10 ».

### CDC-7 [M] Masquer un trajet (critère d'acceptation §13 n° 3)
- **Constat :** dans `moderation`, « Masquer le trajet concerné » n'est qu'un toast (`build.py:907`).
- **Ajouter :**
  - `#signalement-trajet` : panneau latéral pour le signalement #248, avec `trip()` en aperçu et les actions Masquer / Classer / Contacter le conducteur ;
  - `#masquer-trajet` : popup de confirmation (motif en liste, case « Prévenir les passagers », texte `.hint` « Le trajet disparaît de la recherche ; les passagers sont notifiés ») ;
  - un onglet ou une page « Trajets » du back-office : liste avec recherche et bouton « Masquer » ;
  - côté utilisateur, dans `mes-trajets` : une carte avec `badge ko` « Masqué par la modération » (statut = couleur + mot + icône).
- **PLAN :** ajouter les ancres.

### CDC-8 [m] Données fictives (D8)
- **Cdc :** §8 « données fictives », « comptes fictifs ».
- **Remplacer :**
  - « Dintrat » (`build.py:786`) ;
  - `mathis.dintrat@edu.univ-eiffel.fr` (`build.py:789`, `799`), par un persona fictif `@demo.u-mobility.fr` ;
  - « Utilise ton compte universitaire » (`build.py:343`), par « Compte de démonstration (aucune donnée réelle) ».
- **Cohérence :** mettre le même domaine que les comptes démo (`build.py:349`).
- **Documentation :** CLAUDE.md §4, qui mentionne « Mathis D. ».

### CDC-9 [m] Contexte et public
- **Niveau :**
  - « BUT Informatique · 2e année » devient « 3e année » (`build.py:202`, `788`, `859`) ;
  - « BUT Info 2 » (`build.py:396`) devient « BUT Info 3 » ;
  - CLAUDE.md §1 : BUT3, groupe de 6 ; application native = facultative (le cdc demande un « front-end web responsive »).
- **Public :**
  - « Covoiturage étudiant » (`build.py:336`) devient « Covoiturage universitaire » ;
  - « aide les autres étudiants » (`build.py:625`) et « étudiants de ma composante » (`build.py:842`) deviennent « membres de l'université ».

### CDC-10 [m] Score de compatibilité (D5)
- **Cdc :** §14 « filtres simples puis scorer les résultats ».
- **À faire :**
  - `recherche` : option de tri « Meilleure correspondance » (par défaut) ;
  - `trip()` : badge qualitatif facultatif `badge ok` « Très compatible », avec une sous-ligne « Même zone · ± 10 min ». **Pas de pourcentage.**
- **Documentation :** ajuster CLAUDE.md §7.

### CDC-11 [M] États d'erreur, états vides et cas limites
- **Cdc :** §7 « messages d'erreur compréhensibles », « cas limites, erreurs réseau simulées, données manquantes et droits insuffisants ».
- **Composants à créer :**
  - `.field.error` : bordure `--danger`, et `.hint.error` avec `i("alert")` et le texte, relié au champ par `aria-describedby` et `aria-invalid="true"` ;
  - `.empty-state` : icône, titre, texte, action ;
  - variante `data-toast-type="error"` dans `toast()` (`app.js:8-17`).
- **Nouvelles ancres, toutes dans PLAN :**
  - `connexion.html#erreur` : identifiants incorrects ;
  - `publier.html#erreurs` : arrivée avant le départ, places supérieures à celles du véhicule, champ requis ;
  - `recherche.html#vide` : aucun résultat, avec l'action « Élargir l'horaire » et « Créer une alerte » ;
  - `trajet.html#complet` et `trajet.html#indisponible` : trajet complet, annulé ou masqué ;
  - `index.html#hors-ligne` : toast « Connexion perdue · Réessayer » et contenu en squelette. La classe `.skeleton` existe déjà mais n'est pas utilisée ;
  - `acces-refuse.html` : page `raw` « Accès réservé aux modérateurs » ;
  - `404.html` : une vraie page 404, au lieu de la copie du plan (`build.py`, génération de `404.html`) ;
  - `profil.html#incomplet` : bandeau « Complète ton profil mobilité ».
- **Mes trajets, onglet `#envoyees` :** ajouter les statuts Refusée, Expirée (24 h) et Trajet complet (`TripRequest.statut`).

### CDC-12 [M] Challenges et badges
- **Cdc :** §2.1 et §4 avancé, « Challenge par groupe ou promotion avec classement anonymisé ».
- **Nouvelle page `challenges.html`** (entrée dans `USER_NAV`, icône `trophy` à ajouter à `P`) :
  - challenge en cours avec `.progress`, qui existe déjà mais n'est pas utilisée ;
  - classement par promo ou composante (groupes ≥ 10, aucun nom) ;
  - toggle d'opt-in « Participer aux challenges ».
- **Profil :** carte « Mes badges », en réutilisant les pastilles de couleur de `.stat .k`.
- **Rôle `asso` ou `admin` :** `challenges-admin`, avec `#creer-challenge`.
- **Documentation :** PLAN, CLAUDE.md §5 et §10.

### CDC-13 [M] Carte des zones de rendez-vous
- **Cdc :** §4 avancé.
- **À faire :**
  - popup `recherche.html#carte` et `profil.html#carte` : grande `.map` (réutiliser `.map`, `.zone`, `.pin` de `build.py:458-463`), avec toutes les `ZONES_DEP` cliquables (bouton, `aria-pressed`) et une légende ;
  - donner à la `.map` une alternative texte (voir A11Y-12).

### CDC-14 [m] Export du bilan mensuel
- **Constat :** boutons présents (`build.py:667`, `925`), mais seulement `data-loadtoast`.
- **À faire :** popup `#export-bilan` (mois, format PDF/CSV, aperçu du contenu : trajets, km, CO₂), sur `historique` et `direction`.

### CDC-15 [M] Information RGPD
- **À faire :**
  - `profil.html#confidentialite` : popup ou section avec les données collectées, les finalités, les durées de conservation, qui voit quoi, et les droits ;
  - lien « Confidentialité » en pied de `connexion` ;
  - `.hint` dans `publier` et `#demande` : « Ton prénom, initiale, note et zone sont visibles des membres du trajet ».

### CDC-16 [m] Traçabilité, profils vérifiés, divers
- **Journal :** « Journal des actions » dans le back-office (masquages, suspensions, consultations d'identité) : un tableau.
- **Profils vérifiés :** icône `shield` et « Vérifié », aujourd'hui seulement sur Léa (`build.py:481`). À ajouter dans :
  - `req()` (`build.py:556-561`) ;
  - les membres de `messages` (`build.py:730-733`) ;
  - la ligne conducteur de `trip()`.
- **Recherche :** le `.seg` Ponctuel / Régulier (`build.py:406`) n'a pas de `data-show`. Ajouter `data-show` et `days(... )` avec `data-when="regulier"`.
- **Onboarding :** trois étapes `data-step` (campus et zone, créneaux types, modes et préférences), sur `index.html#bienvenue`.

---

## 2. Responsive

**Cause racine des RWD-1 à RWD-6 :** le seuil unique `@container app (max-width: 900px)` porte sur **le cadre entier**. À 901 px, la barre latérale (256 px) apparaît et la zone de contenu tombe à environ 600 px, alors que les grilles sont fixées pour environ 1 000 px. Les captures `docs/audit/captures/messages_1100.png`, `recherche_1024.png` et `publier_1024_viewport.png` le montrent.

**Correctif de fond recommandé**, à faire avant les cas particuliers :
1. `.field { grid-template-columns: minmax(0,1fr) }` (`styles.css:221`). La piste implicite `auto` prend la largeur minimale du texte `nowrap` des `.select`.
2. Un **palier intermédiaire** : `@container app (max-width: 1280px) { … }` qui fait passer `.split`, `.split-left` et `.chat-layout` à des colonnes réduites ou empilées. Alternative : `.main` devient `container: content / inline-size`, et les grilles réagissent à la largeur réelle du contenu.
3. `.trip { container-type: inline-size }` et `@container (max-width: 520px)` reprennent l'empilement mobile (`styles.css:578-584`), à généraliser à partir de `styles.css:348-350`.

| ID | G | Page / plage | Correctif |
|---|---|---|---|
| RWD-1 | B | messages, 901–1180 | `.chat-layout` (`styles.css:120`, `300px 1fr 260px`). Sous 1280 : `260px minmax(0,1fr)`, et `.chat-layout > :last-child { grid-column: 1 / -1 }` (membres sous le fil), ou panneau membres derrière un bouton. |
| RWD-2 | B | recherche, index, 901–1100 | Carte `.trip` (`styles.css:305`, `minmax(0,1fr) auto`). La colonne route tombe à 0–44 px. Container query sur `.trip` (point 3 ci-dessus). |
| RWD-3 | B | recherche, 901–1180 | `.searchgrid` (`styles.css:121`, `1fr auto 1fr 170px 150px`). Correctif `.field` (point 1), puis sous 1180 : `1fr auto 1fr`, avec Date et Heure sur la ligne 2. |
| RWD-4 | M | publier, 901–1100 | `.grid-3` et `.grid-2` (`styles.css:116`, `repeat(3,1fr)` sans `minmax(0,…)`) dans `.split` (`styles.css:118`). `repeat(3, minmax(0,1fr))`, et `.split` en une colonne sous 1180. |
| RWD-5 | M | trajet, 901–1024 | Indicateurs `.grid-3` (`build.py:466`). `repeat(auto-fit, minmax(140px,1fr))`. |
| RWD-6 | M | profil, 901–1180 | `.split` et `.table-wrap` (`build.py:819-826`). Même bascule en une colonne que RWD-4. |
| RWD-7 | B | popups en mobile (`#noter-passagers`, etc.) | Les règles `.list > .li { flex-wrap: wrap }` et `.list .grow { flex: 1 1 180px }` (`styles.css:598-599`) sont dans `@container app`, qui ne voit pas les popups (hors `.frame`). Ajouter `.dialog, .drawer .panel { container: dlg / inline-size }`, puis `@container dlg (max-width: 440px) { .list > .li { flex-wrap: wrap } .list .grow { flex: 1 1 180px } .grid-2, .grid-3 { grid-template-columns: minmax(0,1fr) } }`. Capture `mes-trajets_noter-passagers_390.png`. |
| RWD-8 | M | toutes les popups, ≤ 900 | La règle `.dialog { padding: 16px }` (`styles.css:603`) ne s'applique pas. `@container dlg (max-width: 440px) { .dialog { padding: 16px } }`, ou `@media (max-width: 900px)` plus `.device-m .dialog`. Débordement de l'e-mail à 320 px dans `#modifier-profil` (capture `profil_modifier-profil_320.png`). |
| RWD-9 | M | pages utilisateur, ≤ 900 (D7) | `.tabbar` en `position: relative` (`styles.css:563`) : elle se trouve à environ 2 900 px du haut. `position: sticky; bottom: 0`, plus `padding-bottom: calc(64px + env(safe-area-inset-bottom))` sur `.content`. Garder le mode non fixe sous `body.figma` (à documenter dans CLAUDE.md §9). |
| RWD-10 | M | tout | Tailles de police en px (`styles.css:63` et suivantes) : le texte agrandi dans le navigateur n'a aucun effet (WCAG 1.4.4). Passer les `font-size` et `font:` en `rem` (base 16 : 15 px = .9375rem). Garder les espacements en px. |
| RWD-11 | M | preview.html | Pas de `<meta charset>` ni de viewport : la chaîne `art` (`build.py` vers 1085) commence par `<title>`. Préfixer par `<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">`. |
| RWD-12 | m | popups | Le focus initial tombe sur Fermer (`app.js:55`, `$('input, textarea, button', m)`). Chercher d'abord `input, textarea, select, [role=radio]`, puis `.btn.primary`, en excluant `[data-close]`. |
| RWD-13 | M | mobile | Cibles de moins de 44 px : `.chip` (`styles.css:194`) 32 ; `.iconbtn` (177, 561) 34–40 ; `.btn.sm` (174) 36 ; `.toggle` (252) 40×24 ; `.tag button` (209) 18 ; `.rate button` (292) 36 ; `.days` (257) 40 ; `.tabbar a` (564) 42 ; `.linkbtn`, `a.more` 22 ; `.trip .go` 34 ; `.seg` 34 ; `.suggest` 28 ; `.stepper` 36. Dans `@container app (max-width: 900px)` : `min-height: 44px` (et `min-width` pour les boutons icône). `.toggle` et `.tag button` : zone étendue `::before { content: ""; position: absolute; inset: -10px }`. |
| RWD-14 | m | mobile | Textes de 11 px : `.seg .n` (251), `.days.mini span` (263), `.bubble small` (470), libellés heatmap (396, 398). Minimum 12 px. |
| RWD-15 | m | index, historique, direction | `.heat-wrap` (min 640, `styles.css:395`), peak (560, 411) et `.table-wrap` défilent sans indice. Ajouter un `mask-image` en dégradé à droite, plus `tabindex="0" role="region" aria-label` (voir A11Y-24). Envisager 3 mois de heatmap en mobile. |
| RWD-16 | m | index | Mois de la heatmap collés (« marsavr. », `build.py:284`). Ne pas afficher le libellé d'un mois s'il reste moins de 2 colonnes avant le suivant. |
| RWD-17 | m | index, vers 1024 | `.hero .arc.a2` en `right: 190px` (`styles.css:145`) passe derrière le bouton translucide. Position en `%`, ou masquer sous 1100 px. |
| RWD-18 | m | index, mes-trajets | `.troute li` : colonne horaire de 52 et 58 px (`styles.css:330`, `584`) pour « 17 h 45 » (57 px). Passer à 62 et 58 px, puis recaler `.troute::before`. |
| RWD-19 | m | ≤ 390 | « 7 h / 50 » : voir TXT-2 (espaces insécables). |
| RWD-20 | m | mes-trajets, ≤ 360 | `.seg` (`styles.css:601-602`) sur 2 lignes. `overflow-x: auto; flex-wrap: nowrap`, en gardant la pilule. |
| RWD-21 | m | grandes popups, 320–390 | `.dialog-foot { position: sticky; bottom: calc(-1 * var(--space-6)); background: var(--surface-raised) }`. |
| RWD-22 | m | 1920 | `.content` plafonné à 1180 et collé à gauche (`styles.css:109`), cloche à x = 1888. Plafonner `.topbar` pareil (`max-width` + `margin-inline: auto` sur les deux, ou aucun des deux). |
| RWD-23 | m | preview.html en mobile < 700 | Dans `SHELL_CSS` (`build.py` vers 1090) : `@media (max-width: 700px) { body.device-m .frame { max-width: none; margin: 0; border-radius: 0; box-shadow: none; padding-bottom: 64px } }`. |
| RWD-24 | m | direction, 320–360 | `.grid-4` (`styles.css:570`) sur 2 colonnes serrées. Une colonne sous 360 px. |

---

## 3. Accessibilité (WCAG 2.2 AA)

**Base :**
- axe-core : 50 violations WCAG, 0 contraste texte ;
- scripts : `docs/audit/scripts/run_axe.py`, `kbd.py`, `pairs.py`, `manual.py`.

**Utilitaire à créer d'abord :**
`.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0 }`, à mettre dans `styles.css`.

| ID | G | WCAG | Problème et preuve | Correctif |
|---|---|---|---|---|
| A11Y-1 | B | 2.4.7 | `:focus-visible { outline: 2px solid var(--brand) }` (`styles.css:72`) donne 1:1 sur `--brand`, et c'est invisible dans la barre latérale, `.hero`, `.mobilebar`, `.auth .side`, `.stat.dark`. | Token `--focus-on-brand: var(--accent)` (7,2:1), puis `.sidebar :focus-visible, .hero :focus-visible, .mobilebar :focus-visible, .auth .side :focus-visible, .stat.dark :focus-visible { outline-color: var(--focus-on-brand) }`. |
| A11Y-2 | B | 2.1.1 | `moderation` : `<tr class="click" data-open="signalement">` (`build.py:878`), non focusable. | Dans la cellule Objet, `<button class="linkbtn" data-open="signalement">Compte #3481</button>`. Garder le clic sur le `tr`. |
| A11Y-3 | B | 2.1.1, 4.1.2 | `div.li.click[data-conv]` (`build.py:700-703`) et le choix du membre dans `#signaler-compte` (`build.py:743`), non focusables. | Conversations : `<button type="button" class="li click" aria-pressed>` (ou `role="listbox"` et `option`). Membre à signaler : `<fieldset>` avec des `<input type="radio">` visuellement stylés, ou `role="radiogroup"` avec `role="radio" aria-checked`, les flèches et un roving tabindex. `app.js:156` : mettre à jour `aria-*` **et limiter à `el.closest('.list')`** (voir NAV-5). |
| A11Y-4 | M | 4.1.2, 2.4.3, 1.3.1 | Popups sans nom (axe `aria-dialog-name` sur 16 états) ; Tab sort de la popup (12 sur 25 dans `trajet.html#demande`) ; focus sur `BODY` après Échap. | `modal()` (`build.py:256`) : `role="dialog" aria-modal="true" aria-labelledby="m-{id}-t"`. `dhead()` (`build.py:262`) : paramètre id et `<h2 id="m-{id}-t">`. `openModal()` (`app.js:49`) : mémoriser `document.activeElement`, `document.querySelector('.frame').inert = true`, boucler Tab et Shift+Tab. `closeModals()` (`app.js:59`) : `inert = false`, puis `focus()` sur l'élément mémorisé. |
| A11Y-5 | M | 2.4.3, 4.1.3 | `data-next data-loading` (`app.js:131-132`) : le bouton passe en `disabled`, donc le focus est perdu, et l'étape de succès n'est pas annoncée. | `aria-disabled="true"` et blocage du clic au lieu de `disabled`. Dans `go()`, `focus()` sur `<h2 tabindex="-1">` de `success()` (`build.py:267`) ; `role="status"` sur `.success-state`. Libellé de chargement propre à l'action via `data-loading="Suppression…"` (voir CODE-7). |
| A11Y-6 | M | 4.1.3 | `.toasts` créé sans `aria-live` (`app.js:8-17`). | `<div class="toasts" role="status" aria-live="polite"></div>` dans le gabarit, à côté de `{LOADER}`. `aria-hidden` sur le SVG du toast ; durée ≥ 5 s. |
| A11Y-7 | M | 4.1.2, 1.3.1, 3.3.2, 2.1.1 | `.select` : nom = valeur seule, pas d'`aria-expanded`, `role="listbox"` sans `role="option"`, pas de flèches ; `#s-sort` et `#h-period` (`build.py:431`, `665`) sans `aria-haspopup`. | `select(id, valeur, label)` (`build.py:102`) : `<span class="label" id="{id}-l">`, bouton `aria-haspopup="listbox" aria-expanded="false" aria-controls="{id}-lb" aria-labelledby="{id}-l {id}-v"`, options `role="option" aria-selected`, `.grp` en `role="group" aria-label`. `app.js:147-155` : `aria-expanded`, `aria-selected`, Haut / Bas / Début / Fin / Entrée / Échap, focus rendu au bouton. Plus simple : un `<select>` natif stylé. |
| A11Y-8 | M | 1.3.1, 4.1.2 | Onglets de Mes trajets (`mt_tabs`, `build.py:568`) : axe `aria-required-children`, pas de `role="tab"`, `aria-selected` ni `tabpanel`. | Boutons `role="tab" id="tab-{x}" aria-controls="panel-{x}" aria-selected tabindex="0/-1"`, panneaux `role="tabpanel" aria-labelledby`. `activateTab()` (`app.js:62`) : mettre à jour les attributs, flèches Gauche / Droite / Début / Fin. Corriger aussi le plantage si le premier `[data-tab]` est hors de `[data-tabs]` (CODE-7). |
| A11Y-9 | M | 4.1.2 | `.seg[data-single]`, `.chip[data-radio]`, `.chip[data-toggle]`, `.days button` : seule la classe `.on` change (`app.js:139-143`). `days()` (`build.py:84`) : jours `.off` actifs et à 1,7:1. | Toggles et jours : `aria-pressed`. `seg` et radio : conteneur `role="radiogroup" aria-labelledby`, enfants `role="radio" aria-checked`. Jours non autorisés : `disabled`. Mise à jour dans chaque branche de `app.js`. |
| A11Y-10 | M | 1.3.1 | `days(pick=False, mini=True)` : le lecteur d'écran lit « L M M J V S D ». | Lettres en `aria-hidden`, plus `<span class="sr-only">Lundi, mardi, jeudi, vendredi</span>`. |
| A11Y-11 | M | 4.1.2 | `rate()` (`build.py:75`) : 5 boutons sans état ; `.rate-label` non annoncé. | Conteneur `role="radiogroup" aria-label="Note pour {nom}"`, étoiles `role="radio" aria-checked` en roving tabindex, flèches dans `setRate()` (`app.js:98`), `.rate-label` en `aria-live="polite"`. |
| A11Y-12 | M | 1.1.1 | `stars5()` (`build.py:69`) : `aria-label` sur `<span>` sans rôle (12 `aria-prohibited-attr` dans `historique`) ; même défaut pour `seats()` (`build.py:161`) et `.map` (`build.py:458`). | `role="img"` sur ces conteneurs et `aria-hidden="true"` sur les SVG internes. |
| A11Y-13 | M | 1.3.1, 2.4.4 | `trip()` : `<a class="trip" aria-label="Voir le détail du trajet X vers Y">` (vers `build.py:205`) masque tout le contenu. | `<article class="trip">` avec un titre `<h3><a class="trip-link" href>X → Y</a></h3>`, puis `.trip-link::after { content: ""; position: absolute; inset: 0 }` (`.trip` est déjà en `position: relative`). Les boutons d'action de Mes trajets passent au-dessus (`position: relative; z-index: 1`). Supprimer `aria-label`. |
| A11Y-14 | M | 1.1.1, 1.3.1, 2.1.1, 1.4.13, 1.4.11 | `heatmap()` (`build.py:305`) : seulement « Activité des 6 derniers mois » ; peak (`build.py:920-922`) sans alternative ; `data-tip` au survol seulement (`app.js:88-95`), pas de fermeture avec Échap ; niveaux voisins à 1,44:1. | `aria-label` avec le résumé chiffré, plus `<table class="sr-only">` des totaux par mois (et pour peak). `bars()` : `tabindex="0"` sur `.b`. `app.js` : infobulle aussi sur `focusin` et `focusout`, fermeture avec Échap, infobulle survolable. |
| A11Y-15 | M | 1.4.10, 2.4.6 | ≤ 720 px (et zoom 200 %) : `.sidebar, .topbar { display: none }` (`styles.css:555`) retire `<h1>`, `sub` et `topright` (Semaine / Mois / Exporter sur `direction`). Rôles `mod` et `dir` : aucune navigation ni déconnexion. | `app_page()` (`build.py:226-247`) : la barre mobile porte le `<h1>` (celui du topbar en `aria-hidden`, ou un seul `<h1>` visible selon la largeur). Afficher `sub` et `topright` sous la barre mobile. Barre d'onglets pour `mod`, `dir` et `admin` (Signalements ou Stats, plus Déconnexion). |
| A11Y-16 | M | 2.4.1 | Pas de lien d'évitement (9 à 11 Tab avant le contenu). | `app_page()` : `<a class="skip" href="#contenu">Aller au contenu</a>` en premier, `<main id="contenu" tabindex="-1">`, CSS `.skip` visible au focus. |
| A11Y-17 | M | 1.4.11 | Contours `--line` (#DDDEE2, 1,34:1) sur `.input`, `.select > button`, `.tagbox`, `.chip`, `.days`. `.toggle` éteint à 1,71:1. Étoiles vides à 1,71:1. Halo de focus `--brand-soft` à 1,19:1. `outline: 0` sur les champs (`styles.css:214`, `227`). | Token `--line-input: #8A919B` (≥ 3:1) pour ces composants. `.toggle` éteint : `--ink-muted`. Étoiles vides : contour `--ink-muted`. `.input:focus-within { box-shadow: 0 0 0 2px var(--brand) }`. |
| A11Y-18 | M | 4.1.2 | Messages ≤ 900 : bouton Envoyer sans nom (`<span class="hide-m">Envoyer</span>`, `build.py:724`). | `aria-label="Envoyer"`, ou `.sr-only` en mobile. |
| A11Y-19 | M | 1.3.5 | Pas d'`autocomplete` sur `login-mail`, `login-pass`, `e-prenom`, `e-nom`. | `inp(..., auto=None)` (`build.py:112`), avec les valeurs `email`, `current-password`, `given-name` et `family-name`. |
| A11Y-20 | m | 2.5.3, 4.1.2 | Toggles : le nom accessible diffère du libellé visible (`build.py:425-427`, `544`, `842-844`). | `id` sur le `<span>` du libellé, puis `aria-labelledby` et `role="switch" aria-checked` (`app.js:142`). |
| A11Y-21 | m | 2.4.3, 2.4.6 | Tag ajouté : bouton « Retirer » générique (`app.js:193`) ; focus perdu après suppression. | `aria-label="Retirer " + text`, focus rendu à l'input de `.tagbox`, annonce dans la région de statut. |
| A11Y-22 | m | 4.1.3, 1.3.1 | `.stepper` : valeur non annoncée, boutons non reliés au libellé. | `<output aria-live="polite">`, `role="group" aria-labelledby`, noms « Retirer une place » et « Ajouter une place », `aria-disabled` aux bornes. |
| A11Y-23 | m | 1.3.1 | Titres : `messages` passe de h1 à h3 (`build.py:707`, `728`) ; deux `h1` sur `index` (topbar + bandeau) et sur `connexion` ; aucun `h2` dans Mes trajets. | `messages` : passer en h2. `index` : bandeau en `h2`. `connexion` : le sous-titre devient un `<p>`. `group_head()` (`build.py:564`) : `<h2>`. Titre de carte en `h3` (A11Y-13). |
| A11Y-24 | m | 1.3.1 | Landmarks et tableaux. `connexion` et `plan` n'ont pas de `<main>`. Plusieurs `<aside>` n'ont pas de nom. `nav.tabbar` n'a ni `aria-label` ni `aria-current` (`build.py:231`). `.crumb` n'est pas une `nav`. Il y a des `<th>` vides (`build.py:827`, `890`). `.table-wrap` n'est pas focusable. Les mois de l'historique sont en `td colspan`. | Ajouter `<main>` sur `connexion` et `plan`. Donner `aria-label="Menu principal"` à la barre latérale, et transformer les colonnes de contenu en `<section>`. Ajouter `aria-current="page"` dans la tabbar. Mettre `<nav aria-label="Fil d'Ariane">` autour de `.crumb`. Remplacer les `<th>` vides par `<th><span class="sr-only">Actions</span></th>`. Ajouter `tabindex="0" role="region" aria-label` à `.table-wrap`. Utiliser `<th scope="colgroup">` pour les mois et ajouter un `<caption>`. |
| A11Y-25 | m | 1.3.1, 3.3.2 | Formulaires. `.hint` et `.counter` ne sont pas reliés au champ (`textarea()`, `build.py:117`). La connexion n'est pas un `<form>`, son bouton est un `<a class="btn">`, et aucun champ n'est `required`. L'e-mail du profil est en `disabled`. | Ajouter `aria-describedby` sur ces champs. Faire de la connexion un `<form>` avec `<button type="submit">` et `required`, et gérer la suite en JS (`loader` puis redirection). Passer l'e-mail en `readonly`. |
| A11Y-26 | m | 2.4.4 | Liens et libellés lus sans leur contexte. Le badge de navigation est lu « Mes trajets3 » (`nav_html`, `build.py:208`). Le point de la cloche n'a pas de texte. `stars()` (`build.py:64`) est lu « 4,9 (38) ». | Ajouter `<span class="sr-only"> demandes en attente</span>` au badge. Donner à la cloche `aria-label="Notifications, 2 non lues"`. Ajouter à `stars()` un texte `sr-only` « sur 5, 38 notes ». |
| A11Y-27 | m | 2.4.2 | Aperçu : `document.title = 'U-Mobility'` fixe (`build.py:1103`). | `document.title = PAGES[k].title + ' — U-Mobility'` (injecter les titres dans le JS du routeur). |
| A11Y-28 | m | 4.1.3 | Loader : `role="status"` correct. | Ajouter `aria-busy="true"` sur `<main>` pendant `loader()`. |

---

## 4. Données de démo et cohérence

| ID | G | Problème | Correctif |
|---|---|---|---|
| DATA-1 | M | **Jours de semaine de 2025 pour des dates 2026** (vérifié : 25/09/2026 = vendredi, 26/09 = samedi, 01/10 = jeudi). Exemples : « Demain · jeu. 25 sept. », « Ven. 26 sept. », « Mer. 1er oct. », « Jeu. 18 sept. », « Ven. 12 sept. », « Lundi 15 septembre », « Ven. 20 juin ». La heatmap (`build.py:275`) utilise le vrai calendrier : son infobulle dit « sam. 12 sept. ». | D4. Créer `TODAY = date(2026, 9, 24)` (jeudi) et un helper `fr_day(date, court=True)` qui produit « jeu. 24 sept. » ou « Jeudi 24 septembre » avec `datetime` et des tables FR. Remplacer tous les libellés en dur par `fr_day(TODAY + timedelta(n))`. Chercher avec `grep -nE "(lun|mar|mer|jeu|ven|sam|dim)\.? [0-9]{1,2}(er)? " src/build.py` et `grep -niE "(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) [0-9]"`. |
| DATA-2 | M | Heatmap : « 123 trajets sur les 6 derniers mois », contre 42 dans les stats et l'Historique. Répartition incohérente avec `months` (août 1 trajet contre 0 km). `total_hint` et `role_word` ne servent pas (`build.py:273`). | `heatmap()` génère exactement les jours de trajet d'une liste déterministe dérivée de `months` (42 au total, 0 en août), qui inclut les dates de `hist`. Supprimer les paramètres inutilisés. Recalculer « plus longue série » (`build.py:373`). |
| DATA-3 | M | L'utilisateur conduit Noisy → Copernic L M J V à 7 h 50 (`build.py:380`, `577`) **et** est passager de Léa sur le même trajet, à la même heure, L J V (`build.py:714`, `733`). | L'utilisateur conduit le retour Copernic → Noisy à 17 h 45 L M J V, ou seulement le mardi. Mettre à jour la conversation et les stats en conséquence. |
| DATA-4 | M | `trajet.html` (trajet de Léa, ven. 26) : seulement Inès, 2 places, bouton « Demander à rejoindre », alors que l'utilisateur est membre et que Thomas a rejoint le vendredi. Toutes les cartes pointent vers `trajet.html` (`build.py:168`, `565`). | Résultat de recherche et détail = trajet d'un autre conducteur (Amina S., Copernic, 8 h 25). Ajouter des états `trajet.html#membre` (vue passager confirmé : Quitter, Messagerie) et `trajet.html#conducteur` (vue conducteur : demandes, Modifier, Annuler), dans PLAN. `trip(href=…)` par carte. |
| DATA-5 | M | La carte de Yanis affiche « Demande envoyée » et « Aucune demande en attente » (`pending=0`, `build.py:381`). | Pour une demande envoyée, remplacer la ligne des demandes en attente par « Réponse attendue sous 18 h » (paramètre `sent=True` dans `trip()`). |
| DATA-6 | M | CO₂ : `direction` « 3,9 t depuis la rentrée » (`build.py:930`) contre 1 310 kg en septembre (`build.py:961`). « Ta promo a évité 1,2 t » (`build.py:396`). | Direction : « 1,3 t en septembre » (ou « 3,9 t sur 6 mois »). Promo : environ 90 kg. Seuil de peak « < 5 trajets » (`build.py:922`) : passer à « < 10 » (règle d'anonymisation). |
| DATA-7 | m | Note de Léa : la répartition 31/6/1 (`build.py:441`) donne 4,79, alors que l'écran affiche 4,9. Diviseur 38 en dur. | Calculer la moyenne et le total depuis `dist` dans le helper, ou mettre 35/3/0 (4,92). |
| DATA-8 | m | Historique : le trajet du jeu. 18 sept. avec Léa a `given=5` (`build.py:644`), alors que `#anoter` demande encore de le noter. Le reçu et le donné semblent inversés sur cette ligne. Un trajet avec Léa le 12 sept. précède la création du trajet (15 sept., `build.py:713`). | Mettre `given=None` pour ce trajet (avec l'action « Noter »). Remettre le reçu et le donné dans le bon ordre. Déplacer la création au 8 sept. |
| DATA-9 | m | Voiture : « 4 places » (`build.py:539`) contre « 3 places passagers » (`build.py:833`). Stepper `data-max` à 4. | « 3 places passagers » partout, `data-max="3"`. |
| DATA-10 | m | « Tes 2 trajets à venir seront annulés » (`build.py:805`) au lieu de 3 plus une demande. Badge navigation « Signalements 4 » (`build.py:210`) contre « À traiter 3 ». | Aligner les compteurs (idéalement dérivés de constantes). |
| DATA-11 | m | La conversation « Copernic → Chelles » affiche Inès et un non-lu (`build.py:702`), alors que le trajet n'a ni passager ni demande. La conversation Bienvenüe → Torcy est en attente (voir CDC-5). | Mettre une seule personne (Toi) et « Aucun membre pour l'instant », ou ajouter Inès comme passagère acceptée sur la carte de Mes trajets. |
| DATA-12 | m | Recherche « triés par heure d'arrivée », mais ordre 8 h 20, 8 h 15, 8 h 25, 8 h 25 (`build.py:432-435`). | Réordonner (Hugo P. 8 h 15 en premier). |
| DATA-13 | m | Si D1 est refusée : `trip()` affiche « dont 0,19 € de commission » même quand `driver == "Toi"` (`build.py:176`). | Côté conducteur, afficher « Tu reçois {driver_share} / passager ». |
| DATA-14 | m | Noms et libellés incohérents. Zone « Noisy-Champs · RER A » (`build.py:946`) au lieu de « Gare RER A ». Initiales « MO » et « DI » (`build.py:203-204`). Le signalement « Copernic → Paris 13e » (`build.py:871`) sort des zones. Direction : la somme S34–S39 inclut août alors que le filtre est sur « Mois ». Créneaux types (`build.py:811`) : jeudi 9 h 45 et vendredi 12 h 30, alors que les trajets arrivent à 8 h 20 et 17 h 45. | Utiliser les libellés exacts de `ZONES_DEP` et `ZONES_CAMPUS`. Initiales KB et CV. Signalement vers une zone de la liste. Semaines de septembre (S36–S39). Aligner les créneaux sur les trajets. |
| DATA-15 | m | L'Historique révèle qui a donné quelle note (« Note reçue » à côté de « Avec », `build.py:662-663`), alors que les popups annoncent l'anonymat (`build.py:622`, `634`). | Supprimer la colonne « Note reçue » et garder seulement « Ta note donnée ». La moyenne reçue reste dans les stats. |
| DATA-16 | m | « tes notes moyennes » (`build.py:864`) : c'est une seule note par utilisateur. | Écrire « ta note moyenne ». |

---

## 5. Navigation, parcours, JS

| ID | G | Problème | Correctif |
|---|---|---|---|
| NAV-1 | M | « Se déconnecter » ne fait rien sur les pages statiques (GitHub Pages et import Figma). `app.js:157` appelle `navigate()`, qui s'arrête tout de suite sans `window.UMOB_render` (`app.js:201`). | Dans `navigate(href)` : `if (!window.UMOB_render) { location.href = href; return; }`. Garder le `loader()` avant la redirection. |
| NAV-2 | m | `trajet.html#signaler` : « Le compte de Léa » a `data-show="compte"` sans bloc `data-when` (`build.py:510`). | Deux blocs de motifs, `data-when="trajet"` et `data-when="compte"` (motifs différents). |
| NAV-3 | m | `#annuler-trajet` est la même popup pour le trajet régulier et le ponctuel du 1er oct. (`build.py:578`). | Ajouter une popup `annuler-trajet-ponctuel` et son ancre dans PLAN. |
| NAV-4 | m | « Modifier » un créneau ou une voiture (`build.py:812`, `833`) ouvre un formulaire d'ajout vide. « Modifier » un trajet renvoie vers Publier vierge (`build.py:577`). | Ajouter les états `profil.html#modifier-creneau`, `#modifier-voiture` (préremplis) et `publier.html#modifier` (prérempli, titre « Modifier le trajet », avertissement « les passagers seront prévenus »), dans PLAN. |
| NAV-5 | m | `app.js:156` : choisir un membre dans `#signaler-compte` désélectionne la conversation courante, parce que le script agit sur tous les `.li[data-conv]` de la page. | Limiter à `el.closest('.list')`. |
| NAV-6 | m | Aperçu : le routeur n'écoute pas `hashchange`. | `addEventListener('hashchange', () => navigate(location.hash))`, en évitant la boucle avec `history.replaceState`. |
| NAV-7 | m | États de §5 absents de `PLAN` : `messages.html#annuler`, `historique.html#noter-passagers`, `profil.html#voiture`, `mes-trajets.html#signaler-compte`. Les étapes de succès n'ont pas d'ancre. | Les ajouter à PLAN. `applyState()` : prendre en charge `#<modal>-ok`, qui ouvre la popup directement sur la dernière `[data-step]` (par ex. `trajet.html#demande-ok`). |
| NAV-8 | m | La cloche mène à Messages, y compris depuis Messages. Messages et Historique sont absents de la barre d'onglets mobile. Le retour du détail pointe toujours vers `recherche` (`build.py:443`). | Prévoir un écran ou une popup `#notifications` (CLAUDE.md §10). Mettre Messages dans la tabbar à la place de Publier, ou ajouter un bouton central « + ». Retour selon la provenance (`back=` par carte, ou `history.back()` en statique). |
| NAV-9 | m | `#m-supprimer-compte` : en rouvrant la popup, le champ garde « SUPPRIMER » et le bouton reste actif. | Réinitialiser à l'ouverture dans `openModal()`, en revenant à `[data-step]` 1 et en vidant les champs. |

---

## 6. Code et charte

| ID | G | Problème | Correctif |
|---|---|---|---|
| CODE-1 | m | Rôles dans l'Historique : `.badge.drv` (orange, voiture) et `.badge.line` (`build.py:659`), au lieu de `role_tag()`. CLAUDE.md §7 se contredit : « rôle Conducteur orange (.badge.drv) » et « turquoise = conducteur ». | Utiliser `role_tag("d"/"p")`. Supprimer `.badge.drv` s'il n'est plus utilisé. Corriger CLAUDE.md : un seul code rôle (volant turquoise, siège magenta). Envisager de changer la couleur de `.badge.reg`, qui est aussi turquoise. |
| CODE-2 | m | Pastilles de stats : `.stat.dark .k svg` force le jaune (`styles.css:374`). `ticket` sert à « Frais partagés » (`build.py:672`). | Dans `.stat.dark`, garder la teinte du type (couleur `-soft` sur fond translucide). `ticket` reste réservé à « trajets passager » (sans objet si D1 est acceptée). |
| CODE-3 | m | Popups récupérées en découpant du HTML : `x.split(...)[0] and (...)` (`build.py:693`, `751`). | Une constante par popup (`M_ANNULER`, `M_NOTER_PASSAGERS`, `M_SIGNALER_COMPTE`…), réutilisée par les pages. |
| CODE-4 | m | Le tracé de l'étoile existe trois fois (`P["star"]`, `STAR_SVG`, `stars5`). `driver_share()` relit la chaîne « 2,50 € ». Il y a `rows.replace(...)` pour injecter un style (`build.py:690`). `import re, zlib` est au milieu du fichier (`build.py:1032`). `color_avatars()` retire les classes `b` et `l`, donc `.avatar.b/.l` (`styles.css:274-275`) et `av="b"` sont morts. | Garder un seul tracé d'étoile, passer des prix numériques, faire un paramètre au lieu du `replace`, remonter les imports en tête, supprimer le code mort. |
| CODE-5 | m | 68 `style="…"` en ligne (`gap:6px` ×12, `color:var(--danger)` ×5, `font-weight:400` ×6…). | Créer des classes utilitaires (`.gap-6`, `.iconbtn.danger`, `.fw-400` ou `.opt-label`) et les remplacer. |
| CODE-6 | m | CSS mort. Les classes `.progress`, `.skeleton`, `.section-title` et `.trip.clickable` ne servent pas (`.progress` et `.skeleton` resserviront avec CDC-11 et CDC-12). Les tokens `--brand-soft-2`, `--warning`, `--success-fill` et `--c-vert` ne sont pas utilisés. `--c-nuit-ink` manque. | Supprimer ce qui ne sert pas après les autres lots. Ajouter `--c-nuit-ink`. |
| CODE-7 | m | JS fragile. `tick()` tourne en boucle à chaque image même quand le loader est caché (`app.js:40-46`). « Envoi… » s'affiche pour toutes les actions (`app.js:131`). `activateTab` plante si le premier `[data-tab]` est hors de `[data-tabs]`. | Lancer et arrêter `requestAnimationFrame` dans `loader()`. Utiliser `data-loading="…"` par bouton. Ajouter une garde dans `activateTab`. |
| CODE-8 | m | `dist/` n'est jamais nettoyé : il contient encore `dist/assets/fonts/outfit-*`. `uge-logo.svg`, `uge-symbole.svg` et `u-mobility-loader.svg` sont copiés sans être utilisés. | `shutil.rmtree(EXPORT, ignore_errors=True)` au début du build. Copier seulement les assets référencés, ou le documenter. |
| CODE-9 | m | Couleurs hors `:root` et hors charte dans `styles.css` : `#eeedf7` (94), `#3a3590` (98), `#00654a` (172), `#c9ecd8` (376), `#e6e7ea` (456), `rgba(47,42,133,.14)` (458), `#7fd3b6` (524, vert menthe **hors charte**), `#f7f7fb` (534), plus celles de `SHELL_CSS`. | En faire des tokens (`--sidebar-me`, `--brand-press`, `--success-hover`, `--map-bg`, `--brand-ring`…) dérivés de la palette officielle. `#7fd3b6` et `#c9ecd8` deviennent `--c-vertclair` et `--c-vertclair-soft`. Régénérer la charte. |

---

## 7. Écriture

| ID | G | Problème | Correctif |
|---|---|---|---|
| TXT-1 | m | Heures en « 18:02 », « 20:14 », « 20:20 » (`build.py:716`, `721`, `722`) et « 7h … 19h » (`build.py:914`). | « 18 h 02 », « 7 h ». |
| TXT-2 | m | Espaces ordinaires dans « 7 h 50 », « 2,50 € », « ? », « ! », « : » (environ 30 cas) : coupures « 7 h / 50 » en mobile. | Helper `nb(s)` qui remplace l'espace par U+202F (fine) avant `? ! ; :` et par U+00A0 dans « 7 h 50 » et « 2,50 € ». L'appliquer dans `trip()` et aux textes libres (ou en post-traitement du HTML hors balises). |
| TXT-3 | m | Vocabulaire. « réservation » (`build.py:795`, PLAN 973) contre « demande ». « Demandes à traiter » (index) contre « Demandes reçues » (Mes trajets). « Participation » désigne tantôt le prix, tantôt la part reversée (`build.py:483`, `501`, `538`). | Utiliser « demande » partout. Choisir une seule étiquette pour les demandes reçues. Le point « Participation » est sans objet si D1 est acceptée, sinon dire « Prix par passager » et « Part reversée au conducteur ». |
| TXT-4 | m | Le trajet de Yanis (demande en attente) est rangé dans « prochains trajets » sur le tableau de bord, mais seulement dans « envoyées » dans Mes trajets. Le badge « Mes trajets 3 » ne dit pas ce qu'il compte. | Même classement partout. Badge avec un texte `sr-only` et une infobulle « 3 demandes à traiter ». |
| TXT-5 | m | L'Historique annonce 42 trajets et en montre 7, sans pagination. | Ajouter « Voir plus » ou une pagination, et un libellé « 7 sur 42 ». |
| TXT-6 | m | Apostrophes droites (environ 100). | U+2019 dans les textes (pas dans les attributs techniques). Optionnel. |

---

## 8. Ordre d'exécution conseillé (après les décisions)

1. **Lot 1, rapide et sans décision :** DATA-1 (si D4 est tranchée), DATA-2, DATA-3, DATA-5, NAV-1, A11Y-1, RWD-11, RWD-12, DATA-7 à DATA-12, DATA-14 à DATA-16, TXT-1.
2. **Lot 2, responsive :** correctif de fond (`.field`, palier 1280, conteneur `.trip`), puis RWD-1 à RWD-8, RWD-13, et le reste des RWD.
3. **Lot 3, cahier des charges :** CDC-1, CDC-3, CDC-2, CDC-6, CDC-7, CDC-11, CDC-15, CDC-5, CDC-4, CDC-8, CDC-9, CDC-16.
4. **Lot 4, accessibilité des composants :** `.sr-only`, puis A11Y-4, 5, 6 (popups et annonces), 2, 3, 7, 8, 9, 11, 13, 15, 16, 17, et le reste.
5. **Lot 5, nouveaux écrans :** CDC-12, CDC-13, CDC-14, CDC-10, DATA-4, NAV-3, NAV-4, NAV-7, NAV-8.
6. **Lot 6, nettoyage :** CODE-*, TXT-2 à TXT-6, RWD-10 (rem), mise à jour de CLAUDE.md (§1, §5, §7, §9, §10), régénération de la charte.

**Vérification après chaque lot :**
- `python3 src/build.py` ;
- servir `dist/` et relancer `docs/audit/scripts/audit.py` (débordements, 10 largeurs, **dont 901, 1024, 1100**), `run_axe.py` et `kbd.py` ;
- regarder les captures à 390, 1024 et 1440 ;
- aucune nouvelle violation axe et aucun débordement ne doivent apparaître.
