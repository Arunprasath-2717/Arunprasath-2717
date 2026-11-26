# AP/2717 profile source

- `README.md` — public profile, with accessible text and theme-aware artwork.
- `data/profile.json` — curated identity and project summaries.
- `data/contributions.json` — dated weekly contribution counts from GitHub.
- `scripts/build_profile.py` — dependency-free Python SVG renderer and GraphQL client.
- `scripts/test_build_profile.py` — XML, data, failure-handling and README-reference tests.
- `assets/` — five original SVG modules in dark and light palettes.
- `.github/workflows/profile-telemetry.yml` — read-only validation and scoped write refresh every six hours.

Run `python3 scripts/build_profile.py` to reproduce artwork from checked-in data.
Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to validate it.
For fresh contribution data, run `python3 scripts/build_profile.py --live` with
`GH_TOKEN` supplied through the environment. Never commit credentials.
API failure leaves the published snapshot untouched. Weekly bars are linear and
annotated with actual counts. Animations describe system flow, not service status.
