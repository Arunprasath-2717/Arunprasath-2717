# Signal Foundry — AP/2717

The public profile is assembled from original, self-contained SVGs. No external artwork or runtime JavaScript.

- scripts/foundry.py — animated silicon substrate with one engraved channel per actual GitHub calendar week; skill index.
- scripts/fieldwork.py — project graphics, navigation and action tiles.
- scripts/cinema.py — contribution summary.
- scripts/build_profile.py — deterministic generation and GitHub GraphQL retrieval.
- data/contributions.json — dated weekly counts.
- data/cane-routing.json — aggregate checked-in CANE decisions, not accuracy.
- .github/workflows/profile-telemetry.yml — validation and six-hour refresh, including Platane/snk.

Run `python3 scripts/build_profile.py` to reproduce the fourteen generated SVGs.
Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to validate.
The hero engravings reflect weekly contribution counts; the animated highlights and project graphics are illustrations, not live infrastructure.
Reduced-motion CSS is included throughout. The original ruins artwork remains in Git history.
