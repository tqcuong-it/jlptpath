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
    ],
    6: [
        "Từ vựng (ことば) 🔤 — Nghe và nhắc lại từng từ",
        "Mẫu câu (ぶんけい) 📝 — Nghe mẫu câu, chú ý ngữ pháp",
        "Hội thoại (かいわ) 💬 — Nghe hội thoại, đoán nội dung trước",
        "Luyện tập A (れんしゅうA) ✏️ — Nghe và điền đáp án",
        "Luyện tập B (れんしゅうB) ✏️ — Nghe và trả lời câu hỏi",
        "Mở rộng (おうよう) 🔄 — Nghe và thực hành nâng cao"
    ],
    7: [
        "Từ vựng (ことば) 🔤 — Nghe và nhắc lại từng từ",
        "Mẫu câu (ぶんけい) 📝 — Nghe mẫu câu, chú ý ngữ pháp",
        "Hội thoại (かいわ) 💬 — Nghe hội thoại, đoán nội dung trước",
        "Luyện tập A (れんしゅうA) ✏️ — Nghe và điền đáp án",
        "Luyện tập B (れんしゅうB) ✏️ — Nghe và trả lời câu hỏi",
        "Mở rộng A (おうようA) 🔄 — Nghe và thực hành nâng cao",
        "Mở rộng B (おうようB) 🔄 — Nghe và ứng dụng thực tế"
    ]
}

def get_actual_lesson_number(file_path, level):
    """Extract the actual lesson number from audio files or content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find audio shortcodes
    audio_pattern = r'\{\{<\s*audio-player\s+src="([^"]+)"'
    matches = re.findall(audio_pattern, content)
    
    if matches:
        # Extract lesson number from first audio file
        first_audio = matches[0]
        if level == 'n4':
            # N4 audio files: lesson26_*, lesson27_*, etc.
            match = re.search(r'lesson(\d+)_', first_audio)
            if match:
                return int(match.group(1))
        elif level == 'n3':
            # N3 audio files: chukyu1_lesson10_*, etc.
            match = re.search(r'lesson(\d+)_', first_audio)
            if match:
                return int(match.group(1))
        else:
            # N5 audio files: lesson1_*, lesson2_*, etc.
            match = re.search(r'lesson(\d+)_', first_audio)
            if match:
                return int(match.group(1))
    
    return None

def get_audio_count_from_content(file_path):
    """Count audio shortcodes directly from markdown content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    audio_pattern = r'\{\{<\s*audio-player\s+src="([^"]+)"'
    matches = re.findall(audio_pattern, content)
    return len(matches)

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

def process_minna_levels():
    """Process N4, N5, N3 with Minna patterns"""
    levels = ['n4', 'n5', 'n3']
    
    for level in levels:
        print(f"\n🎯 Processing JLPT {level.upper()}")
        
        content_dir = base_dir / "content" / "jlpt" / level
        lesson_files = list(content_dir.glob("bai-*.md"))
        processed = 0
        
        for file_path in sorted(lesson_files):
            lesson_num = get_actual_lesson_number(file_path, level)
            if not lesson_num:
                print(f"  ⚠️  {file_path.name}: Could not determine lesson number")
                continue
                
            # Get audio count from content
            audio_count = get_audio_count_from_content(file_path)
            if audio_count == 0:
                print(f"  ⚠️  {file_path.name}: No audio files found")
                continue
            
            # Get appropriate titles
            if audio_count in MINNA_TITLES:
                titles = MINNA_TITLES[audio_count]
                print(f"  📝 {file_path.name}: {audio_count} tracks - applying Minna pattern")
                
                if update_audio_shortcodes(file_path, titles, level, lesson_num):
                    processed += 1
                    print(f"     ✅ Updated successfully")
                else:
                    print(f"     ❌ Failed to update")
            else:
                print(f"  ⚠️  {file_path.name}: Unexpected track count {audio_count}")
                
        print(f"✅ {level.upper()}: Updated {processed} lessons")

def process_shinkanzen_level(level):
    """Process N2/N1 with Shinkanzen patterns"""
    print(f"\n🎯 Processing JLPT {level.upper()} (Shinkanzen)")
    
    content_dir = base_dir / "content" / "jlpt" / level
    lesson_files = list(content_dir.glob("bai-*.md"))
    processed = 0
    
    for file_path in sorted(lesson_files):
        # Extract lesson number from filename
        match = re.search(r'bai-(\d+)', file_path.name)
        if not match:
            continue
            
        lesson_num = int(match.group(1))
        
        # Get audio count from content
        audio_count = get_audio_count_from_content(file_path)
        if audio_count == 0:
            print(f"  ⚠️  {file_path.name}: No audio files found")
            continue
        
        # Create Shinkanzen titles
        shinkanzen_titles = []
        for i in range(1, audio_count + 1):
            title = f"聴解問題 {i} 🎧 — Nghe và chọn đáp án đúng"
            shinkanzen_titles.append(title)
        
        print(f"  📝 {file_path.name}: {audio_count} tracks - applying Shinkanzen pattern")
        
        if update_audio_shortcodes(file_path, shinkanzen_titles, level, lesson_num):
            processed += 1
            print(f"     ✅ Updated successfully")
        else:
            print(f"     ❌ Failed to update")
            
    print(f"✅ {level.upper()}: Updated {processed} lessons")

def main():
    print("🎵 Fixing JLPT Audio Track Titles (Version 2)")
    print("=" * 55)
    
    # Process Minna levels (N5, N4, N3)
    process_minna_levels()
    
    # Process Shinkanzen levels (N2, N1)
    process_shinkanzen_level('n2')
    process_shinkanzen_level('n1')
    
    print(f"\n🎉 Audio title fixes completed!")

if __name__ == "__main__":
    main()