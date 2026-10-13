#!/data/data/com.termux/files/usr/bin/bash

VIDEO_APP="$HOME/ai-video-app"
SCRIPTS="$VIDEO_APP/scripts"

show_banner() {
    clear
    echo "╔══════════════════════════════════════════╗"
    echo "║      AI VIDEO GENERATOR - MAIN MENU      ║"
    echo "║          by ikramshabbir                 ║"
    echo "╚══════════════════════════════════════════╝"
    echo ""
}

pick_voice() {
    echo ""
    echo "=== VOICE SELECT KAREIN ==="
    echo "  1. Fast (gTTS) - Robot voice"
    echo "  2. Male (Piper) - Natural"
    echo "  3. Female (Piper) - Natural"
    echo "  4. Kid (Piper) - Bachche jaisi"
    echo ""
    read -p "Choice [1-4]: " vc
    if [ "$vc" = "2" ]; then VOICE="piper-male"
    elif [ "$vc" = "3" ]; then VOICE="piper-female"
    elif [ "$vc" = "4" ]; then VOICE="piper-kid"
    else VOICE="gtts"
    fi
}

main_menu() {
    show_banner
    echo "1)  Naya video banao"
    echo "2)  Batch mode"
    echo "3)  Sirf audio banao"
    echo "4)  Purani videos dekho"
    echo "5)  Exit"
    echo ""
    read -p "Choice [1-5]: " choice
    if [ "$choice" = "1" ]; then single_video
    elif [ "$choice" = "2" ]; then batch_mode
    elif [ "$choice" = "3" ]; then audio_only
    elif [ "$choice" = "4" ]; then list_outputs
    elif [ "$choice" = "5" ]; then echo "Allah Hafiz!"; exit 0
    else echo "Ghalat choice"; sleep 2; main_menu
    fi
}

single_video() {
    show_banner
    echo "=== NAYA VIDEO BANAO ==="
    echo ""
    read -p "Text (Roman Urdu/Hindi): " user_text
    [ -z "$user_text" ] && echo "Text khaali!" && sleep 2 && main_menu
    
    read -p "Search keyword: " search_term
    read -p "Video name: " video_name
    
    echo ""
    read -p "Subtitles [on/off, default=on]: " subs
    subs=${subs:-on}
    
    style="default"
    if [ "$subs" = "on" ]; then
        echo ""
        echo "Styles: 1.default 2.white 3.yellow_big 4.top_white 5.green_bold"
        read -p "Style [1-5, default=1]: " style_num
        if [ "$style_num" = "2" ]; then style="white"
        elif [ "$style_num" = "3" ]; then style="yellow_big"
        elif [ "$style_num" = "4" ]; then style="top_white"
        elif [ "$style_num" = "5" ]; then style="green_bold"
        fi
    fi
    
    echo ""
    read -p "Background music [on/off, default=off]: " music
    music=${music:-off}
    
    pick_voice
    
    echo ""
    echo "=== VIDEO BANANA SHURU (voice: $VOICE) ==="
    echo ""
    python "$SCRIPTS/create_video.py" "$user_text" "$search_term" "$video_name" "$subs" "$style" "$music" "$VOICE"
    
    echo ""
    read -p "Enter dabayein menu ke liye..."
    main_menu
}

batch_mode() {
    show_banner
    echo "=== BATCH MODE ==="
    echo ""
    read -p "Input file (default: input/batch1.txt): " batch_file
    batch_file=${batch_file:-$VIDEO_APP/input/batch1.txt}
    
    if [ ! -f "$batch_file" ]; then
        echo "File nahi mili: $batch_file"
        sleep 3
        main_menu
    fi
    
    echo ""
    python "$SCRIPTS/batch_create.py" "$batch_file"
    echo ""
    read -p "Enter dabayein menu ke liye..."
    main_menu
}

audio_only() {
    show_banner
    echo "=== SIRF AUDIO BANAO ==="
    echo ""
    read -p "Text: " user_text
    read -p "Audio name: " audio_name
    
    pick_voice
    
    echo ""
    python "$SCRIPTS/generate_audio.py" "$audio_name" "$user_text" --translate --voice "$VOICE"
    
    echo ""
    read -p "Music bhi mix karein? [on/off, default=off]: " music
    music=${music:-off}
    if [ "$music" = "on" ]; then
        python "$SCRIPTS/mix_music.py" "$audio_name" "${audio_name}_music"
    fi
    
    echo ""
    read -p "Enter dabayein menu ke liye..."
    main_menu
}

list_outputs() {
    show_banner
    echo "=== OUTPUT FOLDER ==="
    echo ""
    ls -lh "$VIDEO_APP/output/" | grep -E "\.mp4|\.mp3" | tail -20
    echo ""
    read -p "Enter dabayein menu ke liye..."
    main_menu
}

main_menu
