import subprocess
import sys
import re
from pathlib import Path

def run_script(script_name, *args):
    cmd = ["python", str(Path.home() / "ai-video-app" / "scripts" / script_name)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR in {script_name}: {result.stderr[-300:]}")
        return False
    return True

def sanitize(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def detect_script(text):
    if re.search(r'[\u0900-\u097F]', text):
        return 'devanagari'
    if re.search(r'[\u0600-\u06FF]', text):
        return 'arabic'
    return 'roman'

def find_downloaded_video(search_term):
    output = Path.home() / "ai-video-app" / "output"
    safe_name = sanitize(search_term)
    if (output / f"{safe_name}.mp4").exists():
        return safe_name
    if (output / f"{search_term}.mp4").exists():
        return search_term
    return safe_name

def create_video(text, search_term, video_name, subtitles="on", style="default", music="off", voice="gtts"):
    video_name = sanitize(video_name)
    
    print(f"=== Creating video: {video_name} (style: {style}, music: {music}, voice: {voice}) ===")
    
    print("[1/5] Generating audio...")
    script = detect_script(text)
    args = [video_name, text]
    if script == 'roman':
        args.append("--translate")
    args.extend(["--voice", voice])
    
    if not run_script("generate_audio.py", *args):
        return
    
    if music.lower() == "on":
        print("[2/5] Mixing with background music...")
        if not run_script("mix_music.py", video_name, f"{video_name}_music"):
            return
        audio_for_merge = f"{video_name}_music"
    else:
        print("[2/5] Music OFF - using voice only")
        audio_for_merge = video_name
    
    print("[3/5] Downloading video from Pixabay...")
    if not run_script("fetch_video.py", search_term):
        return
    
    actual_video_name = find_downloaded_video(search_term)
    print(f"Using video file: {actual_video_name}.mp4")
    
    print("[4/5] Merging audio + video...")
    if not run_script("merge_video.py", actual_video_name, audio_for_merge, f"{video_name}_merged"):
        return
    
    if subtitles.lower() == "on":
        print("[5/5] Generating + burning subtitles...")
        if not run_script("make_subtitles.py", video_name, text, f"{video_name}_subs"):
            return
        if not run_script("burn_subtitles.py", f"{video_name}_merged", f"{video_name}_subs", f"{video_name}_final", style):
            return
    else:
        print("[5/5] Subtitles OFF - skipping")
        merged = Path.home() / "ai-video-app" / "output" / f"{video_name}_merged.mp4"
        final = Path.home() / "ai-video-app" / "output" / f"{video_name}_final.mp4"
        if merged.exists():
            if final.exists():
                final.unlink()
            merged.rename(final)
            print(f"SUCCESS: {final}")
    
    print(f"=== DONE: {video_name}_final.mp4 ===")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python create_video.py <text> <search> <name> <on/off> [style] [music] [voice]")
        print("Voice options: gtts (fast) | piper (natural)")
        sys.exit(1)
    style = sys.argv[5] if len(sys.argv) >= 6 else "default"
    music = sys.argv[6] if len(sys.argv) >= 7 else "off"
    voice = sys.argv[7] if len(sys.argv) >= 8 else "gtts"
    create_video(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], style, music, voice)
