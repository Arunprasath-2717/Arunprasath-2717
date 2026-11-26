# Profile source

The profile is a single custom SVG illustration and a short README. The illustration uses solid warm colors, system fonts, a reduced-motion fallback, and no external image services.

## Repository layout

- `README.md` — profile composition and selected projects.
- `assets/workshop.svg` — published artwork.
- `scripts/build_profile.py` — standard-library renderer and GitHub GraphQL client.
- `scripts/test_build_profile.py` — automated tests.
- `.github/workflows/profile-telemetry.yml` — validation and six-hour refresh.

Run `python3 -m unittest discover -s scripts -p 'test_*.py'` from the repository root. To regenerate from the published SVG without credentials, use `python3 scripts/build_profile.py --existing`. For fresh data, run `python3 scripts/build_profile.py --live` with `GH_TOKEN` supplied through the environment. Never commit credentials. If the API fails, the workflow fails without replacing the last good image.

The contribution tape is chronological. Bar heights use a square-root scale relative to the busiest week; colors identify inactive, active and peak weeks. The animated conduit is symbolic, not actual service telemetry.
