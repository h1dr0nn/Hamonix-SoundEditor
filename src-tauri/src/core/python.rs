//! Python backend integration module.

use crate::core::logging::log_message;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;
use std::process::{Command, Stdio};
use tauri::Manager;

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
    let (python_cmd, backend_path) = resolve_python(&app)?;

    let json_input = serde_json::to_string(&serde_json::json!({
        "operation": "convert",
        "files": payload.files,
        "format": payload.format,
        "output": payload.output,
    }))
    .map_err(|e| format!("Failed to serialize request: {}", e))?;

    log_message(
        "tauri",
        &format!("Spawning python backend at {}", backend_path.display()),
    );

    let mut child = Command::new(&python_cmd)
        .arg(&backend_path)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
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

fn resolve_python(app: &tauri::AppHandle) -> Result<(String, PathBuf), String> {
    let python_candidates = [
        app.path_resolver().resolve_resource("bin/python"),
        app.path_resolver().resolve_resource("bin/python.exe"),
        app.path_resolver().resolve_resource("src-tauri/bin/python"),
        app.path_resolver()
            .resolve_resource("src-tauri/bin/python.exe"),
    ];

    let python_bin = python_candidates
        .iter()
        .flatten()
        .find(|path| path.exists())
        .map(|path| path.to_string_lossy().to_string())
        .unwrap_or_else(|| "python3".to_string());

    let backend_path = app
        .path_resolver()
        .resolve_resource("backend/main.py")
        .unwrap_or_else(|| PathBuf::from("backend/main.py"));

    if !backend_path.exists() {
        return Err("Unable to locate backend/main.py".to_string());
    }

    Ok((python_bin, backend_path))
}
