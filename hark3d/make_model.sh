#!/usr/bin/env bash
# Usage: ./make_model.sh models/<name>.py [--tex 1024] [--no-bake]
cd "$(dirname "$0")"
BL=./blender/blender; [ -x "$BL" ] || BL=$(command -v blender)
"$BL" -b -P pipeline/build.py -- "$@" 2>&1 | grep -E "HARK3D|Error|Traceback|line [0-9]+" 
