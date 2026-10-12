import os
import sys
import requests
from pathlib import Path

API_KEY = os.environ.get("PIXABAY_API_KEY")
BASE_URL = "https://pixabay.com/api/videos/"

def search_video(query, per_page=3):
    params = {
        "key": API_KEY,
        "q": query,
        "per_page": per_page,
        "video_type": "film",
        "safesearch": "true"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def download_best_video(query):
    data = search_video(query)
    hits = data.get("hits", [])
    if not hits:
        print(f"No video found for: {query}")
        return None
    
    video = hits[0]
    video_url = video["videos"]["medium"]["url"]
    
    output_path = Path.home() / "ai-video-app" / "output" / f"{query.replace(' ', '_')}.mp4"
    print(f"Downloading: {video_url}")
    
    r = requests.get(video_url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Saved: {output_path}")
    return str(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_video.py <search_term>")
        sys.exit(1)
    query = sys.argv[1]
    download_best_video(query)
