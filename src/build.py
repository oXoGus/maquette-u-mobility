#!/usr/bin/env python3
"""U-Mobility v3 — génère le site statique (export Figma) et l'aperçu artifact (une page)."""
import os, base64, random, datetime, shutil, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))                 # src/
EXPORT = os.environ.get("OUT", os.path.join(ROOT, "..", "dist"))  # dist/ (généré, ignoré par git)
ASSETS = os.path.join(ROOT, "assets")

# ------------------------------------------------------------------ icons
P = {
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "ticket": '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z"/><path d="M14 7v10"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2.5 20c1-3.5 3.5-5.5 6.5-5.5s5.5 2 6.5 5.5"/><path d="M16 14.5c2.5 0 4.5 1.5 5.5 4.5"/>',
    "msg": '<path d="M4 5h16v11H9l-5 4z"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "leaf": '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19l7-7"/>',
    "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "history": '<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/><path d="M12 8v4l3 2"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>',
    "trash": '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "filter": '<path d="M4 5h16M7 12h10M10 19h4"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "chevr": '<path d="M9 6l6 6-6 6"/>',
    "repeat": '<path d="M17 2l3 3-3 3"/><path d="M4 11V9a4 4 0 0 1 4-4h12"/><path d="M7 22l-3-3 3-3"/><path d="M20 13v2a4 4 0 0 1-4 4H4"/>',
    "eyeoff": '<path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c6 0 9.5 7 9.5 7a17 17 0 0 1-3 3.8M6.1 6.1C3.9 7.6 2.5 12 2.5 12S6 19 12 19a9 9 0 0 0 4-.9"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/>',
    "eye": '<path d="M2.5 12S6 5 12 5s9.5 7 9.5 7-3.5 7-9.5 7S2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M4 20h16"/>',
    "logout": '<path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h11"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    "route": '<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H16a3.5 3.5 0 0 0 0-7H8a3.5 3.5 0 0 1 0-7h7.5"/>',
    "send": '<path d="M4 12l16-8-6 16-2-7z"/>',
    "swap": '<path d="M7 4v16M3 8l4-4 4 4M17 20V4M13 16l4 4 4-4"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "join": '<circle cx="10" cy="8" r="4"/><path d="M3 21c1.2-4 4-6 7-6 1.4 0 2.7.4 3.8 1.2"/><path d="M19 15v6M16 18h6"/>',
    "leave": '<circle cx="10" cy="8" r="4"/><path d="M3 21c1.2-4 4-6 7-6 1.4 0 2.7.4 3.8 1.2"/><path d="M16 18h6"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
    "wheel": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/><path d="M3.5 10.5h6M14.5 10.5h6M12 14.5V21"/>',
    "seat": '<path d="M7 3h3.5l1.8 9H18a2 2 0 0 1 2 2v3H9.8z"/><path d="M9.8 17 8.5 21M17.5 17v4"/>',
    "bike": '<circle cx="5.5" cy="16.5" r="3.5"/><circle cx="18.5" cy="16.5" r="3.5"/><path d="M5.5 16.5 9 9h7l2.5 7.5"/><path d="M9 9l3.5 7.5L16 9"/><path d="M8 6h2.5"/><path d="M15 6h2l-1 3"/>',
    "walk": '<circle cx="13.5" cy="4" r="2"/><path d="M12.5 8 11 14"/><path d="M11 14l-2.5 7"/><path d="M11 14l3 3 1 4"/><path d="M12.3 9 9 11l-1 3"/><path d="M12.3 9l2.7 3 3 .5"/>',
    "bus": '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 10h16"/><path d="M7.5 14h.01M16.5 14h.01"/><path d="M7 18v2.5M17 18v2.5"/><path d="M9 6.5h6"/>',
    "grid": '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
    "campus": '<path d="M3 10l9-5 9 5-9 5z"/><path d="M7 12.5V17c1.5 1.5 3 2 5 2s3.5-.5 5-2v-4.5"/><path d="M21 10v5"/>',
    "hourglass": '<path d="M6 3h12M6 21h12M7 3c0 5 10 5 10 9s-10 4-10 9M17 3c0 5-10 5-10 9s10 4 10 9"/>',
    # Icônes des tags (catalogue TAGS)
    "moon": '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>',
    "music": '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    "book": '<path d="M12 6.5C10 5 7 4.5 3.5 4.5v14c3.5 0 6.5.5 8.5 2 2-1.5 5-2 8.5-2v-14c-3.5 0-6.5.5-8.5 2z"/><path d="M12 6.5V20"/>',
    "nosmoke": '<path d="M3 3l18 18"/><path d="M11 12H3v4h12"/><path d="M19 12h2v4h-2"/><path d="M8 12v4"/><path d="M18 8c0-2.5-2-2.5-2-5M21.5 8c0-2.5-2-2.5-2-5"/>',
    "paw": '<circle cx="5" cy="10.5" r="1.8"/><circle cx="9.2" cy="5.8" r="1.8"/><circle cx="14.8" cy="5.8" r="1.8"/><circle cx="19" cy="10.5" r="1.8"/><path d="M12 11.5c-2.8 0-5.5 4.2-5.5 6.8 0 1.4.9 2.2 2.2 2.2 1.2 0 2-.7 3.3-.7s2.1.7 3.3.7c1.3 0 2.2-.8 2.2-2.2 0-2.6-2.7-6.8-5.5-6.8z"/>',
    "bag": '<rect x="4" y="7" width="16" height="13" rx="2"/><path d="M9 7V4h6v3"/><path d="M9 11v5M15 11v5"/>',
    "snow": '<path d="M12 2v20M3.5 7l17 10M20.5 7l-17 10"/><path d="M9.5 3.5 12 6l2.5-2.5M9.5 20.5 12 18l2.5 2.5"/>',
    "female": '<circle cx="12" cy="9" r="5.5"/><path d="M12 14.5V22M8.5 18.5h7"/>',
    "access": '<circle cx="12" cy="4" r="2"/><path d="M12 7.5V13h5l2 6"/><path d="M12 10h4.5"/><path d="M9 10.5a6 6 0 1 0 7.8 8"/>',
}
ACT = ' class="active"'
STAR_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>'


def i(name, cls=""):
    return f'<svg class="i {cls}" data-i="{name}" viewBox="0 0 24 24" aria-hidden="true">{P[name]}</svg>'


def stars(avg, n=None):
    tail = f' <span class="n">({n})</span>' if n else ""
    return f'<span class="stars">{STAR_SVG}{avg}{tail}</span>'


def stars5(k):
    """k étoiles pleines sur 5 (note donnée)."""
    out = "".join(f'<svg viewBox="0 0 24 24" style="{"" if j < k else "fill:var(--line-strong)"}"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>' for j in range(5))
    return f'<span class="stars" aria-label="{k} sur 5">{out}</span>'


def rate(id_, value=0):
    btns = "".join(f'<button type="button" aria-label="{k} étoile{"s" if k > 1 else ""}">{STAR_SVG}</button>' for k in range(1, 6))
    return f'<div class="row" style="gap:8px"><div class="rate" id="{id_}" data-value="{value}">{btns}</div><span class="rate-label">Choisis une note</span></div>'


DAYS = ["L", "M", "M", "J", "V", "S", "D"]
DAYS_FULL = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def days(on, pick=True, allowed=None, mini=False):
    out = []
    for k, d in enumerate(DAYS):
        cls = []
        if k in on: cls.append("on")
        if allowed is not None and k not in allowed: cls.append("off")
        c = f' class="{" ".join(cls)}"' if cls else ""
        tag = "button" if pick else "span"
        extra = f' type="button" aria-label="{DAYS_FULL[k]}"' if pick else f' title="{DAYS_FULL[k]}"'
        out.append(f"<{tag}{c}{extra}>{d}</{tag}>")
    return f'<div class="days{" mini" if mini else ""}">{"".join(out)}</div>'


ZONES_DEP = ["Noisy-le-Grand · Mont d'Est", "Noisy-Champs · Gare RER A", "Champs-sur-Marne · Nesles", "Torcy · Centre",
             "Lognes · Mandinet", "Chelles · Gare", "Bussy-Saint-Georges · Centre", "Val d'Europe · Serris"]
ZONES_CAMPUS = ["Cité Descartes · Copernic", "Cité Descartes · Bienvenüe", "Cité Descartes · Lavoisier", "Cité Descartes · Bois de l'Étang"]
# Chaque campus a ses propres points d'arrivée (bâtiments) et zones de rendez-vous. Le campus se choisit dans le profil.
CAMPUSES = [
    ("Marne-la-Vallée · Cité Descartes", ZONES_CAMPUS, ZONES_DEP),
    ("Lille · Villeneuve-d'Ascq", ["Villeneuve-d'Ascq · Site Cité scientifique", "Villeneuve-d'Ascq · Bâtiment Recherche"],
     ["Lille · Gare Lille-Flandres", "Villeneuve-d'Ascq · Pont de Bois", "Roubaix · Grand-Place", "Hellemmes · Mairie"]),
    ("Lyon · Bron", ["Bron · Site Porte des Alpes", "Bron · Bâtiment Transports"],
     ["Lyon · Part-Dieu", "Villeurbanne · Gratte-Ciel", "Vénissieux · Centre", "Bron · Mairie"]),
    ("Nantes · Bouguenais", ["Bouguenais · Site de la route de Bouaye"],
     ["Nantes · Gare Sud", "Rezé · Pont-Rousseau", "Saint-Herblain · Atlantis", "Bouguenais · Centre"]),
    ("Versailles · Satory", ["Versailles · Site de Satory"],
     ["Versailles · Gare Chantiers", "Saint-Cyr-l'École · Gare", "Guyancourt · Centre"]),
]
CAMPUS = CAMPUSES[0][0]


def select(id_, value, icon="pin", groups=None, dyn=None, attrs=""):
    """Liste déroulante. dyn = "arr" | "dep" : options de tous les campus (data-campus), seules celles du campus courant sont visibles."""
    opts = ""
    if dyn:
        for name, pts, zones in CAMPUSES:
            hid = "" if name == CAMPUS else " hidden"
            g, items = ("Sur le campus", pts) if dyn == "arr" else ("Zones de rendez-vous", zones)
            dc = f' data-campus="{H.escape(name)}"'
            opts += f'<div class="grp"{dc}{hid}>{g}</div>' + "".join(
                f'<button type="button" class="opt{" sel" if it == value else ""}"{dc}{hid}>{H.escape(it)}</button>' for it in items)
    else:
        groups = groups or [("Sur le campus", ZONES_CAMPUS), ("Zones de rendez-vous", ZONES_DEP)]
        for g, items in groups:
            opts += f'<div class="grp">{g}</div>' + "".join(
                f'<button type="button" class="opt{" sel" if it == value else ""}">{H.escape(it)}</button>' for it in items)
    return (f'<div class="select" id="{id_}"{attrs}><button type="button" aria-haspopup="listbox">{i(icon, "sm")}<span>{H.escape(value)}</span>{i("chev", "sm chev")}</button>'
            f'<div class="options" role="listbox">{opts}</div></div>')


def inp(id_, value="", ph="", icon=None, typ="text"):
    ic = i(icon, "sm") if icon else ""
    return f'<div class="input">{ic}<input id="{id_}" type="{typ}" value="{H.escape(value)}" placeholder="{H.escape(ph)}"></div>'


def textarea(id_, ph, maxlength=140, value=""):
    return (f'<div class="input"><textarea id="{id_}" maxlength="{maxlength}" placeholder="{H.escape(ph)}">{H.escape(value)}</textarea></div>'
            f'<span class="counter">{len(value)} / {maxlength}</span>')


# ------------------------------------------------------------------ tags
# Catalogue fixe : les utilisateurs ne créent pas de tags, ils les choisissent.
# Une couleur par famille (.f-amb violet, .f-conf turquoise, .f-hor bleu, .f-acc magenta) ;
# modes = où le tag a du sens (Publier ne propose que ceux du mode choisi) ;
# groupe = tags qui s'excluent (cocher l'un décoche l'autre).
TAG_FAMS = {"amb": "Ambiance", "conf": "Confort et règles", "hor": "Horaires et souplesse", "acc": "Profil et accessibilité"}
ALLM = ("car", "bike", "walk", "transit")
TAGS = {  # libellé: (icône, famille, modes, groupe)
    "Calme": ("moon", "amb", ALLM, "ambiance"),
    "Discussion": ("msg", "amb", ALLM, "ambiance"),
    "Musique": ("music", "amb", ("car",), ""),
    "Révisions": ("book", "amb", ("transit", "walk"), ""),
    "Non-fumeur": ("nosmoke", "conf", ("car",), ""),
    "Animaux acceptés": ("paw", "conf", ("car", "walk"), ""),
    "Bagages": ("bag", "conf", ("car",), ""),
    "Vélo dans le coffre": ("bike", "conf", ("car",), ""),
    "Climatisation": ("snow", "conf", ("car",), ""),
    "À l'heure": ("clock", "hor", ALLM, "horaire"),
    "Souple sur l'horaire": ("hourglass", "hor", ALLM, "horaire"),
    "Détour possible": ("route", "hor", ("car", "bike"), ""),
    "Retour possible": ("swap", "hor", ALLM, ""),
    "Entre filles": ("female", "acc", ALLM, ""),
    "Accessible PMR": ("access", "acc", ("car", "transit"), ""),
    "Débutant bienvenu": ("leaf", "acc", ("bike", "walk"), ""),
}
TAG_MAX = 5  # tags au plus sur un trajet publié


def tag(x):
    """Tag affiché (lecture seule) : icône + libellé ; sur une carte de trajet étroite, l'icône seule (libellé en infobulle)."""
    ic, fam, _, _ = TAGS[x]
    return f'<span class="tag f-{fam}" data-tip="{H.escape(x)}">{i(ic)}<span class="tl">{H.escape(x)}</span></span>'


def tags_static(tags, limit=None):
    shown = tags if limit is None else tags[:limit]
    more = f'<span class="tag more" aria-label="{len(tags) - limit} autres tags">+{len(tags) - limit}</span>' if limit is not None and len(tags) > limit else ""
    return "".join(tag(x) for x in shown) + more


def tagpick(id_, sel, mode=None, max_=None, flat=False):
    """Choix de tags dans le catalogue : un tap coche, un tap décoche.
    mode : Publier, n'affiche que les tags du mode (data-when="mode:…", mis à jour par app.js) ;
    max_ : limite (au-delà, les puces restantes sont désactivées) ; flat : une seule rangée, tags cochés en tête (Recherche)."""
    def chip(x):
        ic, fam, modes, grp = TAGS[x]
        on = x in sel
        when = f' data-when="{" ".join("mode:" + m for m in modes)}"' if mode and set(modes) != set(ALLM) else ""
        hid = " hidden" if mode and mode not in modes else ""
        g = f' data-group="{grp}"' if grp else ""
        return (f'<button type="button" class="tagchip f-{fam}{" on" if on else ""}" aria-pressed="{"true" if on else "false"}"{g}{when}{hid}>'
                f'<span class="ic">{i(ic)}</span><span class="ck">{i("check")}</span>{H.escape(x)}</button>')
    mx = f' data-max="{max_}"' if max_ else ""
    if flat:
        return f'<div class="tagpick flat" id="{id_}"{mx} role="group" aria-label="Tags"><div class="tp-row">{"".join(chip(x) for x in sorted(TAGS, key=lambda x: x not in sel))}</div></div>'
    fams = ""
    for f, lbl in TAG_FAMS.items():
        xs = [x for x in TAGS if TAGS[x][1] == f]
        modes = {m for x in xs for m in TAGS[x][2]}
        when = f' data-when="{" ".join("mode:" + m for m in ALLM if m in modes)}"' if mode and modes != set(ALLM) else ""
        hid = " hidden" if mode and mode not in modes else ""
        fams += (f'<div class="tp-fam f-{f}" role="group" aria-label="{lbl}"{when}{hid}><span class="tp-lbl">{lbl}</span>'
                 f'<div class="tp-row">{"".join(chip(x) for x in xs)}</div></div>')
    return f'<div class="tagpick" id="{id_}"{mx}>{fams}</div>'


def tp_head(label, sel, max_=None, clear=False):
    """Libellé d'un choix de tags + compteur « n / max » (jaune) ou lien « Effacer »."""
    right = f'<span class="tp-count"><b>{len(sel)}</b> / {max_}</span>' if max_ else ""
    if clear:
        right = f'<button class="linkbtn tp-clear" type="button"{"" if sel else " hidden"}>Effacer</button>'
    return f'<div class="tp-head"><span class="label">{label}</span>{right}</div>'


