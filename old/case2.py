from build123d import *
from ocp_vscode import show, show_object, set_port, set_defaults, Camera

# ==============================================================================
# 1. PARAMETERS & DIMENSIONS
# ==============================================================================

# -- Global Settings --
WALL_THICKNESS = 2.0
LID_THICKNESS = 4.0
FIT_TOLERANCE = 0.3
LID_REBATE_DEPTH = 2.0
FILLET_R = 4.0       

# -- Fasteners --
INSERT_M3_HOLE_DIA = 4.2      
SCREW_M3_CLEARANCE = 3.4      

# UK Socket Settings
INSERT_M35_LENGTH = 7.1       
INSERT_M35_HOLE_DIA = 4.8     
SOCKET_BOSS_DIA = 12.0        
SOCKET_BOSS_DEPTH = 6.0       

WASHER_OD = 8.0
WASHER_THICKNESS = 2.0

# -- Internal Layout --
SIDE_MARGIN = 25.0       
GAP_BETWEEN_PID_SSR = 30.0 
GAP_SSR_FRONT = 20.0     
GAP_REAR_WIRING = 60.0   

# -- Components --
PID_BODY_W, PID_BODY_H, PID_BODY_D = 44.0, 44.0, 80.0
PID_BEZEL_W, PID_BEZEL_H, PID_BEZEL_D = 48.0, 48.0, 9.0
PID_FLOOR_CLEARANCE = 12.0

SSR_W, SSR_L, SSR_H = 50.0, 80.0, 73.0
SSR_MOUNT_SPACING = 72.0
SSR_SCREW_DEPTH = 7.0
SSR_PLATFORM_H = max(WALL_THICKNESS, SSR_SCREW_DEPTH) - WALL_THICKNESS 
SSR_TOP_CLEARANCE = 10.0 

UK_SOCKET_SIZE = 86.0        
UK_SOCKET_MOUNT_PITCH = 60.3 
UK_SOCKET_BACK_W = 73.0      
UK_SOCKET_BACK_D = 25.0      

C14_BODY_W, C14_BODY_H = 28.0, 48.0
C14_SCREW_PITCH, C14_SCREW_DIA = 40.0, 3.3    
C14_BOSS_DEPTH = 8.0

TERM_W, TERM_D, TERM_H = 36.0, 21.0, 13.0
TERM_MOUNT_X, TERM_MOUNT_Y = 28.0, 8.0
TERM_SCREW_DEPTH = 7.0

MAINS_BLK_W, MAINS_BLK_D, MAINS_BLK_H = 20.0, 15.0, 15.0

# -- Gate Settings --
GATE_WIDTH = 12.0
GATE_THICKNESS = WALL_THICKNESS
GATE_GUIDE_WIDTH = 2.0 # Extra width for the slots

# -- Labels --
MAIN_LABEL_1 = "PID Temp"
MAIN_LABEL_2 = "Controller"
LABEL_LEFT, LABEL_RIGHT = "+", "-"
BOSS_SIZE = 10.0

# -- Derived Dimensions --
INTERNAL_W = SIDE_MARGIN + PID_BEZEL_W + GAP_BETWEEN_PID_SSR + SSR_W + SIDE_MARGIN
LEN_LEFT, LEN_RIGHT = PID_BODY_D, GAP_SSR_FRONT + SSR_L
MAX_COMPONENT_L = max(LEN_LEFT, LEN_RIGHT)
INTERNAL_L = MAX_COMPONENT_L + GAP_REAR_WIRING 

HEIGHT_PID_STACK = PID_FLOOR_CLEARANCE + PID_BODY_H + UK_SOCKET_BACK_D + 10
HEIGHT_SSR_STACK = SSR_PLATFORM_H + SSR_H + SSR_TOP_CLEARANCE 
INTERNAL_H = max(HEIGHT_SSR_STACK, HEIGHT_PID_STACK)

BOX_W = INTERNAL_W + 2 * WALL_THICKNESS
BOX_L = INTERNAL_L + 2 * WALL_THICKNESS
BOX_H = INTERNAL_H + WALL_THICKNESS 

