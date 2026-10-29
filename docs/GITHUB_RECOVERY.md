# GitHub preservation and recovery

Established at the user's explicit request on 28 October 2026. Knowledge, source decisions and completed work must survive conversation-memory, Supabase and Vercel failures.

## Destinations and authority

- **Application, knowledge records and audits:** [mystic-rebels-chart-generator](https://github.com/olsonan26/mystic-rebels-chart-generator), working branch `codex/phsr-numerology-integration-20261028`. This repository was verified **public** during this checkpoint. The default `main` branch predates later research and knowledge work.
- **Private media and recovery assets:** [mystic-rebels-recovery](https://github.com/olsonan26/mystic-rebels-recovery). This repository was created and verified **private** during this checkpoint. Its versioned releases hold the original media and recovery archive; checkpoint manifests identify the exact asset hashes and source revision.
- **Secrets:** retain credentials separately in the user's secret manager. Environment files, CLI authentication stores, private keys and session credentials are excluded from backups and must be re-provisioned during recovery.

Versioned files under `data/knowledge/`, `docs/`, `research/` and application source are the durable knowledge authority. Database records and deployment artifacts are separate consumers. Keep the original media and OCR/index provenance in the private recovery archive; the public portable knowledge export intentionally omits the raw book and scans.

## Every completed work session

1. Save findings, decisions, code, tests and a usable continuation record as files while working. Preserve exact source IDs, hashes, exceptions, conflicts and use limitations.
2. Review the diff and secret exposure. Stage the session's intended files explicitly. Preserve unrelated work in the private snapshot instead of blindly staging everything.
3. Run checks appropriate to the changes. After canonical knowledge changes, regenerate the portable export and run `scripts/export_report_knowledge.py --check`.
4. Commit and push the working branch. Compare its local SHA against `git ls-remote origin refs/heads/<branch>`. Report the actual commit and branch; a local commit does not establish a remote backup.
5. When private input files or external-data exports change, create a new recovery archive, upload it to a new private release, and verify remote asset digests or download/hash readback. Preserve older checkpoints.

This policy does not schedule an unattended backup or authorize a deployment. It is an explicit completion step for future authorized work. If a network/account problem prevents preservation, retain local files and report precisely which remote copy is missing.

## Source and working-file archive

`scripts/recovery_archive.py` uses only Python's standard library. It inventories the current bytes of Git-tracked files, including dirty working files, plus the private `reference/` tree, `evidence/private/` and original ignored instruction/reference documents. Additional project-relative inputs can be passed with `--input`. Commit intended new files before the snapshot or explicitly include them. Default inventories do not infer arbitrary untracked files.

The manifest records repository HEAD, branch, worktree status, every included relative path, exact file hashes, unique content blobs, chunk asset hashes and exclusions. Identical content is stored once. Archives are capped at 512 MiB and large files use segmented blobs. Credentials and dependency/runtime caches are omitted; credential-bearing container archives are excluded rather than silently rewritten. Exclusions remain visible in the manifest. This is a source/workspace archive, not an OS image or database dump.

Create a new checkpoint from the source repository:

```powershell
.\.runtime\python.exe -B scripts\recovery_archive.py create --output tmp\recovery-NEW-CHECKPOINT
.\.runtime\python.exe -B scripts\recovery_archive.py verify --archive tmp\recovery-NEW-CHECKPOINT
git bundle create tmp\recovery-NEW-CHECKPOINT\source-history.bundle --all
```

The code bundle preserves committed history and refs. The manifest/chunks preserve the current working bytes and private inputs. Hash the bundle separately in the checkpoint record. Keep archive output under ignored `tmp/`; never add multi-gigabyte inputs or authentication stores to the public Git tree.

Upload only after `gh repo view olsonan26/mystic-rebels-recovery --json isPrivate` confirms true. Use a new release tag, upload all chunks plus `manifest.json`, `source-history.bundle` and its checksum, and verify the release asset names, sizes and SHA256 digests. GitHub supports release assets under 2 GiB; these chunks deliberately stay below that ceiling. See [official release storage documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

## Restore without Supabase or Vercel

Download every asset from one private recovery release into a single directory. Obtain `scripts/recovery_archive.py` at the source commit recorded in its manifest. The script has no dependency on either cloud service and can run with ordinary Python 3.11 or later.

```powershell
python scripts\recovery_archive.py verify --archive 'C:\Recovery\downloaded-checkpoint'
python scripts\recovery_archive.py restore --archive 'C:\Recovery\downloaded-checkpoint' --destination 'C:\Recovery\restored-working-files'
git clone 'C:\Recovery\downloaded-checkpoint\source-history.bundle' 'C:\Recovery\restored-history'
```

The restore destination must not exist. Verification rejects tampered blobs/chunks and unsafe paths; restoration checks each reconstructed file. `restored-working-files` contains the current snapshot, including files that differed from committed HEAD. `restored-history` is a separate history checkout. Keep both until deliberate reconciliation; cloning the bundle alone does not recover previously dirty/private files.

Install the pinned dependencies and verify ephemeris/source hashes using the source README and audit tools. Re-provision secrets separately. A local source/index/question workflow should remain usable independently of hosted deployment and account storage, subject to its documented method limits.

## Live Supabase data: an explicit remaining gap

The app's saved-chart schema is versioned in `supabase/migrations/20261024100237_mystic_rebels_charts.sql`. Local configuration identifies project `jhxiwuiruwlwfapgjtcv`. The connected Supabase account did not list that project, and its direct public/storage table-inventory request returned **You do not have permission to perform this action** on 28 October 2026. No current saved-chart rows, Auth users, Storage objects or full database dump were acquired. A public/publishable API key cannot legitimately replace administrative export access.

Once the account owning that project is connected, inspect the actual schemas and export the appropriate roles, schema, data and migration history using the [official backup/restore procedure](https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore). Export Storage object bytes and service configuration separately where applicable; record exactly which Auth material is included. Keep exports in the private recovery repository/release and exclude secrets. Test a restore to an isolated database; a row JSON export is not a complete account/service recovery.

Until that export is verified, describe the checkpoint as **source and workspace recovery complete; live database export unavailable**, once the source upload itself has passed verification. Existing chart JSON export offers individual-file preservation, but no automatic all-customer backup is claimed.

## Consultation data going forward

When a question workflow is implemented, save each consultation as a versioned, exportable packet: question and reported context, birth-input uncertainty, chart fingerprint, exact as-of UTC and requested zone/interval, source/rule hashes, calculation results, answer and revision history. Preserve the original on refresh. Persist/export those packets independently of hosted tables and include changed private packets in the next recovery checkpoint. No question storage feature was added by the present audit.

## Verification for this checkpoint

The research review and new recovery tool are separate from application runtime changes. The source, PHDDASR and transit findings are indexed in [the deep audit](research-20261028/DEEP_AUDIT_AND_NEXT_STEPS.md). The private repository checkpoint record is the authority for actual upload, archive/file counts, bundle SHA, restore results and the external database limitation; do not infer upload success merely from this policy document.
