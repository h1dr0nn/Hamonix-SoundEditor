# Phase 1 IPC Implementation

## Overview

This document describes the IPC (Inter-Process Communication) bridge that connects React → Tauri → Python → Tauri → React.

## Architecture

```
┌─────────────┐
│   React UI  │
└──────┬──────┘
       │ invoke('convert_audio', {...})
       ▼
┌─────────────────────┐
│   Tauri (Rust)      │
│  ┌───────────────┐  │
│  │ commands/     │  │
│  │ convert_audio │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ core/python   │  │
│  │ execute_...   │  │
│  └───────┬───────┘  │
└──────────┼──────────┘
           │ spawn process + JSON stdin
           ▼
    ┌──────────────┐
    │ Python       │
    │ backend/     │
    │ main.py      │
    └──────────────┘
```

## Implementation Details

### 1. Tauri Command (`src-tauri/src/commands/mod.rs`)

```rust
#[tauri::command]
pub async fn convert_audio(
    operation: String,
    input_paths: Vec<String>,
    output_directory: String,
    output_format: Option<String>,
) -> Result<ConversionResponse, String>
```

**Usage from React:**
```typescript
import { invoke } from '@tauri-apps/api/tauri';

const result = await invoke('convert_audio', {
  operation: 'convert',
  inputPaths: ['/path/to/file.wav'],
  outputDirectory: '/path/to/output',
  outputFormat: 'mp3'
});
```

### 2. Python Integration (`src-tauri/src/core/python.rs`)

**Key Function:**
```rust
pub fn execute_python_backend(request: &ConversionRequest) 
    -> Result<ConversionResponse, String>
```

**Process:**
1. Spawns `python backend/main.py` as subprocess
2. Writes JSON request to stdin
3. Reads JSON response from stdout
4. Returns parsed response to Tauri command

### 3. Python Backend (`backend/main.py`)

**Input Format (stdin):**
```json
{
  "operation": "convert",
  "input_paths": ["/path/to/file.wav"],
  "output_directory": "/path/to/output",
  "output_format": "mp3"
}
```

**Output Format (stdout):**
```json
{
  "status": "success",
  "message": "Converted 1 files into /path/to/output",
  "outputs": ["/path/to/output/file.mp3"]
}
```

## Data Flow

1. **User Action**: User selects files and clicks convert in React UI
2. **React → Tauri**: `invoke('convert_audio', {...})`
3. **Tauri → Python**: Spawn subprocess, send JSON via stdin
4. **Python Processing**: Read JSON, convert files, write JSON to stdout
5. **Python → Tauri**: Parse JSON response
6. **Tauri → React**: Return result to frontend
7. **UI Update**: Display success/error message

## Error Handling

- **Python spawn failure**: Returns error with spawn details
- **Python process failure**: Returns exit code + stderr
- **JSON parse error**: Returns parsing error with raw output
- **Audio processing error**: Python returns `{"status": "error", ...}`

## Testing

To test the IPC bridge:

```bash
# 1. Build Tauri (requires Rust)
cd src-tauri
cargo build

# 2. Run Tauri dev
npm run tauri dev

# 3. In React, call:
const result = await invoke('convert_audio', {
  operation: 'convert',
  inputPaths: ['test.wav'],
  outputDirectory: './output',
  outputFormat: 'mp3'
});
```

## Production Considerations

### Bundled Python
In production, update `core/python.rs` to use bundled Python:

```rust
let python_cmd = if cfg!(debug_assertions) {
    "python"
} else {
    // Point to bundled Python
    app_handle.path_resolver()
        .resolve_resource("bin/python/python.exe")
        .unwrap()
};
```

### Bundled Backend
Update backend path for production:

```rust
let backend_path = if cfg!(debug_assertions) {
    "backend/main.py"
} else {
    app_handle.path_resolver()
        .resolve_resource("backend/main.py")
        .unwrap()
};
```

## Phase 1 Completion

✅ All Phase 1 tasks complete:
- [x] Init repo structure
- [x] Setup Tauri + React + Tailwind
- [x] Setup Python backend
- [x] **IPC bridge: React ↔ Tauri ↔ Python** ← Just completed
- [x] File drag-and-drop UI

**Next**: Phase 2 - UI/UX (iOS/macOS style)
