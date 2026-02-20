import argparse
import sys
import urllib.request
import urllib.error
import re
import json
import time

def fetch_content(url):
    print(f"Fetching {url}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"[ERROR] Fetch failed: {e}")
        return None

def extract_tag(content, tag_name, attr=None, attr_val=None):
    if attr:
        pattern = fr'<{tag_name}[^>]*{attr}=[\'"]{attr_val}[\'"][^>]*>(.*?)</{tag_name}>'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match: return match.group(1).strip()
        pattern_meta = fr'<{tag_name}[^>]*{attr}=[\'"]{attr_val}[\'"][^>]*content=[\'"](.*?)[\'"]'
        match_meta = re.search(pattern_meta, content, re.DOTALL | re.IGNORECASE)
        if match_meta: return match_meta.group(1).strip()
    else:
        pattern = fr'<{tag_name}[^>]*>(.*?)</{tag_name}>'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match: return match.group(1).strip()
    return None

def analyze_metadata(content):
    print("\n--- Metadata ---")
    title = extract_tag(content, 'title')
    desc = extract_tag(content, 'meta', 'name', 'description')
    h1 = extract_tag(content, 'h1')
    
    print(f"Title:       {'[PASS] ' + title if title else '[FAIL] MISSING'}")
    print(f"Description: {'[PASS] ' + desc if desc else '[FAIL] MISSING'}")
    print(f"H1:          {'[PASS] ' + h1 if h1 else '[FAIL] MISSING'}")

def analyze_links(content, base_url):
    print("\n--- Links ---")
    links = re.findall(r'href=[\'"](.*?)[\'"]', content)
    internal = [l for l in links if l.startswith('/') or base_url in l]
    external = [l for l in links if l.startswith('http') and base_url not in l]
    print(f"Total: {len(links)} | Internal: {len(internal)} | External: {len(external)}")

def validate_schema(content):
    print("\n--- Schema ---")
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not scripts:
        print("[FAIL] No JSON-LD found.")
        return
    
    for i, script in enumerate(scripts):
        try:
            data = json.loads(script)
            print(f"[PASS] Block #{i+1}: Valid JSON - Type: {data.get('@type', 'Unknown')}")
        except json.JSONDecodeError:
            print(f"[FAIL] Block #{i+1}: Invalid JSON")

def run_audit(url):
    start_time = time.time()
    content = fetch_content(url)
    if not content:
        return
        
    analyze_metadata(content)
    analyze_links(content, url)
    validate_schema(content)
    
    print(f"\nAudit completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    args = parser.parse_args()
    
    run_audit(args.url)
