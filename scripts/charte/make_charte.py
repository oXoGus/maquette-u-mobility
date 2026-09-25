#!/usr/bin/env python3
"""Génère le HTML de la charte (scripts/charte/charte.html) ; pdf.js l'imprime en PDF.
Étapes (depuis la racine du dépôt, après python3 src/build.py) :
  npm i -D playwright && npx playwright install chromium
  node scripts/charte/shots.js      # captures des écrans → scripts/charte/img/
  python3 scripts/charte/make_charte.py
  node scripts/charte/pdf.js        # → docs/charte-graphique-u-mobility.pdf
"""
import os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))  # racine du dépôt
SRC = os.path.join(REPO, "src")
IMG = os.path.join(HERE, "img")


def lum(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + .05) / (y + .05)


def rgb(h):
    h = h.lstrip("#"); return " ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


COLORS = [
    ("Indigo", "brand", "#282F7A", "Couleur de l'université. Barre latérale, bouton principal, liens, onglet actif, logo.", True),
    ("Indigo foncé", "brand-hover", "#1E2461", "Survol et état pressé des aplats indigo.", True),
    ("Lavande", "secondary", "#535995", "Arcs de la charte officielle. Aplats secondaires, jauges, avatars. Texte blanc dessus.", True),
    ("Lavande claire", "accent", "#C7C9DB", "Accent provisoire : pastilles de compteur. À confirmer avec le PDF officiel.", False),
    ("Indigo pâle", "brand-soft", "#EAEBF3", "Fonds teintés : bandeaux d'information, badges, onglets.", False),
    ("Fond", "surface", "#F6F6FA", "Fond de page de l'application.", False),
    ("Blanc", "surface-raised", "#FFFFFF", "Cartes, popups, champs de saisie.", False),
    ("Bordure", "line", "#DCDCE8", "Séparateurs et bordures décoratives.", False),
    ("Encre", "ink", "#16193F", "Texte courant et titres.", True),
    ("Encre secondaire", "ink-muted", "#555A7E", "Métadonnées, aides, placeholders.", True),
]
STATUS = [("Succès", "success", "#1D7A4C", "#E3F2EA"), ("Erreur / danger", "danger", "#C42B40", "#FBE8EB"), ("Attente", "warning-ink", "#8A5A00", "#FDF1D8")]
PAIRS = [("#16193F", "#F6F6FA", "Texte sur fond"), ("#16193F", "#FFFFFF", "Texte sur carte"), ("#555A7E", "#F6F6FA", "Texte secondaire sur fond"),
         ("#555A7E", "#EAEBF3", "Texte secondaire sur indigo pâle"), ("#FFFFFF", "#282F7A", "Blanc sur indigo"), ("#FFFFFF", "#535995", "Blanc sur lavande"),
         ("#282F7A", "#EAEBF3", "Indigo sur indigo pâle"), ("#1D7A4C", "#FFFFFF", "Succès sur blanc"), ("#C42B40", "#FFFFFF", "Danger sur blanc"),
         ("#8A5A00", "#FDF1D8", "Attente sur fond attente")]

logo_svg = open(os.path.join(SRC, "assets", "logo-indigo.svg")).read()
logo_inner = re.search(r"<g .*?</g>", logo_svg, re.S).group(0)
def logo(color="#282F7A", w=160):
    return f'<svg viewBox="140 100 640 666" width="{w}" style="display:block">{logo_inner.replace("#282F7A", color)}</svg>'

loader = open(os.path.join(SRC, "assets", "u-mobility-loader.svg")).read()
loader = re.sub(r"<metadata>.*?</metadata>", "", loader, flags=re.S)
g_logo = re.search(r'<g fill="#282F7A" transform=.*?</g>', loader, re.S).group(0)
VPY, K, R, Q, D0 = 495.3, .196, 1.94, 1.63, 84.0
def road(s):
    out = ""
    for n in range(-2, 5):
        d1 = D0 * R ** (n + s); d2 = d1 * Q; y1, y2 = VPY + d1, VPY + d2
        c1 = 457.3 + .0088 * (y1 - 582); c2 = 457.3 + .0088 * (y2 - 582)
        out += f'<polygon points="{c1-K*d1:.1f},{y1:.1f} {c1+K*d1:.1f},{y1:.1f} {c2+K*d2:.1f},{y2:.1f} {c2-K*d2:.1f},{y2:.1f}"/>'
    return out
