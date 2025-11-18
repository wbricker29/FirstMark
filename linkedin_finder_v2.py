#!/usr/bin/env python3
"""
LinkedIn URL Finder V2 - Uses URL pattern matching + validation.

Strategy:
1. Generate likely LinkedIn URLs from name patterns
2. Validate URLs with HTTP HEAD requests
3. Return first valid URL or provide search fallback

Usage:
    python linkedin_finder_v2.py "John Doe" "Acme Corp"
"""

import sys
import argparse
import json
import re
import requests
from typing import List


def normalize_name_for_linkedin(name: str) -> List[str]:
    """
    Generate likely LinkedIn username patterns from a person's name.

    Returns list of candidates in order of likelihood.
    """
    # Clean and split name
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)  # Remove special chars except hyphen
    parts = name.split()

    if len(parts) < 2:
        return [name.replace(" ", "-")]

    first = parts[0]
    last = parts[-1]
    middle = parts[1:-1] if len(parts) > 2 else []

    # Common LinkedIn username patterns
    patterns = [
        f"{first}{last}",  # johndoe
        f"{first}-{last}",  # john-doe
        f"{first}{last[0]}",  # johnd
        f"{first[0]}{last}",  # jdoe
        f"{first}.{last}",  # john.doe (becomes john-dot-last)
        f"{first}-{middle[0] if middle else ''}-{last}".strip("-"),  # john-m-doe
    ]

    # Deduplicate while preserving order
    seen = set()
    unique_patterns = []
    for p in patterns:
        p_clean = p.replace(".", "-")  # LinkedIn converts dots to hyphens
        if p_clean and p_clean not in seen:
            seen.add(p_clean)
            unique_patterns.append(p_clean)

    return unique_patterns


def check_linkedin_url(username: str, timeout: int = 5) -> tuple[bool, str]:
    """
    Check if a LinkedIn profile URL exists.

    Returns (exists, full_url)
    """
    url = f"https://www.linkedin.com/in/{username}"

    try:
        # Use HEAD request for efficiency
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )

        # LinkedIn returns 200 for valid profiles, 404 for invalid
        if response.status_code == 200:
            return True, url
        else:
            return False, url

    except requests.RequestException:
        return False, url


def find_linkedin_profile(name: str, employer: str, timeout: int = 5) -> dict:
    """
    Find LinkedIn profile by trying common username patterns.

    Args:
        name: Full name of the person
        employer: Current or recent employer (used for context in search fallback)
        timeout: Request timeout in seconds

    Returns:
        dict with search results
    """
    # Generate candidate usernames
    candidates = normalize_name_for_linkedin(name)

    # Try each candidate
    for username in candidates:
        exists, url = check_linkedin_url(username, timeout)
        if exists:
            return {
                "found": True,
                "url": url,
                "username": username,
                "name": name,
                "employer": employer,
                "method": "pattern_match",
            }

    # No direct match found - provide search fallback
    from urllib.parse import quote_plus

    search_url = (
        f"https://www.google.com/search?q={quote_plus(f'{name} {employer} linkedin')}"
    )

    return {
        "found": False,
        "url": None,
        "name": name,
        "employer": employer,
        "tried_patterns": candidates,
        "search_url": search_url,
        "message": "No direct match found. Try manual search or check tried patterns.",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Find LinkedIn URLs using pattern matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_finder_v2.py "John Doe" "Acme Corp"
  python linkedin_finder_v2.py -n "Jane Smith" -e "Tech Inc" --json
        """,
    )

    parser.add_argument("name", nargs="?", help="Full name of the person")
    parser.add_argument("employer", nargs="?", help="Employer name")
    parser.add_argument(
        "-n", "--name", dest="name_flag", help="Full name (alternative syntax)"
    )
    parser.add_argument(
        "-e", "--employer", dest="employer_flag", help="Employer (alternative syntax)"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--timeout", type=int, default=5, help="Request timeout in seconds"
    )

    args = parser.parse_args()

    # Handle both positional and flag-based arguments
    name = args.name or args.name_flag
    employer = args.employer or args.employer_flag

    if not name or not employer:
        parser.print_help()
        sys.exit(1)

    # Search for LinkedIn profile
    result = find_linkedin_profile(name, employer, timeout=args.timeout)

    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n🔍 Searching for: {name} at {employer}")
        print("-" * 60)

        if result["found"]:
            print(f"✅ Found: {result['url']}")
            print(f"   Username: {result['username']}")
        else:
            print("❌ Not found via pattern matching")
            print(f"\n   Tried patterns: {', '.join(result['tried_patterns'])}")
            print(f"\n   Manual search: {result['search_url']}")
            print(
                "\n   💡 Tip: Check the tried patterns - one might be correct with slight variation"
            )

        print("-" * 60)


if __name__ == "__main__":
    main()
