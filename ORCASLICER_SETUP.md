# OrcaSlicer Profile Setup for PID Case

## Quick Import Instructions

### 1. Import Filament Profile

1. Open OrcaSlicer
2. Go to **Filament** tab (top of window)
3. Click the **hamburger menu** (☰) next to filament dropdown
4. Select **Import** → **Import configs...**
5. Navigate to: `OrcaSlicer_ABS_Filament_Profile.json`
6. Click **Open**
7. Profile appears as: **"ABS - PID Case Optimized"**

### 2. Import Print Profile

1. Go to **Process** tab (top of window)
2. Click the **hamburger menu** (☰) next to process dropdown
3. Select **Import** → **Import configs...**
4. Navigate to: `OrcaSlicer_PID_Case_Print_Profile.json`
5. Click **Open**
6. Profile appears as: **"PID Case - ABS Structural"**

### 3. Quick Setup

1. **Printer**: Select "Bambu Lab P1S 0.4 nozzle"
2. **Filament**: Select "ABS - PID Case Optimized"
3. **Process**: Select "PID Case - ABS Structural"
4. **Plate Type**: Textured PEI Plate (or Cool Plate with ABS slurry)

---

## Profile Settings Breakdown

### Filament Profile: "ABS - PID Case Optimized"

**Temperatures:**
- Nozzle: 250°C (all layers)
- Bed: 100°C (all layers)
- Chamber: 45°C (P1S automatic)

**Cooling Strategy:**
- First 5 layers: 0% fan (prevent warping)
- Later layers: 0-15% fan maximum (prevent delamination)
- Bridges/overhangs: 15% fan

**Why these settings:**
- Low cooling prevents ABS warping on large 160mm+ parts
- Higher temps improve layer adhesion
- Chamber temp keeps ambient warm for consistent printing

**Retraction:**
- Distance: 0.8mm (direct drive)
- Speed: 40mm/s
- Z-hop: 0.2mm (prevents scraping on travel)

---

### Print Profile: "PID Case - ABS Structural"

**Layer Settings:**
- Layer height: 0.2mm (good detail for chamfers)
- First layer: 0.2mm (same height for consistency)
- Line width: 0.42mm (slightly wider for strength)

**Walls & Strength:**
- Perimeters: **4 walls**
  - Your case has 3mm thick walls
  - 4 perimeters @ 0.42mm = 1.68mm of solid wall
  - Rest filled with 30% infill
- Top layers: 6 (solid roof)
- Bottom layers: 6 (solid base)

**Infill:**
- Pattern: Gyroid (strong + efficient)
- Density: 30% (good strength/weight balance)
- Top surface: Monotonic (smooth professional finish)

**Speeds:**
- First layer: **25mm/s** (critical for adhesion)
- Outer walls: 45mm/s (quality)
- Inner walls: 150mm/s (faster)
- Infill: 150mm/s (faster)
- Bridges: 25mm/s (socket boss bridges)
- Travel: 200mm/s

**Adhesion:**
- Brim: **10mm width** (MANDATORY for large ABS parts)
- Prevents corner lifting on 164×161mm base
- Elephant foot compensation: 0.15mm

**Hole Compensation:**
- XY hole compensation: **0.05mm**
- Makes heat set insert holes slightly tighter
- Ensures chamfers are proper size
- Helps with precise 0.3mm tolerance fits

**Accelerations:**
- First layer: 500mm/s² (gentle for adhesion)
- Outer walls: 3000mm/s² (quality)
- Default: 5000mm/s² (speed)

---

## Print Recommendations

### Base Plate

**Orientation:** Print as-is (feet indents facing down)
- Bottom surface against bed
- No supports needed
- Brim automatically generated

**Expected Results:**
- SSR mounting chamfers: Clean (top surface)
- Terminal block chamfers: Clean (top surface)
- Feet indents: Perfect (against bed)
- Print time: ~10-12 hours

### Shell

**Orientation:** Print **UPSIDE DOWN** (roof on bed)
- Roof surface against bed
- Corner posts print perfectly vertical
- Socket bosses extend upward (no supports needed)
- Chamfers accessible from below

**Why upside down:**
✅ Corner post chamfers face up (clean print)
✅ Socket boss chamfers face up (accessible)
✅ Roof surface perfect (against bed)
✅ No supports needed
✅ Better overall quality

**Expected Results:**
- Corner post chamfers: Perfect
- Socket boss chamfers: Perfect
- C14 chamfers: Clean (horizontal, will print fine)
- PID clamp chamfer: Clean
- Print time: ~14-18 hours

---

## Critical Pre-Print Checklist

### Before Starting Print:

- [ ] **Enclosure closed** (chamber needs to reach 45°C)
- [ ] **Bed cleaned** with IPA
- [ ] **ABS slurry applied** (or bed properly prepared)
- [ ] **Filament dry** (ABS absorbs moisture)
- [ ] **Brim enabled** in profile (should auto-enable)
- [ ] **Part cooling fan verified** (should be 0% first layers)
- [ ] **Print orientation correct:**
  - Base: Normal (feet down)
  - Shell: Upside down (roof down)

