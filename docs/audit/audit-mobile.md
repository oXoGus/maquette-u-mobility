# Audit mobile : ce qui est caché en bas de page

*12 novembre 2026. Captures Playwright en 390 × 844 px. La partie visible fait environ 700 px entre la barre du haut et la barre d'onglets.*

Règle de départ : **l'utilisateur ne pense pas toujours à faire défiler**. Sur chaque écran mobile, l'action principale et les tâches en attente doivent donc se voir sans défiler. Le tableau donne la position verticale de chaque élément, avant et après correction. Un ✓ veut dire visible dans le premier écran.

| Écran | Élément | Avant | Après | Correction |
|---|---|---|---|---|
| Messagerie | conversation | 516 px, sous la liste | ✓ dès l'ouverture | Deux étapes : d'abord la liste seule, puis la conversation seule (dernier message et saisie à l'écran). Les membres, « Signaler » et « Quitter » passent dans une popup. |
| Messagerie | membres du trajet | 1 458 px | ✓ icône en haut à droite | Popup `#membres` (et bouton « Membres » jusqu'à 1 280 px). |
| Détail d'un trajet | « Demander à rejoindre » | 1 977 px (à pied : 1 528) | ✓ 723 px, toujours visible | Barre d'action collée au-dessus des onglets, avec le prix ou « Gratuit ». |
| Détail (place confirmée, vélo) | « Messagerie du trajet » | 1 983 px | ✓ 723 px | Même barre. |
| Mon trajet (conducteur) | demandes en attente | 1 219 px (à pied : 910) | ✓ 138 px (à pied : 168) | Les demandes passent en tête. Accepter / Refuser à 439 px. |
| Mon trajet | Messagerie, Modifier | 2 188 px | ✓ 723 px | Barre d'action collée. |
| Recherche | 1er résultat | ~980 px | ✓ 304 px | Le formulaire se replie en un résumé (« Mont d'Est → Copernic · ven. 26 sept. ») avec « Modifier ». Il se replie aussi après « Rechercher ». |
| Publier | « Publier le trajet » | 2 640 px | ✓ 723 px | Pied du formulaire collé en bas tant que le formulaire est à l'écran. |
| Profil | ta fiche, « Se déconnecter » | 4 374 / 4 579 px | ✓ 100 / 217 px | Fiche en tête, compacte. Chaque section se replie avec un résumé d'une ligne. La page passe de 4 929 à 994 px. |
| Mes trajets | « Mes demandes » | 2 713 px | ✓ raccourci à 216 px | Bandeau « 2 demandes en attente » qui fait défiler jusqu'à la section. Les filtres tiennent sur une ligne qui défile (ils prenaient 3 lignes). |
| Historique | bouton « Noter » du tableau | caché à droite | ✓ | Le tableau devient une liste de cartes en mobile. |
| Signalements | statut et date | cachés à droite | ✓ 1er signalement à 535 px | Tableau en cartes et filtres sur une ligne. |
| Profil > Horaires types | modifier / supprimer | à droite | ✓ | Tableau en cartes. |
| Mes données | sommaire | absent en mobile | ✓ ~580 px | Puces numérotées sous le bandeau. |
| Accueil | « Trajets à noter » | 2 114 px | 1 358 px | 2 trajets à venir en mobile, plus un lien vers les autres. Dans le bandeau, « 2 passagers attendent ta réponse » est maintenant un lien. |

Écrans sans problème : Historique (« À noter » déjà en tête), Back office (tableau de bord), Connexion, Compte suspendu.

Aucun débordement horizontal en 390, 1 024 et 1 440 px. L'affichage ordinateur ne change pas, sauf la messagerie entre 901 et 1 280 px : la colonne des membres, qui passait sous la conversation, est remplacée par le bouton « Membres ».

## Aperçu (artifact)

Le cadre « Mobile » de `preview.html` utilisait `overflow: hidden`, ce qui empêchait les barres de rester collées : la barre d'onglets n'apparaissait qu'en bas de la page. Il est maintenant en `overflow: clip`, donc les onglets, la barre d'action et la zone de saisie se comportent comme sur un téléphone. En mode Mobile, la barre de démo est compacte pour ne pas couvrir le téléphone.

## Reste à voir

- **Accueil** : « Trajets à noter » reste dans le deuxième écran. Si les notes comptent beaucoup (pour la note moyenne des conducteurs), on peut ajouter un bandeau « 2 trajets à noter » sous le bandeau d'accueil.
- **Tablette (901–1 100 px)** : les colonnes s'empilent, donc les actions du détail d'un trajet repassent en bas (« Demander à rejoindre » à 1 622 px en 1 024). La barre d'action collée n'existe qu'en mobile, parce qu'elle s'appuie sur la barre d'onglets.
- **Publier** reste un long formulaire (3 300 px). Le bouton est maintenant toujours visible ; un découpage en étapes serait une évolution plus large.
