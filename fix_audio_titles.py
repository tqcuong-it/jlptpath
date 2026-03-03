#!/usr/bin/env python3

import os
import re
import glob
from pathlib import Path

# Base directory
base_dir = Path("/home/node/.openclaw/workspace/jlptpath")

# Title patterns based on track count and JLPT level
MINNA_TITLES = {
    3: [
        "Từ vựng (ことば) 🔤 — Nghe và nhắc lại từng từ",
        "Mẫu câu (ぶんけい) 📝 — Nghe mẫu câu, chú ý ngữ pháp",
        "Luyện tập (れんしゅう) ✏️ — Nghe và trả lời câu hỏi"
    ],
    4: [
        "Từ vựng (ことば) 🔤 — Nghe và nhắc lại từng từ",
        "Mẫu câu (ぶんけい) 📝 — Nghe mẫu câu, chú ý ngữ pháp",
        "Hội thoại (かいわ) 💬 — Nghe hội thoại, đoán nội dung trước",
        "Luyện tập (れんしゅう) ✏️ — Nghe và trả lời câu hỏi"
    ],
    5: [
        "Từ vựng (ことば) 🔤 — Nghe và nhắc lại từng từ",
        "Mẫu câu (ぶんけい) 📝 — Nghe mẫu câu, chú ý ngữ pháp",
        "Hội thoại (かいわ) 💬 — Nghe hội thoại, đoán nội dung trước",
        "Luyện tập A (れんしゅうA) ✏️ — Nghe và điền đáp án",
        "Luyện tập B (れんしゅうB) ✏️ — Nghe và trả lời câu hỏi"
    ]
}

def get_audio_count(level, lesson_num):
    """Get the number of audio files for a lesson"""
    if level in ['n5', 'n4']:
        pattern = f"{base_dir}/static/audio/{level}/lesson{lesson_num}_*"
    elif level == 'n3':
        pattern = f"{base_dir}/static/audio/{level}/*lesson{lesson_num}_*"
    else:  # n2, n1 - these have different structure
        return 0
        
    files = glob.glob(pattern)
    return len(files)

def get_lesson_files(level):
    """Get all lesson markdown files for a level"""
    content_dir = base_dir / "content" / "jlpt" / level
    return list(content_dir.glob("bai-*.md"))

def extract_lesson_number(filename):
    """Extract lesson number from filename"""
    match = re.search(r'bai-(\d+)', filename.stem)
    return int(match.group(1)) if match else None

def update_audio_shortcodes(file_path, new_titles, level, lesson_num):
    """Update audio shortcodes in a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all audio-player shortcodes
    audio_pattern = r'\{\{<\s*audio-player\s+src="([^"]+)"\s+title="([^"]+)"\s*>\}\}'
    matches = list(re.finditer(audio_pattern, content))
    
    if not matches:
        print(f"  No audio shortcodes found in {file_path.name}")
        return False
    
    # Replace from bottom to top to maintain correct indices
    for i, match in enumerate(reversed(matches)):
        idx = len(matches) - 1 - i  # Original index
        if idx < len(new_titles):
            src = match.group(1)
            new_shortcode = f'{{{{< audio-player src="{src}" title="{new_titles[idx]}" >}}}}'
            content = content[:match.start()] + new_shortcode + content[match.end():]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def process_level(level, max_lessons):
    """Process all lessons for a JLPT level"""
    print(f"\n🎯 Processing JLPT {level.upper()}")
    
    lesson_files = get_lesson_files(level)
    processed = 0
    
    for file_path in sorted(lesson_files):
        lesson_num = extract_lesson_number(file_path)
        if not lesson_num or lesson_num > max_lessons:
            continue
            
        if level in ['n5', 'n4', 'n3']:
            # Get audio count
            audio_count = get_audio_count(level, lesson_num)
            if audio_count == 0:
                print(f"  ⚠️  Lesson {lesson_num}: No audio files found")
                continue
            
            # Get appropriate titles
            if audio_count in MINNA_TITLES:
                titles = MINNA_TITLES[audio_count]
                print(f"  📝 Lesson {lesson_num}: {audio_count} tracks - applying Minna pattern")
                
                if update_audio_shortcodes(file_path, titles, level, lesson_num):
                    processed += 1
                    print(f"     ✅ Updated {file_path.name}")
                else:
                    print(f"     ❌ Failed to update {file_path.name}")
            else:
                print(f"  ⚠️  Lesson {lesson_num}: Unexpected track count {audio_count}")
                
        elif level in ['n2', 'n1']:
            # For N2/N1, use Shinkanzen pattern - need to check actual content
            print(f"  📝 Lesson {lesson_num}: Applying Shinkanzen pattern")
            # Will be handled separately since these have different structure
            
    print(f"✅ {level.upper()}: Updated {processed} lessons")

def main():
    print("🎵 Fixing JLPT Audio Track Titles...")
    print("=" * 50)
    
    # Process each level
    levels_config = {
        'n5': 25,
        'n4': 25,
        'n3': 20,  # Actually only has 12 lessons
        'n2': 20,
        'n1': 20
    }
    
    total_processed = 0
    for level, max_lessons in levels_config.items():
        process_level(level, max_lessons)
    
    print(f"\n🎉 Audio title fixes completed!")

if __name__ == "__main__":
    main()