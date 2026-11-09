#!/usr/bin/env bash
# Installs Blender 4.2 LTS (portable, no root needed) into ./blender
set -e
cd "$(dirname "$0")"
if [ -x blender/blender ]; then echo "Blender already installed"; exit 0; fi
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
  curl -L https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz -o b.tar.xz
  python3 -c "import tarfile,lzma;tarfile.open(fileobj=lzma.open('b.tar.xz')).extractall('.')"
  mv blender-4.2.3-linux-x64 blender && rm b.tar.xz
  # headless needs a few X/GL libs on slim images (ignore errors if no root)
  (sudo apt-get install -y libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libxkbcommon0 libsm6 2>/dev/null || apt-get install -y libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libxkbcommon0 libsm6 2>/dev/null || true)
else
  echo "ARM machine: install with 'sudo apt-get install -y blender' and the scripts will use it"
fi
blender/blender -b --version | head -1
