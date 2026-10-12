import subprocess
import sys
from pathlib import Path

def merge(video_file, audio_file, output_name):
    video_path = Path.home() / "ai-video-app" / "output" / f"{video_file}.mp4"
    audio_path = Path.home() / "ai-video-app" / "output" / f"{audio_file}.mp3"
    output_path = Path.home() / "ai-video-app" / "output" / f"{output_name}.mp4"
    
    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}")
        return
    if not audio_path.exists():
        print(f"ERROR: Audio not found: {audio_path}")
        return
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path)
    ]
    
    print(f"Merging...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {output_path}")
    else:
        print(f"FAILED: {result.stderr[-500:]}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python merge_video.py <video_name> <audio_name> <output_name>")
        sys.exit(1)
    merge(sys.argv[1], sys.argv[2], sys.argv[3])
