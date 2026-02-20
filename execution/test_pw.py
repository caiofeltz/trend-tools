from playwright.sync_api import sync_playwright
import sys

print("Starting test...", flush=True)
try:
    with sync_playwright() as p:
        print("Playwright started.", flush=True)
        browser = p.chromium.launch(headless=True)
        print("Browser launched.", flush=True)
        page = browser.new_page()
        print("Page created.", flush=True)
        page.goto("https://google.com")
        print("Navigated.", flush=True)
        print(page.title())
        browser.close()
        print("Done.", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
