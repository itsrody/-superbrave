import re
from datetime import datetime

UNSUPPORTED_PATTERNS = [
    # AdGuard-style generic cosmetic exceptions
    {"pattern": r"^#@#", "reason": "AdGuard-style `#@#` exception (Brave doesn't support)"},
    # Redirect rules with priority numbers (e.g., `$redirect=noop:3`)
    {"pattern": r"\$\redirect=[^:]+:\d+", "reason": "Redirect with priority number"},
    # Procedural JavaScript injections (Brave only supports limited `+js()`)
    {"pattern": r"##\+js$[^)]*(?=$)", "reason": "Procedural JS injection"},
    # Complex regex (lookaheads/behinds not supported)
    {"pattern": r"/$?\?=[^)]*$|$\?<=[^)]*$/", "reason": "Complex regex (lookaheads/behinds)"},
    # Nested domain scoping (e.g., `||sub.example.com^$domain=parent.com`)
    {"pattern": r"\|\|[^|]+\^\$domain=[^|]+", "reason": "Nested domain scoping"},
    # Unsafe CSP directives (Brave blocks these)
    {"pattern": r"\$csp=[^;]+('unsafe-inline'|'unsafe-eval')", "reason": "Unsafe CSP directive"},
]

def categorize_brave_rules(rules: List[str]) -> List[str]:
    """Return only rules compatible with Brave's adblocker."""
    valid_rules = []
    for rule in rules:
        unsupported_reasons = [
            pattern["reason"] 
            for pattern in UNSUPPORTED_PATTERNS 
            if re.search(pattern["pattern"], rule)
        ]
        if not unsupported_reasons:
            valid_rules.append(rule)
    return valid_rules
