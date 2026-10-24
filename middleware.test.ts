import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createHmac } from 'node:crypto';
import middleware, { validSession } from './middleware';

const secret = 'test-session-secret-'.repeat(3);
function session(expiry = Math.floor(Date.now() / 1000) + 3600) {
  return `${expiry}.${createHmac('sha256', secret).update(String(expiry)).digest('hex')}`;
}
beforeEach(() => {
  vi.stubEnv('SITE_ACCESS_SECRET', secret);
  vi.stubEnv('SITE_ACCESS_HASH', 'server-only-test-record');
});
afterEach(() => vi.unstubAllEnvs());

describe('site access before static cache', () => {
  it('redirects a fresh visitor to the password form', async () => {
    const response = await middleware(new Request('https://example.test/'));
    expect(response.status).toBe(303);
    expect(response.headers.get('location')).toBe('/api/site-access');
  });
  it.each(['/api/charts', '/api/index.py', '/assets/app.js'])('blocks direct access to %s', async path => {
    expect((await middleware(new Request('https://example.test' + path))).status).toBe(401);
  });
  it('passes the form through to server-side password verification', async () => {
    expect((await middleware(new Request('https://example.test/api/site-access'))).headers.get('x-middleware-next')).toBe('1');
  });
  it('allows only an authentic unexpired session', async () => {
    expect(await validSession(session(), secret)).toBe(true);
    expect(await validSession(session(), 'different-secret')).toBe(false);
    expect(await validSession(session(Math.floor(Date.now() / 1000) - 1), secret)).toBe(false);
    expect(await validSession('forged-cookie', secret)).toBe(false);
    const request = new Request('https://example.test/assets/app.js', {headers: {cookie: '__Host-mr_access=' + session()}});
    expect((await middleware(request)).headers.get('x-middleware-next')).toBe('1');
  });
  it('fails closed if configuration is missing', async () => {
    vi.stubEnv('SITE_ACCESS_SECRET', '');
    expect((await middleware(new Request('https://example.test/'))).status).toBe(503);
  });
});