# ==============================================================================
# 2. MASTER POSITION CALCULATIONS
# ==============================================================================
front_inner_y = -INTERNAL_L/2
pid_center_x = -INTERNAL_W/2 + SIDE_MARGIN + PID_BEZEL_W/2
pid_center_y = front_inner_y + PID_BODY_D/2

ssr_center_x = (INTERNAL_W/2 - SIDE_MARGIN - SSR_W/2) + 5.0 
ssr_center_y = front_inner_y + GAP_SSR_FRONT + SSR_L/2

porch_x = pid_center_x # Now Gate X
c14_x, c14_y, c14_z = ssr_center_x, INTERNAL_L/2 + WALL_THICKNESS/2, INTERNAL_H / 2
mains_boss_x = pid_center_x 
mains_boss_y = (pid_center_y + PID_BODY_D/2 + INTERNAL_L/2) / 2
mains_blk_z = WALL_THICKNESS + MAINS_BLK_H/2
earth_boss_x = ssr_center_x - SSR_W/2 - 10 
earth_boss_y = INTERNAL_L/2 - 15

socket_x = pid_center_x + 3.0 
socket_y = 15.0 

# ==============================================================================
# 3. GHOSTS
# ==============================================================================
pid_pos_z = WALL_THICKNESS + PID_FLOOR_CLEARANCE + PID_BODY_H/2
pid_body_ghost = Location((pid_center_x, pid_center_y, pid_pos_z)) * Box(PID_BODY_W, PID_BODY_D, PID_BODY_H)
ssr_pos_z = WALL_THICKNESS + SSR_H/2 + SSR_PLATFORM_H
ssr_ghost = Location((ssr_center_x, ssr_center_y, ssr_pos_z)) * Box(SSR_W, SSR_L, SSR_H)
mains_ghost = Location((mains_boss_x, mains_boss_y, mains_blk_z)) * Box(MAINS_BLK_W, MAINS_BLK_D, MAINS_BLK_H)

