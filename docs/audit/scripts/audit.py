import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765/"
OUT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(OUT, "shots"); os.makedirs(SHOTS, exist_ok=True)
STATES = {
    "connexion": [""], "plan": [""], "index": ["", "loader"], "recherche": [""],
    "trajet": ["", "demande", "signaler"], "publier": ["", "voiture"],
    "mes-trajets": ["", "avenir", "recues", "envoyees", "anoter", "annuler", "annuler-trajet", "noter-conducteur", "noter-passagers", "signaler-compte"],
    "historique": ["", "noter-passagers"], "messages": ["", "signaler-compte", "annuler"],
    "profil": ["", "creneau", "modifier-profil", "voiture", "export-donnees", "supprimer-compte"],
    "moderation": ["", "signalement"], "direction": [""],
}
WIDTHS = [int(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else "320,360,390,768,899,901,1024,1280,1440,1920".split(","))]
SHOT_W = {320, 390, 899, 1440}

JS = open(os.path.join(OUT, "checks.js")).read()

res = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in WIDTHS:
        h = 844 if w <= 430 else (1024 if w <= 900 else 900)
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=w <= 900, reduced_motion="reduce")
        pg = ctx.new_page()
        for page, states in STATES.items():
            for st in states:
                url = f"{BASE}{page}.html" + (f"#{st}" if st else "")
                pg.goto("about:blank")
                pg.goto(url, wait_until="networkidle")
                pg.wait_for_timeout(250)
                r = pg.evaluate(JS)
                r.update(page=page, state=st, width=w)
                res.append(r)
                if w in SHOT_W:
                    name = f"{page}{'_' + st if st else ''}_{w}.png"
                    modal = r.get("modalOpen")
                    pg.screenshot(path=os.path.join(SHOTS, name), full_page=not modal)
        ctx.close()
    b.close()
json.dump(res, open(os.path.join(OUT, f"results_{'_'.join(map(str,WIDTHS)) if len(WIDTHS)<3 else 'all'}.json"), "w"), ensure_ascii=False, indent=1)
print("done", len(res))
