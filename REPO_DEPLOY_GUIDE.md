# Updating mnehan67/neurips-2026 (Windows + GitHub Pages)

This is a complete **repository-root snapshot**, not a ZIP you upload as a single GitHub file. Extract it first. Leave the existing `.git` directory inside your **cloned repository** intact; don't delete/re-create your GitHub repository.

## Easiest: GitHub Desktop

1. Install GitHub Desktop, sign into your GitHub account, and **File > Clone repository** > `mnehan67/neurips-2026`.
2. Download/extract the `NEURIPS_2026_GITHUB_WEBSITE_REPRO_READY.zip` archive. Open its `neurips-2026/` folder.
3. Copy **all contents** of that folder (including `.gitignore`, `.gitattributes`, and `.nojekyll`) into the cloned repo folder, accepting overwrite for changed files. **Do not copy over or delete `.git/`**.
4. In GitHub Desktop, review **Changes**. Expect updated website files, newly added stress-test data/scripts/notebook, improved documentation, and Figure 5. Do not upload the original outer archive or camera-ready PDFs.
5. Enter commit message `Update camera-ready website and reproducibility release`; click **Commit to main**, then **Push origin**.
6. Open `https://github.com/mnehan67/neurips-2026` and check `index.html`, `static/js/explorer.js`, and `reproducibility/results/crossed_stress_tests_v1/` exist.
7. Open repo **Settings > Pages**. Under **Build and deployment**, select **Deploy from a branch**, branch `main`, folder `/(root)`; **Save** if these are not already set.
8. Open `https://mnehan67.github.io/neurips-2026/`, hard-refresh with Ctrl+Shift+R, and test all three visualizer tabs, figures, paper/code links, and the MusIML-only BibTeX block. Check GitHub **Actions** for a failed Pages deployment if changes don't appear.

## Alternative: Git CLI (PowerShell)

```powershell
git clone https://github.com/mnehan67/neurips-2026.git
# Extract the prepared ZIP. Then copy the *contents* of its neurips-2026 folder into your cloned neurips-2026 folder.
cd neurips-2026
git status
git add -A
git diff --cached --stat
git commit -m "Update camera-ready website and reproducibility release"
git push origin main
```

You can always inspect changes before committing with `git diff --cached` (text) and `git status`. This package contains only the public website and reproducibility release, plus repository metadata and documentation.
