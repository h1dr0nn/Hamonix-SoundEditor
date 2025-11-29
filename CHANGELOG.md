# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2025-11-29

### Added

- **Smart Analysis**: Automatically detects audio content type (Music, Podcast, Voice-over) and suggests optimal presets.
- **Waveform Preview**: Integrated, embedded audio player within file cards for quick preview without layout shifts.
- **Native Integration**: Added file associations to open supported audio files directly with Harmonix SE.
- **Native Menus**: Implemented native system menus (File, Edit, Window) for better OS integration.

### Improved

- **UI/UX**: Refined "Embedded Replacement" design for audio preview, ensuring a clean and clutter-free interface.
- **Analysis**: Bundled `ffprobe` binaries for robust audio analysis across macOS, Windows, and Linux.
- **Performance**: Optimized backend communication for analysis and conversion tasks.

### Fixed

- **Audio Cleanup**: Fixed issues where audio would continue playing or duplicate after closing the preview.
- **Layout**: Resolved layout shift issues when toggling the waveform player.
