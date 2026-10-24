import { next } from '@vercel/functions';

const cookieName = '__Host-mr_access';
const loginPath = '/api/site-access';

export async function validSession(token: string, secret: string, now = Date.now()) {
  const match = /^(\d{10,})\.([a-f0-9]{64})$/.exec(token);
  if (!match) return false;
  const remaining = Number(match[1]) - Math.floor(now / 1000);
  if (remaining <= 0 || remaining > 86400) return false;
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
  const signature = Uint8Array.from(match[2].match(/../g)!, value => parseInt(value, 16));
  return crypto.subtle.verify('HMAC', key, signature, new TextEncoder().encode(match[1]));
}

export default async function middleware(request: Request) {
  const secret = process.env.SITE_ACCESS_SECRET ?? '';
  if (secret.length < 32 || !process.env.SITE_ACCESS_HASH) {
    return new Response('Site access is not configured.', { status: 503, headers: { 'Cache-Control': 'no-store' } });
  }
  const url = new URL(request.url);
  // Password verification happens in the server handler, never in browser code.
  if (url.pathname === loginPath) return next();
  const cookie = (request.headers.get('cookie') ?? '').split(';')
    .map(value => value.trim()).find(value => value.startsWith(cookieName + '='));
  if (await validSession(cookie?.slice(cookieName.length + 1) ?? '', secret)) return next();
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/assets/')) {
    return Response.json({ error: { code: 'SITE_PASSWORD_REQUIRED', message: 'Enter the site password.' } },
      { status: 401, headers: { 'Cache-Control': 'private, no-store' } });
  }
  return new Response(null, { status: 303, headers: { Location: loginPath, 'Cache-Control': 'private, no-store' } });
}

export const config = { matcher: '/:path*' };
