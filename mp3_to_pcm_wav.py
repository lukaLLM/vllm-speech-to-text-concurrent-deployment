"""
Minimal MP3 to PCM WAV Conversion Script
=========================================

This script converts all MP3 audio files in the current directory to PCM WAV 16-bit 44.1kHz format using FFmpeg.
"""

import subprocess
from pathlib import Path

def convert_mp3_to_pcm_wav(input_path: str, output_path: str) -> None:
    """
    Convert an MP3 file to PCM WAV 16-bit 44.1kHz format.

    Args:
        input_path: Path to the input MP3 file.
        output_path: Path to save the converted WAV file.
    """
    cmd = [
        'ffmpeg', '-y',  # Overwrite output file
        '-i', input_path,
        '-ar', '44100',      # 16kHz sample rate
        '-ac', '1',          # Mono channel
        '-c:a', 'pcm_s16le', # PCM signed 16-bit little-endian
        '-f', 'wav',         # WAV container format
        output_path
    ]

    subprocess.run(cmd, check=True)

def batch_convert_mp3_to_pcm_wav_in_current_directory() -> None:
    """
    Convert all MP3 files in the current directory to PCM WAV format.
    """
    current_dir = Path.cwd()
    mp3_files = list(current_dir.glob("*.mp3"))

    if not mp3_files:
        print("❌ No MP3 files found in the current directory.")
        return

    print(f"📁 Found {len(mp3_files)} MP3 files in {current_dir}")

    for mp3_file in mp3_files:
        output_file = mp3_file.with_suffix(".wav")
        convert_mp3_to_pcm_wav(str(mp3_file), str(output_file))

if __name__ == "__main__":
    batch_convert_mp3_to_pcm_wav_in_current_directory()