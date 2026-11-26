# Profile artwork and data

The README uses a fixed-camera cinematic hero, an integrated skills scene, three selected projects, a visualization of CANE's checked-in predictions, and an authentic GitHub contribution snake.

- `scripts/ruins_hero.py`: cinematic artwork source; the hero is checked in.
- `scripts/fieldwork.py`: skills scene and CANE prediction distribution.
- `scripts/cinema.py`: contribution totals.
- `scripts/build_profile.py`: reproducible asset generation and GitHub data retrieval.
- `data/cane-routing.json`: aggregate action counts from CANE's published output; not an accuracy metric.
- `data/contributions.json`: weekly GitHub contribution counts.

Run `python3 scripts/build_profile.py` to regenerate the four generated SVGs.
Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to validate the assets.
The scheduled workflow refreshes contribution data and the Platane/snk animation every six hours. GitHub API failures preserve the published snapshot.
The project descriptions link to the original work; no simulated production screenshots are included.
