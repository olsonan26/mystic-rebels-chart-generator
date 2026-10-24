# Mystic Rebels site access

The deployed site uses a shared-password gate without requiring visitors to hold a Vercel account. The routing middleware checks a signed session before serving pages or static assets. The Python ASGI entrypoint separately verifies the session before serving chart API requests, including direct function URLs.

Set `SITE_ACCESS_HASH` and `SITE_ACCESS_SECRET` as server-only Vercel environment variables in production and preview, then redeploy. The hash record format is `pbkdf2_sha256$240000$salt_hex$digest_hex`. Generate a random salt and derive the digest using PBKDF2-HMAC-SHA256. The signing secret must contain at least 32 random characters. Never add either variable to a `VITE_` variable or client code.

Sessions expire after 24 hours and use a Secure, HttpOnly, SameSite=Lax, host-only cookie. Rotate the hash and signing secret together to change the password and invalidate previous sessions. Missing deployment configuration fails closed. Local development remains open when neither variable nor `VERCEL` is set.

Verification: `python -m pytest access_qa -q` and `npm test` cover wrong passwords, authentic sessions, forged or expired cookies, cross-origin login requests, missing configuration, and direct asset/API access. Deployment verification must also check the actual host routing, login form, password submission, and authenticated chart generation.

This access boundary does not change calculation inputs, astronomical results, chart exports, or wheel rendering.
