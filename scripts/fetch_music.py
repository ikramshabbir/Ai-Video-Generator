import os
import sys
import requests
from pathlib import Path

API_KEY = os.environ.get("PIXABAY_API_KEY")
BASE_URL = "https://pixabay.com/api/"

def search_music(mood="happy"):
    params = {
        "key": API_KEY,
        "q": mood,
        "category": "music",
        "per_page": 3,
        "safesearch": "true"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def download_music(mood, output_name):
    data = search_music(mood)
    hits = data.get("hits", [])
    if not hits:
        print(f"No music found for mood: {mood}")
        return None
    
    track = hits[0]
    audio_url = track.get("audio") or track.get("previewURL")
    if not audio_url:
        print("No audio URL found")
        return None
    
    output_path = Path.home() / "ai-video-app" / "output" / f"music_{output_name}.mp3"
    print(f"Downloading music: {audio_url[:80]}...")
    
    r = requests.get(audio_url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Music saved: {output_path}")
    return str(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_music.py <mood>")
        sys.exit(1)
    mood = sys.argv[1]
    download_music(mood, mood)
