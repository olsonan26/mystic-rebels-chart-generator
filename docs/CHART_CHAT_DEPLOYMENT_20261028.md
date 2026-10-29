# Chart chatbot production release — 28 October 2026

The owner requested “deploy please” after local validation and then explicitly selected **“Deploy without authenticated chat test.”** Source commit `265020b44b2000ea17d03b6b5cc0b24fe669bd73` is deployed to [www.cosmodynamicschart.site](https://www.cosmodynamicschart.site/) in the existing Astro Vercel project `prj_MBgBhgCUjxUwJ8OZO9OrqDqK4Vwl`.

Deployment `dpl_BzCTJE9dKNp147z5Fx4kYQpDNTCr` is READY. [Vercel inspection](https://vercel.com/astro-ac32/mystic-rebels-chart-generator/BzCTJE9dKNp147z5Fx4kYQpDNTCr). It was built from an exact Git archive, preserving separate unfinished location changes in the working checkout and private recovery checkpoint. Build duration to ready: approximately 155 seconds. The Python function uses Python 3.12 with a 60-second limit; its reported bundle size is 53,025,005 bytes. The production build includes the lazy-loaded chat client bundle and pinned HTTP client dependency.

Production configuration now includes server-only `OPENROUTER_API_KEY` as a Secret and `OPENROUTER_MODEL` as Config for `deepseek/deepseek-v4.1-flash-1017`. The existing password-gate and account configuration remain on Vercel. No credential values are in this receipt, Git or the source archive.

The deployment was built with production settings and delayed custom-domain promotion. After READY, promotion succeeded. The alias API independently confirmed the new deployment behind `www.cosmodynamicschart.site`, `cosmodynamicschart.site` and `mystic-rebels-chart-generator-seven.vercel.app`; the apex retains its redirect to `www`.

## Verification

- **Source/package integrity:** 83 selected source files, including all 28 deployed `data/knowledge` files, matched exact committed Git-archive bytes using Vercel's source SHA1 identifiers. Chat modules, source dependencies, client sources and configuration were covered. Private source media, environment files, local runtimes and private evidence were excluded. Source integrity is not proof of authenticated execution.
- **Protected public responses after promotion:** `/` redirects to `/api/site-access`; the Python login handler returns 200; anonymous chat status, chat POST and asset requests return 401 with `SITE_PASSWORD_REQUIRED`. Five checks passed without signing in.
- **Runtime observation:** the deployment's recent error-log query returned zero records in the checked 15-minute window. This was a narrow post-release scan, not ongoing monitoring or a test of authenticated chart/chat requests.
- **Prior local evidence:** 414 backend tests, 138 frontend tests and production build passed. A local real OpenRouter/browser test verified generation → popup → reviewed reply → explanation/download/persistence. Those local results are separate from production verification.
- **Authenticated production chat:** intentionally not run, at the owner's choice. No production reply, authenticated chart render, saved-chart cloud flow or model billing success is claimed. Browser automation was unavailable in Work settings. Automatic approval review rejected copying production access configuration locally; no such copy was made.

The release adds the supported bounded chart conversation and dated sky geometry. It does not complete Spark, directed OOI/aspect rules, Delegate synthesis or forecasting, and does not change full-report approval flags. Live Supabase row/Auth/Storage export remains unavailable as previously documented.

Machine-readable receipt: [deployment JSON](../evidence/chart-chat-production-deployment-20261028.json). The deployed source commit precedes this documentation-only receipt commit.
