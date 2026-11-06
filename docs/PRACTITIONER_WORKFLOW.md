# Local practitioner-assisted profiles

This adds an authenticated individual-review workflow to the existing chart and
report product. It does not implement autonomous personal interpretation, modify
the private Knowledge Core, or grant a new source-rule approval.

## Implementation map

| Capability | Current classification | Owning implementation |
|---|---|---|
| Existing chart positions, sufficiently precise houses, uncertainty and source-qualified geometry | Implemented and verified within existing numerical/source scopes | Existing astronomy/service and profile report modules |
| Private v0.7.0 integrity checks and source-function components | Implemented and verified within component scope | Unchanged `nadia_runtime.py` and private release |
| Field/Tone/Pulse, rulership, Delegate and represented-occupant topology | Implemented; semantic use remains partial | Existing report, context graph and composition |
| Finite function/Field and represented-Field theme returns | Partial; personal articulation requires review | Existing `scripts/personal_review.py`, `scripts/semantic_return.py` |
| Complete contextual synthesis, Spark and unresolved authority | Missing or blocked | Existing source gates remain unchanged |
| Local sign-in, saved cases, evidence preparation, editor and individual decisions | Implemented; lifecycle/security regression-tested | `mystic_rebels/practitioner.py`, `PractitionerWorkspace.tsx` |
| Reviewed-section assembly, original wheel and print/PDF export | Implemented; demonstrated in desktop/mobile local workflow | Existing `ReportContents` plus individually reviewed sections |
| Reader feedback and consented reference candidates | Implemented; independent semantic review remains required | Private case/history and benchmark candidate endpoints |
| Reader usefulness, expert certification and commercial deployment | Not established by software tests | Requires actual practitioner/reader review and separate launch validation |

## Start the existing application locally

Use the already installed astronomy runtime; no new dependency or model is needed.

```powershell
python scripts/setup_practitioner.py --actor "Your practitioner name"
npm run build
& ../Mystic-Rebels/.runtime/python.exe -B scripts/run_practitioner_local.py
```

Open `http://127.0.0.1:8011`. Generate a chart and profile, then choose
**Practitioner workspace**. Read the generated password from
`tmp/practitioner-private/sign-in.txt`. Never commit or share that file.
`--rotate` replaces the password and invalidates prior sessions. Existing case
records remain local. Changing the configured actor changes case ownership.

1. Sign in. Prepare the selected chart or reopen a saved case.
2. Choose a question. Inspect all calculated evidence, source components,
   relationship graph, scoped directional composition and unknown conditions.
   Available original images open through authenticated, hash-checked local routes.
3. Write Recognition, Explanation and Practical Application. Each item records
   evidence IDs, source references, applicability reasoning, limits and a rejected
   alternative. Identify expert judgment separately from source-supported claims.
4. Save the draft. Review each item and approve, request revision or reject.
   Approval requires explicit assertion/condition checks and supporting records.
   This records the practitioner's assessment; software does not prove prose
   entailment. Edited items lose approval. Stale revisions are rejected.
5. Assemble the report. Only complete, individually approved questions appear;
   unfinished questions remain incomplete. Download the report or print to PDF.
   The private evidence export keeps the detailed reasoning separate.
6. Optionally record voluntarily supplied feedback. Third-party observations stay
   distinct from the reader's assessment. Agreement is not source/predictive proof.
7. Secondary use is off by default. Record separate explicit subject authorization
   for a private benchmark candidate. It never becomes a gold standard through this
   interface, and demonstration content cannot enter that candidate library.

## Boundaries

- Technical verification, source authority, individual review and automated
  interpretation authorization remain distinct. All global approval flags stay
  false. A reviewer cannot promote a statement into a reusable source rule.
- Demonstration mode is on by default. Its cases and PDFs stay visibly labeled
  as examples, not expert readings. No actual practitioner qualification or
  reader endorsement is inferred from a successful demonstration.
- Evidence is server-calculated and saved as a protected snapshot. Edit endpoints
  accept claim IDs and evidence references, not replacement chart facts. Invalid
  references and unknown fields are rejected. Authored prose still needs a human
  fact/semantic check; this is not an automatic prose verifier.
- The local workspace has a dedicated password, hashed session tokens, HttpOnly
  same-site cookies, explicit origin/CSRF checks, login throttling, ownership,
  revision checks, no-store responses and noindex headers. Remote hosts and Vercel
  execution are rejected. The existing site-access protection is unchanged.
- Cases and append-only revision snapshots live in ignored local SQLite files.
  This is a single-account local application, not deployed multi-tenant storage.
  Files are not encrypted by the application: protect the OS account and backups.
  No automatic cloud backup, inference, analytics or source-image upload is used.
- Full-profile usefulness, licensing, professional review, deployment security,
  account recovery, retention and commercial launch remain separate work. This
  change does not claim a customer-ready launch or a complete autonomous reading.

## Source reference and demonstration evidence

The focused source-example inventory and typed strongest-example reconstruction
are local at `tmp/practitioner-reference/benchmarks.json`. The author conclusion
is the reference anchor; analyst reconstruction, expert judgment and unexplained
transitions are separately marked. This does not certify universal rules.

The real/synthetic demonstration artifacts are local at
`tmp/practitioner-demo/completed-flow/`: case records, report JSON, PDFs, screenshots,
videos and browser results. These contain private data and are not GitHub backups.
Only generic code/tests/docs belong in the public branch.

```powershell
# All public regression checks plus the actual local private-core integration:
& ../Mystic-Rebels/.runtime/python.exe -B -c "import sys;sys.path.insert(0,'.');import pytest;raise SystemExit(pytest.main(['astronomy_qa','access_qa','local_integration_qa','-q']))"
npm test
npm run build
```

`scripts/verify_practitioner.cjs` exercises the actual running UI using private
inputs supplied through `NADIA_REVIEW_DEMO_FILE`; installed Playwright/Chromium
paths can be set with the existing `NADIA_PLAYWRIGHT_MODULE` and
`NADIA_CHROMIUM_EXECUTABLE` variables. It refuses non-loopback destinations.
No private example content is embedded in the public test driver.

The next product priority is a qualified practitioner completing one real
question through this workflow, with the reader's voluntary response and an
independent source/semantic review. That supplies useful reference evidence
without pretending the missing automatic synthesis has already been solved.
