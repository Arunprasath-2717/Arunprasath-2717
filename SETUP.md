# Beyond the Clouds: living field guide

The two landscape SVGs combine generated raster environment artwork with native, locally masked SVG motion. This is a fixed-camera visual effect, not a physically simulated 3D scene or live video. Water texture is restricted to the depicted cascades. The animated engineering examples are conceptual; the contribution count and snake are actual GitHub data.

## Rebuild

- `python3 scripts/build_profile.py` rebuilds the 14 theme-specific technical and contribution assets from the saved data.
- `python3 -m unittest discover -s scripts -p 'test_*.py'` validates the asset layout, data, source integrity and motion.
- `python3 scripts/ruins_hero.py` rebuilds the two cinematic scenes from the WebP source plates (optional Pillow dependency).
- `.github/workflows/profile-telemetry.yml` refreshes contribution data and generates the green contribution snake every six hours. It uses pinned actions and scopes write permissions to the refresh job.

See [DESIGN.md](DESIGN.md) for the art direction and anti-slop audit. Every SVG is self-contained; no JavaScript or external assets are required at render time. The landscape picture elements select static alternatives when reduced motion is requested; the SVGs also include reduced-motion CSS.
