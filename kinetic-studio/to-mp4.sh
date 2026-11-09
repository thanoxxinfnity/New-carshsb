#!/usr/bin/env bash
# Convert a Kinetic Studio WebM export to a high-quality MP4 (H.264 + AAC) for YouTube / social.
# Usage: ./to-mp4.sh input.webm [output.mp4]
set -e
in="$1"; out="${2:-${1%.webm}.mp4}"
ffmpeg -y -i "$in" -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "$out"
echo "Wrote $out"
