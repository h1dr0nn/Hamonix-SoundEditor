//! IPC commands exposed to the frontend layer.

use crate::core::python::{execute_python_backend, ConversionRequest, ConversionResponse};

#[tauri::command]
pub fn ping() -> String {
    "pong".to_string()
}

#[tauri::command]
pub async fn convert_audio(
    operation: String,
    input_paths: Vec<String>,
    output_directory: String,
    output_format: Option<String>,
) -> Result<ConversionResponse, String> {
    let request = ConversionRequest {
        operation,
        input_paths,
        output_directory,
        output_format,
    };

    execute_python_backend(&request)
}
