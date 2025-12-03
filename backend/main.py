"""Minimal backend entrypoint for Phase 1 foundation setup.

This module acts as the CLI entrypoint for the audio conversion backend.
It reads a JSON object from stdin, executes the conversion, and prints
JSON updates to stdout.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from typing import Optional, Dict, Any, Union

# Add vendor directory to Python path for bundled dependencies (e.g., pydub)
# This ensures dependencies installed via `pip install --target backend/vendor`
# are available at runtime when bundled with Tauri
_vendor_dir = Path(__file__).parent / "vendor"
if _vendor_dir.exists():
    sys.path.insert(0, str(_vendor_dir))

from app.handler.converter import ConversionProgress, ConversionRequest, SoundConverter
from app.handler.mastering import MasteringEngine, MasteringParameters, MasteringRequest
from app.handler.modifier import ModificationRequest, process as process_modification
from app.handler.trimmer import SilenceTrimmer, TrimRequest
from utils import ensure_ffmpeg, log_message

# Import new modules
from app.validators.audio_validator import validate_audio_file
from app.validators.parameter_validator import (
    validate_conversion_params,
    validate_mastering_params,
    validate_trim_params,
    validate_modify_params
)
from app.formatters.output_formatter import (
    format_success,
    format_error,
    format_progress
)
from app.exceptions.base import HarmonixError


def emit_progress(progress: Union[ConversionProgress, Dict[str, Any]]) -> None:
    """Emit progress updates to stdout as JSON.
    
    Args:
        progress: ConversionProgress object or dictionary with progress data.
    """
    if isinstance(progress, ConversionProgress):
        payload = {
            "event": "progress",
            "status": progress.status,
            "index": progress.index,
            "total": progress.total,
            "file": str(progress.source),
            "destination": str(progress.destination),
        }
    else:
        payload = progress

    print(json.dumps(payload))
    sys.stdout.flush()


def main() -> None:
    """Read JSON from stdin, run conversion, and print result."""

    # 1. Setup environment
    ffmpeg_path = ensure_ffmpeg()
    log_message("python", f"Backend initialized (ffmpeg={ffmpeg_path})")

    # 2. Read input
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            # If no input, just print ready message (for health checks)
            print(json.dumps({"status": "ready", "message": "Backend ready"}))
            return

        data = json.loads(raw_input)
    except json.JSONDecodeError as e:
        print(json.dumps(format_error("init", f"Invalid JSON input: {e}", "JSON_ERROR")))
        sys.exit(1)
    except Exception as e:
        print(json.dumps(format_error("init", f"Input error: {e}", "INPUT_ERROR")))
        sys.exit(1)

    # 3. Determine operation type
    operation = data.get("operation", "convert")

    try:
        result = None
        if operation == "convert":
            result = handle_conversion(data, ffmpeg_path)
            if result is None or result.get("status") != "success":
                sys.exit(1)
            return
        elif operation == "master":
            result = handle_mastering(data)
        elif operation == "trim":
            result = handle_trimming(data)
        elif operation == "modify":
            result = handle_modification(data)
        elif operation == "analyze":
            result = handle_analysis(data)
        else:
            print(json.dumps(format_error("init", f"Unknown operation: {operation}", "INVALID_OPERATION")))
            sys.exit(1)

        if result is not None:
            print(json.dumps(result))
            sys.stdout.flush()

        if result is None or result.get("status") != "success":
            sys.exit(1)

    except HarmonixError as he:
        # Handle known custom exceptions
        print(json.dumps(format_error(operation, he.message, he.code, he.details)))
        sys.exit(1)
    except Exception as e:
        # Handle unexpected exceptions
        print(json.dumps(format_error(
            operation, 
            str(e), 
            "FATAL_ERROR", 
            {"traceback": traceback.format_exc()}
        )))
        sys.exit(1)


def handle_conversion(data: Dict[str, Any], ffmpeg_path: Optional[Path]) -> Optional[Dict[str, Any]]:
    """Handle audio conversion request.
    
    Args:
        data: Request data dictionary.
        ffmpeg_path: Path to FFmpeg binary.
        
    Returns:
        Result dictionary or None if failed.
    """
    input_paths = [Path(p) for p in data.get("files", data.get("input_paths", []))]
    output_directory = Path(data.get("output") or data.get("output_directory") or ".")
    output_format = data.get("format") or data.get("output_format", "mp3")
    overwrite = data.get("overwrite_existing", True)
    concurrent_files = data.get("concurrent_files", 1)

    # Validate parameters
    params_to_validate = {
        "format": output_format,
        "concurrent_files": concurrent_files
    }
    is_valid, error = validate_conversion_params(params_to_validate)
    if not is_valid:
        emit_progress(format_error("convert", str(error), "VALIDATION_ERROR"))
        return None

    log_message(
        "python",
        f"Received conversion request (files={len(input_paths)}, format={output_format}, output={output_directory}, concurrent={concurrent_files})",
    )

    request = ConversionRequest(
        input_paths=input_paths,
        output_directory=output_directory,
        output_format=output_format,
        overwrite_existing=overwrite,
        ffmpeg_path=ffmpeg_path,
    )

    try:
        result = SoundConverter.convert(
            request,
            progress_callback=lambda progress: emit_progress(progress),
            log_callback=lambda line: log_message("ffmpeg", line),
        )
    except Exception as exc:
        log_message("python", f"Fatal error during conversion: {exc}")
        emit_progress(format_error("convert", str(exc), "CONVERSION_FATAL"))
        return None

    status = "success" if result.success else "error"
    response_data = {
        "event": "complete",
        "status": status,
        "message": result.message,
        "outputs": [str(p) for p in result.outputs],
        "operation_type": "convert"
    }
    emit_progress(response_data)

    return {
        "status": status,
        "message": result.message,
        "outputs": [str(p) for p in result.outputs],
        "operation_type": "convert"
    }


def handle_mastering(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle audio mastering request."""
    input_paths = [Path(p) for p in data.get("input_paths", [])]
    output_directory = Path(data.get("output_directory", "."))
    preset = data.get("preset", "Music")
    overwrite = data.get("overwrite_existing", True)
    
    # Parse parameters
    params_data = data.get("parameters", {})
    
    # Validate
    validation_params = {"preset": preset.lower(), **params_data}
    is_valid, error = validate_mastering_params(validation_params)
    if not is_valid:
        return format_error("master", str(error), "VALIDATION_ERROR")

    parameters = MasteringParameters(
        target_lufs=params_data.get("target_lufs", -14.0),
        apply_compression=params_data.get("apply_compression", True),
        apply_limiter=params_data.get("apply_limiter", True),
        output_gain=params_data.get("output_gain", 0.0)
    )

    request = MasteringRequest(
        input_paths=input_paths,
        output_directory=output_directory,
        preset=preset,
        parameters=parameters,
        overwrite_existing=overwrite
    )

    result = MasteringEngine.process(request)
    
    status = "success" if result.success else "error"
    response_data = {
        "event": "complete",
        "status": status,
        "message": result.message,
        "outputs": [str(p) for p in result.outputs],
        "operation_type": "master"
    }
    emit_progress(response_data)
    
    return {
        "status": status,
        "message": result.message,
        "outputs": [str(p) for p in result.outputs],
        "operation_type": "master"
    }


