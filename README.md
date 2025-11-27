# Harmonix SE

A modern desktop audio converter with an iOS/macOS-inspired UI, built with **Tauri, React, and Python**.

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Beautiful Interface**: iOS/macOS-style UI with glassmorphism, blur effects, and smooth animations
- **Drag & Drop**: Simply drag audio files into the app
- **Multiple Formats**: Convert between MP3, WAV, OGG, FLAC, AAC, WMA, and more
- **Batch Processing**: Convert multiple files simultaneously
- **Real-time Progress**: See conversion progress for each file
- **Light/Dark Mode**: Automatic theme support matching your system
- **Audio Mastering**: Normalize and enhance audio quality with presets
- **Silence Trimming**: Automatically remove silence from the beginning and end of audio files

## 🏗️ Architecture

```
Tauri Desktop App
├── Frontend (React + Tailwind)    → UI Layer
├── Tauri (Rust)                   → Bridge Layer
└── Backend (Python + FFmpeg)      → Processing Logic
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Rust** (for building Tauri)
- **Python** 3.9+
- **FFmpeg** (will be bundled automatically in production builds)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/SoundConverterApp.git
   cd SoundConverterApp
   ```

2. **Install frontend dependencies**:

   ```bash
   cd frontend
   npm install
   ```

3. **Set up Python virtual environment**:

   ```bash
   # Create virtual environment (one-time setup)
   python3 -m venv .venv

   # Activate it
   source .venv/bin/activate  # macOS/Linux
   # Or on Windows: .venv\Scripts\activate
   ```

4. **Install backend dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: Always activate the virtual environment (`source .venv/bin/activate`) before running the backend or tests.

### Development

Run the app in development mode:

```bash
cd frontend
npm run tauri dev
```

This will:

- Start the Vite development server for React
- Launch the Tauri window
- Hot-reload on code changes

### Building for Production

Build the app for your platform:

```bash
cd frontend
npm run tauri build
```

The bundled app will be in `src-tauri/target/release/bundle/`.

### Automated Releases (CI/CD)

The project includes automated multi-platform builds via GitHub Actions:

```bash
# 1. Merge to build branch
git checkout build
git merge main
git push origin build

# 2. Create and push a version tag to trigger release build
git checkout main
git tag v1.0.0
git push origin v1.0.0
```

This will automatically build from the `build` branch for:

- macOS (Apple Silicon + Intel)
- Windows (x64)
- Linux (x64)

See [`.github/RELEASE.md`](./.github/RELEASE.md) for detailed release instructions.

## 🧪 Testing

### Backend Tests

Run Python unit tests:

```bash
cd backend
python -m pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📁 Project Structure

```
SoundConverterApp/
├── frontend/              # React + Tailwind UI
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Main app pages
│   │   ├── hooks/        # Custom React hooks
│   │   └── utils/        # Frontend utilities
│   └── package.json
├── backend/              # Python audio processing
│   ├── app/
│   │   ├── handler/     # Conversion, mastering, trimming
│   │   └── resources/   # FFmpeg binaries
│   ├── main.py          # Backend entrypoint
│   └── utils.py
├── src-tauri/           # Rust/Tauri bridge
│   ├── src/
│   │   ├── commands/   # Tauri commands (IPC)
│   │   └── core/       # Core Tauri logic
│   └── Cargo.toml
└── tests/              # Backend unit tests
```

## 🎨 Design Philosophy

The UI follows Apple's design principles:

- **Glassmorphism**: Blur (24-40px) with semi-transparent layers
- **Rounded Corners**: 12-24px radius for modern feel
- **Smooth Animations**: ≤250ms transitions
- **Clean Typography**: Inter/SF Pro fonts
- **Minimal Shadows**: Soft, subtle depth

## 📖 Documentation

- [**ROADMAP.md**](./ROADMAP.md) - Project milestones and development phases
- [**AGENTS.md**](./AGENTS.md) - Architecture rules and guidelines for contributors

## 🛠️ Technology Stack

| Layer    | Technology                   |
| -------- | ---------------------------- |
| Frontend | React 18, Tailwind CSS, Vite |
| Desktop  | Tauri 1.5                    |
| Backend  | Python 3.9+, FFmpeg          |
| Build    | Rust, Node.js                |

## 🤝 Contributing

Please read [AGENTS.md](./AGENTS.md) for architecture guidelines before contributing.

## 📝 License

MIT License - feel free to use this project for learning or personal use.

---

**Status**: Phase 3 Complete ✅ | Packaging & CI/CD in progress
