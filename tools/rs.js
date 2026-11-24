// node rs.js scene lang times(comma) [prefix]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const [,, scene, lang, times, pre] = process.argv;
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://localhost:'+(process.env.PORT||8765)+'/index.html?v=' + Date.now()); await p.waitForTimeout(800);
  const r = await p.evaluate(async ([sc, lg]) => {
    const e = multtt.eng, lib = await (await fetch('library.json?' + Date.now())).json();
    const s = await (await fetch('scenes/' + sc + '.json?' + Date.now())).json(), tx = await (await fetch(lg + '?' + Date.now())).json();
    e.setLibrary(lib); e.setTexts(tx); const rep = e.load(s); return { errors: rep.errors, warnings: rep.warnings, dur: s.duration };
  }, [scene, lang]);
  console.log(JSON.stringify(r));
  for (const t of times.split(',')) {
    await p.evaluate(t => { multtt.eng.render(t); }, +t);
    const d = await p.evaluate(() => multtt.eng.ctx.canvas.toDataURL('image/png'));
    require('fs').writeFileSync(`shots/${pre || scene}_${t}.png`, Buffer.from(d.split(',')[1], 'base64'));
  }
  if (errs.length) console.log('pageerrors', errs);
  await b.close();
})();
