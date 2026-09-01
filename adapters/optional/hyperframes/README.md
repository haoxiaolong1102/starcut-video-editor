# HyperFrames optional adapter

Install HyperFrames separately and follow its current documentation and Apache-2.0 notices. StarCut uses it for fast information packaging, captions, HTML-native motion, and final render when available.

Implementation rules:

- author original components; do not copy third-party recipe source
- make animations seekable and deterministic
- keep media paths explicit and validate the composition before render
- use FFprobe on the final MP4

Fallback: another renderer or renderer-neutral SHOTBOOK/edit manifest.
