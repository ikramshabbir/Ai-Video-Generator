from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import re
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path.home() / "ai-video-app"
SCRIPTS = BASE_DIR / "scripts"
OUTPUT = BASE_DIR / "output"

def run_script(script_name, *args):
    cmd = ["python", str(SCRIPTS / script_name)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def sanitize(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def find_video(search_term):
    safe = sanitize(search_term)
    if (OUTPUT / f"{safe}.mp4").exists():
        return safe
    if (OUTPUT / f"{search_term}.mp4").exists():
        return search_term
    return safe

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("text", "").strip()
    search = data.get("search", "").strip()
    name = sanitize(data.get("name", "").strip())
    subs = data.get("subtitles", "on")
    style = data.get("style", "default")
    music = data.get("music", "off")
    
    if not text or not search or not name:
        return jsonify({"success": False, "error": "Text, search, aur name zaroori hain"})
    
    logs = []
    
    ok, out, err = run_script("generate_audio.py", name, text)
    logs.append(out)
    if not ok:
        return jsonify({"success": False, "error": "Audio failed", "logs": logs, "details": err})
    
    audio_used = name
    if music == "on":
        ok, out, err = run_script("mix_music.py", name, f"{name}_music")
        logs.append(out)
        if ok:
            audio_used = f"{name}_music"
    
    ok, out, err = run_script("fetch_video.py", search)
    logs.append(out)
    if not ok:
        return jsonify({"success": False, "error": "Video download failed", "logs": logs, "details": err})
    
    actual_video = find_video(search)
    
    ok, out, err = run_script("merge_video.py", actual_video, audio_used, f"{name}_merged")
    logs.append(out)
    if not ok:
        return jsonify({"success": False, "error": "Merge failed", "logs": logs, "details": err})
    
    if subs == "on":
        ok, out, err = run_script("make_subtitles.py", name, text, f"{name}_subs")
        logs.append(out)
        ok, out, err = run_script("burn_subtitles.py", f"{name}_merged", f"{name}_subs", f"{name}_final", style)
        logs.append(out)
    else:
        merged = OUTPUT / f"{name}_merged.mp4"
        final = OUTPUT / f"{name}_final.mp4"
        if merged.exists():
            if final.exists():
                final.unlink()
            merged.rename(final)
            logs.append(f"Renamed to {final.name}")
    
    final_file = f"{name}_final.mp4"
    if (OUTPUT / final_file).exists():
        return jsonify({"success": True, "video": final_file, "logs": logs})
    else:
        return jsonify({"success": False, "error": "Final video not created", "logs": logs})

@app.route("/videos/<filename>")
def serve_video(filename):
    return send_from_directory(str(OUTPUT), filename)

@app.route("/list")
def list_videos():
    videos = [f.name for f in OUTPUT.glob("*_final.mp4")]
    return jsonify({"videos": sorted(videos, reverse=True)})

if __name__ == "__main__":
    print("=" * 50)
    print("  AI Video Generator - Web App")
    print("  Open: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)
