"""Dining table with 6 ladder-back chairs. Units: meters."""
def build(lib):
    walnut = lib.wood("Walnut", (0.12, 0.055, 0.025), (0.30, 0.16, 0.07), 4)
    oak = lib.wood("Oak", (0.35, 0.2, 0.09), (0.6, 0.4, 0.2), 5)
    cushion = lib.fabric("Cushion", (0.05, 0.18, 0.15))
    TW, TD, TH = 1.8, 0.95, 0.76
    lib.box("TableTop", (0, 0, TH - 0.025), (TW, TD, 0.05), walnut, bevel=0.01)
    for sy in (-1, 1):
        lib.box("Apron", (0, sy * (TD/2 - 0.08), TH - 0.1), (TW - 0.2, 0.025, 0.1), walnut)
    for sx in (-1, 1):
        for sy in (-1, 1):
            lib.box("Leg", (sx * (TW/2 - 0.1), sy * (TD/2 - 0.1), (TH - 0.05)/2), (0.06, 0.06, TH - 0.05), walnut)
    def chair(x, y, rot):
        SH = 0.46; p = []
        p.append(lib.box("Seat", (0, 0, SH - 0.02), (0.46, 0.44, 0.04), oak))
        p.append(lib.box("Cushion", (0, 0.01, SH + 0.015), (0.42, 0.38, 0.035), cushion, bevel=0.012))
        for sx in (-1, 1):
            for sy in (-1, 1):
                p.append(lib.cylinder("CLeg", (sx*0.19, sy*0.18, (SH - 0.04)/2), 0.018, SH - 0.04, oak))
            p.append(lib.box("Post", (sx*0.19, -0.2, SH + 0.24), (0.035, 0.035, 0.48), oak))
        for z in (SH + 0.22, SH + 0.36, SH + 0.46):
            p.append(lib.box("Slat", (0, -0.2, z), (0.36, 0.02, 0.05), oak))
        lib.group("Chair", p, (x, y, 0), rot)
    import math
    chair(-0.45, -0.72, 0); chair(0.45, -0.72, 0)
    chair(-0.45, 0.72, math.pi); chair(0.45, 0.72, math.pi)
    chair(-1.12, 0, -math.pi/2); chair(1.12, 0, math.pi/2)