# ------------------------------------------------------------------ trip card
COMMISSION = 0.19  # commission U-Mobility par passager et par trajet, incluse dans le prix affiché (voiture seulement)

def euros(v):
    return f"{v:.2f}".replace(".", ",") + " €"

def driver_share(price):
    """Part reversée au conducteur : prix payé par le passager moins la commission."""
    return euros(float(price.replace(" €", "").replace(",", ".")) - COMMISSION)

# Modes de déplacement : une couleur secondaire UGE par mode (classes .m-car, .m-bike…).
# Seule la voiture a un prix et des places limitées ; les autres modes affichent le nombre de personnes qui ont rejoint.
MODES = {
    "car": ("Voiture", "car"),
    "bike": ("Vélo", "bike"),
    "walk": ("À pied", "walk"),
    "transit": ("Transports en commun", "bus"),
}

def mode_tag(mode, short=False):
    label, ic = MODES[mode]
    return f'<span class="mode m-{mode}">{i(ic)}{"TC" if short and mode == "transit" else label}</span>'

def role_tag(role, mode="car"):
    """Rôle de l'utilisateur dans le trajet : turquoise = conducteur / organisateur, magenta = passager / participant."""
    if mode == "car":
        return (f'<span class="role-tag d">{i("wheel")}Conducteur</span>' if role == "d"
                else f'<span class="role-tag p">{i("seat")}Passager</span>')
    return (f'<span class="role-tag d">{i("route")}Organisateur</span>' if role == "d"
            else f'<span class="role-tag p">{i("join")}Participant</span>')

PAX_POOL = ["IN", "TK", "CL", "AS", "HP", "YB"]

def seats(free, total, pax=None):
    """Passagers déjà acceptés (avatars) + places vides (cercles pointillés)."""
    pax = list(pax) if pax is not None else PAX_POOL[:total - free]
    av = "".join(f'<span class="avatar xs">{x}</span>' for x in pax) + '<span class="seat-free" aria-hidden="true"></span>' * free
    return f'<span class="pax" role="img" aria-label="{len(pax)} passager{"s" if len(pax) > 1 else ""} sur {total}">{av}</span>'

def joined(pax):
    """Modes sans voiture : pas de limite de places, on montre qui a rejoint."""
    n = len(pax)
    av = "".join(f'<span class="avatar xs">{x}</span>' for x in pax[:4]) + (f'<span class="more-pax">+{n - 4}</span>' if n > 4 else "")
    return (f'<span class="pax" aria-hidden="true">{av}</span>'
            f'<span class="badge joined">{i("users","sm")}{n} personne{"s" if n > 1 else ""} {"ont" if n > 1 else "a"} rejoint</span>')

def trip(date, kind, dep_t, dep, arr_t, arr, price, free, total, pending, driver, rating, nr, tags=(),
         href="trajet.html", status="", actions=None, go=True, role=None, pax=None, mode="car", cancel="", sent=False):
    car = mode == "car"
    me = driver == "Toi"
    tags = [x for x in tags if mode in TAGS[x][2]]  # un tag hors de son mode n'a pas de sens (ex. Non-fumeur à vélo)
    if not car:
        role = None  # hors voiture : le mode (et sa couleur) suffit, pas d'étiquette Passager / Conducteur
    if me and href == "trajet.html":
        href = "mon-trajet.html"  # l'utilisateur conduit : vue conducteur (passagers, demandes)
    kind_b = f'<span class="badge reg">{i("repeat","sm")}Régulier · {kind}</span>' if kind != "Ponctuel" else '<span class="badge line">Ponctuel</span>'
    if sent:
        pend = f'<span class="badge line">{i("clock","sm")}Réponse attendue sous 18 h</span>'
    elif not car:
        pend = '<span class="badge line">Sans limite de places</span>'
    elif pending:
        pend = f'<span class="badge wait">{i("hourglass","sm")}{pending} demande{"s" if pending > 1 else ""} en attente</span>'
    else:
        pend = '<span class="badge line">Aucune demande en attente</span>'
    top = f'<div class="trip-top">{mode_tag(mode)}{role_tag(role, mode) if role else ""}<span class="date">{date}</span>{kind_b}{status}</div>'
    route = (f'<ol class="troute"><li><time>{dep_t}</time><span class="dot"></span><span class="place"><small>Départ</small><b>{H.escape(dep)}</b></span></li>'
             f'<li><time>{arr_t}</time><span class="dot"></span><span class="place"><small>Arrivée estimée</small><b>{H.escape(arr)}</b></span></li></ol>')
    if car:
        money = (f'<span class="pr"><span class="price">{price}</span> <small class="muted">/ passager</small></span>'
                 + (f'<small class="fee">tu reçois {driver_share(price)} / passager</small>' if me else f'<small class="fee">dont {euros(COMMISSION)} de commission</small>'))
        places = f'<span class="seatline">{seats(free, total, pax)}<span class="badge seats">{free} place{"s" if free > 1 else ""} restante{"s" if free > 1 else ""}</span></span>'
        who = "Tu conduis" if me else f'Conduit par <b>{driver}</b> {stars(rating, nr)}'
    else:
        money = '<span class="free-tag">Gratuit</span>'
        places = f'<span class="seatline">{joined(list(pax or []))}</span>'
        who = "Tu organises" if me else f'Proposé par <b>{driver}</b> {stars(rating, nr)}'
    side = f'<div class="trip-side">{money}{places}<span class="driver-line">{who}</span></div>'
    label = f'Voir le détail du trajet {H.escape(dep)} vers {H.escape(arr)}, {date}'
    go_el = (f'<a class="go" href="{href}" aria-label="{label}">Voir le détail{i("arrow","sm")}</a>' if actions is not None or cancel
             else f'<span class="go">Voir le détail{i("arrow","sm")}</span>') if go else ""
    rc = f" role-{role}" if role else ""
    if actions is not None or cancel:
        # Mes trajets : l'action d'annulation à gauche, « Voir le détail » à droite (lien étiré sur toute la carte).
        acts = f'<div class="trip-actions">{cancel}{actions or ""}{go_el}</div>'
        foot = f'<div class="trip-foot">{pend}{tags_static(tags, 3)}</div>'
        return f'<article class="trip{rc} m-{mode}"><div class="trip-in">{top}<div>{route}</div>{side}{foot}{acts}</div></article>'
    foot = f'<div class="trip-foot">{pend}{tags_static(tags, 3)}{go_el}</div>'
    if not go:
        return f'<div class="trip{rc} m-{mode} static"><div class="trip-in">{top}<div>{route}</div>{side}{foot}</div></div>'
    return f'<a class="trip{rc} m-{mode}" href="{href}" aria-label="{label}"><div class="trip-in">{top}<div>{route}</div>{side}{foot}</div></a>'


# ------------------------------------------------------------------ layout
USER_NAV = [
    ("index", "home", "Tableau de bord"),
    ("recherche", "search", "Rechercher"),
    ("publier", "plus", "Publier un trajet"),
    ("mes-trajets", "ticket", "Mes trajets", "3"),
    ("historique", "history", "Historique"),
    ("messages", "msg", "Messages", "2"),
    ("profil", "user", "Profil"),
]
# Rôles : utilisateur ; modérateur (signalements uniquement) ; administrateur (back office + signalements).
ROLES = {
    "user": ("MD", "Mathis D.", "BUT Informatique · 2e année", "index"),
    "mod": ("KB", "Karim B.", "Modérateur", "moderation"),
    "admin": ("CV", "Claire V.", "Administratrice · Vie étudiante", "back-office"),
}
NAVS = {
    "user": ("", USER_NAV),
    "mod": ("Modération", [("moderation", "flag", "Signalements", "3")]),
    "admin": ("Back office", [("back-office", "chart", "Statistiques"), ("moderation", "flag", "Signalements", "3")]),
}
TABS = {
    "user": [("index", "home", "Accueil"), ("recherche", "search", "Rechercher"), ("publier", "plus", "Publier"),
             ("mes-trajets", "ticket", "Mes trajets"), ("profil", "user", "Profil")],
    "mod": [("moderation", "flag", "Signalements")],
    "admin": [("back-office", "chart", "Statistiques"), ("moderation", "flag", "Signalements")],
}


def nav_html(role, act):
    head, items = NAVS[role]
    out = [f'<div class="nav-label">{head}</div>' if head else ""]
    for it in items:
        key, ic, label = it[:3]
        count = f'<span class="count">{it[3]}</span>' if len(it) > 3 else ""
        cls = ' class="active" aria-current="page"' if key == act else ""
        out.append(f'<a href="{key}.html"{cls}>{i(ic)}{label}{count}</a>')
    return "\n".join(out)


def tabbar_html(role, act):
    out = []
    for k, ic, l in TABS[role]:
        cur = ' class="active" aria-current="page"' if k == act else ""
        out.append(f'<a href="{k}.html" class="plus"><span class="p">{i(ic)}</span>{l}</a>' if ic == "plus"
                   else f'<a href="{k}.html"{cur}>{i(ic, "lg")}{l}</a>')
    if role != "user":  # pas de page Profil : la déconnexion reste accessible en mobile
        out.append(f'<button type="button" data-logout>{i("logout", "lg")}Déconnexion</button>')
    return "".join(out)


def app_page(key, title, body, roles=("user",), active=None, sub="", mtitle=None, back=None, topright=""):
    """Gabarit des pages connectées. Une page peut accepter plusieurs rôles (ex. modération : modérateur et admin) :
    la navigation de chaque rôle est rendue, app.js affiche celle du rôle choisi dans la barre de démo."""
    act = active or key
    views, tabs = "", ""
    for k, r in enumerate(roles):
        ini, name, desc, home = ROLES[r]
        hid = "" if k == 0 else " hidden"
        views += (f'<div class="role-view" data-role-view="{r}"{hid}>'
                  f'<a class="brandmark" href="{home}.html"><img src="assets/logo-blanc.png" alt=""><div><b>U-Mobility</b><span>Université Gustave Eiffel</span></div></a>'
                  f'<nav class="nav" aria-label="Navigation principale">{nav_html(r, act)}</nav>'
                  f'<div class="me"><a class="who" href="{"profil" if r == "user" else home}.html"><span class="avatar sm">{ini}</span><div><b>{name}</b><small>{desc}</small></div></a>'
                  f'<button class="logout" type="button" data-logout>{i("logout","sm")}Se déconnecter</button></div></div>')
        tabs += f'<nav class="tabbar" data-role-view="{r}" aria-label="Navigation mobile"{hid}>{tabbar_html(r, act)}</nav>'
    mleft = (f'<a class="iconbtn" href="{back}.html" aria-label="Retour">{i("back")}</a>' if back
             else '<img src="assets/logo-blanc.png" alt="U-Mobility">')
    bell = f'<a class="iconbtn" href="messages.html" aria-label="Notifications, 2 non lues">{i("bell")}<span class="dot"></span></a>' if "user" in roles else ""
    tr = f'<div class="tr">{topright}</div>' if topright else ""
    return f'''<div class="app" data-roles="{" ".join(roles)}">
<aside class="sidebar">
{views}
</aside>
<main class="main">
<header class="mobilebar">{mleft}<b>{mtitle or title}</b>{bell}</header>
<div class="topbar"><div class="grow"><h1>{title}</h1>{f'<p class="sub">{sub}</p>' if sub else ""}</div>{tr}{bell}</div>
<div class="content">
{body}
</div>
</main>
{tabs}
</div>'''


# Barre de démo (maquette uniquement) : changer de rôle depuis n'importe quelle page + accès au plan de toutes les pages.
DEMOBAR = (f'<div class="demobar" role="toolbar" aria-label="Outils de la maquette"><span class="lbl">Voir en tant que</span>'
           f'<div class="seg"><button type="button" data-role="user">Utilisateur</button><button type="button" data-role="mod">Modérateur</button><button type="button" data-role="admin">Admin</button></div>'
           f'<a class="btn sm light" href="plan.html" title="Toutes les pages de la maquette">{i("grid","sm")}<span>Toutes les pages</span></a></div>')


def modal(id_, content, wide=False, drawer=False):
    if drawer:
        return f'<div class="drawer" id="m-{id_}" role="dialog" aria-modal="true"><div class="panel">{content}</div></div>'
    return f'<div class="modal" id="m-{id_}" role="dialog" aria-modal="true"><div class="dialog{" wide" if wide else ""}">{content}</div></div>'


def dhead(title, sub="", icon="info", red=False):
    return (f'<div class="dialog-head"><span class="ico{" red" if red else ""}">{i(icon)}</span><div class="grow"><h2>{title}</h2>'
            f'{f"<p class=muted>{sub}</p>" if sub else ""}</div><button class="iconbtn" type="button" data-close aria-label="Fermer">{i("x","sm")}</button></div>')


def success(title, text, extra=""):
    return (f'<div class="success-state"><span class="ok">{i("check")}</span><h2>{title}</h2><p class="muted">{text}</p></div>'
            f'<div class="dialog-foot">{extra}<button class="btn" type="button" data-close>Fermer</button></div>')


# ------------------------------------------------------------------ heatmap data
def heatmap(seed, total_hint, weeks=26, role_word="trajets"):
    rnd = random.Random(seed)
    end = datetime.date(2026, 9, 27)  # dimanche
    start = end - datetime.timedelta(days=weeks * 7 - 1)  # lundi
    cells, months, total, streak, best = [], [], 0, 0, 0
    mois = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
    jours = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]
    # Libellé du mois sur la première semaine qui le contient, seulement s'il reste au moins 3 semaines
    # avant le mois suivant (sinon les libellés se collent : « marsavr. »).
    starts = [w for w in range(weeks) if w == 0 or (start + datetime.timedelta(days=w * 7)).month != (start + datetime.timedelta(days=(w - 1) * 7)).month]
    for w in range(weeks):
        wd0 = start + datetime.timedelta(days=w * 7)
        nxt = next((x for x in starts if x > w), weeks)
        show = w in starts and nxt - w >= 3
        months.append(f'<span>{mois[wd0.month - 1] if show else ""}</span>')
        for d in range(7):
            day = wd0 + datetime.timedelta(days=d)
            if day > datetime.date(2026, 9, 24):
                cells.append('<i class="x"></i>'); continue
            vac = datetime.date(2026, 7, 11) <= day <= datetime.date(2026, 8, 30)
            if d >= 5 or vac:
                n = 1 if (d == 5 and not vac and rnd.random() < .08) else 0
            else:
                r = rnd.random()
                n = 0 if r < .22 else (1 if r < .5 else (2 if r < .9 else 3))
                if day.month == 9 and n == 0 and rnd.random() < .7: n = 2
            total += n
            streak = streak + 1 if n else 0
            best = max(best, streak)
            lvl = min(n, 4)
            label = f'{n} trajet{"s" if n > 1 else ""} le {jours[d]} {day.day} {mois[day.month - 1]}' if n else f'Aucun trajet le {jours[d]} {day.day} {mois[day.month - 1]}'
            cells.append(f'<i data-l="{lvl}" data-tip="{label}"></i>')
    lbl = "".join(f"<span>{x}</span>" for x in ["Lun", "", "Mer", "", "Ven", "", ""])
    legend = ('<div class="heat-legend">Moins' + "".join(f'<i style="background:var(--heat-{k})"></i>' for k in range(5)) + 'Plus</div>')
    return total, best, f'''<div class="heat-wrap"><div class="heat" role="img" aria-label="Activité des 6 derniers mois : {total} trajets">
<span></span><div class="months">{"".join(months)}</div>
<div class="days-lbl">{lbl}</div><div class="cells">{"".join(cells)}</div>
</div></div>{legend}'''


def bars(data, now_key, unit="", mx=None, h=130):
    mx = mx or max(v for _, v in data)
    b = "".join(f'<div class="b{" now" if k == now_key else ""}" data-tip="{k} : {v}{unit}"><em>{v}</em><i style="height:{max(3, round(v / mx * h))}px"></i></div>' for k, v in data)
    x = "".join(f"<span>{k}</span>" for k, _ in data)
    return f'<div class="chart"><div class="bars">{b}</div><div class="bars-x">{x}</div></div>'


def hbars(data, suffix=" %", scale=None):
    """data : (libellé, valeur) ou (libellé, valeur, mode) ; avec un mode, la barre prend la couleur du mode."""
    scale = scale or max(d[1] for d in data)
    out = ""
    for d in data:
        k, v = d[0], d[1]
        m = d[2] if len(d) > 2 else None
        lbl = f'<span class="hk">{i(MODES[m][1], "sm")}{k}</span>' if m else f'<span>{k}</span>'
        out += f'<div class="hbar{" m-" + m if m else ""}">{lbl}<span class="t"><i style="width:{v / scale * 100:.0f}%"></i></span><b>{v}{suffix}</b></div>'
    return out


