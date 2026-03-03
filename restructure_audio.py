#!/usr/bin/env python3
"""
Restructure JLPT lesson audio placement:
- Move audio from bottom section to inline with content sections
- Place each audio type right after its corresponding heading
- Keep Mondai tracks in a separate section at bottom
"""

import os
import re
import glob
from pathlib import Path

def get_lesson_number_from_filename(filename):
    """Extract lesson number from filename like 'bai-1-...' or 'bai-26-...'"""
    match = re.search(r'bai-(\d+)', filename)
    return int(match.group(1)) if match else None

def get_available_audio_files(level):
    """Get dict of available audio files for a level (n5 or n4)"""
    audio_dir = f"/home/node/.openclaw/workspace/jlptpath/static/audio/{level}/"
    if not os.path.exists(audio_dir):
        return {}
    
    files = os.listdir(audio_dir)
    audio_map = {}
    
    for file in files:
        if file.endswith('.mp3'):
            # Parse filename like "1_-_1_-_Kotoba.mp3"
            parts = file.replace('.mp3', '').split('_-_')
            if len(parts) >= 3:
                lesson_num = int(parts[0])
                track_num = parts[1]
                track_type = parts[2]
                
                if lesson_num not in audio_map:
                    audio_map[lesson_num] = {}
                audio_map[lesson_num][track_type] = file
    
    return audio_map

def create_audio_shortcode(src_path, title):
    """Create an audio-player shortcode"""
    return f'{{{{< audio-player src="{src_path}" title="{title}" >}}}}'

def get_audio_title(track_type, lesson_num):
    """Get proper title for each track type"""
    titles = {
        'Kotoba': f"🔊 Nghe từ vựng bài {lesson_num}",
        'Bunkei': "🔊 Nghe mẫu câu", 
        'Reibun': "🔊 Nghe ví dụ",
        'Kaiwa': "🔊 Nghe hội thoại",
        'Renshuu_C1': "🔊 Luyện tập C1",
        'Renshuu_C2': "🔊 Luyện tập C2", 
        'Renshuu_C3': "🔊 Luyện tập C3",
        'Mondai_1': "🔊 問題1 — Nghe và trả lời",
        'Mondai_2': "🔊 問題2 — Nghe và trả lời",
        'Mondai_3': "🔊 問題3 — Nghe và trả lời",
        'Mondai_4': "🔊 問題4 — Nghe và trả lời",
    }
    return titles.get(track_type, f"🔊 {track_type}")

def restructure_lesson_content(content, lesson_num, level, audio_map):
    """Restructure a single lesson's content"""
    
    # Remove the entire audio section (heading + all content until next heading or EOF)
    audio_section_pattern = r'## 🎧 Audio bài học.*?(?=^## |\Z)'
    content = re.sub(audio_section_pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Get available audio for this lesson
    lesson_audio = audio_map.get(lesson_num, {})
    
    if not lesson_audio:
        print(f"   No audio files found for lesson {lesson_num}")
        return content
    
    # Prepare audio shortcodes for each section
    audio_inserts = {}
    mondai_tracks = []
    
    for track_type, filename in lesson_audio.items():
        src_path = f"/audio/{level}/{filename}"
        title = get_audio_title(track_type, lesson_num)
        shortcode = create_audio_shortcode(src_path, title)
        
        # Group tracks by where they should be placed
        if track_type == 'Kotoba':
            audio_inserts.setdefault('vocab', []).append(shortcode)
        elif track_type in ['Bunkei', 'Reibun']:
            audio_inserts.setdefault('grammar', []).append(shortcode)
        elif track_type == 'Kaiwa':
            audio_inserts.setdefault('dialogue', []).append(shortcode)
        elif track_type.startswith('Renshuu_C'):
            audio_inserts.setdefault('exercises', []).append(shortcode)
        elif track_type.startswith('Mondai_'):
            mondai_tracks.append(shortcode)
    
    # Insert audio after each section heading
    section_mappings = [
        (r'(## 1\. Từ vựng mới)', 'vocab'),
        (r'(## 2\. Ngữ pháp)', 'grammar'), 
        (r'(## 3\. Hội thoại mẫu)', 'dialogue'),
        (r'(## 4\. Bài tập)', 'exercises'),
    ]
    
    for pattern, audio_key in section_mappings:
        if audio_key in audio_inserts:
            audio_block = '\n\n' + '\n\n'.join(audio_inserts[audio_key])
            content = re.sub(pattern, r'\1' + audio_block, content)
    
    # Add Mondai section at the end if we have any
    if mondai_tracks:
        mondai_section = '\n\n## 🎧 Bài nghe kiểm tra\n\n' + '\n\n'.join(mondai_tracks)
        content += mondai_section
    
    # Clean up any double newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def process_level(level):
    """Process all lessons in a level (n5 or n4)"""
    print(f"\n📚 Processing {level.upper()} lessons...")
    
    # Get available audio files
    audio_map = get_available_audio_files(level)
    if not audio_map:
        print(f"   No audio files found for {level}")
        return
    
    print(f"   Found audio for lessons: {sorted(audio_map.keys())}")
    
    # Get all lesson files
    content_dir = f"/home/node/.openclaw/workspace/jlptpath/content/jlpt/{level}/"
    lesson_files = glob.glob(os.path.join(content_dir, "bai-*.md"))
    
    if not lesson_files:
        print(f"   No lesson files found in {content_dir}")
        return
    
    print(f"   Found {len(lesson_files)} lesson files")
    
    processed = 0
    
    for file_path in sorted(lesson_files):
        filename = os.path.basename(file_path)
        lesson_num = get_lesson_number_from_filename(filename)
        
        if lesson_num is None:
            print(f"   Skipping {filename} - couldn't extract lesson number")
            continue
        
        print(f"   Processing lesson {lesson_num}: {filename}")
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if no audio section found
            if '## 🎧 Audio bài học' not in content:
                print(f"     No audio section found - skipping")
                continue
            
            # Restructure content
            new_content = restructure_lesson_content(content, lesson_num, level, audio_map)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"     ✅ Restructured successfully")
            processed += 1
            
        except Exception as e:
            print(f"     ❌ Error processing {filename}: {e}")
    
    print(f"   📊 {processed} lessons restructured")

def main():
    print("🎵 JLPT Audio Restructuring Tool")
    print("Moving audio from bottom section to inline with content sections...")
    
    # Process both N5 and N4 levels
    process_level('n5')
    process_level('n4')
    
    print("\n✨ Audio restructuring complete!")
    print("\n📋 Summary:")
    print("  - Kotoba → after '## 1. Từ vựng mới'")
    print("  - Bunkei + Reibun → after '## 2. Ngữ pháp'")
    print("  - Kaiwa → after '## 3. Hội thoại mẫu'") 
    print("  - Renshuu_C1/C2/C3 → after '## 4. Bài tập'")
    print("  - Mondai_1/2/3 → new section '## 🎧 Bài nghe kiểm tra'")

if __name__ == "__main__":
    main()