from build123d import *
from ocp_vscode import show, show_object, set_port, set_defaults, Camera

# ==============================================================================
# 1. CONFIGURATION SWITCHES
# ==============================================================================
# Configure which locations use heat set inserts vs direct screw tapping
# True = Heat set inserts (larger holes + entry chamfers for easy installation)
# False = Direct screw tap (smaller holes for tapping threads directly)
#
# TOTAL: 15 threaded holes in this design
#   - 2x SSR mounting (M3)
#   - 4x Terminal block (M3)
#   - 4x Corner posts (M3) - structural, holds shell to base
#   - 2x UK socket (M3.5)
#   - 2x C14 inlet (M3)
#   - 1x PID clamp (M3)

USE_INSERTS_SSR = True          # SSR mounting (2x M3 on base)
USE_INSERTS_TERMINAL = False     # Terminal block (4x M3 on base)
USE_INSERTS_CORNERS = True      # Corner posts (4x M3 shell-to-base) - RECOMMENDED for inserts
USE_INSERTS_SOCKET = True       # UK socket mounting (2x M3.5 on roof)
USE_INSERTS_C14 = True          # C14 inlet (2x M3 on back wall)
USE_INSERTS_PID_CLAMP = True    # PID clamp screw (1x M3 on front wall)

# Quick presets (uncomment one to use)
# ALL INSERTS: USE_INSERTS_SSR = USE_INSERTS_TERMINAL = USE_INSERTS_CORNERS = USE_INSERTS_SOCKET = USE_INSERTS_C14 = USE_INSERTS_PID_CLAMP = True
# ALL SCREWS: USE_INSERTS_SSR = USE_INSERTS_TERMINAL = USE_INSERTS_CORNERS = USE_INSERTS_SOCKET = USE_INSERTS_C14 = USE_INSERTS_PID_CLAMP = False
# HYBRID (Structural only): USE_INSERTS_CORNERS = True 

# ==============================================================================
# 2. PARAMETERS
# ==============================================================================

# -- Global Settings --
WALL_THICKNESS = 3.0
ROOF_THICKNESS = 3.0 
BASE_THICKNESS = 5.0 
FILLET_R = 4.0       
FIT_TOLERANCE = 0.3  

# -- Feet Settings --
FOOT_DIA = 12.0       
FOOT_DEPTH = 2.0      
FOOT_OFFSET = 15.0    

# -- Fasteners Logic --
SCREW_M3_CLEARANCE = 3.4      
M3_HEAD_DIA = 6.0             
M3_HEAD_H = 3.0               

# -- Fastener Sizes (per location) --
# M3 Heat set insert: 4.0mm OD x 5.7mm L (standard)
# M3.5 Heat set insert: 4.6mm OD x 6.0mm L (standard)
THREAD_M3_INSERT = 4.2         # Hole for M3 heat set insert
THREAD_M35_INSERT = 4.8        # Hole for M3.5 heat set insert
THREAD_M3_TAP = 2.8            # Hole for direct M3 screw tapping
THREAD_M35_TAP = 2.8           # Hole for direct M3.5 screw tapping

# Chamfer for heat set insert entry (makes installation MUCH easier!)
# - Guides insert in straight
# - Prevents surface mushrooming
# - Reduces installation force
INSERT_CHAMFER_M3_DIA = 5.5    # Slightly larger than M3 insert OD
INSERT_CHAMFER_M35_DIA = 5.8   # Slightly larger than M3.5 insert OD
INSERT_CHAMFER_DEPTH = 0.8     # ~45° chamfer depth (0.8mm gives ~45° angle)      

# -- Components --
# Standard 1/16 DIN Inkbird Sizes
PID_BODY_W, PID_BODY_H = 45.0, 45.0   
PID_BODY_D = 100.0                    
PID_BEZEL_W, PID_BEZEL_H = 48.0, 48.0 
PID_FLOOR_CLEARANCE = 12.0 

