from build123d import *
from ocp_vscode import show, show_object, set_port, set_defaults, Camera

# ==============================================================================
# 1. CONFIGURATION SWITCH
# ==============================================================================
USE_INSERTS = False 

# ==============================================================================
# 2. PARAMETERS
# ==============================================================================

# -- Global Settings --
WALL_THICKNESS = 2.0
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

if USE_INSERTS:
    THREAD_M3_DIA = 4.2       
    THREAD_M35_DIA = 4.8      
else:
    THREAD_M3_DIA = 2.8       
    THREAD_M35_DIA = 2.8      

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
pid_z = 20.0 

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
    with Locations((ssr_x, ssr_y, 0)):
        with Locations((0, SSR_MOUNT_SPACING/2), (0, -SSR_MOUNT_SPACING/2)):
            Cylinder(radius=THREAD_M3_DIA/2, height=BASE_THICKNESS + SSR_PLATFORM_HEIGHT + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Terminal Block Platform
    with Locations((term_x, term_y, BASE_THICKNESS)):
        Box(TERM_W + 4, TERM_D + 4, TERM_BOSS_HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
    # Terminal Block Holes
    with Locations((term_x, term_y, 0)):
        with GridLocations(TERM_MOUNT_X, TERM_MOUNT_Y, 2, 2):
            Cylinder(radius=THREAD_M3_DIA/2, height=BASE_THICKNESS + TERM_BOSS_HEIGHT + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

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
# 5. BUILD SHELL (With Clamp Posts)
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
    with Locations((0,0, BOX_H - ROOF_THICKNESS)): 
        with Locations(
            (corner_off_x, corner_off_y), (-corner_off_x, corner_off_y),
            (corner_off_x, -corner_off_y), (-corner_off_x, -corner_off_y)
        ):
            Cylinder(radius=5.0, height=post_h, align=(Align.CENTER, Align.CENTER, Align.MAX))
            Cylinder(radius=THREAD_M3_DIA/2, height=post_h, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # PID Cutout
    with Locations((pid_x, -BOX_L/2, pid_z + PID_BODY_H/2)):
        Box(PID_BODY_W + FIT_TOLERANCE, WALL_THICKNESS*4, PID_BODY_H + FIT_TOLERANCE, mode=Mode.SUBTRACT)

    # --- NEW: PID Clamp Posts ---
    # Two posts growing from the Front Face (inside) up to 48mm height
    clamp_post_h = 48.0 # Just taller than the PID body (45mm)
    clamp_spacing = PID_BODY_W + 10.0 # 5mm clearance each side
    with Locations((pid_x, -BOX_L/2 + WALL_THICKNESS, pid_z + PID_BODY_H/2)):
        # We need to rotate coordinates to build on the floor (Front Face Inner)
        # Actually easiest to place them relative to Global Z=0 (Top of box)? No, relative to front wall.
        # Front wall is at Y = -BOX_L/2
        pass

    # Let's place them relative to the PID center
    with Locations((pid_x, -BOX_L/2 + WALL_THICKNESS, pid_z + PID_BODY_H/2)):
         with Locations((clamp_spacing/2, 0, 0), (-clamp_spacing/2, 0, 0)):
             # Cylinder pointing +Y (into the case)
             Cylinder(radius=4.0, height=clamp_post_h, rotation=(90, 0, 0), align=(Align.CENTER, Align.CENTER, Align.MIN))
             # Screw Hole
             Cylinder(radius=THREAD_M3_DIA/2, height=clamp_post_h, rotation=(90, 0, 0), align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Socket Mounts
    left_screw_x = socket_x - UK_SOCKET_MOUNT_PITCH/2
    right_screw_x = socket_x + UK_SOCKET_MOUNT_PITCH/2
    
    with Locations((0, socket_y, BOX_H - ROOF_THICKNESS)):
        with Locations((socket_x, 0)):
            Box(UK_SOCKET_CUTOUT_SIZE, UK_SOCKET_CUTOUT_SIZE, ROOF_THICKNESS*4, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

        with Locations((right_screw_x, 0)):
             Cylinder(radius=SOCKET_BOSS_DIA/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX))
             with Locations((7.5, 0, -SOCKET_BOSS_DEPTH/2)):
                 Box(15.0, SOCKET_BOSS_DIA, SOCKET_BOSS_DEPTH)
             Cylinder(radius=THREAD_M35_DIA/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

        left_wall_x = -BOX_W/2 + WALL_THICKNESS
        bridge_len = abs(left_screw_x - left_wall_x) + 2.0 
        
        with Locations((left_screw_x, 0)):
             Cylinder(radius=SOCKET_BOSS_DIA/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX))
             with Locations((-bridge_len/2, 0, -SOCKET_BOSS_DEPTH/2)):
                 Box(bridge_len, SOCKET_BOSS_DIA, SOCKET_BOSS_DEPTH)
             Cylinder(radius=THREAD_M35_DIA/2, height=SOCKET_BOSS_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # C14
    c14_inner_wall_y = BOX_L/2 - WALL_THICKNESS
    with Locations((c14_x, c14_inner_wall_y, 0)): 
        pilaster_h = BOX_H - ROOF_THICKNESS
        screw_x_offset = C14_SCREW_PITCH/2 
        with Locations((screw_x_offset, 0, 0), (-screw_x_offset, 0, 0)):
             Box(12.0, C14_BOSS_DEPTH, pilaster_h, align=(Align.CENTER, Align.MAX, Align.MIN))

    with Locations((c14_x, BOX_L/2, c14_z)):
        Box(C14_BODY_W, WALL_THICKNESS*4, C14_BODY_H, mode=Mode.SUBTRACT)
        with Locations((C14_SCREW_PITCH/2, 0), (-C14_SCREW_PITCH/2, 0)):
             Cylinder(radius=THREAD_M3_DIA/2, height=30.0, rotation=(90,0,0), mode=Mode.SUBTRACT)

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
# 6. BUILD CLAMP BAR (Separate Part)
# ==============================================================================
with BuildPart() as clamp_bar:
    with BuildSketch():
        # Width: Spanning the posts + extra
        # Height: 10mm bar
        Rectangle(PID_BODY_W + 20.0, 10.0)
        fillet(vertices(), radius=2.0)
    extrude(amount=3.0) # 3mm thick bar
    
    # Holes matching the posts
    with Locations((clamp_spacing/2, 0), (-clamp_spacing/2, 0)):
         Cylinder(radius=SCREW_M3_CLEARANCE/2, height=10.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)


# ==============================================================================
# 7. EXPORT
# ==============================================================================
print(f"Shell Dimensions: {BOX_W:.1f} x {BOX_L:.1f} x {BOX_H:.1f} mm")

export_stl(base.part, "pid_inv_base.stl")
export_stl(shell.part, "pid_inv_shell.stl")
export_stl(clamp_bar.part, "pid_inv_clamp_bar.stl") # Don't forget to print this!

# ==============================================================================
# 8. VISUALIZATION
# ==============================================================================
shell_viz = shell.part.move(Location((0,0, 60)))
base_viz = base.part
clamp_viz = clamp_bar.part.move(Location((pid_x, -BOX_L/2 + 45.0, pid_z + PID_BODY_H/2))).rotate(Axis.X, 90)

# Ghosts
pid_ghost = Location((pid_x, pid_y, pid_z + PID_BODY_H/2)) * Box(PID_BODY_W, PID_BODY_D, PID_BODY_H)
ssr_ghost = Location((ssr_x, ssr_y, ssr_z + SSR_H/2)) * Box(SSR_W, SSR_L, SSR_H)
term_ghost = Location((term_x, term_y, BASE_THICKNESS + TERM_BOSS_HEIGHT + TERM_H/2)) * Box(TERM_W, TERM_D, TERM_H)
c14_ghost_y = (BOX_L/2) - (C14_GHOST_DEPTH / 2)
c14_ghost = Location((c14_x, c14_ghost_y, c14_z)) * Box(C14_BODY_W, C14_GHOST_DEPTH, C14_BODY_H)

show_object(base_viz, name="Base Plate", options={"alpha": 1.0, "color": (0.3, 0.3, 0.3)})
show_object(shell_viz, name="Shell (Raised)", options={"alpha": 0.6, "color": (0.9, 0.9, 0.9)})
show_object(clamp_viz, name="Clamp Bar (Green)", options={"alpha": 1.0, "color": (0.0, 1.0, 0.0)})
show_object(pid_ghost, name="PID Ghost", options={"alpha": 0.3, "color": (1, 0, 0)})
show_object(ssr_ghost, name="SSR Ghost", options={"alpha": 0.3, "color": (0, 1, 0)})
show_object(term_ghost, name="Terminal Ghost", options={"alpha": 0.3, "color": (0, 0, 1)})
show_object(c14_ghost, name="C14 Ghost (+Cables)", options={"alpha": 0.4, "color": (1.0, 1.0, 0.0)})