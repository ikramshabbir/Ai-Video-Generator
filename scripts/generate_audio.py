from gtts import gTTS
from deep_translator import GoogleTranslator, MyMemoryTranslator
import sys
import re
from pathlib import Path

def detect_script(text):
    if re.search(r'[\u0900-\u097F]', text):
        return 'devanagari'
    if re.search(r'[\u0600-\u06FF]', text):
        return 'arabic'
    return 'roman'

def translate_roman_to_hindi(text):
    try:
        print("Trying Google Translate...")
        result = GoogleTranslator(source='auto', target='hi').translate(text)
        if result and result != text:
            print(f"Google: {result}")
            return result
    except Exception as e:
        print(f"Google failed: {str(e)[:80]}")
    
    try:
        print("Trying MyMemory Translate...")
        result = MyMemoryTranslator(source='en-GB', target='hi-IN').translate(text)
        if result and result != text:
            print(f"MyMemory: {result}")
            return result
    except Exception as e:
        print(f"MyMemory failed: {str(e)[:80]}")
    
    return None

def text_to_audio(text, filename, force_translate=False):
    output_path = Path.home() / "ai-video-app" / "output" / f"{filename}.mp3"
    script = detect_script(text)
    
    if script == 'devanagari':
        lang, tld = 'hi', 'com'
        final_text = text
        print("Detected: Hindi (Devanagari) — using Hindi voice")
    elif script == 'arabic':
        lang, tld = 'ur', 'com.pk'
        final_text = text
        print("Detected: Urdu (Nastaliq) — using Urdu voice")
    else:
        if force_translate:
            print("Detected: Roman — translating to Hindi...")
            translated = translate_roman_to_hindi(text)
            if translated:
                lang, tld = 'hi', 'com'
                final_text = translated
            else:
                lang, tld = 'ur', 'com.pk'
                final_text = text
                print("All translators failed, using Urdu fallback")
        else:
            lang, tld = 'ur', 'com.pk'
            final_text = text
            print("Detected: Roman — using Urdu voice")
    
    tts = gTTS(text=final_text, lang=lang, tld=tld, slow=False)
    tts.save(str(output_path))
    print(f"Audio saved: {output_path}")
    return final_text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <filename> <text> [--translate]")
        sys.exit(1)
    filename = sys.argv[1]
    text = sys.argv[2]
    force = len(sys.argv) >= 4 and sys.argv[3] == "--translate"
    text_to_audio(text, filename, force_translate=force)
