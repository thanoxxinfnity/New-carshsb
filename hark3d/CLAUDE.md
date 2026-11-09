# Hark3D: textured 3D models for the game

When asked for a 3D model (e.g. "make a wooden barrel"):
1. Create `models/<snake_name>.py` with `def build(lib):` that builds the model using helpers in `pipeline/lib.py`.
2. Run `./make_model.sh models/<snake_name>.py` (first time: `./setup.sh`).
3. Check `out/<snake_name>/preview.png` (look at it). Fix proportions if wrong and re-run.
4. Deliver `out/<snake_name>/<snake_name>.glb` (preferred: Godot/Unity/Unreal/web) or `.fbx`, plus `textures/`.

## Rules
- Units are meters, Z is up, object sits on the floor at z=0, centered at x=0,y=0. Use real-world sizes.
- Build only from lib shapes: `box, cylinder, cone, sphere, torus` and `group(name, objs, loc, rot_z)` for repeated parts.
- Materials: `wood(name, dark, light, grain)`, `metal(name, color, rough, rust)`, `fabric(name, color)`, `stone(name, color)`, `plain(name, color, rough, metallic)`. Colors are linear RGB 0-1. Give each material a unique name.
- Procedural materials are baked automatically into color/roughness/normal PNGs and a single game-ready mesh.
- Keep it low-poly for games: avoid > ~200 parts. Use `--tex 2048` for hero props, `--tex 512` for small props.
- See `models/table_chairs.py` for an example.
