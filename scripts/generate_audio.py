from gtts import gTTS
from deep_translator import GoogleTranslator, MyMemoryTranslator
import sys
import re
import subprocess
from pathlib import Path

ROOTFS = Path("/data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs")
PIPER_OUTPUT = ROOTFS / "root" / "piper" / "output.wav"
TERMUX_OUTPUT = Path.home() / "ai-video-app" / "output"

def detect_script(text):
    if re.search(r'[\u0900-\u097F]', text):
        return 'devanagari'
    if re.search(r'[\u0600-\u06FF]', text):
        return 'arabic'
    return 'roman'

def translate_roman_to_hindi(text):
    try:
        result = GoogleTranslator(source='auto', target='hi').translate(text)
        if result and result != text:
            print(f"Google: {result}")
            return result
    except Exception as e:
        print(f"Google failed: {str(e)[:60]}")
    
    try:
        result = MyMemoryTranslator(source='en-GB', target='hi-IN').translate(text)
        if result and result != text:
            print(f"MyMemory: {result}")
            return result
    except Exception as e:
        print(f"MyMemory failed: {str(e)[:60]}")
    
    return None

def generate_gtts(text, output_path, lang, tld):
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.save(str(output_path))
    print(f"gTTS Audio saved: {output_path}")

def generate_piper(text, output_path, filename):
    print(f"Using Piper (natural voice)...")
    ubuntu_cmd = f'bash /root/piper/run_piper.sh "{text}" /root/piper/output.wav'
    cmd = ["proot-distro", "login", "ubuntu", "--", "bash", "-c", ubuntu_cmd]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if not PIPER_OUTPUT.exists():
        print(f"Piper ERROR: {result.stderr[-200:]}")
        return False
    
    import subprocess as sp
    sp.run(["cp", str(PIPER_OUTPUT), str(output_path)])
    PIPER_OUTPUT.unlink()
    
    mp3_path = output_path.with_suffix('.mp3')
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", str(output_path), "-codec:a", "libmp3lame", "-qscale:a", "4", str(mp3_path)]
    sp.run(ffmpeg_cmd, capture_output=True)
    output_path.unlink()
    
    print(f"Piper Audio saved: {mp3_path}")
    return True

def text_to_audio(text, filename, force_translate=False, voice="gtts"):
    wav_path = TERMUX_OUTPUT / f"{filename}.wav"
    mp3_path = TERMUX_OUTPUT / f"{filename}.mp3"
    
    script = detect_script(text)
    
    if script == 'devanagari':
        lang, tld = 'hi', 'com'
        final_text = text
        print("Detected: Hindi (Devanagari)")
    elif script == 'arabic':
        lang, tld = 'ur', 'com.pk'
        final_text = text
        print("Detected: Urdu (Nastaliq)")
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
                print("Translation failed, using Urdu fallback")
        else:
            lang, tld = 'ur', 'com.pk'
            final_text = text
            print("Detected: Roman — using Urdu voice")
    
    if voice.lower() == "piper":
        if lang == 'ur':
            print("⚠️ Piper only supports Hindi — using gTTS for Urdu")
            generate_gtts(final_text, mp3_path, lang, tld)
        else:
            success = generate_piper(final_text, wav_path, filename)
            if not success:
                print("Piper failed, falling back to gTTS")
                generate_gtts(final_text, mp3_path, lang, tld)
    else:
        generate_gtts(final_text, mp3_path, lang, tld)
    
    return final_text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <filename> <text> [--translate] [--voice piper|gtts]")
        sys.exit(1)
    filename = sys.argv[1]
    text = sys.argv[2]
    force = "--translate" in sys.argv
    voice = "gtts"
    if "--voice" in sys.argv:
        idx = sys.argv.index("--voice")
        if idx + 1 < len(sys.argv):
            voice = sys.argv[idx + 1]
    text_to_audio(text, filename, force_translate=force, voice=voice)
