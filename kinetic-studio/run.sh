#!/usr/bin/env bash
# Launch Kinetic Studio as a standalone window on Linux (uses any installed Chromium/Chrome/Firefox).
DIR="$(cd "$(dirname "$0")" && pwd)"
URL="file://$DIR/index.html"
for b in chromium chromium-browser google-chrome google-chrome-stable brave-browser; do
  if command -v "$b" >/dev/null; then exec "$b" --app="$URL" --window-size=1440,860; fi
done
exec xdg-open "$URL"
