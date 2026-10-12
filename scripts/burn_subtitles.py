import subprocess
import sys
import json
from pathlib import Path

def load_style(style_name):
    config_path = Path.home() / "ai-video-app" / "config" / "subtitle_styles.json"
    if not config_path.exists():
        return None
    styles = json.loads(config_path.read_text())
    return styles.get(style_name)

def burn_subtitles(video_name, subtitle_name, output_name, style_name="default"):
    video_path = Path.home() / "ai-video-app" / "output" / f"{video_name}.mp4"
    srt_path = Path.home() / "ai-video-app" / "output" / f"{subtitle_name}.srt"
    output_path = Path.home() / "ai-video-app" / "output" / f"{output_name}.mp4"
    
    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}")
        return
    if not srt_path.exists():
        print(f"ERROR: Subtitle not found: {srt_path}")
        return
    
    style = load_style(style_name)
    if not style:
        print(f"ERROR: Style '{style_name}' not found in config")
        return
    
    print(f"Using style: {style_name}")
    style_str = (
        f"FontSize={style['font_size']},"
        f"PrimaryColour={style['primary_color']},"
        f"OutlineColour={style['outline_color']},"
        f"BorderStyle=3,"
        f"Outline={style['outline_width']},"
        f"Alignment={style['alignment']},"
        f"Bold={style['bold']}"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles={srt_path}:force_style='{style_str}'",
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
        print("Usage: python burn_subtitles.py <video> <subs> <output> [style_name]")
        print("Available styles: default, white, yellow_big, top_white, green_bold")
        sys.exit(1)
    style = sys.argv[4] if len(sys.argv) >= 5 else "default"
    burn_subtitles(sys.argv[1], sys.argv[2], sys.argv[3], style)
