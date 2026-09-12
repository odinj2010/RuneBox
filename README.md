# RuneBox // Subwoofer Enclosure Lab

**Creator:** NfgOdin  
**Target Output:** Standalone Windows Executable (`RuneBox.exe`)  
**Purpose:** Commercial-grade acoustic engineering and fabrication cut-sheet CAD suite for car audio builders, SPL competitors, and custom trunk fabricators.

---

## Key Features

1. **Thiele/Small Parameter Modeling & Alignment Synthesizer (`acoustic_math.py`)**
   - Direct entry or instant driver presets (Sundown SA/U-Series, JL Audio W7, Skar EVL, Dayton Audio Reference).
   - **Efficiency Bandwidth Product (EBP):**
     $$\text{EBP} = \frac{F_s}{Q_{es}}$$
     - Real-time classification: Sealed ($\le 50$), Flexible ($50\text{--}85$), Ported/Bandpass ($\ge 85$).
   - **Sealed Box Alignment (Acoustic Suspension):**
     $$V_b = \frac{V_{as}}{\left(\frac{Q_{tc}}{Q_{ts}}\right)^2 - 1}, \quad F_c = F_s \cdot \frac{Q_{tc}}{Q_{ts}}$$
   - **Bass Reflex Optimal Keele/Hoge Alignment:**
     $$V_b \approx 15 \cdot V_{as} \cdot (Q_{ts}^{2.87}), \quad F_b \approx 0.42 \cdot F_s \cdot (Q_{ts}^{-0.9})$$
   - **4th & 6th-Order Bandpass Synthesis:**
     - Computes low cutoff ($F_L$), high cutoff ($F_H$), center tuning ($F_o$), chamber volumes ($V_r, V_f$), and acoustic gain ($\text{dB}$).
   - **Isobaric Compound Mode:**
     - Dual-woofer push-pull or face-to-face configurations halve required $V_{as}$.

2. **Vehicle Trunk Spatial Constraint Solver & 3D Geometry (`geometry.py`)**
   - Profiles: Standard Rectangular Cuboid, Single Angled Wedge (seat recline / truck cab), Double Angled Wedge (symmetric trapezoid).
   - **Spatial Constraint Engine:** Lock 1 or 2 maximum trunk clearance boundaries (Height, Width) and back-solve Depth to hit target volume.
   - Comprehensive volumetric deduction engine accounting for:
     - Wood thickness (0.5", 0.75", 1.0", 1.5" double baffle)
     - Subwoofer motor/basket displacement
     - Physical port volume and slot divider wall wood displacement
     - Internal braces, dowels, and 45° corner kerfs

3. **Port Fluid Dynamics & Chuffing Prevention**
   - Supports flared aeroports, round PVC, and rectangular MDF slot ports (with straight or L-bend turns).
   - Boundary wall end-correction factor ($k \in [0.614, 2.227]$).
   - **Peak Port Velocity & Mach Meter:**
     $$V_o = \frac{\sqrt{2} \cdot S_d \cdot X_{max} \cdot 2\pi F_b}{A_p}$$
     - Visual warning badges when velocity exceeds $17\text{ m/s}$ (0.05 Mach) to prevent audible chuffing and compression.

4. **Fabrication Cut Sheet & CNC Export**
   - Generates exact panel cut lists with widths, heights, thicknesses, and recline miter bevel angles.
   - Export full build reports to `.txt` and cut dimensions to `.csv`.

---

## Quick Start (Development)

1. **Activate the Virtual Environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run Application:**
   ```powershell
   python main.py
   ```

---

## Compiling Standalone `.exe` (`RuneBox.exe`)

Run the automated one-click compilation batch script:
```cmd
build.bat
```
The compiled standalone executable will be generated in `dist\RuneBox.exe`.
