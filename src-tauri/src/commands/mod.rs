//! IPC commands exposed to the frontend layer.

use crate::core::logging::log_message;
use crate::core::python::{execute_python_conversion, BackendResult, ConvertPayload};

#[tauri::command]
pub fn ping() -> String {
    "pong".to_string()
}

#[tauri::command]
pub async fn convert_audio(
    app: tauri::AppHandle,
    payload: ConvertPayload,
) -> Result<BackendResult, String> {
    log_message(
        "tauri",
        &format!("Received convert_audio with {} files", payload.files.len()),
    );

    let app_handle = app.clone();

    tauri::async_runtime::spawn_blocking(move || execute_python_conversion(app_handle, payload))
        .await
        .map_err(|err| format!("Background task join error: {}", err))?
}

#[tauri::command]
pub async fn analyze_audio(
    app: tauri::AppHandle,
    payload: ConvertPayload,
) -> Result<BackendResult, String> {
    log_message(
        "tauri",
        &format!("Received analyze_audio with {} files", payload.files.len()),
    );

    let app_handle = app.clone();

    // Reuse execute_python_conversion as it handles the JSON IPC
    tauri::async_runtime::spawn_blocking(move || execute_python_conversion(app_handle, payload))
        .await
        .map_err(|err| format!("Background task join error: {}", err))?
}
