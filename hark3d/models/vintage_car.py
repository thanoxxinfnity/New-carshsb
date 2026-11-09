"""1930s-style vintage touring sedan. Units: meters, Z up, front of the car faces +Y.
~4.4 m long, 2.1 m wide (over fenders), 1.9 m tall."""
import math

def build(lib):
    # NOTE: the bake keeps ONE metallic value for the whole mesh, so every material stays < 0.5 metallic.
    paint   = lib.plain("CarPaint",  (0.30, 0.012, 0.02), 0.22, 0.4)
    black   = lib.plain("BlackPaint", (0.012, 0.012, 0.014), 0.3, 0.3)
    chrome  = lib.plain("Chrome",   (0.78, 0.8, 0.84), 0.12, 0.45)
    rubber  = lib.plain("Rubber",   (0.02, 0.02, 0.02), 0.85, 0.0)
    white   = lib.plain("Whitewall", (0.8, 0.76, 0.65), 0.7, 0.0)
    glass   = lib.plain("Glass",    (0.02, 0.035, 0.045), 0.04, 0.0)
    lamp    = lib.plain("Lamp",     (1.0, 0.9, 0.6), 0.08, 0.0)
    redlamp = lib.plain("TailLamp", (0.6, 0.02, 0.02), 0.15, 0.0)
    under   = lib.plain("Underbody", (0.03, 0.03, 0.035), 0.7, 0.0)
    leather = lib.fabric("Leather", (0.015, 0.012, 0.012))
    wood    = lib.wood("RunningBoard", (0.16, 0.07, 0.03), (0.38, 0.2, 0.09), 5)

    # ---- body ----
    lib.box("Underbody", (0, -0.1, 0.32), (1.3, 3.9, 0.14), under, bevel=0.01)
    lib.box("BodyLower", (0, -0.1, 0.6), (1.5, 3.1, 0.4), paint, bevel=0.06)
    lib.box("Hood", (0, 1.375, 0.98), (1.1, 1.4, 0.45), paint, bevel=0.1)
    lib.box("HoodStrip", (0, 1.375, 1.215), (0.06, 1.4, 0.03), chrome, bevel=0.005)
    lib.box("Cowl", (0, 0.5, 1.05), (1.45, 0.35, 0.5), paint, bevel=0.05)
    lib.box("Cabin", (0, -0.3, 1.3), (1.42, 1.3, 1.0), paint, bevel=0.07)
    lib.box("Roof", (0, -0.3, 1.84), (1.5, 1.5, 0.07), black, bevel=0.03)
    lib.box("Visor", (0, 0.5, 1.8), (1.3, 0.22, 0.03), black, rot=(-0.25, 0, 0), bevel=0.005)
    lib.box("Trunk", (0, -1.35, 1.0), (1.35, 0.75, 0.5), paint, bevel=0.08)

    # ---- glass + door seams + handles ----
    lib.box("GlassFront", (0, 0.36, 1.42), (1.2, 0.03, 0.5), glass, bevel=0.0)
    lib.box("GlassRear", (0, -0.96, 1.42), (1.2, 0.03, 0.5), glass, bevel=0.0)
    for sx in (-1, 1):
        lib.box("GlassSide", (sx * 0.715, -0.3, 1.42), (0.03, 0.9, 0.5), glass, bevel=0.0)
        lib.box("DoorLineA", (sx * 0.712, 0.17, 1.1), (0.02, 0.012, 0.95), black, bevel=0.0)
        lib.box("DoorLineB", (sx * 0.712, -0.72, 1.1), (0.02, 0.012, 0.95), black, bevel=0.0)
        lib.box("Handle", (sx * 0.73, -0.1, 1.1), (0.03, 0.14, 0.025), chrome, bevel=0.004)
        lib.box("Handle", (sx * 0.73, -0.95, 1.1), (0.03, 0.14, 0.025), chrome, bevel=0.004)
        lib.box("RunningBoard", (sx * 0.92, -0.05, 0.42), (0.3, 1.7, 0.04), wood, bevel=0.01)

    # ---- grille / radiator ----
    lib.box("RadShell", (0, 2.1, 0.95), (0.78, 0.08, 0.72), chrome, bevel=0.03)
    lib.box("Grille", (0, 2.108, 0.93), (0.64, 0.08, 0.56), black, bevel=0.0)
    for i in range(9):
        lib.box("GrilleBar", (-0.28 + i * 0.07, 2.15, 0.93), (0.012, 0.02, 0.56), chrome, bevel=0.0)
    lib.cone("Ornament", (0, 2.1, 1.36), 0.04, 0.0, 0.14, chrome, rot=(0, 0, 0))
    lib.cylinder("OrnamentBase", (0, 2.1, 1.31), 0.035, 0.06, chrome)

    # ---- bumpers ----
    lib.box("BumperF", (0, 2.2, 0.45), (1.8, 0.08, 0.1), chrome, bevel=0.03)
    lib.box("BumperR", (0, -2.1, 0.45), (1.8, 0.08, 0.1), chrome, bevel=0.03)
    for sx in (-1, 1):
        lib.box("BumperArmF", (sx * 0.6, 2.1, 0.45), (0.05, 0.2, 0.05), chrome)
        lib.box("BumperArmR", (sx * 0.6, -2.0, 0.45), (0.05, 0.2, 0.05), chrome)

    # ---- headlights, tail lights ----
    for sx in (-1, 1):
        lib.cylinder("LampStalk", (sx * 0.72, 1.72, 0.96), 0.018, 0.16, chrome)
        lib.sphere("LampShell", (sx * 0.72, 1.72, 1.06), 0.14, chrome, scale=(1, 0.85, 1))
        lib.sphere("LampLens", (sx * 0.72, 1.81, 1.06), 0.105, lamp, scale=(1, 0.5, 1))
        lib.cylinder("TailLamp", (sx * 0.55, -1.74, 1.05), 0.04, 0.05, redlamp, rot=(math.pi/2, 0, 0))

    # ---- fenders ----
    def fender(x, y):
        s = 1 if x > 0 else -1
        lib.box("FenderTop", (x, y, 0.9), (0.38, 1.0, 0.05), black, bevel=0.02)
        lib.box("FenderFrontLip", (x, y + 0.5, 0.82), (0.38, 0.36, 0.05), black, rot=(-0.65, 0, 0), bevel=0.015)
        lib.box("FenderRearLip", (x, y - 0.5, 0.82), (0.38, 0.36, 0.05), black, rot=(0.65, 0, 0), bevel=0.015)
        lib.box("FenderSkirt", (x + s * 0.18, y, 0.76), (0.03, 1.0, 0.22), black, bevel=0.01)
    FX, FY, RY = 0.84, 1.35, -1.25
    for sx in (-1, 1):
        fender(sx * FX, FY)
        fender(sx * FX, RY)

    # ---- wheels (wire wheels with whitewalls) ----
    R = 0.4
    def wheel(x, y, axis_rot=(0, math.pi/2, 0), spare=False):
        s = 1 if x >= 0 else -1
        if not spare:
            lib.cylinder("Tire", (x, y, R), R, 0.22, rubber, rot=axis_rot, sides=36, bevel=0.03)
            lib.cylinder("Whitewall", (x, y, R), 0.34, 0.226, white, rot=axis_rot, sides=36)
            lib.cylinder("Rim", (x, y, R), 0.27, 0.23, chrome, rot=axis_rot, sides=36)
            for i in range(6):
                lib.box("Spoke", (x + s * 0.02, y, R), (0.02, 0.5, 0.012), chrome, rot=(i * math.pi / 6, 0, 0), bevel=0)
            lib.sphere("Hubcap", (x + s * 0.115, y, R), 0.09, chrome, scale=(0.45, 1, 1))
        else:
            c = (0, y, 0.78)
            rr = (math.pi/2, 0, 0)
            lib.cylinder("SpareTire", c, 0.36, 0.2, rubber, rot=rr, sides=36, bevel=0.03)
            lib.cylinder("SpareWhite", c, 0.3, 0.206, white, rot=rr, sides=36)
            lib.cylinder("SpareRim", c, 0.23, 0.21, chrome, rot=rr, sides=36)
    for sx in (-1, 1):
        wheel(sx * FX, FY)
        wheel(sx * FX, RY)
    wheel(0, -1.9, spare=True)
    lib.box("SpareMount", (0, -1.82, 0.5), (0.1, 0.1, 0.3), chrome)

    # ---- details: exhaust, mirrors, steering wheel peek ----
    lib.cylinder("Exhaust", (0.45, -1.9, 0.3), 0.04, 0.4, chrome, rot=(math.pi/2, 0, 0))
    for sx in (-1, 1):
        lib.sphere("Mirror", (sx * 0.78, 0.55, 1.5), 0.06, chrome)
        lib.cylinder("MirrorArm", (sx * 0.78, 0.55, 1.42), 0.01, 0.15, chrome)
    lib.box("LicensePlate", (0, -2.16, 0.62), (0.34, 0.01, 0.17), white, bevel=0.0)
