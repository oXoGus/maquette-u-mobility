import json
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8766/"
D = "/private/tmp/claude-501/-Users-mathis-d-projets-maquette-u-mobility/373aff1b-cd1a-4477-9f4f-12d0b415b620/scratchpad/a11y/"
PAGES = ["plan", "connexion", "index", "recherche", "trajet", "publier", "mes-trajets", "historique", "messages", "profil", "moderation", "direction"]

HELP = """
window.__rgb = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if(!m) return null; const p = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [p[0],p[1],p[2], p.length>3?p[3]:1]; };
window.__lum = c => { const f = x => { x/=255; return x<=0.03928? x/12.92 : Math.pow((x+0.055)/1.055,2.4); }; return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); };
window.__cr = (a,b) => { const x=__lum(a), y=__lum(b); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05); };
window.__bg = el => { let layers=[]; let e=el; while(e && e.nodeType===1){ const cs=getComputedStyle(e); if(cs.backgroundImage!=='none' && !cs.backgroundImage.startsWith('url("data:image/svg')) return null; const c=__rgb(cs.backgroundColor); if(c && c[3]>0){ layers.push(c); if(c[3]>=1) break; } e=e.parentElement; } let base=[255,255,255]; for(let i=layers.length-1;i>=0;i--){ const c=layers[i]; base=[0,1,2].map(k=>c[k]*c[3]+base[k]*(1-c[3])); } return base; };
window.__sel = el => { let s=el.tagName.toLowerCase(); if(el.id) s+='#'+el.id; if(el.className && typeof el.className==='string') s+='.'+el.className.trim().split(/\\s+/).join('.'); return s; };
window.__name = el => !el ? '' : (el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('placeholder') || '').trim().replace(/\\s+/g,' ').slice(0,50);
"""

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    # ---------- 1. contrast scan + focus + targets + reflow
    for w, h in [(1440, 900), (390, 844)]:
        ctx = b.new_context(viewport={"width": w, "height": h})
        pg = ctx.new_page()
        for k in PAGES:
            pg.goto(BASE + k + ".html"); pg.wait_for_timeout(300); pg.evaluate(HELP)
            contrast = pg.evaluate("""() => { const out=[]; const seen=new Set();
              document.querySelectorAll('body *').forEach(el => { if(!el.offsetParent && getComputedStyle(el).position!=='fixed') return;
                const txt=[...el.childNodes].filter(n=>n.nodeType===3 && n.textContent.trim()).map(n=>n.textContent.trim()).join(' '); if(!txt) return;
                const cs=getComputedStyle(el); if(cs.visibility==='hidden') return; let c=__rgb(cs.color); let op=1, e=el; while(e){ op*=parseFloat(getComputedStyle(e).opacity); e=e.parentElement; }
                const bg=__bg(el); if(!bg) return; const fg=[0,1,2].map(i=>c[i]*c[3]*op+bg[i]*(1-c[3]*op)); const r=__cr(fg,bg);
                const fs=parseFloat(cs.fontSize), fw=parseInt(cs.fontWeight); const large= fs>=24 || (fs>=18.66 && fw>=700); const th= large?3:4.5;
                if(r<th){ const key=__sel(el)+'|'+r.toFixed(2); if(!seen.has(key)){ seen.add(key); out.push({el:__sel(el), txt:txt.slice(0,40), ratio:+r.toFixed(2), fs, fw, disabled: !!el.closest('[disabled],.is-disabled,.off')}); } } });
              return out; }""")
            # focus walk
            pg.goto(BASE + k + ".html"); pg.wait_for_timeout(200); pg.evaluate(HELP)
            focus = []
            for n in range(80):
                pg.keyboard.press("Tab")
                f = pg.evaluate("""() => { const el=document.activeElement; if(!el || el===document.body) return null; const cs=getComputedStyle(el); const r=el.getBoundingClientRect();
                   const oc=__rgb(cs.outlineColor); const pbg=__bg(el.parentElement)||[255,255,255]; const own=__bg(el)||pbg;
                   return {sel:__sel(el), name:__name(el), outline:cs.outlineStyle+' '+cs.outlineWidth, ocr: cs.outlineStyle!=='none'? +__cr(oc,pbg).toFixed(2): null, boxShadow: cs.boxShadow.slice(0,60),
                     vis: r.width>0 && r.height>0, inView: r.top>=0 && r.bottom<=innerHeight+1, w:Math.round(r.width), h:Math.round(r.height), inModal: !!el.closest('.modal,.drawer')}; }""")
                if f is None: break
                if focus and f["sel"] == focus[0]["sel"] and f["name"] == focus[0]["name"]: break
                focus.append(f)
            targets = pg.evaluate("""() => [...document.querySelectorAll('a[href],button,input,textarea,[data-open],[data-conv],.select > button')].filter(e=>e.offsetParent).map(e=>{const r=e.getBoundingClientRect(); return {sel:__sel(e), name:__name(e), w:Math.round(r.width), h:Math.round(r.height)};}).filter(t=>t.w<44||t.h<44)""")
            clickable_nonfocus = pg.evaluate("""() => [...document.querySelectorAll('[data-open],[data-conv],[data-tip],.li.click,tr.click')].filter(e=>e.offsetParent!==null || e.closest('.modal,.drawer')).filter(e=>!(e.matches('a[href],button,input,textarea,select,[tabindex]'))).map(e=>__sel(e)+' :: '+__name(e).slice(0,30))""")
            res[f"{w}:{k}"] = dict(contrast=contrast, focus=focus, targets=targets, nonfocus=clickable_nonfocus)
        ctx.close()
    # ---------- 2. reflow 320 px (≈ 1280 px à 400 %) et 720 px (1440 à 200 %)
    reflow = {}
    for w in (320, 720):
        ctx = b.new_context(viewport={"width": w, "height": 800}); pg = ctx.new_page()
        for k in PAGES:
            pg.goto(BASE + k + ".html"); pg.wait_for_timeout(200)
            reflow[f"{w}:{k}"] = pg.evaluate("""(w) => { const sw=document.documentElement.scrollWidth; const over=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect(); return r.right>w+1 && e.offsetParent && !e.closest('.table-wrap,.heat-wrap,.options')}).slice(0,5).map(e=>e.tagName.toLowerCase()+'.'+(e.className||'')+' r='+Math.round(e.getBoundingClientRect().right)); return {sw, over}; }""", w)
        ctx.close()
    res["reflow"] = reflow
    # ---------- 3. text spacing 1.4.12
    ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page(); ts = {}
    for k in PAGES:
        pg.goto(BASE + k + ".html"); pg.wait_for_timeout(200)
        pg.add_style_tag(content="* { line-height:1.5 !important; letter-spacing:.12em !important; word-spacing:.16em !important; } p { margin-bottom: 2em !important; }")
        pg.wait_for_timeout(100)
        ts[k] = pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e=>{ if(!e.offsetParent) return false; const cs=getComputedStyle(e); return (cs.overflow.includes('hidden')||cs.overflowX==='hidden'||cs.textOverflow==='ellipsis') && (e.scrollWidth>e.clientWidth+1 || e.scrollHeight>e.clientHeight+1); }).slice(0,6).map(e=>e.tagName.toLowerCase()+'.'+e.className+' :: '+(e.innerText||'').slice(0,30))""")
    res["textspacing"] = ts
    ctx.close()
    b.close()
json.dump(res, open(D + "manual.json", "w"), ensure_ascii=False, indent=1)
print("ok")
