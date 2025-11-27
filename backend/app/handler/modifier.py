"""Audio modification logic (Speed, Pitch, Cut)."""

from __future__ import annotations

import math
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Tuple

from ..ffmpeg_runner import (
    AudioProcessingError,
    ExportFailureError,
    MissingEncoderError,
    resolve_environment,
    validate_input_paths,
)


@dataclass(frozen=True)
class ModificationRequest:
    """Data container describing a batch modification job."""

    input_paths: list[Path]
    output_directory: Path
    speed: float
    pitch: int  # semitones
    cut_start: float  # percentage 0-100
    cut_end: float  # percentage 0-100
    ffmpeg_path: Optional[Path] = None

    def outputs(self) -> Iterable[Tuple[Path, Path]]:
        """Yield tuples of ``(input_path, output_path)`` for the batch."""
        allocated: set[Path] = set()

        for source in self.input_paths:
            # Output format defaults to wav for modification to preserve quality before final conversion
            # or we can keep original extension if possible. Let's use wav for safety/compatibility.
            # Or better, keep original extension if supported, but changing speed/pitch might require re-encoding.
            # Let's default to .wav for now as intermediate/final output.
            base_destination = self.output_directory / f"{source.stem}_modified.wav"
            destination = base_destination

            candidate = base_destination
            index = 1
            while candidate.exists() or candidate in allocated:
                candidate = base_destination.with_stem(
                    f"{base_destination.stem} ({index})"
                )
                index += 1
            destination = candidate

            allocated.add(destination)
            yield source, destination


def get_audio_info(file_path: Path, ffmpeg_path: str = "ffmpeg") -> dict:
    """Get duration and sample rate using ffprobe."""
    # We assume ffprobe is next to ffmpeg or in path
    ffprobe_path = "ffprobe"
    if ffmpeg_path != "ffmpeg":
        probe_candidate = Path(ffmpeg_path).parent / "ffprobe"
        if probe_candidate.exists():
            ffprobe_path = str(probe_candidate)
        elif Path(ffmpeg_path).with_name("ffprobe.exe").exists():
             ffprobe_path = str(Path(ffmpeg_path).with_name("ffprobe.exe"))

    cmd = [
        ffprobe_path,
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=duration,sample_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    
    try:
        # On Windows, creationflags=0x08000000 prevents cmd window popping up
        creationflags = 0
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            creationflags = subprocess.CREATE_NO_WINDOW
            
        output = subprocess.check_output(cmd, creationflags=creationflags).decode().strip().split('\n')
        
        # Output order depends on show_entries, usually sample_rate then duration or vice versa
        # But since we requested specific entries, let's parse carefully.
        # Actually ffprobe output order is consistent with request order? Not always.
        # Let's use csv format for easier parsing or json.
        
        # Retry with json for reliability
        cmd = [
            ffprobe_path,
            "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=duration,sample_rate",
            "-of", "json",
            str(file_path)
        ]
        import json
        output = subprocess.check_output(cmd, creationflags=creationflags).decode()
        data = json.loads(output)
        stream = data["streams"][0]
        return {
            "duration": float(stream.get("duration", 0)),
            "sample_rate": int(stream.get("sample_rate", 44100))
        }
    except Exception as e:
        print(f"Error probing file {file_path}: {e}")
        return {"duration": 0, "sample_rate": 44100}


def build_filter_complex(speed: float, pitch: int, sample_rate: int) -> str:
    """Build FFmpeg filter complex for speed and pitch."""
    filters = []
    
    # Pitch Shift (Time-Stretch + Resample)
    # To change pitch without changing speed:
    # 1. Change speed and pitch together using asetrate (resampling)
    # 2. Counteract speed change using atempo
    
    # Formula:
    # ratio = 2^(semitones/12)
    # new_rate = sample_rate * ratio
    # tempo_correction = 1 / ratio
    
    pitch_ratio = 2 ** (pitch / 12.0)
    new_sample_rate = int(sample_rate * pitch_ratio)
    
    if pitch != 0:
        filters.append(f"asetrate={new_sample_rate}")
        
        # Counteract speed change from asetrate
        tempo_correction = 1.0 / pitch_ratio
        
        # atempo filter is limited to [0.5, 2.0]
        # We need to chain multiple atempo filters if outside range
        while tempo_correction < 0.5:
            filters.append("atempo=0.5")
            tempo_correction /= 0.5
        while tempo_correction > 2.0:
            filters.append("atempo=2.0")
            tempo_correction /= 2.0
        
        if abs(tempo_correction - 1.0) > 0.001:
             filters.append(f"atempo={tempo_correction}")

    # Apply requested Speed change
    # Speed change also uses atempo
    # If speed is 2.0, duration is halved.
    if abs(speed - 1.0) > 0.001:
        current_speed = speed
        while current_speed < 0.5:
            filters.append("atempo=0.5")
            current_speed /= 0.5
        while current_speed > 2.0:
            filters.append("atempo=2.0")
            current_speed /= 2.0
            
        if abs(current_speed - 1.0) > 0.001:
            filters.append(f"atempo={current_speed}")
            
    return ",".join(filters)


def process(request: ModificationRequest) -> list[Path]:
    """Execute the modification batch."""
    resolve_environment()
    validate_input_paths(request.input_paths)

    ffmpeg_path = "ffmpeg"
    if request.ffmpeg_path:
        ffmpeg_path = str(request.ffmpeg_path)

    processed_files = []
    total_files = len(request.input_paths)

    for i, (source, destination) in enumerate(request.outputs()):
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Get audio info
            info = get_audio_info(source, ffmpeg_path)
            duration = info["duration"]
            sample_rate = info["sample_rate"]
            
            # Calculate cut times
            start_time = (request.cut_start / 100.0) * duration
            end_time = (request.cut_end / 100.0) * duration
            
            # Ensure valid time range
            if end_time <= start_time:
                end_time = duration
                
            # Build command
            cmd = [ffmpeg_path, "-y", "-i", str(source)]
            
            # Cut logic
            # Using -ss before -i is faster but less accurate. 
            # Using -ss after -i is accurate.
            # Since we are modifying, accuracy is preferred.
            cmd.extend(["-ss", str(start_time)])
            cmd.extend(["-to", str(end_time)])
            
            # Filter logic
            filter_str = build_filter_complex(request.speed, request.pitch, sample_rate)
            if filter_str:
                cmd.extend(["-filter:a", filter_str])
            
            # Output
            cmd.append(str(destination))
            
            # Run
            creationflags = 0
            if hasattr(subprocess, "CREATE_NO_WINDOW"):
                creationflags = subprocess.CREATE_NO_WINDOW
                
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=creationflags
            )
            
            processed_files.append(destination)

        except subprocess.CalledProcessError as e:
            raise ExportFailureError(source, e, total_files) from e
        except Exception as e:
            raise ExportFailureError(source, e, total_files) from e

    if not processed_files:
        raise NoOutputProducedError()

    return processed_files
