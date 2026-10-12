import subprocess
import sys
from pathlib import Path

def mix_music(voice_name, output_name, music_volume=0.15, voice_volume=1.0):
    voice_path = Path.home() / "ai-video-app" / "output" / f"{voice_name}.mp3"
    music_path = Path.home() / "ai-video-app" / "input" / "music.mp3"
    output_path = Path.home() / "ai-video-app" / "output" / f"{output_name}.mp3"
    
    if not voice_path.exists():
        print(f"ERROR: Voice not found: {voice_path}")
        return
    if not music_path.exists():
        print(f"ERROR: Music not found: {music_path}")
        return
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_path),
        "-i", str(music_path),
        "-filter_complex",
        f"[0:a]volume={voice_volume}[v];[1:a]volume={music_volume}[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
        "-map", "[a]",
        str(output_path)
    ]
    
    print(f"Mixing voice + music (music volume: {music_volume})...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {output_path}")
    else:
        print(f"FAILED: {result.stderr[-500:]}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mix_music.py <voice_name> <output_name> [music_volume 0.0-1.0]")
        sys.exit(1)
    vol = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.15
    mix_music(sys.argv[1], sys.argv[2], music_volume=vol)