PAGES = {}  # key -> dict(title, app, modals, raw)

# Logotype officiel Université Gustave Eiffel, version monochrome blanc (charte V2.4 p. 10-11 : fonds foncés).
# Vectorisé depuis docs/Charte_Gustave_Eiffel_V2-4.pdf ; inséré en ligne pour que l'aperçu reste autonome.
UGE_BLANC = open(os.path.join(ASSETS, "uge-logo-blanc.svg"), encoding="utf-8").read().replace("<svg ", '<svg class="uge" ', 1)

# ================================================================== CONNEXION
PAGES["connexion"] = dict(title="Connexion", raw=True, modals="", app=f'''<div class="auth">
<section class="side">
<div class="pattern" aria-hidden="true"></div>
<span class="arc a1" aria-hidden="true"></span><span class="arc a2" aria-hidden="true"></span>
<div class="brandmark" style="padding-left:24px"><img src="assets/logo-blanc.png" alt=""><div><b>U-Mobility</b><span>Université Gustave Eiffel</span></div></div>
<div style="display:grid;gap:16px;padding-left:24px">
<h1>Covoiturage<br>étudiant</h1>
<p>Partage tes trajets vers le campus avec des étudiants et personnels de l'université. Moins de CO₂, plus de rencontres.</p>
</div>
<div style="padding-left:24px">{UGE_BLANC}</div>
</section>
<section class="form"><div>
<h1>Connexion</h1>
<p class="muted">Utilise ton compte universitaire ou un compte de démonstration.</p>
<div class="field"><label for="login-mail">Adresse e-mail universitaire</label>{inp("login-mail", "", "prenom.nom@edu.univ-eiffel.fr", "user", "email")}</div>
<div class="field"><label for="login-pass">Mot de passe</label>{inp("login-pass", "", "••••••••••", "lock", "password")}</div>
<a class="btn block" href="index.html">Se connecter</a>
<p class="small muted" style="text-align:center">Comptes de démonstration (POC)</p>
<div class="demo">
<a href="index.html" data-set-role="user"><span class="avatar sm">MD</span><div class="grow"><b>Étudiant · passager et conducteur</b><small>mathis.demo@u-mobility.fr</small></div>{i("arrow","sm")}</a>
<a href="moderation.html" data-set-role="mod"><span class="avatar sm">KB</span><div class="grow"><b>Modérateur · signalements</b><small>moderation.demo@u-mobility.fr</small></div>{i("arrow","sm")}</a>
<a href="back-office.html" data-set-role="admin"><span class="avatar sm">CV</span><div class="grow"><b>Administrateur · back office et modération</b><small>admin.demo@u-mobility.fr</small></div>{i("arrow","sm")}</a>
</div>
</div></section>
</div>''')

# ================================================================== TABLEAU DE BORD
# Une seule vue : chaque utilisateur est à la fois passager et conducteur.
tot_a, best_a, heat_a = heatmap(7, 0)
PAGES["index"] = dict(title="Tableau de bord", mtitle="U-Mobility", app=None, modals="", body=f'''
<section class="hero">
<span class="arc a1" aria-hidden="true"></span><span class="arc a2" aria-hidden="true"></span>
<h1>Bonjour Mathis, où vas-tu aujourd'hui ?</h1>
<p>Prochain trajet : demain, départ 7 h 50 de Noisy-le-Grand · Mont d'Est, arrivée 8 h 20 à Cité Descartes · Copernic. 2 passagers attendent ta réponse pour ton trajet du vendredi.</p>
<div class="cta"><a class="btn light" href="recherche.html">{i("search","sm")}Rechercher un trajet</a><a class="btn secondary" href="publier.html">{i("plus","sm")}Publier un trajet</a></div>
</section>
<div class="grid-4">
<div class="stat dark"><span class="k">{i("route","sm")}Trajets effectués</span><span class="v">42</span><span class="d m">28 en passager · 14 en conducteur</span></div>
<div class="stat"><span class="k">{i("leaf","sm")}CO₂ évité</span><span class="v">116 <small>kg</small></span><span class="d">+27 kg ce mois-ci</span></div>
<div class="stat"><span class="k">{i("users","sm")}Personnes rencontrées</span><span class="v">19</span><span class="d m">conducteurs et passagers</span></div>
<div class="stat"><span class="k">{i("star","sm")}Ma note</span><span class="v">4,8 <small>/ 5</small></span><span class="d m">48 notes reçues</span></div>
</div>
<section class="card">
<div class="card-head"><div><h2>Mon activité</h2><p class="small muted">{tot_a} trajets sur les 6 derniers mois, en passager et en conducteur · plus longue série : {best_a} jours</p></div><a class="more" href="historique.html">Historique{i("chevr","sm")}</a></div>
{heat_a}
</section>
<div class="split">
<section class="stack">
<div class="card-head"><h2>Mes prochains trajets</h2><a class="more" href="mes-trajets.html">Tout voir{i("chevr","sm")}</a></div>
{trip("Demain · jeu. 25 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "2,50 €", 1, 3, 2, "Léa M.", "4,9", 38, ("Non-fumeur", "Musique"), status='<span class="badge ok">' + i("check","sm") + 'Place confirmée</span>', role="p", pax=["MD", "IN"], href="trajet.html#membre")}
{trip("Ven. 26 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "2,50 €", 2, 3, 2, "Toi", "", None, ("Non-fumeur",), role="d", pax=["CL"])}
{trip("Ven. 26 sept.", "Ponctuel", "17 h 45", "Cité Descartes · Bienvenüe", "18 h 10", "Torcy · Centre", "3,00 €", 2, 3, 0, "Yanis B.", "4,7", 12, ("Bagages",), status='<span class="badge wait">' + i("clock","sm") + 'Demande envoyée</span>', role="p", pax=["HP"], sent=True)}
{trip("Lun. 29 sept.", "L J", "17 h 30", "Cité Descartes · Copernic", "17 h 50", "Noisy-Champs · Gare RER A", "", 0, 0, 0, "Amina S.", "5,0", 22, ("Calme",), role="p", pax=["AS", "MD", "PR", "CL", "HP"], mode="bike", href="trajet.html#velo")}
</section>
<aside class="stack-lg">
<section class="card">
<div class="card-head"><h2>Trajets à noter</h2><span class="badge">2</span></div>
<div class="list">
<a class="li" href="historique.html#noter-conducteur"><span class="avatar sm">LM</span><div class="grow"><b>Noter Léa M.</b><span>Jeu. 18 sept. · tu étais passager</span></div>{i("chevr","sm")}</a>
<a class="li" href="historique.html#noter-passagers"><span class="avatars"><span class="avatar xs">IN</span><span class="avatar xs">TK</span><span class="avatar xs">CL</span></span><div class="grow"><b>Noter tes 3 passagers</b><span>Mer. 17 sept. · tu conduisais</span></div>{i("chevr","sm")}</a>
</div>
</section>
<section class="card">
<div class="card-head"><h2>Mes modes ce mois-ci</h2><a class="more" href="profil.html">Modifier{i("chevr","sm")}</a></div>
<div class="stack">{hbars([("Voiture", 9, "car"), ("Vélo", 4, "bike"), ("À pied", 2, "walk"), ("Transports", 3, "transit")], " trajets", 9)}</div>
<div class="notice">{i("leaf")}<span>Ta promo (BUT Info 2) a évité <b>1,2 t de CO₂</b> depuis la rentrée.</span></div>
</section>
</aside>
</div>
''')

# ================================================================== RECHERCHE
PREFS = ["Non-fumeur", "Musique", "À l'heure"]  # préférences du profil, précochées dans la recherche
PAGES["recherche"] = dict(title="Rechercher un trajet", mtitle="Rechercher", modals="", body=f'''
<section class="card">
<div class="between"><div class="seg" data-single><button type="button" class="on">Ponctuel</button><button type="button">Régulier</button></div>
<span class="small muted campus-line">{i("campus","sm")}Campus <b data-campus-name>{CAMPUS}</b> · <a href="profil.html">changer</a></span></div>
<div class="field"><span class="label">Modes de déplacement</span><div class="row modechips">{"".join(f'<button class="chip mchip m-{m} on" data-toggle type="button" aria-pressed="true">{i(ic,"sm")}{lbl}</button>' for m, (lbl, ic) in MODES.items())}</div></div>
<div class="searchgrid">
<div class="field"><span class="label">Départ</span>{select("s-dep", "Noisy-le-Grand · Mont d'Est")}</div>
<button class="iconbtn swap" type="button" aria-label="Inverser départ et arrivée" data-toast="Départ et arrivée inversés">{i("swap","sm")}</button>
<div class="field"><span class="label">Arrivée</span>{select("s-arr", "Cité Descartes · Copernic")}</div>
<div class="field"><label for="s-date">Date</label>{inp("s-date", "Ven. 26 sept.", "", "calendar")}</div>
<div class="field"><label for="s-time">Arriver avant</label>{inp("s-time", "8 h 30", "", "clock")}</div>
</div>
<div class="between"><p class="small muted">{i("info","sm")} Les zones de départ et d'arrivée sont définies par l'université.</p><button class="btn" type="button" data-loadtoast="6 trajets compatibles trouvés">{i("search","sm")}Rechercher</button></div>
</section>
<div class="split-left">
<aside class="card">
<div class="card-head"><h2>Filtres</h2><button class="linkbtn" type="button" data-toast="Filtres réinitialisés">Réinitialiser</button></div>
<div class="field"><span class="label">Heure d'arrivée</span><div class="row" style="gap:6px"><button class="chip" data-radio type="button">7 h – 8 h</button><button class="chip on" data-radio type="button">8 h – 9 h</button><button class="chip" data-radio type="button">9 h – 10 h</button></div></div>
<div class="field"><span class="label">Places minimum <span class="muted" style="font-weight:400">(voiture)</span></span><div class="stepper" data-max="3"><button class="iconbtn" type="button" aria-label="Moins">−</button><b>1</b><button class="iconbtn" type="button" aria-label="Plus">+</button></div></div>
<div class="divider"></div>
<div class="field">{tp_head("Tags", PREFS, clear=True)}{tagpick("s-tags", PREFS, flat=True)}
<span class="hint">Tes préférences du profil sont précochées.</span></div>
<div class="divider"></div>
<div class="optline"><span>Conducteurs notés 4 ★ et plus</span><button class="toggle on" type="button" aria-pressed="true" aria-label="Conducteurs notés 4 et plus"></button></div>
<div class="optline"><span>Compatible avec mes horaires types</span><button class="toggle on" type="button" aria-pressed="true" aria-label="Horaires types"></button></div>
<div class="optline"><span>Même composante</span><button class="toggle" type="button" aria-pressed="false" aria-label="Même composante"></button></div>
</aside>
<section class="stack">
<div class="between"><p><b>6 trajets</b> <span class="muted">· triés par heure d'arrivée</span></p>
<div class="select" id="s-sort" style="min-width:200px"><button type="button">{i("filter","sm")}<span>Heure d'arrivée</span>{i("chev","sm chev")}</button><div class="options"><button type="button" class="opt sel">Heure d'arrivée</button><button type="button" class="opt">Prix</button><button type="button" class="opt">Note du conducteur</button><button type="button" class="opt">Places libres</button></div></div></div>
{trip("Ven. 26 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "2,50 €", 2, 3, 2, "Léa M.", "4,9", 38, ("Non-fumeur", "Musique"))}
{trip("Ven. 26 sept.", "Ponctuel", "8 h 00", "Noisy-Champs · Gare RER A", "8 h 15", "Cité Descartes · Bienvenüe", "1,50 €", 3, 4, 0, "Hugo P.", "4,6", 9, ("Discussion",))}
{trip("Ven. 26 sept.", "L M V", "7 h 55", "Noisy-le-Grand · Mont d'Est", "8 h 25", "Cité Descartes · Lavoisier", "2,50 €", 1, 3, 1, "Amina S.", "5,0", 22, ("Calme", "Non-fumeur", "Bagages", "À l'heure"))}
{trip("Ven. 26 sept.", "Ponctuel", "8 h 10", "Champs-sur-Marne · Nesles", "8 h 25", "Cité Descartes · Copernic", "1,00 €", 2, 2, 0, "Paul R.", "4,8", 15, ("Bagages",))}
{trip("Ven. 26 sept.", "L M M J V", "7 h 55", "Noisy-Champs · Gare RER A", "8 h 20", "Cité Descartes · Copernic", "", 0, 0, 0, "Chloé L.", "4,9", 17, ("Discussion",), pax=["CL", "IN", "TK"], mode="walk")}
{trip("Ven. 26 sept.", "Ponctuel", "7 h 40", "Torcy · Centre", "8 h 25", "Cité Descartes · Bienvenüe", "", 0, 0, 0, "Thomas K.", "4,5", 8, ("Calme",), pax=["TK", "YB", "HP", "AS", "PR", "LM"], mode="transit")}
</section>
</div>
''')

