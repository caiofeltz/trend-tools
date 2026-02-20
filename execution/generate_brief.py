import argparse
import sys
import re

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text).strip('-')

def generate_brief(topic, keywords, audience):
    brief_template = f"""# Content Brief: {topic}

## Strategy
- **Target Audience**: {audience}
- **Primary Intent**: (Informational/Commercial/Transactional)
- **Target Keywords**: {keywords}

## Suggested Structure

### H1: {topic} (Draft Title)

### H2: Introduction
- Hook the reader.
- Define the problem/solution.

### H2: Core Concept 1
- Detailed explanation.
- Use {keywords.split(',')[0] if keywords else 'primary keyword'} here.

### H2: Core Concept 2
- Expand on the topic.

### H2: FAQ
- What are common questions regarding {topic}?

### H2: Conclusion
- Summary and Call to Action.

## SEO Requirements
- **Word Count Goal**: 1500+ words
- **Entities to Include**: (Related terms to {topic})
- **Internal Links**: (Link to related product/service pages)
"""
    return brief_template

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a content brief.')
    parser.add_argument('--topic', required=True, help='Main topic')
    parser.add_argument('--keywords', default='', help='Comma-separated keywords')
    parser.add_argument('--audience', default='General Audience', help='Target audience')

    args = parser.parse_args()

    brief_content = generate_brief(args.topic, args.keywords, args.audience)
    
    filename = f".tmp/brief_{slugify(args.topic)}.md"
    
    # Ensure .tmp exists (simple check, though usually handled by directives)
    import os
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(brief_content)
    
    print(f"Brief generated: {filename}")
