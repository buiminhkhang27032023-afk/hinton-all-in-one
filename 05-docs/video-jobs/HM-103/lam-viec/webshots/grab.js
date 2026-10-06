const puppeteer = require('/workspace/AI-auto-generate-video/node_modules/puppeteer-core');
const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
(async () => {
  const browser = await puppeteer.launch({executablePath: '/usr/bin/google-chrome', headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars']});
  const out = {};
  for (const j of jobs) {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36');
    await page.setViewport({width: 1280, height: 1600, deviceScaleFactor: 1});
    if (j.block) await page.setRequestInterception(true), page.on('request', r => (['script','media','font'].includes(r.resourceType()) && !r.url().startsWith('file:')) ? r.abort() : r.continue());
    try { await page.goto(j.url, {waitUntil: 'domcontentloaded', timeout: 45000}); } catch (e) { console.error('goto', j.name, e.message); }
    await new Promise(r => setTimeout(r, j.wait || 4000));
    const rects = await page.evaluate((phrases) => {
      const res = {};
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const nodes = []; let full = '';
      while (walker.nextNode()) { nodes.push([walker.currentNode, full.length]); full += walker.currentNode.nodeValue; }
      const norm = s => s.replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"');
      const F = norm(full);
      for (const p of phrases) {
        const idx = F.indexOf(norm(p)); if (idx < 0) { res[p] = null; continue; }
        const locate = (off) => { for (let i = nodes.length - 1; i >= 0; i--) if (nodes[i][1] <= off) return [nodes[i][0], off - nodes[i][1]]; };
        const [sn, so] = locate(idx); const [en, eo] = locate(idx + p.length - 1);
        const r = document.createRange(); r.setStart(sn, so); r.setEnd(en, eo + 1);
        res[p] = Array.from(r.getClientRects()).filter(c => c.width > 2).map(c => [Math.round(c.left + scrollX), Math.round(c.top + scrollY), Math.round(c.right + scrollX), Math.round(c.bottom + scrollY)]);
      }
      return res;
    }, j.phrases);
    const H = Math.min(j.maxh || 12000, await page.evaluate(() => document.documentElement.scrollHeight));
    await page.setViewport({width: 1280, height: H, deviceScaleFactor: 1});
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({path: j.out, clip: {x: 0, y: 0, width: 1280, height: H}});
    out[j.name] = {file: j.out, h: H, rects};
    console.error('ok', j.name, H);
    await page.close();
  }
  fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
  await browser.close();
})();
