import subprocess
import sys
from pathlib import Path

def run_script(script_name, *args):
    cmd = ["python", str(Path.home() / "ai-video-app" / "scripts" / script_name)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR in {script_name}: {result.stderr[-300:]}")
        return False
    return True

def create_video(text, search_term, video_name, subtitles="on"):
    print(f"=== Creating video: {video_name} ===")
    
    print("[1/4] Generating audio...")
    if not run_script("generate_audio.py", video_name, text):
        return
    
    print("[2/4] Downloading video from Pixabay...")
    if not run_script("fetch_video.py", search_term):
        return
    
    print("[3/4] Merging audio + video...")
    if not run_script("merge_video.py", search_term, video_name, f"{video_name}_merged"):
        return
    
    if subtitles.lower() == "on":
        print("[4/4] Generating + burning subtitles...")
        if not run_script("make_subtitles.py", video_name, text, f"{video_name}_subs"):
            return
        if not run_script("burn_subtitles.py", f"{video_name}_merged", f"{video_name}_subs", f"{video_name}_final"):
            return
    else:
        print("[4/4] Subtitles OFF - skipping")
        merged = Path.home() / "ai-video-app" / "output" / f"{video_name}_merged.mp4"
        final = Path.home() / "ai-video-app" / "output" / f"{video_name}_final.mp4"
        merged.rename(final)
        print(f"SUCCESS: {final}")
    
    print(f"=== DONE: {video_name}_final.mp4 ===")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python create_video.py <text> <search_term> <video_name> <subtitles on/off>")
        sys.exit(1)
    create_video(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
