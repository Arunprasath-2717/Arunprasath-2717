# AP/2717 — Spectrum

The profile uses original animated SVG artwork, clickable project and contact cards, six engineering skill domains and real GitHub activity.

- scripts/spectrum.py: original folded spectrum, project demonstrations, skill index and links.
- scripts/build_profile.py: standard-library generation and GitHub GraphQL retrieval.
- scripts/cinema.py: contribution summary in light and dark.
- data/contributions.json: actual weekly counts.
- data/cane-routing.json: aggregate checked-in CANE decisions, not accuracy.
- .github/workflows/profile-telemetry.yml: six-hour refresh, validation and pinned Platane/snk generation.

Run `python3 scripts/build_profile.py` to regenerate the fourteen SVGs.
Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to test.
The hero's lower chart uses actual weekly counts. Project examples are illustrative, not live traffic. No runtime JS or external artwork. Reduced-motion CSS is included.
