import subprocess
import sys
from pathlib import Path

def burn_subtitles(video_name, subtitle_name, output_name):
    video_path = Path.home() / "ai-video-app" / "output" / f"{video_name}.mp4"
    srt_path = Path.home() / "ai-video-app" / "output" / f"{subtitle_name}.srt"
    output_path = Path.home() / "ai-video-app" / "output" / f"{output_name}.mp4"
    
    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}")
        return
    if not srt_path.exists():
        print(f"ERROR: Subtitle not found: {srt_path}")
        return
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,BorderStyle=3,Outline=2,Alignment=2'",
        "-c:a", "copy",
        str(output_path)
    ]
    
    print("Burning subtitles...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {output_path}")
    else:
        print(f"FAILED: {result.stderr[-600:]}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python burn_subtitles.py <video_name> <subtitle_name> <output_name>")
        sys.exit(1)
    burn_subtitles(sys.argv[1], sys.argv[2], sys.argv[3])
