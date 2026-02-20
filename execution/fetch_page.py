import argparse
import sys
import urllib.request
import urllib.error
import os

def fetch_page(url):
    print(f"Fetching {url}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        # Save to .tmp
        filename = ".tmp/page.html"
        if not os.path.exists('.tmp'):
            os.makedirs('.tmp')
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Success. Saved to {filename}")
        
    except Exception as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    args = parser.parse_args()
    
    fetch_page(args.url)
