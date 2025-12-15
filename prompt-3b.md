# Master Design Prompt

**Project Goal:**
Create a two-part 3D printed enclosure for a PID temperature control system. The design is **"Inverted"**: the "Lid" acts as the main structural body (printed upside down), and the "Base" is a removable bottom plate.

**Core Components:**
1.  **PID Controller:** Inkbird ITC-100 (1/16 DIN Standard).
2.  **SSR:** Solid State Relay + Heatsink (50x80mm footprint).
3.  **Power:** UK Mains Socket (Standard 73mm square) + C14 Inlet (Fused/Switched).
4.  **Sensors:** K-Type Thermocouple Terminal Block.

---

### **Part A: The Base Plate (Bottom Cover)**
* **Thickness:** 5.0mm (Critical for thread engagement).
* **SSR Mounting:**
    * **Standoffs:** Do NOT use a solid block. Use two circular pillars (12mm dia) or rectangular bars to support the SSR corners only.
    * **Ventilation:** Cut a grill of 30mm slots directly between these standoffs (Bottom Intake).
* **Terminal Block:** Mount on a 5mm boss. Position this **40mm forward** from the rear edge to allow stiff thermocouple wires to bend naturally.
* **Fasteners:**
    * **Component Mounts:** Sized for M3 Self-Tapping Screws (2.8mm pilot holes) or Heat-Set Inserts (4.2mm) based on a boolean switch.
    * **Case Screws:** 4x M3 Countersunk Clearance holes in the corners.
    * **Gotcha Fix:** Ensure counterbores cut **UP** from the bottom face (Z=0), not down from the top.

### **Part B: The Shell (Inverted Body)**
* **Orientation:** Printed "Upside Down" (Roof on build plate at Z=0; Open bottom at Z=Height).
* **PID Mounting (The "Clamp & Anvil"):**
    * **The Anvil (Brace):** A solid block extending from the **Roof (Z=0)** down to the **Top of the PID**. This prevents the controller from floating up.
    * **The Hammer (Clamp):** A 10mm block located immediately **Below the PID** (near the open bottom).
    * **Access:** A vertical screw hole through the Hammer, accessible from the open bottom, pushing the PID **UP** against the Anvil.
* **UK Socket:**
    * **Right Boss:** Needs a "Dog Bone" reinforcement tail extending sideways to prevent snapping.
    * **Left Boss:** Bridge to the nearest wall for strength.
    * **Holes:** Sized for M3.5 (standard electrical screw) or M3 if prototyping.
* **C14 Inlet:**
    * **Location:** Rear wall, vertically centered.
    * **Reinforcement:** Add full-height "Pilasters" (12mm thick) next to the cutout to support the mounting screws.
    * **Clearance:** Ensure the screw cutter cylinders are long enough (30mm) to punch through these thick pilasters.
* **Ventilation (Chimney Effect):**
    * **Front Face:** SOLID (No vents).
    * **Top Face (Roof):** Grill slots directly above the SSR.
    * **Logic:** Cool air enters Base Grill → Rises through SSR → Exits Roof Grill.

### **Part C: "Gotcha" Avoidance Checklist**
1.  **Z-Axis Orientation:** Remember the shell is inverted. "Top" of the case is Z=0. "Bottom" opening is Z=Max.
2.  **Counterbore Direction:** Base plate holes must be cut from Z=0 upwards, leaving a solid shoulder for the screw head.
3.  **SSR Insulation:** Never place the SSR heatsink on a solid block of plastic; it insulates the heat. Use standoffs.
4.  **C14 Cable Clearance:** Leave at least **45mm of depth** behind the C14 inlet for the stiff power cables.
5.  **Thermocouple Wire Path:** K-Type wires are stiff springs. Do not place the terminal block too close to the strain relief pillars; they need ~20mm of "runway" to straighten out.