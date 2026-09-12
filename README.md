# RuneBox // Subwoofer Enclosure Lab

<p align="center">
  <strong>High-Precision Acoustic CAD & Electrical Synthesis Suite for Custom Trunk Fabricators, Audio Engineers, and SPL Competitors.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.0.0-00E5FF?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-blueviolet?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/3D%20Engine-Pure%20Python%20Canvas-00C853?style=for-the-badge" alt="Pure Python 3D">
  <img src="https://img.shields.io/badge/Platform-Windows%20Standalone%20EXE-0078D6?style=for-the-badge&logo=windows" alt="Platform">
</p>

---

## ⚡ Overview & Architectural Vision

**RuneBox** is an all-in-one acoustic engineering workstation engineered by **NfgOdin** (System Architect & Audio DSP / Subwoofer Box Specialist). It bridges the gap between raw Thiele/Small electrical modeling, 3D CAD trunk spatial packaging, fluid aerodynamic port tuning, and workshop fabrication cut sheets.

Designed with **zero heavy external 3D runtime dependencies** (no OpenGL DLL issues or bulky game engines), RuneBox utilizes a dedicated mathematical matrix projection pipeline that renders real-time 3D vector models, 2D front-baffle blueprints, and electrical wiring schematics natively on standard Tkinter canvases.

---

## 🎛️ Core Feature Suites

### 1. 🎴 Responsive Dashboard & Workflow Navigation (`dashboard.py`)
- **Dynamic Adaptive Grid**: Home dashboard automatically adapts its layout dynamically (1 to 6+ modules) with high-tech glowing cards and dark-mode aesthetics.
- **5-Step Guided Enclosure Studio Flow (`gui.py`)**:
  1. `Woofer & T/S Specs`: Load presets or enter custom electromechanical parameters.
  2. `Enclosure Alignment`: Calculate EBP, target Net $V_b$, tuning frequency, and chamber boundaries.
  3. `Dimensions & 3D Shape`: Configure physical dimensions, wedge angles, baffle thicknesses, and driver counts.
  4. `Port Dynamics`: Tune slot or aeroports with real-time velocity and air chuffing meters.
  5. `Fabrication Cut Sheet`: Generate exact wood cut lists with fraction readouts and export options.
- **Top Bar & Dynamic Routing**: Global navigation bar with persistent `🏠 Home`, contextual `⬅ Back`, and live breadcrumbs.
- **Executive Business Card About Modal**: Direct access to system specifications, creator credits, and GitHub repository integration.

---

### 2. 📐 Pure Python 3D Vector & 2D CAD Blueprint Engine (`visualizer_3d.py`, `geometry.py`)
- **Real-Time Interactive 3D Orbiting**:
  - Full mouse yaw/pitch rotation and scroll-wheel zoom.
  - Multi-panel depth-sorted polygon rendering.
- **4 Visual Display Modes**:
  - **Wireframe**: Transparent geometric wireframe for interior alignment checks.
  - **Solid**: Shaded solid panels for realistic aesthetic appraisal.
  - **X-Ray**: Semi-transparent panels revealing internal slot ports, dividers, and woofer baskets.
  - **Exploded View**: Dynamic assembly breakdown demonstrating how panels join.
- **2D CAD Front Baffle Blueprint**:
  - Accurate cut-hole diameters, flange outer rings, and pitch circle diameter (PCD).
  - Real-time woofer collision detection and minimum edge clearance checks.
  - Front-baffle dimension arrows and extension callout lines.

---

### 3. 🔊 Acoustic Suspensions & Aerodynamic Port Dynamics (`acoustic_math.py`)
- **Sealed Box Alignment (True Acoustic Suspension)**:
  - Automatically locks port displacement to strictly `0.0 cu.ft` / `0.0 L`.
  - Centers drivers across the full internal width without wasting baffle real estate.
  - Omits port divider walls and corner deflectors from fabrication cut lists.
- **Vented & Bass Reflex (Keele / Small Alignment)**:
  - Computes optimal net box volume ($V_b$) and resonance tuning ($F_b$).
  - Supports flared aeroports, round PVC, and rectangular MDF slot ports with L-turn bends.
- **Port Aerodynamics & Chuffing Guard**:
  - Peak port air velocity calculation ($V_o$).
  - Built-in chuffing guard alerts: green (<17 m/s laminar flow) and visual warning flags (>25 m/s turbulence).
  - Recommended vent area ratio: 12 to 16 sq.in per net cubic foot.
- **4th & 6th-Order Bandpass & Isobaric Modeling**:
  - Dual-chamber sealed/vented modeling with cutoff points and isobaric compound halving.

---

### 4. ⚡ Multi-Subwoofer Visual Wiring & Exact Electrical Lab (`wiring_math.py`)
- **Comprehensive Multi-Woofer Architectures**:
  - Supports 1, 2, 3, or 4 subwoofers.
  - Single Voice Coil (SVC) and Dual Voice Coil (DVC) configurations.
  - Independent per-subwoofer coil impedance (1Ω, 2Ω, 4Ω).
- **Exact Kirchhoff / Ohm's Law Power Engine**:
  - Calculates true per-woofer wattage dissipation using $P = I^2 R = V^2 / R$ rather than assuming equal division on imbalanced or hybrid series-parallel loads.
- **CAD Schematic Visualizer**:
  - Multi-lane collision-free wiring channels for amplifier positive, negative, and inter-coil series jumpers.
  - Real-time impedance matching and amplifier load safety analysis.

---

### 5. 🪚 Fabrication & Workshop Cut Sheets
- **Dual Measurement Readouts**:
  - Precise decimal tape measurements and nearest 1/16" fractional readouts.
- **Full Structural Breakdown**:
  - Top, Bottom, Front Baffle, Rear, Left/Right sides, Port Walls, L-port extensions, and bevel angles.
- **Workshop Export**:
  - One-click export to formatted `.csv`, clean `.txt` workshop summaries, or printable shop order layout.

---

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.14+ (or 3.11+)
- Windows 10/11 recommended

### 1. Clone the Repository
```powershell
git clone https://github.com/odinj2010/RuneBox.git
cd RuneBox
```

### 2. Setup Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Requirements
```powershell
pip install -r requirements.txt
```

### 4. Run Application
```powershell
python main.py
```

---

## 📦 Standalone Binary Compilation (`RuneBox.exe`)

To compile the entire suite into a single, zero-dependency Windows executable:

```powershell
.\build.bat
```

Or invoke PyInstaller directly:
```powershell
.venv\Scripts\pyinstaller --noconfirm RuneBox.spec
```

The output binary will be located at:
```text
dist\RuneBox.exe
```

---

## 👨‍💻 Creator & Architectural Credits

- **Architect & Lead Developer:** **NfgOdin**
- **Domain Focus:** Audio DSP, Subwoofer Acoustic Enclosure Engineering, and SPL Car Audio Systems.
- **Repository:** [https://github.com/odinj2010/RuneBox](https://github.com/odinj2010/RuneBox)
