# Kinetic Studio

An original keyframe motion-graphics and edit-style video editor for Linux (any modern Chromium/Chrome/Firefox). No install: `./run.sh`.

## Features
- **Drawing:** rect, ellipse, star/polygon, smooth bezier pen, text (typewriter reveal), images; gradients, strokes, 16 blend modes.
- **Video & audio:** import clips and music, trim/move on the timeline, volume and keyframed **speed ramps**, audio mixed into export.
- **Keyframes** on position, size, rotation, opacity, blur and every effect; 6 easing curves; drag diamonds to retime.
- **Effects** (per layer or on an **adjustment layer** that affects everything below): RGB split, glitch, shake, glow, pixelate, zoom punch, flash, brightness/contrast/saturation/hue/invert, film grain, vignette, VHS lines, motion blur (4×/8×).
- **Fast-edit workflow:** beat markers (`M`, or auto-detected from imported music), one-click *Hit* presets (Shake, RGB hit, Glitch, Zoom punch, Flash, Impact) and **Beat-sync** presets that stamp a hit on every marker; looks (Cinematic, VHS, Dream glow, B&W, Neon); entrances (fade, pop, slide, spin); light leak; cinematic bars.
- **Canvas sizes:** 16:9, 9:16 (Shorts/Reels), 1:1, 4:5. Export WebM (video + audio) or PNG frame. Save/open projects as JSON.

## Shortcuts
V select · R rect · E ellipse · S star · P pen · T text · I image · Space play · K key all transform props · M add marker (Shift+M clear) · N / Shift+N next/prev marker · ←/→ step frame · Ctrl+Z/Y · Ctrl+D · Delete.

## Export to MP4
`./to-mp4.sh "My project.webm"` (needs ffmpeg).

## Notes
Imported video/audio files are not embedded in the project JSON; re-import them after opening a saved project.