SSR_W, SSR_L, SSR_H = 50.0, 80.0, 73.0
SSR_MOUNT_SPACING = 72.0
SSR_PLATFORM_HEIGHT = 4.0 

UK_SOCKET_CUTOUT_SIZE = 73.0 
UK_SOCKET_MOUNT_PITCH = 60.3
SOCKET_BOSS_DIA = 12.0
SOCKET_BOSS_DEPTH = 8.0 

C14_BODY_W, C14_BODY_H = 28.0, 48.0
C14_SCREW_PITCH = 40.0
C14_BOSS_DEPTH = 10.0
C14_GHOST_DEPTH = 30.0 + 15.0 

TERM_W, TERM_D, TERM_H = 36.0, 21.0, 13.0
TERM_MOUNT_X, TERM_MOUNT_Y = 28.0, 8.0
TERM_BOSS_HEIGHT = 5.0

# -- Layout --
SIDE_MARGIN = 20.0
INTERNAL_L = 155.0 
INTERNAL_H = 100.0 

INTERNAL_W = SIDE_MARGIN + PID_BEZEL_W + 20 + SSR_W + SIDE_MARGIN

BOX_W = INTERNAL_W + 2 * WALL_THICKNESS
BOX_L = INTERNAL_L + 2 * WALL_THICKNESS
BOX_H = INTERNAL_H + ROOF_THICKNESS

# ==============================================================================
# 3. POSITIONING
# ==============================================================================
pid_x = -INTERNAL_W/2 + SIDE_MARGIN + PID_BODY_W/2
pid_y = -INTERNAL_L/2 + PID_BODY_D/2 
# PID Position: Starts 20mm up from Z=0
pid_z_start = 20.0 
pid_z_end = pid_z_start + PID_BODY_H + FIT_TOLERANCE 
pid_z_center = pid_z_start + (PID_BODY_H + FIT_TOLERANCE)/2

ssr_x = INTERNAL_W/2 - SIDE_MARGIN - SSR_W/2
ssr_y = -INTERNAL_L/2 + 20 + SSR_L/2
ssr_z = BASE_THICKNESS + SSR_PLATFORM_HEIGHT

socket_x = pid_x + 5.0
socket_y = 10.0 

c14_x = ssr_x 
c14_y = BOX_L/2 
c14_z = 45.0 

term_x = pid_x
term_y = INTERNAL_L/2 - 40.0

