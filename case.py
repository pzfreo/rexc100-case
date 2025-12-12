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

# -- Internal Layout & Spacing --
SIDE_MARGIN = 20.0       
GAP_BETWEEN_PID_SSR = 20.0 
GAP_SSR_FRONT = 20.0     
GAP_REAR_WIRING = 50.0   

# -- REX-C100 PID --
PID_BODY_W = 44.0
PID_BODY_H = 44.0
PID_BODY_D = 80.0
PID_BEZEL_W = 48.0
PID_BEZEL_H = 48.0
PID_BEZEL_D = 9.0
PID_FLOOR_CLEARANCE = 12.0

# -- SSR + Heatsink --
SSR_W = 50.0
SSR_L = 80.0
SSR_H = 73.0
SSR_MOUNT_SPACING = 72.0
SSR_SCREW_DEPTH = 7.0

# -- External Terminal Block --
TERM_W = 36.0
TERM_D = 21.0
TERM_H = 13.0
TERM_MOUNT_X = 28.0
TERM_MOUNT_Y = 8.0
TERM_SCREW_DEPTH = 7.0

# -- INTERNAL Mains Terminal Block --
MAINS_BLK_W = 20.0
MAINS_BLK_D = 15.0
MAINS_BLK_H = 15.0

# -- Porch Settings --
PORCH_FREE_SPACE = 5.0   
PORCH_WALL_H = TERM_H + 5
PORCH_EXT_W = TERM_W + 16
PORCH_EXT_D = TERM_D + 6 + PORCH_FREE_SPACE 

# -- Labels --
MAIN_LABEL_1 = "PID Temp"
MAIN_LABEL_2 = "Controller"
LABEL_LEFT = "+"
LABEL_RIGHT = "-"

# -- Cable Management --
CABLE_DIA = 8.0
CABLE_SPACING = 22.0  
BOSS_SIZE = 10.0      
ANCHOR_HEIGHT = 8.0
ANCHOR_HOLE_W = 5.0   
ANCHOR_HOLE_H = 3.5   

# -- Derived Dimensions --
INTERNAL_W = SIDE_MARGIN + PID_BEZEL_W + GAP_BETWEEN_PID_SSR + SSR_W + SIDE_MARGIN

LEN_LEFT = PID_BODY_D
LEN_RIGHT = GAP_SSR_FRONT + SSR_L
MAX_COMPONENT_L = max(LEN_LEFT, LEN_RIGHT)
INTERNAL_L = MAX_COMPONENT_L + GAP_REAR_WIRING 

INTERNAL_H = max(SSR_H + 5, PID_FLOOR_CLEARANCE + PID_BODY_H + 5)

BOX_W = INTERNAL_W + 2 * WALL_THICKNESS
BOX_L = INTERNAL_L + 2 * WALL_THICKNESS
BOX_H = INTERNAL_H + WALL_THICKNESS 

# -- Component Positions --
front_inner_y = -INTERNAL_L/2

# PID (Left)
pid_center_x = -INTERNAL_W/2 + SIDE_MARGIN + PID_BEZEL_W/2
pid_center_y = front_inner_y + PID_BODY_D/2

# SSR (Right)
ssr_center_x = INTERNAL_W/2 - SIDE_MARGIN - SSR_W/2
ssr_center_y = front_inner_y + GAP_SSR_FRONT + SSR_L/2

# Rear Porch (Left)
porch_x = pid_center_x

# Cable Entries (Right Rear)
cables_center_x = ssr_center_x
cable_1_x = cables_center_x - CABLE_SPACING/2
cable_2_x = cables_center_x + CABLE_SPACING/2

# Mains Block (Moved to LEFT Side, behind PID)
# This uses the dead space behind the controller
mains_boss_x = pid_center_x 
# Position it midway between PID back and Rear Wall
pid_back_y = pid_center_y + PID_BODY_D/2
rear_wall_y = INTERNAL_L/2
mains_boss_y = (pid_back_y + rear_wall_y) / 2
mains_blk_z = WALL_THICKNESS + MAINS_BLK_H/2

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
# 3. GHOSTS
# ==============================================================================
pid_pos_z = WALL_THICKNESS + PID_FLOOR_CLEARANCE + PID_BODY_H/2
pid_body_ghost = Box(PID_BODY_W, PID_BODY_D, PID_BODY_H)
pid_body_ghost = Location((pid_center_x, pid_center_y, pid_pos_z)) * pid_body_ghost

bezel_pos_y = front_inner_y - PID_BEZEL_D/2
pid_bezel_ghost = Box(PID_BEZEL_W, PID_BEZEL_D, PID_BEZEL_H)
pid_bezel_ghost = Location((pid_center_x, bezel_pos_y, pid_pos_z)) * pid_bezel_ghost
pid_ghost_assembly = Compound(children=[pid_body_ghost, pid_bezel_ghost])

ssr_pos_z = WALL_THICKNESS + SSR_H/2
ssr_ghost = Box(SSR_W, SSR_L, SSR_H)
ssr_ghost = Location((ssr_center_x, ssr_center_y, ssr_pos_z)) * ssr_ghost

