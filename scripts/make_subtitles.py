import sys
import subprocess
from pathlib import Path

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

def make_srt(audio_name, text, output_name):
    audio_path = Path.home() / "ai-video-app" / "output" / f"{audio_name}.mp3"
    output_path = Path.home() / "ai-video-app" / "output" / f"{output_name}.srt"
    
    if not audio_path.exists():
        print(f"ERROR: Audio not found: {audio_path}")
        return
    
    total_seconds = get_audio_duration(audio_path)
    
    words = text.split()
    if not words:
        print("ERROR: No text provided")
        return
    
    per_word = total_seconds / len(words)
    
    srt_content = ""
    current_time = 0.0
    for idx, word in enumerate(words, start=1):
        start = current_time
        end = current_time + per_word
        srt_content += f"{idx}\n"
        srt_content += f"{format_time(start)} --> {format_time(end)}\n"
        srt_content += f"{word}\n\n"
        current_time = end
    
    output_path.write_text(srt_content, encoding="utf-8")
    print(f"SRT saved: {output_path}")
    print(f"Total words: {len(words)}, Duration: {total_seconds:.2f}s")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python make_subtitles.py <audio_name> <text> <output_name>")
        sys.exit(1)
    make_srt(sys.argv[1], sys.argv[2], sys.argv[3])
