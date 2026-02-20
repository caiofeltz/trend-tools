import argparse
import json
import re

def validate_schema(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for JSON-LD
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    
    print(f"--- Schema Validation ---")
    if not scripts:
        print("[WARN] No JSON-LD Schema found.")
        return

    for i, script in enumerate(scripts):
        print(f"\nChecking Schema Block #{i+1}...")
        try:
            data = json.loads(script)
            print("[PASS] Valid JSON.")
            print(f"Type: {data.get('@type', 'Unknown')}")
            
            # Basic validation
            if '@context' not in data:
                print("[FAIL] Missing @context")
            elif data['@context'] != "https://schema.org":
                print(f"[WARN] Suspicious @context: {data['@context']}")
            else:
                print("[PASS] @context is schema.org")
                
        except json.JSONDecodeError as e:
            print(f"[FAIL] Invalid JSON: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    
    validate_schema(args.input)
