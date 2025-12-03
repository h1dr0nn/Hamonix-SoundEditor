"""Audio format conversion logic.

This module handles the core audio conversion functionality, managing batch processing,
FFmpeg execution, and progress reporting.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional, Sequence, Tuple, Set, Dict, Any, Union

from ..ffmpeg_runner import (
    AudioSegment,
    AudioProcessingError,
    ExportFailureError,
    MissingEncoderError,
    NoOutputProducedError,
    format_error_message,
    resolve_environment,
    validate_input_paths,
    validate_pydub_available,
)


@dataclass(frozen=True)
class ConversionRequest:
    """Data container describing a batch conversion job.
    
    Attributes:
        input_paths: List of paths to source audio files.
        output_directory: Directory where converted files will be saved.
        output_format: Target audio format extension (e.g., 'mp3', 'wav').
        overwrite_existing: Whether to overwrite files if they already exist.
        ffmpeg_path: Optional explicit path to FFmpeg binary.
    """

    input_paths: Sequence[Path]
    output_directory: Path
    output_format: str
    overwrite_existing: bool = True
    ffmpeg_path: Optional[Path] = None

    def outputs(self) -> Iterable[Tuple[Path, Path]]:
        """Yield tuples of ``(input_path, output_path)`` for the batch.
        
        Handles filename conflicts if overwrite_existing is False by appending
        counters to filenames.
        
        Yields:
            Tuple containing (source_path, destination_path).
        """
        allocated: Set[Path] = set()

        for source in self.input_paths:
            base_destination = self.output_directory / f"{source.stem}.{self.output_format}"
            destination = base_destination

            if not self.overwrite_existing:
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


@dataclass(frozen=True)
class ConversionResult:
    """Outcome returned by :meth:`SoundConverter.convert`.
    
    Attributes:
        success: True if the operation completed successfully.
        message: Human-readable result message.
        outputs: Tuple of paths to successfully generated files.
    """

    success: bool
    message: str
    outputs: Tuple[Path, ...] = ()


@dataclass(frozen=True)
class ConversionProgress:
    """Progress payload for individual files.
    
    Attributes:
        status: Current status string (e.g., 'processing', 'completed').
        index: Index of the current file being processed (1-based).
        total: Total number of files in the batch.
        source: Path to the source file.
        destination: Path to the destination file.
    """

    status: str
    index: int
    total: int
    source: Path
    destination: Path


class SoundConverter:
    """Convert audio files to a different format using FFmpeg directly.
    
    This class manages the conversion process, including environment validation,
    batch processing, and error handling.
    """

    SUPPORTED_FORMATS: Sequence[str] = ("mp3", "wav", "ogg", "flac", "aac", "wma", "m4a", "opus", "aiff")

    @staticmethod
    def available_formats() -> Iterable[str]:
        """Get list of supported output formats."""
        return SoundConverter.SUPPORTED_FORMATS

    @staticmethod
    def convert(
        request: ConversionRequest,
        progress_callback: Optional[Callable[[ConversionProgress], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None,
    ) -> ConversionResult:
        """Run the conversion and return a structured result.

        Args:
            request: Conversion request payload.
            progress_callback: Optional callback invoked with :class:`ConversionProgress` updates.
            log_callback: Optional callback invoked with FFmpeg stderr lines.

        Returns:
            ConversionResult object indicating success or failure.
        """
        try:
            validate_input_paths(list(request.input_paths))
            # Note: We don't strictly need pydub for direct ffmpeg conversion, 
            # but we keep the check if other parts rely on it.
            # validate_pydub_available() 
            resolve_environment()
            
            outputs = SoundConverter._export_batch(
                request, progress_callback, log_callback
            )
            
            if not outputs:
                raise NoOutputProducedError()
                
        except AudioProcessingError as error:
            message = format_error_message(error)
            return ConversionResult(False, message, ())

        message = SoundConverter._format_success_message(request, outputs)
        return ConversionResult(True, message, outputs)

    @staticmethod
    def _export_batch(
        request: ConversionRequest,
        progress_callback: Optional[Callable[[ConversionProgress], None]],
        log_callback: Optional[Callable[[str], None]],
    ) -> Tuple[Path, ...]:
        """Export all files in the batch.
        
        Args:
            request: The conversion request.
            progress_callback: Callback for progress updates.
            log_callback: Callback for logging.
            
        Returns:
            Tuple of successfully converted file paths.
        """
        converted = []
        request.output_directory.mkdir(parents=True, exist_ok=True)

        for index, (input_path, output_path) in enumerate(request.outputs(), start=1):
            if progress_callback:
                progress_callback(
                    ConversionProgress(
                        status="processing",
                        index=index,
                        total=len(request.input_paths),
                        source=input_path,
                        destination=output_path,
                    )
                )

            try:
                converter = _resolve_converter_path(request)
                
                # Check for in-place conversion (input == output)
                # FFmpeg cannot read/write same file, so we write to temp file first
                use_temp_file = input_path.resolve() == output_path.resolve()
                actual_output_path = output_path
                
                if use_temp_file:
                    actual_output_path = output_path.with_suffix(f".tmp{output_path.suffix}")
                    if log_callback:
                        log_callback(f"In-place conversion detected. Using temp file: {actual_output_path}")

                _run_ffmpeg_conversion(
                    converter,
                    input_path,
                    actual_output_path,
                    request.output_format.lower(),
                    log_callback,
                )
                
                # If using temp file, move it to final destination after success
                if use_temp_file:
                    import shutil
                    shutil.move(str(actual_output_path), str(output_path))
                    if log_callback:
                        log_callback(f"Renamed temp file to: {output_path}")
            except Exception as exc:
                raise ExportFailureError(input_path, exc, len(request.input_paths))

            converted.append(output_path)

            if progress_callback:
                progress_callback(
                    ConversionProgress(
                        status="completed",
                        index=index,
                        total=len(request.input_paths),
                        source=input_path,
                        destination=output_path,
                    )
                )

        return tuple(converted)

    @staticmethod
    def _format_success_message(request: ConversionRequest, outputs: Tuple[Path, ...]) -> str:
        """Format the success message based on output count."""
        if len(outputs) == 1:
            return f"Saved file to {outputs[0]}"
        destination_text = (
            request.output_directory if request.output_directory else outputs[0].parent
        )
        return f"Converted {len(outputs)} files into {destination_text}"


def _run_ffmpeg_conversion(
    converter: Path,
    input_path: Path,
    output_path: Path,
    output_format: str,
    log_callback: Optional[Callable[[str], None]],
) -> None:
    """Run FFmpeg conversion with explicit format and codec specification.
    
    Args:
        converter: Path to FFmpeg executable.
        input_path: Source file path.
        output_path: Destination file path.
        output_format: Target format string.
        log_callback: Callback for stderr logging.
        
    Raises:
        RuntimeError: If FFmpeg exits with non-zero code.
    """
    
    # Map output format to FFmpeg codec and format
    # This ensures proper encoding instead of relying on extension guessing
    format_codec_map: Dict[str, Dict[str, str]] = {
        "mp3": {"format": "mp3", "codec": "libmp3lame", "bitrate": "192k"},
        "aac": {"format": "adts", "codec": "aac", "bitrate": "192k"},
        "m4a": {"format": "ipod", "codec": "aac", "bitrate": "192k"},
        "wav": {"format": "wav", "codec": "pcm_s16le"},
        "flac": {"format": "flac", "codec": "flac"},
        "ogg": {"format": "ogg", "codec": "libvorbis", "bitrate": "192k"},
        "opus": {"format": "opus", "codec": "libopus", "bitrate": "128k"},
        "wma": {"format": "asf", "codec": "wmav2", "bitrate": "192k"},
        "aiff": {"format": "aiff", "codec": "pcm_s16be"},
    }
    
    format_lower = output_format.lower()
    codec_config = format_codec_map.get(format_lower, {})
    
    # Build FFmpeg command with explicit codec and format
    command = [
        str(converter),
        "-y",  # Overwrite output
        "-i", str(input_path),
    ]
    
    # Add codec specification
    if "codec" in codec_config:
        command.extend(["-c:a", codec_config["codec"]])
    
    # Add bitrate for lossy formats
    if "bitrate" in codec_config:
        command.extend(["-b:a", codec_config["bitrate"]])
    
    # Add format specification
    if "format" in codec_config:
        command.extend(["-f", codec_config["format"]])
    
    command.append(str(output_path))

    # Windows-specific: Hide console window
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        startupinfo=startupinfo
    )

    assert process.stderr is not None
    for line in process.stderr:
        if log_callback:
            log_callback(line.rstrip())

    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"ffmpeg exited with code {return_code}")


def _resolve_converter_path(request: ConversionRequest) -> Path:
    """Resolve the ffmpeg binary to use for conversion.
    
    Checks explicit path, environment variables, pydub configuration,
    and system PATH.
    
    Args:
        request: Conversion request containing optional explicit path.
        
    Returns:
        Path to the FFmpeg executable.
        
    Raises:
        MissingEncoderError: If FFmpeg cannot be found.
    """

    candidates = []

    if request.ffmpeg_path:
        candidates.append(request.ffmpeg_path)

    env_candidates = [
        os.environ.get("FFMPEG_BINARY"),
        os.environ.get("FFMPEG_BIN"),
    ]
    candidates.extend(Path(path) for path in env_candidates if path)

    # Check pydub's AudioSegment.converter if available
    try:
        from pydub import AudioSegment as PydubAudioSegment # type: ignore
        converter_attr = getattr(PydubAudioSegment, "converter", None)
        if converter_attr:
            candidates.append(Path(converter_attr))
    except ImportError:
        pass

    from shutil import which

    default_path = which("ffmpeg")
    if default_path:
        candidates.append(Path(default_path))

    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate

    raise MissingEncoderError()
