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

def create_one(text, search_term, video_name, subtitles):
    print(f"\n{'='*50}")
    print(f"VIDEO: {video_name}")
    print(f"{'='*50}")
    
    if not run_script("generate_audio.py", video_name, text):
        return False
    
    if not run_script("fetch_video.py", search_term):
        return False
    
    if not run_script("merge_video.py", search_term, video_name, f"{video_name}_merged"):
        return False
    
    if subtitles.lower() == "on":
        if not run_script("make_subtitles.py", video_name, text, f"{video_name}_subs"):
            return False
        if not run_script("burn_subtitles.py", f"{video_name}_merged", f"{video_name}_subs", f"{video_name}_final"):
            return False
    else:
        merged = Path.home() / "ai-video-app" / "output" / f"{video_name}_merged.mp4"
        final = Path.home() / "ai-video-app" / "output" / f"{video_name}_final.mp4"
        if merged.exists():
            merged.rename(final)
        print(f"SUCCESS: {final}")
    
    return True

def batch_create(input_file):
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        return
    
    lines = input_path.read_text(encoding="utf-8").strip().split("\n")
    total = len([l for l in lines if l.strip() and not l.startswith("#")])
    
    print(f"\n{'#'*50}")
    print(f"BATCH MODE: {total} videos to create")
    print(f"{'#'*50}\n")
    
    success = 0
    failed = 0
    
    for idx, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            print(f"SKIPPING line {idx}: needs 4 parts (text|search|name|subtitles)")
            failed += 1
            continue
        
        text, search_term, video_name, subtitles = parts[0], parts[1], parts[2], parts[3]
        
        try:
            if create_one(text, search_term, video_name, subtitles):
                success += 1
                print(f"✓ {video_name} DONE")
            else:
                failed += 1
                print(f"✗ {video_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {video_name} ERROR: {e}")
    
    print(f"\n{'='*50}")
    print(f"BATCH COMPLETE: {success} success, {failed} failed")
    print(f"{'='*50}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_create.py <input_file.txt>")
        sys.exit(1)
    batch_create(sys.argv[1])
