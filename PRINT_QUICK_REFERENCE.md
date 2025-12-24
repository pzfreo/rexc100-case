# PID Case - Quick Print Reference Card

Print this page and keep next to printer!

---

## Profile Selection

```
┌─────────────────────────────────────────┐
│ Printer:  Bambu Lab P1S 0.4 nozzle      │
│ Filament: ABS - PID Case Optimized      │
│ Process:  PID Case - ABS Structural     │
│ Plate:    Textured PEI + ABS slurry     │
└─────────────────────────────────────────┘
```

---

## Part Orientations

### Base Plate
```
  ┌─────────────────┐
  │                 │  ← Top (holes/bosses face up)
  │    BASE         │
  │                 │
  └─────────────────┘
 ═══════════════════  ← Bed (feet indents down)
```
**Print as-is. No rotation needed.**

### Shell
```
 ═══════════════════  ← Bed (roof surface down)
  ┌─────────────────┐
  │                 │
  │    SHELL        │
  │                 │  ← Top (open bottom faces up)
  └─────────────────┘
```
**FLIP UPSIDE DOWN. Roof on bed!**

---

## Critical Settings Checklist

**Before Slicing:**
- [ ] Shell oriented upside down
- [ ] Brim: 10mm (auto-enabled in profile)
- [ ] Supports: OFF (not needed)

**Before Printing:**
- [ ] Enclosure CLOSED
- [ ] Bed cleaned with IPA
- [ ] ABS slurry applied
- [ ] Filament loaded and dry
- [ ] No drafts

**During Print:**
- [ ] Watch first 5 minutes
- [ ] Verify brim adhering
- [ ] Chamber at 45°C

**After Completion:**
- [ ] WAIT 30-45 min before opening
- [ ] Let chamber cool to <60°C
- [ ] Then remove part

---

## Temperatures

```
╔══════════════════════════════╗
║  Nozzle:  250°C              ║
║  Bed:     100°C              ║
║  Chamber: 45°C (automatic)   ║
╚══════════════════════════════╝
```

---

## Print Times & Material

| Part  | Time    | Material | Cost  |
|-------|---------|----------|-------|
| Base  | 10-12h  | 180-220g | $5-7  |
| Shell | 14-18h  | 250-300g | $7-10 |
| TOTAL | 24-30h  | 430-520g | $12-15|

---

## Heat Set Insert Guide

**Iron Temperature:** 280-300°C
**Dwell Time:** 4-6 seconds
**Pressure:** Medium (let iron weight do work)

### Insert Count (Your Config)
```
SSR:       2× M3    ✓ Inserts
Terminal:  4× M3    ✗ Screws
Corners:   4× M3    ✓ Inserts
Socket:    2× M3.5  ✓ Inserts
C14:       2× M3    ✓ Inserts
PID Clamp: 1× M3    ✓ Inserts

Total inserts needed: 11 pieces
```

**Buy:**
- M3 inserts: 9 pieces (4.0mm OD × 5.7mm L)
- M3.5 inserts: 2 pieces (4.6mm OD × 6.0mm L)

---

## Common Issues - Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| **Corners lifting** | Increase brim to 15mm, verify enclosure closed |
| **First layer not sticking** | Clean bed, apply ABS slurry, increase bed to 105°C |
| **Warping mid-print** | Check for drafts, ensure chamber 45°C |
| **Stringing** | Already optimized, try reducing temp to 245°C |
| **Layer gaps** | Reduce cooling to 0%, increase temp to 255°C |

---

## Bambu P1S AMS Settings

**If using AMS:**
- Slot 1: ABS (this profile)
- Drying: 65°C for 6+ hours before print
- Humidity: Keep <15% if possible

**Multi-color not recommended** for structural parts.

---

## Safety Reminders

⚠️ **ABS emits styrene fumes**
- Print in ventilated area
- Use air filter if available
- Don't print in living spaces

🔥 **Fire safety**
- Don't leave unattended for long prints
- Ensure smoke detector nearby

---

## Post-Print Workflow

1. ⏱️  **Wait 30-45 min** (enclosure closed)
2. 🌡️  **Chamber <60°C** before opening
3. 🔧  **Remove carefully** (may still be warm)
4. ✂️  **Remove brim** with flush cutters
5. 🕐  **Rest 24h** before installing inserts
6. 🔥  **Install inserts** at 280-300°C
7. 🔩  **Assemble** case

---

## Profile Files Location

```
/Users/paul/repos/pid-case/
├── OrcaSlicer_ABS_Filament_Profile.json
├── OrcaSlicer_PID_Case_Print_Profile.json
└── ORCASLICER_SETUP.md (detailed instructions)
```

---

**Version:** 1.0
**Optimized for:** Bambu P1S + ABS + Large structural parts
**Last updated:** 2024

---

**Emergency Stop Conditions:**
- Visible smoke/burning smell → STOP
- Nozzle clogging repeatedly → STOP
- Part completely detached → STOP
- Layers visibly separating → STOP

**Good luck with your print! 🎯**
