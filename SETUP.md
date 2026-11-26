# AP / 2717 — installation and operation

This package is designed for `Arunprasath-2717/Arunprasath-2717`, branch `main`. It replaces README.md and adds only `assets/`, `scripts/` and `.github/workflows/profile-telemetry.yml`. It does not delete the old README from Git history or change other repositories. The initial render is a verified seven-repository sample (2026-11-26), not account-wide statistics.

## Install

1. Extract `ap2717-profile.zip`. Clone your profile repository with your existing GitHub credentials, then copy the extracted contents (including hidden `.github`) into the clone. Inspect `git diff` and `git status` before committing. Do not overwrite unrelated files if you have added any since this package was created.
2. Commit and push the files to `main` using your own GitHub credentials. GitHub may require workflow permission for a token used to push `.github/workflows/`.
3. Open repository **Actions** and select **AP 2717 / telemetry refresh**. If not already run automatically, enable workflows and click **Run workflow** on `main`. Repository settings must allow Actions and the workflow's requested `contents: write` permission; branch protection may prevent the bot from pushing.
4. Check the job log and your profile at https://github.com/Arunprasath-2717. The telemetry panel will change from “INITIAL VERIFIED SAMPLE” to “SCHEDULED PUBLIC DATA” after a successful repository API refresh. Contribution calendar is optional; if GitHub rejects GraphQL access, the card explicitly shows unavailable and still publishes actual repository metrics.

## Operation

- Runs at minute 17 of every sixth UTC hour, on manual dispatch, and on changes to the renderer/workflow. GitHub may delay scheduled jobs or disable inactive public-repository workflows. GitHub image caching can also delay visible changes. This is scheduled data, not a streaming dashboard.
- Uses the built-in GitHub Actions token (no PAT or third-party service needed for REST). It does not save the token. GraphQL contribution visibility and access are governed by GitHub; no attempt is made to access or expose private repository details.
- Repository metrics include publicly accessible owned non-fork repositories, excluding this profile repo. Language distribution uses the reported primary language per repository, not code bytes or skill percentages. Recent repository pushes are not necessarily authored commits. The contribution calendar reflects GitHub's reported contribution data and its visibility rules.
- REST errors fail the job before publication so the previous valid snapshot remains visible. GraphQL errors have a labeled fallback. Tests run before the generated assets are committed. Git pushes are non-force; if another push races the workflow, it fails safely.
- The AP/2717 identity includes an angular monogram and a decorative fingerprint derived from the GitHub username; it is not a cryptographic ownership claim. SVG CSS includes reduced-motion support and static fallbacks; GitHub client behavior may vary.

## Local preview and maintenance

```bash
python3 scripts/render_profile.py --snapshot scripts/initial_snapshot.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

To regenerate from GitHub, run `python3 scripts/render_profile.py --live` (authenticated through `GH_TOKEN` if configured; unauthenticated REST may work, but GraphQL needs authentication). Edit the source renderer rather than generated SVG files. All visual assets are local SVG; the only third-party links are intentional external destinations in the README. The previous project links and technical interests have been preserved, with project summaries checked against their own README files.
