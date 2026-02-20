import argparse
import csv
import sys
import time
from urllib.parse import urlparse, urljoin
import os

# Try importing Playwright, handle error gracefully
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright is not installed. Please run: pip install playwright && playwright install chromium")
    sys.exit(1)

def normalize_url(url):
    return url.split('#')[0].rstrip('/')

def crawl_site(start_url, max_pages=50):
    domain = urlparse(start_url).netloc
    visited = set()
    queue = [start_url]
    results = []
    
    print(f"Starting crawl on {start_url} (Max: {max_pages} pages)")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if normalize_url(url) in visited:
                continue
            
            visited.add(normalize_url(url))
            print(f"[{len(visited)}/{max_pages}] Crawling: {url}")
            
            try:
                # 1. Navigate
                response = page.goto(url, wait_until="networkidle", timeout=20000)
                status = response.status if response else 0
                
                # 2. Extract Data
                title = page.title()
                
                # Meta Description
                desc_el = page.query_selector('meta[name="description"]')
                description = desc_el.get_attribute('content') if desc_el else ""
                
                # H1
                h1_el = page.query_selector('h1')
                h1 = h1_el.inner_text() if h1_el else ""
                
                # Word Count (Rough approximation from text content)
                body_text = page.inner_text('body')
                word_count = len(body_text.split())
                
                results.append({
                    "url": url,
                    "status": status,
                    "title": title,
                    "description": description,
                    "h1": h1,
                    "word_count": word_count
                })
                
                # 3. Find Internal Links
                hrefs = page.eval_on_selector_all('a', 'elements => elements.map(e => e.href)')
                for href in hrefs:
                    # Basic filtering
                    if not href: continue
                    parsed = urlparse(href)
                    
                    # Internal only
                    if parsed.netloc == domain:
                        clean_href = normalize_url(href)
                        if clean_href not in visited and clean_href not in queue:
                            # Avoid static assets
                            if not any(ext in clean_href for ext in ['.jpg', '.png', '.css', '.js', '.pdf']):
                                queue.append(clean_href)
                                
            except Exception as e:
                print(f"Error crawling {url}: {e}")
                results.append({
                    "url": url,
                    "status": "ERROR",
                    "title": "",
                    "description": "",
                    "h1": "",
                    "word_count": 0
                })
        
        browser.close()

    # Save to CSV
    output_file = ".tmp/crawl_report.csv"
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["url", "status", "title", "description", "h1", "word_count"])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\nCrawl complete. Report saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    
    crawl_site(args.url, args.limit)
