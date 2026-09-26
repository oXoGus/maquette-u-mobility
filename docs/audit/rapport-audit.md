# Audit de la maquette U-Mobility

*25 septembre 2026. Audit du commit `0416f3b` (V2).*

J'ai analysé la maquette selon quatre axes, en parallèle :

1. la conformité au cahier des charges SAÉ BUT3 ;
2. le responsive, testé automatiquement sur 34 écrans et états, chacun à 10 largeurs de 320 à 1920 px ;
3. l'accessibilité : axe-core, tests au clavier, contrastes, WCAG 2.2 AA ;
4. la cohérence générale : données de démo, liens, code, textes.

Je n'ai modifié aucun fichier de la maquette. Les détails techniques pour corriger sont dans [`corrections-pour-claude.md`](corrections-pour-claude.md).

---

## En bref

| Axe | État | À retenir |
|---|---|---|
| Cahier des charges | **À revoir** | Le **prix et la commission de 0,19 €** contredisent le cdc : « paiement ou partage de frais réel » y est **hors périmètre**. Il manque aussi les badges et challenges, la carte des zones, les états d'erreur et le masquage de trajet côté back-office (critère d'acceptation n° 3). |
| Responsive | **Bien en mobile, cassé entre 901 et 1280 px** | Le téléphone (320–899 px) et le grand écran (≥ 1280 px) sont propres. Sur tablette et petit portable, la barre latérale apparaît et **Messages, Recherche, Publier, Trajet et Profil se tassent** : texte un mot par ligne, colonnes qui se chevauchent. Les popups ne passent pas non plus en mode mobile. |
| Accessibilité | **Moyenne** | Les contrastes de texte sont bons partout. En revanche, **plusieurs écrans sont inutilisables au clavier** : les signalements en modération, le choix d'une conversation, la personne à signaler. Le **focus est invisible sur les fonds bleus**, et les composants maison (listes, onglets, étoiles, puces) ne donnent pas leur état aux lecteurs d'écran. |
| Cohérence | **Quelques erreurs visibles** | Les **jours de la semaine sont décalés d'un jour** : ce sont ceux de 2025, alors que la démo est en 2026. La heatmap annonce 123 trajets contre 42 partout ailleurs. **« Se déconnecter » ne marche pas** sur le site publié. |

---

## 1. Contradictions avec le cahier des charges

### Vraies contradictions

**1. Prix et commission : bloquant.**
Le cdc (§4, hors périmètre) exclut « Paiement ou partage de frais réel. Responsabilité contractuelle sur les trajets. » La maquette affiche pourtant un prix sur chaque carte, « dont 0,19 € de commission », un récapitulatif « part reversée au conducteur », un champ prix dans Publier, une stat « Frais partagés 96 € », un tri par prix et un motif de signalement « Tarif abusif ». Une commission fait d'U-Mobility un intermédiaire commercial, ce qui touche aussi la responsabilité contractuelle.
- **Recommandation :** retirer tout montant. Ce qui compte pour le cdc, c'est l'impact (CO₂, régularité), pas l'argent. Au pire, une phrase « Participation éventuelle à convenir entre vous, non gérée par U-Mobility ».
- **À faire valider :** c'était une décision de ta part, donc à confirmer avec l'enseignant.

**2. Voiture uniquement, sans modes : majeur.**
Le cdc parle de « transports, vélo, marche, covoiturage » (§1) et le modèle de données prévoit `MobilityProfile.modes` (§6). Ne proposer que du covoiturage en voiture reste défendable. En revanche, le profil devrait avoir un champ « Mes modes de déplacement » pour les statistiques.

**3. Campus : majeur.**
Le cdc veut un champ **campus** dans le profil et sur l'utilisateur (§5 et §6). La maquette appelle « campus » quatre bâtiments de la Cité Descartes. Il faut séparer :
- le **campus** (Marne-la-Vallée, Paris, Lille…) ;
- le **point d'arrivée** (Copernic, Bienvenüe…).

**4. Rôles « Modérateur » et « Direction » au lieu d'un back-office administrateur : à arbitrer.**
Le cdc parle d'**administrateurs** et d'un **back-office** qui regroupe modération, signalements et statistiques. Il cite aussi les **associations et services campus**, qui animent les challenges, comme utilisateurs cibles. La maquette n'a aucun rôle association.

