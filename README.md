# Mystic Rebels Chart Generator

Independent Mystic Rebels web application with a native Swiss Ephemeris calculation API, precise SVG natal/Dual wheels, grouped object selection, a full-precision position model, and Supabase account/saved-chart integration.

Private repository: https://github.com/olsonan26/mystic-rebels-chart-generator

## Run the installed application on this Windows machine

```powershell
cd 'C:\Users\olson\OneDrive\Documents\Reverse Skill\work\Mystic-Rebels'
npm ci
npm run build
.\.runtime\python.exe scripts\run.py
```

Open http://127.0.0.1:8000. `Load example` loads the documented illustrative Los Alamitos chart. This is labelled Example chart; its coordinates are editable and are not represented as a certified individual birthplace.

For frontend development run `npm run dev` in a second terminal. Vite proxies `/api` to the same Python API on port 8000.

## Fresh installation

Linux/macOS or a normal Python 3.12 installation:

```sh
python -m venv .venv
# Activate .venv using the command appropriate to your shell.
python -m pip install -r requirements-qa.txt
npm ci
python scripts/provision_ephemeris.py
npm run build
python scripts/run.py
```

On Windows, the upstream pinned binding supplies CPython 3.11 wheels. `scripts/bootstrap_runtime.py` installs an isolated official CPython 3.11.9 embedded runtime. Install dependencies into it with a recent system pip: `python -m pip --python .runtime/python.exe install -r requirements-qa.txt`. The Windows runtime is used only for development; Vercel is explicitly configured for Python 3.12. Never install the binding into a different existing application environment.

Pinned official ephemeris files and the compact offline place index are included in the private repository. The executable provisioner verifies SHA256 and downloads missing files from recorded official/vendor-published URLs. `data/ephemeris-manifest.json` records origins, exact sizes, retrieval times, and hashes. `scripts/provision_locations.py` regenerates the compact location dataset from the pinned development dependency.

## Verify

```powershell
.\.runtime\python.exe -m pytest astronomy_qa -q
npm test
npm run build
.\.runtime\python.exe scripts\validate_horizons.py
```

The last command performs live NASA queries and stores raw responses. Ordinary tests use the saved independent reference data without network access. Historical research checks remain unchanged in the private input package; their 87 checks are separately recorded in `evidence/research-87.xml` and are not counted as new astronomical validation.

## Hosting

The Vite frontend and `/api/index.py` ASGI calculator deploy together on Vercel. GitHub is linked to the Vercel project. `vercel.json`, `.python-version`, and `pyproject.toml` configure the native Python function and data inclusion. The compact GeoNames index avoids shipping the much larger development database package in the function.

Set `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY` in each intended Vercel environment. Only the publishable key is exposed by `/api/config`. No service-role key is required by the client or calculation API. Local values go in ignored `.env`; see `.env.example`.

Apply `supabase/migrations/20261024100237_mystic_rebels_charts.sql` to the intended project using an authenticated project administrator. The table uses ownership checks and RLS for all read/write operations. Until schema application and live verification are completed, cloud saving is not a verified completed capability.

Keep deployments authenticated until numerical acceptance and the Swiss Ephemeris release license are resolved. The official vendor requires choosing its AGPL-compatible or professional licensing route before distribution/public service activation. This private development repository does not imply a purchased professional license. See `docs/PRECISION.md` for actual measured numerical agreement and release limitations.

## Input data and privacy

The calculator does not persist birth data. Chart responses are `no-store`. Saving a chart is an explicit signed-in action. The source PDF and historical reference directory are excluded from Git and deployment. Geographical search uses GeoNames city centroids in WGS84, with attribution to https://www.geonames.org/ under CC BY 4.0. Users can enter more precise coordinates; a city centroid is not an exact individual birth location.
