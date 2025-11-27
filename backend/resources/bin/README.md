# FFmpeg binaries

Place platform-specific FFmpeg executables in this directory when running the
application from source. During packaged execution (PyInstaller), the
``ensure_ffmpeg`` helper will automatically add this directory to ``PATH`` and
configure ``pydub`` to use the bundled binary.

When executed via Tauri, the launcher sets ``SOUNDCONVERTER_BIN_DIR`` to the
bundled ``src-tauri/bin`` directory. ``ensure_ffmpeg`` reads this environment
variable first, ensuring the packaged FFmpeg binary is always preferred.

Expected file names include:

- `ffmpeg` (Linux/macOS)
- `ffmpeg.exe` (Windows)

You may also provide other compatible encoder binaries such as `avconv`.
