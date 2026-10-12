# AI Video Generator

**Text to Video with Roman Urdu/Hindi voice, subtitles, and background music — built for Termux (Android).**

---

## Features

| Feature | Description |
|---------|-------------|
| Text to Voice | Roman Urdu / Hindi text to Natural voice (gTTS) |
| Auto Video | Pixabay se related video automatically download |
| Subtitles | 5 customizable styles (color, size, position) |
| Background Music | Voice + music mixing (music 15% volume) |
| Batch Mode | Ek file se multiple videos banao |
| Interactive Menu | User-friendly menu (1, 2, 3 dabao) |

---

## Installation (Termux)

### Step 1: Required Packages
```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg git nodejs file -y
```

### Step 2: Python Libraries
```bash
pip install gtts requests
```

### Step 3: API Key Setup
Pixabay se free API key lein: https://pixabay.com/api/docs/

```bash
echo 'export PIXABAY_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Clone Repository
```bash
git clone https://github.com/ikramshabbir/Ai-Video-Generator.git
cd Ai-Video-Generator
```

---

## Usage

### Option 1: Interactive Menu (Recommended)
```bash
bash scripts/menu.sh
```
Phir numbers dabao:
- `1` — Naya video banao
- `2` — Batch mode (kai videos)
- `3` — Sirf audio banao
- `4` — Purani videos dekho
- `5` — Exit

### Option 2: Direct Command
```bash
python scripts/create_video.py "Aapka text" "search_term" "video_name" on white on
```

### Option 3: Batch Mode
```bash
python scripts/batch_create.py input/batch1.txt
```

Input file format:
```
text | search_term | video_name | subtitles
Yeh ek billi hai | cat | video1 | on
Sher jungle ka raja | lion | video2 | on
```

---

## Subtitle Styles

| Style | Color | Size | Position |
|-------|-------|------|----------|
| default | Yellow | 24 | Bottom |
| white | White | 28 | Bottom |
| yellow_big | Yellow | 32 | Bottom |
| top_white | White | 26 | Top |
| green_bold | Green | 30 | Bottom |

Styles customize karne ke liye: `config/subtitle_styles.json`

---

## Project Structure

```
ai-video-app/
├── scripts/
│   ├── menu.sh              # Interactive menu
│   ├── create_video.py      # Master pipeline
│   ├── generate_audio.py    # Text to Voice
│   ├── fetch_video.py       # Pixabay download
│   ├── merge_video.py       # Audio + Video
│   ├── make_subtitles.py    # SRT generation
│   ├── burn_subtitles.py    # SRT burn with style
│   ├── mix_music.py         # Voice + music
│   └── batch_create.py      # Batch mode
├── config/
│   └── subtitle_styles.json # 5 styles
├── input/
│   ├── batch1.txt           # Batch example
│   └── music.mp3            # Background music
├── output/                  # Generated files
└── README.md
```

---

## Tech Stack

- **Termux** — Android Linux environment
- **Python 3.14** — Core logic
- **gTTS** — Google Text-to-Speech
- **FFmpeg** — Video/audio processing
- **Pixabay API** — Free stock videos

---

## License

MIT License — Free to use, modify, and distribute.

---

## Author

**ikramshabbir**
- GitHub: [@ikramshabbir](https://github.com/ikramshabbir)
- Repository: [Ai-Video-Generator](https://github.com/ikramshabbir/Ai-Video-Generator)

---

**Made with love in Termux**