def loader_frame(s, idx):
    return f'''<svg viewBox="140 100 640 1020" width="92"><defs><linearGradient id="f{idx}" gradientUnits="userSpaceOnUse" x1="0" y1="760" x2="0" y2="1110"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m{idx}" maskUnits="userSpaceOnUse" x="140" y="572" width="640" height="548"><rect x="140" y="572" width="640" height="190" fill="#fff"/><rect x="140" y="760" width="640" height="360" fill="url(#f{idx})"/></mask></defs>
<g fill="#282F7A" mask="url(#m{idx})">{road(s)}</g>{g_logo}</svg>'''
# schéma de géométrie : lignes de fuite
geo = f'''<svg viewBox="300 440 320 700" width="170"><g stroke="#C42B40" stroke-width="3" stroke-dasharray="10 8" fill="none">
<line x1="457.3" y1="495.3" x2="{457.3-K*640:.1f}" y2="{495.3+640:.1f}"/><line x1="457.3" y1="495.3" x2="{457.3+K*640:.1f}" y2="{495.3+640:.1f}"/></g>
<g fill="#282F7A">{road(0)}</g><circle cx="457.3" cy="495.3" r="8" fill="#C42B40"/>
<line x1="300" y1="495.3" x2="620" y2="495.3" stroke="#C42B40" stroke-width="2"/></svg>'''

def img(name, cls=""):
    return f'<img class="{cls}" src="file://{IMG}/{name}.jpg" alt="">'

css = open(os.path.join(SRC, "styles.css")).read()
fonts = open(os.path.join(SRC, "fonts.css")).read().replace('url("assets/', f'url("file://{SRC}/assets/')

sw = "".join(f'''<div class="sw"><div class="chip-c" style="background:{h};{'box-shadow:inset 0 0 0 1px #dcdce8' if h in ('#FFFFFF','#F6F6FA','#EAEBF3') else ''}"><span style="color:{'#fff' if cr('#FFFFFF',h)>4.5 else '#16193F'}">{n}</span></div>
<div class="meta"><b>{h}</b><span>RGB {rgb(h)} · <code>--{t}</code></span><p>{u}</p></div></div>''' for n, t, h, u, dark in COLORS)
st = "".join(f'<div class="stc"><span class="badge" style="background:{bg};color:{h}">{n}</span><b>{h}</b><span>fond {bg} · <code>--{t}</code></span></div>' for n, t, h, bg in STATUS)
pairs = "".join(f'<tr><td><span class="pair" style="background:{b};color:{a};{"box-shadow:inset 0 0 0 1px #dcdce8" if b in ("#FFFFFF","#F6F6FA") else ""}">Aa</span></td><td>{lbl}</td><td class="num">{a} / {b}</td><td class="num"><b>{cr(a,b):.1f}:1</b></td><td>{"AAA" if cr(a,b)>=7 else "AA"}</td></tr>' for a, b, lbl in PAIRS)

TYPE = [("display", "Outfit", 40, 44, 700, "On part ensemble ?", "Accueil, onboarding (1 fois par écran)"),
        ("title-lg", "Outfit", 28, 34, 600, "Trajets vers Cité Descartes", "Titre d'écran"),
        ("title-md", "Outfit", 20, 26, 600, "Demain, départ 7 h 50", "Titre de carte, de section, de popup"),
        ("body-lg", "Figtree", 17, 24, 400, "Départ Noisy-le-Grand · Mont d'Est, arrivée Copernic.", "Introductions, messages"),
        ("body", "Figtree", 15, 22, 400, "Il reste 2 places. Léa accepte les bagages.", "Texte courant par défaut"),
        ("label", "Figtree", 14, 18, 600, "Demander à rejoindre ce trajet", "Boutons, onglets, libellés"),
        ("caption", "Figtree", 12, 16, 600, "2 PLACES LIBRES SUR 3", "Badges, métadonnées (majuscules espacées)")]
ty = "".join(f'<tr><td><code>{n}</code></td><td class="spec" style="font-family:\'{f}\';font-size:{s}px;line-height:{l}px;font-weight:{w};{"letter-spacing:.06em;text-transform:uppercase" if n=="caption" else ""}">{t}</td><td class="num">{f} {w}<br>{s} / {l} px</td><td>{u}</td></tr>' for n, f, s, l, w, t, u in TYPE)

PISTES = [("1 · Éco", "#282284", "#2DB273", "#5EC8F2"), ("2 · Corail", "#282284", "#FF6F59", "#FFD55A"), ("3 · Route", "#282284", "#00A6A6", "#FF8A00"),
          ("4 · Électrique", "#282284", "#C8F03C", "#FF5C9A"), ("5 · Campus", "#282284", "#8FB8FF", "#F5A300"), ("6 · Officielle UGE ✓", "#282F7A", "#535995", "#C7C9DB")]
pistes = "".join(f'<div class="piste{" on" if "✓" in n else ""}"><div class="bar">' + "".join(f'<i style="background:{c}"></i>' for c in cs) + f'</div><b>{n}</b><span>{" · ".join(cs[1:])}</span></div>' for n, *cs in PISTES)

def page(content, cls="", n=None, title=""):
    foot = f'<footer><span>U-Mobility · Charte graphique v1.0</span><span>{title}</span><span>{n}</span></footer>' if n else ""
    return f'<section class="page {cls}">{content}{foot}</section>'

