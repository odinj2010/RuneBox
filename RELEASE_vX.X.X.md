# RuneBox // Release Notes & Changelog (Unreleased / Next Release)

All upcoming and unreleased additions, modifications, and bugfixes are cataloged here. When a release is authorized, this file is finalized as `RELEASE_v<version>.md` and a fresh `RELEASE_vX.X.X.md` is initialized.

---

## [v1.0.0] — Initial Production Release

### Architecture & UI Framework
- **Card-Based Dashboard Hub (`dashboard.py`)**:
  - Implemented responsive, dynamic auto-adapting home card grid supporting 1 to 6+ studio modules.
  - Interactive hover glow styling with accent borders.
  - Persistent top navigation bar with dynamic breadcrumbs, `🏠 Home`, and contextual `⬅ Back` button.
- **5-Step Guided Enclosure Studio Flow (`gui.py`)**:
  - Linear 5-step guided workflow:
    1. *Woofer & T/S Specs*
    2. *Enclosure Alignment*
    3. *Dimensions & 3D Shape*
    4. *Port Dynamics*
    5. *Fabrication Cut Sheet*
  - Bottom persistent `⬅ Previous Step` and `Next Step ➡` navigation controls with boundary clamping and step tracking.
- **Global Settings & About Modal**:
  - Global units toggle (Imperial / Metric).
  - High-end dark executive business-card modal dialog featuring creator branding (**NfgOdin**), system specs, and direct GitHub repository link.

### Acoustic & Enclosure Engineering Engine
- **Sealed Box (Acoustic Suspension) Topology**:
  - True acoustic suspension calculations: automatically zeroes port displacement to strictly `0.0 cu.ft` / `0.0 L`.
  - Suppresses port rendering in 2D blueprints and 3D visualizers.
  - Optimizes woofer placement across full internal width.
  - Eliminates port walls and deflectors from fabrication cut sheets.
- **Port Aerodynamics & Vent Chuffing Guard**:
  - Laminar flow velocity checks with visual warnings when exceeding safety thresholds (25 m/s).
  - Port ratio safety index (recommended 12–16 sq.in per net cu.ft).
- **Driver Database & Custom Subwoofer Spec Builder**:
  - Integrated subwoofer driver presets (Sundown Audio, JL Audio, Skar Audio, Rockford Fosgate, Kicker).
  - Custom driver creation and dynamic persistence.

### Real-Time 3D & 2D Vector Visualizers
- **Zero-Dependency 3D Vector Engine (`visualizer_3d.py`)**:
  - Pure Python matrix projection and depth-sorted polygon rendering on standard Tkinter canvas.
  - Real-time mouse rotation (yaw/pitch) and scroll zoom.
  - Interactive render modes: Wireframe, Solid Shaded, X-Ray semi-transparent, and Exploded assembly view.
  - True physical representation of outer shells, slot/aero ports, internal dividing walls, and dual-ring woofer flanges.
- **2D CAD Blueprint Engine**:
  - Detailed front baffle cut-hole blueprint with CAD extension lines, dimension arrows, and flange pitch circle diameter (PCD).
  - Real-time woofer collision detection and wall clearance enforcement.

### Electrical & Multi-Subwoofer Wiring Lab (`wiring_math.py`)
- **Multi-Woofer Impedance & Power Engine**:
  - Supports 1, 2, 3, or 4 subwoofers with independent Single Voice Coil (SVC) or Dual Voice Coil (DVC) configurations.
  - Independent per-subwoofer coil impedance selections (1Ω, 2Ω, 4Ω).
  - Full Kirchhoff / Ohm's Law exact electrical power math ($P = I^2 R = V^2 / R$) for imbalanced or hybrid series-parallel circuits.
- **CAD Schematic Wiring Visualizer**:
  - Multi-lane collision-free wire routing for positive (+), negative (-), and inter-coil jumper paths.
  - Detailed terminal post indicators, polarity labeling, and per-subwoofer power dissipation readouts.

### Fabrication & Workshop Cut Sheets
- **Precision Panel Cutting List**:
  - Dual-mode dimension readouts: Decimal tape measurements and nearest 1/16" fractional markings.
  - Full part breakdown: Top, Bottom, Front Baffle, Back, Left/Right sides, Port Walls, and L-port extensions.
  - Export capabilities to CSV, TXT, and printable clean workshop format.
