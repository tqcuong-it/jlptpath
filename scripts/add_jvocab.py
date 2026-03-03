#!/usr/bin/env python3
"""Convert ruby annotations in reading posts to clickable jvocab spans.

For each post:
1. Parse vocab table to get word → reading + meaning
2. In the 📰 Bài đọc section, replace <ruby>word<rt>reading</rt></ruby> 
   with <span class="jvocab" data-reading="reading" data-meaning="meaning">word</span>
3. Keep ruby for words NOT in vocab table (so furigana still shows)
"""

import re
import os
import glob

READING_DIR = "/home/node/.openclaw/workspace/jlptpath/content/reading"

def parse_vocab_table(content):
    """Extract vocab from markdown table: | 今日 | きょう | hôm nay | danh từ |"""
    vocab = {}
    in_table = False
    for line in content.split('\n'):
        if '| Từ vựng' in line or '| **Từ vựng**' in line:
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and line.startswith('|'):
            cols = [c.strip() for c in line.split('|')]
            cols = [c for c in cols if c]  # remove empty
            if len(cols) >= 3:
                word = cols[0].strip('* ')
                reading = cols[1].strip('* ')
                meaning = cols[2].strip('* ')
                if word and reading:
                    vocab[word] = {'reading': reading, 'meaning': meaning}
        elif in_table and not line.startswith('|'):
            in_table = False
    return vocab

def replace_ruby_with_jvocab(content, vocab):
    """In bài đọc section, replace <ruby>X<rt>Y</rt></ruby> with jvocab span if X is in vocab."""
    
    # Find the bài đọc section (between ## 📰 Bài đọc and next ##)
    sections = re.split(r'(## [^\n]+)', content)
    result = []
    in_reading = False
    
    for i, section in enumerate(sections):
        if '📰 Bài đọc' in section or 'Bài đọc' in section and section.startswith('##'):
            in_reading = True
            result.append(section)
            continue
        
        if section.startswith('##') and in_reading:
            in_reading = False
        
        if in_reading:
            # Replace ruby tags with jvocab spans
            def ruby_replacer(m):
                word = m.group(1)
                reading = m.group(2)
                if word in vocab:
                    meaning = vocab[word]['meaning']
                    # Escape HTML attributes
                    meaning_esc = meaning.replace('"', '&quot;')
                    reading_esc = reading.replace('"', '&quot;')
                    return f'<span class="jvocab" data-reading="{reading_esc}" data-meaning="{meaning_esc}">{word}</span>'
                else:
                    # Keep ruby for non-vocab words
                    return m.group(0)
            
            section = re.sub(
                r'<ruby>([^<]+)<rt>([^<]+)</rt></ruby>',
                ruby_replacer,
                section
            )
        
        result.append(section)
    
    return ''.join(result)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has jvocab
    if 'class="jvocab"' in content:
        return False
    
    # Skip if no ruby tags
    if '<ruby>' not in content:
        return False
    
    vocab = parse_vocab_table(content)
    if not vocab:
        return False
    
    new_content = replace_ruby_with_jvocab(content, vocab)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    files = sorted(glob.glob(os.path.join(READING_DIR, "bai-*.md")))
    converted = 0
    skipped = 0
    no_ruby = 0
    
    for f in files:
        basename = os.path.basename(f)
        result = process_file(f)
        if result:
            converted += 1
            print(f"✅ {basename}")
        elif result is False:
            with open(f, 'r') as fh:
                c = fh.read()
            if 'class="jvocab"' in c:
                skipped += 1
            else:
                no_ruby += 1
    
    print(f"\n📊 Converted: {converted} | Already done: {skipped} | No ruby: {no_ruby} | Total: {len(files)}")

if __name__ == '__main__':
    main()
