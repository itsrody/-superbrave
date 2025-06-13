from datetime import datetime
from pathlib import Path

def write_super_brave_file(rules: List[str], output_path: str, author: str = "Murtaza Salih") -> None:
    """Write valid rules to a file with a descriptive header."""
    version = datetime.utcnow().isoformat() + "Z"  # UTC timestamp
    header = (
        f"# SuperBrave AdBlock Filter List
"
        f"# Title: Valid AdBlock Rules for Brave Browser
"
        f"# Author: {author}
"
        f"# Version: {version}
"
        f"# Description: Rules validated for Brave's adblocker compatibility.
"
        f"# Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"
        f"

"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)
        for rule in rules:
            f.write(f"{rule}
")
