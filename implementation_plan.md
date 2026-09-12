# Implementation Plan: Rules Expansion (Implementation Plans, GitHub Strictness, Release Tracking) & Initial GitHub Push

## Overview
1. Update `AGENTS.md` and `.agents/AGENTS.md` to establish strict operational rules:
   - **Mandatory Implementation Plan Rule**: An implementation plan must ALWAYS be presented and explicitly approved by the user BEFORE any code or file modifications are performed.
   - **Strict GitHub Rule**: NEVER interact with Git/GitHub (commits, pushes, pull requests, remotes, branches) unless explicitly commanded by the user in that prompt. NEVER suggest or ask to do so.
   - **Release & Changelog Tracking Rule**: All ongoing development changes must be recorded in `RELEASE_vX.X.X.md`. When the user explicitly calls for a release, assess additions, determine the semver tag (e.g. `v1.0.0`), rename `RELEASE_vX.X.X.md` to `RELEASE_v1.0.0.md`, and generate a fresh blank `RELEASE_vX.X.X.md` for subsequent work.
2. Initialize and configure the repository for initial GitHub push to `https://github.com/odinj2010/RuneBox`:
   - Create a clean `.gitignore` to exclude build artifacts (`dist/`, `build/`, `__pycache__/`, `.venv/`).
   - Initialize `RELEASE_vX.X.X.md` documenting current additions.
   - Connect remote `origin` to `https://github.com/odinj2010/RuneBox.git` and push the initial commit.

---

## User Review Required

> [!IMPORTANT]
> **Pushing to Remote Repository**:
> - Remote destination: `https://github.com/odinj2010/RuneBox.git`
> - Branch: `main` (standard default branch)
> - Excluded via `.gitignore`: `.venv/`, `build/`, `dist/`, `__pycache__/`

---

## Proposed Changes

### 1. Update Rules (`AGENTS.md` and `.agents/AGENTS.md`)
Add the following mandatory rule sections:
- **Mandatory Implementation Plan**: Always provide an implementation plan artifact and halt execution until the user gives explicit acceptance before touching any code.
- **GitHub Policy**: Absolute silence and inaction on GitHub unless explicitly instructed in that prompt. Never propose or ask.
- **Changelog & Release Lifecycle**:
  - Unreleased changes are actively tracked in `RELEASE_vX.X.X.md`.
  - When a release is commanded, determine appropriate version (`v1.0.0` for initial), rename to `RELEASE_v<version>.md`, and spawn a fresh blank `RELEASE_vX.X.X.md`.

### 2. Changelog & Git Setup
#### [NEW] [RELEASE_vX.X.X.md](file:///c:/Users/jonat/Documents/Antigravity%20Projects/RuneBox%20%28Subwoofer%20Enclosure%29/RELEASE_vX.X.X.md)
Document all features built up to this point (Dashboard card navigation, Box Builder 5-step studio, 2D/3D visualizer, visual wiring & exact wattage distribution, sealed acoustic suspension support, shop order views, global settings, About modal).

#### [NEW] [.gitignore](file:///c:/Users/jonat/Documents/Antigravity%20Projects/RuneBox%20%28Subwoofer%20Enclosure%29/.gitignore)
Ignore Python bytecode, virtual environments, PyInstaller output (`dist/`, `build/`).

### 3. GitHub Initial Push
Execute:
- Add remote `origin https://github.com/odinj2010/RuneBox.git`.
- Stage files, commit initial version, and push to GitHub.

---

## Verification Plan
1. Inspect `.agents/AGENTS.md` and `AGENTS.md` to confirm rule wording.
2. Confirm `RELEASE_vX.X.X.md` is initialized.
3. Verify git remote and git push status.
