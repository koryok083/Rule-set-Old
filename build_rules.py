#!/usr/bin/env python3
import os
import requests
import yaml
from pathlib import Path
from datetime import datetime

CONFIG = {
    "output_dir": "rules",
    "sources": {
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
}

def clean_domain(domain: str) -> str:
    """Clean and validate domain format"""
    domain = ''.join(c for c in domain.lower() if c.isalnum() or c in '.-')
    parts = domain.split('.')
    return domain if len(parts) > 1 and len(parts[-1]) >= 2 else None

def fetch_domains(url: str) -> set:
    """Fetch and parse domains from URL"""
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        
        domains = set()
        for line in response.text.splitlines():
            line = line.strip()
            if not line or line.startswith(('#', '!', '/')): 
                continue
            
            # Handle multiple formats
            domain = (
                line.split()[1] if line.startswith('0.0.0.0') else
                line[2:].split('^')[0] if line.startswith('||') else
                line.split()[0]
            )
            
            if clean_domain(domain):
                domains.add(clean_domain(domain))
                
        return domains
    except Exception as e:
        print(f"⚠️ Error processing {url}: {str(e)}")
        return set()

def generate_rule(category: str, sources: list) -> int:
    """Generate YAML rule file for a category"""
    domains = set()
    for url in sources:
        print(f"🔗 Fetching {category} from {url}")
        domains.update(fetch_domains(url))
    
    if not domains:
        print(f"❌ No valid domains found for {category}")
        return 0
    
    # Prepare output
    Path(CONFIG['output_dir']).mkdir(exist_ok=True)
    output_path = Path(CONFIG['output_dir']) / f"{category}.yaml"
    
    # Generate YAML structure
    rule_data = {
        "metadata": {
            "category": category,
            "updated": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            "sources": sources,
            "domain_count": len(domains)
        },
        "rules": sorted(domains)
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(rule_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Generated {output_path} with {len(domains)} domains")
    return len(domains)

if __name__ == "__main__":
    print("🚀 Starting Rule-Sets Builder")
    total = 0
    
    for category, urls in CONFIG['sources'].items():
        total += generate_rule(category, urls)
    
    print(f"\n🎉 Success! Processed {total} domains across all categories")
