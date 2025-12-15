This master prompt captures the exact specifications of the final V5.9 design, along with specific technical "guardrails" to prevent the bugs we encountered (floating parts, missing vents, `hull()` errors).

You can use this prompt to regenerate the project from scratch or to instruct another AI/developer on exactly how to build this specific version.

***

### Master Prompt: The "RexC100 Optimized" PID Controller Case

**Goal:**
Create a Python script using the `build123d` library to generate a high-quality, DFM-optimized enclosure for a RexC100 PID Controller, an SSR (Solid State Relay), and a UK Mains Socket. The design must be 3D-printable without support material ("support-free") and feature a "Chimney Effect" passive cooling system.

**Technical Constraints & Anti-Regression Rules:**
1.  **Absolute Coordinates Only:** Do not rely on relative face selection (`faces().sort_by(...)`) for critical positioning. Pre-calculate global `(x, y, z)` coordinates for the PID, SSR, and Socket centers at the start of the script and use `Locations((x,y,z))` for placement.
2.  **No `hull()` Operations:** Use simple boolean unions (`add(shape1 + shape2)`) to create reinforced shapes like the "Dog Bone" lid mounts. `hull()` is unstable in some library versions.
3.  **Solid Boolean Cuts:** For all vents (especially front/side walls), use **Solid Primitives** (`Box(..., mode=Mode.SUBTRACT)`) positioned to intersect the wall. Do not sketch 2D shapes on face surfaces, as this leads to "zero-thickness" errors where cuts fail to appear.
4.  **"Pilaster" Construction:** For the C14 inlet and side mounts, do not use floating cylinders. Build "Pilasters" (engaged columns) by unioning a `Cylinder` (boss) with a `Box` (support) that extends down to the floor (`Z=2.0`). This eliminates the need for 3D print supports.
5.  **Face Normal Safety:** When cutting the front vents, do not rely on plane normals. Use a cutter object that is thick enough to penetrate the wall in both directions (e.g., `Box(..., align=(Align.CENTER...))`).

**Design Specifications (V5.9 Standard):**

* **Global Dims:**
    * Wall Thickness: **2.0mm**
    * Lid Thickness: **4.0mm**
    * Fillet Radius: **4.0mm** (Vertical edges)
    * Base Chamfer: **1.0mm** (To prevent elephant's foot)

* **Layout Strategy (Split-Level):**
    * **PID:** Front-Left.
    * **SSR:** Front-Right. **Shifted +5mm Right** to clear the socket.
    * **UK Socket:** Top-Center-Left. **Shifted +15mm Back** and **+3mm Right** relative to PID. This creates a "DMZ" gap for wiring and reduces total case height.
    * **C14 Inlet:** Left Wall, aligned with SSR depth.
    * **Divider Wall:** **REMOVED** to improve airflow and wiring ease.

* **Thermal Management (Chimney Effect):**
    * **Intake:** Vertical slots on the **Front Face**, aligned with the SSR heatsink.
    * **Exhaust:** Matching slots on the **Lid**, directly above the SSR.
    * **Floor:** Grid of slots directly under the SSR.

* **Fasteners & Mounts:**
    * **C14 Mounts:** M3 inserts (Hole 4.2mm), Boss Depth **8.0mm**. Built as Pilasters.
    * **Socket Mounts:** M3.5 inserts (Hole 4.8mm), Boss Depth **6.0mm**. Built as "Dog Bones" (Circle + Rectangle union) connecting to the lid side walls.
    * **Lid Screws:** M3 Counterbored holes in corners.

**Output:**
The script must generate and export four STL files:
1.  `pid_case_body.stl`
2.  `pid_lid.stl`
3.  `pid_term_cover.stl` (Rear safety cover)
4.  `pid_washer.stl` (Safety washer)

**Visualization:**
Include `show_object()` calls with transparency for the "Ghost" components (PID body, SSR, Mains Block) to verify fitment visually.