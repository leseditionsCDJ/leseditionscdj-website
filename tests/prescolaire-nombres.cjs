/* Exécution : node tests/prescolaire-nombres.cjs URL_DU_SITE [NOM_DE_PAGE] */
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:8123';
const only = process.argv[3];
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  // Silent speech implementation records French phrases without relying on system voices.
  await context.addInitScript(() => {
    window.spokenPhrases = [];
    Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: {
      cancel() {}, getVoices() { return []; }, addEventListener() {},
      speak(u) { window.spokenPhrases.push(u.text); }
    }});
  });
  const page = await context.newPage(); const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('response', r => { if(r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
  const filenames = only ? [only] : ['prescolaire-5-ans-chiffre-ecoute.html'];
  let totalRounds = 0;
  for (const filename of filenames) {
    await page.goto(`${base}/plateforme-educative/${filename}`);
    const age = Number(await page.locator('body').getAttribute('data-number-age'));
    const ranges = age === 5 ? [[1,10],[11,20],[21,31],[1,31]] : [[1,5],[6,10],[11,15],[1,15]];
    const mode = await page.evaluate(() => CFG.mode);
    await page.locator('.club-settings summary').click(); await page.locator('#effects').uncheck(); await page.locator('.club-settings summary').click();
    for(const [min,max] of ranges) {
      await page.selectOption('#number-band', `${min}-${max}`);
      const seen = new Set();
      const roundsToRun = Math.ceil((max-min+1)/Math.min(6,max-min+1));
      for(let run=0;run<roundsToRun;run++) {
        if(run) await page.locator('#replay').click();
        const count = await page.evaluate(() => rounds.length);
        for(let i=0;i<count;i++) {
          const d = await page.evaluate(() => rounds[round]); seen.add(d.n);
          assert(d.n >= min && d.n <= max);
          if(mode === 'numberListen') {
            const target = String(d.n), tiles = page.locator('#play button.tile');
            const choices = await tiles.evaluateAll(es=>es.map(e=>e.getAttribute('aria-label')));
            assert.equal(choices.length, age===5?4:3); assert.equal(new Set(choices).size,choices.length);
            assert(choices.includes(target));
            for(const v of choices) assert(Number(v)>=min&&Number(v)<=max);
            const visible = await tiles.allTextContents(); assert(visible.some(v=>v.trim()===target));
            const wrong = page.getByRole('button',{name:choices.find(v=>v!==target),exact:true});
            await wrong.click(); assert(await page.locator('#next').isHidden());
            await page.locator('#listen').click();
            assert((await page.evaluate(()=>window.spokenPhrases.at(-1))).includes(target));
            await page.getByRole('button',{name:target,exact:true}).focus(); await page.keyboard.press('Enter');
          } else if(mode === 'numberMatch') {
            await page.getByRole('button',{name:`Panier de ${d.n} objets`,exact:true}).click();
          } else if(mode === 'numberOrder') {
            const vals=await page.locator('#play .tile').evaluateAll(es=>es.map(e=>Number(e.getAttribute('aria-label'))).sort((a,b)=>a-b));
            assert(vals[0]>=min && vals.at(-1)<=max);
            for(const v of vals) await page.getByRole('button',{name:String(v),exact:true}).click();
          } else if(mode === 'numberMissing') {
            const answer=await page.evaluate(()=>{let es=[...document.querySelectorAll('#play>.display-model>svg,#play>.display-model>.slot')];let idx=es.findIndex(e=>e.classList.contains('slot'));let first=es[0].textContent;return idx===0?Number(es[1].textContent)-1:Number(first)+idx;});
            assert(answer>=min&&answer<=max); await page.getByRole('button',{name:String(answer),exact:true}).click();
          } else if(mode === 'countTouch') {
            assert.equal(await page.locator('#play .tile').count(),d.n);
            for(const tile of await page.locator('#play .tile').all()) await tile.click();
          } else if(['feed','countMake','equal'].includes(mode)) {
            const plus=page.getByRole('button',{name:'Ajouter',exact:true});
            for(let j=0;j<d.n+1;j++) await plus.click();
            await page.getByRole('button',{name:'Vérifier',exact:true}).click();
            assert(await page.locator('#next').isHidden());
            await page.getByRole('button',{name:'Retirer',exact:true}).click();
            await page.getByRole('button',{name:'Vérifier',exact:true}).click();
          } else if(mode === 'moreLess') {
            const choices=await page.locator('#play button.tile').evaluateAll(es=>es.map(e=>Number(e.getAttribute('aria-label').match(/\d+/)[0])));
            assert.equal(new Set(choices).size,2); for(const v of choices)assert(v>=min&&v<=max);
            const more=(await page.locator('#instruction').textContent()).includes('plus');
            await page.getByRole('button',{name:`Panier de ${more?Math.max(...choices):Math.min(...choices)} objets`,exact:true}).click();
          } else if(mode === 'share') {
            for(const tile of await page.locator('#play .tile').all()) await tile.click();
          } else throw new Error('Test de résolution manquant '+mode);
          assert(await page.locator('#next').isVisible(),`La manche ${mode} n'est pas résolue`);
          await page.locator('#next').click(); totalRounds++;
        }
        assert(await page.locator('#finish').isVisible());
      }
      for(let n=min;n<=max;n++)assert(seen.has(n),`Nombre ${n} absent du palier ${min}-${max}`);
    }
    await page.setViewportSize({width:390,height:844});
    await page.locator('#replay').click();
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Débordement sur téléphone');
    await page.screenshot({path:`/workspace/work/${filename}.png`,fullPage:true});
    await page.locator('#restart').click(); assert(await page.locator('#next').isHidden());
    await page.reload(); assert.equal(await page.locator('#number-band').inputValue(),`1-${age===5?31:15}`);
    // Blocked storage must neither prevent startup nor band changes.
    await page.evaluate(()=>{Storage.prototype.setItem=()=>{throw new Error('blocked')};Storage.prototype.getItem=()=>{throw new Error('blocked')};});
    await page.selectOption('#number-band',`${ranges[0][0]}-${ranges[0][1]}`);
    assert((await page.locator('#play').innerHTML()).length>0); assert((await page.locator('#instruction').textContent()).length>0);
    await page.setViewportSize({width:1280,height:900});
    console.log(`PASS ${filename}: tous les paliers et toutes les valeurs, erreurs, fin, clavier, stockage, mobile`);
  }
  // Navigation and unavailable audio are independently exercised for the first 5-year game.
  if(filenames.includes('prescolaire-5-ans-chiffre-ecoute.html')) {
    await page.goto(`${base}/plateforme-educative/index.html#/annees/prescolaire-5`);
    await page.waitForURL('**/prescolaire-5-ans.html');
    await page.locator('a[href="prescolaire-5-ans-chiffre.html"]').click();
    await page.locator('a[href="prescolaire-5-ans-chiffre-ecoute.html"]').click();
    await page.evaluate(()=>{Object.defineProperty(window,'speechSynthesis',{value:undefined,configurable:true});});
    await page.locator('#listen').click(); assert(await page.locator('#voice-note').isVisible());
    await page.getByRole('button',{name:'Abonnement',exact:true}).click(); assert(await page.locator('#club-info').isVisible());
  }
  assert.deepEqual(errors,[]);
  console.log(`PASS total ${totalRounds} manches. Aucune erreur JavaScript ou HTTP.`);
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
