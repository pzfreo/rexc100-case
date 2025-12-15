**Role:** Act as a Senior Mechanical Design Engineer. Write a Python script using the `build123d` library to generate a parametric, 3D-printable industrial enclosure.

**1. Environment & Constraints**
* **Library:** `build123d` (Algebra mode preferred).
* **Visualizer:** `ocp_vscode` (Show Body, Lid, Cover, Washer, and transparent "Ghost" electronics).
* **Printer Constraint:** The final assembly length must fit on a **256x256mm build plate** (Target total length < 250mm).
* **Printability:** Design for FDM printing without supports (chamfers on overhangs, text on top faces).

**2. Global Case Settings**
* **Wall Thickness:** 2.0 mm.
* **Lid Thickness:** 4.0 mm.
* **Fillets:** 4.0 mm external corner radius.
* **Fasteners:** Design for M3 self-tapping screws.
* **Hole Type:** Use **Counterbores** (flat bottom) for all lids to ensure solid screw grip.

**3. Component Dimensions ("Ghost" Objects)**
* **REX-C100 PID:**
    * Bezel: 48x48mm, Depth 9mm.
    * Body: 44x44mm, Depth 80mm.
    * *Placement:* Front wall, centered.
* **SSR + Heatsink:**
    * Footprint: 50mm (W) x 80mm (L).
    * Height: 73mm.
    * *Placement:* Floor mounted, behind PID.
* **External Terminal Block:**
    * Size: 36mm (W) x 21mm (D) x 13mm (H).
    * *Placement:* External "Porch" on the rear wall.

**4. Design Requirements & Layout**

* **A. Internal Layout & Spacing:**
    * **Gap (PID to SSR):** 40mm (Wire routing).
    * **Gap (SSR to Rear Wall):** 45mm (Critical for bending stiff mains cable).
    * **Wiring Margin:** Add 40mm width margin for side cable routing.

* **B. Rear "Porch" (Left Side):**
    * Create a U-shaped extension on the **Left Side** of the rear wall.
    * **Walls:** Extend walls up from the porch floor (approx 18mm high).
    * **Wire Exit:** Rear-facing slot for external wires.
    * **Mounting:** Floor holes for the terminal block.

* **C. Cable Management (Right Side):**
    * Locate two (2) cable entry holes on the **Right Side** of the rear wall (spaced 22mm apart).
    * **Anchors:** Create two raised block anchors on the floor corresponding to the entries.
    * **Zip Tie Slots:** Large **5.0mm x 3.5mm** slots.
    * **Refinement:** Apply a **0.5mm fillet** to the slot edges to prevent cutting the zip ties.

* **D. Main Lid:**
    * Top-fitting lid, 4mm thick.
    * **Ventilation:** Grid of slots above the SSR area. Ribs must be **3mm thick** (6mm pitch).
    * **Label:** Emboss **"PID Temp" / "Controller"** (2 lines) on the top face (0.6mm height), oriented for reading from the front.
    * **Order of Operations:** Ensure ventilation is cut *before* text is embossed to avoid artifacts.

* **E. Terminal Safety Cover:**
    * A flat lid (4mm thick) that screws onto the Porch walls.
    * **Tolerance:** Ensure a **1.0mm air gap** between the cover and the main case wall.
    * **Safety Labels:** Engrave `+` and `-` symbols on the **Top Face** (0.6mm deep).
    * **Poka-yoke (Mistake Proofing):**
        1.  Offset the screw holes by 3mm (asymmetric) so the lid cannot be reversed.
        2.  Add a semi-circular "finger notch" on the rear edge to indicate orientation.

* **F. Accessories:**
    * Generate a separate **M3 Washer** (8mm OD, 2mm thick) for load distribution.

**5. Output Generation**
* Export four STLs: `pid_case_body.stl`, `pid_lid.stl`, `pid_term_cover.stl`, `pid_washer.stl`.
* Show an exploded assembly view in the visualizer.