# AP/2717 — Night Shift

An original, self-contained SVG profile. The fictional night-shift lab is a visual narrative, not a photograph or live machine. Project motion represents conceptual processing; only the activity chart uses measured GitHub data.

- README.md — accessible profile composition
- assets/ — six SVG modules, two themes each; cinematic hero uses the same intentional dark film frame in both modes
- data/profile.json — project identity and source links
- data/contributions.json — dated weekly activity snapshot
- scripts/cinema.py — original SVG illustration and module generators
- scripts/build_profile.py — local renderer entrypoint and GraphQL retrieval
- scripts/test_build_profile.py — rendering, reference, motion and data validation
- .github/workflows/profile-telemetry.yml — six-hour refresh, PR validation, and manual dispatch

Run `python3 scripts/build_profile.py` to rebuild from the checked-in data.
Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to test.
For fresh contribution data, pass `--live` with GH_TOKEN in the environment.
API failure prevents publication and preserves the last good snapshot.
The artwork uses system fonts, no external assets, no JavaScript and reduced-motion CSS.
