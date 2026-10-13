import subprocess
import sys
from pathlib import Path

ROOTFS = Path("/data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs")
PIPER_OUTPUT = ROOTFS / "root" / "piper" / "output.wav"
TERMUX_OUTPUT = Path.home() / "ai-video-app" / "output"

def text_to_audio_piper(text, filename):
    print(f"Running Piper (natural voice)...")
    print(f"Target filename: {filename}.wav")
    
    ubuntu_cmd = f'bash /root/piper/run_piper.sh "{text}" /root/piper/output.wav'
    
    cmd = [
        "proot-distro", "login", "ubuntu", "--",
        "bash", "-c", ubuntu_cmd
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if not PIPER_OUTPUT.exists():
        print(f"ERROR: Piper output not found at {PIPER_OUTPUT}")
        print(f"STDERR: {result.stderr[-300:]}")
        return False
    
    final_path = TERMUX_OUTPUT / f"{filename}.wav"
    subprocess.run(["cp", str(PIPER_OUTPUT), str(final_path)])
    print(f"Audio saved: {final_path}")
    
    PIPER_OUTPUT.unlink()
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_audio_piper.py <filename> <text>")
        sys.exit(1)
    filename = sys.argv[1]
    text = sys.argv[2]
    text_to_audio_piper(text, filename)
