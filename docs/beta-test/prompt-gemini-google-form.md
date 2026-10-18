# Prompt Gemini : questionnaire du bêta-test U-Mobility

À coller tel quel dans Gemini. Il produit les questions du Google Form et un script Apps Script qui crée le formulaire.
Formulaire en ligne : https://forms.gle/WMSWoxK83A2rpWDDA (constante `BETA_FORM` dans `src/build.py`), ouvert par le bouton jaune « Donner mon avis » de la barre de démo, présent sur toutes les pages (masqué avec `?figma`).

---

```text
Tu es chercheur UX. Rédige le questionnaire Google Forms du bêta-test d'une maquette.

## Produit
U-Mobility : covoiturage et mobilité durable pour les étudiants et personnels de l'Université Gustave Eiffel (campus Cité Descartes). Projet de BUT Informatique. Objectif : faciliter les trajets vers le campus et mesurer l'impact mobilité.
On teste une maquette cliquable (ordinateur et mobile), données fictives, rôles utilisateur / modérateur / administrateur.

## Contenu de la maquette
- Tableau de bord : trajets à venir (conducteur ou passager), trajets à noter, CO₂ évité, régularité.
- Recherche par zones prédéfinies (pas de géolocalisation), jour, heure, mode, tags.
- 4 modes avec chacun sa couleur : voiture (seul mode avec prix et places, sans commission), vélo, à pied, transports.
- Détail d'un trajet (ponctuel ou régulier, 0 à 2 arrêts) et demande pour le rejoindre.
- Publier un trajet : mode, arrêts, jours, places, prix, 5 tags au plus parmi 16.
- Mes trajets, vue conducteur (accepter / refuser les demandes), historique, notes 5 étoiles sans avis écrit.
- Messagerie par trajet avec bouton Signaler ; modération des signalements ; back office de statistiques anonymisées.
- Profil : campus, zone, créneaux, préférences, modes ; page RGPD.
- Design : charte officielle de l'Université Gustave Eiffel (bleu #2F2A85, couleurs secondaires pour modes, rôles et statuts).
- Pas encore fait : carte des zones de rendez-vous, challenges avec classement anonymisé, badges, export du bilan mensuel, notifications, suggestion automatique de trajets.

## Sections du formulaire
1. Introduction : but, durée (10 min), anonymat, case de consentement obligatoire.
2. Profil : statut, campus, mode de transport actuel, fréquence, déjà covoituré (logique conditionnelle), appareil utilisé. Ni nom ni e-mail obligatoire.
3. Scénarios : 5 tâches concrètes (trouver un trajet depuis Noisy-Champs lundi 8 h et demander à le rejoindre ; publier un trajet régulier à vélo avec un arrêt ; accepter une demande ; noter un conducteur ; signaler un membre). Pour chacune : réussie / avec difficulté / pas réussie, difficulté 1 à 5, « Où as-tu bloqué ? » (facultatif).
4. Utilisabilité : SUS en français, 10 items, 1 à 5.
5. Fonctionnalités : grille d'utilité des fonctionnalités existantes (inutile → indispensable) ; top 3 des fonctionnalités à ajouter parmi « pas encore fait » + Autre ; ce qui manque pour l'utiliser vraiment ; ce qui est inutile ou trop compliqué ; ce qui rassurerait pour voyager avec un inconnu ; freins à l'usage.
6. Design : 3 adjectifs au plus parmi une liste équilibrée (positifs et négatifs) ; échelles de lisibilité, navigation, esthétique, cohérence avec l'identité de l'université ; compris sans explication ? (couleurs des modes, conducteur / passager, icônes, tags, statuts) ; confort sur mobile ; difficulté de lecture ou de contraste ; écran préféré et écran le moins aimé.
7. Bilan : utiliserais-tu U-Mobility et à quelle fréquence ; NPS 0 à 10 ; une chose à garder ; une chose à changer ; commentaire libre ; e-mail facultatif pour un entretien.

## Règles
- Français, tutoiement, pas d'emoji, vocabulaire simple.
- Questions neutres, une idée par question.
- 35 questions au plus, surtout fermées, ouvertes facultatives.
- Échelles libellées aux deux bornes (1 = négatif), option « Je n'ai pas testé » si utile.
- RGPD : minimisation, anonymat par défaut.

## Format de sortie
1. Par section : titre, description, puis tableau (n°, question, type Google Forms, options ou bornes, obligatoire, ce qui est mesuré).
2. Les règles de logique conditionnelle.
3. Un script Google Apps Script (FormApp) complet qui crée le formulaire, prêt à exécuter.
4. 5 conseils pour analyser les réponses (score SUS, NPS, taux de réussite, réponses ouvertes).
```
