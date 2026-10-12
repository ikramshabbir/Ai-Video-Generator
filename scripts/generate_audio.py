from gtts import gTTS
import sys
import re
from pathlib import Path

def detect_language(text):
    devanagari = re.search(r'[\u0900-\u097F]', text)
    if devanagari:
        return 'hi', 'com'
    
    arabic_urdu = re.search(r'[\u0600-\u06FF]', text)
    if arabic_urdu:
        return 'ur', 'com.pk'
    
    return 'ur', 'com.pk'

def text_to_audio(text, filename):
    lang, tld = detect_language(text)
    output_path = Path.home() / "ai-video-app" / "output" / f"{filename}.mp3"
    print(f"Detected language: {lang} ({'Hindi' if lang=='hi' else 'Urdu'})")
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.save(str(output_path))
    print(f"Audio saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <filename> <text>")
        sys.exit(1)
    filename = sys.argv[1]
    text = sys.argv[2]
    text_to_audio(text, filename)
