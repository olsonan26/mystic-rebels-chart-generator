# Phase 8 owner actions — credentials and approvals only

Do not paste credentials into chat, Git, commands, dependency URLs or PR comments.
Enter them directly into the named platform's secret-value UI. Existing public
CI is separate from the protected private-wheel check.

## GitHub: approve the actual code

1. Authorize a real independent reviewer with Write access to this consumer
   repository. The only current collaborator is `olsonan26`, also PR #6's author.
   The author cannot satisfy the required approving review.
2. Have that reviewer inspect and approve PR #6's **current exact head**. Keep its
   base `codex/phsr-numerology-integration-20261028`. New pushes dismiss stale
   approvals; do not approve the obsolete `2f1d6a2` after workflow changes.
3. Settings > Environments > `nadia-private-build`: add the actual independent
   reviewer as an allowed environment reviewer as well. Retain required review,
   prevent-self-review, no admin bypass and the existing integration branch rule.
   Add the exact pull-request ref `refs/pull/6/merge` to allowed branch policies
   for the pre-merge run; do not allow every branch or arbitrary fork code.
4. Environment secret **`NADIA_CORE_READ_TOKEN`**: use an approved GitHub App
   installation token or fine-grained PAT restricted to
   `olsonan26/NADIA-KNOWLEDGE-CORE`, **Contents: read** (Metadata read is implicit).
   No write, administration, workflow or access to unrelated repositories is
   needed. App tokens must be refreshed/generated for the run; do not store an
   expired short-lived installation token as a permanent credential. Do not copy
   the broad local GitHub login credential into Actions.
5. Keep environment variable **`NADIA_CONSUMER_REF`** equal to
   `codex/phsr-numerology-integration-20261028`. After approvals and secret scope
   are verified, change **`NADIA_PRIVATE_BUILD_ENABLED`** from `false` to `true`.
6. Re-run the pending PR private-preflight job, or the complete PR workflow if it
   failed before configuration. An authorized reviewer other than the initiating
   actor approves the environment request. For PR runs the workflow independently
   checks GitHub's native `APPROVED` decision and unchanged head/base before
   checkout and private acquisition. A missing approval/credential is a failure,
   not a passing skipped check. Do not merge until this preflight and public CI
   pass for the exact proposed integration candidate.

The owner cannot approve an owner-initiated environment job under
prevent-self-review. The separate reviewer can do so after inspecting the run.
The post-merge push path remains available to verify the actual merge SHA.
Manual workflow dispatch is unavailable until its definition reaches default
`main`; the PR path avoids requiring a premature broader main promotion.

## Vercel: configure Preview only

Project: Astro / `mystic-rebels-chart-generator`, ID
`prj_MBgBhgCUjxUwJ8OZO9OrqDqK4Vwl`. Do not use the disconnected library project.
Production tracks `main`; do not change that setting or existing domains.

Project Settings > Environment Variables, target **Preview**, scoped to the
reviewed Phase 8 branch where branch-scoped variables are supported:

| Name | Configuration |
|---|---|
| `NADIA_CORE_READ_TOKEN` | Secret; approved core-only Contents:read credential |
| `NADIA_HEALTH_TOKEN` | Secret; dedicated cryptographically random credential, at least 32 characters |
| `NADIA_PRIVATE_BUILD_ENABLED` | Non-secret `true`, only after code and protected preflight approval |

Do not prefix these names with `VITE_` or `NEXT_PUBLIC_`. Keep
`NADIA_PRODUCTION_ENABLED` absent/false. Existing Preview site-password and
Supabase settings are already present; do not replace or disclose them.
The Vercel build hook validates the system project ID and explicit Preview
environment. No Vercel access token is needed for the existing authenticated
connector to manage deployments. These GitHub asset-reader and health secrets
are distinct from Vercel account authentication.

The Phase 8 Git branch disables automatic Vercel deployment. Once preflight and
review pass, use the authenticated connector to create an explicit Preview of
the exact approved integration commit in the existing project. The deployment
must report READY, then prove correct version/commit/digest, anonymous and wrong
token 401, authorized 200, private static-file isolation and blocked full
readings. Supply the health credential to the verification process through its
protected environment, never through chat, URL query parameters or shell text.

## Production: separate approval after verified Preview

Keep existing production deployment `dpl_HANKwJ2ddujE6iKZYL216GjDjWeh` as the
rollback reference. Its API metadata does not establish a Git SHA; do not claim
it already contains Phase 8. Production licensing must be explicitly cleared
for proprietary core distribution and applicable astronomical dependencies/
assets. Source-methodology approval is separate: full readings stay disabled.

After exact-merge Preview verification, prepare a separate integration-to-main
promotion PR covering the 54 historical integration commits and reconciliation
of later application repairs. Require its own review, CI and release assessment.
Only after those gates and licensing clearance may the approved production
credentials/flags be configured. Preserve domains, project identity and rollback.
No approval, merge or deployment receipt exists until the actual operation and
post-operation checks succeed.
