//! Python backend integration module.

use crate::core::logging::log_message;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use tauri::Manager;

#[derive(Debug)]
struct PythonResolution {
    command: PathBuf,
    backend_path: PathBuf,
    bin_dir: Option<PathBuf>,
    python_home: Option<PathBuf>,
    uses_embedded: bool,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ConvertPayload {
    pub files: Vec<String>,
    pub format: String,
    pub output: String,
}

#[derive(Debug, Serialize, Deserialize, Clone, Default)]
pub struct BackendResult {
    pub status: String,
    pub message: String,
    #[serde(default)]
    pub outputs: Vec<String>,
}

/// Execute Python backend with JSON input via stdin and stream progress events.
pub fn execute_python_conversion(
    app: tauri::AppHandle,
    payload: ConvertPayload,
) -> Result<BackendResult, String> {
    let resolution = resolve_python(&app)?;

    let json_input = serde_json::to_string(&serde_json::json!({
        "operation": "convert",
        "files": payload.files,
        "format": payload.format,
        "output": payload.output,
    }))
    .map_err(|e| format!("Failed to serialize request: {}", e))?;

    log_message(
        "tauri",
        &format!(
            "Spawning python backend at {} (embedded={})",
            resolution.backend_path.display(),
            resolution.uses_embedded,
        ),
    );

    let mut command = Command::new(&resolution.command);
    command
        .arg(&resolution.backend_path)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());

    if let Some(bin_dir) = resolution.bin_dir.as_ref() {
        let bin_dir_str = bin_dir.to_string_lossy().to_string();
        command.env("SOUNDCONVERTER_BIN_DIR", &bin_dir_str);

        if let Some(path) = std::env::var_os("PATH") {
            let mut entries = std::env::split_paths(&path).collect::<Vec<_>>();
            if !entries.contains(bin_dir) {
                entries.insert(0, bin_dir.clone());
                let merged = std::env::join_paths(entries)
                    .map_err(|e| format!("Unable to join PATH entries: {}", e))?;
                command.env("PATH", merged);
            }
        } else {
            command.env("PATH", &bin_dir_str);
        }
    }

    if let Some(python_home) = resolution.python_home.as_ref() {
        command.env("PYTHONHOME", python_home);
    }

    command
        .env("PYTHONUNBUFFERED", "1")
        .env("PYTHONDONTWRITEBYTECODE", "1");

    let mut child = command
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;

    if let Some(mut stdin) = child.stdin.take() {
        stdin
            .write_all(json_input.as_bytes())
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
    }

    let stderr_handle = child.stderr.take().map(|stderr| {
        std::thread::spawn(move || {
            let reader = BufReader::new(stderr);
            for line in reader.lines() {
                if let Ok(text) = line {
                    log_message("python", &text);
                }
            }
        })
    });

    let mut final_result: Option<BackendResult> = None;
    let mut last_stdout = String::new();

    if let Some(stdout) = child.stdout.take() {
        let reader = BufReader::new(stdout);
        for line in reader.lines() {
            if let Ok(mut text) = line {
                if text.trim().is_empty() {
                    continue;
                }

                text = text.trim().to_string();
                last_stdout = text.clone();

                match serde_json::from_str::<Value>(&text) {
                    Ok(value) => {
                        if let Err(err) = app.emit_all("conversion-progress", value.clone()) {
                            log_message(
                                "tauri",
                                &format!("Failed to emit progress event: {}", err),
                            );
                        }

                        if let Some(status) = value
                            .get("event")
                            .and_then(|event| event.as_str())
                            .filter(|event| *event == "complete")
                        {
                            let outputs = value
                                .get("outputs")
                                .and_then(|raw| serde_json::from_value(raw.clone()).ok())
                                .unwrap_or_default();
                            let message = value
                                .get("message")
                                .and_then(|raw| raw.as_str())
                                .unwrap_or_default()
                                .to_string();

                            final_result = Some(BackendResult {
                                status: value
                                    .get("status")
                                    .and_then(|s| s.as_str())
                                    .unwrap_or(status)
                                    .to_string(),
                                message,
                                outputs,
                            });
                        }
                    }
                    Err(err) => {
                        log_message(
                            "tauri",
                            &format!("Failed to parse python output '{}': {}", text, err),
                        );
                    }
                }
            }
        }
    }

    if let Some(handle) = stderr_handle {
        let _ = handle.join();
    }

    let status = child
        .wait()
        .map_err(|e| format!("Failed to wait for Python process: {}", e))?;

    if !status.success() {
        let code = status.code().unwrap_or(-1);
        let message = if last_stdout.is_empty() {
            format!("Python process failed with exit code {}", code)
        } else {
            format!(
                "Python process failed with exit code {}: {}",
                code, last_stdout
            )
        };
        return Err(message);
    }

    final_result.ok_or_else(|| "Python backend did not return a final status".to_string())
}

fn resolve_python(app: &tauri::AppHandle) -> Result<PythonResolution, String> {
    let backend_path = app
        .path_resolver()
        .resolve_resource("backend/main.py")
        .unwrap_or_else(|| PathBuf::from("backend/main.py"));

    if !backend_path.exists() {
        return Err("Unable to locate backend/main.py".to_string());
    }

    let bin_root_candidates = [
        app.path_resolver().resolve_resource("bin"),
        app.path_resolver().resolve_resource("src-tauri/bin"),
    ];

    let bin_root = bin_root_candidates
        .into_iter()
        .flatten()
        .find(|path| path.exists());
    let python_candidates = bin_root
        .iter()
        .flat_map(|bin_root| embedded_python_candidates(bin_root))
        .collect::<Vec<_>>();

    let embedded_python = python_candidates.iter().find(|path| path.exists());

    let uses_embedded = embedded_python.is_some();
    let python_cmd = embedded_python
        .cloned()
        .or_else(|| {
            if cfg!(debug_assertions) {
                log_message(
                    "tauri",
                    "Embedded python runtime was not found. Falling back to system python for dev build.",
                );
                Some(PathBuf::from("python3"))
            } else {
                None
            }
        })
        .ok_or_else(|| {
            "Embedded Python runtime missing. Place it under src-tauri/bin/python".to_string()
        })?;

    let python_home = embedded_python
        .as_ref()
        .and_then(|bin| derive_python_home(bin.as_path()));

    Ok(PythonResolution {
        command: python_cmd,
        backend_path,
        bin_dir: bin_root,
        python_home,
        uses_embedded,
    })
}

fn embedded_python_candidates(bin_root: &Path) -> Vec<PathBuf> {
    let python_dir = bin_root.join("python");
    vec![
        python_dir.join("python.exe"),
        python_dir.join("python"),
        python_dir.join("python3"),
        python_dir.join("bin").join("python3"),
        python_dir.join("bin").join("python"),
    ]
}

fn derive_python_home(python_bin: &Path) -> Option<PathBuf> {
    let parent = python_bin.parent()?;

    if parent.file_name().is_some_and(|name| name == "bin") {
        parent.parent().map(|path| path.to_path_buf())
    } else {
        Some(parent.to_path_buf())
    }
}
