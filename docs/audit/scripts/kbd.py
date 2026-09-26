from playwright.sync_api import sync_playwright
BASE = "http://localhost:8766/"
AE = "(() => { const e=document.activeElement; return e===document.body? 'BODY' : e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+'.'+(e.className||'')+' «'+(e.getAttribute('aria-label')||e.innerText||'').trim().slice(0,30)+'» inModal='+!!e.closest('.modal,.drawer'); })()"
def ae(pg): return pg.evaluate(AE)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    print("== 1. Popup #demande ouverte au clavier (trajet.html)")
    pg.goto(BASE + "trajet.html"); pg.wait_for_timeout(300)
    pg.focus('[data-open="demande"]'); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    print("après Entrée :", ae(pg))
    out = []
    for n in range(25):
        pg.keyboard.press("Tab"); out.append(ae(pg))
    esc = [x for x in out if "inModal=false" in x]
    print("Tab x25 : sorties de la popup =", len(esc), "ex:", esc[:2])
    pg.keyboard.press("Shift+Tab")
    pg.focus('#m-demande [data-close]')
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    print("après Échap : modal ouverte ?", pg.evaluate("!!document.querySelector('.modal.open')"), "| focus :", ae(pg))
    print("fond inert/aria-hidden ?", pg.evaluate("[document.querySelector('.frame').inert, document.querySelector('.frame').getAttribute('aria-hidden')]"))

    print("== 2. Bouton data-loading : focus après envoi")
    pg.goto(BASE + "trajet.html#demande"); pg.wait_for_timeout(300)
    pg.focus('#m-demande [data-next]'); pg.keyboard.press("Enter"); pg.wait_for_timeout(100)
    print("pendant chargement :", ae(pg)); pg.wait_for_timeout(1100)
    print("étape succès affichée, focus :", ae(pg))

    print("== 3. Onglets Mes trajets : flèches")
    pg.goto(BASE + "mes-trajets.html"); pg.wait_for_timeout(300)
    pg.focus('[data-tab="avenir"]'); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(100)
    print("ArrowRight -> focus", ae(pg), "| panneau visible :", pg.evaluate("[...document.querySelectorAll('[data-panel-of=mt]')].filter(p=>!p.hidden).map(p=>p.dataset.panel)"))
    print("attributs onglet :", pg.evaluate("[...document.querySelectorAll('[data-tab]')].slice(0,4).map(b=>[b.getAttribute('role'),b.getAttribute('aria-selected'),b.getAttribute('aria-controls')])"))
    pg.keyboard.press("Enter"); pg.wait_for_timeout(100)

    print("== 4. Liste déroulante .select (recherche)")
    pg.goto(BASE + "recherche.html"); pg.wait_for_timeout(300)
    pg.focus('#s-dep > button'); pg.keyboard.press("Enter"); pg.wait_for_timeout(100)
    print("ouverte :", pg.evaluate("document.querySelector('#s-dep').classList.contains('open')"), "aria-expanded :", pg.evaluate("document.querySelector('#s-dep > button').getAttribute('aria-expanded')"))
    pg.keyboard.press("ArrowDown"); print("ArrowDown -> focus", ae(pg))
    pg.keyboard.press("Tab"); print("Tab -> focus", ae(pg))
    print("nom accessible du bouton :", pg.evaluate("(()=>{const b=document.querySelector('#s-dep > button'); return b.innerText.trim()})()"))
    print("rôles des options :", pg.evaluate("[...document.querySelectorAll('#s-dep .opt')].slice(0,2).map(o=>o.getAttribute('role')+'/'+o.getAttribute('aria-selected'))"))

    print("== 5. Notation .rate au clavier (mes-trajets#noter-conducteur)")
    pg.goto(BASE + "mes-trajets.html#noter-conducteur"); pg.wait_for_timeout(300)
    pg.focus('#rate-lea button:nth-child(4)'); pg.keyboard.press("Enter"); pg.wait_for_timeout(100)
    print("Entrée sur 4e étoile -> data-value", pg.evaluate("document.querySelector('#rate-lea').dataset.value"), "| label", pg.evaluate("document.querySelector('#rate-lea').parentNode.querySelector('.rate-label').textContent"))
    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(50)
    print("ArrowRight -> data-value", pg.evaluate("document.querySelector('#rate-lea').dataset.value"), "focus", ae(pg))
    print("aria-pressed/checked :", pg.evaluate("[...document.querySelectorAll('#rate-lea button')].map(b=>b.getAttribute('aria-pressed')||b.getAttribute('aria-checked'))"))

    print("== 6. Modération : ouvrir un signalement au clavier")
    pg.goto(BASE + "moderation.html"); pg.wait_for_timeout(300)
    stops = []
    for n in range(20):
        pg.keyboard.press("Tab"); stops.append(ae(pg))
    print("des <tr> atteints au Tab ?", any(s.startswith("tr") for s in stops))

    print("== 7. Messages : choisir une conversation / une personne à signaler")
    pg.goto(BASE + "messages.html#signaler-compte"); pg.wait_for_timeout(300)
    stops = []
    for n in range(15):
        pg.keyboard.press("Tab"); stops.append(ae(pg))
    print("des .li[data-conv] atteints au Tab ?", any("li click" in s for s in stops))

    print("== 8. Toast : région live ?")
    pg.goto(BASE + "recherche.html"); pg.wait_for_timeout(300)
    pg.click('[data-toast="Filtres réinitialisés"]'); pg.wait_for_timeout(100)
    print(pg.evaluate("(()=>{const t=document.querySelector('.toasts'); return [t.getAttribute('role'), t.getAttribute('aria-live')]})()"))

    print("== 9. Infobulles data-tip au focus")
    pg.goto(BASE + "index.html"); pg.wait_for_timeout(300)
    print("cellules focusables :", pg.evaluate("document.querySelectorAll('.heat [data-tip][tabindex]').length"), "/", pg.evaluate("document.querySelectorAll('.heat [data-tip]').length"))

    print("== 10. Retrait d'un tag : focus")
    pg.goto(BASE + "publier.html"); pg.wait_for_timeout(300)
    pg.focus('#p-tags'); pg.keyboard.type("Covoit"); pg.keyboard.press("Enter")
    print("nom du bouton ajouté :", pg.evaluate("[...document.querySelectorAll('.tagbox button')].pop().getAttribute('aria-label')"))
    pg.focus('.tagbox .tag button'); pg.keyboard.press("Enter"); pg.wait_for_timeout(50)
    print("après retrait, focus :", ae(pg))

    print("== 11. Stepper")
    pg.focus('.stepper .iconbtn[aria-label=Plus]'); pg.keyboard.press("Enter")
    print("valeur :", pg.evaluate("document.querySelector('.stepper b').textContent"), "aria-live ?", pg.evaluate("document.querySelector('.stepper b').getAttribute('aria-live')"))

    print("== 12. prefers-reduced-motion : loader")
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); q = ctx.new_page()
    q.goto(BASE + "index.html#loader"); q.wait_for_timeout(200)
    a1 = q.evaluate("document.querySelector('[data-road]').innerHTML"); q.wait_for_timeout(500)
    a2 = q.evaluate("document.querySelector('[data-road]').innerHTML")
    print("route animée en reduce ?", a1 != a2, "| durée anim .modal :", q.evaluate("getComputedStyle(document.querySelector('.loader')).animationDuration"))
    q.goto(BASE + "index.html#loader"); q2 = b.new_page(); q2.goto(BASE + "index.html#loader"); q2.wait_for_timeout(200)
    c1 = q2.evaluate("document.querySelector('[data-road]').innerHTML"); q2.wait_for_timeout(400); c2 = q2.evaluate("document.querySelector('[data-road]').innerHTML")
    print("route animée sans reduce ?", c1 != c2)
    print("aria-busy sur main ?", q.evaluate("document.querySelector('main').getAttribute('aria-busy')"))

    print("== 13. Titres par page")
    for k in ["index", "recherche", "messages", "mes-trajets", "connexion"]:
        pg.goto(BASE + k + ".html")
        print(k, pg.evaluate("[...document.querySelectorAll('h1,h2,h3,h4')].filter(h=>h.offsetParent).map(h=>h.tagName+':'+h.innerText.slice(0,25)).slice(0,8)"))
    pg.set_viewport_size({"width": 390, "height": 844})
    for k in ["recherche", "moderation"]:
        pg.goto(BASE + k + ".html")
        print("390", k, "h1 visibles :", pg.evaluate("[...document.querySelectorAll('h1')].filter(h=>h.offsetParent).length"), "| sub perdu :", pg.evaluate("(()=>{const s=document.querySelector('.topbar .sub'); return s? s.innerText + ' visible=' + !!s.offsetParent : null})()"))
    b.close()
