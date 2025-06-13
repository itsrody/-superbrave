import asyncio
from pathlib import Path
from typing import List

from super_brave.config import load_config
from fetcher import fetch_all_rules
from analyzer import categorize_brave_rules
from utils import write_super_brave_file

def main() -> None:
    # Load configuration
    config = load_config()
    rule_urls = config["rule_urls"]
    output_file = config["output_file"]
    concurrency = config.get("concurrency", 5)

    # Fetch rules from all URLs
    print(f"🔍 Fetching rules from {len(rule_urls)} URLs...")
    all_rules = asyncio.run(fetch_all_rules(rule_urls, concurrency))
    print(f"✅ Fetched {len(all_rules)} raw rules (after deduplication).")

    # Validate rules for Brave compatibility
    print("🔎 Validating rules for Brave...")
    valid_rules = categorize_brave_rules(all_rules)
    print(f"✅ {len(valid_rules)} valid rules remaining.")

    # Write to SuperBrave.txt
    output_path = Path(output_file)
    write_super_brave_file(valid_rules, str(output_path))
    print(f"🎉 Output saved to {output_path.absolute()}")

if __name__ == "__main__":
    main()