term_center_y = BOX_L/2 + TERM_D/2 
term_pos_z = WALL_THICKNESS + TERM_H/2
term_ghost = Box(TERM_W, TERM_D, TERM_H)
term_ghost = Location((porch_x, term_center_y, term_pos_z)) * term_ghost

mains_ghost = Box(MAINS_BLK_W, MAINS_BLK_D, MAINS_BLK_H)
mains_ghost = Location((mains_boss_x, mains_boss_y, mains_blk_z)) * mains_ghost

# ==============================================================================
# 4. BUILD CASE BODY
# ==============================================================================

with BuildPart() as body:
    # A. Hull
    with BuildSketch():
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=BOX_H)
    
    # B. Hollow
    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        Rectangle(BOX_W - 2*WALL_THICKNESS, BOX_L - 2*WALL_THICKNESS)
        if FILLET_R - WALL_THICKNESS > 0:
            fillet(vertices(), radius=FILLET_R - WALL_THICKNESS)
    extrude(amount=-BOX_H + WALL_THICKNESS, mode=Mode.SUBTRACT)

    # C. SSR Platform
    platform_h = max(WALL_THICKNESS, SSR_SCREW_DEPTH) - WALL_THICKNESS
    if platform_h > 0:
        with BuildSketch(Plane.XY.offset(WALL_THICKNESS)): 
            with Locations((ssr_center_x, ssr_center_y)):
                Rectangle(SSR_W + 4, SSR_L + 4)
        extrude(amount=platform_h)

    # D. SSR Holes
    hole_top_z = WALL_THICKNESS + platform_h
    with Locations((ssr_center_x, ssr_center_y, hole_top_z)): 
        with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
            Cylinder(radius=1.4, height=SSR_SCREW_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # NEW: Mains Block Mounting Boss (Moved to LEFT)
    with Locations((mains_boss_x, mains_boss_y, WALL_THICKNESS)):
        Cylinder(radius=4.0, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0,0,6)):
            Cylinder(radius=1.4, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # E. Rear Porch
    porch_floor_z = max(WALL_THICKNESS, TERM_SCREW_DEPTH) 
    porch_center_y = BOX_L/2 + PORCH_EXT_D/2 - 2

    # 1. Floor
    with BuildSketch(Plane.XY): 
        with Locations((porch_x, porch_center_y)): 
            Rectangle(PORCH_EXT_W, PORCH_EXT_D) 
    extrude(amount=porch_floor_z)

    # 2. Walls
    with BuildSketch(Plane.XY.offset(porch_floor_z)):
        with Locations((porch_x, porch_center_y)):
            Rectangle(PORCH_EXT_W, PORCH_EXT_D) 
            with Locations((0, -2)): 
                Rectangle(PORCH_EXT_W - 2*4, PORCH_EXT_D + 4, mode=Mode.SUBTRACT) 
    extrude(amount=PORCH_WALL_H)

    # 3. Terminal Holes
    with Locations((porch_x, BOX_L/2 + TERM_D/2, porch_floor_z)):
        with GridLocations(TERM_MOUNT_X, TERM_MOUNT_Y, 2, 2):
            Cylinder(radius=1.4, height=TERM_SCREW_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # 4. Cover Screw Holes
    porch_top_z = porch_floor_z + PORCH_WALL_H
    with Locations((porch_x, porch_center_y, porch_top_z)):
        with GridLocations(PORCH_EXT_W - 8, 0, 2, 1): 
            Cylinder(radius=1.4, height=10, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # 5. External Wire Exit
    with Locations((porch_x, BOX_L/2 + PORCH_EXT_D, porch_floor_z + PORCH_WALL_H)):
        Box(TERM_W, 10, 10, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # F. Internal Wire Pass-through
    with Locations((porch_x, BOX_L/2, WALL_THICKNESS + TERM_H/2)):
        Box(TERM_W - 4, WALL_THICKNESS*4, TERM_H, mode=Mode.SUBTRACT)

    # G. Front Cutout
    with Locations((pid_center_x, -BOX_L/2, pid_pos_z)):
        Box(PID_BODY_W + FIT_TOLERANCE, WALL_THICKNESS*4, PID_BODY_H + FIT_TOLERANCE, mode=Mode.SUBTRACT)

    # H. Cable Entries
    shelf_z = WALL_THICKNESS + ANCHOR_HEIGHT
    with Locations((cable_1_x, BOX_L/2, shelf_z), (cable_2_x, BOX_L/2, shelf_z)):
        Box(CABLE_DIA, WALL_THICKNESS*4, CABLE_DIA, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        with Locations((0, 0, CABLE_DIA)):
            Cylinder(radius=CABLE_DIA/2, height=WALL_THICKNESS*4, rotation=(90, 0, 0), mode=Mode.SUBTRACT)

    # I. Anchors
    with Locations(
        (cable_1_x, BOX_L/2 - WALL_THICKNESS, WALL_THICKNESS),
        (cable_2_x, BOX_L/2 - WALL_THICKNESS, WALL_THICKNESS)
    ):
        add(master_anchor.part)

    # J. Bosses
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
             Cylinder(radius=1.4, height=15, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # K. Side Intake Vents
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
    LID_REBATE_DEPTH = 2.0
    LID_REBATE_TOLERANCE = 0.4
    with BuildSketch(faces().sort_by(Axis.Z)[0]): 
        Rectangle(INTERNAL_W - LID_REBATE_TOLERANCE*2, INTERNAL_L - LID_REBATE_TOLERANCE*2)
        with Locations(
            (INTERNAL_W/2 - BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, INTERNAL_L/2 - BOSS_SIZE/2),
            (INTERNAL_W/2 - BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2),
            (-INTERNAL_W/2 + BOSS_SIZE/2, -INTERNAL_L/2 + BOSS_SIZE/2)
        ):
            Circle(radius=BOSS_SIZE/2 + LID_REBATE_TOLERANCE, mode=Mode.SUBTRACT)
    extrude(amount=LID_REBATE_DEPTH)

    hole_offset_x = INTERNAL_W/2 - BOSS_SIZE/2
    hole_offset_y = INTERNAL_L/2 - BOSS_SIZE/2
    
    with Locations(
        (hole_offset_x, hole_offset_y, LID_THICKNESS), (-hole_offset_x, hole_offset_y, LID_THICKNESS),
        (hole_offset_x, -hole_offset_y, LID_THICKNESS), (-hole_offset_x, -hole_offset_y, LID_THICKNESS)
    ):
        CounterBoreHole(radius=1.7, counter_bore_radius=3.1, counter_bore_depth=2.0)

    # Ventilation (Over SSR)
    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((ssr_center_x, ssr_center_y)):
            with GridLocations(x_spacing=6, y_spacing=0, x_count=int(SSR_W/6), y_count=1):
                SlotOverall(width=SSR_L - 10, height=3, rotation=90)
    extrude(amount=-LID_THICKNESS - LID_REBATE_DEPTH, mode=Mode.SUBTRACT)

    # Embossed Label (Centered over PID)
    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((pid_center_x, ssr_center_y)):
             with Locations((0, 9)): 
                 Text(MAIN_LABEL_1, font_size=12, font_style=FontStyle.BOLD, rotation=0, align=(Align.CENTER, Align.CENTER))
             with Locations((0, -9)): 
                 Text(MAIN_LABEL_2, font_size=12, font_style=FontStyle.BOLD, rotation=0, align=(Align.CENTER, Align.CENTER))
    extrude(amount=0.6)

# ==============================================================================
# 6. BUILD TERMINAL COVER
# ==============================================================================

GAP_TO_WALL = 1.0  
COVER_DEPTH = PORCH_EXT_D - 2.0 - GAP_TO_WALL 

with BuildPart() as term_cover:
    
    with BuildSketch():
        Rectangle(PORCH_EXT_W, COVER_DEPTH)
        fillet(vertices(), radius=2.0)
    extrude(amount=LID_THICKNESS) 
    
    p_cen = BOX_L/2 + PORCH_EXT_D/2 - 2
    c_start = BOX_L/2 + GAP_TO_WALL
    c_end = BOX_L/2 + PORCH_EXT_D - 2
    c_cen = (c_start + c_end) / 2
    y_shift = p_cen - c_cen
    
    ASYMMETRY_OFFSET = 3.0
    y_hole_pos = y_shift - ASYMMETRY_OFFSET

    # Screw Holes
    with Locations((0, y_hole_pos, LID_THICKNESS)): 
        with GridLocations(PORCH_EXT_W - 8, 0, 2, 1):
             CounterBoreHole(radius=1.7, counter_bore_radius=3.1, counter_bore_depth=2.0)

    # Polarity Labels
    with BuildSketch(faces().sort_by(Axis.Z)[-1]):
        with Locations((0, y_hole_pos)):
            with Locations((-12, 0)): 
                Text(LABEL_LEFT, font_size=10, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER))
            with Locations((12, 0)): 
                Text(LABEL_RIGHT, font_size=10, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-0.6, mode=Mode.SUBTRACT)
    
    # Visual Notch
    with Locations((0, COVER_DEPTH/2, 0)):
        Cylinder(radius=3, height=LID_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

# ==============================================================================
# 7. BUILD WASHER
# ==============================================================================
with BuildPart() as washer:
    Cylinder(radius=4.0, height=2.0)
    Hole(radius=1.75)

# ==============================================================================
# 8. EXPORT & VISUALIZE
# ==============================================================================

lid_moved = lid.part.move(Location((0,0, BOX_H + 5)))
cover_viz_y = (BOX_L/2 + GAP_TO_WALL) + COVER_DEPTH/2
term_cover_moved = term_cover.part.move(Location((porch_x, cover_viz_y, porch_floor_z + PORCH_WALL_H)))
washer_moved = washer.part.move(Location((0, BOX_L/2 + 20, 0))) 

assembly = Compound(children=[
    body.part, 
    lid_moved, 
    term_cover_moved, 
    washer_moved,
    pid_ghost_assembly, 
    ssr_ghost, 
    term_ghost,
    mains_ghost
])

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