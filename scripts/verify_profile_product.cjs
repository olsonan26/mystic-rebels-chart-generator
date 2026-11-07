/* End-to-end real-chart demonstration. Birth input and artifacts stay in ignored
 * tmp; never add personal details to this script or public test fixtures.
 * Uses the running real API, installed Playwright and installed Chromium.
 */
const { chromium } = require(process.env.NADIA_PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');

(async () => {
  const inputFile = process.env.NADIA_PROFILE_BIRTH_FILE;
  if (!inputFile) throw new Error('Set NADIA_PROFILE_BIRTH_FILE to a local private JSON birth input.');
  const birth = JSON.parse(await fs.readFile(inputFile, 'utf8'));
  if (!birth.timezone) throw new Error('Include the expected IANA timezone in the private input for independent verification.');
  const out = path.resolve(__dirname, '../tmp/profile-product');
  await fs.mkdir(out, { recursive: true });
  const browser = await chromium.launch({ headless: true, slowMo: 120, ...(process.env.NADIA_CHROMIUM_EXECUTABLE ? { executablePath: process.env.NADIA_CHROMIUM_EXECUTABLE } : {}) });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1050 }, acceptDownloads: true,
      recordVideo: { dir: path.join(out, 'video'), size: { width: 1440, height: 1050 } } });
    const page = await context.newPage();
    const errors = [], posts = [], external = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('request', r => {
      if (r.method() === 'POST') posts.push(r.postData() || '');
      if (!new URL(r.url()).hostname.match(/^(127\.0\.0\.1|localhost)$/)) external.push(r.url().split('?')[0]);
    });
    await page.goto(process.env.NADIA_TEST_URL || 'http://127.0.0.1:5175');
    await page.getByLabel('Chart name', { exact: true }).fill(birth.name);
    await page.getByLabel('Birth date', { exact: true }).fill(birth.local_date);
    await page.getByLabel('Birth time', { exact: true }).fill(birth.local_time);
    await page.getByLabel('Time accuracy', { exact: true }).selectOption('nearest_minute');
    await page.getByLabel('Search birthplace', { exact: true }).fill(birth.birthplace_query);
    if (birth.coordinates) {
      await page.locator('.coordinate-details > summary').click();
      await page.getByLabel('Birthplace label', { exact: true }).fill(birth.location_name);
      await page.getByLabel('Latitude', { exact: true }).fill(String(birth.coordinates.latitude));
      await page.getByLabel('Longitude', { exact: true }).fill(String(birth.coordinates.longitude));
      await page.getByRole('button', { name: 'Find time zone from coordinates', exact: true }).click();
      await page.waitForFunction(expected => [...document.querySelectorAll('.coordinate-details input')].some(input => input.value === expected), birth.timezone);
    } else {
      const place = page.getByRole('option', { name: new RegExp(birth.birthplace_match) }).first();
      await place.click();
    }
    await page.screenshot({ path: path.join(out, '01-birth-details.png'), fullPage: true });
    await page.getByRole('button', { name: 'Generate chart', exact: true }).click();
    await page.locator('.nadia-open-report:not(:disabled)').waitFor();
    const close = page.getByRole('button', { name: 'Close chart chat', exact: true });
    if (await close.isVisible()) await close.click();
    await page.screenshot({ path: path.join(out, '02-calculated-chart.png'), fullPage: true });
    await page.getByRole('button', { name: 'Generate profile', exact: true }).click();
    await page.getByRole('heading', { name: birth.name, exact: true }).waitFor();
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('.nadia-synthetic').count(), 0);
    assert.equal(await page.locator('.nadia-placement-table tbody tr').count(), 10);
    assert.equal(await page.locator('.nadia-focus-item').count(), 2);
    await page.getByLabel('Inspect chart object', { exact: true }).selectOption('Moon');
    await page.screenshot({ path: path.join(out, '03-profile-desktop.png'), fullPage: true });
    await page.screenshot({ path: path.join(out, '03-profile-cover.png') });
    for (const [selector, filename] of [['.nadia-profile-overview', '03a-placements.png'], ['.nadia-profile-connections', '03b-connections.png'], ['.nadia-profile-focus', '03c-source-context.png'], ['.nadia-profile-review', '03d-review.png']]) {
      const section = page.locator(selector);
      await section.scrollIntoViewIfNeeded();
      await page.waitForTimeout(600);
      await section.screenshot({ path: path.join(out, filename) });
    }
    const note = 'PRIVATE_REFLECTION_TEST_NOT_FOR_EXPORT';
    await page.locator('#profile-reflection').fill(note);
    async function saveDownload(label, filename) {
      const event = page.waitForEvent('download');
      await page.getByRole('button', { name: label, exact: true }).click();
      await (await event).saveAs(path.join(out, filename));
    }
    await saveDownload('Download JSON', 'profile.json');
    await saveDownload('Download review brief', 'review-brief.txt');
    const packet = JSON.parse(await fs.readFile(path.join(out, 'profile.json'), 'utf8'));
    assert.equal(packet.synthetic, false);
    assert.equal(packet.profile.birth_time, birth.local_time);
    assert.equal(packet.profile.timezone, birth.timezone);
    assert.equal(packet.readiness.knowledge_status, 'verified');
    assert.equal(packet.readiness.complete_personal_reading, false);
    assert.equal(packet.review.status, 'required');
    assert.equal(packet.review.submitted, false);
    assert.equal(packet.lead.personalized_answer, null);
    for (const name of ['profile.json', 'review-brief.txt']) assert.ok(!(await fs.readFile(path.join(out, name), 'utf8')).includes(note));
    assert.ok(!posts.join('').includes(note));
    assert.ok(!await page.evaluate(n => Object.values(localStorage).some(v => v.includes(n)), note));
    await page.emulateMedia({ media: 'print' });
    assert.equal(await page.locator('#profile-reflection').isVisible(), false);
    await page.pdf({ path: path.join(out, 'NADIA-Profile.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
    await page.emulateMedia({ media: 'screen' });
    await page.locator('.nadia-technical-appendix > summary').click();
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: path.join(out, 'NADIA-Profile-with-evidence.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
    await page.emulateMedia({ media: 'screen' });
    await page.locator('.nadia-technical-appendix > summary').click();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => scrollTo(0, 0));
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await page.screenshot({ path: path.join(out, '04-profile-mobile.png'), fullPage: true });
    await page.getByRole('button', { name: 'Back to chart', exact: true }).click();
    await page.getByRole('button', { name: 'Generate profile', exact: true }).waitFor();
    assert.deepEqual(errors, []);
    assert.deepEqual(external, []);
    const result = { realApi: true, report_id: packet.report_id, actualBirthInput: packet.chart.input,
      verifiedCore: packet.core_identity, knowledgeStatus: packet.readiness.knowledge_status,
      placements: 10, sourceFocusComponents: 2, reviewRequired: true, reviewSubmitted: false,
      completePersonalReading: false, localExports: ['NADIA-Profile.pdf', 'NADIA-Profile-with-evidence.pdf', 'profile.json', 'review-brief.txt'],
      reflectionExcluded: true, externalRequests: external, mobileOverflow: false, pageErrors: errors,
      workflow: ['birth input', 'birthplace selection', 'calculate chart', 'generate profile', 'inspect Moon', 'download JSON', 'download review brief', 'export PDF', 'open evidence appendix', 'mobile report', 'back to chart'] };
    await fs.writeFile(path.join(out, 'results.json'), JSON.stringify(result, null, 2));
    const video = page.video();
    await context.close();
    if (video) await video.saveAs(path.join(out, 'NADIA-Profile-Flow.webm'));
    console.log(JSON.stringify({ status: 'passed', output: out, report_id: packet.report_id }));
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