dots = "".join('<i></i>' for _ in range(40))
pages = []
pages.append(page(f'''<div class="cover-dots">{dots}</div><span class="carc c1"></span><span class="carc c2"></span><span class="carc c3"></span>
<div class="cover-logo">{logo("#FFFFFF", 120)}</div>
<div class="cover-t"><h1>CHARTE<br>GRAPHIQUE</h1><p class="v">U-Mobility · v1.0</p><p class="s">Application de covoiturage étudiant<br>Université Gustave Eiffel · septembre 2026</p></div>''', "cover"))

pages.append(page(f'''<p class="eyebrow">01 · Le projet</p><h2>Covoiturer entre étudiants de la même université</h2>
<p class="lead">U-Mobility met en relation les étudiants et personnels de l'Université Gustave Eiffel qui font le même trajet vers le campus. L'application existe en version web et mobile ; cette charte s'applique aux deux.</p>
<div class="cols3">
<div class="box"><h3>Proche</h3><p>On partage un trajet avec quelqu'un de sa fac. Prénom, formation et notes sont visibles ; l'adresse jamais.</p></div>
<div class="box"><h3>Pratique</h3><p>Zones de rendez-vous prédéfinies, horaires types, trajets réguliers : trouver un trajet prend moins d'une minute.</p></div>
<div class="box"><h3>Rassurant</h3><p>Comptes universitaires vérifiés, notes après chaque trajet, messagerie encadrée, signalement en un clic.</p></div>
</div>
<h3 class="mt">Ton et écriture</h3>
<table class="t"><thead><tr><th>Règle</th><th>À faire</th><th>À éviter</th></tr></thead><tbody>
<tr><td>Tutoyer</td><td>« Où vas-tu aujourd'hui ? »</td><td>« Où allez-vous ? »</td></tr>
<tr><td>Boutons = l'action exacte</td><td>« Demander à rejoindre ce trajet »</td><td>« Valider », « OK »</td></tr>
<tr><td>Vrais lieux du campus</td><td>« Cité Descartes · Copernic »</td><td>« Bâtiment A »</td></tr>
<tr><td>Formats français</td><td>7 h 50 · 2,50 € · 1,4 kg de CO₂</td><td>7:50 · 2.50€ · 1.4kg</td></tr>
<tr><td>Libeller heures et lieux</td><td>« Départ 7 h 50 », « Arrivée estimée 8 h 20 »</td><td>Une heure seule sans libellé</td></tr>
<tr><td>Sobriété</td><td>Phrases courtes, pas d'emoji dans l'interface</td><td>« Super !!! 🎉 »</td></tr>
</tbody></table>
<h3 class="mt">Rôles de l'application</h3>
<p>Étudiant (passager <b>ou</b> conducteur, une vue à la fois) · Modérateur (page Signalements uniquement) · Direction (tableau de bord de statistiques anonymisées).</p>''', n=2, title="Le projet"))

pages.append(page(f'''<p class="eyebrow">02 · Logo</p><h2>Le pictogramme U-Mobility</h2>
<p class="lead">Deux passagers au-dessus d'une voiture, sur une route pointillée en perspective. Il s'utilise en indigo ou en blanc, jamais dans une autre couleur.</p>
<div class="cols2">
<div class="logo-tile light">{logo("#282F7A", 150)}<span>logo-indigo.svg · sur fonds clairs</span></div>
<div class="logo-tile dark">{logo("#FFFFFF", 150)}<span>logo-blanc.svg · sur indigo ou encre</span></div>
</div>
<div class="cols2 mt">
<div><h3>Zone de protection</h3><div class="protect"><div class="zone">{logo("#282F7A", 110)}</div></div><p class="small">Garder autour du logo un espace libre égal au diamètre d'une tête du pictogramme (≈ 1/6 de sa largeur).</p></div>
<div><h3>Tailles minimales</h3><div class="row" style="align-items:flex-end;gap:24px">{logo("#282F7A", 64)}{logo("#282F7A", 40)}{logo("#282F7A", 24)}</div><p class="small">64 px en en-tête · 40 px dans la barre latérale · <b>24 px minimum</b> (favicon, onglet mobile).</p>
<h3 class="mt">Interdits</h3>
<div class="row" style="gap:14px;margin-bottom:22px">
<div class="nope"><div style="transform:scaleX(1.5)">{logo("#282F7A", 44)}</div><span>Déformer</span></div>
<div class="nope"><div style="transform:rotate(-18deg)">{logo("#282F7A", 44)}</div><span>Pivoter</span></div>
<div class="nope">{logo("#535995", 44)}<span>Recolorer</span></div>
<div class="nope" style="background:#535995">{logo("#282F7A", 44)}<span>Fond lavande</span></div>
</div><p class="small">Le logo de l'Université Gustave Eiffel suit sa propre charte officielle (V2.4) : il n'est pas modifié ni associé au pictogramme dans un même bloc.</p></div>
</div>''', n=3, title="Logo"))

