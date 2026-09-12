# RuneBox // Subwoofer Enclosure Lab — Agent Operating Rules

Welcome to the **RuneBox** codebase. As an Antigravity coding agent working in this repository, you **MUST** strictly adhere to the following architectural, mathematical, and coding guidelines on every turn.

---

## 1. Project Overview & Creator Identity
- **Application Name**: RuneBox // Subwoofer Enclosure Lab
- **Creator / Architect**: **NfgOdin** (System Architect & Audio DSP / Subwoofer Box Specialist)
- **Tech Stack**: Python 3.14+, `customtkinter`, `tkinter`, pure Python Canvas 3D vector engine, `PyInstaller`.
- **Packaging Target**: Standalone Windows binary (`dist\RuneBox.exe`) built via `RuneBox.spec`.

---

## 2. Core Architectural Principles
1. **Zero Unnecessary Dependencies**:
   - Do **NOT** introduce heavy 3D game engines, OpenGL wrappers, or external visualization packages (e.g. `matplotlib`, `pygame`, `pyglet`, `moderngl`, `vpython`) that cause packaging issues or Windows DLL incompatibilities.
   - All 2D and 3D graphics (blueprints, wiring schematics, 3D rotating box models) MUST use pure Python matrix projection, geometry math, and standard Tkinter/CustomTkinter Canvas objects.
2. **Dashboard Card Navigation**:
   - The application root uses a card-based home dashboard (`dashboard.py`).
   - The top header provides persistent `🏠 Home` and `⬅ Back` buttons and dynamic breadcrumb routing.
   - When introducing new studio sections or tools, add them as responsive `DashboardCard` entries on the home grid.
3. **Step-by-Step Guided Workflows**:
   - Inside the **Enclosure Studio (Box Builder)**, stages follow the 5-step sequence:
     1. `Woofer & T/S Specs`
     2. `Enclosure Alignment`
     3. `Dimensions & 3D Shape`
     4. `Port Dynamics`
     5. `Fabrication Cut Sheet`
   - Maintain the bottom `⬅ Previous Step` and `Next Step ➡` navigation buttons alongside the step tabs.

---

## 3. Acoustic, Physical & Electrical Math Invariants
1. **Acoustic Suspensions (Sealed Boxes)**:
   - When topology is `sealed`, `port_type` must be `"none"`.
   - Port displacement is strictly `0.0 cu.ft` / `0.0 L`.
   - Never draw slot ports or aeroports on the 2D baffle or 3D visualizer when sealed.
   - The baffle span calculation must center drivers across the full internal box width without reserving space for a non-existent port.
   - Cut sheet panel list must never include port walls, L-port extensions, or 45° corner deflectors when sealed.
2. **Port Aerodynamics & Chuffing Guard**:
   - Keep air velocity below 17 m/s for clean laminar flow; warn when velocity exceeds 25 m/s.
   - Recommended port vent area ratio: `12.0` to `16.0` sq.in per cubic foot of Net Vb.
3. **Multi-Subwoofer Wiring & Power Calculations**:
   - Support independent coil counts (Single/Dual) and per-coil impedance for each speaker.
   - In hybrid series-parallel or imbalanced loads, compute exact individual driver wattages using Ohm's & Kirchhoff's laws ($P = I^2 R = V^2 / R$) rather than assuming equal division.
   - Ensure wiring schematic wire lines (positive, negative, series jumpers) maintain dedicated routing lanes and zero wire-on-wire collisions.

---

## 4. Operational & Workflow Directives
1. **Mandatory Implementation Plan**:
   - You **MUST** provide a detailed implementation plan artifact (`implementation_plan.md`) and wait for the user's explicit approval **BEFORE** making any changes, edits, or running modifying commands on any code or project files.
   - Never skip the implementation plan phase.
2. **Strict GitHub & Git Policy**:
   - **NEVER** perform any Git or GitHub actions (commit, push, pull, remote modification, branch creation/checkout) unless the user explicitly and specifically tells you to do so in that exact prompt.
   - Do **NOT** ask, prompt, or suggest doing anything with GitHub or pushing commits. Maintain absolute silence on Git/GitHub actions unless ordered.
3. **Release & Changelog Tracking (`RELEASE_vX.X.X.md`)**:
   - All current ongoing additions, refactors, and feature changes must be logged and maintained in `RELEASE_vX.X.X.md`.
   - When the user explicitly states that a release is being made, review all accumulated features/fixes to determine the appropriate semantic version tag (e.g. initial release is `v1.0.0`, subsequent releases `v1.0.1`, `v1.1.0`, etc.).
   - Rename `RELEASE_vX.X.X.md` to `RELEASE_v<version>.md` (e.g. `RELEASE_v1.0.0.md`).
   - Immediately create a fresh blank `RELEASE_vX.X.X.md` to begin tracking subsequent changes for the next version.

---

## 5. Coding & Modification Standards
1. **Preserve Code Integrity**:
   - Preserve existing comments, docstrings, variable naming, and styling.
   - Avoid destructive full-file rewrites when surgical edits suffice.
2. **Verification Protocol**:
   - After modifying GUI, math, or geometry logic, always verify with a headless Python test script (e.g. instantiating `gui.RuneBoxApp()` or running unit tests in `.venv\Scripts\python.exe`).
   - After code changes are verified, recompile the standalone binary using:
     ```powershell
     .venv\Scripts\pyinstaller --noconfirm RuneBox.spec
     ```
   - If `PermissionError: [WinError 5]` occurs during compilation, check for running `RuneBox.exe` processes and terminate them before building.
3. **Units & Precision**:
   - Always support both **Imperial** (inches, cu.ft, lbs) and **Metric** (cm, mm, Liters, kg).
   - Cut lists must support both decimal tape measurements and nearest 1/16" fractional readouts.
