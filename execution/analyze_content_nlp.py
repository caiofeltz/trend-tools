import argparse
import re
import collections
import math
import os
import sys

# Note: In a full production env, we would use spaCy or NLTK.
# This script implements a basic TF-IDF and Entity-like extraction using standard lib + optional upgrades.

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def get_word_counts(text):
    words = clean_text(text).split()
    return collections.Counter(words), len(words)

def calculate_readability(text):
    # Approximate Flesch-Kincaid
    sentences = max(1, text.count('.') + text.count('!') + text.count('?'))
    words = len(clean_text(text).split())
    syllables = 0
    for word in clean_text(text).split():
        # Very rough syllable estimation
        syllables += max(1, len(re.findall(r'[aeiouy]+', word)))
    
    if words == 0: return 0
    
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return round(score, 2)

def analyze_content(input_path, keywords):
    content = ""
    # Support URL eventually, for now only file path
    if input_path.startswith('http'):
        print("Error: URL fetching not yet implemented in this script. Download page first.")
        sys.exit(1)
        
    if not os.path.exists(input_path):
        print(f"Error: File not found {input_path}")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    word_counts, total_words = get_word_counts(content)
    readability = calculate_readability(content)
    
    print(f"--- Analysis Report for {os.path.basename(input_path)} ---")
    print(f"Total Words: {total_words}")
    print(f"Readability Score: {readability} (Aim for 60-70)")
    print("\n--- Keyword Analysis ---")
    
    if keywords:
        kw_list = [k.strip().lower() for k in keywords.split(',')]
        for kw in kw_list:
            count = word_counts[kw] if ' ' not in kw else content.lower().count(kw)
            density = (count / total_words) * 100 if total_words > 0 else 0
            status = "Good" if 0.5 <= density <= 2.5 else ("Low" if density < 0.5 else "High")
            print(f"Keyword '{kw}': {count} instances ({density:.2f}%) - {status}")
    
    print("\n--- Top Entities (Simulated) ---")
    # Simple frequent nouns heuristic (words > 4 chars)
    common = [w for w, c in word_counts.most_common(20) if len(w) > 4 and w not in ['which', 'there', 'their', 'about', 'would']]
    print(", ".join(common[:10]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze content using NLP metrics.')
    parser.add_argument('--input', required=True, help='Path to content file')
    parser.add_argument('--keywords', help='Target keywords')

    args = parser.parse_args()
    analyze_content(args.input, args.keywords)