pages.append(page(f'''<p class="eyebrow">03 · Couleurs</p><h2>Palette de la charte officielle</h2>
<p class="lead">L'indigo et la lavande sont relevés sur la couverture de la charte officielle de l'Université Gustave Eiffel (V2.4) ; la lavande est l'indigo recouvert de 20 % de blanc.</p>
<div class="swatches">{sw}</div>
<div class="ratio"><i style="flex:60;background:#282F7A">Indigo + fond · 60 %</i><i style="flex:30;background:#535995">Lavande et teintes · 30 %</i><i style="flex:10;background:#C7C9DB;color:#16193F">Accent · 10 %</i></div>
<h3 class="mt">Couleurs de statut</h3><div class="stats">{st}</div>
<p class="small">Un statut n'est jamais indiqué par la couleur seule : toujours un mot (« Confirmé », « Annulé », « En attente ») et une icône.</p>''', n=4, title="Couleurs"))

pages.append(page(f'''<p class="eyebrow">03 · Couleurs</p><h2>Contrastes vérifiés</h2>
<p class="lead">Tous les couples texte / fond utilisés dans l'interface dépassent le niveau AA des WCAG (4,5:1 pour le texte courant, 3:1 pour le texte de 24 px et plus, les icônes et les bordures porteuses de sens).</p>
<table class="t"><thead><tr><th></th><th>Usage</th><th>Couleurs</th><th>Ratio</th><th>WCAG</th></tr></thead><tbody>{pairs}</tbody></table>
<div class="box mt"><h3>Règles d'usage</h3><ul>
<li>Un seul bouton lavande (<code>secondary</code>) par écran : l'appel à l'action principal (Demander à rejoindre, Publier).</li>
<li>La lavande claire (<code>accent</code>) n'est jamais une couleur de texte ; elle sert aux pastilles de compteur, avec du texte encre.</li>
<li>Texte sur indigo ou lavande : toujours blanc. Texte sur fonds clairs : encre ou encre secondaire.</li>
<li>Focus clavier : contour indigo de 2 px, décalé de 2 px, sur tous les éléments interactifs.</li>
</ul></div>''', n=5, title="Contrastes"))

pages.append(page(f'''<p class="eyebrow">04 · Typographie</p><h2>Outfit pour les titres, Figtree pour le texte</h2>
<p class="lead">Deux familles géométriques et arrondies, en écho aux formes du logo. Toutes deux sous licence SIL Open Font License, auto-hébergées dans le projet (aucun appel à Google Fonts).</p>
<div class="cols2"><div class="spec-big" style="font-family:Outfit"><span style="font-weight:300">Aa</span><span style="font-weight:600">Aa</span><p>Outfit · 300 à 700<br>Titres, chiffres clés, heures</p></div>
<div class="spec-big" style="font-family:Figtree"><span style="font-weight:400">Aa</span><span style="font-weight:700">Aa</span><p>Figtree · 400 à 700<br>Texte courant, interface</p></div></div>
<table class="t mt"><thead><tr><th>Style</th><th>Exemple</th><th>Réglage</th><th>Usage</th></tr></thead><tbody>{ty}</tbody></table>
<p class="small">Les chiffres alignés en colonne (prix, heures, statistiques) utilisent <code>font-variant-numeric: tabular-nums</code>. Titres d'accueil : Outfit Light 300 avec la seconde ligne en 600, comme la couverture de la charte officielle.</p>
<p class="small">Polices provisoires : à remplacer par la police officielle de l'université si le PDF complet de la charte V2.4 en impose une.</p>''', n=6, title="Typographie"))

sp = "".join(f'<div class="sp"><i style="width:{v}px;height:{v}px"></i><b>{v} px</b><code>space-{k}</code></div>' for k, v in [(1, 4), (2, 8), (3, 12), (4, 16), (6, 24), (8, 32), (12, 48)])
rd = "".join(f'<div class="rd"><i style="border-radius:{v}"></i><b>{v}</b><code>{n}</code><span>{u}</span></div>' for n, v, u in [("radius-sm", "8px", "Champs"), ("radius-md", "14px", "Boutons, cartes"), ("radius-lg", "24px", "Popups, bandeaux"), ("radius-pill", "999px", "Badges, avatars")])
pages.append(page(f'''<p class="eyebrow">05 · Espaces et formes</p><h2>Grille de 4 px, formes généreuses</h2>
<h3>Espacements</h3><div class="row sps">{sp}</div>
<h3 class="mt">Arrondis</h3><div class="row rds">{rd}</div>
<h3 class="mt">Ombres</h3><div class="row" style="gap:24px"><div class="sh" style="box-shadow:var(--shadow-card)">shadow-card<br><small>cartes au repos</small></div><div class="sh" style="box-shadow:var(--shadow-hover)">shadow-hover<br><small>carte survolée, menus</small></div><div class="sh" style="box-shadow:var(--shadow-dialog)">shadow-dialog<br><small>popups</small></div></div>
<h3 class="mt">Mise en page</h3>
<div class="cols2"><div class="box"><b>Ordinateur (≥ 901 px)</b><p>Barre latérale indigo de 256 px (compte collé en bas), contenu jusqu'à 1 180 px, marges de 32 px, 2 colonnes (contenu + colonne de 360 px).</p></div>
<div class="box"><b>Mobile (≤ 900 px)</b><p>Barre d'en-tête indigo, barre d'onglets en bas (Accueil, Rechercher, Publier, Mes trajets, Profil), marges de 16 px, une colonne.</p></div></div>''', n=7, title="Espaces et formes"))

