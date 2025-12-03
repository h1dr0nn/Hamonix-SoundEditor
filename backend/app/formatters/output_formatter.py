"""JSON response formatting utilities.

This module standardizes the structure of JSON messages sent to stdout
for the Tauri frontend to consume.
"""

from typing import Any, Dict, Optional, Union
import json
from datetime import datetime


def format_success(
    operation: str,
    data: Optional[Dict[str, Any]] = None,
    message: str = "Operation successful"
) -> Dict[str, Any]:
    """Format a success response.

    Args:
        operation: Name of the operation (e.g., 'convert', 'analyze').
        data: Optional dictionary containing result data.
        message: Human-readable success message.

    Returns:
        Dict representing the standard success response structure.
    """
    response = {
        "status": "success",
        "operation": operation,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
    }
    
    if data:
        response["data"] = data
        
    return response


def format_error(
    operation: str,
    error_message: str,
    error_code: str = "UNKNOWN_ERROR",
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Format an error response.

    Args:
        operation: Name of the operation that failed.
        error_message: Human-readable error description.
        error_code: Machine-readable error code.
        details: Optional dictionary with debug details.

    Returns:
        Dict representing the standard error response structure.
    """
    response = {
        "status": "error",
        "operation": operation,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "error": {
            "code": error_code,
            "message": error_message
        }
    }
    
    if details:
        response["error"]["details"] = details
        
    return response


def format_progress(
    operation: str,
    percent: float,
    current_file: Optional[str] = None,
    stage: str = "processing"
) -> Dict[str, Any]:
    """Format a progress update.

    Args:
        operation: Name of the operation.
        percent: Progress percentage (0.0 to 100.0).
        current_file: Name of the file currently being processed.
        stage: Current processing stage description.

    Returns:
        Dict representing the progress update structure.
    """
    return {
        "status": "progress",
        "operation": operation,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "progress": {
            "percent": round(percent, 2),
            "stage": stage,
            "file": current_file
        }
    }


def format_analysis_result(
    file_path: str,
    duration: float,
    format_info: Dict[str, Any],
    audio_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """Format the result of an audio analysis.

    Args:
        file_path: Path to the analyzed file.
        duration: Duration in seconds.
        format_info: Dictionary with format details (bitrate, sample_rate).
        audio_stats: Dictionary with audio statistics (loudness, peak).

    Returns:
        Dict representing the analysis result data block.
    """
    return {
        "file": file_path,
        "duration_seconds": duration,
        "format": format_info,
        "statistics": audio_stats,
        "analyzed_at": datetime.utcnow().isoformat() + "Z"
    }
