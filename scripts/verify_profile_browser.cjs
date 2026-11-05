/* Real-browser report regression. Outputs stay in ignored tmp, never CI artifacts.
 * Set NADIA_PLAYWRIGHT_MODULE to an installed playwright module when not local.
 * Set NADIA_CHROMIUM_EXECUTABLE to use an already installed Chromium binary.
 * Start the existing API/Vite app first; no mocked chart or interpretation API.
 */
const {chromium} = require(process.env.NADIA_PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const out = path.resolve(ROOT, 'tmp/profile-browser');
const base = process.env.NADIA_TEST_URL || 'http://127.0.0.1:5173';

async function openReport(page) {
  await page.locator('.nadia-open-report:not(:disabled)').waitFor({state:'visible'});
  const close = page.getByRole('button',{name:'Close chart chat',exact:true});
  if (await close.isVisible()) await close.click();
  await page.getByRole('button',{name:'Generate profile',exact:true}).click();
}

(async () => {
  await fs.mkdir(out, {recursive:true});
  const browser = await chromium.launch({headless:true, ...(process.env.NADIA_CHROMIUM_EXECUTABLE ? {executablePath:process.env.NADIA_CHROMIUM_EXECUTABLE} : {})});
  const results = [];
  try {
    for (const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]) {
      const context = await browser.newContext({viewport:{width,height},acceptDownloads:true});
      const page = await context.newPage();
      await page.addInitScript(()=>{ window.__nadiaPrintCalls=0; window.print=()=>{window.__nadiaPrintCalls++;}; });
      const failures=[];
      const posted=[];
      page.on('request',request=>{if(request.method()==='POST')posted.push(request.postData()||'');});
      page.on('pageerror', error=>failures.push(error.message));
      await page.goto(base);
      await page.getByRole('button',{name:'Load synthetic example',exact:true}).click();
      await page.getByRole('button',{name:'Generate profile',exact:true}).waitFor({state:'visible'});
      await openReport(page);
      await page.getByRole('article',{name:'NADIA profile report'}).waitFor();
      await page.getByRole('button',{name:'Download JSON',exact:true}).waitFor();
      await page.evaluate(()=>document.fonts.ready);
      assert.equal(await page.getByText('Synthetic demonstration · not a real person\'s reading',{exact:true}).count(),1);
      assert.equal(await page.locator('.nadia-report-wheel svg').count(),1);
      await page.getByRole('button',{name:/^Moon,/}).click();
      await page.getByLabel('Inspect chart object',{exact:true}).selectOption('Sun');
      assert.equal(await page.locator('.nadia-report-wheel svg [role="button"][aria-pressed="true"]').count(),1);
      assert.equal(await page.locator('[data-profile-section="placement-moon"]').count(),1);
      const overflow=await page.evaluate(()=>({body:document.documentElement.scrollWidth,view:innerWidth}));
      assert.ok(overflow.body<=overflow.view+1, JSON.stringify({name,overflow}));
      const note='PRIVATE_REFLECTION_TEST_NOT_FOR_EXPORT';
      await page.getByLabel('When have you felt understood and cared for, and what did the other person do?').fill(note);
      const downloadWait=page.waitForEvent('download');
      await page.getByRole('button',{name:'Download JSON',exact:true}).click();
      const download=await downloadWait;
      await download.saveAs(path.join(out,`${name}.json`));
      const packet=JSON.parse(await fs.readFile(path.join(out,`${name}.json`),'utf8'));
      assert.equal(packet.synthetic,true);
      assert.equal(packet.profile.birth_date,'2000-01-01');
      assert.equal(packet.profile.timezone,'Etc/UTC');
      assert.equal(packet.readiness.complete_personal_reading,false);
      assert.equal(packet.lead.personalized_answer,null);
      assert.ok(!JSON.stringify(packet).includes(note));
      assert.ok(!posted.join('').includes(note),'Reflection was sent to a server');
      assert.ok(!await page.evaluate(note=>Object.values(localStorage).some(v=>v.includes(note)),note),'Reflection persisted');
      assert.equal(await page.locator('a.nadia-booking').count(),packet.lead.booking_url ? 1 : 0);
      await page.getByLabel('Profile',{exact:true}).selectOption('premium');
      await page.getByText('Premium profile',{exact:true}).waitFor();
      await page.screenshot({path:path.join(out,`${name}.png`),fullPage:true});
      await page.evaluate(()=>window.scrollTo(0,0));
      await page.screenshot({path:path.join(out,`${name}-viewport.png`)});
      if(name==='desktop'){
        await page.getByRole('button',{name:'Print / save PDF',exact:true}).click();
        assert.equal(await page.evaluate(()=>window.__nadiaPrintCalls),1);
        await page.emulateMedia({media:'print'});
        assert.equal(await page.locator('#profile-reflection').isVisible(),false);
        await page.pdf({path:path.join(out,'nadia-synthetic-profile.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,
          displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:8px;color:#555;width:100%;text-align:center">NADIA synthetic demonstration — <span class="pageNumber"></span> / <span class="totalPages"></span></div>'});
        await page.emulateMedia({media:'screen'});
        await page.getByRole('button',{name:'Back to chart',exact:true}).click();
        const longName='Synthetic long-name verification '.repeat(4).slice(0,120);
        await page.getByLabel('Chart name',{exact:true}).fill(longName);
        await page.getByLabel('Time accuracy',{exact:true}).selectOption('unknown');
        await page.getByRole('button',{name:'Generate chart',exact:true}).click();
        await openReport(page);
        await page.getByRole('article',{name:'NADIA profile report'}).waitFor();
        await page.getByRole('heading',{name:longName,exact:true}).waitFor();
        const missingDownload=page.waitForEvent('download');
        await page.getByRole('button',{name:'Download JSON',exact:true}).click();
        await (await missingDownload).saveAs(path.join(out,'unknown-time.json'));
        const missing=JSON.parse(await fs.readFile(path.join(out,'unknown-time.json'),'utf8'));
        assert.deepEqual(missing.chart.angles,{});
        assert.ok(missing.chart.points.every(p=>p.house===null));
        assert.ok(!missing.sections.some(s=>s.status==='source_context'));
        await page.emulateMedia({media:'print'});
        await page.pdf({path:path.join(out,'nadia-unknown-time-long-name.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true});
        await page.emulateMedia({media:'screen'});
        await page.setViewportSize({width:390,height:844});
        assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Long name overflows mobile');
        await page.screenshot({path:path.join(out,'mobile-long-name.png')});
        await page.getByRole('button',{name:'Back to chart',exact:true}).click();
        if (await page.getByRole('button',{name:'Close chart chat',exact:true}).isVisible()) {
          await page.getByRole('button',{name:'Close chart chat',exact:true}).click();
        }
        await page.getByLabel('Search birthplace',{exact:true}).fill('London');
        await page.getByRole('option',{name:/^London, United Kingdom/}).first().click();
        await page.getByRole('button',{name:'Generate chart',exact:true}).click();
        await openReport(page);
        await page.getByRole('article',{name:'NADIA profile report'}).waitFor();
        assert.ok((await page.locator('.nadia-birth-summary').innerText()).includes('Europe/London'),'Selected birthplace did not determine timezone');
        results.push({case:'unknown_time_long_name',houseOutputsWithheld:true,fullNameRendered:true,mobileOverflow:false});
        results.push({case:'birthplace_search',citySelected:true,ianaTimezone:'Europe/London'});
      }
      assert.deepEqual(failures,[]);
      assert.ok(!posted.join('').includes(note),'Reflection was transmitted after a tier change');
      results.push({viewport:name,width,height,horizontalOverflow:false,syntheticFixture:true,jsonDownload:true,tierSelector:true,chartSvg:true,reflectionExcludedFromJson:true,bookingConfigured:!!packet.lead.booking_url,pageErrors:failures});
      await context.close();
    }
    // Controlled configuration variants, reusing a real calculated report.
    // The .invalid address is test-only and is never visited or a live booking.
    for (const [url,expected] of [['https://booking.example.invalid/consultation',1],['javascript:alert(1)',0]]) {
      const context=await browser.newContext(); const page=await context.newPage();
      await page.route('**/api/profile-reports',async route=>{
        const response=await route.fetch(); const data=await response.json();
        data.lead.booking_url=url;
        await route.fulfill({response,json:data});
      });
      await page.goto(base);
      await page.getByRole('button',{name:'Load synthetic example',exact:true}).click();
      await openReport(page);
      await page.getByRole('article',{name:'NADIA profile report'}).waitFor();
      assert.equal(await page.locator('a.nadia-booking').count(),expected);
      if(expected){
        assert.equal(await page.locator('a.nadia-booking').getAttribute('href'),url);
        assert.equal(await page.locator('a.nadia-booking').getAttribute('rel'),'noopener noreferrer');
      }
      await context.close();
    }
    results.push({case:'booking_configuration_variants',testOnlyHttpsRendered:true,javascriptRejected:true,externalNavigation:false});
    await fs.writeFile(path.join(out,'results.json'),JSON.stringify({realApi:true,pdf:'nadia-synthetic-profile.pdf',results},null,2)+'\n');
    console.log(JSON.stringify({status:'passed',results,outputDirectory:'tmp/profile-browser'}));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