pages.append(page(f'''<p class="eyebrow">06 · Composants</p><h2>Boutons, badges, champs</h2>
<h3>Boutons</h3><div class="row" style="gap:10px"><span class="btn">Principal</span><span class="btn secondary">Appel à l'action</span><span class="btn ghost">Secondaire</span><span class="btn danger">Annuler ma place</span><span class="btn success">Accepter</span><span class="btn is-disabled">Désactivé</span></div>
<p class="small">Hauteur 44 px (36 px en petit), rayon 14 px. Survol : teinte plus foncée et ombre ; bouton rouge : se remplit au survol.</p>
<h3 class="mt">Badges et tags</h3><div class="row" style="gap:8px"><span class="badge">Régulier · L M J V</span><span class="badge line">Ponctuel</span><span class="badge lav">2 places libres sur 3</span><span class="badge wait">2 demandes en attente</span><span class="badge ok">Place confirmée</span><span class="badge ko">Annulé</span><span class="tag static">Non-fumeur</span><span class="tag static">Musique douce</span></div>
<h3 class="mt">Sélection</h3><div class="row" style="gap:10px"><span class="chip on">8 h – 9 h</span><span class="chip">9 h – 10 h</span><span class="seg"><button class="on">Passager</button><button>Conducteur</button></span><span class="toggle on"></span><span class="toggle"></span>
<span class="days"><span class="on">L</span><span class="on">M</span><span>M</span><span class="on">J</span><span class="on">V</span><span class="off">S</span></span></div>
<h3 class="mt">Notes</h3><div class="row" style="gap:24px"><span class="stars" style="font-size:15px"><svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>4,9 <span class="n">(38)</span></span>
<span class="rate">{"".join('<button class="on"><svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg></button>' if k < 4 else '<button><svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg></button>' for k in range(5))}</span></div>
<p class="small">Note de 1 à 5 étoiles après chaque trajet, sans commentaire écrit : le passager note le conducteur, le conducteur note chaque passager.</p>
<h3 class="mt">Champs</h3><div class="cols2"><div class="field"><span class="label">Départ</span><div class="select"><button>Noisy-le-Grand · Mont d'Est</button></div><span class="hint">Zones de rendez-vous prédéfinies : jamais d'adresse.</span></div>
<div class="field"><span class="label">Tags (facultatif)</span><div class="tagbox"><span class="tag">Non-fumeur</span><span class="tag">Calme</span><span class="ph">Ajouter un tag…</span></div></div></div>''', n=8, title="Composants"))

pages.append(page(f'''<p class="eyebrow">06 · Composants</p><h2>La carte de trajet</h2>
<p class="lead">Brique centrale des listes. Toute la carte est cliquable : elle se soulève au survol et le bouton « Voir le détail » s'anime.</p>
<div class="anat">{img("c-trip", "w100")}</div>
<ol class="legend">
<li><b>Date et type</b> : « Régulier · L M J V » ou « Ponctuel », plus le statut éventuel (place confirmée, demande envoyée).</li>
<li><b>Itinéraire</b> : chaque heure est libellée « Départ » ou « Arrivée estimée », reliée par la route pointillée du logo.</li>
<li><b>Prix et places</b> : prix par passager en indigo, badge « x places libres sur y ».</li>
<li><b>Conducteur</b> : nom et note moyenne avec le nombre de notes, sans photo dans la carte.</li>
<li><b>Pied de carte</b> : nombre de demandes en attente, tags du trajet, bouton « Voir le détail ».</li>
</ol>
<div class="box mt"><h3>Ce que la carte ne montre pas</h3><p>Pas d'avatar du conducteur, pas de pourcentage de compatibilité, pas d'adresse. Les tags facultatifs remplacent la compatibilité : ils sont comparés aux tags écrits par le passager dans ses préférences.</p></div>''', n=9, title="Carte de trajet"))

