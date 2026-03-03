#!/usr/bin/env python3
"""Add jvocab spans to posts without ruby tags (N2/N1).

For each word in the vocab table, find its FIRST occurrence in the 
📰 Bài đọc section and wrap it with a jvocab span.
"""

import re
import os
import glob

READING_DIR = "/home/node/.openclaw/workspace/jlptpath/content/reading"

def parse_vocab_table(content):
    """Extract vocab: word → {reading, meaning}"""
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
            cols = [c for c in cols if c]
            if len(cols) >= 3:
                word = cols[0].strip('* ')
                reading = cols[1].strip('* ')
                meaning = cols[2].strip('* ')
                if word and reading and len(word) >= 2:
                    vocab[word] = {'reading': reading, 'meaning': meaning}
        elif in_table and not line.startswith('|'):
            in_table = False
    return vocab

def add_jvocab_to_reading(content, vocab):
    """Find bài đọc section and wrap first occurrence of each vocab word."""
    
    # Split into before-reading, reading, after-reading
    reading_start = re.search(r'## 📰 Bài đọc\n', content)
    if not reading_start:
        return content
    
    after_reading = content[reading_start.end():]
    next_section = re.search(r'\n## ', after_reading)
    if not next_section:
        return content
    
    reading_text = after_reading[:next_section.start()]
    rest = after_reading[next_section.start():]
    
    # Sort vocab by length (longer first to avoid partial matches)
    sorted_vocab = sorted(vocab.items(), key=lambda x: len(x[0]), reverse=True)
    
    used = set()
    for word, info in sorted_vocab:
        if word in used:
            continue
        # Only replace first occurrence, skip if inside HTML tags
        meaning_esc = info['meaning'].replace('"', '&quot;')
        reading_esc = info['reading'].replace('"', '&quot;')
        replacement = f'<span class="jvocab" data-reading="{reading_esc}" data-meaning="{meaning_esc}">{word}</span>'
        
        # Find first occurrence not inside an HTML tag
        pattern = re.compile(re.escape(word))
        match = pattern.search(reading_text)
        if match:
            # Check we're not inside an existing span
            before = reading_text[:match.start()]
            if '<span' in before:
                last_span = before.rfind('<span')
                last_close = before.rfind('</span>')
                if last_span > last_close:
                    # Inside a span, skip
                    continue
            
            reading_text = reading_text[:match.start()] + replacement + reading_text[match.end():]
            used.add(word)
    
    return content[:reading_start.end()] + reading_text + rest

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has jvocab
    if 'class="jvocab"' in content:
        return 'skip'
    
    # Skip if has ruby (handled by other script)
    if '<ruby>' in content:
        return 'ruby'
    
    vocab = parse_vocab_table(content)
    if not vocab:
        return 'no_vocab'
    
    new_content = add_jvocab_to_reading(content, vocab)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return 'ok'
    return 'unchanged'

def main():
    files = sorted(glob.glob(os.path.join(READING_DIR, "bai-*.md")))
    stats = {'ok': 0, 'skip': 0, 'ruby': 0, 'no_vocab': 0, 'unchanged': 0}
    
    for f in files:
        basename = os.path.basename(f)
        result = process_file(f)
        stats[result] += 1
        if result == 'ok':
            print(f"✅ {basename}")
    
    print(f"\n📊 Converted: {stats['ok']} | Already done: {stats['skip']} | Has ruby: {stats['ruby']} | No vocab: {stats['no_vocab']} | Unchanged: {stats['unchanged']}")

if __name__ == '__main__':
    main()
