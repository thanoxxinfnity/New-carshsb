"""Hark3D runner.
Usage: blender -b -P pipeline/build.py -- models/<name>.py [out_dir] [--tex 1024] [--no-bake]
A model file must define:  def build(lib): ...   (create objects using lib helpers)
Outputs in out_dir/<name>/: <name>.glb, <name>.fbx, <name>.blend, preview.png, textures/*.png
"""
import bpy, sys, os, math, importlib.util, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
model_path = os.path.abspath(argv[0])
out_root = os.path.abspath(argv[1]) if len(argv) > 1 and not argv[1].startswith("--") else os.path.join(os.path.dirname(model_path), "..", "out")
tex = int(argv[argv.index("--tex") + 1]) if "--tex" in argv else 1024
do_bake = "--no-bake" not in argv
name = os.path.splitext(os.path.basename(model_path))[0]
out = os.path.join(out_root, name); os.makedirs(os.path.join(out, "textures"), exist_ok=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
lib.clear()
spec = importlib.util.spec_from_file_location("model", model_path)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.build(lib)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'

# ---- apply modifiers + parents, join into one game-ready mesh ----
meshes = [o for o in scene.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
bpy.ops.object.convert(target='MESH')
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.join()
obj = bpy.context.object; obj.name = name
for o in [o for o in scene.objects if o.type == 'EMPTY']: bpy.data.objects.remove(o)

# ---- UV unwrap ----
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.01)
bpy.ops.object.mode_set(mode='OBJECT')

# ---- bake procedural textures to images ----
if do_bake:
    scene.cycles.samples = 16
    imgs = {}
    for kind in ("color", "roughness", "normal"):
        img = bpy.data.images.new(f"{name}_{kind}", tex, tex)
        if kind != "color": img.colorspace_settings.name = 'Non-Color'
        imgs[kind] = img
    def set_target(img):
        for slot in obj.material_slots:
            nt = slot.material.node_tree
            node = nt.nodes.get("BAKE") or nt.nodes.new("ShaderNodeTexImage")
            node.name = "BAKE"; node.image = img; nt.nodes.active = node
    bake = scene.render.bake; bake.margin = 8
    set_target(imgs["color"]); bake.use_pass_direct = False; bake.use_pass_indirect = False; bake.use_pass_color = True
    bpy.ops.object.bake(type='DIFFUSE')
    set_target(imgs["roughness"]); bpy.ops.object.bake(type='ROUGHNESS')
    set_target(imgs["normal"]); bpy.ops.object.bake(type='NORMAL')
    # metallic: keep max value of source materials
    metal = max(s.material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value for s in obj.material_slots)
    for k, img in imgs.items():
        img.filepath_raw = os.path.join(out, "textures", f"{name}_{k}.png"); img.file_format = 'PNG'; img.save()
    m = bpy.data.materials.new(f"{name}_baked"); m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links; b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexImage"); tc.image = imgs["color"]
    tr = n.new("ShaderNodeTexImage"); tr.image = imgs["roughness"]
    tn = n.new("ShaderNodeTexImage"); tn.image = imgs["normal"]
    nm = n.new("ShaderNodeNormalMap")
    l.new(tc.outputs["Color"], b.inputs["Base Color"]); l.new(tr.outputs["Color"], b.inputs["Roughness"])
    l.new(tn.outputs["Color"], nm.inputs["Color"]); l.new(nm.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Metallic"].default_value = metal if metal > 0.5 else 0.0
    obj.data.materials.clear(); obj.data.materials.append(m)

# ---- export ----
bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(out, f"{name}.glb"), use_selection=True, export_format='GLB')
try:
    bpy.ops.export_scene.fbx(filepath=os.path.join(out, f"{name}.fbx"), use_selection=True,
                             path_mode='COPY', embed_textures=True)
except Exception as e:
    print("FBX export skipped:", e)

# ---- preview render (auto-framed) ----
bb = [obj.matrix_world @ mathutils.Vector(c) for c in obj.bound_box]
ctr = sum(bb, mathutils.Vector()) / 8; rad = max((v - ctr).length for v in bb)
bpy.ops.mesh.primitive_plane_add(size=rad * 30, location=(0, 0, min(v.z for v in bb)))
fl = bpy.context.object; fm = lib.plain("Floor", (0.6, 0.6, 0.6), 0.6); fl.data.materials.append(fm)
d = rad * 2.6
bpy.ops.object.camera_add(location=ctr + mathutils.Vector((d * 0.75, -d * 0.85, d * 0.6)))
cam = bpy.context.object; scene.camera = cam; cam.data.lens = 40
cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
bpy.ops.object.light_add(type='AREA', location=ctr + mathutils.Vector((rad * 2, -rad * 2.5, rad * 3)))
L = bpy.context.object; L.data.energy = 250 * rad * rad; L.data.size = rad * 2
L.rotation_euler = (ctr - L.location).to_track_quat('-Z', 'Y').to_euler()
w = bpy.data.worlds.new("W"); scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.78, 0.82, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.7
scene.cycles.samples = 64; scene.cycles.use_denoising = False
scene.render.resolution_x, scene.render.resolution_y = 1024, 768
scene.view_settings.view_transform = 'AgX'
scene.render.filepath = os.path.join(out, "preview.png")
bpy.ops.render.render(write_still=True)
bpy.data.objects.remove(fl)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, f"{name}.blend"))
print(f"HARK3D DONE -> {out}")