# ==============================================================================
# 4. BUILD BASE PLATE
# ==============================================================================
with BuildPart() as base:
    # Main Plate
    with BuildSketch():
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=BASE_THICKNESS)
    
    # SSR Mounts
    with Locations((ssr_x, ssr_y, BASE_THICKNESS)):
        with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
            Box(SSR_W, 12.0, SSR_PLATFORM_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # SSR Base Grill
    with BuildSketch(Plane.XY):
        with Locations((ssr_x, ssr_y)):
            with GridLocations(6, 0, 6, 1):
                SlotOverall(30, 3, rotation=90)
    extrude(amount=BASE_THICKNESS, mode=Mode.SUBTRACT)

    # SSR Holes
    ssr_boss_top = BASE_THICKNESS + SSR_PLATFORM_HEIGHT
    ssr_hole_dia = THREAD_M3_INSERT if USE_INSERTS_SSR else THREAD_M3_TAP
    with Locations((ssr_x, ssr_y, 0)):
        with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
            Cylinder(radius=ssr_hole_dia/2, height=ssr_boss_top + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Chamfer for heat set insert entry (from top of boss)
    if USE_INSERTS_SSR:
        with Locations((ssr_x, ssr_y, ssr_boss_top)):
            with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
                Cylinder(radius=INSERT_CHAMFER_M3_DIA/2, height=INSERT_CHAMFER_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Terminal Block Platform
    with Locations((term_x, term_y, BASE_THICKNESS)):
        Box(TERM_W + 4, TERM_D + 4, TERM_BOSS_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
    # Terminal Block Holes
    term_boss_top = BASE_THICKNESS + TERM_BOSS_HEIGHT
    term_hole_dia = THREAD_M3_INSERT if USE_INSERTS_TERMINAL else THREAD_M3_TAP
    with Locations((term_x, term_y, 0)):
        with GridLocations(TERM_MOUNT_X, TERM_MOUNT_Y, 2, 2):
            Cylinder(radius=term_hole_dia/2, height=term_boss_top + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Chamfer for heat set insert entry (from top of boss)
    if USE_INSERTS_TERMINAL:
        with Locations((term_x, term_y, term_boss_top)):
            with GridLocations(TERM_MOUNT_X, TERM_MOUNT_Y, 2, 2):
                Cylinder(radius=INSERT_CHAMFER_M3_DIA/2, height=INSERT_CHAMFER_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Labyrinth Strain Relief
    lab_y = INTERNAL_L/2 - 8.0 
    with Locations((term_x, lab_y, BASE_THICKNESS)):
        Cylinder(radius=2.5, height=12, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-7, -5), (7, -5)):
            Cylinder(radius=2.5, height=12, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Feet Indents
    with BuildSketch(Plane.XY):
        with Locations(
            (BOX_W/2 - FOOT_OFFSET, BOX_L/2 - FOOT_OFFSET), (-BOX_W/2 + FOOT_OFFSET, BOX_L/2 - FOOT_OFFSET),
            (BOX_W/2 - FOOT_OFFSET, -BOX_L/2 + FOOT_OFFSET), (-BOX_W/2 + FOOT_OFFSET, -BOX_L/2 + FOOT_OFFSET)
        ):
             Circle(radius=FOOT_DIA/2)
    extrude(amount=FOOT_DEPTH, mode=Mode.SUBTRACT)

    # Corner Screw Holes
    corner_off_x = BOX_W/2 - 6.0
    corner_off_y = BOX_L/2 - 6.0
    with Locations(
        (corner_off_x, corner_off_y), (-corner_off_x, corner_off_y),
        (corner_off_x, -corner_off_y), (-corner_off_x, -corner_off_y)
    ):
        Cylinder(radius=SCREW_M3_CLEARANCE/2, height=BASE_THICKNESS + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        Cylinder(radius=M3_HEAD_DIA/2, height=M3_HEAD_H, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)


# ==============================================================================
# 5. BUILD SHELL
# ==============================================================================
with BuildPart() as shell:
    with BuildSketch():
        Rectangle(BOX_W, BOX_L)
        fillet(vertices(), radius=FILLET_R)
    extrude(amount=BOX_H)
    
    with BuildSketch(faces().sort_by(Axis.Z)[0]): 
        Rectangle(BOX_W - 2*WALL_THICKNESS, BOX_L - 2*WALL_THICKNESS)
        fillet(vertices(), radius=FILLET_R - WALL_THICKNESS)
    extrude(amount=-(BOX_H - ROOF_THICKNESS), mode=Mode.SUBTRACT)

    # Corner Posts
    post_h = BOX_H - ROOF_THICKNESS
    corner_hole_dia = THREAD_M3_INSERT if USE_INSERTS_CORNERS else THREAD_M3_TAP
    with Locations((0,0, BOX_H - ROOF_THICKNESS)):
        with Locations(
            (corner_off_x, corner_off_y), (-corner_off_x, corner_off_y),
            (corner_off_x, -corner_off_y), (-corner_off_x, -corner_off_y)
        ):
            Cylinder(radius=5.0, height=post_h, align=(Align.CENTER, Align.CENTER, Align.MAX))
            Cylinder(radius=corner_hole_dia/2, height=post_h, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Chamfer for heat set insert entry (from bottom of posts)
    if USE_INSERTS_CORNERS:
        with Locations((0, 0, 0)):
            with Locations(
                (corner_off_x, corner_off_y), (-corner_off_x, corner_off_y),
                (corner_off_x, -corner_off_y), (-corner_off_x, -corner_off_y)
            ):
                Cylinder(radius=INSERT_CHAMFER_M3_DIA/2, height=INSERT_CHAMFER_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # PID Cutout
    with Locations((pid_x, -BOX_L/2, pid_z_center)):
        Box(PID_BODY_W + FIT_TOLERANCE, WALL_THICKNESS*4, PID_BODY_H + FIT_TOLERANCE, mode=Mode.SUBTRACT)

    # --- FINAL CLAMP LOGIC ---
    # Width=50, Depth=8
    clamp_w, clamp_d = 50.0, 8.0
    # Attached to the inside face of the front wall
    clamp_y_center = -BOX_L/2 + WALL_THICKNESS + clamp_d/2

    # 1. THE BRACE (Anvil)
    # Extends from Top of PID (Z=65) to Roof Inner Surface (Z=97)
    roof_inner_z = BOX_H - ROOF_THICKNESS
    brace_h = roof_inner_z - pid_z_end
    brace_z_center = pid_z_end + brace_h/2
    
    with Locations((pid_x, clamp_y_center, brace_z_center)):
        Box(clamp_w, clamp_d, brace_h, align=(Align.CENTER, Align.CENTER, Align.CENTER))

    # 2. THE CLAMP (Hammer)
    # Extends from Bottom of PID (Z=20) down by 10mm (ends at Z=10)
    # Does not reach Z=0.
    clamp_h = 10.0
    clamp_z_center = pid_z_start - clamp_h/2
    pid_clamp_hole_dia = THREAD_M3_INSERT if USE_INSERTS_PID_CLAMP else THREAD_M3_TAP

    with Locations((pid_x, clamp_y_center, clamp_z_center)):
        # Block
        Box(clamp_w, clamp_d, clamp_h, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        # Threaded Hole (Vertical through center)
        Cylinder(radius=pid_clamp_hole_dia/2, height=clamp_h + 20.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

    # Chamfer for heat set insert entry (from bottom of clamp block - accessible end)
    if USE_INSERTS_PID_CLAMP:
        clamp_bottom_z = clamp_z_center - clamp_h/2  # Z=10
        with Locations((pid_x, clamp_y_center, clamp_bottom_z)):
            Cylinder(radius=INSERT_CHAMFER_M3_DIA/2, height=INSERT_CHAMFER_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)


    # Socket Mounts
    left_screw_x = socket_x - UK_SOCKET_MOUNT_PITCH/2
    right_screw_x = socket_x + UK_SOCKET_MOUNT_PITCH/2
    socket_boss_z = BOX_H - ROOF_THICKNESS
    socket_hole_dia = THREAD_M35_INSERT if USE_INSERTS_SOCKET else THREAD_M35_TAP

    with Locations((0, socket_y, socket_boss_z)):
        with Locations((socket_x, 0)):
            Box(UK_SOCKET_CUTOUT_SIZE, UK_SOCKET_CUTOUT_SIZE, ROOF_THICKNESS*4, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

        with Locations((right_screw_x, 0)):
             Cylinder(radius=SOCKET_BOSS_DIA/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX))
             with Locations((7.5, 0, -SOCKET_BOSS_DEPTH/2)):
                 Box(15.0, SOCKET_BOSS_DIA, SOCKET_BOSS_DEPTH)
             Cylinder(radius=socket_hole_dia/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

        left_wall_x = -BOX_W/2 + WALL_THICKNESS
        bridge_len = abs(left_screw_x - left_wall_x) + 2.0

        with Locations((left_screw_x, 0)):
             Cylinder(radius=SOCKET_BOSS_DIA/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX))
             with Locations((-bridge_len/2, 0, -SOCKET_BOSS_DEPTH/2)):
                 Box(bridge_len, SOCKET_BOSS_DIA, SOCKET_BOSS_DEPTH)
             Cylinder(radius=socket_hole_dia/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Chamfer for heat set insert entry (from bottom of socket bosses - accessible from inside)
    if USE_INSERTS_SOCKET:
        socket_boss_bottom_z = socket_boss_z - SOCKET_BOSS_DEPTH
        with Locations((0, socket_y, socket_boss_bottom_z)):
            with Locations((right_screw_x, 0), (left_screw_x, 0)):
                # M3.5 inserts need slightly larger chamfer
                Cylinder(radius=INSERT_CHAMFER_M35_DIA/2, height=INSERT_CHAMFER_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # C14
    c14_inner_wall_y = BOX_L/2 - WALL_THICKNESS
    with Locations((c14_x, c14_inner_wall_y, 0)): 
        pilaster_h = BOX_H - ROOF_THICKNESS
        screw_x_offset = C14_SCREW_PITCH/2 
        with Locations((screw_x_offset, 0, 0), (-screw_x_offset, 0, 0)):
             Box(12.0, C14_BOSS_DEPTH, pilaster_h, align=(Align.CENTER, Align.MAX, Align.MIN))

    c14_hole_dia = THREAD_M3_INSERT if USE_INSERTS_C14 else THREAD_M3_TAP
    with Locations((c14_x, BOX_L/2, c14_z)):
        Box(C14_BODY_W, WALL_THICKNESS*4, C14_BODY_H, mode=Mode.SUBTRACT)
        with Locations((C14_SCREW_PITCH/2, 0), (-C14_SCREW_PITCH/2, 0)):
             Cylinder(radius=c14_hole_dia/2, height=30.0, rotation=(90,0,0), mode=Mode.SUBTRACT)

    # Chamfer for heat set insert entry (from outside of C14 wall - accessible from exterior)
    if USE_INSERTS_C14:
        with Locations((c14_x, BOX_L/2, c14_z)):
            with Locations((C14_SCREW_PITCH/2, 0), (-C14_SCREW_PITCH/2, 0)):
                # Chamfer extends from outer wall surface inward
                Cylinder(radius=INSERT_CHAMFER_M3_DIA/2, height=INSERT_CHAMFER_DEPTH, rotation=(90,0,0), align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Lid Vents
    with BuildSketch(Plane.XY.offset(BOX_H)):
        with Locations((ssr_x, ssr_y)):
            with GridLocations(6, 0, 6, 1):
                SlotOverall(40, 3, rotation=90)
    extrude(amount=-ROOF_THICKNESS, mode=Mode.SUBTRACT)

    # Mouse Hole
    with Locations((term_x, BOX_L/2, 0)):
        Cylinder(radius=3.5, height=10.0, rotation=(90, 0, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)


# ==============================================================================
# 6. M3 WASHER
# ==============================================================================
# Small ABS washer: 9mm OD, M3 clearance hole, 1.5mm thick
WASHER_OD = 9.0
WASHER_ID = 3.4  # M3 clearance hole
WASHER_THICKNESS = 1.5

with BuildPart() as washer:
    Cylinder(radius=WASHER_OD/2, height=WASHER_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(radius=WASHER_ID/2, height=WASHER_THICKNESS + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)


# ==============================================================================
# 7. EXPORT
# ==============================================================================
print(f"Shell Dimensions: {BOX_W:.1f} x {BOX_L:.1f} x {BOX_H:.1f} mm")
print(f"Washer: {WASHER_OD}mm OD × {WASHER_ID}mm ID × {WASHER_THICKNESS}mm thick (for M3 bolts)")
print("Fastener Configuration:")
print(f"  SSR (2x):        {'INSERTS' if USE_INSERTS_SSR else 'SCREWS'}")
print(f"  Terminal (4x):   {'INSERTS' if USE_INSERTS_TERMINAL else 'SCREWS'}")
print(f"  Corners (4x):    {'INSERTS' if USE_INSERTS_CORNERS else 'SCREWS'}")
print(f"  Socket (2x):     {'INSERTS' if USE_INSERTS_SOCKET else 'SCREWS'}")
print(f"  C14 (2x):        {'INSERTS' if USE_INSERTS_C14 else 'SCREWS'}")
print(f"  PID Clamp (1x):  {'INSERTS' if USE_INSERTS_PID_CLAMP else 'SCREWS'}")

# Summary
insert_count = sum([USE_INSERTS_SSR*2, USE_INSERTS_TERMINAL*4, USE_INSERTS_CORNERS*4, USE_INSERTS_SOCKET*2, USE_INSERTS_C14*2, USE_INSERTS_PID_CLAMP*1])
total_holes = 15
if insert_count == 0:
    print("Mode: ALL DIRECT SCREW TAPPING")
elif insert_count == total_holes:
    print("Mode: ALL HEAT SET INSERTS")
else:
    print(f"Mode: HYBRID ({insert_count}/{total_holes} locations use inserts)")

# Export STLs (For 3D Printing / Slicers)
export_stl(base.part, "pid_inv_base.stl")
export_stl(shell.part, "pid_inv_shell.stl")
export_stl(washer.part, "pid_m3_washer.stl")
print("✅ STL files generated (for 3D Printing).")

# Export STEPs (For Fusion 360 / SolidWorks / CAD)
export_step(base.part, "pid_inv_base.step")
export_step(shell.part, "pid_inv_shell.step")
export_step(washer.part, "pid_m3_washer.step")
print("✅ STEP files generated (for Fusion 360).")

# ==============================================================================
# 7. VISUALIZATION
# ==============================================================================
# View in OCP CAD Viewer (optional - skips gracefully if viewer not running)
shell_viz = shell.part.move(Location((0,0, 60)))
base_viz = base.part
washer_viz = washer.part.move(Location((BOX_W/2 + 20, 0, 0)))  # Position washer to the side

# Ghosts
pid_ghost = Location((pid_x, pid_y, pid_z_center)) * Box(PID_BODY_W, PID_BODY_D, PID_BODY_H)
ssr_ghost = Location((ssr_x, ssr_y, ssr_z + SSR_H/2)) * Box(SSR_W, SSR_L, SSR_H)
term_ghost = Location((term_x, term_y, BASE_THICKNESS + TERM_BOSS_HEIGHT + TERM_H/2)) * Box(TERM_W, TERM_D, TERM_H)
c14_ghost_y = (BOX_L/2) - (C14_GHOST_DEPTH / 2)
c14_ghost = Location((c14_x, c14_ghost_y, c14_z)) * Box(C14_BODY_W, C14_GHOST_DEPTH, C14_BODY_H)

try:
    show_object(base_viz, name="Base Plate", options={"alpha": 1.0, "color": (0.3, 0.3, 0.3)})
    show_object(shell_viz, name="Shell (Raised)", options={"alpha": 0.6, "color": (0.9, 0.9, 0.9)})
    show_object(washer_viz, name="M3 Washer (9mm OD)", options={"alpha": 1.0, "color": (0.8, 0.4, 0.0)})
    show_object(pid_ghost, name="PID Ghost", options={"alpha": 0.3, "color": (1, 0, 0)})
    show_object(ssr_ghost, name="SSR Ghost", options={"alpha": 0.3, "color": (0, 1, 0)})
    show_object(term_ghost, name="Terminal Ghost", options={"alpha": 0.3, "color": (0, 0, 1)})
    show_object(c14_ghost, name="C14 Ghost (+Cables)", options={"alpha": 0.4, "color": (1.0, 1.0, 0.0)})
    print("✅ 3D visualization sent to OCP Viewer.")
except Exception as e:
    print("ℹ️  3D viewer not available (this is normal when running from command line).")
    print("   STL/STEP files generated successfully - import them into your CAD software or slicer.")