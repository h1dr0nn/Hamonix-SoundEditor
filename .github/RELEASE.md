# CI/CD Release Guide

This document explains how to use the automated release pipeline for **Harmonix SE**.

## Overview

The CI/CD pipeline is configured in `.github/workflows/release.yml` and automatically builds releases for:

- **macOS** (Apple Silicon + Intel)
- **Windows** (x64)
- **Linux** (x64)

## Triggering a Release

### Important: Build Branch Required

The CI/CD workflow **always builds from the `build` branch**, regardless of where you push the tag. This ensures consistent, production-ready code.

**Workflow**:

1. Merge your changes into the `build` branch
2. Push a version tag from any branch (usually `main`)
3. CI/CD automatically checks out `build` branch for building

### 1. Prepare the Build Branch

```bash
# Update build branch with latest main
git checkout build
git merge main
git push origin build
```

### 2. Create and Push Version Tag

```bash
# From any branch (usually main)
git checkout main
git tag v1.0.0
git push origin v1.0.0
```

### 2. Automatic Build Process

The workflow will automatically:

1. Create a GitHub Release draft
2. Build for all platforms in parallel
3. Download and embed Python runtime + FFmpeg
4. Install backend dependencies in bundled Python
5. Package artifacts in platform-specific formats
6. Upload all artifacts to the GitHub Release

### 3. Monitor Progress

Go to: `https://github.com/your-username/SoundConverterApp/actions`

You can monitor each build job:

- **build-macos** (runs twice: arm64 and x64)
- **build-windows**
- **build-linux**

## Artifacts Produced

### macOS

- `Harmonix-SE-v1.0.0-macOS-arm64.app.tar.gz` (Apple Silicon)
- `Harmonix-SE-v1.0.0-macOS-x64.app.tar.gz` (Intel)

### Windows

- `Harmonix-SE-v1.0.0-Windows-x64.msi` (MSI Installer)
- `Harmonix-SE-v1.0.0-Windows-x64_setup.exe` (NSIS Installer)
- `Harmonix-SE-v1.0.0-Windows-x64.exe` (Portable)

### Linux

- `Harmonix-SE-v1.0.0-Linux-x64.AppImage` (Portable)
- `Harmonix-SE-v1.0.0-Linux-x64.deb` (Debian/Ubuntu)

## Manual Trigger (Testing)

You can also manually trigger the workflow from GitHub Actions UI:

1. Go to Actions → Release Build
2. Click "Run workflow"
3. Select branch
4. Click "Run workflow"

## Troubleshooting

### Build Failures

If a build fails:

1. Check the job logs in GitHub Actions
2. Build logs are automatically uploaded as artifacts on failure
3. Download `build-logs-{platform}` from the failed workflow run

### Common Issues

**Python not found**:

- Check that `download-binaries.sh` ran successfully
- Verify Python was downloaded to `src-tauri/binaries/python-{target}/`

**FFmpeg not found**:

- Check that FFmpeg was downloaded to `src-tauri/binaries/ffmpeg-{target}`
- Verify executable permissions

**Backend dependencies failed**:

- Check if `requirements.txt` is present
- Verify Python pip is working

## Code Signing (Optional)

To enable code signing:

1. Generate a Tauri signing key:

   ```bash
   tauri signer generate
   ```

2. Add secrets to GitHub repository:
   - `TAURI_PRIVATE_KEY`: Your private key
   - `TAURI_KEY_PASSWORD`: Your password

The workflow will automatically use these if present.

## Testing Locally

Before pushing a tag, you can test the build process locally:

```bash
# Download binaries
chmod +x scripts/download-binaries.sh
./scripts/download-binaries.sh

# Install backend dependencies
./src-tauri/binaries/python-{your-target}/bin/python3 -m pip install -r requirements.txt

# Build
cd frontend
npm run tauri build
```

## Release Checklist

Before creating a release tag:

- [ ] Update version in `tauri.conf.json`
- [ ] Update version in `Cargo.toml`
- [ ] Update version in `frontend/package.json`
- [ ] Update version in `SettingsPage.jsx` (About tab)
- [ ] Test app locally on your platform
- [ ] Create and push version tag
- [ ] Wait for CI/CD to complete
- [ ] Test downloaded artifacts
- [ ] Publish the GitHub Release (if draft)

## Notes

- Builds run on GitHub-hosted runners (free for public repos)
- Each build takes approximately 10-20 minutes
- The workflow uses caching to speed up subsequent builds
- All three platforms build in parallel
