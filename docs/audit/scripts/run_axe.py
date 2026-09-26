import json, re, sys, collections
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8766/"
D = "/private/tmp/claude-501/-Users-mathis-d-projets-maquette-u-mobility/373aff1b-cd1a-4477-9f4f-12d0b415b620/scratchpad/a11y/"
AXE = open(D + "axe.min.js").read()
plan = open("/Users/mathis.d/projets/maquette-u-mobility/dist/plan.html").read()
urls = ["plan.html"] + re.findall(r'<a href="([^"]+)"><b>', plan)
urls += ["messages.html#annuler"]
seen = []
for u in urls:
    if u not in seen: seen.append(u)
urls = seen
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa", "best-practice"]
out = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 900), (390, 844)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, locale="fr-FR")
        pg = ctx.new_page()
        for u in urls:
            pg.goto(BASE + u)
            pg.wait_for_timeout(500)
            pg.add_script_tag(content=AXE)
            r = pg.evaluate("""async (tags) => { const r = await axe.run(document, {runOnly:{type:'tag', values: tags}, resultTypes:['violations','incomplete']});
              const m = v => ({id:v.id, impact:v.impact, tags:v.tags.filter(t=>/wcag|best/.test(t)), help:v.help, n:v.nodes.length,
                 nodes:v.nodes.slice(0,6).map(n=>({t:n.target.join(' '), html:n.html.slice(0,180), msg:(n.any.concat(n.all,n.none).map(x=>x.message).join(' | ')).slice(0,220)}))});
              return {v:r.violations.map(m), inc:r.incomplete.map(m)}; }""", TAGS)
            out.append({"url": u, "vp": w, **r})
            print(w, u, len([x for x in r["v"] if "best-practice" not in x["tags"] or any(t.startswith("wcag") for t in x["tags"])]), [f'{x["id"]}({x["n"]})' for x in r["v"]])
        ctx.close()
    b.close()
json.dump(out, open(D + "axe_results.json", "w"), ensure_ascii=False, indent=1)
