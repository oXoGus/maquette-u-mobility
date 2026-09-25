// Captures des écrans de dist/ pour la charte PDF (JPEG dans scripts/charte/img/).
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const D = path.resolve(__dirname, '../../dist') + '/', OUT = path.join(__dirname, 'img');
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const shot = async (p, file) => { await p.waitForTimeout(300); await p.screenshot({ path: path.join(OUT, file + '.jpg'), type: 'jpeg', quality: 84 }); };
  let p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.25 });
  for (const n of ['index', 'recherche', 'trajet', 'mes-trajets']) { await p.goto('file://' + D + n + '.html'); await shot(p, 'd-' + n); }
  await p.goto('file://' + D + 'trajet.html#demande'); await shot(p, 'd-demande');
  p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  for (const n of ['index', 'recherche', 'messages']) { await p.goto('file://' + D + n + '.html'); await shot(p, 'm-' + n); }
  p = await b.newPage({ viewport: { width: 1440, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto('file://' + D + 'recherche.html'); await p.waitForTimeout(300);
  await (await p.$('.trip')).screenshot({ path: path.join(OUT, 'c-trip.jpg'), type: 'jpeg', quality: 88 });
  await b.close();
})();
