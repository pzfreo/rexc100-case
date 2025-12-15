from build123d import *
from ocp_vscode import show, show_object, set_port, set_defaults, Camera

# ==============================================================================
# 1. PARAMETERS & DIMENSIONS
# ==============================================================================

# -- Global Settings --
WALL_THICKNESS = 2.0
LID_THICKNESS = 4.0
FIT_TOLERANCE = 0.3
FILLET_R = 4.0       

# -- Fasteners (Heat-Set Inserts) --
INSERT_M3_HOLE_DIA = 4.2      
SCREW_M3_CLEARANCE = 3.4      

INSERT_M35_LENGTH = 7.1       
INSERT_M35_HOLE_DIA = 4.8     
SOCKET_BOSS_DIA = 10.0        
SOCKET_BOSS_DEPTH = 5.0       

WASHER_OD = 8.0
WASHER_THICKNESS = 2.0

# -- Internal Layout --
SIDE_MARGIN = 25.0       
GAP_BETWEEN_PID_SSR = 25.0 
GAP_SSR_FRONT = 20.0     
GAP_REAR_WIRING = 60.0   

# -- Components --
PID_BODY_W, PID_BODY_H, PID_BODY_D = 44.0, 44.0, 80.0
PID_BEZEL_W, PID_BEZEL_H, PID_BEZEL_D = 48.0, 48.0, 9.0
PID_FLOOR_CLEARANCE = 12.0

SSR_W, SSR_L, SSR_H = 50.0, 80.0, 73.0
SSR_MOUNT_SPACING = 72.0
SSR_SCREW_DEPTH = 7.0

UK_SOCKET_SIZE = 86.0        
UK_SOCKET_MOUNT_PITCH = 60.3 
UK_SOCKET_BACK_W = 70.0      
UK_SOCKET_BACK_D = 25.0      

C14_BODY_W, C14_BODY_H = 28.0, 48.0
C14_SCREW_PITCH, C14_SCREW_DIA = 40.0, 3.3    
C14_BOSS_DEPTH = 6.0

TERM_W, TERM_D, TERM_H = 36.0, 21.0, 13.0
TERM_MOUNT_X, TERM_MOUNT_Y = 28.0, 8.0
TERM_SCREW_DEPTH = 7.0

MAINS_BLK_W, MAINS_BLK_D, MAINS_BLK_H = 20.0, 15.0, 15.0

# -- Porch Settings --
PORCH_FREE_SPACE = 5.0   
PORCH_WALL_H = TERM_H + 5
PORCH_EXT_W = TERM_W + 16
PORCH_EXT_D = TERM_D + 6 + PORCH_FREE_SPACE 

# -- Labels --
MAIN_LABEL_1 = "PID Temp"
MAIN_LABEL_2 = "Controller"
LABEL_LEFT, LABEL_RIGHT = "+", "-"

# -- Cable Management --
CABLE_DIA, CABLE_SPACING = 8.0, 22.0
BOSS_SIZE, ANCHOR_HEIGHT = 10.0, 8.0
ANCHOR_HOLE_W, ANCHOR_HOLE_H = 5.0, 3.5   

# -- Derived Dimensions --
INTERNAL_W = SIDE_MARGIN + PID_BEZEL_W + GAP_BETWEEN_PID_SSR + SSR_W + SIDE_MARGIN
LEN_LEFT, LEN_RIGHT = PID_BODY_D, GAP_SSR_FRONT + SSR_L
MAX_COMPONENT_L = max(LEN_LEFT, LEN_RIGHT)
INTERNAL_L = MAX_COMPONENT_L + GAP_REAR_WIRING 
HEIGHT_SSR_STACK = SSR_H + 5
HEIGHT_PID_STACK = PID_FLOOR_CLEARANCE + PID_BODY_H + UK_SOCKET_BACK_D + 10
INTERNAL_H = max(HEIGHT_SSR_STACK, HEIGHT_PID_STACK)

BOX_W = INTERNAL_W + 2 * WALL_THICKNESS
BOX_L = INTERNAL_L + 2 * WALL_THICKNESS
BOX_H = INTERNAL_H + WALL_THICKNESS 

# -- Positions --
front_inner_y = -INTERNAL_L/2
pid_center_x = -INTERNAL_W/2 + SIDE_MARGIN + PID_BEZEL_W/2
pid_center_y = front_inner_y + PID_BODY_D/2
ssr_center_x = INTERNAL_W/2 - SIDE_MARGIN - SSR_W/2
ssr_center_y = front_inner_y + GAP_SSR_FRONT + SSR_L/2
porch_x = pid_center_x
c14_x, c14_y, c14_z = ssr_center_x, INTERNAL_L/2 + WALL_THICKNESS/2, INTERNAL_H / 2
mains_boss_x = pid_center_x 
mains_boss_y = (pid_center_y + PID_BODY_D/2 + INTERNAL_L/2) / 2
mains_blk_z = WALL_THICKNESS + MAINS_BLK_H/2
earth_boss_x = ssr_center_x - SSR_W/2 - 10 
earth_boss_y = INTERNAL_L/2 - 15