# ==============================================================================
# 4. BUILD CASE BODY
# ==============================================================================
with BuildPart() as body:
    # A. Hull
    with BuildSketch():
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=BOX_H)
    chamfer(body.edges().filter_by(lambda e: abs(e.center().Z) < 0.1), length=1.0)

    # B. Hollow
    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        Rectangle(BOX_W - 2*WALL_THICKNESS, BOX_L - 2*WALL_THICKNESS)
        if FILLET_R - WALL_THICKNESS > 0:
            fillet(vertices(), radius=FILLET_R - WALL_THICKNESS)
    extrude(amount=-BOX_H + WALL_THICKNESS, mode=Mode.SUBTRACT)

    # C. Feet Recesses
    with BuildSketch(faces().sort_by(Axis.Z)[0]):
        with Locations(
            (INTERNAL_W/2 - 5, INTERNAL_L/2 - 5), (-INTERNAL_W/2 + 5, INTERNAL_L/2 - 5),
            (INTERNAL_W/2 - 5, -INTERNAL_L/2 + 5), (-INTERNAL_W/2 + 5, -INTERNAL_L/2 + 5)
        ):
            Circle(radius=10.0) 
    extrude(amount=1.0, mode=Mode.SUBTRACT)

    # D. Platforms & Bosses
    if SSR_PLATFORM_H > 0:
        with BuildSketch(Plane.XY.offset(WALL_THICKNESS)): 
            with Locations((ssr_center_x, ssr_center_y)):
                Rectangle(SSR_W + 4, SSR_L + 4)
        extrude(amount=SSR_PLATFORM_H)

    with Locations((ssr_center_x, ssr_center_y, WALL_THICKNESS + SSR_PLATFORM_H)): 
        with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
            Cylinder(radius=1.4, height=SSR_SCREW_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Mains & Earth Bosses
    with Locations((mains_boss_x, mains_boss_y, WALL_THICKNESS)):
        Cylinder(radius=5.0, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0,0,6)):
            Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((earth_boss_x, earth_boss_y, WALL_THICKNESS)):
        Cylinder(radius=5.0, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0,0,6)):
            Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # H. Rear "Gate" Slot (Replaces Porch)
    # ------------------------------------
    # We cut a slot in the rear wall for the "Gate" to slide into.
    gate_x_pos = porch_x
    rear_wall_y = BOX_L/2
    
    # 1. Main Pass-Through (The hole the wire goes through)
    with Locations((gate_x_pos, rear_wall_y, BOX_H/2 + WALL_THICKNESS)):
        # 12mm wide slot, all the way down to Z=10 (leaving a 10mm lip at bottom)
        slot_h = BOX_H - 10.0 # Leave 10mm at bottom
        Box(GATE_WIDTH, WALL_THICKNESS*4, slot_h, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    
    # 2. Guide Slots (The grooves the gate slides in)
    # 2mm wider than the main slot (1mm each side), centered in the wall thickness
    with Locations((gate_x_pos, rear_wall_y, BOX_H/2 + WALL_THICKNESS)):
        guide_w = GATE_WIDTH + 2 * GATE_GUIDE_WIDTH
        # Cut slightly shallower than full wall thickness to create a rebate? 
        # Easier: Cut a T-slot.
        # Let's just cut a wider slot *inside* the wall material.
        # This is complex to subtract.
        # Simpler approach: Cut the full slot, add "Rails" inside.
        pass

    # Actually, simpler "Drop-In" geometry:
    # Just a U-cutout in the wall. The Gate will be slightly wider and sit in "Rebates" inside the case.
    # Let's cut the REBATE first (Wider, Partial Depth), then the SLOT (Narrower, Full Depth).
    
    # Rebate (Inside face of rear wall)
    # Position: On the inner surface of rear wall (Y = INTERNAL_L/2)
    # Dimensions: GATE_WIDTH + 4mm wide, 2mm deep (into wall), Height = Top to Floor+10
    with Locations((gate_x_pos, INTERNAL_L/2, WALL_THICKNESS + 10)):
        # Box from Z=10 upwards
        # Width: 16mm (12 + 2+2)
        # Depth: 1.0mm (Half wall thickness)
        # Height: To top
        rebate_h = INTERNAL_H - 10.0
        # Align: Center X, Min Y (cutting into wall from inside), Min Z
        Box(GATE_WIDTH + 4.0, 2.0, rebate_h, align=(Align.CENTER, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    # Labyrinth Strain Relief (Floor Posts)
    # -------------------------------------
    # 3 Posts in a triangle/zigzag in front of the gate
    # Position: ~15mm inside the back wall
    lab_y = INTERNAL_L/2 - 15.0
    with Locations((gate_x_pos, lab_y, WALL_THICKNESS)):
        # Center Post
        Cylinder(radius=2.0, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Side Posts (slightly forward/back to create weave)
        with Locations((-6, -5), (6, -5)):
            Cylinder(radius=2.0, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # I. C14 Inlet
    c14_inner_y = BOX_L/2 - WALL_THICKNESS
    col_height = c14_z - WALL_THICKNESS 
    col_z_center = WALL_THICKNESS + col_height/2 
    col_y_center = c14_inner_y - C14_BOSS_DEPTH/2 
    with Locations((c14_x, 0, 0)): 
        with Locations((C14_SCREW_PITCH/2, 0, 0), (-C14_SCREW_PITCH/2, 0, 0)):
            with Locations((0, col_y_center, col_z_center)):
                Box(9.0, C14_BOSS_DEPTH, col_height)
            with Locations((0, col_y_center, c14_z)):
                Cylinder(radius=4.5, height=C14_BOSS_DEPTH, rotation=(90, 0, 0))
    with Locations((c14_x, BOX_L/2, c14_z)):
        Box(C14_BODY_W, WALL_THICKNESS*4, C14_BODY_H, mode=Mode.SUBTRACT)
    with Locations((c14_x, c14_inner_y, c14_z)):
        with Locations((C14_SCREW_PITCH/2, 0, 0), (-C14_SCREW_PITCH/2, 0, 0)):
             Cylinder(radius=SCREW_M3_CLEARANCE/2, height=WALL_THICKNESS*4, rotation=(90,0,0), align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)
             Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=C14_BOSS_DEPTH, rotation=(90,0,0), align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # I2. PID Cutout
    with Locations((pid_center_x, -BOX_L/2, pid_pos_z)):
        Box(PID_BODY_W + FIT_TOLERANCE, WALL_THICKNESS*4, PID_BODY_H + FIT_TOLERANCE, mode=Mode.SUBTRACT)

    # J. Corner Pillars
    with BuildSketch(Plane.XY.offset(WALL_THICKNESS)):
        with Locations(
            (INTERNAL_W/2 - BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (INTERNAL_W/2 - BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2)
        ):
            Rectangle(BOSS_SIZE, BOSS_SIZE)
            Circle(4) 
    extrude(amount=BOX_H - WALL_THICKNESS)
    with Locations(
        (INTERNAL_W/2 - BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
        (-INTERNAL_W/2 + BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
        (INTERNAL_W/2 - BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2),
        (-INTERNAL_W/2 + BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2)
    ):
         with Locations((0,0, BOX_H)):
             Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=15, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # K. Vents
    vent_z = WALL_THICKNESS + 6.0 
    with Locations((BOX_W/2, ssr_center_y, vent_z)):
        with GridLocations(0, 10, 1, 4):
            Box(WALL_THICKNESS*4, 6, 4, rotation=(0, 0, 0), mode=Mode.SUBTRACT)

    front_vent_z = BOX_H / 2 
    with Locations((ssr_center_x, -BOX_L/2, front_vent_z)):
        with GridLocations(6, 0, 5, 1): 
            Box(3.0, 10.0, 25.0, mode=Mode.SUBTRACT)

# ==============================================================================
# 5. BUILD GATE (New Part)
# ==============================================================================
# A simple rectangular plate that fits in the rebate.
# Height: From Z=10 to Top (INTERNAL_H) - Tolerance
# Width: GATE_WIDTH + 4.0 - Tolerance
# Thickness: 2.0mm (fits in rebate)
gate_h = INTERNAL_H - 10.0 - 0.5 
gate_w = GATE_WIDTH + 4.0 - 0.4
with BuildPart() as gate:
    with BuildSketch():
        Rectangle(gate_w, gate_h)
    extrude(amount=2.0)
    # Add a little "Arch" cutout at the bottom for the wire
    with Locations((0, -gate_h/2)):
        Cylinder(radius=2.5, height=10, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

# ==============================================================================
# 6. BUILD LID
# ==============================================================================
with BuildPart() as lid:
    with BuildSketch(Plane.XY):
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=LID_THICKNESS)
    
    with BuildSketch(Plane.XY): 
        Rectangle(INTERNAL_W - 0.8, INTERNAL_L - 0.8) 
        with Locations(
            (INTERNAL_W/2 - BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (INTERNAL_W/2 - BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2)
        ):
            Rectangle(BOSS_SIZE + 0.6, BOSS_SIZE + 0.6, mode=Mode.SUBTRACT)
    extrude(amount=-2.0) 

    with BuildSketch(Plane.XY.offset(10.0)):
        with Locations((socket_x, socket_y)):
            Rectangle(UK_SOCKET_BACK_W, UK_SOCKET_BACK_W)
    extrude(amount=-50.0, mode=Mode.SUBTRACT)

    left_screw_x = socket_x - UK_SOCKET_MOUNT_PITCH/2 
    right_screw_x = socket_x + UK_SOCKET_MOUNT_PITCH/2 
    with BuildSketch(Plane.XY): 
        with Locations((left_screw_x, socket_y)):
            c_left = Circle(radius=SOCKET_BOSS_DIA/2, mode=Mode.PRIVATE)
        with Locations((left_screw_x - 7.5, socket_y)):
            r_left = Rectangle(15.0, SOCKET_BOSS_DIA, mode=Mode.PRIVATE)
        add(c_left + r_left)
        with Locations((right_screw_x, socket_y)):
            c_right = Circle(radius=SOCKET_BOSS_DIA/2, mode=Mode.PRIVATE)
        with Locations((right_screw_x + 7.5, socket_y)):
            r_right = Rectangle(15.0, SOCKET_BOSS_DIA, mode=Mode.PRIVATE)
        add(c_right + r_right)
    extrude(amount=-SOCKET_BOSS_DEPTH)

    with Locations((socket_x, socket_y, LID_THICKNESS)):
        with Locations((UK_SOCKET_MOUNT_PITCH/2, 0), (-UK_SOCKET_MOUNT_PITCH/2, 0)):
             Cylinder(radius=INSERT_M35_HOLE_DIA/2, height=30, mode=Mode.SUBTRACT)

    hole_off_x, hole_off_y = INTERNAL_W/2 - BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2
    with Locations(
        (hole_off_x, hole_off_y, LID_THICKNESS), (-hole_off_x, hole_off_y, LID_THICKNESS),
        (hole_off_x, -hole_off_y, LID_THICKNESS), (-hole_off_x, -hole_off_y, LID_THICKNESS)
    ):
        CounterBoreHole(radius=SCREW_M3_CLEARANCE/2, counter_bore_radius=3.1, counter_bore_depth=2.0)

    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((ssr_center_x, ssr_center_y)):
            with GridLocations(x_spacing=6, y_spacing=0, x_count=int(SSR_W/6), y_count=1):
                SlotOverall(width=SSR_L - 10, height=3, rotation=90)
    extrude(amount=-20, mode=Mode.SUBTRACT)

    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((pid_center_x, -50)):
             with Locations((0, 9)): 
                 Text(MAIN_LABEL_1, font_size=10, font_style=FontStyle.BOLD, rotation=0, align=(Align.CENTER, Align.CENTER))
             with Locations((0, -9)): 
                 Text(MAIN_LABEL_2, font_size=10, font_style=FontStyle.BOLD, rotation=0, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-0.6, mode=Mode.SUBTRACT)

# ==============================================================================
# 7. BUILD WASHER
# ==============================================================================
with BuildPart() as washer:
    Cylinder(radius=WASHER_OD/2, height=WASHER_THICKNESS)
    Hole(radius=SCREW_M3_CLEARANCE/2)

# ==============================================================================
# 8. EXPORT & VISUALIZE
# ==============================================================================
lid_moved = lid.part.move(Location((0,0, BOX_H + 5)))
gate_moved = gate.part.move(Location((porch_x, INTERNAL_L/2 - 5, BOX_H/2), (0,0,0)))
washer_moved = washer.part.move(Location((0, BOX_L/2 + 20, 0))) 

assembly = Compound(children=[body.part, lid_moved, gate_moved, washer_moved, pid_body_ghost, ssr_ghost, mains_ghost])
print(f"Case Dimensions: {BOX_W:.1f} x {BOX_L:.1f} x {BOX_H:.1f} mm")

export_stl(body.part, "pid_case_body.stl")
export_stl(lid.part, "pid_lid.stl")
export_stl(gate.part,  "pid_rear_gate.stl")
export_stl(washer.part, "pid_washer.stl")

show_object(body, name="Body", options={"alpha": 1.0, "color": (0.8, 0.8, 0.8)})
show_object(lid_moved, name="Lid", options={"alpha": 0.5, "color": (0.6, 0.6, 1.0)})
show_object(gate_moved, name="Gate", options={"alpha": 0.8, "color": (1.0, 0.6, 0.0)})
show_object(washer_moved, name="Washer", options={"alpha": 1.0, "color": (0.2, 0.2, 0.2)})
show_object(pid_body_ghost, name="PID Ghost", options={"alpha": 0.3, "color": (1, 0, 0)})
show_object(ssr_ghost, name="SSR Ghost", options={"alpha": 0.3, "color": (0, 1, 0)})
show_object(mains_ghost, name="Mains Block Ghost", options={"alpha": 0.3, "color": (1, 1, 0)})