pages.append(page(f'''<p class="eyebrow">07 · Motifs</p><h2>Les arcs et la route</h2>
<div class="cols2"><div><h3>Arcs de la charte officielle</h3><div class="arcs-demo"><span class="carc d1"></span><span class="carc d2"></span></div><p class="small">Anneaux lavande sur fond indigo, coupés par les bords : bandeaux d'accueil, écran de connexion, bas de la barre latérale. Toujours partiellement hors cadre, jamais plus de deux par bloc.</p></div>
<div><h3>Loader : la route qui défile</h3><div class="row" style="gap:6px;justify-content:center;flex-wrap:nowrap">{loader_frame(0, 0)}{loader_frame(.33, 1)}{loader_frame(.66, 2)}</div><p class="small">Les tirets du logo continuent vers le bas avec la même perspective et défilent en boucle (0,9 s). À l'arrêt, l'image est identique au logo. Fichier : <code>u-mobility-loader.svg</code> (animation SMIL, sans JavaScript).</p></div></div>
<div class="cols2 mt"><div class="box"><h3>Géométrie</h3><p>Mesurée sur les deux tirets du logo : les bords convergent vers un point de fuite (y = 495).</p><ul class="small"><li>demi-largeur = 0,196 × d (d = distance au point de fuite)</li><li>début du tiret n = 84 × 1,94<sup>n</sup></li><li>fin du tiret = début × 1,63</li><li>animation : n → n + s, s de 0 à 1</li></ul></div><div style="display:grid;place-items:center">{geo}</div></div>''', n=10, title="Motifs"))

pages.append(page(f'''<p class="eyebrow">08 · Écrans</p><h2>Version ordinateur</h2>
<div class="shot">{img("d-index", "w100")}<span>Tableau de bord · vue passager (activité façon GitHub, prochaines réservations)</span></div>
<div class="shot">{img("d-recherche", "w100")}<span>Rechercher un trajet · zones prédéfinies, tags, filtres</span></div>''', n=11, title="Écrans ordinateur"))
pages.append(page(f'''<p class="eyebrow">08 · Écrans</p><h2>Détail et popups</h2>
<div class="shot">{img("d-trajet", "w100")}<span>Détail du trajet · notes sans avis écrit, demandes en attente</span></div>
<div class="shot">{img("d-demande", "w100")}<span>Popup de demande · jours au choix parmi ceux du conducteur, message facultatif</span></div>''', n=12, title="Écrans ordinateur"))
pages.append(page(f'''<p class="eyebrow">08 · Écrans</p><h2>Version mobile</h2>
<div class="phones"><div class="shot">{img("m-index")}<span>Tableau de bord</span></div><div class="shot">{img("m-recherche")}<span>Recherche</span></div><div class="shot">{img("m-messages")}<span>Messagerie du trajet</span></div></div>
<p class="small">390 × 844 px. Barre d'onglets en bas, bouton Publier central en lavande. Les popups gardent la largeur de l'écran moins 16 px de chaque côté.</p>''', n=13, title="Écrans mobile"))

pages.append(page(f'''<p class="eyebrow">09 · Règles</p><h2>Accessibilité, sécurité et RGPD</h2>
<div class="cols2">
<div class="box"><h3>Accessibilité</h3><ul><li>Contrastes AA minimum (page 5).</li><li>Focus clavier visible partout ; touche Échap ferme les popups.</li><li>Cibles tactiles de 44 px minimum.</li><li>Statuts : couleur + mot + icône.</li><li>Animations désactivées si l'utilisateur a demandé moins d'animations.</li></ul></div>
<div class="box"><h3>Sécurité</h3><ul><li>Zones de rendez-vous prédéfinies, pas de géolocalisation.</li><li>Messagerie par trajet uniquement, numéros et liens masqués, fermée 24 h après le trajet.</li><li>Signalement d'un compte (depuis les messages) ou d'un trajet, traité par les modérateurs.</li><li>Comptes pseudonymisés côté modération, consultation d'identité journalisée.</li></ul></div>
</div>
<div class="box mt"><h3>RGPD</h3><ul><li><b>Droit d'accès et de portabilité</b> (articles 15 et 20) : bouton « Télécharger mes données » (JSON ou CSV) dans Profil → Confidentialité et données.</li>
<li><b>Droit à l'effacement</b> (article 17) : bouton « Supprimer mon compte et mes données », confirmation en écrivant SUPPRIMER. Les trajets passés restent dans les statistiques sous forme anonyme.</li>
<li><b>Minimisation</b> : pas de plaque d'immatriculation, pas d'adresse, nom réduit à l'initiale pour les autres membres.</li>
<li><b>Statistiques de la direction</b> : consolidées et anonymisées, aucun indicateur pour un groupe de moins de 10 personnes.</li>
<li><b>Polices auto-hébergées</b> : aucune donnée de navigation envoyée à Google Fonts.</li></ul>
<p class="small">À faire valider par le délégué à la protection des données de l'université avant une mise en service réelle.</p></div>''', n=14, title="Règles"))