# ==============================================================================
# 2. PRE-BUILD COMPONENTS
# ==============================================================================
with BuildPart() as master_anchor:
    Box(12, 15, ANCHOR_HEIGHT, align=(Align.CENTER, Align.MAX, Align.MIN))
    with Locations((0, -7.5, ANCHOR_HEIGHT/2)): 
            Box(20, ANCHOR_HOLE_W, ANCHOR_HOLE_H, mode=Mode.SUBTRACT)
    entry_edges = master_anchor.edges().filter_by(
        lambda e: abs(e.center().X) > 5.9 and 2.0 < e.center().Z < 6.0
    )
    fillet(entry_edges, radius=0.5)

# ==============================================================================
# 3. GHOSTS (Visualization)
# ==============================================================================
pid_pos_z = WALL_THICKNESS + PID_FLOOR_CLEARANCE + PID_BODY_H/2
pid_body_ghost = Location((pid_center_x, pid_center_y, pid_pos_z)) * Box(PID_BODY_W, PID_BODY_D, PID_BODY_H)
ssr_pos_z = WALL_THICKNESS + SSR_H/2
ssr_ghost = Location((ssr_center_x, ssr_center_y, ssr_pos_z)) * Box(SSR_W, SSR_L, SSR_H)
mains_ghost = Location((mains_boss_x, mains_boss_y, mains_blk_z)) * Box(MAINS_BLK_W, MAINS_BLK_D, MAINS_BLK_H)
c14_ghost = Location((c14_x, c14_y, c14_z)) * Box(C14_BODY_W, 20, C14_BODY_H)
socket_ghost = Location((pid_center_x, 0, BOX_H+5)) * Box(UK_SOCKET_SIZE, UK_SOCKET_SIZE, 10) # Simple plate for viz

# ==============================================================================
# 4. BUILD CASE BODY
# ==============================================================================