# ================================================================== DÉTAIL DU TRAJET
dist = [("5 ★", 31), ("4 ★", 6), ("3 ★", 1), ("2 ★", 0), ("1 ★", 0)]
dist_html = "".join(f'<div><span>{k}</span><span class="t"><i style="width:{v / 38 * 100:.0f}%"></i></span><b>{v}</b></div>' for k, v in dist)
PAGES["trajet"] = dict(title="Détail du trajet", mtitle="Trajet de Léa", back="recherche", active="recherche", body=f'''
<div class="crumb" data-view="public" data-mode="car" data-mtitle="Trajet de Léa"><a href="recherche.html">Rechercher</a>{i("chevr","sm")}<span>Trajet de Léa · ven. 26 sept.</span></div>
<div class="crumb" data-view="membre" data-back="mes-trajets" data-mode="car" data-mtitle="Trajet de Léa" hidden><a href="mes-trajets.html">Mes trajets</a>{i("chevr","sm")}<span>Trajet de Léa · ta place confirmée</span></div>
<div class="crumb" data-view="velo" data-back="mes-trajets" data-mode="bike" data-mtitle="Trajet à vélo" hidden><a href="mes-trajets.html">Mes trajets</a>{i("chevr","sm")}<span>Trajet à vélo d'Amina · lun. 29 sept.</span></div>
<div class="split mode-scope m-car" data-mode-default="car">
<div class="stack-lg">
<section class="card" data-view="public">
<div class="between" style="align-items:flex-start"><div class="stack" style="gap:6px;justify-items:start"><div class="row" style="gap:6px">{mode_tag("car")}<span class="badge reg">{i("repeat","sm")}Trajet régulier</span></div><h2>Chaque lundi, mardi, jeudi et vendredi</h2></div><span class="price" style="font-size:26px;line-height:30px">2,50 € <small>/ passager</small></span></div>
<div class="recur">
<div class="stack" style="gap:6px"><span class="small muted">Jours</span>{days([0, 1, 3, 4], pick=False, mini=True)}</div>
<div class="stack" style="gap:2px"><span class="small muted">Période</span><b>Du 26 sept. au 19 déc. 2026</b><span class="small muted">12 semaines, hors vacances universitaires</span></div>
<div class="stack" style="gap:2px"><span class="small muted">Prochain départ</span><b>Ven. 26 sept. · 7 h 50</b></div>
</div>
<ol class="troute" style="gap:22px">
<li><time>7 h 50</time><span class="dot"></span><span class="place"><small>Départ</small><b>Noisy-le-Grand · Mont d'Est</b><span class="small muted">Point de rendez-vous exact partagé dans la messagerie du trajet après acceptation</span></span></li>
<li><time>8 h 20</time><span class="dot"></span><span class="place"><small>Arrivée estimée</small><b>Cité Descartes · Copernic</b><span class="small muted">Parking P2, entrée nord</span></span></li>
</ol>
<div class="map" aria-label="Carte des zones de rendez-vous (fictive)">
<span class="road" style="left:0;right:0;top:120px;height:10px"></span><span class="road" style="left:55%;width:10px;top:0;bottom:0"></span>
<span class="zone" style="left:40px;top:50px;width:150px;height:150px"></span>
<span class="pin" style="left:62px;top:112px"><i></i>Mont d'Est</span>
<span class="pin" style="right:24px;top:24px"><i style="background:var(--secondary)"></i>Copernic</span>
</div>
<div class="stack" style="gap:8px"><div class="between"><span class="label">Passagers</span><span class="badge seats">2 places restantes</span></div>
<div class="row" style="gap:16px"><span class="row" style="gap:8px"><span class="avatar sm">IN</span><span><b>Inès N.</b> {stars("4,8")}</span></span><span class="row" style="gap:8px"><span class="seat-free lg" aria-hidden="true"></span><span class="muted">Place libre</span></span><span class="row" style="gap:8px"><span class="seat-free lg" aria-hidden="true"></span><span class="muted">Place libre</span></span></div></div>
<div class="grid-auto">
<div class="stack" style="gap:2px"><span class="small muted">Demandes en attente</span><b>2</b></div>
<div class="stack" style="gap:2px"><span class="small muted">Véhicule</span><b>Clio grise</b></div>
<div class="stack" style="gap:2px"><span class="small muted">CO₂ évité / passager</span><b>1,4 kg</b></div>
</div>
<div class="row" style="gap:6px">{tags_static(["Non-fumeur", "Musique", "Bagages"])}</div>
</section>
<section class="card" data-view="membre" hidden>
<div class="between" style="align-items:flex-start"><div class="stack" style="gap:6px;justify-items:start"><div class="row" style="gap:6px">{role_tag("p")}{mode_tag("car")}<span class="badge ok">{i("check","sm")}Place confirmée</span><span class="badge reg">{i("repeat","sm")}Trajet régulier</span></div><h2>Chaque lundi, mardi, jeudi et vendredi</h2></div>
<div class="stack price-box" style="gap:2px"><span class="price" style="font-size:26px;line-height:30px">2,50 € <small>/ trajet</small></span><small class="fee">ce que tu paies, dont {euros(COMMISSION)} de commission</small></div></div>
<div class="recur">
<div class="stack" style="gap:6px"><span class="small muted">Tes jours</span>{days([0, 3, 4], pick=False, mini=True)}<span class="small muted">Léa conduit L M J V</span></div>
<div class="stack" style="gap:2px"><span class="small muted">Période</span><b>Du 26 sept. au 19 déc. 2026</b><span class="small muted">12 semaines, hors vacances universitaires</span></div>
<div class="stack" style="gap:2px"><span class="small muted">Ton prochain départ</span><b>Demain · jeu. 25 sept. · 7 h 50</b></div>
</div>
<ol class="troute" style="gap:22px">
<li><time>7 h 50</time><span class="dot"></span><span class="place"><small>Départ</small><b>Noisy-le-Grand · Mont d'Est</b><span class="meet">{i("pin","sm")}Rendez-vous devant la pharmacie du Mont d'Est</span></span></li>
<li><time>8 h 20</time><span class="dot"></span><span class="place"><small>Arrivée estimée</small><b>Cité Descartes · Copernic</b><span class="small muted">Parking P2, entrée nord</span></span></li>
</ol>
<div class="map" role="img" aria-label="Carte des zones de rendez-vous (fictive)">
<span class="road" style="left:0;right:0;top:120px;height:10px"></span><span class="road" style="left:55%;width:10px;top:0;bottom:0"></span>
<span class="zone" style="left:40px;top:50px;width:150px;height:150px"></span>
<span class="pin" style="left:62px;top:112px"><i></i>Pharmacie du Mont d'Est</span>
<span class="pin" style="right:24px;top:24px"><i style="background:var(--secondary)"></i>Copernic</span>
</div>
<div class="stack" style="gap:8px"><div class="between"><span class="label">Passagers</span><span class="badge seats">1 place restante</span></div>
<div class="row" style="gap:16px"><span class="row" style="gap:8px"><span class="avatar sm">MD</span><span><b>Toi</b> <span class="small muted">· L J V</span></span></span><span class="row" style="gap:8px"><span class="avatar sm">IN</span><span><b>Inès N.</b> {stars("4,8")} <span class="small muted">· J V</span></span></span><span class="row" style="gap:8px"><span class="seat-free lg" aria-hidden="true"></span><span class="muted">Place libre</span></span></div></div>
<div class="grid-auto">
<div class="stack" style="gap:2px"><span class="small muted">Ta réservation</span><b>1 place</b></div>
<div class="stack" style="gap:2px"><span class="small muted">Véhicule</span><b>Clio grise</b></div>
<div class="stack" style="gap:2px"><span class="small muted">CO₂ évité / trajet</span><b>1,4 kg</b></div>
</div>
<div class="row" style="gap:6px">{tags_static(["Non-fumeur", "Musique", "Bagages"])}</div>
</section>
<section class="card" data-view="velo" hidden>
<div class="between" style="align-items:flex-start"><div class="stack" style="gap:6px;justify-items:start"><div class="row" style="gap:6px">{mode_tag("bike")}<span class="badge reg">{i("repeat","sm")}Régulier · L J</span></div><h2>Chaque lundi et jeudi</h2></div><span class="free-tag" style="font-size:22px;line-height:28px">Gratuit</span></div>
<div class="recur">
<div class="stack" style="gap:6px"><span class="small muted">Jours</span>{days([0, 3], pick=False, mini=True)}</div>
<div class="stack" style="gap:2px"><span class="small muted">Période</span><b>Du 29 sept. au 18 déc. 2026</b><span class="small muted">hors vacances universitaires</span></div>
<div class="stack" style="gap:2px"><span class="small muted">Prochain départ</span><b>Lun. 29 sept. · 17 h 30</b></div>
</div>
<ol class="troute" style="gap:22px">
<li><time>17 h 30</time><span class="dot"></span><span class="place"><small>Départ</small><b>Cité Descartes · Copernic</b><span class="meet">{i("pin","sm")}Rendez-vous au parking vélos, entrée nord</span></span></li>
<li><time>17 h 50</time><span class="dot"></span><span class="place"><small>Arrivée estimée</small><b>Noisy-Champs · Gare RER A</b><span class="small muted">Arceaux vélos côté gare routière</span></span></li>
</ol>
<div class="stack" style="gap:8px"><div class="between"><span class="label">Participants</span><span class="badge joined">{i("users","sm")}5 personnes ont rejoint</span></div>
<div class="row" style="gap:16px"><span class="row" style="gap:8px"><span class="avatar sm">AS</span><span><b>Amina S.</b> <span class="small muted">· organise</span></span></span><span class="row" style="gap:8px"><span class="avatar sm">MD</span><b>Toi</b></span><span class="row" style="gap:8px"><span class="avatar sm">PR</span><b>Paul R.</b></span><span class="row" style="gap:8px"><span class="avatar sm">CL</span><b>Chloé L.</b></span><span class="row" style="gap:8px"><span class="avatar sm">HP</span><b>Hugo P.</b></span></div></div>
<div class="grid-auto">
<div class="stack" style="gap:2px"><span class="small muted">Distance</span><b>4 km</b></div>
<div class="stack" style="gap:2px"><span class="small muted">Durée</span><b>20 min</b></div>
<div class="stack" style="gap:2px"><span class="small muted">CO₂ évité / trajet</span><b>0,9 kg</b></div>
</div>
<div class="notice">{i("users")}<span>Sans voiture : pas de prix ni de limite de places. Chacun peut rejoindre ou quitter le trajet librement.</span></div>
<div class="row" style="gap:6px">{tags_static(["Calme"])}</div>
</section>
<section class="card" data-view="public membre">
<div class="card-head"><h2>Notes reçues par Léa</h2>{stars("4,9", "38 notes")}</div>
<div class="dist">{dist_html}</div>
</section>
</div>
<aside class="stack-lg">
<div class="stack-lg" data-view="public">
<section class="card">
<div class="row"><span class="avatar lg b">LM</span><div><h2>Léa M.</h2><p class="muted">Master Génie civil · conductrice</p><p>{stars("4,9", 38)}</p></div></div>
<div class="row" style="gap:6px"><span class="badge ok">{i("shield","sm")}Compte universitaire vérifié</span><span class="badge line">42 trajets conduits</span></div>
<div class="recap">
<div class="between small"><span class="muted">Participation reversée à Léa</span><b class="num">{driver_share("2,50 €")}</b></div>
<div class="between small"><span class="muted">Commission U-Mobility</span><b class="num">{euros(COMMISSION)}</b></div>
<div class="divider"></div>
<div class="between"><b>Prix par trajet</b><b class="num">2,50 €</b></div>
</div>
<button class="btn secondary block" type="button" data-open="demande">{i("join","sm")}Demander à rejoindre ce trajet</button>
<p class="small muted">Léa a 24 h pour accepter ou refuser. Tu rejoindras ensuite la messagerie du trajet.</p>
</section>
<button class="btn danger block" type="button" data-open="signaler">{i("flag","sm")}Signaler ce trajet</button>
</div>
<div class="stack-lg" data-view="velo" hidden>
<section class="card">
<div class="row"><span class="avatar lg">AS</span><div><h2>Amina S.</h2><p class="muted">Licence Informatique · organisatrice</p><p>{stars("5,0", 22)}</p></div></div>
<div class="row" style="gap:6px"><span class="badge ok">{i("shield","sm")}Compte universitaire vérifié</span></div>
<a class="btn block" href="messages.html">{i("msg","sm")}Messagerie du trajet</a>
<button class="btn danger block" type="button" data-toast="Tu as quitté le trajet à vélo">{i("leave","sm")}Quitter ce trajet</button>
</section>
<button class="btn danger block" type="button" data-open="signaler">{i("flag","sm")}Signaler ce trajet</button>
</div>
<div class="stack-lg" data-view="membre" hidden>
<section class="card">
<div class="row"><span class="avatar lg b">LM</span><div><h2>Léa M.</h2><p class="muted">Master Génie civil · ta conductrice</p><p>{stars("4,9", 38)}</p></div></div>
<div class="row" style="gap:6px"><span class="badge ok">{i("shield","sm")}Compte universitaire vérifié</span><span class="badge line">42 trajets conduits</span></div>
<a class="btn block" href="messages.html">{i("msg","sm")}Messagerie du trajet</a>
<button class="btn danger block" type="button" data-open="annuler">{i("x","sm")}Annuler ma place</button>
<p class="small muted">Tu peux annuler une date ou tous tes jours. Léa et les autres passagers sont prévenus automatiquement.</p>
</section>
<button class="btn danger block" type="button" data-open="signaler">{i("flag","sm")}Signaler ce trajet</button>
</div>
</aside>
</div>
''', modals=modal("demande", f'''
<div data-step>
{dhead("Demander à rejoindre", "Trajet de Léa · départ 7 h 50 · Noisy-le-Grand → Copernic", "join")}
<div class="field"><span class="label">Jours souhaités</span>{days([3, 4], allowed=[0, 1, 3, 4])}<span class="hint">Trajet régulier : choisis parmi les jours proposés par Léa (lundi, mardi, jeudi, vendredi).</span></div>
<div class="field"><span class="label">Places</span><div class="stepper" data-max="2"><button class="iconbtn" type="button" aria-label="Moins">−</button><b>1</b><button class="iconbtn" type="button" aria-label="Plus">+</button></div></div>
<div class="field"><label for="d-msg">Message à Léa <span class="muted" style="font-weight:400">(facultatif)</span></label>{textarea("d-msg", "Ex. : je peux être au point de rendez-vous 5 min avant.")}</div>
<div class="recap"><div class="between small"><span class="muted">Période</span><b>du 26 sept. au 19 déc.</b></div>
<div class="between small"><span class="muted">Participation reversée à Léa</span><b class="num">{driver_share("2,50 €")}</b></div>
<div class="between small"><span class="muted">Commission U-Mobility</span><b class="num">{euros(COMMISSION)}</b></div>
<div class="between small"><b>Prix par trajet</b><b class="num">2,50 €</b></div></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn secondary" type="button" data-next data-loading>{i("send","sm")}Envoyer la demande</button></div>
</div>
<div data-step hidden>{success("Demande envoyée", "Léa a 24 h pour répondre. Tu seras notifié dès qu'elle accepte ou refuse.", '<a class="btn ghost" href="mes-trajets.html#envoyees">Voir mes demandes</a>')}</div>
''') + modal("signaler", f'''
<div data-step>
{dhead("Signaler", "Ton signalement est transmis uniquement à l'équipe de modération.", "flag", True)}
<div class="seg" data-single><button type="button" class="on" data-show="trajet">Ce trajet</button><button type="button" data-show="compte">Le compte de Léa</button></div>
<div class="field"><span class="label">Motif</span><div class="row" style="gap:6px">{"".join(f'<button class="chip{" on" if k == 0 else ""}" data-radio type="button">{m}</button>' for k, m in enumerate(["Trajet non conforme", "Tarif abusif", "Annonce commerciale", "Informations fausses", "Autre"]))}</div></div>
<div class="field"><label for="r-msg">Détails <span class="muted" style="font-weight:400">(facultatif)</span></label>{textarea("r-msg", "Décris ce qui pose problème.", 500)}</div>
<div class="notice warn">{i("info")}<span>En cas d'urgence, appelle le 112. Ce formulaire ne remplace pas les secours.</span></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn danger-solid" type="button" data-next data-loading>{i("flag","sm")}Envoyer le signalement</button></div>
</div>
<div data-step hidden>{success("Signalement envoyé", "L'équipe de modération le traite sous 48 h. La personne signalée ne sait pas qui l'a signalée.")}</div>
'''))

