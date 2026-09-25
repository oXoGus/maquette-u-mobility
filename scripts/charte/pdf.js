// Imprime scripts/charte/charte.html en A4 → docs/charte-graphique-u-mobility.pdf
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'charte.html')); await p.waitForTimeout(800);
  await p.pdf({ path: path.resolve(__dirname, '../../docs/charte-graphique-u-mobility.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
