def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def blend(fg, a, bg):
    f = [int(fg.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]; b = [int(bg.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    return '#' + ''.join(f'{round(a*x+(1-a)*y):02x}' for x, y in zip(f, b))
def cr(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + .05) / (lb + .05)
T = dict(brand='#2f2a85', brand_soft='#ebeaf4', on_brand_muted='#d6d5ea', secondary='#8b4a97', accent='#fbba00', on_accent='#0f273b',
         surface='#f2f2f3', white='#ffffff', line='#dddee2', line_strong='#c4c6cd', ink='#0f273b', muted='#52606e', success='#007a5a',
         success_fill='#00936e', success_soft='#e0f2ec', danger='#d2213c', danger_hover='#b01b33', danger_soft='#fbe7ea', warning='#ef7d00',
         warning_ink='#9a4f00', warning_soft='#fff1d9')
C = {'magenta': ('#e83583', '#fce7f1', '#b3155c'), 'turquoise': ('#1eafd0', '#e1f4f9', '#006c85'), 'bleu': ('#0097d7', '#e1f1fa', '#00679a'),
     'vertclair': ('#92c56e', '#edf6e6', '#3d7020'), 'jaune': ('#fbba00', '#fff4d1', '#835c00'), 'orange': ('#ef7d00', '#fff1d9', '#9a4f00'),
     'violet': ('#8b4a97', '#f3eaf5', '#7a3f86'), 'vert': ('#00936e', '#e0f2ec', '#007a5a')}
t = T
rows = [
 ('--ink-muted / --surface (texte secondaire sur fond page)', t['muted'], t['surface'], 4.5),
 ('--ink-muted / --surface-raised', t['muted'], t['white'], 4.5),
 ('--ink-muted / --brand-soft (.sys, .req-group header span, .li.sel)', t['muted'], t['brand_soft'], 4.5),
 ('--ink-muted / --line (bouton désactivé)', t['muted'], t['line'], 4.5),
 ('--ink-muted / --warning-soft (.notice.warn)', t['muted'], t['warning_soft'], 4.5),
 ('--ink / --surface', t['ink'], t['surface'], 4.5),
 ('--brand / --brand-soft (.badge, .tag, .seg, .go)', t['brand'], t['brand_soft'], 4.5),
 ('--on-brand-muted / --brand (hero p, .brandmark span, stat.dark)', t['on_brand_muted'], t['brand'], 4.5),
 ('#eeedf7 / --brand (.nav a)', '#eeedf7', t['brand'], 4.5),
 ('--on-brand-muted / #3a3590 (.me small)', t['on_brand_muted'], '#3a3590', 4.5),
 ('#c9ecd8 / --brand (.stat.dark .d)', '#c9ecd8', t['brand'], 4.5),
 ('--accent / --brand (icône stat.dark, non-texte)', t['accent'], blend('#ffffff', .14, t['brand']), 3),
 ('--on-accent / --accent (.count, .seg .n)', t['on_accent'], t['accent'], 4.5),
 ('--accent / --surface-raised (jaune seul sur blanc)', t['accent'], t['white'], 3),
 ('blanc / --secondary (.btn.secondary, .badge.lav, .avatar)', '#ffffff', t['secondary'], 4.5),
 ('--secondary / --surface (.bubble .by 12px)', t['secondary'], t['surface'], 4.5),
 ('blanc / --danger (.btn.danger-solid, hover .btn.danger)', '#ffffff', t['danger'], 4.5),
 ('--danger / --surface-raised (.btn.danger 13-14px 700)', t['danger'], t['white'], 4.5),
 ('--danger-hover / --danger-soft (.badge.ko)', t['danger_hover'], t['danger_soft'], 4.5),
 ('--danger / --danger-soft (.linkbtn.red dans notice ?)', t['danger'], t['danger_soft'], 4.5),
 ('blanc / --success (.btn.success)', '#ffffff', t['success'], 4.5),
 ('--success / --success-soft (.badge.ok)', t['success'], t['success_soft'], 4.5),
 ('--success / --surface-raised (.stat .d)', t['success'], t['white'], 4.5),
 ('--warning-ink / --warning-soft (.badge.wait)', t['warning_ink'], t['warning_soft'], 4.5),
 ('--warning / --surface-raised (orange seul)', t['warning'], t['white'], 3),
 ('blanc / --brand-hover', '#ffffff', '#231f66', 4.5),
 ('blanc 75 % / --brand (.bubble.out small)', blend('#ffffff', .75, t['brand']), t['brand'], 4.5),
 ('--ink 75 % / --surface (.bubble.in small)', blend(t['ink'], .75, t['surface']), t['surface'], 4.5),
 ('blanc / rgba(255,255,255,.14) sur --brand (.hero .btn.secondary)', '#ffffff', blend('#ffffff', .14, t['brand']), 4.5),
 ('#7fd3b6 / --ink (icône toast)', '#7fd3b6', t['ink'], 3),
 ('placeholder Chrome #757575 / blanc', '#757575', t['white'], 4.5),
 ('--ink-muted 35 % (.days .off) / blanc', blend(t['muted'], .35, t['white']), t['white'], 4.5),
 ('.map .pin texte --ink / blanc', t['ink'], t['white'], 4.5),
 # non-texte (1.4.11 : 3:1)
 ('NT --line / blanc (bordure .input, .select, .tagbox)', t['line'], t['white'], 3),
 ('NT --line / blanc (contour .chip, .days, .badge.line)', t['line'], t['white'], 3),
 ('NT --line-strong / blanc (.toggle off, étoile vide .rate, .seat-free)', t['line_strong'], t['white'], 3),
 ('NT pastille blanche / --line-strong (.toggle off)', '#ffffff', t['line_strong'], 3),
 ('NT --brand / --brand-soft (.toggle on ? non : .seg on)', t['brand'], t['brand_soft'], 3),
 ('NT --brand (anneau focus) / blanc', t['brand'], t['white'], 3),
 ('NT --brand (anneau focus) / --surface', t['brand'], t['surface'], 3),
 ('NT --brand (anneau focus) / --brand (sidebar, hero, mobilebar)', t['brand'], t['brand'], 3),
 ('NT --brand (anneau focus) / #3a3590 (.me)', t['brand'], '#3a3590', 3),
 ('NT --brand-soft (halo focus champ) / blanc', t['brand_soft'], t['white'], 3),
 ('NT --heat-1 #c5c3e0 / --heat-0 #ebeaf4', '#c5c3e0', '#ebeaf4', 3),
 ('NT --heat-0 / blanc (case vide heatmap)', '#ebeaf4', t['white'], 3),
 ('NT --heat-2 #8d89c2 / blanc (barres)', '#8d89c2', t['white'], 3),
 ('NT --c-turquoise liseré .trip / blanc', C['turquoise'][0], t['white'], 3),
 ('NT --c-magenta liseré .trip / blanc', C['magenta'][0], t['white'], 3),
]
for n, (f, s, ink) in C.items():
    rows.append((f'--c-{n}-ink / --c-{n}-soft', ink, s, 4.5))
    rows.append((f'--c-{n}-ink / blanc', ink, t['white'], 4.5))
tags = ['magenta', 'turquoise', 'bleu', 'vertclair', 'jaune', 'violet']
for k, n in enumerate(tags):
    rows.append((f'.tag.t{k} (--c-{n}-ink / --c-{n}-soft)', C[n][2], C[n][1], 4.5))
av = [('av0 blanc / violet', '#ffffff', C['violet'][0]), ('av1 ink / turquoise', t['ink'], C['turquoise'][0]), ('av2 ink / jaune', t['ink'], C['jaune'][0]),
      ('av3 ink / vertclair', t['ink'], C['vertclair'][0]), ('av4 ink / orange', t['ink'], C['orange'][0]), ('av5 ink / bleu', t['ink'], C['bleu'][0]),
      ('av6 magenta-ink / magenta-soft', C['magenta'][2], C['magenta'][1]), ('.avatar.l brand / brand-soft', t['brand'], t['brand_soft'])]
for n, a, b in av: rows.append(('.avatar.' + n, a, b, 4.5))
rows += [('.role-tag svg blanc / --c-turquoise-ink', '#ffffff', C['turquoise'][2], 3), ('.role-tag svg blanc / --c-magenta-ink', '#ffffff', C['magenta'][2], 3)]
for n, a, b, th in rows:
    r = cr(a, b); print(f'{"OK  " if r >= th else "FAIL"} {r:5.2f}:1 (seuil {th})  {n}  [{a} sur {b}]')