**5. Messagerie pas assez « limitée » : majeur.**
Beaucoup est déjà bien fait : 300 caractères, numéros et liens masqués, fermeture 24 h après le trajet. Mais une conversation existe pour une demande **encore en attente** (Bienvenüe → Torcy), ce qui contredit ton propre texte « tu rejoindras la messagerie après acceptation ». Il manque aussi « Signaler ce message » sur chaque bulle.

**6. Détails de contexte : mineur.**
- **Année et groupe :** le cdc dit BUT3 et groupe de 6, alors que la maquette et CLAUDE.md disent « BUT Informatique · 2e année ».
- **Données réelles :** le profil utilise ton vrai nom et un e-mail `@edu.univ-eiffel.fr`, alors que le cdc exige des **données fictives**.
- **Public :** « Covoiturage étudiant » exclut les **personnels**, qui sont pourtant ciblés. Il vaut mieux dire « covoiturage universitaire ».
- **Matching :** le cdc demande de « scorer les résultats » (§14). Sans remettre de pourcentage, un tri « Meilleure correspondance » avec un badge « Très compatible » ferait l'affaire.

### Ce qui manque

| Manque | Gravité | Référence cdc |
|---|---|---|
| **Régularité** dans le tableau de bord (seulement « plus longue série ») | Majeur | §5 MVP |
| **Masquer un trajet** depuis le back-office : aujourd'hui un simple toast, sans dossier de signalement de trajet ni état « trajet masqué » côté utilisateur | **Majeur (critère d'acceptation)** | §13 |
| **Statistiques cohérentes avec les données** (voir §4 plus bas) | **Majeur (critère d'acceptation)** | §13 |
| **Badges et challenges** avec classement anonymisé | Majeur | §2.1, §4 avancé |
| **Carte des zones de rendez-vous** | Majeur | §4 avancé |
| **États d'erreur** : mauvais mot de passe, formulaire invalide, aucun résultat, trajet complet, erreur réseau, accès refusé, vraie page 404 | Majeur | §7 robustesse et ergonomie |
| **Information RGPD** : politique de confidentialité, qui voit quoi | Majeur | §7 |
| Écran d'**export du bilan mensuel** (le bouton existe, sans écran) | Mineur | §4 avancé |
| Statuts de demande **Refusée / Expirée / Complet** | Mineur | §6 TripRequest |
| Badge « profil vérifié » visible partout (seulement sur Léa) | Mineur | §2.1 |
| Mention « U-Mobility met en relation, sans responsabilité » | Mineur | §4 hors périmètre |
| Onboarding du profil mobilité | Mineur | §5 |
| Recherche « Régulier » : on ne peut pas choisir les jours | Mineur | §5 |

### Ce qui est conforme

- Zones approximatives sans géolocalisation.
- Trajets réguliers et ponctuels.
- Demande avec acceptation ou refus.
- Historique avec CO₂.
- Signalement et page de modération.
- Identité révélée seulement en consultation journalisée.
- Statistiques de direction avec un seuil de 10 personnes.
- Export et suppression RGPD.
- Versions ordinateur et mobile.
- Comptes de démo par rôle.

---

## 2. Responsive

**Ce qui va bien :**
- aucun défilement horizontal de la page, quelle que soit la largeur (y compris 320 px et le zoom à 200 %) ;
- la version mobile est propre sur tous les écrans ;
- `.hide-m` et `.hide-d` sont corrects ;
- la bascule Mobile de l'aperçu fonctionne.

**Le vrai problème : l'intervalle 901–1280 px** (tablette paysage, petit portable).
À 901 px, la barre latérale de 256 px apparaît. Il reste environ 600 px pour des grilles pensées pour 1 200 px.

| Écran | Ce qu'on voit | Gravité |
|---|---|---|
| Messages | La colonne de discussion fait 48 à 190 px de large, avec des bulles d'un mot par ligne et un champ de saisie de 28 px | **Bloquant** |
| Recherche, Tableau de bord | Sur les cartes de trajet, « Noisy- / le- / Grand » s'affiche un mot par ligne, sous les avatars | **Bloquant** |
| Recherche (barre de filtres) | Les listes Départ et Arrivée débordent sur la date | **Bloquant** |
| Publier | Heures tronquées (« 7 h 5 »), champs qui se chevauchent | Majeur |
| Trajet, Profil | Indicateurs écrasés, tableau des créneaux serré | Majeur |

**En mobile, les popups ne suivent pas.** Elles sont hors du cadre responsive, donc les règles mobiles ne s'y appliquent pas :
- dans « Noter les passagers », les étoiles recouvrent les noms (**bloquant**) ;
- les marges restent celles de l'ordinateur ;
- Prénom et Nom restent sur 2 colonnes.

**Autres points :**
- **Cibles tactiles sous 44 px** (ta règle) : puces à 32 px, petits boutons à 36 px, étoiles, jours, interrupteurs, croix de retrait d'un tag à 18 px.
- **Polices en px :** augmenter la taille du texte dans le navigateur ne change rien.
- **Barre d'onglets mobile non fixe :** c'est voulu pour Figma, mais pour la vraie appli il faudra la coller en bas.
- **`preview.html` sans `<meta charset>` :** hors artifact, les accents sont cassés.
- **Petits défauts :**
  - libellés de mois collés dans la heatmap (« marsavr. ») ;
  - « 7 h 50 » coupé en fin de ligne (il faut des espaces insécables) ;
  - onglets de Mes trajets sur 2 lignes à 320 px ;
  - contenu collé à gauche en 1920 px.

---

## 3. Accessibilité

**Ce qui est bien :**
- **tous les contrastes de texte passent l'AA** : 80 paires de couleurs vérifiées, le minimum est à 4,6:1 ;
- `lang="fr"`, titres de page uniques ;
- icônes décoratives cachées, boutons-icônes nommés ;
- tous les champs ont un libellé ;
- Échap ferme les popups ;
- `prefers-reduced-motion` est respecté ;
- les statuts combinent couleur, mot et icône.

axe-core ne trouve que 50 erreurs. Les vrais problèmes sont apparus aux **tests clavier** :

**Bloquants :**
1. **Focus invisible sur le bleu :** l'anneau de focus est bleu sur fond bleu (contraste 1:1). C'est le cas dans la barre latérale, le bandeau d'accueil et la barre mobile.
2. **Modération :** les lignes de signalement ne s'ouvrent qu'à la souris.
3. **Messages :** on ne peut pas choisir une conversation au clavier, ni la personne à signaler.

**Majeurs :**
- **Popups :** pas de nom, le Tab sort de la popup vers la page derrière, et à la fermeture le focus est perdu.
- **Annonces vocales :** les toasts et le passage à l'étape « succès » ne sont pas annoncés au lecteur d'écran.
- **Composants maison** : listes déroulantes, onglets de Mes trajets, puces, jours, étoiles. Ils changent de couleur sans exposer leur état (sélectionné, coché), et les flèches du clavier ne marchent pas.
- **Cartes de trajet :** le lecteur d'écran lit seulement « Voir le détail du trajet X vers Y ». Date, heure, places et statut ne sont pas lus.
- **Graphiques :** heatmap et graphiques sans équivalent texte, infobulles à la souris seulement.
- **En mobile et au zoom 200 % :**
  - le titre `<h1>` disparaît ;
  - les boutons Semaine / Mois / Exporter de la page Direction disparaissent ;
  - les comptes **modérateur et direction n'ont plus aucune navigation ni déconnexion**.
- **Navigation et formulaires :**
  - pas de lien « Aller au contenu » ;
  - contours des champs trop pâles (1,3:1 au lieu de 3:1) ;
  - bouton « Envoyer » sans nom en mobile ;
  - pas d'`autocomplete` sur la connexion et le profil.

**Mineurs :** hiérarchie des titres, landmarks, tableaux, stepper, tags, cibles < 44 px, titre de l'aperçu qui reste toujours « U-Mobility ».

---

## 4. Cohérence de la maquette

**Erreurs visibles tout de suite :**
- **Les jours de semaine sont ceux de 2025.** Le 25 sept. 2026 est un **vendredi**, pas un jeudi ; « Ven. 26 sept. » est un samedi. La heatmap, elle, utilise le vrai calendrier 2026 : elle dit « aucun trajet le sam. 12 sept. » alors que l'Historique liste « Ven. 12 sept. ».
- **Heatmap : 123 trajets** contre **42** dans les stats et l'Historique. Elle a aussi des trajets en août alors que la distance d'août est de 0 km.
- **« Se déconnecter » ne fait rien** sur le site publié (GitHub Pages) : ça ne marche que dans l'aperçu.
- **Tu conduis ET tu es passager de Léa** sur le même trajet, à la même heure.
- **Détail du trajet :** le trajet de Léa y apparaît comme si tu n'en faisais pas partie (bouton « Demander à rejoindre »), alors que tu y as une place.
- **Carte de Yanis :** elle affiche « Demande envoyée » et « Aucune demande en attente ».

**Autres incohérences :**
- **CO₂ :** « 3,9 t depuis la rentrée » côté Direction, alors que septembre = 1,3 t. « Ta promo a évité 1,2 t » représenterait presque toute l'université.
- **Note de Léa :** sa répartition donne 4,79, alors que l'écran affiche 4,9.
- **Voiture :** « 4 places » dans Publier, « 3 places » dans Profil.
- **Compteurs :** « 2 trajets à venir » au lieu de 3, badge Signalements à 4 pour 3 à traiter.
- **Rôles :** l'Historique utilise des couleurs différentes du reste (orange « voiture » au lieu de volant turquoise / siège magenta).
- **Anonymat des notes :** l'Historique affiche « Note reçue » à côté de « Avec », donc on sait qui t'a donné quelle note.
- **Formats :** « 18:02 » dans la messagerie au lieu de « 18 h 02 », « 7h » dans Direction.
- **Vocabulaire :** « réservation » et « demande », « participation » pour deux choses différentes.
- **Boutons « Modifier »** qui ouvrent un formulaire d'ajout vide.
- **Plan :** 4 états de §5 absents du `PLAN` (import Figma).

**Charte UGE :**
- **Logotype :** bien utilisé (taille, zone de protection).
- **Couleurs :** 6 couleurs codées en dur hors palette, dont un vert menthe `#7fd3b6`.

**Code :**
- pas d'erreur JS, aucun lien cassé, HTML bien imbriqué ;
- un peu de CSS mort ;
- 68 styles en ligne ;
- `dist/` jamais nettoyé : il contient encore les anciennes polices Outfit.

---

## 5. Décisions à prendre avant de corriger

Ces points changent des choix que tu avais faits, donc c'est à toi de trancher. Idéalement, montre-les à l'enseignant à la soutenance d'octobre.

1. **Prix et commission :** supprimer entièrement (recommandé), ou garder une mention « participation à convenir, non gérée » ?
2. **Modes de déplacement :** ajouter un champ « modes » au profil pour les stats, tout en gardant la publication en voiture seule (recommandé) ?
3. **Rôles :** fusionner modérateur et direction en un **back-office administrateur**, et ajouter un rôle **association** pour les challenges ?
4. **Dates de démo :** passer toute la démo en 2025, ou décaler les libellés pour coller à 2026 (recommandé, puisque le projet démarre le 26/09/2026) ?
5. **Score de compatibilité :** accepter un badge qualitatif et un tri « meilleure correspondance », sans pourcentage ?
6. **Réponses rapides dans la messagerie :** c'est la façon la plus simple de montrer une messagerie « limitée », mais tu les avais refusées.
7. **Barre d'onglets mobile fixe** (vraie appli) ou non fixe (import Figma) ?
8. **Persona fictif** à la place de ton vrai nom et e-mail ?

## 6. Ordre de correction conseillé

1. **Rapides et visibles :**
   - dates 2026 ;
   - heatmap à 42 trajets ;
   - déconnexion ;
   - trajet conducteur / passager en double ;
   - focus sur fond bleu ;
   - `meta charset` de l'aperçu.
2. **Responsive :**
   - palier 901–1280 px ;
   - popups en mobile ;
   - cibles de 44 px.
3. **Cahier des charges** (après tes décisions) :
   - prix ;
   - campus et modes ;
   - régularité ;
   - masquer un trajet ;
   - états d'erreur ;
   - RGPD.
4. **Accessibilité des composants :**
   - popups ;
   - listes ;
   - onglets ;
   - puces et étoiles ;
   - cartes ;
   - clavier en modération et dans Messages.
5. **Nouveaux écrans :** challenges et badges, carte des zones, export du bilan.
6. **Finitions :**
   - formats ;
   - vocabulaire ;
   - CSS mort ;
   - mise à jour de CLAUDE.md et régénération de la charte.
