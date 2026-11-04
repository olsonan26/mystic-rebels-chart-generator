# Private NADIA integration

Status: implemented and locally verified; deployment remains BLOCKED.

The consumer repository is public. Only the adapter, tests and release identity
are published here. The core wheel, installed rules and credentials must remain
outside Git and browser artifacts.

## Immutable dependency

- Version: `0.7.0`
- Core commit: `5a472f5f8236aa53ae90529a91a6ad20dd9e1382`
- Wheel: `nadia_knowledge_core-0.7.0-py3-none-any.whl`
- SHA256: `352bb1251ef471e9535ae514ba4ea692411ee91ab0a14d18f269002818b1612b`

An approved protected build must acquire this asset from the private core release
using a GitHub App installation token or fine-grained token restricted to
Contents:read on that repository. Do not put a token in a dependency URL, Git,
VITE-prefixed variables, command arguments, logs or public Actions artifacts.
No such protected consumer credential is currently configured.

With the private wheel available locally, run with Python 3.12:

```text
python scripts/install_nadia.py /private/path/nadia_knowledge_core-0.7.0-py3-none-any.whl
python scripts/verify_nadia_private.py
python -m pytest astronomy_qa access_qa -q
npm ci
npm test
npm run build
python scripts/check_nadia_boundary.py
```

The installer verifies the wheel before installation and installs offline with
no dependencies. `.nadia-private/` is an ignored server runtime. Its wheel and
installed files are checked again before core initialization. Installation over
an existing runtime is rejected; stage upgrades and rollback in fresh checkouts.
Do not upload the runtime as a public CI artifact. Vercel function inclusion is
configured, but function packaging has not been verified on Vercel.

`GET /api/nadia/health` requires a dedicated `Authorization: Bearer ...` token
from server environment `NADIA_HEALTH_TOKEN` (at least 32 characters). It rejects
anonymous, incorrect and unconfigured credentials with 401. This machine route
uses its own authentication instead of the site's browser password cookie.
Authenticated integrity/import failures return generic 503 with no-store.
It returns release identity and capability metadata only. It does not assert
that the separate astronomical engine has passed a live readiness check.

`nadia_backend.structured_evidence` is an internal server function delegating
composition and validation to the private library. It retains question/owner
binding, source references and explicit incomplete-reading flags internally.
No HTTP evidence/retrieval route or unrestricted reading generator is provided.
Existing application interpretation is separate from this core capability.

## Required release gates

Public CI runs the existing application suite and browser/Git boundary scan.
It receives no private wheel or credential. Its success alone does not establish
private integration readiness: `verify_nadia_private.py` is a separate mandatory
protected-build preflight, which fails if the wheel is unavailable. Neither a
missing private preflight nor a skipped numerical test counts as passing.

`nadia-private-preflight.yml` implements that separate workflow-dispatch
contract using the existing core delivery input names. It rejects a different
version/commit/digest, an unset enable flag, an unset approved branch or a wrong
dispatch branch. It acquires the wheel with `NADIA_CORE_READ_TOKEN`, verifies it,
runs the real private preflight and full regressions, rejects skips, builds the
web bundle and scans the boundary. It uploads no private artifact and performs
no deployment. It has not run while the required environment is unconfigured.

Before enabling it, configure environment `nadia-private-build` with an
independent required reviewer and prevent self-review; restrict allowed branches
to the confirmed integration branch. Set environment variables
`NADIA_PRIVATE_BUILD_ENABLED=true` and `NADIA_CONSUMER_REF` only after those
protections and exact-head consumer review are verified. Store a scoped
`NADIA_CORE_READ_TOKEN` there. Do not expose that credential to pull-request
workflows. These settings have not been enabled in this phase.

Before preview: independently review the exact head, configure a protected
scoped asset reader and health token, confirm Vercel account/project/team and
production branch through a fresh authenticated connection, and validate the
server package with the real Vercel build. Branch `codex/nadia-consumer-phase8`
has automatic Vercel deployment disabled. No deployment workflow is enabled.

After preview: verify anonymous 401, authorized 200, exact version/commit/hash,
blocked readings, no private static files, existing astronomical regressions
and license clearance. Promote only that verified build. Rollback means restoring
the previous verified consumer deployment; v0.7.0 is the immutable core pin.
No earlier deployed NADIA consumer integration has yet been verified.

## Review and destination blockers

The candidate integration branch is
`codex/phsr-numerology-integration-20261028` at
`6adf7ae270ebe02b7aa5fa8cde556403270c0bd5`; this is not proof of Vercel's production
branch. GitHub's default is `main`, an older application baseline. The Phase 8
patch excludes 18 unrelated local commits and all unrelated working-tree edits.
Do not merge those application histories or change production routing merely
to complete this integration.

Only the owner is currently a repository collaborator. No independent approval
is recorded. The manual route is to add an authorized reviewer, obtain exact-head
review and all applicable checks, confirm the target branch, then merge under
the owner's standing release instruction. Do not self-approve or reuse the
core's Phase 7 bootstrap exception. The core stays at v0.7.0; no new knowledge
version is justified by consumer-only changes.

Vercel access is not freshly authenticated. The previously rejected credential
was not retried. Candidate local project/team identifiers remain unverified.
No preview or production URL, deployment identity or live health result exists
for this integration. Proprietary-rule and ephemeris production licensing also
requires explicit clearance; successful calculation is not license clearance.
