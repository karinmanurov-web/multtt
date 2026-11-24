// node hashes.js out.json [sceneId...]  — хэши кадров каждые 0.5 с для сцен манифеста
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const out = process.argv[2]; const only = process.argv.slice(3);
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1200);
  const ids = await p.evaluate(() => fetch('manifest.json').then(r => r.json()).then(m => m.scenes.map(s => s.id)));
  const res = {};
  for (const id of ids) {
    if (only.length && !only.includes(id)) continue;
    for (const sv of await p.$$eval('#selStory option', o => o.map(x => x.value))) {
      await p.selectOption('#selStory', sv); await p.waitForTimeout(150);
      if (await p.$(`#selScene option[value="${id}"]`)) break;
    }
    await p.selectOption('#selScene', id); await p.waitForTimeout(800);
    res[id] = await p.evaluate(async () => {
      const e = multtt.eng; e.setQuality(0.25); const hs = [];
      for (let t = 0; t <= e.C.dur; t += 0.5) {
        e.render(t);
        const buf = new TextEncoder().encode(e.canvas.toDataURL('image/png'));
        const h = await crypto.subtle.digest('SHA-1', buf);
        hs.push([...new Uint8Array(h)].slice(0, 6).map(x => x.toString(16).padStart(2, '0')).join(''));
      }
      return hs;
    });
  }
  fs.writeFileSync(out, JSON.stringify(res));
  console.log(Object.entries(res).map(([k, v]) => k + ':' + v.length).join(' '), 'pageerrors', JSON.stringify(errs));
  await b.close();
})();
