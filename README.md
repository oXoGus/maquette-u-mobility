# U-Mobility — maquette interactive

Maquette de l'application de covoiturage étudiant de l'Université Gustave Eiffel (SAÉ BUT Informatique). 12 écrans et leurs popups, en version ordinateur et mobile, avec la charte graphique officielle de l'université.

- **Charte officielle de l'université (source du design)** : [`docs/Charte_Gustave_Eiffel_V2-4.pdf`](docs/Charte_Gustave_Eiffel_V2-4.pdf)
- **Charte graphique du projet** : [`docs/charte-graphique-u-mobility.pdf`](docs/charte-graphique-u-mobility.pdf)
- **Contexte complet** (pour Claude Code ou un nouveau développeur) : [`CLAUDE.md`](CLAUDE.md)
- **Product Backlog** : [`docs/product-backlog-initial.xlsx`](docs/product-backlog-initial.xlsx)

## Lancer en local

Avec Docker :

```bash
docker compose -f docker-compose.dev.yml up --build
# → http://localhost:8080 (modifie src/, recharge la page)
```

Sans Docker (Python 3.10+) :

```bash
python3 scripts/dev.py
# → http://localhost:8080
```

Générer le site une fois : `python3 src/build.py` → `dist/`.

## Mise en ligne (GitHub Pages)

1. Pousser le dépôt sur GitHub.
2. Settings → Pages → Build and deployment → Source : **GitHub Actions**.
3. Chaque push sur `main` reconstruit et publie le site (`.github/workflows/deploy.yml`).
   Le lien s'affiche dans l'onglet Actions : `https://<compte>.github.io/<dépôt>/`.

## Importer dans Figma

Plugin **html.to.design** → onglet **Web** → coller l'URL d'une page → Viewports `1440` et `390` → Import.
Les popups et onglets s'ouvrent avec une ancre (ex. `trajet.html#demande`) : la liste complète est sur `plan.html`.

## Structure

| Dossier | Contenu |
|---|---|
| `src/` | générateur (`build.py`), styles, interactions, logos, polices |
| `dist/` | site généré (non versionné) |
| `scripts/` | serveur de dev, génération de la charte PDF |
| `docs/` | charte officielle UGE V2.4 (PDF source), charte du projet, backlog, design system |
