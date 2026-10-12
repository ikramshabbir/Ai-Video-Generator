from gtts import gTTS
import sys
from pathlib import Path

def text_to_audio(text, filename, lang='ur', tld='com.pk'):
    output_path = Path.home() / "ai-video-app" / "output" / f"{filename}.mp3"
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
