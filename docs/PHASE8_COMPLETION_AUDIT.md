# Phase 8 completion audit — 2026-11-04

## Deployment architecture corrected

The authenticated Vercel account is `x12dna-4793`, Astro (`astro-ac32`), team
`team_8iuNbs04mGL8bwcfLrYefuKD`. The library project is
`nadia-knowledge-core`, ID `prj_RvvHnVbF9ydRxmSK0l3BzKAKKojs`.
Deployment `dpl_8azZR13DyQfJag1jDxLmoaTyz2tQ` attempted production from private
core `main`, exact commit `5a472f5f8236aa53ae90529a91a6ad20dd9e1382`.
The build logs confirm `PYTHON_ENTRYPOINT_NOT_FOUND`: Vercel auto-selected the
Python application framework for a library with no HTTP entrypoint.

Applied project settings: `commandForIgnoringBuildStep=exit 0` and
`previewDeploymentsDisabled=true`. The dashboard independently read back
Ignored Build Step **Don't build anything**, command **exit 0**. Also removed
only this project's Vercel Git repository connection. The dashboard then showed
the Git provider connection choices instead of a linked repository; subsequent
authenticated Git deployment context reported no linked library project.
Git pushes can no longer automatically deploy that library project. The old
failed deployment remains history; no replacement dummy application was built.
The private GitHub repository, CI and v0.7.0 release were preserved.

## Actual consumer found

The authenticated default Vercel scope and dashboard identify the existing
`mystic-rebels-chart-generator`, project `prj_MBgBhgCUjxUwJ8OZO9OrqDqK4Vwl`,
in the same Astro team. Explicit-team connector lookups inconsistently returned
404 or omitted this project; default-scope lookup and authenticated dashboard
both succeeded. Do not repeat the conclusion that the project is absent.

The dashboard confirms GitHub link `olsonan26/mystic-rebels-chart-generator` and
Production > Branch Tracking = **main**. PR #6 continues targeting
`codex/phsr-numerology-integration-20261028`; merging there is integration only
and may create a preview, not automatic Git production. No production branch,
domain or ownership setting was changed.

Latest existing READY production deployment: `dpl_HANKwJ2ddujE6iKZYL216GjDjWeh`,
URL `https://mystic-rebels-chart-generator-gq4ge6ytc-astro-ac32.vercel.app`.
Its API response contains no Git SHA: do not claim it includes this PR.
Existing domains include `www.cosmodynamicschart.site`, `cosmodynamicschart.site`
and `mystic-rebels-chart-generator-seven.vercel.app`. These are existing legacy
deployments/domains, not newly deployed NADIA-core integration URLs.

Project Vercel SSO/password/IP protection is disabled; the application retains
its own site-password boundary. Production and preview have site-access
variables, with production/preview Supabase variables. Provider configuration
is production-only. No NADIA health token, core reader or build-enablement
variable was present. Values were not decrypted or logged.

## Private build stage repaired

Previously, `vercel.json` only ran the frontend build, so it could not install
the private library. It now runs `python scripts/build_nadia.py` first. The
hook fails before network access unless private-build enablement, the exact
consumer project, explicit preview/production environment, dedicated health
token and scoped core reader are present. Production additionally requires
`NADIA_PRODUCTION_ENABLED=true`; no enablement or credential was added to Vercel.

The hook downloads only from the private core release API, checks repository,
release commit, wheel name/size and SHA256, strips repository authorization from
cross-origin asset redirects, rejects insecure/untrusted redirect targets and
uses offline installation. HTTP bodies, signed URLs and tokens are not logged.
`nadia_runtime.py` separates standard-library integrity/import verification from
FastAPI, so this stage can run before the Python function's web dependencies are
installed. The backend reuses the same verifier and original reading gates.
The web build remains independent in public CI; the private package is included
only in the server function configuration, never `dist`.

The protected workflow now also triggers on pushes to the integration branch.
This repairs another operational gap: `workflow_dispatch` alone is unavailable
while the workflow exists only outside default `main`. The existing core
release infrastructure is unchanged. Cloud function packaging remains a real
preview gate, not a claim established by local tests.

## Review and protected-build state

Both consumer `main` and the integration branch now enforce the already-required
policy: one approving review, stale approval dismissal, last-push approval,
strict current-head `astronomy-and-web` from GitHub Actions app 15368, resolved
conversations, administrator enforcement, no force pushes or branch deletion.
Only `olsonan26` is a collaborator; no independent approval exists. No manual
exception was explicitly granted by the completion prompt. Self-review and the
core's Phase 7 bootstrap exception cannot be used to merge this PR.

Created `nadia-private-build` with required owner environment review and
`prevent_self_review=true`, restricted to the integration branch. Owner review
of an environment is not independent approval of the owner's PR. The enable
variable is explicitly **false**, the consumer ref names the integration branch,
and no private reader secret is configured. An owner-initiated run cannot be
self-approved. Hosted private preflight has not passed or been counted as a
skipped successful check. No broad local GitHub token was copied into CI/Vercel.

Minimum remaining external actions: authorize an actual independent reviewer;
configure a GitHub App/fine-grained core-only Contents:read credential in the
protected build environment and approved Vercel preview configuration; configure
the dedicated health token; clear applicable production licenses. After review,
merge into integration, enable/run protected private preflight, validate actual
Vercel preview packaging/authentication, then consider production under separate
promotion gates. No credentials need to be pasted into this chat.

## Branch consolidation assessment

Remote integration is 54 commits ahead of `main`, with no commits unique to
`main`; PR #6 is kept narrow against that integration branch. Preserve the 18
additional local application commits separately; they are not part of PR #6.
After this integration, open a separate integration-to-main promotion PR. Review
its complete application/source/license diff, reconcile later deployed local
repairs, run the full suite and protected preflight on the proposed merge, test
the exact production candidate on preview, and obtain review before main merge.
Retain existing refs and rollback deployment `dpl_HANKwJ2ddujE6iKZYL216GjDjWeh`.
Do not fast-forward production or silently include local history as part of this
consumer adapter change. Long-term, use reviewed main as the single delivery
branch and archive the old integration branch after consumers are verified.

The private core remains v0.7.0; no source authority changed. Spark/FCA,
body/angle boundaries, shadow overlap/progression applicability, full contextual
composition and complete personal readings remain unresolved. The private author
clarification draft is prepared and unsent. Legacy application interpretation
remains explicitly separate and is never a fallback for unavailable core rules.
