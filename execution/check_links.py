import argparse
import re

def check_links(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all hrefs
    links = re.findall(r'href=[\'"](.*?)[\'"]', content)
    
    internal = [l for l in links if l.startswith('/') or l.startswith('#') or 'mysite.com' in l]
    external = [l for l in links if l.startswith('http') and l not in internal]
    
    print(f"--- Link Analysis ---")
    print(f"Total Links Found: {len(links)}")
    print(f"Internal: {len(internal)}")
    print(f"External: {len(external)}")
    
    # In a real script, we would ping them. 
    # For now, we just list them.
    if len(external) > 0:
        print("\nTop 5 External Links:")
        for l in external[:5]:
            print(f"- {l}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    
    check_links(args.input)