pages.append(page(f'''<p class="eyebrow">Annexe</p><h2>Pistes de couleurs étudiées</h2>
<p class="lead">Cinq alternatives de couleurs secondaires ont été explorées autour de l'indigo du logo avant de retenir la charte officielle de l'université (piste 6).</p>
<div class="pistes">{pistes}</div>
<h3 class="mt">Fichiers de référence</h3>
<table class="t"><tbody>
<tr><td><code>src/assets/logo-indigo.svg</code>, <code>logo-blanc.svg</code></td><td>Logo vectoriel</td></tr>
<tr><td><code>src/assets/u-mobility-loader.svg</code></td><td>Loader animé</td></tr>
<tr><td><code>src/assets/fonts/</code></td><td>Outfit et Figtree (woff2, licence OFL)</td></tr>
<tr><td><code>src/styles.css</code></td><td>Tokens (variables CSS) et composants</td></tr>
<tr><td><code>docs/design-system/tokens.json</code></td><td>Tokens des 6 pistes</td></tr>
<tr><td><code>docs/charte-officielle-uge-couverture.png</code></td><td>Couverture de la charte officielle V2.4 (source des couleurs)</td></tr>
</tbody></table>
<p class="small mt">Éléments à compléter avec le PDF complet de la charte officielle : police officielle, couleurs complémentaires (l'accent lavande claire est provisoire), logo vectoriel de l'université et règles d'association des logos.</p>''', n=15, title="Annexe"))

