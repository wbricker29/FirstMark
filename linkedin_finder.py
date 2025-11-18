#!/usr/bin/env python3
"""
LinkedIn URL Finder - Simple script to find LinkedIn profiles by name and employer.

Usage:
    python linkedin_finder.py "John Doe" "Acme Corp"
    python linkedin_finder.py --name "John Doe" --employer "Acme Corp"
"""

import sys
import argparse
import json
import re
from urllib.parse import quote_plus
import requests


def extract_linkedin_urls(text: str) -> list[str]:
    """Extract LinkedIn profile URLs from HTML text."""
    # Pattern to match linkedin.com/in/ URLs
    pattern = r"https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+"
    urls = re.findall(pattern, text)

    # Deduplicate and clean
    seen = set()
    clean_urls = []
    for url in urls:
        # Remove trailing slashes and normalize
        clean_url = url.rstrip("/").split("?")[0].split("#")[0]
        if clean_url not in seen:
            seen.add(clean_url)
            clean_urls.append(clean_url)

    return clean_urls


def search_linkedin_profile(name: str, employer: str, timeout: int = 10) -> dict:
    """
    Search for a LinkedIn profile using name and employer.

    Args:
        name: Full name of the person
        employer: Current or recent employer
        timeout: Request timeout in seconds

    Returns:
        dict with 'url', 'name', 'employer', and 'found' keys
    """
    # Try multiple search strategies for robustness
    strategies = [
        # Strategy 1: DuckDuckGo Lite (text-only interface)
        {
            "url": f"https://lite.duckduckgo.com/lite/?q={quote_plus(f'{name} {employer} linkedin')}",
            "name": "DuckDuckGo Lite",
        },
        # Strategy 2: Direct Google search (may be blocked without API key, but worth trying)
        {
            "url": f"https://www.google.com/search?q={quote_plus(f'{name} {employer} site:linkedin.com/in')}",
            "name": "Google",
        },
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    all_found_urls = []

    for strategy in strategies:
        try:
            response = requests.get(strategy["url"], headers=headers, timeout=timeout)
            if response.status_code == 200:
                urls = extract_linkedin_urls(response.text)
                all_found_urls.extend(urls)

                if urls:
                    # Found results with this strategy
                    break
        except requests.RequestException:
            # Try next strategy
            continue

    # Deduplicate results
    unique_urls = []
    seen = set()
    for url in all_found_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    if unique_urls:
        return {
            "found": True,
            "url": unique_urls[0],
            "name": name,
            "employer": employer,
            "all_urls": unique_urls[:5],  # Include top 5 results
        }
    else:
        # Provide a manual search URL as fallback
        search_url = f"https://www.google.com/search?q={quote_plus(f'{name} {employer} linkedin')}"
        return {
            "found": False,
            "url": None,
            "name": name,
            "employer": employer,
            "search_url": search_url,
            "message": "No LinkedIn profile found automatically. Try manual search at the provided URL.",
        }


def main():
    parser = argparse.ArgumentParser(
        description="Find LinkedIn URLs by name and employer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_finder.py "John Doe" "Acme Corp"
  python linkedin_finder.py --name "Jane Smith" --employer "Tech Inc"
  python linkedin_finder.py -n "Bob Jones" -e "StartupXYZ" --json
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
        "--timeout", type=int, default=10, help="Request timeout in seconds"
    )

    args = parser.parse_args()

    # Handle both positional and flag-based arguments
    name = args.name or args.name_flag
    employer = args.employer or args.employer_flag

    if not name or not employer:
        parser.print_help()
        sys.exit(1)

    # Search for LinkedIn profile
    result = search_linkedin_profile(name, employer, timeout=args.timeout)

    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n🔍 Searching for: {name} at {employer}")
        print("-" * 60)

        if result["found"]:
            print(f"✅ Found: {result['url']}")
            if len(result.get("all_urls", [])) > 1:
                print("\nOther matches:")
                for url in result["all_urls"][1:]:
                    print(f"   • {url}")
        else:
            print("❌ Not found")
            if "error" in result:
                print(f"   Error: {result['error']}")
            elif "message" in result:
                print(f"   {result['message']}")
            if "search_url" in result:
                print(f"\n   Manual search: {result['search_url']}")

        print("-" * 60)


if __name__ == "__main__":
    main()