with BuildPart() as body:
    # A. Hull
    with BuildSketch():
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=BOX_H)
    
    # NEW: Bottom Chamfer (Elephant Foot Compensation & Comfort)
    bottom_edges = body.edges().filter_by(Axis.Z).sort_by(Axis.Z)[0]
    chamfer(bottom_edges, length=1.0)

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
    if (SSR_SCREW_DEPTH - WALL_THICKNESS) > 0:
        with BuildSketch(Plane.XY.offset(WALL_THICKNESS)): 
            with Locations((ssr_center_x, ssr_center_y)):
                Rectangle(SSR_W + 4, SSR_L + 4)
        extrude(amount=SSR_SCREW_DEPTH - WALL_THICKNESS)

    with Locations((ssr_center_x, ssr_center_y, WALL_THICKNESS + max(0, SSR_SCREW_DEPTH - WALL_THICKNESS))): 
        with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
            Cylinder(radius=1.4, height=SSR_SCREW_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Mains Boss
    with Locations((mains_boss_x, mains_boss_y, WALL_THICKNESS)):
        Cylinder(radius=5.0, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0,0,6)):
            Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Earth Boss
    with Locations((earth_boss_x, earth_boss_y, WALL_THICKNESS)):
        Cylinder(radius=5.0, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0,0,6)):
            Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # G. Divider Wall (With Reinforced Base)
    divider_y_start = pid_center_y + PID_BODY_D/2 
    divider_len = (INTERNAL_L/2) - divider_y_start - 5 
    divider_y_pos = divider_y_start + divider_len/2
    
    with Locations((0, divider_y_pos, WALL_THICKNESS)):
        # Create Wall
        with BuildPart() as divider:
            Box(2.0, divider_len, 25.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Add fillets to the base edges for strength
            # Filter edges at Z=0 (local)
            base_edges = divider.edges().filter_by(lambda e: e.center().Z == 0)
            fillet(base_edges, radius=2.0)
        add(divider.part)

    # H. Rear Porch
    porch_floor_z = max(WALL_THICKNESS, TERM_SCREW_DEPTH) 
    porch_center_y = BOX_L/2 + PORCH_EXT_D/2 - 2
    with BuildSketch(Plane.XY): 
        with Locations((porch_x, porch_center_y)): Rectangle(PORCH_EXT_W, PORCH_EXT_D) 
    extrude(amount=porch_floor_z)
    with BuildSketch(Plane.XY.offset(porch_floor_z)):
        with Locations((porch_x, porch_center_y)):
            Rectangle(PORCH_EXT_W, PORCH_EXT_D) 
            with Locations((0, -2)): Rectangle(PORCH_EXT_W - 2*4, PORCH_EXT_D + 4, mode=Mode.SUBTRACT) 
    extrude(amount=PORCH_WALL_H)
    
    # Porch Details
    with Locations((porch_x, porch_center_y, porch_floor_z + PORCH_WALL_H)):
        with GridLocations(PORCH_EXT_W - 8, 0, 2, 1): 
            Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((porch_x, BOX_L/2 + TERM_D/2, porch_floor_z)):
        with GridLocations(TERM_MOUNT_X, TERM_MOUNT_Y, 2, 2):
            Cylinder(radius=1.4, height=TERM_SCREW_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((porch_x, BOX_L/2 + PORCH_EXT_D, porch_floor_z + PORCH_WALL_H)):
        Box(TERM_W, 10, 10, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # I. Cutouts
    with Locations((porch_x, BOX_L/2, WALL_THICKNESS + TERM_H/2)):
        Box(TERM_W - 4, WALL_THICKNESS*4, TERM_H, mode=Mode.SUBTRACT)
    with Locations((pid_center_x, -BOX_L/2, pid_pos_z)):
        Box(PID_BODY_W + FIT_TOLERANCE, WALL_THICKNESS*4, PID_BODY_H + FIT_TOLERANCE, mode=Mode.SUBTRACT)
    
    # C14 Inlet
    c14_inner_y = BOX_L/2 - WALL_THICKNESS
    with Locations((c14_x, c14_inner_y, c14_z)):
        with Locations((C14_SCREW_PITCH/2, 0, 0), (-C14_SCREW_PITCH/2, 0, 0)):
            Cylinder(radius=4.0, height=C14_BOSS_DEPTH, rotation=(90,0,0), align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((c14_x, BOX_L/2, c14_z)):
        Box(C14_BODY_W, WALL_THICKNESS*4, C14_BODY_H, mode=Mode.SUBTRACT)
        with Locations((C14_SCREW_PITCH/2, 0, 0), (-C14_SCREW_PITCH/2, 0, 0)):
             Cylinder(radius=SCREW_M3_CLEARANCE/2, height=WALL_THICKNESS*2, rotation=(90,0,0), mode=Mode.SUBTRACT)
    with Locations((c14_x, c14_inner_y, c14_z)):
        with Locations((C14_SCREW_PITCH/2, 0, 0), (-C14_SCREW_PITCH/2, 0, 0)):
             Cylinder(radius=INSERT_M3_HOLE_DIA/2, height=C14_BOSS_DEPTH, rotation=(90,0,0), align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

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

    # K. Cable & Vents
    shelf_z = WALL_THICKNESS + ANCHOR_HEIGHT
    with Locations((cable_1_x, BOX_L/2, shelf_z), (cable_2_x, BOX_L/2, shelf_z)):
        Box(CABLE_DIA, WALL_THICKNESS*4, CABLE_DIA, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        with Locations((0, 0, CABLE_DIA)):
            Cylinder(radius=CABLE_DIA/2, height=WALL_THICKNESS*4, rotation=(90, 0, 0), mode=Mode.SUBTRACT)
    with Locations((cable_1_x, BOX_L/2 - WALL_THICKNESS, WALL_THICKNESS), (cable_2_x, BOX_L/2 - WALL_THICKNESS, WALL_THICKNESS)):
        add(master_anchor.part)

    vent_z = WALL_THICKNESS + 6.0 
    with Locations((BOX_W/2, ssr_center_y, vent_z)):
        with GridLocations(0, 10, 1, 4):
            Box(WALL_THICKNESS*4, 6, 4, rotation=(0, 0, 0), mode=Mode.SUBTRACT)

# ==============================================================================
# 5. BUILD LID
# ==============================================================================
with BuildPart() as lid:
    with BuildSketch():
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=LID_THICKNESS)
    
    # Rebate
    with BuildSketch(faces().sort_by(Axis.Z)[0]): 
        Rectangle(INTERNAL_W - 0.8, INTERNAL_L - 0.8) 
        with Locations(
            (INTERNAL_W/2 - BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (INTERNAL_W/2 - BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2)
        ):
            Circle(radius=BOSS_SIZE/2 + 0.4, mode=Mode.SUBTRACT)
    extrude(amount=2.0)

    # Socket Bosses
    socket_x, socket_y = pid_center_x, 0
    with BuildSketch(faces().sort_by(Axis.Z)[0]): 
        with Locations((socket_x, socket_y)):
            with Locations((0, UK_SOCKET_MOUNT_PITCH/2), (0, -UK_SOCKET_MOUNT_PITCH/2)):
                Circle(radius=SOCKET_BOSS_DIA/2)
    extrude(amount=LID_THICKNESS + SOCKET_BOSS_DEPTH)

    # Holes & Cutouts
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

    with Locations((socket_x, socket_y, LID_THICKNESS)):
        Box(UK_SOCKET_BACK_W, UK_SOCKET_BACK_W, 30, mode=Mode.SUBTRACT)
        with Locations((0, UK_SOCKET_MOUNT_PITCH/2), (0, -UK_SOCKET_MOUNT_PITCH/2)):
             Cylinder(radius=INSERT_M35_HOLE_DIA/2, height=30, mode=Mode.SUBTRACT)

    # DEBOSSED Label (Engraved - Good for Face Down printing)
    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((pid_center_x, -50)):
             with Locations((0, 9)): 
                 Text(MAIN_LABEL_1, font_size=10, font_style=FontStyle.BOLD, rotation=0, align=(Align.CENTER, Align.CENTER))
             with Locations((0, -9)): 
                 Text(MAIN_LABEL_2, font_size=10, font_style=FontStyle.BOLD, rotation=0, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-0.6, mode=Mode.SUBTRACT) # Cut IN 0.6mm

# ==============================================================================
# 6. BUILD TERMINAL COVER
# ==============================================================================
COVER_DEPTH = PORCH_EXT_D - 2.0 - 1.0 
with BuildPart() as term_cover:
    with BuildSketch():
        Rectangle(PORCH_EXT_W, COVER_DEPTH)
        fillet(vertices(), radius=2.0)
    extrude(amount=LID_THICKNESS) 
    
    p_cen = BOX_L/2 + PORCH_EXT_D/2 - 2
    y_hole = (p_cen - (BOX_L/2 + 1.0 + BOX_L/2 + PORCH_EXT_D - 2) / 2) - 3.0

    with Locations((0, y_hole, LID_THICKNESS)): 
        with GridLocations(PORCH_EXT_W - 8, 0, 2, 1):
             CounterBoreHole(radius=SCREW_M3_CLEARANCE/2, counter_bore_radius=3.1, counter_bore_depth=2.0)

    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((0, y_hole)):
            with Locations((-12, 0)): Text(LABEL_LEFT, font_size=10, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER))
            with Locations((12, 0)): Text(LABEL_RIGHT, font_size=10, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER))
    extrude(amount=0.6) # Emboss (Print Face Up)
    with Locations((0, COVER_DEPTH/2, 0)):
        Cylinder(radius=3, height=LID_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

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
cover_viz_y = (BOX_L/2 + 1.0) + COVER_DEPTH/2
term_cover_moved = term_cover.part.move(Location((porch_x, cover_viz_y, porch_floor_z + PORCH_WALL_H)))
washer_moved = washer.part.move(Location((0, BOX_L/2 + 20, 0))) 

assembly = Compound(children=[body.part, lid_moved, term_cover_moved, washer_moved, pid_ghost_assembly, ssr_ghost, term_ghost, mains_ghost, c14_ghost, socket_ghost])
print(f"Case Dimensions: {BOX_W:.1f} x {BOX_L:.1f} x {BOX_H:.1f} mm")

export_stl(body.part, "pid_case_body.stl")
export_stl(lid.part, "pid_lid.stl")
export_stl(term_cover.part, "pid_term_cover.stl")
export_stl(washer.part, "pid_washer.stl")

show_object(body, name="Body", options={"alpha": 1.0, "color": (0.8, 0.8, 0.8)})
show_object(lid_moved, name="Lid", options={"alpha": 0.5, "color": (0.6, 0.6, 1.0)})
show_object(term_cover_moved, name="Safety Cover", options={"alpha": 0.8, "color": (1.0, 0.6, 0.0)})
show_object(washer_moved, name="Washer", options={"alpha": 1.0, "color": (0.2, 0.2, 0.2)})
show_object(pid_ghost_assembly, name="PID Ghost", options={"alpha": 0.3, "color": (1, 0, 0)})
show_object(ssr_ghost, name="SSR Ghost", options={"alpha": 0.3, "color": (0, 1, 0)})
show_object(term_ghost, name="Term Ghost", options={"alpha": 0.3, "color": (0, 0, 1)})
show_object(mains_ghost, name="Mains Block Ghost", options={"alpha": 0.3, "color": (1, 1, 0)})