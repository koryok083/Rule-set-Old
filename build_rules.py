#!/usr/bin/env python3
import os
import requests
from pathlib import Path
from datetime import datetime

# Config
RULES_DIR = "rules"
SOURCES = {
    "bank": [
        "https://raw.githubusercontent.com/malikshi/v2ray-rules-dat/rule/rule_bank-id.txt",
        "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/banking.txt"
    ],
    "ads": [
        "https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.txt",
        "https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt"
    ],
    "social": [
        "https://raw.githubusercontent.com/malikshi/v2ray-rules-dat/rule/rule_sosmed.txt",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Telegram.list"
    ]
}

def clean_domain(domain):
    """Clean and validate domain"""
    domain = ''.join(c for c in domain if c.isalnum() or c in '.-')
    if domain.count('.') < 1:
        return None
    return domain.lower()

def fetch_domains(url):
    """Fetch domains from URL with error handling"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        domains = set()
        for line in response.text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Handle different formats
            if line.startswith('||'):
                domain = line[2:].split('^')[0]
            elif line.startswith('0.0.0.0'):
                domain = line.split()[1]
            else:
                domain = line.split()[0]
            
            if clean_domain(domain):
                domains.add(clean_domain(domain))
                
        return domains
    except Exception as e:
        print(f"⚠️ Error processing {url}: {str(e)}")
        return set()

def generate_rule(category, sources):
    """Generate YAML rule file"""
    domains = set()
    for url in sources:
        print(f"🔗 Fetching {category} from {url}")
        domains.update(fetch_domains(url))
    
    if not domains:
        print(f"❌ No domains found for {category}")
        return 0
    
    # Create rules directory
    Path(RULES_DIR).mkdir(exist_ok=True)
    
    # Generate YAML
    output_path = Path(RULES_DIR) / f"{category}.yaml"
    with open(output_path, 'w') as f:
        f.write(f"# {category.capitalize()} Rule-Set\n")
        f.write(f"# Sources: {len(sources)} trusted repositories\n")
        f.write(f"# Updated: {os.getenv('LAST_UPDATED')}\n")
        f.write(f"# Total Domains: {len(domains)}\n\n")
        f.write("payload:\n")
        for domain in sorted(domains):
            f.write(f"  - \"{domain}\"\n")
    
    print(f"✅ Generated {output_path} with {len(domains)} domains")
    return len(domains)

def main():
    print("🚀 Starting Rule-Sets Builder")
    stats = {}
    
    for category, urls in SOURCES.items():
        count = generate_rule(category, urls)
        stats[category] = count
    
    print("\n📊 Build Summary:")
    for category, count in stats.items():
        print(f"  - {category.capitalize()}: {count} domains")
    
    print(f"\n🎉 All rule-sets generated in '{RULES_DIR}' directory")

if __name__ == "__main__":
    main()
