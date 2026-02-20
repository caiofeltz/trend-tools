import argparse
import re
import sys

# Simulating parsing without BeautifulSoup for reliability if not installed, 
# although in a real setup we'd probably assume BS4 is present or install it.
# Using Regex for basic extraction (Note: Regex is fragile for HTML, but keeps valid deps low).

def extract_tag(content, tag_name, attr=None, attr_val=None):
    if attr:
        # crude regex for <tag attr="val">...</tag> or <tag attr="val" />
        pattern = fr'<{tag_name}[^>]*{attr}=[\'"]{attr_val}[\'"][^>]*>(.*?)</{tag_name}>'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match: return match.group(1).strip()
        
        # Self closing/meta
        pattern_meta = fr'<{tag_name}[^>]*{attr}=[\'"]{attr_val}[\'"][^>]*content=[\'"](.*?)[\'"]'
        match_meta = re.search(pattern_meta, content, re.DOTALL | re.IGNORECASE)
        if match_meta: return match_meta.group(1).strip()
        
    else:
        pattern = fr'<{tag_name}[^>]*>(.*?)</{tag_name}>'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match: return match.group(1).strip()
    return None

def analyze_metadata(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_tag(content, 'title')
    desc = extract_tag(content, 'meta', 'name', 'description')
    h1 = extract_tag(content, 'h1')
    canonical = extract_tag(content, 'link', 'rel', 'canonical')
    
    print("--- Metadata Report ---")
    if title:
        print(f"[PASS] Title: {title} ({len(title)} chars)")
    else:
        print(f"[FAIL] Title: MISSING")
        
    if desc:
        print(f"[PASS] Description: {desc} ({len(desc)} chars)")
    else:
        print(f"[FAIL] Description: MISSING")
        
    if h1:
         print(f"[PASS] H1: {h1}")
    else:
         print(f"[FAIL] H1: MISSING")
         
    if canonical:
        print(f"[INFO] Canonical: {canonical}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    
    analyze_metadata(args.input)
