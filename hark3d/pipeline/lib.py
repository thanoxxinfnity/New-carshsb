"""Hark3D helper library: shapes + procedural materials for Blender (bpy)."""
import bpy, math

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------- materials ----------
def _mat(name):
    if name in bpy.data.materials:
        return bpy.data.materials[name], None
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree

def wood(name="Wood", dark=(0.12, 0.055, 0.025), light=(0.30, 0.16, 0.07), grain=4.0):
    m, nt = _mat(name)
    if nt is None: return m
    n, l = nt.nodes, nt.links; b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1, 8, 1)
    no = n.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value = 2; no.inputs["Detail"].default_value = 8
    wv = n.new("ShaderNodeTexWave"); wv.wave_type = 'RINGS'
    wv.inputs["Scale"].default_value = grain; wv.inputs["Distortion"].default_value = 6
    rp = n.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*dark, 1); rp.color_ramp.elements[1].color = (*light, 1)
    bu = n.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.15
    l.new(tc.outputs["Object"], mp.inputs["Vector"]); l.new(mp.outputs["Vector"], no.inputs["Vector"])
    l.new(no.outputs["Color"], wv.inputs["Vector"]); l.new(wv.outputs["Fac"], rp.inputs["Fac"])
    l.new(rp.outputs["Color"], b.inputs["Base Color"]); l.new(wv.outputs["Fac"], bu.inputs["Height"])
    l.new(bu.outputs["Normal"], b.inputs["Normal"]); b.inputs["Roughness"].default_value = 0.4
    return m

def metal(name="Metal", color=(0.6, 0.6, 0.62), rough=0.3, rust=0.0):
    m, nt = _mat(name)
    if nt is None: return m
    n, l = nt.nodes, nt.links; b = n["Principled BSDF"]
    b.inputs["Metallic"].default_value = 1.0
    no = n.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value = 30; no.inputs["Detail"].default_value = 10
    rp = n.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*color, 1)
    rp.color_ramp.elements[1].color = (0.35, 0.12, 0.04, 1) if rust > 0 else tuple(c * 0.8 for c in color) + (1,)
    rp.color_ramp.elements[1].position = 1.0 - rust * 0.5 if rust else 1.0
    l.new(no.outputs["Fac"], rp.inputs["Fac"]); l.new(rp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    return m

def fabric(name="Fabric", color=(0.05, 0.18, 0.15)):
    m, nt = _mat(name)
    if nt is None: return m
    n, l = nt.nodes, nt.links; b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = 0.9
    ck = n.new("ShaderNodeTexChecker"); ck.inputs["Scale"].default_value = 300
    bu = n.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.08
    l.new(ck.outputs["Fac"], bu.inputs["Height"]); l.new(bu.outputs["Normal"], b.inputs["Normal"])
    return m

def stone(name="Stone", color=(0.45, 0.43, 0.4)):
    m, nt = _mat(name)
    if nt is None: return m
    n, l = nt.nodes, nt.links; b = n["Principled BSDF"]
    vo = n.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 8
    no = n.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value = 15; no.inputs["Detail"].default_value = 12
    rp = n.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = tuple(c * 0.6 for c in color) + (1,); rp.color_ramp.elements[1].color = (*color, 1)
    mx = n.new("ShaderNodeMath"); mx.operation = 'MULTIPLY'
    bu = n.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.4
    l.new(vo.outputs["Distance"], mx.inputs[0]); l.new(no.outputs["Fac"], mx.inputs[1])
    l.new(mx.outputs[0], rp.inputs["Fac"]); l.new(rp.outputs["Color"], b.inputs["Base Color"])
    l.new(mx.outputs[0], bu.inputs["Height"]); l.new(bu.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.85
    return m

def plain(name="Plastic", color=(0.8, 0.1, 0.1), rough=0.4, metallic=0.0):
    m, nt = _mat(name)
    if nt is None: return m
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metallic
    return m

# ---------- shapes (meters, Z up, origin at floor) ----------
def _finish(o, name, mat, bevel):
    o.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if bevel:
        bv = o.modifiers.new("bev", "BEVEL"); bv.width = bevel; bv.segments = 2
    if mat: o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return o

def box(name, loc, size, mat=None, rot=(0, 0, 0), bevel=0.005):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = (size[0]/2, size[1]/2, size[2]/2)
    return _finish(o, name, mat, bevel)

def cylinder(name, loc, radius, height, mat=None, rot=(0, 0, 0), sides=24, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=loc, rotation=rot, vertices=sides)
    return _finish(bpy.context.object, name, mat, bevel)

def cone(name, loc, r1, r2, height, mat=None, rot=(0, 0, 0), sides=24):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=height, location=loc, rotation=rot, vertices=sides)
    return _finish(bpy.context.object, name, mat, 0)

def sphere(name, loc, radius, mat=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc, segments=24, ring_count=12)
    o = bpy.context.object; o.scale = scale
    return _finish(o, name, mat, 0)

def torus(name, loc, major, minor, mat=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=loc, rotation=rot)
    return _finish(bpy.context.object, name, mat, 0)

def group(name, objects, loc=(0, 0, 0), rot_z=0.0):
    """Parent objects under an empty so you can move/rotate them together."""
    bpy.ops.object.empty_add(location=(0, 0, 0)); e = bpy.context.object; e.name = name
    for o in objects: o.parent = e
    e.location = loc; e.rotation_euler = (0, 0, rot_z)
    return e

def deg(d): return math.radians(d)
