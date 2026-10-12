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

main_menu() {
    show_banner
    echo "1)  Naya video banao (single)"
    echo "2)  Batch mode (kai videos ek saath)"
    echo "3)  Sirf audio banao (voice only)"
    echo "4)  Purani videos dekho (output folder)"
    echo "5)  Exit"
    echo ""
    read -p "Apna choice daalein [1-5]: " choice
    case $choice in
        1) single_video ;;
        2) batch_mode ;;
        3) audio_only ;;
        4) list_outputs ;;
        5) echo "Allah Hafiz!"; exit 0 ;;
        *) echo "Ghalat choice! Wapas try karein..."; sleep 2; main_menu ;;
    esac
}

single_video() {
    show_banner
    echo "=== NAYA VIDEO BANAO ==="
    echo ""
    read -p "Text likhein (Roman Urdu/Hindi): " user_text
    if [ -z "$user_text" ]; then
        echo "Text khaali nahi ho sakta!"
        sleep 2
        main_menu
    fi
    
    read -p "Video search keyword (e.g., cat, dog, ocean): " search_term
    read -p "Video ka naam (file name): " video_name
    
    echo ""
    echo "Subtitles chahiye? [on/off]: "
    read -p "> " subs
    subs=${subs:-on}
    
    style="default"
    if [ "$subs" = "on" ]; then
        echo ""
        echo "Subtitle styles available:"
        echo "  1. default (yellow bottom)"
        echo "  2. white (white bottom)"
        echo "  3. yellow_big (big yellow)"
        echo "  4. top_white (white top)"
        echo "  5. green_bold (green bottom)"
        read -p "Style number [1-5, default=1]: " style_num
        case $style_num in
            1|"") style="default" ;;
            2) style="white" ;;
            3) style="yellow_big" ;;
            4) style="top_white" ;;
            5) style="green_bold" ;;
            *) style="default" ;;
        esac
    fi
    
    echo ""
    read -p "Background music chahiye? [on/off, default=off]: " music
    music=${music:-off}
    
    echo ""
    echo "=== VIDEO BANANA SHURU ==="
    echo ""
    python "$SCRIPTS/create_video.py" "$user_text" "$search_term" "$video_name" "$subs" "$style" "$music"
    
    echo ""
    read -p "Enter dabayein main menu ke liye..."
    main_menu
}

batch_mode() {
    show_banner
    echo "=== BATCH MODE ==="
    echo ""
    echo "Input file ka format:"
    echo "  text | search | video_name | subs"
    echo ""
    read -p "Input file ka path (default: input/batch1.txt): " batch_file
    batch_file=${batch_file:-$VIDEO_APP/input/batch1.txt}
    
    if [ ! -f "$batch_file" ]; then
        echo "File nahi mili: $batch_file"
        sleep 3
        main_menu
    fi
    
    echo ""
    echo "=== BATCH SHURU ==="
    python "$SCRIPTS/batch_create.py" "$batch_file"
    
    echo ""
    read -p "Enter dabayein main menu ke liye..."
    main_menu
}

audio_only() {
    show_banner
    echo "=== SIRF AUDIO BANAO ==="
    echo ""
    read -p "Text likhein: " user_text
    read -p "Audio file ka naam: " audio_name
    
    echo ""
    python "$SCRIPTS/generate_audio.py" "$audio_name" "$user_text"
    
    echo ""
    read -p "Music bhi mix karein? [on/off, default=off]: " music
    music=${music:-off}
    if [ "$music" = "on" ]; then
        python "$SCRIPTS/mix_music.py" "$audio_name" "${audio_name}_music"
    fi
    
    echo ""
    read -p "Enter dabayein main menu ke liye..."
    main_menu
}

list_outputs() {
    show_banner
    echo "=== OUTPUT FOLDER ==="
    echo ""
    ls -lh "$VIDEO_APP/output/" | grep -E "\.mp4|\.mp3" | tail -20
    echo ""
    read -p "Enter dabayein main menu ke liye..."
    main_menu
}

main_menu