PCSS = '''
@page { size: A4; margin: 0; }
html, body { margin: 0; background: #fff; }
body { font-family: "Figtree", system-ui, sans-serif; color: #16193F; -webkit-print-color-adjust: exact; print-color-adjust: exact; font-size: 11.5px; line-height: 17px; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm 20mm; position: relative; overflow: hidden; page-break-after: always; display: flex; flex-direction: column; gap: 10px; }
.page footer { position: absolute; left: 16mm; right: 16mm; bottom: 9mm; display: flex; justify-content: space-between; font-size: 9px; color: #555A7E; border-top: 1px solid #DCDCE8; padding-top: 6px; }
.eyebrow { font: 600 10px/14px "Figtree"; letter-spacing: .12em; text-transform: uppercase; color: #535995; margin: 0; }
h2 { font: 600 26px/31px "Outfit"; margin: 0 0 4px; letter-spacing: -.01em; }
h3 { font: 600 14px/19px "Outfit"; margin: 0 0 6px; }
.lead { font-size: 13px; line-height: 20px; color: #3a3f68; max-width: 150mm; margin: 0 0 6px; }
.small { font-size: 10px; line-height: 15px; color: #555A7E; margin: 4px 0 0; }
.mt { margin-top: 10px; }
code { font: 500 10px "DejaVu Sans Mono", monospace; color: #282F7A; background: #EAEBF3; padding: 1px 4px; border-radius: 4px; }
ul { margin: 0; padding-left: 16px; display: grid; gap: 4px; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.cols3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.box { background: #F6F6FA; border-radius: 12px; padding: 12px 14px; }
.box p { margin: 0; }
.t { width: 100%; border-collapse: collapse; font-size: 10.5px; }
.t th { text-align: left; font: 600 9px/12px "Figtree"; letter-spacing: .06em; text-transform: uppercase; color: #555A7E; padding: 0 8px 6px; border-bottom: 1px solid #DCDCE8; }
.t td { padding: 6px 8px; border-bottom: 1px solid #EAEBF3; vertical-align: middle; }
.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
.pair { display: inline-grid; place-items: center; width: 32px; height: 22px; border-radius: 6px; font: 700 12px "Outfit"; }
.w100 { width: 100%; display: block; border-radius: 10px; box-shadow: 0 0 0 1px #DCDCE8; }
/* couverture */
.cover { background: #282F7A; color: #fff; padding: 0; }
.cover-dots { position: absolute; left: 0; top: 0; bottom: 0; width: 16mm; display: grid; align-content: start; gap: 12px; padding-top: 8px; }
.cover-dots i { width: 26px; height: 26px; border-radius: 50%; border: 6px solid #535995; border-left-color: transparent; margin-left: -6px; }
.cover-dots i:nth-child(3n) { width: 12px; height: 12px; border: 0; background: #535995; margin-left: 12px; }
.carc { position: absolute; border-radius: 50%; border: 70px solid #535995; }
.c1 { width: 420px; height: 420px; right: -230px; top: 120px; border-width: 90px; }
.c2 { width: 360px; height: 360px; left: 120px; top: -250px; }
.c3 { width: 300px; height: 300px; left: 150px; bottom: -220px; border-width: 60px; }
.cover-logo { position: absolute; left: 34mm; top: 60mm; }
.cover-t { position: absolute; left: 34mm; top: 150mm; }
.cover-t h1 { font: 300 50px/56px "Outfit"; margin: 0; letter-spacing: .01em; color: #fff; }
.cover-t .v { font: 600 16px/22px "Outfit"; margin: 18px 0 0; }
.cover-t .s { font-size: 13px; line-height: 20px; color: #d6d8ea; margin: 36px 0 0; }
/* couleurs */
.swatches { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 14px; }
.sw { display: grid; grid-template-columns: 64px 1fr; gap: 10px; align-items: center; }
.chip-c { height: 52px; border-radius: 10px; display: grid; align-items: end; padding: 6px; font: 600 9px "Figtree"; }
.sw .meta b { font: 600 12px "Outfit"; display: block; }
.sw .meta span { font-size: 9.5px; color: #555A7E; }
.sw .meta p { margin: 2px 0 0; font-size: 9.5px; line-height: 13px; }
.ratio { display: flex; height: 30px; border-radius: 10px; overflow: hidden; margin-top: 8px; }
.ratio i { display: grid; place-items: center; color: #fff; font: 600 10px "Figtree"; font-style: normal; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.stc { display: grid; gap: 3px; font-size: 10px; color: #555A7E; }
.stc b { font: 600 12px "Outfit"; color: #16193F; }
/* logo */
.logo-tile { border-radius: 14px; height: 70mm; display: grid; place-items: center; align-content: center; gap: 12px; }
.logo-tile span { font-size: 10px; }
.logo-tile.light { background: #F6F6FA; color: #555A7E; }
.logo-tile.dark { background: #282F7A; color: #d6d8ea; }
.protect { background: #F6F6FA; border-radius: 12px; padding: 14px; display: grid; place-items: center; }
.protect .zone { padding: 18px; outline: 1.5px dashed #C42B40; outline-offset: 0; }
.nope { width: 70px; height: 70px; border-radius: 10px; background: #F6F6FA; display: grid; place-items: center; position: relative; }
.nope::after { content: ""; position: absolute; inset: 8px; background: linear-gradient(45deg, transparent calc(50% - 1.5px), #C42B40 calc(50% - 1.5px), #C42B40 calc(50% + 1.5px), transparent calc(50% + 1.5px)); }
.nope span { position: absolute; bottom: -16px; font-size: 9px; color: #555A7E; }
/* typo */
.spec-big { background: #F6F6FA; border-radius: 12px; padding: 12px 16px; display: grid; grid-template-columns: auto auto 1fr; gap: 10px; align-items: center; }
.spec-big span { font-size: 64px; line-height: 64px; color: #282F7A; }
.spec-big p { margin: 0; font-family: "Figtree"; font-size: 10.5px; color: #555A7E; }
td.spec { color: #16193F; }
/* espaces */
.sps { gap: 18px; align-items: flex-end; }
.sp { display: grid; justify-items: center; gap: 4px; font-size: 9.5px; }
.sp i { background: #535995; border-radius: 2px; display: block; }
.rds { gap: 16px; }
.rd { display: grid; justify-items: center; gap: 3px; font-size: 9.5px; }
.rd i { width: 70px; height: 50px; background: #EAEBF3; border: 2px solid #282F7A; display: block; }
.rd span { color: #555A7E; }
.sh { background: #fff; border-radius: 14px; padding: 16px 18px; font: 600 11px "Figtree"; }
.sh small { font-weight: 400; color: #555A7E; }
/* composants (réutilise styles.css) */
.page .btn, .page .badge, .page .chip, .page .seg, .page .tag { font-family: "Figtree"; }
.select > button { width: 100%; min-height: 40px; border: 1px solid #DCDCE8; border-radius: 8px; background: #fff; text-align: left; padding: 0 12px; }
.tagbox .ph { color: #555A7E; font-size: 12px; }
.anat { background: #F6F6FA; border-radius: 14px; padding: 12px; }
.legend { margin: 6px 0 0; padding-left: 18px; display: grid; gap: 5px; font-size: 11px; }
.arcs-demo { height: 150px; background: #282F7A; border-radius: 14px; position: relative; overflow: hidden; }
.d1 { width: 220px; height: 220px; right: -70px; top: -110px; border-width: 44px; }
.d2 { width: 180px; height: 180px; left: 60px; bottom: -140px; border-width: 38px; }
.shot { display: grid; gap: 5px; }
.shot span { font-size: 10px; color: #555A7E; }
.phones { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.phones img { width: 100%; border-radius: 16px; box-shadow: 0 0 0 5px #16193F; }
.pistes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.piste { border: 1px solid #DCDCE8; border-radius: 12px; padding: 10px; display: grid; gap: 6px; font-size: 10px; color: #555A7E; }
.piste.on { border: 2px solid #282F7A; }
.piste b { font: 600 12px "Outfit"; color: #16193F; }
.piste .bar { display: flex; height: 34px; border-radius: 8px; overflow: hidden; }
.piste .bar i { flex: 1; }
.piste .bar i:first-child { flex: 2; }
'''
html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Charte graphique U-Mobility</title>
<style>{fonts}</style><style>{css}</style><style>{PCSS}</style></head><body>{"".join(pages)}</body></html>'''
out_html = os.path.join(HERE, "charte.html")  # (ignoré par git)
open(out_html, "w").write(html)
print("html ok", len(pages), "pages")
