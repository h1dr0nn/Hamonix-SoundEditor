# Bundled runtimes

Place platform-specific binaries in this directory before packaging:

- `python/` — embedded Python runtime (`python`, `python3`, or `python.exe`).
- `ffmpeg/` — FFmpeg executables (`ffmpeg` and/or `ffmpeg.exe`).

Ensure executables are marked as runnable (e.g., `chmod +x ffmpeg python/bin/python3`) prior to building.
