#!/usr/bin/env python3
"""
LinkedIn micro-tools - Composable utilities for LinkedIn profile discovery.

Each function does ONE thing well. Combine as needed.
"""

import re
import requests
from urllib.parse import quote_plus
from typing import List, Dict, Optional


def build_google_search_url(name: str, employer: str) -> str:
    """
    Build a Google search URL for finding LinkedIn profiles.

    Returns: Search URL string
    """
    query = f"{name} {employer} site:linkedin.com/in"
    return f"https://www.google.com/search?q={quote_plus(query)}"


def extract_linkedin_urls(html: str) -> List[str]:
    """
    Extract LinkedIn profile URLs from HTML text.

    Returns: List of unique LinkedIn URLs found
    """
    pattern = r"https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+"
    urls = re.findall(pattern, html)

    # Deduplicate and normalize
    seen = set()
    clean = []
    for url in urls:
        normalized = url.rstrip("/").split("?")[0].split("#")[0]
        if normalized not in seen:
            seen.add(normalized)
            clean.append(normalized)

    return clean


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """
    Fetch URL content with proper headers.

    Returns: HTML content or None if failed
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def check_url_exists(url: str, timeout: int = 5) -> bool:
    """
    Check if a URL exists using HEAD request.

    Returns: True if URL is accessible
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.head(
            url, headers=headers, timeout=timeout, allow_redirects=True
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def generate_username_patterns(name: str) -> List[str]:
    """
    Generate likely LinkedIn username patterns from a name.

    Returns: List of username patterns in order of likelihood
    """
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    parts = name.split()

    if len(parts) < 2:
        return [name.replace(" ", "-")]

    first = parts[0]
    last = parts[-1]
    middle = parts[1:-1] if len(parts) > 2 else []

    patterns = [
        f"{first}{last}",
        f"{first}-{last}",
        f"{first}{last[0]}",
        f"{first[0]}{last}",
        f"{first}.{last}".replace(".", "-"),
    ]

    if middle:
        patterns.append(f"{first}-{middle[0]}-{last}")

    # Deduplicate
    seen = set()
    unique = []
    for p in patterns:
        if p and p not in seen:
            seen.add(p)
            unique.append(p)

    return unique


def build_linkedin_url(username: str) -> str:
    """
    Build a LinkedIn profile URL from username.

    Returns: Full LinkedIn URL
    """
    return f"https://www.linkedin.com/in/{username}"


# --- Composite workflows ---


def search_google_for_linkedin(
    name: str, employer: str, timeout: int = 10
) -> List[str]:
    """
    Search Google and extract LinkedIn URLs.

    Returns: List of LinkedIn URLs found in search results
    """
    search_url = build_google_search_url(name, employer)
    html = fetch_url(search_url, timeout)

    if html:
        return extract_linkedin_urls(html)
    return []


def try_username_patterns(name: str, timeout: int = 5) -> Optional[Dict[str, str]]:
    """
    Try common username patterns and return first valid one.

    Returns: Dict with 'username' and 'url' if found, None otherwise
    """
    patterns = generate_username_patterns(name)

    for username in patterns:
        url = build_linkedin_url(username)
        if check_url_exists(url, timeout):
            return {"username": username, "url": url}

    return None


def find_linkedin_profile(name: str, employer: str) -> Dict:
    """
    Complete workflow: try patterns first, then search.

    Returns: Dict with results and metadata
    """
    # Strategy 1: Try direct patterns (fast)
    pattern_result = try_username_patterns(name)
    if pattern_result:
        return {
            "found": True,
            "method": "pattern",
            **pattern_result,
            "name": name,
            "employer": employer,
        }

    # Strategy 2: Search Google (slower, but more comprehensive)
    urls = search_google_for_linkedin(name, employer)
    if urls:
        return {
            "found": True,
            "method": "search",
            "url": urls[0],
            "all_urls": urls,
            "name": name,
            "employer": employer,
        }

    # Fallback: provide search URL
    return {
        "found": False,
        "search_url": build_google_search_url(name, employer),
        "tried_patterns": generate_username_patterns(name),
        "name": name,
        "employer": employer,
    }


if __name__ == "__main__":
    # Demo usage
    import sys

    if len(sys.argv) < 3:
        print("Usage: python linkedin_tools.py <name> <employer>")
        print("\nAvailable functions:")
        print("  build_google_search_url(name, employer)")
        print("  extract_linkedin_urls(html)")
        print("  fetch_url(url)")
        print("  check_url_exists(url)")
        print("  generate_username_patterns(name)")
        print("  search_google_for_linkedin(name, employer)")
        print("  try_username_patterns(name)")
        print("  find_linkedin_profile(name, employer)")
        sys.exit(1)

    name = sys.argv[1]
    employer = sys.argv[2]

    result = find_linkedin_profile(name, employer)

    import json

    print(json.dumps(result, indent=2))