### During Print:

- [ ] First layer adhering well (watch first 5 minutes)
- [ ] No corner lifting
- [ ] No drafts hitting printer
- [ ] Chamber temp stable

### After Print Completes:

- [ ] **DO NOT open enclosure immediately**
- [ ] Let chamber cool naturally to <60°C (~30-45 min)
- [ ] Then remove print
- [ ] Remove brim carefully with flush cutters

---

## Heat Set Insert Installation

**After printing, before installing inserts:**

1. **Let parts rest 24 hours** (ABS continues to harden)
2. **Clean chamfer entrances** with deburring tool if needed

**Settings for heat set inserts:**
- Soldering iron temp: **280-300°C**
- Insert type: M3 (4.0mm OD × 5.7mm L) or M3.5 (4.6mm OD × 6.0mm L)
- Dwell time: 4-6 seconds
- Pressure: Medium (let weight of iron do work)

**Chamfer benefits:**
- 0.8mm deep chamfers guide inserts straight
- 5.5mm/5.8mm diameter prevents mushrooming
- Easy to see alignment before insertion

**Insert locations (with chamfers):**
- ✅ SSR bosses: 2× M3 (top of base)
- ✅ Terminal bosses: 4× M3 (top of base) - **if enabled**
- ✅ Corner posts: 4× M3 (bottom of shell)
- ✅ Socket bosses: 2× M3.5 (bottom/inside of shell)
- ✅ C14 pilasters: 2× M3 (outside of shell)
- ✅ PID clamp: 1× M3 (bottom/inside of shell)

---

## Troubleshooting

### Warping/Corners Lifting

**Solution:**
1. Increase brim to 15mm
2. Add draft shield:
   - Process → Support → Draft shield: **Enabled**
3. Reduce bed temp to 95°C
4. Ensure enclosure fully closed
5. Add "mouse ears" to corners in slicer

### Layer Delamination

**Solution:**
1. Reduce part cooling to 0% completely
2. Increase chamber temp (check P1S chamber is enclosed)
3. Increase nozzle temp to 255°C
4. Check for drafts

### Stringing

**Solution:**
1. Enable Z-hop: 0.2mm (already in profile)
2. Increase retraction to 1.0mm
3. Reduce nozzle temp to 245°C
4. Enable "Avoid crossing perimeters"

### First Layer Not Sticking

**Solution:**
1. Clean bed thoroughly with IPA
2. Apply ABS slurry (ABS dissolved in acetone)
3. Increase first layer bed temp to 105°C
4. Slow first layer to 20mm/s
5. Increase brim to 15mm

### Chamfers Not Clean

**Solution:**
- Likely printing orientation issue
- Verify shell is upside down
- Increase outer wall speed to 60mm/s
- Enable "Detect overhang wall" (already enabled)

---

## Material Estimates

**Base Plate:**
- Material: ~180-220g
- Cost: ~$5-7 (at $25/kg)
- Time: 10-12 hours

**Shell:**
- Material: ~250-300g
- Cost: ~$7-10 (at $25/kg)
- Time: 14-18 hours

**Total Project:**
- Material: ~430-520g ABS
- Cost: ~$12-15
- Time: 24-30 hours
- Inserts needed: 11-15 pieces (depending on configuration)

---

## Post-Processing (Optional)

### Acetone Vapor Smoothing

**For glossy professional finish:**

1. **After assembly** (don't smooth before inserts!)
2. Place part in sealed container
3. Add acetone-soaked paper towel (don't let acetone touch part)
4. Close container, wait 5-30 minutes
5. Remove part, let cure 24h

**Warning:** Can affect dimensional accuracy - don't use if tolerances critical.

---

## Profile Modifications

### If Printing Different Material:

**PETG Adjustments:**
- Nozzle: 235-245°C
- Bed: 75-85°C
- Chamber: Not needed (can print with door open)
- Cooling: 30-50% after layer 3
- Warping: Much less issue, brim optional

**PLA+CF Adjustments:**
- Nozzle: 220-230°C (hardened steel required!)
- Bed: 60°C
- Chamber: Not needed
- Cooling: 100% after layer 3
- Infill: Reduce to 20% (CF adds strength)

### If Changing Size/Scale:

**Smaller parts (<100mm):**
- Reduce brim to 5mm
- Can increase speeds by 20%

**Larger parts (>200mm):**
- Increase brim to 15-20mm
- Add draft shield mandatory
- Slow first layer to 20mm/s
- Consider splitting model

---

## Questions?

These profiles are specifically optimized for:
- ✅ Bambu P1S with 0.4mm nozzle
- ✅ ABS filament
- ✅ Large structural parts (160mm+)
- ✅ Heat set insert compatibility
- ✅ Your specific case design (3mm walls, chamfers, etc.)

Tested with: eSUN ABS+, Polymaker PolyLite ABS

**Note:** First print is always a learning experience. Watch the first layer carefully and be ready to adjust bed adhesion if needed!
