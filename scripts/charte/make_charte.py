#!/usr/bin/env python3
"""Génère le HTML de la charte (scripts/charte/charte.html) ; pdf.js l'imprime en PDF.
Étapes (depuis la racine du dépôt, après python3 src/build.py) :
  npm i -D playwright && npx playwright install chromium
  node scripts/charte/shots.js      # captures des écrans → scripts/charte/img/
  python3 scripts/charte/make_charte.py
  node scripts/charte/pdf.js        # → docs/charte-graphique-u-mobility.pdf
Source des couleurs, de la typographie et des règles de logo : docs/Charte_Gustave_Eiffel_V2-4.pdf.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))  # racine du dépôt
SRC = os.path.join(REPO, "src")
IMG = os.path.join(HERE, "img")
BRAND, INK, MUTED, SURF, LINE, SOFT, VIOLET, JAUNE, ROUGE = "#2F2A85", "#0F273B", "#52606E", "#F2F2F3", "#DDDEE2", "#EBEAF4", "#8B4A97", "#FBBA00", "#D2213C"


def lum(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + .05) / (y + .05)


def rgb(h):
    h = h.lstrip("#"); return " ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


_BUILD = open(os.path.join(SRC, "build.py"), encoding="utf-8").read()


def ico(name):  # icône du dictionnaire P de build.py
    path = re.search(r'"' + name + r"\": '(.*?)',\n", _BUILD).group(1)
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{path}</svg>'


def tg(label, icon, fam, chip=False, on=False):  # tag affiché ou puce de choix (mêmes classes que build.py)
    if chip:
        return f'<button class="tagchip f-{fam}{" on" if on else ""}"><span class="ic">{ico(icon)}</span><span class="ck">{ico("check")}</span>{label}</button>'
    return f'<span class="tag f-{fam}">{ico(icon)}<span class="tl">{label}</span></span>'


def fr(x, d=2):  # 5.96 → « 5,96 »
    return f"{x:.{d}f}".replace(".", ",")


# Rôles de l'interface (tokens de src/styles.css)
COLORS = [
    ("Bleu UGE", "brand", "#2F2A85", "Couleur principale (Pantone 2746C). Barre latérale, en-tête mobile, bandeaux d'accueil, bouton principal, liens, onglet actif, logo."),
    ("Bleu foncé", "brand-hover", "#231F66", "Survol et état pressé des aplats bleus."),
    ("Violet UGE", "secondary", "#8B4A97", "Boutons d'engagement (Demander à rejoindre, Envoyer la demande, Publier le trajet), avatars. Texte blanc dessus."),
    ("Jaune UGE", "accent", "#FBBA00", "Pastilles de compteur et « Nouveau », toujours avec du texte bleu nuit."),
    ("Bleu pâle", "brand-soft", "#EBEAF4", "Fonds teintés : bandeaux d'information, badges, onglets, heatmap."),
    ("Gris de page", "surface", "#F2F2F3", "Fond de page : le gris clair des pages de la charte."),
    ("Blanc", "surface-raised", "#FFFFFF", "Cartes, popups, champs de saisie."),
    ("Filet", "line", "#DDDEE2", "Contour des cartes, séparateurs."),
    ("Bleu nuit UGE", "ink", "#0F273B", "Texte courant et titres."),
    ("Encre secondaire", "ink-muted", "#52606E", "Métadonnées, aides, placeholders."),
]
LIGHT = ("#FFFFFF", "#F2F2F3", "#EBEAF4", "#DDDEE2")
STATUS = [("Confirmé", "success", "#007A5A", "#E0F2EC", "vert UGE assombri"), ("Annulé / erreur", "danger", "#D2213C", "#FBE7EA", "rouge UGE"),
          ("En attente", "warning-ink", "#9A4F00", "#FFF1D9", "orange UGE assombri")]
PAIRS = [("#0F273B", "#F2F2F3", "Texte sur fond de page"), ("#0F273B", "#FFFFFF", "Texte sur carte"), ("#52606E", "#F2F2F3", "Texte secondaire sur fond"),
         ("#52606E", "#EBEAF4", "Texte secondaire sur bleu pâle"), ("#FFFFFF", "#2F2A85", "Blanc sur bleu UGE"), ("#D6D5EA", "#2F2A85", "Texte secondaire sur bleu UGE"),
         ("#FFFFFF", "#8B4A97", "Blanc sur violet (boutons d'engagement)"), ("#2F2A85", "#EBEAF4", "Bleu sur bleu pâle"), ("#0F273B", "#FBBA00", "Bleu nuit sur jaune (compteurs)"),
         ("#007A5A", "#E0F2EC", "Succès sur fond succès"), ("#FFFFFF", "#007A5A", "Blanc sur succès (Accepter)"), ("#D2213C", "#FFFFFF", "Danger sur blanc"),
         ("#B01B33", "#FBE7EA", "Badge « Annulé »"), ("#9A4F00", "#FFF1D9", "Attente sur fond attente")]

# Palette officielle, charte V2.4 p. 7 : (nom, hex, CMJN, rôle dans l'interface)
PRINCIPALE = ("Bleu UGE", "#2F2A85", "100 · 98 · 0 · 0", "Pantone 2746C")
SECONDAIRES = [("Bleu nuit", "#0F273B", "100 · 78 · 47 · 56", "ink · texte"), ("Magenta", "#E83583", "0 · 89 · 9 · 0", ""),
               ("Rouge", "#D2213C", "11 · 97 · 71 · 2", "danger"), ("Vert", "#00936E", "98 · 7 · 70 · 0", "success-fill"),
               ("Vert clair", "#92C56E", "50 · 0 · 70 · 0", ""), ("Turquoise", "#1EAFD0", "70 · 0 · 11 · 8", ""),
               ("Bleu", "#0097D7", "83 · 21 · 0 · 0", ""), ("Jaune", "#FBBA00", "0 · 30 · 100 · 0", "accent"),
               ("Orange", "#EF7D00", "0 · 60 · 100 · 0", "warning"), ("Violet", "#8B4A97", "55 · 80 · 0 · 0", "secondary")]

# ---------- logos ----------
logo_svg = open(os.path.join(SRC, "assets", "logo-indigo.svg")).read()
logo_inner = re.search(r"<g .*?</g>", logo_svg, re.S).group(0)
def logo(color=BRAND, w=160):
    return f'<svg viewBox="140 100 640 666" width="{w}" style="display:block">{logo_inner.replace(BRAND, color)}</svg>'

uge_svg = open(os.path.join(SRC, "assets", "uge-logo.svg")).read()
uge_inner = re.search(r"<g .*?</g>", uge_svg, re.S).group(0)
def uge(color=BRAND, w=200, vb="0 0 325.65 67.38", style=""):
    return f'<svg viewBox="{vb}" width="{w}" style="display:block;{style}">{uge_inner.replace(BRAND, color)}</svg>'
sym_svg = open(os.path.join(SRC, "assets", "uge-symbole.svg")).read()
sym_path = re.search(r'd="([^"]+)"', sym_svg).group(1)
def sym(color=BRAND, w=60):
    return f'<svg viewBox="0 0 86.78 86.96" width="{w}" style="display:block"><path fill="{color}" d="{sym_path}"/></svg>'

# ---------- loader ----------
loader = open(os.path.join(SRC, "assets", "u-mobility-loader.svg")).read()
loader = re.sub(r"<metadata>.*?</metadata>", "", loader, flags=re.S)
g_logo = re.search(r'<g fill="#2F2A85" transform=.*?</g>', loader, re.S | re.I).group(0)
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
<g fill="{BRAND}" mask="url(#m{idx})">{road(s)}</g>{g_logo}</svg>'''
# schéma de géométrie : lignes de fuite
geo = f'''<svg viewBox="300 440 320 700" width="170"><g stroke="{ROUGE}" stroke-width="3" stroke-dasharray="10 8" fill="none">
<line x1="457.3" y1="495.3" x2="{457.3-K*640:.1f}" y2="{495.3+640:.1f}"/><line x1="457.3" y1="495.3" x2="{457.3+K*640:.1f}" y2="{495.3+640:.1f}"/></g>
<g fill="{BRAND}">{road(0)}</g><circle cx="457.3" cy="495.3" r="8" fill="{ROUGE}"/>
<line x1="300" y1="495.3" x2="620" y2="495.3" stroke="{ROUGE}" stroke-width="2"/></svg>'''

def img(name, cls=""):
    return f'<img class="{cls}" src="file://{IMG}/{name}.jpg" alt="">'

css = open(os.path.join(SRC, "styles.css")).read()
fonts = open(os.path.join(SRC, "fonts.css")).read().replace('url("assets/', f'url("file://{SRC}/assets/')

sw = "".join(f'''<div class="sw"><div class="chip-c" style="background:{h};{f'box-shadow:inset 0 0 0 1px {LINE}' if h in LIGHT else ''}"><span style="color:{'#fff' if cr('#FFFFFF',h)>4.5 else INK}">{n}</span></div>
<div class="meta"><b>{h}</b><span>RVB {rgb(h)} · <code>--{t}</code></span><p>{u}</p></div></div>''' for n, t, h, u in COLORS)
st = "".join(f'<div class="stc"><span class="badge" style="background:{bg};color:{h}">{n}</span><b>{h}</b><span>{src} · fond {bg} · <code>--{t}</code></span></div>' for n, t, h, bg, src in STATUS)
pairs = "".join(f'<tr><td><span class="pair" style="background:{b};color:{a};{f"box-shadow:inset 0 0 0 1px {LINE}" if b in LIGHT else ""}">Aa</span></td><td>{lbl}</td><td class="num">{a} / {b}</td><td class="num"><b>{fr(cr(a,b))}:1</b></td><td>{"AAA" if cr(a,b)>=7 else "AA" if cr(a,b)>=4.5 else "—"}</td></tr>' for a, b, lbl in PAIRS)
assert all(cr(a, b) >= 4.5 for a, b, _ in PAIRS), "un couple de PAIRS est sous 4,5:1"

def offi(n, h, cmjn, role, big=False):
    txt = "#fff" if cr("#FFFFFF", h) >= cr(INK, h) else INK
    return (f'<div class="off{" big" if big else ""}"><div class="offc" style="background:{h};color:{txt}"><b>{n}</b>{f"<span>{role}</span>" if role else ""}</div>'
            f'<div class="offm"><b>{h.lower()}</b><span>CMJN {cmjn}</span><span>RVB {rgb(h).replace(" ", " · ")}</span></div></div>')
off_sec = "".join(offi(*c) for c in SECONDAIRES)

TYPE = [("cover", 56, 60, 300, "COVOITURAGE", "Titre de connexion, capitales (couverture de la charte)"),
        ("display", 40, 44, 800, "On part ensemble ?", "Bandeau d'accueil, une fois par écran"),
        ("title-lg", 30, 36, 800, "Trajets vers Cité Descartes", "Titre d'écran (h1), chiffres clés"),
        ("title-md", 20, 26, 700, "Demain, départ 7 h 50", "Titre de carte, de section, de popup (h2)"),
        ("body-lg", 16, 24, 400, "Départ Noisy-le-Grand · Mont d'Est, arrivée Copernic.", "Introductions"),
        ("body", 15, 22, 400, "Il reste 2 places. Léa accepte les bagages.", "Texte courant par défaut"),
        ("label", 14, 18, 700, "Demander à rejoindre ce trajet", "Boutons ; libellés de champ en 600 13 px"),
        ("caption", 12, 16, 600, "2 places libres sur 3", "Badges, métadonnées, en casse de phrase")]
LS = {"cover": "-0.01em", "display": "-0.025em", "title-lg": "-0.02em", "title-md": "-0.01em"}
ty = "".join(f'<tr><td><code>{n}</code></td><td class="spec" style="font-family:Figtree;font-size:{min(s, 30)}px;line-height:{min(l, 36)}px;font-weight:{w};letter-spacing:{LS.get(n, "0")};{"text-transform:uppercase" if n=="cover" else ""}">{t}</td><td class="num">Figtree {w}<br>{s} / {l} px</td><td>{u}</td></tr>' for n, s, l, w, t, u in TYPE)

def page(content, cls="", n=None, title=""):
    foot = f'<footer><span>U-Mobility · Charte graphique v2.0</span><span>{title}</span><span>{n}</span></footer>' if n else ""
    return f'<section class="page {cls}">{content}{foot}</section>'

pages = []
pages.append(page(f'''<div class="cover-pat"></div><span class="carc c1"></span><span class="carc c2"></span><svg class="c3" viewBox="0 0 340 340" width="340" height="340"><circle cx="170" cy="170" r="132" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="76"/></svg>
<div class="cover-logo">{logo("#FFFFFF", 110)}</div>
<div class="cover-t"><h1>CHARTE<br>GRAPHIQUE</h1><p class="v">U-Mobility · v2.0</p><p class="s">Application de covoiturage étudiant<br>d'après la charte graphique de l'Université Gustave Eiffel V2.4<br>septembre 2026</p></div>
<div class="cover-uge">{uge("#FFFFFF", 190)}</div>''', "cover"))

pages.append(page(f'''<p class="eyebrow">01 · Le projet</p><h2>Covoiturer entre étudiants de la même université</h2>
<p class="lead">U-Mobility met en relation les étudiants et personnels de l'Université Gustave Eiffel qui font le même trajet vers le campus. L'application existe en version web et mobile ; cette charte s'applique aux deux. Elle décline la charte graphique officielle de l'université (V2.4) : couleurs, typographie, logotype et principe graphique en sont repris.</p>
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
<tr><td>Casse de phrase</td><td>« 2 places libres sur 3 »</td><td>« 2 PLACES LIBRES »</td></tr>
<tr><td>Sobriété</td><td>Phrases courtes, pas d'emoji dans l'interface</td><td>« Super !!! 🎉 »</td></tr>
</tbody></table>
<h3 class="mt">Rôles de l'application</h3>
<p>Étudiant (passager <b>ou</b> conducteur, une vue à la fois) · Modérateur (page Signalements uniquement) · Direction (tableau de bord de statistiques anonymisées).</p>''', n=2, title="Le projet"))

pages.append(page(f'''<p class="eyebrow">02 · Logos</p><h2>Le logotype de l'université</h2>
<p class="lead">Vectorisé depuis la charte officielle V2.4 (<code>uge-logo.svg</code>, <code>uge-logo-blanc.svg</code>, <code>uge-symbole.svg</code>). Il n'est jamais redessiné ni modifié.</p>
<div class="cols3">
<div class="logo-tile light sm">{uge(BRAND, 170)}<span>Bleu · sur fond blanc</span></div>
<div class="logo-tile sm" style="background:#92C56E;color:{INK}">{uge("#000000", 170)}<span>Noir · sur fonds de couleur claire</span></div>
<div class="logo-tile dark sm">{uge("#FFFFFF", 170)}<span>Blanc · sur fonds plus foncés</span></div>
</div>
<div class="cols2 mt">
<div><h3>Zone de protection et taille minimale</h3><div class="protect"><div class="zone uz">{uge(BRAND, 200)}</div></div>
<p class="small">Dégagement minimal tout autour = la largeur du demi-cercle du symbole. Largeur minimale : <b>25 mm</b> à l'impression (≈ 96 px à l'écran).</p></div>
<div><h3>Le symbole seul</h3><div class="row" style="gap:18px;align-items:center">{sym(BRAND, 64)}<div class="symtile">{sym("#FFFFFF", 44)}</div></div>
<p class="small">Élément graphique (motif, avatar de réseau social). <b>Il ne remplace jamais le logotype.</b> Dans U-Mobility, il sert au motif de la bande gauche.</p></div>
</div>
<h3 class="mt">Interdits</h3>
<div class="row" style="gap:14px;margin-bottom:22px">
<div class="nope w">{uge(BRAND, 84, style="transform:rotate(-14deg)")}<span>Incliner</span></div>
<div class="nope w">{uge(BRAND, 84, style="transform:scaleY(1.7)")}<span>Déformer</span></div>
<div class="nope w">{uge("#E83583", 84)}<span>Recolorer</span></div>
<div class="nope w">{uge(BRAND, 64, vb="80 0 245.65 67.38")}<span>Retirer un élément</span></div>
<div class="nope w"><div class="row" style="gap:4px;flex-wrap:nowrap">{sym(BRAND, 22)}<span class="serif">Université<br>Gustave Eiffel</span></div><span>Autre typographie</span></div>
<div class="nope w" style="background:#1EAFD0">{uge(BRAND, 84)}<span>Illisible</span></div>
</div>
<p class="small">Inventer un nouveau principe d'endossement est aussi interdit. Sur un fond complexe (photo), utiliser le logo bleu dans un cartouche blanc.</p>''', n=3, title="Logotype UGE"))

pages.append(page(f'''<p class="eyebrow">02 · Logos</p><h2>Le pictogramme U-Mobility</h2>
<p class="lead">Deux passagers au-dessus d'une voiture, sur une route pointillée en perspective. Il s'utilise en bleu UGE ou en blanc, jamais dans une autre couleur.</p>
<div class="cols2">
<div class="logo-tile light">{logo(BRAND, 130)}<span>logo-indigo.svg · bleu #2F2A85 sur fonds clairs</span></div>
<div class="logo-tile dark">{logo("#FFFFFF", 130)}<span>logo-blanc.svg · sur bleu UGE ou bleu nuit</span></div>
</div>
<div class="cols2 mt">
<div><h3>Zone de protection</h3><div class="protect"><div class="zone">{logo(BRAND, 90)}</div></div><p class="small">Garder autour du pictogramme un espace libre égal au diamètre d'une tête (≈ 1/6 de sa largeur).</p>
<h3 class="mt">Tailles minimales</h3><div class="row" style="align-items:flex-end;gap:24px">{logo(BRAND, 64)}{logo(BRAND, 40)}{logo(BRAND, 24)}</div><p class="small">64 px en en-tête · 40 px dans la barre latérale · <b>24 px minimum</b> (favicon, onglet mobile).</p></div>
<div><h3>Avec le logotype de l'université</h3><div class="assoc"><div class="row" style="gap:10px;flex-wrap:nowrap">{logo("#FFFFFF", 40)}<div><b>U-Mobility</b><small>Université Gustave Eiffel</small></div></div><div class="assoc-uge">{uge("#FFFFFF", 150)}</div></div>
<p class="small">Écran de connexion : le pictogramme et le nom de l'application en haut, le logotype UGE blanc en signature, séparés. Les deux ne sont jamais fusionnés dans un même bloc et le logotype garde sa zone de protection.</p>
<h3 class="mt">Interdits</h3>
<div class="row" style="gap:14px;margin-bottom:22px">
<div class="nope"><div style="transform:scaleX(1.5)">{logo(BRAND, 40)}</div><span>Déformer</span></div>
<div class="nope"><div style="transform:rotate(-18deg)">{logo(BRAND, 40)}</div><span>Pivoter</span></div>
<div class="nope">{logo(VIOLET, 40)}<span>Recolorer</span></div>
<div class="nope" style="background:{VIOLET}">{logo(BRAND, 40)}<span>Fond violet</span></div>
</div></div>
</div>''', n=4, title="Logo U-Mobility"))

pages.append(page(f'''<p class="eyebrow">03 · Couleurs</p><h2>Les couleurs de l'interface</h2>
<p class="lead">Toutes viennent de la palette officielle de l'université (page suivante) : le bleu UGE domine, le bleu nuit écrit, le violet et le jaune ponctuent. Seules des teintes claires et deux variantes de texte plus foncées ont été ajoutées.</p>
<div class="swatches">{sw}</div>
<div class="ratio"><i style="flex:60;background:{BRAND}">Bleu UGE + gris de page · 60 %</i><i style="flex:30;background:{INK}">Bleu nuit, blanc, teintes · 30 %</i><i style="flex:6;background:{VIOLET}">Violet</i><i style="flex:4;background:{JAUNE};color:{INK}">Jaune</i></div>
<h3 class="mt">Couleurs de statut</h3><div class="stats">{st}</div>
<p class="small">Le vert (#00936E) et l'orange (#EF7D00) officiels restent pour les aplats non textuels ; le texte utilise leurs versions assombries, qui passent le niveau AA. Un statut n'est jamais indiqué par la couleur seule : toujours un mot (« Confirmé », « Annulé », « En attente ») et une icône.</p>''', n=5, title="Couleurs"))

pages.append(page(f'''<p class="eyebrow">03 · Couleurs</p><h2>Palette officielle de l'université</h2>
<p class="lead">Charte graphique Université Gustave Eiffel V2.4, page 7. Valeurs reprises sans modification ; le rôle dans l'interface est indiqué sur chaque pastille.</p>
<h3>Couleur principale</h3>
<div class="offp">{offi(*PRINCIPALE, big=True)}<div class="box"><p>Le bleu UGE est la couleur de l'université et la couleur dominante de l'application : aplats de navigation, bandeaux, bouton principal, liens, logo. Texte blanc dessus (11,73:1).</p><p class="small">Teintes dérivées : #231F66 (survol) · #EBEAF4 et #DCDAEC (fonds) · #D6D5EA (texte secondaire sur bleu) · heatmap #EBEAF4 → #2F2A85.</p></div></div>
<h3 class="mt">Couleurs secondaires</h3>
<div class="offg">{off_sec}</div>
<p class="small">Magenta, vert clair, turquoise et bleu ne sont pas utilisés pour l'instant (réserve pour graphiques et illustrations) : leur contraste avec le blanc est insuffisant pour du texte (2,0 à 4,0:1).</p>''', n=6, title="Palette officielle"))

pages.append(page(f'''<p class="eyebrow">03 · Couleurs</p><h2>Contrastes vérifiés</h2>
<p class="lead">Tous les couples texte / fond utilisés dans l'interface dépassent le niveau AA des WCAG (4,5:1 pour le texte courant, 3:1 pour le texte de 24 px et plus, les icônes et les bordures porteuses de sens). Ratios calculés par le script de la charte.</p>
<table class="t"><thead><tr><th></th><th>Usage</th><th>Couleurs</th><th>Ratio</th><th>WCAG</th></tr></thead><tbody>{pairs}</tbody></table>
<div class="box mt"><h3>Règles d'usage</h3><ul>
<li>Un seul bouton violet (<code>secondary</code>) par écran : l'engagement principal (Demander à rejoindre, Envoyer la demande, Publier le trajet).</li>
<li>Le jaune (<code>accent</code>) n'est jamais une couleur de texte ; il sert aux pastilles de compteur, avec du texte bleu nuit.</li>
<li>Texte sur bleu UGE ou violet : toujours blanc. Texte sur fonds clairs : bleu nuit ou encre secondaire.</li>
<li>Focus clavier : contour bleu de 2 px, décalé de 2 px, sur tous les éléments interactifs.</li>
</ul></div>''', n=7, title="Contrastes"))

pages.append(page(f'''<p class="eyebrow">04 · Typographie</p><h2>Une seule famille, titres et texte</h2>
<p class="lead">La charte impose <b>TT Norms®</b> pour toutes les communications de l'université, aussi bien pour les titres que pour le texte. Sa licence étant payante, <b>Figtree</b> (géométrique, SIL Open Font License, auto-hébergée) la remplace. Pile : <code>"TT Norms Pro", "TT Norms", "Figtree", system-ui</code>.</p>
<div class="cols2"><div class="spec-big"><span style="font-weight:300">Aa</span><span style="font-weight:800">Aa</span><p>Figtree · 300 à 800<br>Light 300 : titre de connexion<br>ExtraBold 800 : titres</p></div>
<div class="spec-big"><span style="font-weight:400">Aa</span><span style="font-weight:700">Aa</span><p>Figtree · 400 à 700<br>Texte courant, interface<br>Gras 700 : boutons, h2, h3</p></div></div>
<table class="t mt"><thead><tr><th>Style</th><th>Exemple</th><th>Réglage</th><th>Usage</th></tr></thead><tbody>{ty}</tbody></table>
<p class="small">Titres en gras 800 et en casse de phrase, comme les affiches de la charte ; seul le titre de l'écran de connexion reprend la couverture (« CHARTE GRAPHIQUE ») en Light 300 et capitales (56 / 60 px, réduit ici). Pas de libellés en capitales espacées. Les chiffres alignés en colonne (prix, heures, statistiques) utilisent <code>font-variant-numeric: tabular-nums</code>.</p>''', n=8, title="Typographie"))

sp = "".join(f'<div class="sp"><i style="width:{v}px;height:{v}px"></i><b>{v} px</b><code>space-{k}</code></div>' for k, v in [(1, 4), (2, 8), (3, 12), (4, 16), (6, 24), (8, 32), (12, 48)])
rd = "".join(f'<div class="rd"><i style="border-radius:{v}"></i><b>{v}</b><code>{n}</code><span>{u}</span></div>' for n, v, u in [("radius-sm", "4px", "Champs, navigation"), ("radius-md", "6px", "Cartes, menus"), ("radius-lg", "8px", "Bandeaux, popups"), ("radius-pill", "999px", "Boutons, puces, avatars")])
pages.append(page(f'''<p class="eyebrow">05 · Espaces et formes</p><h2>Ce qui contient est droit, ce qui se touche est rond</h2>
<p class="lead">Cartes, champs, panneaux et popups gardent des angles à peine adoucis, comme les blocs de la charte ; tout ce qu'on touche du doigt (boutons, puces, contrôles segmentés, jours, avatars) est en pilule ou en cercle, en écho aux demi-cercles du symbole.</p>
<h3>Espacements · grille de 4 px</h3><div class="row sps">{sp}</div>
<h3 class="mt">Arrondis</h3><div class="row rds">{rd}</div>
<h3 class="mt">Aplats et élévation</h3><div class="row shs"><div class="sh" style="box-shadow:var(--shadow-card)">shadow-card<br><small>filet 1 px, cartes au repos</small></div><div class="sh" style="box-shadow:var(--shadow-hover)">shadow-hover<br><small>filet bleu, carte survolée</small></div><div class="sh" style="box-shadow:var(--shadow-pop)">shadow-pop<br><small>menus, infobulles</small></div><div class="sh" style="box-shadow:var(--shadow-dialog)">shadow-dialog<br><small>popups</small></div></div>
<p class="small">Les cartes sont posées à plat sur le gris de page, sans ombre flottante ; seules les couches qui passent au-dessus de la page ont une ombre portée.</p>
<h3 class="mt">Mise en page</h3>
<div class="cols2"><div class="box"><b>Ordinateur (≥ 901 px)</b><p>Barre latérale bleue de 256 px (compte collé en bas), contenu jusqu'à 1 180 px, marges de 32 px, 2 colonnes (contenu + colonne de 360 px).</p></div>
<div class="box"><b>Mobile (≤ 900 px)</b><p>Barre d'en-tête bleue, barre d'onglets en bas (Accueil, Rechercher, Publier, Mes trajets, Profil), marges de 16 px, une colonne.</p></div></div>''', n=9, title="Espaces et formes"))

STAR = '<svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>'
pages.append(page(f'''<p class="eyebrow">06 · Composants</p><h2>Boutons, badges, champs</h2>
<h3>Boutons</h3><div class="row" style="gap:10px"><span class="btn">Principal</span><span class="btn secondary">Demander à rejoindre</span><span class="btn ghost">Secondaire</span><span class="btn danger">Annuler ma place</span><span class="btn success">Accepter</span><span class="btn is-disabled">Désactivé</span></div>
<p class="small">Pilules de 44 px de haut (36 px en petit), texte gras 14 px. Bleu : action principale ; violet : engagement (une fois par écran) ; contour : action secondaire ; rouge : se remplit au survol.</p>
<h3 class="mt">Badges et tags</h3><div class="row" style="gap:8px"><span class="badge">Régulier · L M J V</span><span class="badge line">Ponctuel</span><span class="badge lav">2 places libres sur 3</span><span class="badge wait">2 demandes en attente</span><span class="badge ok">Place confirmée</span><span class="badge ko">Annulé</span>{tg("Non-fumeur", "nosmoke", "conf")}{tg("Musique", "music", "amb")}{tg("À l'heure", "clock", "hor")}</div>
<h3 class="mt">Sélection</h3><div class="row" style="gap:10px"><span class="chip on">8 h – 9 h</span><span class="chip">9 h – 10 h</span><span class="seg"><button class="on">Passager</button><button>Conducteur</button></span><span class="toggle on"></span><span class="toggle"></span>
<span class="days"><span class="on">L</span><span class="on">M</span><span>M</span><span class="on">J</span><span class="on">V</span><span class="off">S</span></span></div>
<h3 class="mt">Notes</h3><div class="row" style="gap:24px"><span class="stars" style="font-size:15px">{STAR}4,9 <span class="n">(38)</span></span>
<span class="rate">{"".join(f'<button class="on">{STAR}</button>' if k < 4 else f'<button>{STAR}</button>' for k in range(5))}</span></div>
<p class="small">Note de 1 à 5 étoiles bleues après chaque trajet, sans commentaire écrit : le passager note le conducteur, le conducteur note chaque passager.</p>
<h3 class="mt">Champs</h3><div class="cols2"><div class="field"><span class="label">Départ</span><div class="select"><button>Noisy-le-Grand · Mont d'Est</button></div><span class="hint">Zones de rendez-vous prédéfinies : jamais d'adresse.</span></div>
<div class="field"><div class="tp-head"><span class="label">Tags (facultatif)</span><span class="tp-count"><b>2</b> / 5</span></div><div class="tp-row">{tg("Calme", "moon", "amb", True, True)}{tg("Discussion", "msg", "amb", True)}{tg("Non-fumeur", "nosmoke", "conf", True, True)}{tg("Bagages", "bag", "conf", True)}</div></div></div>
<p class="small">Champs à angles droits adoucis (4 px), filet gris qui se renforce au survol et devient bleu au focus. Tags : catalogue fixe de 16 tags en 4 familles (ambiance violet, confort turquoise, horaires bleu, profil et accessibilité magenta) ; un tap coche (fond pâle, coche à la place de l'icône), un tap décoche ; 5 au plus sur un trajet.</p>''', n=10, title="Composants"))

pages.append(page(f'''<p class="eyebrow">06 · Composants</p><h2>La carte de trajet</h2>
<p class="lead">Brique centrale des listes. Posée à plat sur le gris de page avec un filet ; toute la carte est cliquable : au survol, le filet devient bleu et le bouton « Voir le détail » s'anime.</p>
<div class="anat">{img("c-trip", "w100")}</div>
<ol class="legend">
<li><b>Date et type</b> : « Régulier · L M J V » ou « Ponctuel », plus le statut éventuel (place confirmée, demande envoyée).</li>
<li><b>Itinéraire</b> : chaque heure est libellée « Départ » ou « Arrivée estimée », reliée par la route pointillée du logo.</li>
<li><b>Prix et places</b> : prix par passager en bleu UGE, badge violet « x places libres sur y ».</li>
<li><b>Conducteur</b> : nom et note moyenne avec le nombre de notes, sans photo dans la carte.</li>
<li><b>Pied de carte</b> : nombre de demandes en attente, tags du trajet, bouton « Voir le détail ».</li>
</ol>
<div class="box mt"><h3>Ce que la carte ne montre pas</h3><p>Pas d'avatar du conducteur, pas de pourcentage de compatibilité, pas d'adresse. Les tags facultatifs remplacent la compatibilité : ils sont comparés aux préférences cochées par le passager dans son profil.</p></div>''', n=11, title="Carte de trajet"))

pages.append(page(f'''<p class="eyebrow">07 · Motifs</p><h2>Le principe graphique et la route</h2>
<div class="cols2"><div><h3>Principe graphique de l'université</h3><div class="arcs-demo"><span class="pat"></span><span class="carc d1"></span><span class="carc d2"></span><b>On part ensemble ?</b></div>
<p class="small">Charte p. 24-25 : de grands demi-anneaux de la couleur du fond entaillent l'aplat bleu, un anneau blanc translucide fait écho au symbole et une bande du motif (le symbole répété, p. 6) borde le côté gauche. Bandeaux d'accueil, écran de connexion, bas de la barre latérale. Anneaux toujours coupés par les bords, jamais plus de deux par bloc.</p></div>
<div><h3>Loader : la route qui défile</h3><div class="row" style="gap:6px;justify-content:center;flex-wrap:nowrap">{loader_frame(0, 0)}{loader_frame(.33, 1)}{loader_frame(.66, 2)}</div><p class="small">Les tirets du logo continuent vers le bas avec la même perspective et défilent en boucle (0,9 s). À l'arrêt, l'image est identique au logo. Fichier : <code>u-mobility-loader.svg</code> (animation SMIL, sans JavaScript).</p></div></div>
<div class="cols2 mt"><div class="box" style="align-self:start"><h3>Géométrie de la route</h3><p>Mesurée sur les deux tirets du logo : les bords convergent vers un point de fuite (y = 495).</p><ul class="small"><li>demi-largeur = 0,196 × d (d = distance au point de fuite)</li><li>début du tiret n = 84 × 1,94<sup>n</sup></li><li>fin du tiret = début × 1,63</li><li>animation : n → n + s, s de 0 à 1</li></ul></div><div style="display:grid;place-items:center">{geo}</div></div>''', n=12, title="Motifs"))

pages.append(page(f'''<p class="eyebrow">08 · Écrans</p><h2>Version ordinateur</h2>
<div class="shot">{img("d-index", "w100")}<span>Tableau de bord · vue passager (principe graphique dans le bandeau, activité façon GitHub)</span></div>
<div class="shot">{img("d-recherche", "w100")}<span>Rechercher un trajet · zones prédéfinies, tags, filtres</span></div>''', n=13, title="Écrans ordinateur"))
pages.append(page(f'''<p class="eyebrow">08 · Écrans</p><h2>Détail et popups</h2>
<div class="shot">{img("d-trajet", "w100")}<span>Détail du trajet · notes sans avis écrit, demandes en attente</span></div>
<div class="shot">{img("d-demande", "w100")}<span>Popup de demande · jours au choix parmi ceux du conducteur, message facultatif</span></div>''', n=14, title="Écrans ordinateur"))
pages.append(page(f'''<p class="eyebrow">08 · Écrans</p><h2>Version mobile</h2>
<div class="phones"><div class="shot">{img("m-index")}<span>Tableau de bord</span></div><div class="shot">{img("m-recherche")}<span>Recherche</span></div><div class="shot">{img("m-messages")}<span>Messagerie du trajet</span></div></div>
<p class="small">390 × 844 px. En-tête bleu, barre d'onglets en bas avec le bouton Publier au centre. Les popups gardent la largeur de l'écran moins 16 px de chaque côté.</p>''', n=15, title="Écrans mobile"))

pages.append(page(f'''<p class="eyebrow">09 · Règles</p><h2>Accessibilité, sécurité et RGPD</h2>
<div class="cols2">
<div class="box"><h3>Accessibilité</h3><ul><li>Contrastes AA minimum (page 7).</li><li>Focus clavier visible partout ; touche Échap ferme les popups.</li><li>Cibles tactiles de 44 px minimum.</li><li>Statuts : couleur + mot + icône.</li><li>Animations désactivées si l'utilisateur a demandé moins d'animations.</li></ul></div>
<div class="box"><h3>Sécurité</h3><ul><li>Zones de rendez-vous prédéfinies, pas de géolocalisation.</li><li>Messagerie par trajet uniquement, numéros et liens masqués, fermée 24 h après le trajet.</li><li>Signalement d'un compte (depuis les messages) ou d'un trajet, traité par les modérateurs.</li><li>Comptes pseudonymisés côté modération, consultation d'identité journalisée.</li></ul></div>
</div>
<div class="box mt"><h3>RGPD</h3><ul><li><b>Droit d'accès et de portabilité</b> (articles 15 et 20) : bouton « Télécharger mes données » (JSON ou CSV) dans Profil → Confidentialité et données.</li>
<li><b>Droit à l'effacement</b> (article 17) : bouton « Supprimer mon compte et mes données », confirmation en écrivant SUPPRIMER. Les trajets passés restent dans les statistiques sous forme anonyme.</li>
<li><b>Minimisation</b> : pas de plaque d'immatriculation, pas d'adresse, nom réduit à l'initiale pour les autres membres.</li>
<li><b>Statistiques de la direction</b> : consolidées et anonymisées, aucun indicateur pour un groupe de moins de 10 personnes.</li>
<li><b>Polices auto-hébergées</b> : aucune donnée de navigation envoyée à Google Fonts.</li></ul>
<p class="small">À faire valider par le délégué à la protection des données de l'université avant une mise en service réelle.</p></div>''', n=16, title="Règles"))

pages.append(page(f'''<p class="eyebrow">Annexe</p><h2>Fichiers de référence</h2>
<table class="t"><tbody>
<tr><td><code>docs/Charte_Gustave_Eiffel_V2-4.pdf</code></td><td>Charte graphique officielle de l'université : source des couleurs, de la typographie, du logotype et du principe graphique</td></tr>
<tr><td><code>src/assets/uge-logo.svg</code>, <code>uge-logo-blanc.svg</code>, <code>uge-symbole.svg</code></td><td>Logotype et symbole UGE, vectorisés depuis le PDF officiel</td></tr>
<tr><td><code>src/assets/logo-indigo.svg</code>, <code>logo-blanc.svg</code></td><td>Pictogramme U-Mobility (bleu #2F2A85 et blanc)</td></tr>
<tr><td><code>src/assets/u-mobility-loader.svg</code></td><td>Loader animé</td></tr>
<tr><td><code>src/assets/fonts/</code></td><td>Figtree 300 à 800 (woff2, licence OFL), en remplacement de TT Norms®</td></tr>
<tr><td><code>src/styles.css</code></td><td>Tokens (variables CSS du bloc <code>:root</code>) et composants</td></tr>
<tr><td><code>docs/design-system/</code></td><td><code>tokens.json</code>, <code>palettes.md</code> (palette officielle) et <code>README.md</code> (règles d'usage)</td></tr>
</tbody></table>
<div class="box mt"><h3>Points ouverts</h3><ul>
<li><b>Police officielle</b> : obtenir la licence TT Norms® auprès du service communication ; il suffira alors d'ajouter ses <code>@font-face</code>, la pile de polices la prend en premier.</li>
<li><b>Logotype</b> : les SVG ont été vectorisés depuis le PDF ; les remplacer par les fichiers sources fournis par le service communication s'ils sont disponibles.</li>
<li><b>Association des logos</b> : faire valider par le service communication la présence du pictogramme U-Mobility à côté du logotype de l'université.</li>
</ul></div>''', n=17, title="Annexe"))

PCSS = f'''
@page {{ size: A4; margin: 0; }}
html, body {{ margin: 0; background: #fff; }}
body {{ font-family: "Figtree", system-ui, sans-serif; color: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact; font-size: 11.5px; line-height: 17px; }}
.page {{ width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm 20mm; position: relative; overflow: hidden; page-break-after: always; display: flex; flex-direction: column; gap: 10px; }}
.page footer {{ position: absolute; left: 16mm; right: 16mm; bottom: 9mm; display: flex; justify-content: space-between; font-size: 9px; color: {MUTED}; border-top: 1px solid {LINE}; padding-top: 6px; }}
.eyebrow {{ font: 700 11px/14px "Figtree"; color: {VIOLET}; margin: 0; }}
h2 {{ font: 800 26px/31px "Figtree"; margin: 0 0 4px; letter-spacing: -.02em; color: {BRAND}; }}
h3 {{ font: 700 14px/19px "Figtree"; margin: 0 0 6px; }}
.lead {{ font-size: 13px; line-height: 20px; color: #2c3e50; max-width: 160mm; margin: 0 0 6px; }}
.small {{ font-size: 10px; line-height: 15px; color: {MUTED}; margin: 4px 0 0; }}
.mt {{ margin-top: 10px; }}
code {{ white-space: nowrap; font: 500 10px "DejaVu Sans Mono", monospace; color: {BRAND}; background: {SOFT}; padding: 1px 4px; border-radius: 3px; }}
ul {{ margin: 0; padding-left: 16px; display: grid; gap: 4px; }}
.cols2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
.cols3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
.box {{ background: {SURF}; border-radius: 6px; padding: 12px 14px; }}
.box p {{ margin: 0; }}
.t {{ width: 100%; border-collapse: collapse; font-size: 10.5px; }}
.t th {{ text-align: left; font: 700 10px/12px "Figtree"; color: {MUTED}; padding: 0 8px 6px; border-bottom: 1px solid {LINE}; }}
.t td {{ padding: 6px 8px; border-bottom: 1px solid {SOFT}; vertical-align: middle; }}
.num {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
.pair {{ display: inline-grid; place-items: center; width: 32px; height: 22px; border-radius: 4px; font: 800 12px "Figtree"; }}
.w100 {{ width: 100%; display: block; border-radius: 6px; box-shadow: 0 0 0 1px {LINE}; }}
/* couverture : bande du motif, demi-anneaux, titre Light en capitales (comme la charte V2.4) */
.cover {{ background: {BRAND}; color: #fff; padding: 0; }}
.cover-pat {{ position: absolute; left: 0; top: 0; bottom: 0; width: 17mm; background: var(--pattern) -30px 6px / 92px 92px repeat-y; opacity: .2; }}
.carc {{ position: absolute; border-radius: 50%; border-style: solid; }}
.c1 {{ width: 560px; height: 560px; right: -300px; top: 260px; border-width: 130px; border-color: rgba(255,255,255,.14); }}
.c2 {{ width: 360px; height: 360px; left: 150px; top: -240px; border-width: 80px; border-color: rgba(255,255,255,.14); }}
.c3 {{ position: absolute; left: 90px; bottom: -200px; }}
.cover-logo {{ position: absolute; left: 32mm; top: 50mm; }}
.cover-t {{ position: absolute; left: 32mm; top: 138mm; }}
.cover-t h1 {{ font: 300 54px/58px "Figtree"; margin: 0; letter-spacing: -.01em; color: #fff; text-transform: uppercase; }}
.cover-t .v {{ font: 700 16px/22px "Figtree"; margin: 18px 0 0; }}
.cover-t .s {{ font-size: 13px; line-height: 20px; color: #D6D5EA; margin: 30px 0 0; }}
.cover-uge {{ position: absolute; left: 32mm; top: 232mm; }}
/* couleurs */
.swatches {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px 14px; }}
.sw {{ display: grid; grid-template-columns: 64px 1fr; gap: 10px; align-items: center; }}
.chip-c {{ height: 52px; border-radius: 6px; display: grid; align-items: end; padding: 6px; font: 700 9px "Figtree"; }}
.sw .meta b {{ font: 700 12px "Figtree"; display: block; }}
.sw .meta span {{ font-size: 9.5px; color: {MUTED}; }}
.sw .meta p {{ margin: 2px 0 0; font-size: 9.5px; line-height: 13px; }}
.ratio {{ display: flex; height: 30px; border-radius: 6px; overflow: hidden; margin-top: 8px; }}
.ratio i {{ display: grid; place-items: center; color: #fff; font: 700 10px "Figtree"; font-style: normal; }}
.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
.stc {{ display: grid; gap: 3px; font-size: 10px; color: {MUTED}; justify-items: start; }}
.stc b {{ font: 700 12px "Figtree"; color: {INK}; }}
/* palette officielle */
.offp {{ display: grid; grid-template-columns: 62mm 1fr; gap: 14px; align-items: stretch; }}
.offp .box {{ display: grid; gap: 6px; align-content: center; }}
.offg {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px 10px; }}
.off {{ display: grid; gap: 6px; }}
.offc {{ height: 30mm; border-radius: 6px; padding: 8px; display: flex; flex-direction: column; justify-content: space-between; }}
.offc b {{ font: 800 12px/15px "Figtree"; }}
.offc span {{ font: 600 9px/12px "DejaVu Sans Mono", monospace; opacity: .95; }}
.off.big .offc {{ height: 40mm; }}
.off.big .offc b {{ font-size: 16px; line-height: 20px; }}
.offm {{ display: grid; font-size: 9px; line-height: 13px; color: {MUTED}; }}
.offm b {{ font: 700 11px "Figtree"; color: {INK}; }}
/* logos */
.logo-tile {{ border-radius: 8px; height: 62mm; display: grid; place-items: center; align-content: center; gap: 12px; }}
.logo-tile.sm {{ height: 38mm; }}
.logo-tile span {{ font-size: 10px; }}
.logo-tile.light {{ background: #fff; box-shadow: inset 0 0 0 1px {LINE}; color: {MUTED}; }}
.logo-tile.dark {{ background: {BRAND}; color: #D6D5EA; }}
.protect {{ background: {SURF}; border-radius: 6px; padding: 14px; display: grid; place-items: center; }}
.protect .zone {{ padding: 16px; outline: 1.5px dashed {ROUGE}; outline-offset: 0; background: #fff; }}
.protect .zone.uz {{ padding: 9mm; }}
.symtile {{ width: 64px; height: 64px; border-radius: 50%; background: {BRAND}; display: grid; place-items: center; }}
.assoc {{ background: {BRAND}; border-radius: 6px; padding: 16px 18px; display: grid; gap: 26px; color: #fff; }}
.assoc b {{ display: block; font: 800 16px/20px "Figtree"; }}
.assoc small {{ display: block; font-size: 10px; color: #D6D5EA; }}
.nope {{ width: 70px; height: 70px; border-radius: 6px; background: {SURF}; display: grid; place-items: center; position: relative; }}
.nope.w {{ width: 96px; }}
.nope::after {{ content: ""; position: absolute; inset: 8px; background: linear-gradient(45deg, transparent calc(50% - 1.5px), {ROUGE} calc(50% - 1.5px), {ROUGE} calc(50% + 1.5px), transparent calc(50% + 1.5px)); }}
.nope > span {{ position: absolute; bottom: -16px; font-size: 9px; color: {MUTED}; white-space: nowrap; }}
.nope .serif {{ font: 700 10px/11px Georgia, "Times New Roman", serif; color: {BRAND}; position: static; }}
/* typo */
.spec-big {{ background: {SURF}; border-radius: 6px; padding: 12px 16px; display: grid; grid-template-columns: auto auto 1fr; gap: 10px; align-items: center; font-family: Figtree; }}
.spec-big span {{ font-size: 64px; line-height: 64px; color: {BRAND}; }}
.spec-big p {{ margin: 0; font-size: 10.5px; color: {MUTED}; }}
td.spec {{ color: {INK}; }}
/* espaces */
.sps {{ gap: 18px; align-items: flex-end; }}
.sp {{ display: grid; justify-items: center; gap: 4px; font-size: 9.5px; }}
.sp i {{ background: {VIOLET}; display: block; }}
.rds {{ gap: 16px; }}
.rd {{ display: grid; justify-items: center; gap: 3px; font-size: 9.5px; }}
.rd i {{ width: 70px; height: 50px; background: {SOFT}; border: 2px solid {BRAND}; display: block; }}
.rd span {{ color: {MUTED}; }}
.shs {{ gap: 18px; background: {SURF}; padding: 18px; border-radius: 6px; }}
.sh {{ background: #fff; border-radius: 6px; padding: 14px 16px; font: 700 11px "Figtree"; }}
.sh small {{ font-weight: 400; color: {MUTED}; }}
/* composants (réutilise styles.css) */
.select > button {{ width: 100%; min-height: 40px; border: 1px solid {LINE}; border-radius: 4px; background: #fff; text-align: left; padding: 0 12px; }}
.anat {{ background: {SURF}; border-radius: 8px; padding: 12px; }}
.legend {{ margin: 6px 0 0; padding-left: 18px; display: grid; gap: 5px; font-size: 11px; }}
.arcs-demo {{ height: 160px; background: {BRAND}; border-radius: 8px; position: relative; overflow: hidden; }}
.arcs-demo .pat {{ position: absolute; left: 0; top: 0; bottom: 0; width: 14px; background: var(--pattern) -14px 4px / 28px 28px repeat-y; opacity: .2; }}
.arcs-demo b {{ position: absolute; left: 30px; bottom: 22px; color: #fff; font: 800 20px/24px "Figtree"; letter-spacing: -.02em; }}
.d1 {{ width: 230px; height: 230px; right: -80px; top: -130px; border-width: 50px; border-color: #fff; }}
.d2 {{ width: 170px; height: 170px; right: 110px; bottom: -120px; border-width: 36px; border-color: rgba(255,255,255,.14); }}
.shot {{ display: grid; gap: 5px; }}
.shot span {{ font-size: 10px; color: {MUTED}; }}
.phones {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
.phones img {{ width: 100%; border-radius: 16px; box-shadow: 0 0 0 5px {INK}; }}
'''
html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Charte graphique U-Mobility</title>
<style>{fonts}</style><style>{css}</style><style>{PCSS}</style></head><body>{"".join(pages)}</body></html>'''
out_html = os.path.join(HERE, "charte.html")  # (ignoré par git)
open(out_html, "w").write(html)
print("html ok", len(pages), "pages")
