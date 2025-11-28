#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod commands;
mod core;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_notification::init())
        .invoke_handler(tauri::generate_handler![
            commands::ping,
            commands::convert_audio
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
