# Palette officielle — charte Université Gustave Eiffel V2.4

Source : page 7 de `docs/Charte_Gustave_Eiffel_V2-4.pdf`. Les valeurs officielles ne sont jamais modifiées ; l'interface y ajoute seulement des teintes claires (`*-soft`) et deux variantes assombries pour que le texte atteigne le niveau AA (voir plus bas). Les tokens correspondants sont dans `tokens.json` et dans le bloc `:root` de `src/styles.css`.

Les 5 pistes de couleurs étudiées auparavant (et l'ancienne « piste officielle » indigo #282F7A et lavande #535995, relevée à tort sur une image de couverture) sont abandonnées : il n'y a plus qu'un seul thème.

## Couleur principale

| Nom | Hex | Pantone | CMJN | RVB | Token |
| --- | --- | --- | --- | --- | --- |
| Bleu UGE | `#2F2A85` | 2746C | 100 · 98 · 0 · 0 | 47 · 42 · 133 | `brand` |

Le bleu est la couleur dominante : barre latérale, en-tête mobile, bandeaux d'accueil, bouton principal, liens, onglet actif, logo. Texte blanc dessus (11,73:1).

Teintes dérivées pour l'interface : `brand-hover` #231F66 (survol), `brand-soft` #EBEAF4 et `brand-soft-2` #DCDAEC (fonds teintés), `on-brand-muted` #D6D5EA (texte secondaire sur le bleu), heatmap #EBEAF4 → #C5C3E0 → #8D89C2 → #5B56A3 → #2F2A85.

## Couleurs secondaires

| Nom | Hex | CMJN | RVB | Dans l'interface |
| --- | --- | --- | --- | --- |
| Bleu nuit | `#0F273B` | 100 · 78 · 47 · 56 | 15 · 39 · 59 | `ink` : texte courant et titres ; `on-accent` : texte sur le jaune |
| Magenta | `#E83583` | 0 · 89 · 9 · 0 | 232 · 53 · 131 | Non utilisée |
| Rouge | `#D2213C` | 11 · 97 · 71 · 2 | 210 · 33 · 60 | `danger` : erreurs, annulation, suppression, Signaler |
| Vert | `#00936E` | 98 · 7 · 70 · 0 | 0 · 147 · 110 | `success-fill` (aplats non textuels) ; le texte utilise `success` #007A5A |
| Vert clair | `#92C56E` | 50 · 0 · 70 · 0 | 146 · 197 · 110 | Non utilisée |
| Turquoise | `#1EAFD0` | 70 · 0 · 11 · 8 | 30 · 175 · 208 | Non utilisée |
| Bleu | `#0097D7` | 83 · 21 · 0 · 0 | 0 · 151 · 215 | Non utilisée |
| Jaune | `#FBBA00` | 0 · 30 · 100 · 0 | 251 · 186 · 0 | `accent` : pastilles de compteur, « Nouveau », toujours avec texte bleu nuit (8,83:1) |
| Orange | `#EF7D00` | 0 · 60 · 100 · 0 | 239 · 125 · 0 | `warning` (aplats non textuels) ; le texte utilise `warning-ink` #9A4F00 |
| Violet | `#8B4A97` | 55 · 80 · 0 · 0 | 139 · 74 · 151 | `secondary` : boutons d'engagement (Demander à rejoindre, Envoyer la demande, Publier le trajet), avatars ; texte blanc (5,96:1) |

Les couleurs non utilisées restent disponibles pour de futures illustrations ou graphiques (par exemple les séries du tableau de bord de la direction) ; ne pas les employer pour du texte sur blanc sans vérifier le contraste (magenta 3,99:1, turquoise 2,59:1, bleu 3,28:1, vert clair 2,01:1).

## Variantes créées pour l'accessibilité

| Token | Hex | Pourquoi |
| --- | --- | --- |
| `success` | `#007A5A` | Le vert officiel #00936E donne 3,89:1 avec du blanc : trop faible pour du texte. Assombri, il atteint 5,34:1 sur blanc et 4,6:1 sur `success-soft`. |
| `warning-ink` | `#9A4F00` | L'orange officiel donne 2,76:1 sur blanc. La version foncée atteint 5,39:1 sur `warning-soft` #FFF1D9. |
| `ink-muted` | `#52606E` | Gris bleuté dérivé du bleu nuit pour le texte secondaire (5,76:1 sur `surface`). |

## Neutres

| Token | Hex | Usage |
| --- | --- | --- |
| `surface` | `#F2F2F3` | Fond de page : le gris clair des pages de la charte |
| `surface-raised` | `#FFFFFF` | Cartes, popups, champs |
| `line` | `#DDDEE2` | Filets des cartes, séparateurs |
| `line-strong` | `#C4C6CD` | Bordures au survol, interrupteur éteint, étoiles vides |