def handle_trimming(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle silence trimming request."""
    input_paths = [Path(p) for p in data.get("input_paths", [])]
    output_directory = Path(data.get("output_directory", "."))
    silence_threshold = data.get("silence_threshold", -50.0)
    minimum_silence_ms = data.get("minimum_silence_ms", 500)
    padding_ms = data.get("padding_ms", 0)
    overwrite = data.get("overwrite_existing", True)

    # Validate
    validation_params = {
        "threshold": silence_threshold,
        "min_silence_len": minimum_silence_ms
    }
    is_valid, error = validate_trim_params(validation_params)
    if not is_valid:
        return format_error("trim", str(error), "VALIDATION_ERROR")

    request = TrimRequest(
        input_paths=input_paths,
        output_directory=output_directory,
        silence_threshold=silence_threshold,
        minimum_silence_ms=minimum_silence_ms,
        padding_ms=padding_ms,
        overwrite_existing=overwrite
    )

    result = SilenceTrimmer.process(request)

    status = "success" if result.success else "error"
    response_data = {
        "event": "complete",
        "status": status,
        "message": result.message,
        "outputs": [str(p) for p in result.outputs],
        "operation_type": "trim"
    }
    emit_progress(response_data)

    return {
        "status": status,
        "message": result.message,
        "outputs": [str(p) for p in result.outputs],
        "operation_type": "trim"
    }


def handle_modification(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle audio modification request."""
    input_paths = [Path(p) for p in data.get("input_paths", [])]
    output_directory = Path(data.get("output_directory", "."))
    speed = float(data.get("speed", 1.0))
    pitch = int(data.get("pitch", 0))
    cut_start = float(data.get("cut_start", 0.0))
    cut_end = float(data.get("cut_end", 100.0))

    # Validate
    validation_params = {"speed": speed, "pitch": pitch}
    is_valid, error = validate_modify_params(validation_params)
    if not is_valid:
        return format_error("modify", str(error), "VALIDATION_ERROR")

    request = ModificationRequest(
        input_paths=input_paths,
        output_directory=output_directory,
        speed=speed,
        pitch=pitch,
        cut_start=cut_start,
        cut_end=cut_end
    )

    try:
        outputs = process_modification(request)
        response_data = {
            "event": "complete",
            "status": "success",
            "message": f"Modified {len(outputs)} files",
            "outputs": [str(p) for p in outputs],
            "operation_type": "modify"
        }
        emit_progress(response_data)
        return {
            "status": "success",
            "message": f"Modified {len(outputs)} files",
            "outputs": [str(p) for p in outputs],
            "operation_type": "modify"
        }
    except Exception as e:
        error_response = format_error("modify", str(e), "MODIFICATION_ERROR")
        error_response["event"] = "complete"
        emit_progress(error_response)
        return error_response


def handle_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle audio analysis request."""
    input_paths = [Path(p) for p in data.get("files", data.get("input_paths", []))]
    if not input_paths:
        return format_error("analyze", "No input files provided", "NO_INPUT")

    ffmpeg_path = ensure_ffmpeg()
    if not ffmpeg_path:
        log_message("python", "FFmpeg not found during analysis")
        return format_error("analyze", "FFmpeg not found", "FFMPEG_MISSING")

    log_message("python", f"Starting analysis with ffmpeg: {ffmpeg_path}")
    ffprobe_path = ffmpeg_path.parent / ("ffprobe.exe" if sys.platform == "win32" else "ffprobe")
    
    # Fallback: try system ffprobe if bundled one not found
    if not ffprobe_path.exists():
        ffprobe_path = Path("ffprobe")

    results = []
    import subprocess
    import re

    def analyze_with_ffmpeg(ffmpeg_bin: Path, file_path: Path) -> Optional[Dict[str, Any]]:
        """Fallback analysis using ffmpeg stderr output."""
        try:
            # Run ffmpeg -i input -f null -
            # This prints metadata to stderr
            cmd = [str(ffmpeg_bin), "-i", str(file_path), "-f", "null", "-"]
            process = subprocess.run(cmd, capture_output=True, text=True)
            output = process.stderr

            # Parse Duration and bitrate
            # Duration: 00:03:30.05, start: 0.000000, bitrate: 128 kb/s
            duration_match = re.search(r"Duration:\s+(\d{2}):(\d{2}):(\d{2}\.\d+)", output)
            bitrate_match = re.search(r"bitrate:\s+(\d+)\s+kb/s", output)
            
            duration = 0.0
            if duration_match:
                h, m, s = map(float, duration_match.groups())
                duration = h * 3600 + m * 60 + s
            
            bit_rate = int(bitrate_match.group(1)) * 1000 if bitrate_match else 0

            # Parse Stream info for Audio
            # Stream #0:0: Audio: aac (LC), 44100 Hz, stereo, fltp, 128 kb/s
            audio_match = re.search(r"Stream.*Audio:.*,\s+(\d+)\s+Hz,\s+([^,]+),", output)
            
            sample_rate = 0
            channels = 0
            codec = "unknown"
            
            if audio_match:
                sample_rate = int(audio_match.group(1))
                channel_str = audio_match.group(2)
                if "stereo" in channel_str:
                    channels = 2
                elif "mono" in channel_str:
                    channels = 1
                else:
                    # Try to extract numeric channel count or default to 0 (unknown)
                    channels = 0
                
                # Extract codec from the part before Hz
                # Stream #0:0: Audio: aac (LC), ...
                codec_match = re.search(r"Stream.*Audio:\s+([^,]+),", output)
                if codec_match:
                    codec = codec_match.group(1).split()[0]

            return {
                "file": str(file_path),
                "duration": duration,
                "bit_rate": bit_rate,
                "channels": channels,
                "sample_rate": sample_rate,
                "codec": codec
            }
        except Exception as e:
            log_message("python", f"FFmpeg fallback analysis failed: {e}")
            return None

    for file_path in input_paths:
        analysis = None
        
        # Try ffprobe first
        try:
            cmd = [
                str(ffprobe_path),
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path)
            ]
            
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0:
                probe_data = json.loads(process.stdout)
                format_info = probe_data.get("format", {})
                streams = probe_data.get("streams", [])
                audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
                
                analysis = {
                    "file": str(file_path),
                    "duration": float(format_info.get("duration", 0)),
                    "bit_rate": int(format_info.get("bit_rate", 0)),
                    "channels": int(audio_stream.get("channels", 0)),
                    "sample_rate": int(audio_stream.get("sample_rate", 0)),
                    "codec": audio_stream.get("codec_name", "unknown")
                }
        except Exception:
            pass
        
        # Fallback to ffmpeg if ffprobe failed
        if not analysis:
            analysis = analyze_with_ffmpeg(ffmpeg_path, file_path)

        if analysis:
            # Simple heuristic for suggestion
            suggestion = "Music"
            if analysis["channels"] == 1 or analysis["bit_rate"] < 96000:
                suggestion = "Voice-over"
            elif analysis["duration"] > 600: # > 10 mins
                suggestion = "Podcast"
                
            analysis["suggestion"] = suggestion
            results.append(analysis)
        else:
            results.append({
                "file": str(file_path),
                "error": "Analysis failed"
            })

    return {
        "event": "complete",
        "status": "success",
        "message": "Analysis complete",
        "outputs": [],
        "data": results,
        "operation_type": "analyze"
    }


if __name__ == "__main__":
    main()
