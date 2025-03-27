#!/usr/bin/env python3
import os
import requests
import yaml
from pathlib import Path
from datetime import datetime

# Configuration
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
    parts = domain.split('.')
    if len(parts) < 2:
        return None
    return domain.lower()

def fetch_domains(url):
    """Fetch and process domains from URL"""
    try:
        response = requests.get(url, timeout=15)
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
            
            cleaned = clean_domain(domain)
            if cleaned:
                domains.add(cleaned)
                
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
    
    # Prepare directory
    Path(RULES_DIR).mkdir(exist_ok=True)
    
    # Generate YAML
    rule_data = {
        "metadata": {
            "category": category,
            "sources": sources,
            "updated": os.getenv("LAST_UPDATED"),
            "domain_count": len(domains)
        },
        "payload": sorted(domains)
    }
    
    output_path = Path(RULES_DIR) / f"{category}.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(rule_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Generated {output_path} with {len(domains)} domains")
    return len(domains)

if __name__ == "__main__":
    print("🚀 Starting Rule-Sets Builder")
    total_domains = 0
    
    for category, urls in SOURCES.items():
        count = generate_rule(category, urls)
        total_domains += count
    
    print(f"\n🎉 Total {total_domains} domains processed")
    print(f"📁 Output directory: {RULES_DIR}")
