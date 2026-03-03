#!/usr/bin/env python3
"""
Move audio-player shortcodes from right after headings to the end of each section.

Current (WRONG):
## 1. Từ vựng mới
{{< audio-player ... >}}
[content...]

Target (CORRECT):
## 1. Từ vựng mới
[content...]
{{< audio-player ... >}}
"""

import os
import re
from pathlib import Path

def fix_audio_positions(content):
    """
    Move audio-player shortcodes from after headings to the end of sections.
    """
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        result_lines.append(line)
        
        # Check if this is a heading (but not the final "🎧 Bài nghe kiểm tra" section)
        if (line.startswith('## ') and 
            not line.startswith('## 🎧') and 
            '🎧' not in line):
            
            # Look ahead to collect audio players immediately after this heading
            audio_players = []
            j = i + 1
            
            # Skip empty lines first
            while j < len(lines) and lines[j].strip() == '':
                result_lines.append(lines[j])
                j += 1
            
            # Collect consecutive audio-player shortcodes
            while j < len(lines) and lines[j].strip().startswith('{{< audio-player'):
                audio_players.append(lines[j])
                j += 1
                # Skip empty line after audio player if exists
                if j < len(lines) and lines[j].strip() == '':
                    j += 1
            
            if audio_players:
                # Skip the audio players in the original position
                i = j - 1  # -1 because the loop will increment i
                
                # Find the end of this section (before next ## heading or end of file)
                section_end = j
                while section_end < len(lines):
                    if lines[section_end].startswith('## '):
                        break
                    section_end += 1
                
                # Add content lines until section end
                content_lines = []
                for k in range(j, section_end):
                    content_lines.append(lines[k])
                
                # Remove trailing empty lines
                while content_lines and content_lines[-1].strip() == '':
                    content_lines.pop()
                
                # Add content lines
                result_lines.extend(content_lines)
                
                # Add audio players at the end of the section
                if content_lines:  # Only add if there was content
                    result_lines.append('')  # Empty line before audio
                for audio in audio_players:
                    result_lines.append(audio)
                
                # Add empty line after audio if next section exists
                if section_end < len(lines):
                    result_lines.append('')
                
                # Skip to the next section
                i = section_end - 1  # -1 because the loop will increment i
        
        i += 1
    
    return '\n'.join(result_lines)

def process_lesson_file(file_path):
    """Process a single lesson file."""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix audio positions
        fixed_content = fix_audio_positions(content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ Fixed: {file_path}")
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def main():
    """Process all lesson files in N5 and N4 directories."""
    base_dir = Path('/home/node/.openclaw/workspace/jlptpath/content/jlpt')
    
    # Process N5 lessons (bai-1 to bai-25)
    n5_dir = base_dir / 'n5'
    n4_dir = base_dir / 'n4'
    
    processed_count = 0
    
    # N5 lessons
    for i in range(1, 26):  # bai-1 to bai-25
        pattern = f"bai-{i}-*.md"
        files = list(n5_dir.glob(pattern))
        for file_path in files:
            process_lesson_file(file_path)
            processed_count += 1
    
    # N4 lessons
    for i in range(26, 51):  # bai-26 to bai-50
        pattern = f"bai-{i}-*.md"
        files = list(n4_dir.glob(pattern))
        for file_path in files:
            process_lesson_file(file_path)
            processed_count += 1
    
    print(f"\n🎉 Processed {processed_count} lesson files!")
    print("Audio players have been moved to the end of their respective sections.")

if __name__ == "__main__":
    main()