# 🎵 Harmonix SE

**Professional audio converter with an elegant, modern interface**

Harmonix SE is a powerful desktop application for converting, enhancing, and processing audio files. Built with cutting-edge technology and designed with a beautiful macOS/iOS-inspired interface.

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.2-brightgreen)

---

## ✨ Features

### 🔄 Format Conversion

Convert audio files between popular formats:

- **MP3** - Universal compatibility
- **AAC/M4A** - High quality, small size
- **FLAC** - Lossless quality
- **WAV** - Professional uncompressed
- **OGG** - Open source alternative

### 🎚️ Audio Enhancement

- **Smart Analysis** - Automatically detect content type (Music, Podcast, Voice-over)
- **Audio Mastering** - Professional-grade normalization and compression
- **Preset System** - Optimized settings for different content types
- **LUFS Normalization** - Industry-standard loudness management

### ✂️ Audio Cleanup

- **Silence Trimming** - Remove quiet sections from beginning and end
- **Customizable Threshold** - Fine-tune detection sensitivity
- **Padding Control** - Add buffer space around trimmed audio

### 🛠️ Audio Modification

- **Speed Adjustment** - Change playback speed (0.5x - 2.0x)
- **Pitch Shifting** - Adjust pitch without changing tempo
- **Precision Cutting** - Trim exact sections with visual controls

### 🎨 Beautiful Interface

- **Modern Design** - Glassmorphism effects with blur and transparency
- **Light & Dark Modes** - Automatic theme switching
- **Drag & Drop** - Simple, intuitive file handling
- **Real-time Progress** - Watch your files convert live
- **Waveform Preview** - Visual audio playback before converting
- **Multi-language** - English, Vietnamese, Japanese, Korean, Chinese, Spanish, and more

---

## 📥 Download

### Latest Release: v1.0.2

Download the latest version for your platform:

- **macOS** (Intel & Apple Silicon)
- **Windows** (64-bit)
- **Linux** (64-bit)

👉 [Download from Releases](https://github.com/h1dr0nn/SoundConverterApp/releases/latest)

### Installation

**macOS:**

1. Download the `.dmg` file
2. Open it and drag Harmonix SE to Applications
3. Launch from Applications folder

**Windows:**

1. Download the `.msi` or `.exe` installer
2. Run the installer and follow the prompts
3. Launch from Start Menu or Desktop

**Linux:**

1. Download the `.AppImage` or `.deb` file
2. Make it executable: `chmod +x Harmonix-SE.AppImage`
3. Run the application

---

## 🚀 Getting Started

### Basic Usage

1. **Add Files**

   - Drag and drop audio files into the app
   - Or click to browse and select files
   - Supports multiple files at once

2. **Choose Operation Mode**

   - **Format** - Convert to different format
   - **Enhance** - Improve audio quality with mastering
   - **Clean** - Remove silence from edges
   - **Modify** - Adjust speed, pitch, or trim sections

3. **Select Output**

   - Choose where to save converted files
   - Files are saved with original name + format extension

4. **Process**
   - Click the "Process Files" button
   - Watch real-time progress for each file
   - Done! Files are ready in your output folder

### Smart Analysis

For audio enhancement:

1. Add your audio files
2. Switch to **Enhance** mode
3. Click **Smart Analysis**
4. The app automatically detects content type and applies optimal settings
5. Review the suggested preset or adjust manually
6. Process your files

---

## ⚙️ Settings

Access settings via the gear icon in the top-right corner.

### Configuration

- **Default Format** - Choose your preferred output format
- **Output Location** - Set where files are saved
- **Auto-clear** - Remove completed files automatically
- **Notifications** - Get desktop notifications when done

### Advanced

- **Concurrent Processing** - Process multiple files simultaneously
- **File Size Limit** - Set maximum file size
- **Debug Logging** - Enable detailed logs for troubleshooting

### Appearance

- **Theme** - Light or Dark mode (auto-sync with system)
- **Language** - Choose from 11+ supported languages
- **Accent Color** - Customize the app's color scheme
- **Font Size** - Adjust text size for comfort

---

## � Auto-Updates

Harmonix SE can check for updates automatically:

1. Go to **Settings > About**
2. Click **Check for Updates**
3. If an update is available, you'll be prompted to install

Updates are downloaded and installed seamlessly with minimal disruption.

---

## 🎯 Use Cases

**For Musicians:**

- Convert between studio formats (WAV ↔ FLAC)
- Master tracks for streaming platforms
- Normalize loudness across albums

**For Podcasters:**

- Remove silence and optimize audio
- Convert to web-friendly formats (MP3, AAC)
- Ensure consistent volume levels

**For Content Creators:**

- Quick format conversion for video editing
- Audio cleanup and enhancement
- Batch processing for multiple episodes

**For Audio Engineers:**

- Professional LUFS normalization
- Precision audio trimming
- High-quality format preservation

---

## 💡 Tips & Tricks

- **Use Smart Analysis** for automatic optimization
- **Enable concurrent processing** for faster batch conversions
- **Preview audio** with the built-in waveform player before converting
- **Save custom presets** for your most-used settings
- **Check the About page** for keyboard shortcuts

---

## ❓ FAQ

**Q: Do I need to install FFmpeg separately?**  
A: No! FFmpeg is bundled with the app. Everything works out of the box.

**Q: What's the maximum file size?**  
A: Default is 500MB. You can adjust this in Settings > Advanced.

**Q: Can I convert video files?**  
A: Currently only audio files are supported. Video support may come in future updates.

**Q: Is my audio data sent to any servers?**  
A: No. All processing happens locally on your computer. Your files never leave your device.

**Q: The app won't open on macOS. What do I do?**  
A: Right-click the app and select "Open" to bypass Gatekeeper on first launch.

---

## 🛟 Support

**Found a bug?** [Report it on GitHub](https://github.com/h1dr0nn/SoundConverterApp/issues)

**Have a feature request?** [Share your ideas](https://github.com/h1dr0nn/SoundConverterApp/discussions)

**Need help?** Check the [Wiki](https://github.com/h1dr0nn/SoundConverterApp/wiki) or open a discussion

---

## 📝 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and release notes.

---

## � Acknowledgments

| Layer    | Technology                   |
| -------- | ---------------------------- |
| Frontend | React 18, Tailwind CSS, Vite |
| Desktop  | Tauri 2.0                    |
| Backend  | Python 3.12, FFmpeg          |
| Build    | Rust, Node.js                |

---

## � License

MIT License - Free for personal and commercial use.

See [LICENSE](./LICENSE) for details.

---

**Made with ❤️ by h1dr0n**

_Transform your audio workflow with Harmonix SE_
