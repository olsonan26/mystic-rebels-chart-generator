/* Actual local UI, calculator, authenticated review and report/PDF demonstration.
 * Private birth and example text are supplied by an ignored local file, never
 * embedded in this public test driver. No external inference or source upload.
 */
const { chromium } = require(process.env.NADIA_PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const url = process.env.NADIA_REVIEW_URL || 'http://127.0.0.1:8011';

(async () => {
  assert.ok(['127.0.0.1','localhost'].includes(new URL(url).hostname), 'Private demonstrations require loopback');
  let ready=false;
  for(let attempt=0;attempt<30;attempt++) {
    try { if((await fetch(url+'/api/health')).ok) { ready=true;break; } } catch {}
    await new Promise(resolve=>setTimeout(resolve,300));
  }
  assert.ok(ready,'Start the local practitioner service before the demonstration.');
  const input = JSON.parse(await fs.readFile(process.env.NADIA_REVIEW_DEMO_FILE, 'utf8'));
  const password = (await fs.readFile(path.join(root, 'tmp/practitioner-private/sign-in.txt'), 'utf8')).trim();
  const out = path.join(root, 'tmp/practitioner-demo/completed-flow'); await fs.mkdir(out, { recursive: true });
  const browser = await chromium.launch({ headless: true, ...(process.env.NADIA_CHROMIUM_EXECUTABLE ? { executablePath: process.env.NADIA_CHROMIUM_EXECUTABLE } : {}) });
  const results = [];
  try {
    for (const fixture of input.fixtures) {
      const directory = path.join(out, fixture.id); await fs.mkdir(directory, { recursive: true });
      const context = await browser.newContext({ viewport: { width: 1440, height: 1050 }, acceptDownloads: true,
        recordVideo: { dir: path.join(directory, 'video'), size: { width: 1440, height: 1050 } } });
      const page = await context.newPage(); const errors = [], external = [];
      page.on('pageerror', e => errors.push(e.message));
      page.on('request', r => { if (!['127.0.0.1', 'localhost'].includes(new URL(r.url()).hostname)) external.push(r.url().split('?')[0]); });
      await page.goto(url);
      if (fixture.birth) {
        const b = fixture.birth;
        await page.getByLabel('Chart name', { exact: true }).fill(b.name);
        await page.getByLabel('Birth date', { exact: true }).fill(b.local_date);
        await page.getByLabel('Birth time', { exact: true }).fill(b.local_time);
        await page.getByLabel('Time accuracy', { exact: true }).selectOption(b.time_accuracy);
        await page.locator('.coordinate-details > summary').click();
        await page.getByLabel('Birthplace label', { exact: true }).fill(b.location_name);
        await page.getByLabel('Latitude', { exact: true }).fill(String(b.latitude));
        await page.getByLabel('Longitude', { exact: true }).fill(String(b.longitude));
        await page.getByRole('button', { name: 'Find time zone from coordinates', exact: true }).click();
        await page.waitForFunction(expected => [...document.querySelectorAll('.coordinate-details input')].some(i => i.value === expected), b.timezone);
      }
      await page.getByRole('button', { name: 'Generate chart', exact: true }).click();
      await page.locator('.nadia-open-report:not(:disabled)').waitFor();
      const chat = page.getByRole('button', { name: 'Close chart chat', exact: true });
      if (await chat.isVisible()) await chat.click();
      await page.getByRole('button', { name: 'Generate profile', exact: true }).click();
      await page.locator('.nadia-placement-table tbody tr').first().waitFor();
      assert.equal(await page.locator('.nadia-placement-table tbody tr').count(), 10);
      await page.screenshot({ path: path.join(directory, '01-calculated-profile.png'), fullPage: true });
      await page.getByRole('button', { name: 'Practitioner workspace', exact: true }).click();
      await page.getByLabel('Practitioner password', { exact: true }).fill(password);
      await page.getByRole('button', { name: 'Sign in', exact: true }).click();
      await page.getByRole('button', { name: 'Prepare selected chart', exact: true }).waitFor();
      await page.getByRole('button', { name: 'Prepare selected chart', exact: true }).click();
      await page.getByRole('heading', { name: 'What do I need to feel loved?', exact: true }).waitFor();
      await page.screenshot({ path: path.join(directory, '02-prepared-case.png'), fullPage: true });
      if (fixture.id === 'synthetic') await page.setViewportSize({ width: 390, height: 844 });
      const refs = await context.request.get(url + '/api/practitioner/references');
      assert.equal(refs.status(), 200);
      const benchmark = await refs.json(); assert.equal(benchmark.strongest_reference.id, 'source-C-venus-moon-v1');
      const photograph = await context.request.get(url + '/api/practitioner/source/original-page-542');
      assert.equal(photograph.status(), 200); assert.ok(photograph.headers()['content-type'].includes('image/jpeg'));
      await page.locator('.review-evidence > details > summary').filter({ hasText: 'Expert-reference reconstruction' }).click();
      await page.getByRole('button', { name: 'Load local reference', exact: true }).click();
      await page.locator('.review-reference h3').waitFor();
      await page.locator('.review-evidence > details > summary').filter({ hasText: 'Expert-reference reconstruction' }).click();
      for (const [index, role] of ['recognition', 'explanation', 'practical_application'].entries()) {
        const block = page.locator('.review-claim').nth(index);
        await block.getByLabel('Reader-facing text', { exact: true }).fill(fixture.text[role]);
        await block.locator('.review-claim-evidence > summary').click();
        await block.getByLabel('Supporting evidence', { exact: true }).selectOption(fixture.evidence_ids || ['point:Moon']);
        await block.getByLabel('Source references', { exact: true }).selectOption(fixture.source_refs || ['original-page-112']);
        await block.getByLabel('Why the interpretation follows', { exact: true }).fill(fixture.rationale);
        await block.getByLabel('Unknown conditions and limits', { exact: true }).fill(fixture.limitations);
        await block.getByLabel('Rejected alternative', { exact: true }).fill('A fluent statement or a source citation alone establishes this person’s dominant love need.');
      }
      await page.getByRole('button', { name: 'Save question draft', exact: true }).click();
      await page.getByText('Draft saved. Changed items require a new review.', { exact: true }).waitFor();
      await page.screenshot({ path: path.join(directory, '03-authored-draft.png'), fullPage: true });
      for (let i = 0; i < 3; i++) {
        const block = page.locator('.review-claim').nth(i);
        await block.locator('.review-decision > summary').click();
        await block.getByLabel('Review note', { exact: true }).fill('Workflow example checked for labels, linked evidence and explicit limits; not expert certification of a personal interpretation.');
        await block.getByRole('checkbox').check();
        await block.getByRole('button', { name: 'Approve individually', exact: true }).click();
        await block.locator('.state-approved').waitFor();
      }
      await page.locator('.review-evidence > details > summary').filter({ hasText: 'Review history' }).click();
      await page.getByRole('button', { name: 'Load review history', exact: true }).click();
      await page.screenshot({ path: path.join(directory, '04-individual-review.png'), fullPage: true });
      await page.setViewportSize({ width: 390, height: 844 });
      await page.screenshot({ path: path.join(directory, '05-mobile-editor.png'), fullPage: true });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false, 'Mobile editor overflow');
      await page.setViewportSize({ width: 1440, height: 1050 });
      await page.getByRole('button', { name: 'Open reviewed report', exact: true }).click();
      await page.locator('.nadia-individual-insights').waitFor();
      await page.evaluate(() => document.fonts.ready);
      assert.equal(await page.locator('.nadia-individual-insights').count(), 1);
      const download = page.waitForEvent('download');
      await page.getByRole('button', { name: 'Download reviewed report JSON', exact: true }).click();
      await (await download).saveAs(path.join(directory, 'reviewed-report.json'));
      const report = JSON.parse(await fs.readFile(path.join(directory, 'reviewed-report.json'), 'utf8'));
      assert.equal(report.demonstration, true); assert.equal(report.automated_interpretation_authorized, false);
      assert.equal(report.packet.readiness.complete_personal_reading, false);
      assert.equal(report.packet.readiness.knowledge_status, 'verified');
      assert.equal(report.incomplete_questions.length, 8);
      const record = await context.request.get(url + `/api/practitioner/cases/${report.case_id}`);
      await fs.writeFile(path.join(directory, 'private-review-case.json'), JSON.stringify(await record.json(), null, 2));
      await page.screenshot({ path: path.join(directory, '06-reviewed-report.png'), fullPage: true });
      await page.pdf({ path: path.join(directory, 'NADIA-Reviewed-Profile-DEMONSTRATION.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
      await page.setViewportSize({ width: 390, height: 844 });
      await page.screenshot({ path: path.join(directory, '07-mobile-report.png'), fullPage: true });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false, 'Mobile report overflow');
      const library = await context.request.get(url + '/api/practitioner/benchmarks');
      assert.deepEqual(await library.json(), []);
      await page.getByRole('button', { name: 'Back to review', exact: true }).click();
      await page.getByRole('button', { name: 'Sign out', exact: true }).click();
      await page.getByRole('button', { name: 'Sign in', exact: true }).waitFor();
      assert.equal((await context.request.get(url + `/api/practitioner/cases/${report.case_id}`)).status(), 401);
      assert.deepEqual(errors, []); assert.deepEqual(external, []);
      const result = { fixture: fixture.id, chart_id: report.packet.chart.chart_id, case_id: report.case_id,
        revision: report.revision, approved_items: 3, completed_questions: 1, incomplete_questions: 8,
        content: 'clearly_labeled_demonstration_not_expert_reading', source_image_verified: true,
        authorship_and_item_review_viewport: fixture.id === 'synthetic' ? '390x844_mobile' : '1440x1050_desktop',
        benchmark_reference_loaded: true, secondary_use: false, mobile_editor_overflow: false,
        mobile_report_overflow: false, unauthenticated_case_access: 401, page_errors: errors, external_requests: external };
      results.push(result); await fs.writeFile(path.join(directory, 'results.json'), JSON.stringify(result, null, 2));
      const video = page.video(); await context.close(); if (video) await video.saveAs(path.join(directory, 'workflow.webm'));
    }
    await fs.writeFile(path.join(out, 'results.json'), JSON.stringify(results, null, 2));
    console.log(JSON.stringify({ status: 'passed', fixtures: results.map(r => r.fixture), artifacts: out }));
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
