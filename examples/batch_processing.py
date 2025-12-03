"""Batch audio processing example.

This script demonstrates how to process multiple files concurrently
using the Harmonix SE backend modules.
"""

import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.handler.converter import SoundConverter, ConversionRequest
from app.utils.file_utils import list_audio_files
from utils import ensure_ffmpeg

def process_single_file(file_path: Path, output_dir: Path) -> dict:
    """Process a single file and return result dict."""
    converter = SoundConverter()
    
    request = ConversionRequest(
        input_path=str(file_path),
        output_dir=str(output_dir),
        format="flac",  # Convert everything to FLAC
        sample_rate=48000
    )
    
    start_time = time.time()
    try:
        result = converter.process(request)
        duration = time.time() - start_time
        
        return {
            "file": file_path.name,
            "success": result.success,
            "duration": duration,
            "output": result.output_path if result.success else None,
            "error": result.error
        }
    except Exception as e:
        return {
            "file": file_path.name,
            "success": False,
            "error": str(e)
        }

def main():
    print("=== Batch Audio Processor ===")
    
    if not ensure_ffmpeg():
        print("FFmpeg not found.")
        return

    input_dir = Path("samples")
    output_dir = Path("output/batch")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find files
    files = list_audio_files(input_dir)
    if not files:
        print(f"No audio files found in {input_dir}")
        return
        
    print(f"Found {len(files)} files. Starting processing...")
    
    # Process concurrently
    results = []
    max_workers = 4
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_single_file, f, output_dir): f 
            for f in files
        }
        
        for future in as_completed(future_to_file):
            res = future.result()
            results.append(res)
            status = "✅" if res["success"] else "❌"
            print(f"{status} {res['file']} ({res.get('duration', 0):.2f}s)")

    # Summary
    success_count = sum(1 for r in results if r["success"])
    print(f"\nCompleted: {success_count}/{len(files)} successful.")

if __name__ == "__main__":
    main()
