//! Python backend integration module.

use serde::{Deserialize, Serialize};
use std::process::{Command, Stdio};
use std::io::Write;

#[derive(Debug, Serialize, Deserialize)]
pub struct ConversionRequest {
    pub operation: String,
    pub input_paths: Vec<String>,
    pub output_directory: String,
    pub output_format: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ConversionResponse {
    pub status: String,
    pub message: String,
    pub outputs: Vec<String>,
}

/// Execute Python backend with JSON input via stdin
pub fn execute_python_backend(request: &ConversionRequest) -> Result<ConversionResponse, String> {
    // Get the path to the Python backend
    // In development: use python from PATH
    // In production: use bundled python from resources
    let python_cmd = if cfg!(debug_assertions) {
        "python"
    } else {
        // TODO: Point to bundled Python in production
        "python"
    };

    let backend_path = if cfg!(debug_assertions) {
        // Development: relative to project root
        "backend/main.py"
    } else {
        // Production: relative to app bundle
        // TODO: Update this path for production
        "backend/main.py"
    };

    // Serialize request to JSON
    let json_input = serde_json::to_string(request)
        .map_err(|e| format!("Failed to serialize request: {}", e))?;

    // Spawn Python process
    let mut child = Command::new(python_cmd)
        .arg(backend_path)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn Python process: {}", e))?;

    // Write JSON to stdin
    if let Some(mut stdin) = child.stdin.take() {
        stdin
            .write_all(json_input.as_bytes())
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;
    }

    // Wait for process to complete and capture output
    let output = child
        .wait_with_output()
        .map_err(|e| format!("Failed to wait for Python process: {}", e))?;

    // Parse stdout as JSON
    let stdout_str = String::from_utf8_lossy(&output.stdout);
    
    if !output.status.success() {
        let stderr_str = String::from_utf8_lossy(&output.stderr);
        return Err(format!(
            "Python process failed with exit code {:?}\nStdout: {}\nStderr: {}",
            output.status.code(),
            stdout_str,
            stderr_str
        ));
    }

    // Parse response
    serde_json::from_str(&stdout_str)
        .map_err(|e| format!("Failed to parse Python response: {}\nOutput: {}", e, stdout_str))
}
