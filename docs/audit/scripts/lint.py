import re, os, glob, collections
from html.parser import HTMLParser
D = "/Users/mathis.d/projets/maquette-u-mobility/dist"
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr","path","circle","rect","polygon","stop","image"}
INTER = {"a","button"}
class P(HTMLParser):
    def __init__(s, name):
        super().__init__(); s.name=name; s.stack=[]; s.ids=collections.Counter(); s.opens=[]; s.hrefs=[]; s.issues=[]; s.classes=set(); s.fors=[]
    def handle_starttag(s, tag, attrs):
        a=dict(attrs)
        if "id" in a: s.ids[a["id"]]+=1
        if "for" in a: s.fors.append(a["for"])
        if "data-open" in a: s.opens.append(a["data-open"])
        if tag=="a" and "href" in a: s.hrefs.append(a["href"])
        for c in (a.get("class") or "").split(): s.classes.add(c)
        if tag in INTER or tag in ("input","select","textarea"):
            anc=[t for t,_ in s.stack if t in INTER]
            if anc: s.issues.append(f"<{tag} {a.get('class','')}> inside <{anc[-1]}> : {s.stack[-1]}")
        if tag in ("div","section","ol","ul","header","article","aside","p","h2") :
            if any(t in ("span","b","small","p") for t,_ in s.stack[-1:]) and tag!="span":
                s.issues.append(f"block <{tag}> inside inline <{s.stack[-1][0]}>")
        if tag=="div" and any(t=="p" for t,_ in s.stack): s.issues.append("div in p")
        if tag not in VOID: s.stack.append((tag,a.get("class","")))
    def handle_endtag(s, tag):
        if tag in VOID: return
        if s.stack and s.stack[-1][0]==tag: s.stack.pop(); return
        s.issues.append(f"mismatch </{tag}> ; open={[t for t,_ in s.stack[-4:]]}")
        for k in range(len(s.stack)-1,-1,-1):
            if s.stack[k][0]==tag: del s.stack[k:]; break
allclasses=set()
pages=sorted(glob.glob(D+"/*.html"))
for f in pages:
    n=os.path.basename(f)
    if n in("preview.html","404.html"): continue
    p=P(n); p.feed(open(f,encoding="utf-8").read())
    allclasses|=p.classes
    dup={k:v for k,v in p.ids.items() if v>1}
    missing=[o for o in set(p.opens) if ("m-"+o) not in p.ids]
    badfor=[x for x in p.fors if x not in p.ids]
    badh=[]
    for h in set(p.hrefs):
        if h.startswith("http"): continue
        fn=h.split("#")[0]
        if fn and not os.path.exists(os.path.join(D,fn)): badh.append(h)
    print("==",n,"dup:",dup,"missingOpen:",missing,"badFor:",badfor,"badHref:",badh)
    for x in p.issues[:15]: print("   ",x)
# CSS classes
css=open(D+"/styles.css").read()
cls=set(re.findall(r"\.([a-zA-Z][\w-]*)",re.sub(r"url\([^)]*\)","",css)))
js=open(D+"/app.js").read()
unused=sorted(c for c in cls if c not in allclasses and c not in js)
print("CSS classes unused in pages:",unused)
defs=set(re.findall(r"(--[\w-]+)\s*:",css)); uses=set(re.findall(r"var\((--[\w-]+)",css))
src=open("/Users/mathis.d/projets/maquette-u-mobility/src/build.py").read()
uses|=set(re.findall(r"var\((--[\w-]+)",src))
print("undefined vars:",sorted(uses-defs)); print("defined unused:",sorted(defs-uses))