# ================================================================== PUBLIER
MODE_HINT = {"car": "Prix par passager, places limitées", "bike": "Gratuit, sans limite", "walk": "Gratuit, sans limite", "transit": "Gratuit, sans limite"}
NOCAR = "mode:bike mode:walk mode:transit"
modepick = "".join(f'<button type="button" class="m-{m}{" on" if m == "car" else ""}" data-show="mode:{m}" role="radio" aria-checked="{"true" if m == "car" else "false"}"><span class="mi">{i(ic)}</span><b>{lbl}</b><small>{MODE_HINT[m]}</small></button>' for m, (lbl, ic) in MODES.items())
previews = "".join(
    f'<div data-when="mode:{m}"{"" if m == "car" else " hidden"}>' + (
        trip("Ven. 26 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "2,50 €", 3, 3, 0, "Toi", "", None, ("Non-fumeur", "Musique"), go=False)
        if m == "car" else
        trip("Ven. 26 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "", 0, 0, 0, "Toi", "", None, ("Calme", "À l'heure"), go=False, pax=["MD"], mode=m)
    ) + '</div>' for m in MODES)
PAGES["publier"] = dict(title="Publier un trajet", mtitle="Publier", sub="En voiture, à vélo, à pied ou en transports en commun.", body=f'''
<div class="split mode-scope m-car" data-show-scope>
<section class="card">
<div class="field"><span class="label">Mode de déplacement</span><div class="modepick" data-single role="radiogroup" aria-label="Mode de déplacement">{modepick}</div></div>
<div class="field"><span class="label">Type de trajet</span><div class="seg" data-single><button type="button" data-show="ponctuel">Ponctuel</button><button type="button" class="on" data-show="regulier">Régulier</button></div></div>
<div class="grid-2">
<div class="field"><span class="label">Départ</span>{select("p-dep", "Noisy-le-Grand · Mont d'Est")}</div>
<div class="field"><span class="label">Arrivée</span>{select("p-arr", "Cité Descartes · Copernic")}</div>
</div>
<p class="small muted" style="margin-top:-8px">Zones de rendez-vous définies par l'université : ton adresse n'est jamais demandée.</p>
<div class="field" data-when="regulier"><span class="label">Jours</span>{days([0, 1, 3, 4])}</div>
<div class="field" data-when="ponctuel" hidden><label for="p-date">Date</label>{inp("p-date", "Mer. 1er oct.", "", "calendar")}</div>
<div class="grid-3">
<div class="field"><label for="p-dep-t">Heure de départ</label>{inp("p-dep-t", "7 h 50", "", "clock")}</div>
<div class="field"><label for="p-arr-t">Arrivée estimée</label>{inp("p-arr-t", "8 h 20", "", "clock")}</div>
<div class="field" data-when="regulier"><label for="p-period">Période</label>{inp("p-period", "26 sept. → 19 déc.", "", "calendar")}</div>
</div>
<div class="grid-3" data-when="mode:car">
<div class="field"><span class="label">Places proposées</span><div class="stepper" data-max="3"><button class="iconbtn" type="button" aria-label="Moins">−</button><b>3</b><button class="iconbtn" type="button" aria-label="Plus">+</button></div></div>
<div class="field"><label for="p-price">Participation par passager</label>{inp("p-price", "2,50 €")}<span class="hint">Suggestion : 2,40 € pour 12 km. Tu reçois <b>{driver_share("2,50 €")}</b> par passager, U-Mobility garde une commission de {euros(COMMISSION)}.</span></div>
<div class="field"><span class="label">Véhicule</span>{select("p-car", "Renault Clio · grise · 3 places", "car", [("Mes véhicules", ["Renault Clio · grise · 3 places"])])}<button class="linkbtn" type="button" data-open="voiture" style="font-size:13px">{i("plus","sm")}Ajouter une voiture</button></div>
</div>
<div class="notice" data-when="{NOCAR}" hidden>{i("users")}<span>Sans voiture, pas de prix ni de limite de places : tout le monde peut rejoindre. Le trajet affiche le nombre de personnes qui ont rejoint.</span></div>
<div class="field">{tp_head('Tags <span class="muted" style="font-weight:400">(facultatif)</span>', ["Non-fumeur", "Musique"], TAG_MAX)}{tagpick("p-tags", ["Non-fumeur", "Musique"], mode="car", max_=TAG_MAX)}
<span class="hint">Jusqu'à {TAG_MAX} tags, selon le mode choisi. Ils aident les autres à trouver ton trajet : ils sont comparés à leurs recherches et à leurs préférences.</span></div>
<div class="optline" data-when="mode:car"><span>Accepter automatiquement les passagers déjà notés 4 ★ et plus</span><button class="toggle" type="button" aria-pressed="false" aria-label="Acceptation automatique"></button></div>
<div class="dialog-foot"><a class="btn ghost" href="index.html">Annuler</a><button class="btn secondary" type="button" data-loadtoast="Trajet publié · visible dans Mes trajets">{i("check","sm")}Publier le trajet</button></div>
</section>
<aside class="stack">
<h2>Aperçu</h2>
{previews}
</aside>
</div>
''', modals="")  # modal voiture ajouté plus bas (partagé avec profil)

# ================================================================== MES TRAJETS
def req(init, name, rating, dd, places, note):
    msg = f'<span class="small">« {note} »</span>' if note else '<span class="small muted">Aucun message</span>'
    return (f'<div class="req"><span class="avatar">{init}</span><div class="grow"><b>{name} · {stars(rating)}</b>'
            f'<div class="row" style="gap:8px"><span class="small muted">Jours demandés</span>{days(dd, pick=False, mini=True)}<span class="small muted">· {places}</span></div>{msg}</div>'
            f'<div class="acts"><button class="btn sm danger" type="button" data-toast="Demande de {name} refusée" data-remove=".req">{i("x","sm")}Refuser</button>'
            f'<button class="btn sm success" type="button" data-toast="{name} a rejoint le trajet" data-remove=".req">{i("check","sm")}Accepter</button></div></div>')


def group_head(title, meta, extra="", href="trajet.html", role="d"):
    return f'<header><span class="role-ico {role}" title="{"Conducteur" if role == "d" else "Passager"}">{i("wheel" if role == "d" else "seat")}</span><div class="grow"><b>{title}</b><span>{meta}</span></div>{extra}<a class="btn sm ghost" href="{href}">Voir le trajet</a></header>'


# Popups partagées entre plusieurs pages (une constante par popup)
M_ANNULER = modal("annuler", f'''
<div data-step>
{dhead("Annuler ta place ?", "Trajet de Léa · jeu. 25 sept. · départ 7 h 50", "x", True)}
<div class="field"><span class="label">Que veux-tu annuler ?</span><div class="seg" data-single><button type="button" class="on">Ce trajet seulement</button><button type="button">Tous les jeudis</button></div></div>
<div class="notice">{i("msg")}<span>Léa et les autres passagers sont prévenus par un message automatique dans la messagerie du trajet.</span></div>
<div class="notice warn">{i("clock")}<span>Le trajet part dans moins de 24 h : pense à prévenir le plus tôt possible.</span></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Garder ma place</button><button class="btn danger-solid" type="button" data-next data-loading>Annuler ma place</button></div>
</div>
<div data-step hidden>{success("Place annulée", "La place est de nouveau disponible pour les autres passagers.")}</div>
''')
M_ANNULER_TRAJET = modal("annuler-trajet", f'''
<div data-step>
{dhead("Annuler le trajet ?", "Noisy-le-Grand → Copernic · régulier L M J V · 7 h 50", "x", True)}
<div class="field"><span class="label">Que veux-tu annuler ?</span><div class="seg" data-single><button type="button" class="on">Le ven. 26 sept. seulement</button><button type="button">Tout le trajet régulier</button></div></div>
<div class="field"><span class="label">Motif <span class="muted" style="font-weight:400">(visible par les passagers)</span></span><div class="row" style="gap:6px">{"".join(f'<button class="chip{" on" if k == 0 else ""}" data-radio type="button">{m}</button>' for k, m in enumerate(["Empêchement", "Voiture indisponible", "Changement d'emploi du temps", "Autre"]))}</div></div>
<div class="notice">{i("users")}<span>1 passager confirmé et 2 demandes en attente seront prévenus. Les demandes en attente sont refusées automatiquement.</span></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Garder le trajet</button><button class="btn danger-solid" type="button" data-next data-loading>Annuler le trajet</button></div>
</div>
<div data-step hidden>{success("Trajet annulé", "Les passagers ont été prévenus dans la messagerie du trajet.")}</div>
''')
M_NOTER_C = modal("noter-conducteur", f'''
<div data-step>
{dhead("Noter Léa", "Trajet du jeu. 18 sept. · Noisy-le-Grand → Copernic", "star")}
<div class="card tight" style="box-shadow:none;background:var(--surface)"><div class="row"><span class="avatar">LM</span><div class="grow"><b>Léa M.</b><span class="small muted" style="display:block">Conductrice</span></div></div>{rate("rate-lea", 0)}</div>
<p class="small muted">La note est anonyme pour Léa et n'a pas de commentaire écrit. Un problème ? <button class="linkbtn red" type="button" data-open="signaler-compte" style="font-size:13px">Signaler plutôt ce compte</button></p>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Plus tard</button><button class="btn" type="button" data-next data-loading>Envoyer ma note</button></div>
</div>
<div data-step hidden>{success("Merci !", "Ta note aide les autres étudiants à choisir leurs trajets.")}</div>
''')
M_NOTER_P = modal("noter-passagers", f'''
<div data-step>
{dhead("Noter tes passagers", "Trajet du mer. 17 sept. · Copernic → Torcy", "star")}
<div class="list">
<div class="li"><span class="avatar">IN</span><div class="grow"><b>Inès N.</b><span>Passagère</span></div>{rate("rate-ines", 5)}</div>
<div class="li"><span class="avatar">TK</span><div class="grow"><b>Thomas K.</b><span>Passager</span></div>{rate("rate-thomas", 0)}</div>
<div class="li"><span class="avatar">CL</span><div class="grow"><b>Chloé L.</b><span>Passagère</span></div>{rate("rate-chloe", 0)}</div>
</div>
<p class="small muted">Notes de 1 à 5 étoiles, sans commentaire. Les passagers voient leur moyenne, jamais qui a donné quelle note.</p>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Plus tard</button><button class="btn" type="button" data-next data-loading>Envoyer les notes</button></div>
</div>
<div data-step hidden>{success("Notes envoyées", "Merci d'aider la communauté U-Mobility.")}</div>
''', wide=True)
MEMBERS = [("LM", "Léa M.", "Conductrice"), ("IN", "Inès N.", "Passagère"), ("TK", "Thomas K.", "Passager")]
M_SIGNALER_COMPTE = modal("signaler-compte", f'''
<div data-step>
{dhead("Signaler un compte", "Ton signalement est transmis uniquement à l'équipe de modération.", "flag", True)}
<div class="field"><span class="label">Qui veux-tu signaler ?</span><div class="list">{"".join(f'<div class="li click{" sel" if k == 0 else ""}" data-conv><span class="avatar sm">{a}</span><div class="grow"><b>{n}</b><span>{r}</span></div></div>' for k, (a, n, r) in enumerate(MEMBERS))}</div></div>
<div class="field"><span class="label">Motif</span><div class="row" style="gap:6px">{"".join(f'<button class="chip{" on" if k == 1 else ""}" data-radio type="button">{m}</button>' for k, m in enumerate(["Comportement inapproprié", "Absence au rendez-vous", "Conduite dangereuse", "Harcèlement", "Faux profil", "Autre"]))}</div></div>
<div class="field"><label for="rc-msg">Détails <span class="muted" style="font-weight:400">(facultatif)</span></label>{textarea("rc-msg", "Décris ce qui s'est passé.", 500)}</div>
<div class="notice warn">{i("info")}<span>En cas d'urgence, appelle le 112. Ce formulaire ne remplace pas les secours.</span></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn danger-solid" type="button" data-next data-loading>{i("flag","sm")}Envoyer le signalement</button></div>
</div>
<div data-step hidden>{success("Signalement envoyé", "L'équipe de modération le traite sous 48 h. La personne signalée ne sait pas qui l'a signalée.")}</div>
''')

PAGES["trajet"]["modals"] += M_ANNULER  # vue passager confirmé (trajet.html#membre)

# Mes trajets : la liste des trajets à venir, sans les demandes (gérées dans le détail conducteur) ni les notes (Historique).
PAGES["mes-trajets"] = dict(title="Mes trajets", mtitle="Mes trajets", body=f'''
<div class="between"><div class="row" style="gap:6px" data-filter-list="mt-list"><button class="chip on" data-radio data-filter="" type="button">Tous <span class="muted">5</span></button><button class="chip mchip r-d" data-radio data-filter="role-d" type="button">{i("wheel","sm")}Conducteur</button><button class="chip mchip r-p" data-radio data-filter="role-p" type="button">{i("seat","sm")}Passager</button>{"".join(f'<button class="chip mchip m-{m}" data-radio data-filter="m-{m}" type="button">{i(ic,"sm")}{lbl}</button>' for m, (lbl, ic) in MODES.items() if m != "car")}</div>
<a class="more small" href="historique.html">Trajets passés et notes{i("chevr","sm")}</a></div>
<div class="stack" id="mt-list">
{trip("Demain · jeu. 25 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "2,50 €", 1, 3, 2, "Léa M.", "4,9", 38, ("Non-fumeur",), status='<span class="badge ok">' + i("check","sm") + 'Place confirmée</span>', role="p", pax=["MD", "IN"], href="trajet.html#membre", cancel=f'<button class="btn sm danger" type="button" data-open="annuler">{i("x","sm")}Annuler ma place</button>')}
{trip("Ven. 26 sept.", "L M J V", "7 h 50", "Noisy-le-Grand · Mont d'Est", "8 h 20", "Cité Descartes · Copernic", "2,50 €", 2, 3, 2, "Toi", "", None, ("Non-fumeur", "Musique"), role="d", pax=["CL"], cancel=f'<button class="btn sm danger" type="button" data-open="annuler-trajet">{i("x","sm")}Annuler le trajet</button>', actions=f'<a class="btn sm ghost" href="publier.html">{i("edit","sm")}Modifier</a>')}
{trip("Ven. 26 sept.", "Ponctuel", "17 h 45", "Cité Descartes · Bienvenüe", "18 h 10", "Torcy · Centre", "3,00 €", 2, 3, 0, "Yanis B.", "4,7", 12, ("Bagages",), status='<span class="badge wait">' + i("clock","sm") + 'Demande envoyée</span>', role="p", pax=["HP"], sent=True, cancel=f'<button class="btn sm danger" type="button" data-toast="Demande retirée" data-remove=".trip">{i("x","sm")}Retirer ma demande</button>')}
{trip("Lun. 29 sept.", "L J", "17 h 30", "Cité Descartes · Copernic", "17 h 50", "Noisy-Champs · Gare RER A", "", 0, 0, 0, "Amina S.", "5,0", 22, ("Calme",), role="p", pax=["AS", "MD", "PR", "CL", "HP"], mode="bike", href="trajet.html#velo", cancel=f'<button class="btn sm danger" type="button" data-toast="Tu as quitté le trajet à vélo" data-remove=".trip">{i("leave","sm")}Quitter</button>')}
{trip("Mer. 1er oct.", "Ponctuel", "18 h 00", "Cité Descartes · Copernic", "18 h 30", "Chelles · Gare", "2,00 €", 3, 3, 0, "Toi", "", None, (), role="d", cancel=f'<button class="btn sm danger" type="button" data-open="annuler-trajet">{i("x","sm")}Annuler le trajet</button>', actions=f'<a class="btn sm ghost" href="publier.html">{i("edit","sm")}Modifier</a>')}
</div>
<div class="notice">{i("info")}<span>Les demandes reçues se traitent dans le détail de chaque trajet que tu conduis. Les notes se donnent depuis l'<a href="historique.html">Historique</a>.</span></div>
''', modals=M_ANNULER + M_ANNULER_TRAJET)

# ================================================================== MON TRAJET (vue conducteur)
PAGES["mon-trajet"] = dict(title="Mon trajet", mtitle="Mon trajet", back="mes-trajets", active="mes-trajets", body=f'''
<div class="crumb"><a href="mes-trajets.html">Mes trajets</a>{i("chevr","sm")}<span>Noisy-le-Grand → Copernic · ven. 26 sept.</span></div>
<div class="split mode-scope m-car">
<div class="stack-lg">
<section class="card">
<div class="between" style="align-items:flex-start"><div class="stack" style="gap:6px;justify-items:start"><div class="row" style="gap:6px">{role_tag("d")}{mode_tag("car")}<span class="badge reg">{i("repeat","sm")}Trajet régulier</span></div><h2>Chaque lundi, mardi, jeudi et vendredi</h2></div>
<div class="stack price-box" style="gap:2px"><span class="price" style="font-size:26px;line-height:30px">2,50 € <small>/ passager</small></span><small class="fee">tu reçois {driver_share("2,50 €")} par passager</small></div></div>
<div class="recur">
<div class="stack" style="gap:6px"><span class="small muted">Jours</span>{days([0, 1, 3, 4], pick=False, mini=True)}</div>
<div class="stack" style="gap:2px"><span class="small muted">Période</span><b>Du 26 sept. au 19 déc. 2026</b><span class="small muted">12 semaines, hors vacances universitaires</span></div>
<div class="stack" style="gap:2px"><span class="small muted">Prochain départ</span><b>Ven. 26 sept. · 7 h 50</b></div>
</div>
<ol class="troute" style="gap:22px">
<li><time>7 h 50</time><span class="dot"></span><span class="place"><small>Départ</small><b>Noisy-le-Grand · Mont d'Est</b><span class="small muted">Précise le point exact aux passagers dans la messagerie</span></span></li>
<li><time>8 h 20</time><span class="dot"></span><span class="place"><small>Arrivée estimée</small><b>Cité Descartes · Copernic</b><span class="small muted">Parking P2, entrée nord</span></span></li>
</ol>
<div class="grid-auto">
<div class="stack" style="gap:2px"><span class="small muted">Places</span><b>1 prise sur 3</b></div>
<div class="stack" style="gap:2px"><span class="small muted">Véhicule</span><b>Clio grise</b></div>
<div class="stack" style="gap:2px"><span class="small muted">CO₂ évité / trajet</span><b>1,4 kg</b></div>
</div>
<div class="row" style="gap:6px">{tags_static(["Non-fumeur", "Musique"])}</div>
</section>
<section class="card" id="demandes">
<div class="card-head"><div><h2>Demandes en attente</h2><p class="small muted">Accepte ou refuse chaque passager. Sans réponse sous 24 h, la demande est refusée automatiquement.</p></div><span class="badge wait">{i("hourglass","sm")}2 en attente</span></div>
<div class="req-list">
{req("IN", "Inès N.", "4,8", [3, 4], "1 place", "Je peux être au Mont d'Est 5 min avant.")}
{req("TK", "Thomas K.", "4,5", [4], "1 place", "")}
</div>
</section>
</div>
<aside class="stack-lg">
<section class="card">
<div class="card-head"><h2>Passagers</h2><span class="badge seats">2 places restantes</span></div>
<div class="list">
<div class="li"><span class="avatar sm">CL</span><div class="grow"><b>Chloé L. · {stars("4,7")}</b><span>Passagère · V</span></div><button class="iconbtn flag" type="button" data-open="signaler-compte" aria-label="Signaler Chloé" title="Signaler Chloé">{i("flag","sm")}</button></div>
<div class="li"><span class="seat-free lg" aria-hidden="true"></span><div class="grow"><b class="muted">Place libre</b></div></div>
<div class="li"><span class="seat-free lg" aria-hidden="true"></span><div class="grow"><b class="muted">Place libre</b></div></div>
</div>
</section>
<section class="card">
<a class="btn block" href="messages.html">{i("msg","sm")}Messagerie du trajet</a>
<a class="btn ghost block" href="publier.html">{i("edit","sm")}Modifier le trajet</a>
<button class="btn danger block" type="button" data-open="annuler-trajet">{i("x","sm")}Annuler le trajet</button>
</section>
</aside>
</div>
''', modals=M_ANNULER_TRAJET + M_SIGNALER_COMPTE)

# ================================================================== HISTORIQUE
months = [("Avr", 142), ("Mai", 188), ("Juin", 96), ("Juil", 24), ("Août", 0), ("Sept", 168)]
hist = [
    ("Septembre 2026", [
        ("Jeu. 18 sept.", "7 h 50 → 8 h 20", "Noisy-le-Grand · Mont d'Est → Copernic", "p", ["LM"], "12 km", "1,4 kg", 5, None),
        ("Mer. 17 sept.", "18 h 00 → 18 h 25", "Copernic → Torcy · Centre", "d", ["IN", "TK", "CL"], "9 km", "3,1 kg", 5, None),
        ("Mar. 16 sept.", "7 h 50 → 8 h 20", "Noisy-le-Grand · Mont d'Est → Copernic", "d", ["IN", "YB"], "12 km", "2,8 kg", 4, 5),
        ("Lun. 15 sept.", "8 h 00 → 8 h 15", "Noisy-Champs · Gare RER A → Bienvenüe", "p", ["HP"], "4 km", "0,5 kg", 5, 4),
        ("Ven. 12 sept.", "7 h 50 → 8 h 20", "Noisy-le-Grand · Mont d'Est → Copernic", "p", ["LM"], "12 km", "1,4 kg", 5, 5),
    ]),
    ("Juin 2026", [
        ("Ven. 20 juin", "12 h 30 → 13 h 00", "Lavoisier → Chelles · Gare", "p", ["AS"], "10 km", "1,2 kg", 5, 5),
        ("Jeu. 19 juin", "7 h 50 → 8 h 20", "Noisy-le-Grand · Mont d'Est → Copernic", "d", ["IN", "CL"], "12 km", "2,8 kg", 5, 5),
    ]),
]
rows = ""
for month, items in hist:
    rows += f'<tr class="month"><td colspan="6"><b>{month}</b></td></tr>'
    for d, t, r, role, who, km, co, received, given in items:
        av = '<span class="avatars">' + "".join(f'<span class="avatar xs">{x}</span>' for x in who) + '</span>'
        gv = stars5(given) if given else f'<button class="btn sm" type="button" data-open="{"noter-passagers" if role == "d" else "noter-conducteur"}">{i("star","sm")}Noter</button>'
        rows += f'<tr><td class="muted" style="white-space:nowrap">{d}</td><td><b>{r}</b><br><span class="small muted num">{t}</span></td><td>{role_tag(role)}</td><td>{av}</td><td class="num" style="white-space:nowrap">{km} · {co}</td><td>{gv}</td></tr>'
PAGES["historique"] = dict(title="Historique", mtitle="Historique", back="index", body=f'''
<section class="card">
<div class="card-head"><div><h2>À noter</h2><p class="small muted">Note tes trajets terminés : 1 à 5 étoiles, sans commentaire.</p></div><span class="badge">2</span></div>
<div class="list">
<div class="li"><span class="role-ico p" title="Passager">{i("seat")}</span><div class="grow"><b>Comment s'est passé ton trajet avec Léa ?</b><span>Jeu. 18 sept. · Noisy-le-Grand → Copernic · tu étais passager</span></div><button class="btn sm" type="button" data-open="noter-conducteur">{i("star","sm")}Noter Léa</button></div>
<div class="li"><span class="role-ico d" title="Conducteur">{i("wheel")}</span><div class="grow"><b>Note tes 3 passagers</b><span>Mer. 17 sept. · Copernic → Torcy · Inès N., Thomas K., Chloé L.</span></div><button class="btn sm" type="button" data-open="noter-passagers">{i("star","sm")}Noter les passagers</button></div>
</div>
</section>
<div class="between"><div class="row" style="gap:6px"><button class="chip on" data-radio type="button">Tous</button><button class="chip" data-radio type="button">Conducteur</button><button class="chip" data-radio type="button">Passager</button></div>
<div class="row"><div class="select" id="h-period" style="min-width:210px"><button type="button">{i("calendar","sm")}<span>Année 2025–2026</span>{i("chev","sm chev")}</button><div class="options"><button type="button" class="opt sel">Année 2025–2026</button><button type="button" class="opt">Septembre 2026</button><button type="button" class="opt">Juin 2026</button><button type="button" class="opt">Mai 2026</button></div></div>
<button class="btn ghost sm" type="button" data-loadtoast="Bilan mensuel exporté (PDF)">{i("download","sm")}Exporter le bilan</button></div></div>
<div class="grid-4">
<div class="stat dark"><span class="k">{i("route","sm")}Trajets effectués</span><span class="v">42</span><span class="d m">28 passager · 14 conducteur</span></div>
<div class="stat"><span class="k">{i("route","sm")}Distance</span><span class="v">618 <small>km</small></span><span class="d m">14,7 km par trajet</span></div>
<div class="stat"><span class="k">{i("leaf","sm")}CO₂ évité</span><span class="v">116 <small>kg</small></span><span class="d">= 5 arbres pendant 1 an</span></div>
<div class="stat"><span class="k">{i("ticket","sm")}Frais partagés</span><span class="v">96 <small>€</small></span><span class="d m">économisés sur l'essence</span></div>
</div>
<div class="grid-2">
<section class="card">
<div class="card-head"><h2>Distance par mois</h2><span class="small muted">en km</span></div>
{bars(months, "Sept", " km")}
</section>
<section class="card">
<h2>Mes trajets fréquents</h2>
<div class="stack">{hbars([("Noisy-le-Grand → Copernic", 24), ("Copernic → Torcy", 9), ("Noisy-Champs → Bienvenüe", 5), ("Lavoisier → Chelles", 4)], " trajets", 24)}</div>
<div class="divider"></div>
<div class="stack" style="gap:4px"><span class="small muted">Ma note, donnée par mes conducteurs et mes passagers</span>{stars("4,8", "48 notes")}</div>
</section>
</div>
<section class="card">
<div class="card-head"><h2>Tous mes trajets</h2><span class="small muted">42 trajets</span></div>
<div class="table-wrap" tabindex="0" role="region" aria-label="Tous mes trajets"><table class="table">
<thead><tr><th>Date</th><th>Trajet</th><th>Rôle</th><th>Avec</th><th>Distance · CO₂</th><th>Ma note</th></tr></thead>
<tbody>{rows}</tbody></table></div>
</section>
''', modals=M_NOTER_C + M_NOTER_P + M_SIGNALER_COMPTE)

# ================================================================== MESSAGES
# Une conversation n'existe qu'une fois la demande acceptée : pas de conversation pour une demande en attente.
PAGES["messages"] = dict(title="Messages", mtitle="Messages", back="index", sub="Une conversation par trajet, avec tous ses membres.", body=f'''
<div class="chat-layout">
<aside class="card tight conv-list">
<div class="list">
<div class="li click sel" data-conv><span class="avatars"><span class="avatar xs">LM</span><span class="avatar xs">IN</span></span><div class="grow"><b>Noisy → Copernic</b><span>Régulier · 4 membres · « J'y serai à 7 h 45 »</span></div><span class="badge lav">1</span></div>
<div class="li click" data-conv><span class="avatars"><span class="avatar xs">AS</span><span class="avatar xs">PR</span></span><div class="grow"><b>Copernic → Noisy-Champs à vélo</b><span>Lun. 29 sept. · 5 membres</span></div></div>
<div class="li click" data-conv><span class="avatars"><span class="avatar xs">MD</span><span class="avatar xs">IN</span></span><div class="grow"><b>Copernic → Chelles</b><span>Mer. 1er oct. · tu conduis</span></div><span class="badge lav">1</span></div>
<div class="li click" data-conv><span class="avatars"><span class="avatar xs">AS</span></span><div class="grow"><b>Lavoisier → Chelles</b><span>Terminé · conversation fermée</span></div>{i("lock","sm")}</div>
</div>
<p class="small muted conv-note">{i("info","sm")} La conversation d'un trajet s'ouvre quand ta demande est acceptée.</p>
</aside>
<section class="card chat-main">
<div class="chat-head"><div class="grow"><h3>Noisy-le-Grand · Mont d'Est → Copernic</h3><span class="small muted">Régulier L M J V · départ 7 h 50 · Léa, Inès, Thomas et toi</span></div>
<a class="btn sm ghost" href="trajet.html#membre">Voir le trajet</a>
<button class="btn sm danger" type="button" data-open="signaler-compte">{i("flag","sm")}Signaler</button></div>
<div class="divider"></div>
<div class="chat">
<span class="daysep">Lundi 15 septembre</span>
<span class="sys">{i("car","sm")}<span><b>Léa</b> a créé le trajet</span></span>
<span class="sys">{i("join","sm")}<span><b>Mathis</b> a rejoint le trajet (L J V)</span></span>
<span class="sys">{i("join","sm")}<span><b>Inès</b> a rejoint le trajet (J V)</span></span>
<div class="bubble in"><span class="by">Léa</span>Bienvenue ! Je me gare devant la pharmacie du Mont d'Est.<small>18 h 02</small></div>
<span class="daysep">Hier</span>
<span class="sys">{i("edit","sm")}<span><b>Léa</b> a modifié l'heure de départ : <b>7 h 45 → 7 h 50</b></span></span>
<span class="sys red">{i("leave","sm")}<span><b>Chloé</b> a quitté le trajet</span></span>
<span class="sys">{i("join","sm")}<span><b>Thomas</b> a rejoint le trajet (V)</span></span>
<div class="bubble in"><span class="by">Inès</span>Je serai là 5 min avant demain.<small>20 h 14</small></div>
<div class="bubble out">Parfait, j'y serai à 7 h 45.<small>Toi · 20 h 20</small></div>
</div>
<div class="composer"><div class="input"><input id="chat-input" maxlength="300" placeholder="Écrire aux membres du trajet…" aria-label="Message"></div><button class="btn" type="button" data-toast="Message envoyé" aria-label="Envoyer">{i("send","sm")}<span class="hide-m">Envoyer</span></button></div>
<p class="small muted">{i("lock","sm")} Messagerie encadrée : numéros de téléphone et liens masqués. Fermée 24 h après la fin du trajet.</p>
</section>
<aside class="card tight members">
<h3>Membres du trajet</h3>
<div class="list">
<div class="li"><span class="avatar sm">LM</span><div class="grow"><b>Léa M.</b><span>Conductrice · {stars("4,9")}</span></div><button class="iconbtn flag" type="button" data-open="signaler-compte" aria-label="Signaler Léa" title="Signaler Léa">{i("flag","sm")}</button></div>
<div class="li"><span class="avatar sm">IN</span><div class="grow"><b>Inès N.</b><span>Passagère · J V</span></div><button class="iconbtn flag" type="button" data-open="signaler-compte" aria-label="Signaler Inès" title="Signaler Inès">{i("flag","sm")}</button></div>
<div class="li"><span class="avatar sm">TK</span><div class="grow"><b>Thomas K.</b><span>Passager · V</span></div><button class="iconbtn flag" type="button" data-open="signaler-compte" aria-label="Signaler Thomas" title="Signaler Thomas">{i("flag","sm")}</button></div>
<div class="li"><span class="avatar sm">MD</span><div class="grow"><b>Toi</b><span>Passager · L J V</span></div></div>
</div>
<button class="btn sm danger block" type="button" data-open="annuler">{i("leave","sm")}Quitter ce trajet</button>
</aside>
</div>
''', modals=M_SIGNALER_COMPTE + M_ANNULER)

# ================================================================== PROFIL
voiture = modal("voiture", f'''
<div data-step>
{dhead("Ajouter une voiture", "Elle pourra être choisie quand tu publies un trajet.", "car")}
<div class="grid-2" style="gap:12px">
<div class="field"><label for="v-marque">Marque</label>{inp("v-marque", "", "Ex. : Peugeot")}</div>
<div class="field"><label for="v-modele">Modèle</label>{inp("v-modele", "", "Ex. : 208")}</div>
</div>
<div class="field"><span class="label">Couleur</span><div class="row" style="gap:6px">{"".join(f'<button class="chip{" on" if c == "Grise" else ""}" data-radio type="button">{c}</button>' for c in ["Blanche", "Noire", "Grise", "Bleue", "Rouge", "Autre"])}</div></div>
<div class="field"><span class="label">Places passagers</span><div class="stepper" data-max="6"><button class="iconbtn" type="button" aria-label="Moins">−</button><b>3</b><button class="iconbtn" type="button" aria-label="Plus">+</button></div></div>
<p class="small muted">{i("shield","sm")} La plaque d'immatriculation n'est pas demandée.</p>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn" type="button" data-next data-loading>Ajouter la voiture</button></div>
</div>
<div data-step hidden>{success("Voiture ajoutée", "Tu peux maintenant la choisir en publiant un trajet.")}</div>
''')
PAGES["publier"]["modals"] = voiture
creneau = modal("creneau", f'''
<div data-step>
{dhead("Ajouter un créneau", "Tes horaires types servent à te proposer des trajets compatibles.", "clock")}
<div class="field"><span class="label">Jours</span>{days([2])}</div>
<div class="grid-2" style="gap:12px">
<div class="field"><label for="c-arr">Arrivée au campus</label>{inp("c-arr", "9 h 45", "", "clock")}</div>
<div class="field"><label for="c-dep">Départ du campus</label>{inp("c-dep", "12 h 30", "", "clock")}</div>
</div>
<div class="field"><span class="label">Point d'arrivée</span>{select("c-campus", "Cité Descartes · Copernic", "pin", dyn="arr")}</div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn" type="button" data-close data-toast="Créneau du mercredi ajouté">Ajouter le créneau</button></div>
</div>''')
edit_profile = modal("modifier-profil", f'''
{dhead("Modifier le profil", "Ces informations sont visibles par les membres de tes trajets.", "edit")}
<div class="row"><span class="avatar lg">MD</span><div class="stack" style="gap:6px"><button class="btn sm ghost" type="button" data-toast="Photo mise à jour">Changer la photo</button><button class="linkbtn red" type="button" data-toast="Photo retirée" style="font-size:13px">Retirer la photo</button></div></div>
<div class="grid-2" style="gap:12px">
<div class="field"><label for="e-prenom">Prénom</label>{inp("e-prenom", "Mathis")}</div>
<div class="field"><label for="e-nom">Nom <span class="muted" style="font-weight:400">(initiale affichée)</span></label>{inp("e-nom", "Dintrat")}</div>
</div>
<div class="field"><span class="label">Formation</span>{select("e-form", "BUT Informatique · 2e année", "user", [("IUT", ["BUT Informatique · 1re année", "BUT Informatique · 2e année", "BUT Informatique · 3e année", "BUT MMI · 2e année"]), ("Autres", ["Licence", "Master", "Personnel de l'université"])])}</div>
<div class="field"><label for="e-mail">E-mail universitaire</label><div class="input">{i("lock","sm")}<input id="e-mail" value="mathis.dintrat@edu.univ-eiffel.fr" disabled></div><span class="hint">Lié à ton compte universitaire, non modifiable.</span></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn" type="button" data-close data-toast="Profil mis à jour">Enregistrer</button></div>
''')
export = modal("export-donnees", f'''
<div data-step>
{dhead("Télécharger mes données", "Droit d'accès et de portabilité (RGPD, articles 15 et 20).", "download")}
<p>L'export contient ton profil, tes préférences, tes trajets, tes réservations, tes notes données et reçues, et tes messages encore conservés.</p>
<div class="field"><span class="label">Format</span><div class="seg" data-single><button type="button" class="on">JSON</button><button type="button">CSV</button></div></div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Annuler</button><button class="btn" type="button" data-next data-loading>{i("download","sm")}Préparer l'export</button></div>
</div>
<div data-step hidden>{success("Export prêt", "Un lien de téléchargement valable 48 h a été envoyé à mathis.dintrat@edu.univ-eiffel.fr.")}</div>
''')
delete = modal("supprimer-compte", f'''
<div data-step>
{dhead("Supprimer mon compte et mes données", "Droit à l'effacement (RGPD, article 17). Cette action est définitive.", "trash", True)}
<div class="notice red">{i("info")}<span>Seront supprimés : ton profil, tes préférences, tes véhicules, tes trajets à venir et tes messages. Tes trajets passés restent dans les statistiques, sous forme anonyme.</span></div>
<div class="notice">{i("users")}<span>Tes 2 trajets à venir seront annulés et leurs membres prévenus.</span></div>
<div class="field"><label for="del-confirm">Pour confirmer, écris <b>SUPPRIMER</b></label>{inp("del-confirm", "", "SUPPRIMER")}</div>
<div class="dialog-foot"><button class="btn ghost" type="button" data-close>Garder mon compte</button><button class="btn danger-solid is-disabled" id="del-go" type="button" disabled data-next data-loading>{i("trash","sm")}Supprimer définitivement</button></div>
</div>
<div data-step hidden>{success("Compte supprimé", "Tes données personnelles ont été effacées. Un e-mail de confirmation t'a été envoyé.", '<a class="btn ghost" href="connexion.html">Retour à la connexion</a>')}</div>
''')
slots = [("Lundi", "8 h 30", "17 h 30"), ("Mardi", "8 h 30", "18 h 00"), ("Jeudi", "9 h 45", "17 h 45"), ("Vendredi", "8 h 30", "12 h 30")]
slot_rows = "".join(f'<tr><td><b>{d}</b></td><td class="num">{a}</td><td class="num">{b}</td><td style="text-align:right;white-space:nowrap"><button class="iconbtn" type="button" data-open="creneau" aria-label="Modifier {d}" title="Modifier" style="width:34px;height:34px">{i("edit","sm")}</button> <button class="iconbtn" type="button" data-toast="Créneau du {d.lower()} supprimé" data-remove="tr" aria-label="Supprimer {d}" title="Supprimer" style="width:34px;height:34px;color:var(--danger)">{i("trash","sm")}</button></td></tr>' for d, a, b in slots)
PAGES["profil"] = dict(title="Profil", mtitle="Profil", body=f'''
<div class="split">
<div class="stack-lg">
<section class="card">
<div class="card-head"><div><h2>Mon campus et mes zones</h2><p class="small muted">Chaque campus a ses propres zones de rendez-vous, définies par l'université. Pas de géolocalisation, pas d'adresse.</p></div></div>
<div class="field"><span class="label">Campus</span>{select("pr-site", CAMPUS, "campus", [("Campus de l'Université Gustave Eiffel", [c[0] for c in CAMPUSES])], attrs=" data-campus-ctl")}<span class="hint">Change de campus : les zones de départ et les points d'arrivée ci-dessous se mettent à jour.</span></div>
<div class="grid-2">
<div class="field"><span class="label">Zone de départ habituelle</span>{select("pr-zone", "Noisy-le-Grand · Mont d'Est", "pin", dyn="dep")}</div>
<div class="field"><span class="label">Point d'arrivée habituel</span>{select("pr-campus", "Cité Descartes · Copernic", "pin", dyn="arr")}</div>
</div>
</section>
<section class="card">
<div class="card-head"><div><h2>Mes modes de déplacement</h2><p class="small muted">Comment viens-tu au campus ? Sert aux statistiques anonymisées de l'université et à te proposer les bons trajets.</p></div></div>
<div class="row modechips">{"".join(f'<button class="chip mchip m-{m}{" on" if m in ("car", "bike", "transit") else ""}" data-toggle type="button" aria-pressed="{"true" if m in ("car", "bike", "transit") else "false"}">{i(ic,"sm")}{lbl}</button>' for m, (lbl, ic) in MODES.items())}</div>
<div class="field"><span class="label">Mode principal</span><div class="seg" data-single>{"".join(f'<button type="button"{ACT.replace("active", "on") if m == "car" else ""}>{"Transports" if m == "transit" else lbl}</button>' for m, (lbl, ic) in MODES.items())}</div></div>
</section>
<section class="card">
<div class="card-head"><h2>Horaires types</h2><button class="btn sm" type="button" data-open="creneau">{i("plus","sm")}Ajouter un créneau</button></div>
<div class="table-wrap"><table class="table">
<thead><tr><th>Jour</th><th>Arrivée au campus</th><th>Départ du campus</th><th></th></tr></thead>
<tbody>{slot_rows}</tbody></table></div>
</section>
<section class="card">
<div class="card-head"><h2>Mes véhicules</h2><button class="btn sm ghost" type="button" data-open="voiture">{i("plus","sm")}Ajouter une voiture</button></div>
<div class="list">
<div class="li"><span class="iconbtn">{i("car","sm")}</span><div class="grow"><b>Renault Clio · grise</b><span>3 places passagers</span></div><button class="iconbtn" type="button" data-open="voiture" aria-label="Modifier la voiture" title="Modifier">{i("edit","sm")}</button><button class="iconbtn" type="button" data-toast="Voiture supprimée" data-remove=".li" aria-label="Supprimer la voiture" title="Supprimer" style="color:var(--danger)">{i("trash","sm")}</button></div>
</div>
</section>
<section class="card">
<h2>Préférences</h2>
<div class="field">{tp_head("Ce qui compte pour moi", PREFS)}{tagpick("pr-tags", PREFS)}
<span class="hint">Coche ou décoche d'un tap. Ces préférences sont comparées aux tags des trajets pour te proposer les plus compatibles.</span></div>
<div class="divider"></div>
<div class="optline"><span>Uniquement des trajets avec des étudiants de ma composante</span><button class="toggle" type="button" aria-pressed="false" aria-label="Ma composante uniquement"></button></div>
<div class="optline"><span>Notifications de nouvelles demandes</span><button class="toggle on" type="button" aria-pressed="true" aria-label="Notifications de demandes"></button></div>
<div class="optline"><span>Rappel 30 min avant le départ</span><button class="toggle on" type="button" aria-pressed="true" aria-label="Rappel de départ"></button></div>
</section>
<section class="card">
<h2>Confidentialité et données</h2>
<p class="small muted">U-Mobility applique le RGPD : tu peux consulter, exporter ou effacer tes données à tout moment.</p>
<div class="list">
<div class="li"><span class="iconbtn">{i("download","sm")}</span><div class="grow"><b>Télécharger mes données</b><span>Profil, trajets, notes et messages (JSON ou CSV)</span></div><button class="btn sm ghost" type="button" data-open="export-donnees">Télécharger</button></div>
<div class="li"><span class="iconbtn">{i("eye","sm")}</span><div class="grow"><b>Visibilité du profil</b><span>Nom complet visible uniquement par les membres de tes trajets</span></div><button class="toggle on" type="button" aria-pressed="true" aria-label="Visibilité limitée"></button></div>
<div class="li"><span class="iconbtn" style="color:var(--danger)">{i("trash","sm")}</span><div class="grow"><b>Supprimer mon compte et mes données</b><span>Effacement définitif de tes données personnelles</span></div><button class="btn sm danger" type="button" data-open="supprimer-compte">Supprimer</button></div>
</div>
</section>
</div>
<aside class="stack-lg">
<section class="card" style="justify-items:center;text-align:center">
<span class="avatar lg">MD</span>
<div><h2>Mathis D.</h2><p class="muted">BUT Informatique · 2e année</p><p class="small muted campus-line" style="justify-content:center">{i("campus","sm")}<span data-campus-name>{CAMPUS}</span></p></div>
<div class="stack" style="gap:2px;justify-items:center"><span class="small muted">Ma note</span>{stars("4,8", "48 notes")}</div>
<button class="btn ghost block" type="button" data-open="modifier-profil">{i("edit","sm")}Modifier le profil</button>
<button class="btn danger block" type="button" data-logout>{i("logout","sm")}Se déconnecter</button>
</section>
<div class="notice">{i("shield")}<span>Les autres membres voient ton prénom, l'initiale de ton nom, ta formation, ton campus et ta note moyenne.</span></div>
</aside>
</div>
''', modals=creneau + voiture + edit_profile + export + delete)

# ================================================================== MODÉRATION
sig = [
    ("#248", "Trajet", "Copernic → Paris 13e", "Tarif abusif (25 €)", "Aujourd'hui 9 h 12", "wait", "Nouveau", 1),
    ("#247", "Compte", "Compte #3481", "Absence au rendez-vous", "Aujourd'hui 8 h 40", "wait", "Nouveau", 3),
    ("#246", "Compte", "Compte #1022", "Comportement inapproprié", "Hier", "", "En cours", 2),
    ("#245", "Trajet", "Torcy → Bienvenüe", "Annonce commerciale", "22 sept.", "ko", "Trajet masqué", 1),
    ("#241", "Compte", "Compte #2107", "Harcèlement", "20 sept.", "ok", "Traité · suspendu 7 j", 4),
]
srows = "".join(
    f'<tr class="click" data-open="signalement"><td class="muted num">{n}</td><td><span class="badge line">{i("car" if t == "Trajet" else "user","sm")}{t}</span></td><td><b>{o}</b></td><td>{m}</td><td class="num">{c}</td><td class="muted" style="white-space:nowrap">{d}</td><td><span class="badge {cls}">{s}</span></td><td>{i("chevr","sm")}</td></tr>'
    for n, t, o, m, d, cls, s, c in sig)
PAGES["moderation"] = dict(title="Signalements", roles=("mod", "admin"), mtitle="Signalements", sub="Visible uniquement par les modérateurs et les administrateurs.", body=f'''
<div class="grid-4">
<div class="stat dark"><span class="k">{i("flag","sm")}À traiter</span><span class="v">3</span><span class="d m">dont 2 nouveaux</span></div>
<div class="stat"><span class="k">{i("clock","sm")}Délai moyen de traitement</span><span class="v">19 <small>h</small></span><span class="d">objectif 48 h</span></div>
<div class="stat"><span class="k">{i("eyeoff","sm")}Trajets masqués (30 j)</span><span class="v">3</span></div>
<div class="stat"><span class="k">{i("users","sm")}Comptes suspendus</span><span class="v">1</span></div>
</div>
<section class="card">
<div class="card-head"><div class="row" style="gap:6px"><button class="chip on" data-radio type="button">Tous</button><button class="chip" data-radio type="button">Comptes</button><button class="chip" data-radio type="button">Trajets</button><button class="chip" data-radio type="button">Nouveaux</button><button class="chip" data-radio type="button">Traités</button></div><div class="input" style="min-width:220px">{i("search","sm")}<input id="mod-q" placeholder="N° de signalement ou de compte" aria-label="Rechercher"></div></div>
<div class="table-wrap"><table class="table">
<thead><tr><th>N°</th><th>Type</th><th>Objet</th><th>Motif</th><th>Signalé</th><th>Reçu</th><th>Statut</th><th></th></tr></thead>
<tbody>{srows}</tbody></table></div>
</section>
<div class="notice">{i("lock")}<span>Les comptes sont pseudonymisés. L'identité ne s'affiche qu'à la demande dans le dossier, et chaque consultation est journalisée.</span></div>
''', modals=modal("signalement", f'''
<div class="dialog-head"><span class="ico red">{i("flag")}</span><div class="grow"><h2>Signalement #247</h2><p class="muted">Compte · Absence au rendez-vous · reçu aujourd'hui 8 h 40</p></div><button class="iconbtn" type="button" data-close aria-label="Fermer">{i("x","sm")}</button></div>
<div class="recap"><div class="between small"><span class="muted">Compte signalé</span><b>Compte #3481</b></div><div class="between small"><span class="muted">Signalé par</span><b>Compte #0917 (passager)</b></div><div class="between small"><span class="muted">Trajet concerné</span><b>Noisy → Copernic · 23 sept.</b></div><div class="between small"><span class="muted">Note moyenne du compte</span>{stars("3,1", 14)}</div></div>
<button class="linkbtn" type="button" data-toast="Identité affichée · consultation journalisée">{i("eye","sm")}Afficher l'identité (journalisé)</button>
<div class="field"><span class="label">Message du signalement</span><p class="small" style="background:var(--surface);padding:12px;border-radius:8px">« Le conducteur n'est pas venu et ne répond pas dans la messagerie. C'est la 2e fois. »</p></div>
<div class="field"><span class="label">Historique du compte</span><div class="list">
<div class="li"><span class="badge wait">#239</span><div class="grow"><b>Absence au rendez-vous</b><span>18 sept. · avertissement envoyé</span></div></div>
<div class="li"><span class="badge line">#221</span><div class="grow"><b>Retard répété</b><span>9 sept. · classé sans suite</span></div></div>
</div></div>
<div class="field"><label for="mod-note">Note interne</label>{textarea("mod-note", "Visible uniquement par les modérateurs.", 500)}</div>
<div class="stack" style="gap:8px">
<button class="btn block" type="button" data-close data-toast="Avertissement envoyé au compte #3481">Envoyer un avertissement</button>
<button class="btn danger-solid block" type="button" data-close data-toast="Compte #3481 suspendu 7 jours">Suspendre le compte 7 jours</button>
<button class="btn ghost block" type="button" data-close data-toast="Trajet masqué">{i("eyeoff","sm")}Masquer le trajet concerné</button>
<button class="btn quiet block" type="button" data-close data-toast="Signalement classé sans suite">Classer sans suite</button>
</div>
''', drawer=True))

# ================================================================== DONNÉES DU BACK OFFICE
wk = [("S34", 38), ("S35", 52), ("S36", 124), ("S37", 186), ("S38", 214), ("S39", 231)]
peak_hours = ["7h", "8h", "9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h"]
peak_data = {
    "Lun": [2, 4, 3, 1, 0, 1, 1, 0, 0, 1, 3, 4, 1], "Mar": [2, 4, 3, 1, 0, 1, 0, 1, 0, 1, 3, 3, 1],
    "Mer": [1, 3, 2, 1, 0, 3, 2, 0, 0, 0, 1, 1, 0], "Jeu": [2, 4, 4, 1, 0, 1, 1, 0, 1, 1, 3, 4, 1],
    "Ven": [1, 3, 2, 1, 1, 3, 2, 1, 0, 1, 2, 1, 0],
}
peak = '<div class="peak"><span></span>' + "".join(f"<span>{h}</span>" for h in peak_hours)
for d, vals in peak_data.items():
    peak += f'<span style="text-align:left">{d}</span>' + "".join(f'<i data-l="{v}" data-tip="{d} {peak_hours[k]} : {["moins de 5", "5 à 15", "15 à 30", "30 à 50", "plus de 50"][v]} trajets"></i>' for k, v in enumerate(vals))
peak += "</div>"
# ================================================================== BACK OFFICE (administrateur)
PAGES["back-office"] = dict(title="Back office · statistiques", roles=("admin",), mtitle="Statistiques", sub="Indicateurs consolidés et anonymisés · données au 24 sept. 2026",
    topright=f'''<div class="select" id="bo-campus" style="min-width:230px"><button type="button" aria-haspopup="listbox">{i("campus","sm")}<span>Tous les campus</span>{i("chev","sm chev")}</button><div class="options" role="listbox"><button type="button" class="opt sel">Tous les campus</button>{"".join(f'<button type="button" class="opt">{H.escape(c[0])}</button>' for c in CAMPUSES)}</div></div>'''
    f'<div class="seg" data-single><button type="button">Semaine</button><button type="button" class="on">Mois</button><button type="button">Année</button></div><button class="btn ghost" type="button" data-loadtoast="Bilan de septembre exporté (PDF)">{i("download","sm")}Exporter le bilan</button>', body=f'''
<div class="notice">{i("shield")}<span>Données anonymisées : aucun indicateur n'est affiché pour un groupe de moins de 10 personnes.</span></div>
<div class="grid-4">
<div class="stat dark"><span class="k">{i("users","sm")}Utilisateurs actifs</span><span class="v">1 284</span><span class="d">+212 ce mois-ci</span></div>
<div class="stat"><span class="k">{i("route","sm")}Trajets réalisés</span><span class="v">845</span><span class="d">+38 % vs sept. 2025</span></div>
<div class="stat"><span class="k">{i("leaf","sm")}CO₂ évité</span><span class="v">3,9 <small>t</small></span><span class="d m">depuis la rentrée</span></div>
<div class="stat"><span class="k">{i("car","sm")}Taux de remplissage</span><span class="v">2,6 <small>pers. / voiture</small></span><span class="d">+0,3 vs juin</span></div>
</div>
<div class="grid-4">
<div class="stat"><span class="k">{i("users","sm")}Conducteurs actifs</span><span class="v">312</span><span class="d m">24 % des actifs</span></div>
<div class="stat"><span class="k">{i("repeat","sm")}Trajets réguliers</span><span class="v">68 <small>%</small></span><span class="d m">des trajets publiés</span></div>
<div class="stat"><span class="k">{i("star","sm")}Note moyenne</span><span class="v">4,7 <small>/ 5</small></span><span class="d m">2 940 notes</span></div>
<div class="stat"><span class="k">{i("flag","sm")}Signalements</span><span class="v">0,6 <small>%</small></span><span class="d m">des trajets réalisés</span></div>
</div>
<div class="grid-2">
<section class="card">
<div class="card-head"><h2>Trajets réalisés par semaine</h2><span class="small muted">rentrée 2026</span></div>
{bars(wk, "S39", " trajets")}
</section>
<section class="card">
<div class="card-head"><h2>Zones de départ les plus actives</h2><span class="small muted">part des trajets</span></div>
<div class="stack">{hbars([("Noisy-Champs · RER A", 26), ("Noisy-le-Grand · Mont d'Est", 21), ("Torcy · Centre", 15), ("Chelles · Gare", 12), ("Lognes · Mandinet", 9), ("Autres zones", 17)], " %", 30)}</div>
</section>
</div>
<section class="card">
<div class="card-head"><div><h2>Heures de pointe</h2><p class="small muted">Départs vers ou depuis le campus, du lundi au vendredi</p></div>
<div class="heat-legend">Moins<i style="background:var(--heat-0)"></i><i style="background:var(--heat-1)"></i><i style="background:var(--heat-2)"></i><i style="background:var(--heat-3)"></i><i style="background:var(--heat-4)"></i>Plus</div></div>
<div class="table-wrap">{peak}</div>
</section>
<section class="card">
<div class="card-head"><div><h2>Part modale déclarée</h2><p class="small muted">Modes cochés dans « Mes modes de déplacement » (plusieurs choix possibles) · 1 284 profils</p></div></div>
<div class="stack">{hbars([("Voiture", 46, "car"), ("Transports en commun", 38, "transit"), ("Vélo", 11, "bike"), ("À pied", 5, "walk")], " %", 50)}</div>
</section>
<div class="grid-2">
<section class="card">
<h2>Répartition par composante</h2>
<div class="stack">{hbars([("IUT", 34), ("École d'ingénieurs", 22), ("UFR Sciences", 18), ("Personnels", 14), ("Autres", 12)], " %", 40)}</div>
</section>
<section class="card">
<div class="card-head"><h2>CO₂ évité par mois</h2><span class="small muted">en kg</span></div>
{bars([("Avr", 820), ("Mai", 1040), ("Juin", 610), ("Juil", 90), ("Août", 40), ("Sept", 1310)], "Sept", " kg")}
</section>
</div>
''', modals="")

# ================================================================== PLAN
PLAN = [
    ("Accès", "", [("connexion.html", "Connexion", "Comptes de démonstration par rôle")]),
    ("Utilisateur", "user", [
        ("index.html", "Tableau de bord", "Activité façon GitHub, prochains trajets, trajets à noter"),
        ("recherche.html", "Rechercher un trajet", "Modes de déplacement, zones du campus, tags, filtres"),
        ("trajet.html", "Détail du trajet (passager)", "Notes sans avis, demandes en attente"),
        ("trajet.html#demande", "Popup · demande pour rejoindre", "Jours, places, message facultatif"),
        ("trajet.html#signaler", "Popup · signaler un trajet", ""),
        ("trajet.html#membre", "Détail du trajet (passager confirmé)", "Tes jours, point de rendez-vous, annuler ma place"),
        ("trajet.html#velo", "Détail d'un trajet à vélo", "Sans prix ni limite de places, couleur du mode"),
        ("mon-trajet.html", "Mon trajet (conducteur)", "Passagers, demandes à accepter ou refuser"),
        ("mon-trajet.html#annuler-trajet", "Popup · annuler le trajet (conducteur)", ""),
        ("mon-trajet.html#signaler-compte", "Popup · signaler un passager", ""),
        ("publier.html", "Publier un trajet", "Voiture, vélo, à pied ou transports ; tags facultatifs"),
        ("publier.html#voiture", "Popup · ajouter une voiture", ""),
        ("mes-trajets.html", "Mes trajets", "Trajets à venir des deux rôles, annulation claire"),
        ("mes-trajets.html#annuler", "Popup · annuler ma place", ""),
        ("mes-trajets.html#annuler-trajet", "Popup · annuler le trajet", ""),
        ("historique.html", "Historique", "Trajets à noter, statistiques, trajets fréquents"),
        ("historique.html#noter-conducteur", "Popup · noter le conducteur", "5 étoiles, sans texte"),
        ("historique.html#noter-passagers", "Popup · noter les passagers", "5 étoiles, sans texte"),
        ("historique.html#signaler-compte", "Popup · signaler un compte", ""),
        ("messages.html", "Messagerie du trajet", "Messages système, membres"),
        ("messages.html#signaler-compte", "Popup · signaler un compte", ""),
        ("messages.html#annuler", "Popup · quitter le trajet", ""),
        ("profil.html", "Profil", "Campus et zones, modes, créneaux, véhicules, tags, RGPD"),
        ("profil.html#creneau", "Popup · ajouter un créneau", ""),
        ("profil.html#modifier-profil", "Popup · modifier le profil", ""),
        ("profil.html#voiture", "Popup · ajouter une voiture", ""),
        ("profil.html#export-donnees", "Popup · télécharger mes données", "RGPD"),
        ("profil.html#supprimer-compte", "Popup · supprimer mon compte", "RGPD"),
        ("index.html#loader", "Loader", "Chargement entre les pages"),
    ]),
    ("Modérateur", "mod", [("moderation.html", "Signalements", "Réservé aux modérateurs et administrateurs"), ("moderation.html#signalement", "Dossier de signalement", "Panneau latéral")]),
    ("Administrateur", "admin", [("back-office.html", "Back office · statistiques", "Statistiques anonymisées, part modale, filtre par campus"), ("moderation.html", "Signalements (vue admin)", "Même page, navigation administrateur")]),
]
plan_html = ""
for g, r, items in PLAN:
    sr = f' data-set-role="{r}"' if r else ""
    plan_html += f'<h2>{g}</h2><div class="plan">' + "".join(f'<a href="{h}"{sr}><b>{t}</b>{f"<span>{d}</span>" if d else ""}<code>{h}</code></a>' for h, t, d in items) + "</div>"
PAGES["plan"] = dict(title="Plan de la maquette", raw=True, modals="", app=f'''<div class="content" style="margin:0 auto">
<section class="hero plan-hero"><span class="arc a1" aria-hidden="true"></span><span class="arc a2" aria-hidden="true"></span><h1>Maquette <span style="white-space:nowrap">U-Mobility</span> v3</h1><p>Tous les écrans et popups, en version ordinateur et mobile. Chaque lien s'importe dans Figma avec html.to.design.</p></section>
{plan_html}
</div>''')

# ------------------------------------------------------------------ assemble
# Loader : les pointillés du logo continuent vers le bas avec la même perspective.
# Géométrie relevée sur le logo (coordonnées du fichier original) :
#   point de fuite y = 495,3 ; demi-largeur = 0,196 × (y − 495,3) ; axe x ≈ 457,3
#   tiret n : début d = 84 × 1,94^n, fin = début × 1,63 (d = y − point de fuite)
VPY, K, R, Q, D0 = 495.3, 0.196, 1.94, 1.63, 84.0
def road_polys(s=0.0):
    out = []
    for n in range(-2, 5):
        d1 = D0 * R ** (n + s); d2 = d1 * Q
        y1, y2 = VPY + d1, VPY + d2
        if y1 > 1160: continue
        cx1 = 457.3 + 0.0088 * (y1 - 582); cx2 = 457.3 + 0.0088 * (y2 - 582)
        out.append(f'<polygon points="{cx1 - K*d1:.1f},{y1:.1f} {cx1 + K*d1:.1f},{y1:.1f} {cx2 + K*d2:.1f},{y2:.1f} {cx2 - K*d2:.1f},{y2:.1f}"/>')
    return "".join(out)
LOADER = f'''<div class="loader" id="loader" role="status" aria-live="polite"><div class="lm">
<svg viewBox="140 100 640 1060" aria-hidden="true">
<defs><linearGradient id="lm-fg" gradientUnits="userSpaceOnUse" x1="0" y1="760" x2="0" y2="1110"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="lm-mask" maskUnits="userSpaceOnUse" x="140" y="572" width="640" height="590"><rect x="140" y="572" width="640" height="190" fill="#fff"/><rect x="140" y="760" width="640" height="400" fill="url(#lm-fg)"/></mask></defs>
<g class="road" mask="url(#lm-mask)" data-road>{road_polys(0)}</g>
<image href="assets/logo-loader.png" x="140" y="100" width="640" height="660"/>
</svg>
<p>Chargement…</p></div></div>'''


# Avatars : une couleur secondaire UGE stable par personne, calculée sur les initiales (classes av0…av6).
import re, zlib
AVATAR_RE = re.compile(r'class="avatar((?: xs| sm| lg)?)(?: b| l)? ?"([^>]*)>([A-ZÉ]{2})<')
def color_avatars(h):
    return AVATAR_RE.sub(lambda m: f'class="avatar{m.group(1)} av{zlib.crc32(("u-mobility" + m.group(3)).encode()) % 7}"{m.group(2)}>{m.group(3)}<', h)

# Espaces insécables : « 7 h 50 », « 2,50 € », « 1,4 kg » ne se coupent jamais en fin de ligne.
NB_RE = [(re.compile(r"(\d) h (\d)"), "\\1\u00a0h\u00a0\\2"), (re.compile(r"(\d) (h|€|kg|km|t|%)(?=[\s<.,)·/])"), "\\1\u00a0\\2")]
def nbsp(h):
    for rx, rep in NB_RE:
        h = rx.sub(rep, h)
    return h

for k, p in PAGES.items():
    if not p.get("raw"):
        p["app"] = app_page(k, p["title"], p["body"], roles=p.get("roles", ("user",)), active=p.get("active"),
                            sub=p.get("sub", ""), mtitle=p.get("mtitle"), back=p.get("back"), topright=p.get("topright", ""))
for p in PAGES.values():
    p["app"], p["modals"] = nbsp(color_avatars(p["app"])), nbsp(color_avatars(p["modals"]))

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700;800&display=swap">'

shutil.rmtree(EXPORT, ignore_errors=True)  # repart d'un dist/ propre (anciennes pages et polices)
os.makedirs(EXPORT, exist_ok=True)
shutil.copytree(ASSETS, os.path.join(EXPORT, "assets"), dirs_exist_ok=True)
css = open(os.path.join(ROOT, "styles.css"), encoding="utf-8").read()
js = open(os.path.join(ROOT, "app.js"), encoding="utf-8").read()
open(os.path.join(EXPORT, "styles.css"), "w", encoding="utf-8").write(css)
open(os.path.join(EXPORT, "app.js"), "w", encoding="utf-8").write(js)
open(os.path.join(EXPORT, "fonts.css"), "w", encoding="utf-8").write(open(os.path.join(ROOT, "fonts.css"), encoding="utf-8").read())
for k, p in PAGES.items():
    doc = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]} — U-Mobility</title>
<link rel="icon" href="assets/logo-indigo.svg" type="image/svg+xml">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="frame">
{p["app"]}
</div>
{p["modals"]}
{LOADER}
{DEMOBAR}
<script src="app.js"></script>
</body>
</html>
'''
    open(os.path.join(EXPORT, f"{k}.html"), "w", encoding="utf-8").write(doc)

# ---- artifact (une seule page, routeur par ancre)
logo = "data:image/png;base64," + base64.b64encode(open(os.path.join(ASSETS, "logo-blanc.png"), "rb").read()).decode()
logo_ld = "data:image/png;base64," + base64.b64encode(open(os.path.join(ASSETS, "logo-loader.png"), "rb").read()).decode()
def emb(s): return s.replace("assets/logo-blanc.png", logo).replace("assets/logo-loader.png", logo_ld)
order = ["plan", "connexion", "index", "recherche", "trajet", "mon-trajet", "publier", "mes-trajets", "historique", "messages", "profil", "moderation", "back-office"]
opts = "".join(f'<option value="{k}">{PAGES[k]["title"]}</option>' for k in order)
tpls = "".join(f'<template id="tpl-{k}">{PAGES[k]["app"]}</template><template id="tpl-{k}-m">{PAGES[k]["modals"]}</template>' for k in order)
SHELL_CSS = '''
body { background: var(--surface); }
body.device-m { background: #dddee2; }
body.device-m .frame { max-width: 390px; margin: 24px auto 96px; min-height: 844px; border-radius: 28px; overflow: hidden; box-shadow: 0 0 0 10px #0f273b, 0 30px 80px rgba(15,39,59,.35); }
body.device-m .frame .app { min-height: 844px; }
.shell-bar { position: fixed; right: 16px; bottom: 72px; z-index: 100; display: flex; align-items: center; gap: 6px; padding: 6px; border-radius: 999px; background: #0f273b; color: #fff; box-shadow: 0 10px 30px rgba(15,39,59,.35); font: 500 13px/18px var(--font-sans); }
.shell-bar select { background: #24394c; color: #fff; border: 0; border-radius: 999px; padding: 8px 12px; font: 600 13px/18px var(--font-sans); max-width: 220px; }
.shell-bar .dev { display: inline-flex; background: #24394c; border-radius: 999px; padding: 3px; }
.shell-bar .dev button { border: 0; background: transparent; color: #c8d0d8; padding: 6px 12px; border-radius: 999px; font: 600 12px/16px var(--font-sans); cursor: pointer; }
.shell-bar .dev button.on { background: #fff; color: #0f273b; }
.shell-bar label { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
@media (max-width: 700px) {
  .shell-bar { left: 8px; right: 8px; bottom: 8px !important; justify-content: space-between; } .shell-bar .dev { display: none; } .shell-bar select { max-width: none; flex: 1; }
  body.device-m { background: var(--surface); }
  body.device-m .frame { max-width: none; margin: 0; border-radius: 0; box-shadow: none; min-height: 0; }
  .tabbar { bottom: 60px !important; }
  .demobar { bottom: 136px; }
}
'''
SHELL_JS = '''
window.UMOB_SPA = true;
(function(){
  var frame = document.getElementById('frame'), mods = document.getElementById('modals'), sel = document.getElementById('pg');
  window.UMOB_render = function(page){
    var t = document.getElementById('tpl-' + page); if (!t) { page = 'plan'; t = document.getElementById('tpl-plan'); }
    frame.innerHTML = t.innerHTML.split('assets/logo-blanc.png').join(window.UMOB_LOGO); mods.innerHTML = document.getElementById('tpl-' + page + '-m').innerHTML;
    sel.value = page; document.title = 'U-Mobility';
  };
  sel.addEventListener('change', function(){ window.UMOB_navigate(sel.value + '.html'); });
  function setDev(d){ document.body.classList.toggle('device-m', d === 'm'); Array.prototype.forEach.call(document.querySelectorAll('.dev button'), function(b){ b.classList.toggle('on', b.getAttribute('data-dev') === d); }); try { localStorage.setItem('umob-dev', d); } catch (e) {} }
  Array.prototype.forEach.call(document.querySelectorAll('.dev button'), function(b){ b.addEventListener('click', function(){ setDev(b.getAttribute('data-dev')); }); });
  var saved = 'd'; try { saved = localStorage.getItem('umob-dev') || 'd'; } catch (e) {}
  setDev(saved);
})();
'''
art = f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>U-Mobility</title>
{FONTS}
<style>
{css}
{SHELL_CSS}
</style>
<div class="frame" id="frame"></div>
<div id="modals"></div>
{emb(LOADER)}
{DEMOBAR}
<div class="shell-bar" role="toolbar" aria-label="Aperçu de la maquette"><label for="pg">Écran</label><select id="pg">{opts}</select><div class="dev"><button type="button" data-dev="d">Ordinateur</button><button type="button" data-dev="m">Mobile</button></div></div>
{tpls}
<script>window.UMOB_LOGO = '{logo}';{SHELL_JS}</script>
<script>{js}</script>
'''
# preview.html : aperçu une page (routeur par ancre) — c'est ce fichier qui est publié en artifact Claude.
# Il est autonome (images en data URI, polices Google Fonts) : l'artifact bloque les fichiers externes.
open(os.path.join(EXPORT, "preview.html"), "w", encoding="utf-8").write(art)
# GitHub Pages : page 404 = plan du site, et pas de traitement Jekyll
shutil.copyfile(os.path.join(EXPORT, "plan.html"), os.path.join(EXPORT, "404.html"))
open(os.path.join(EXPORT, ".nojekyll"), "w").close()
print(f"{len(PAGES)} pages → {os.path.abspath(EXPORT)} · preview.html {len(art) // 1024} Ko")
