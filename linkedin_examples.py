#!/usr/bin/env python3
"""
Examples of composing LinkedIn micro-tools.

Shows the flexibility and power of small, focused functions.
"""

from linkedin_tools import (
    build_google_search_url,
    extract_linkedin_urls,
    fetch_url,
    check_url_exists,
    generate_username_patterns,
    build_linkedin_url,
    search_google_for_linkedin,
    try_username_patterns,
    find_linkedin_profile,
)


# Example 1: Simple search - let the tool decide
def example_simple():
    print("\n=== Example 1: Simple Search ===")
    result = find_linkedin_profile("Satya Nadella", "Microsoft")
    print(f"Found: {result.get('found')}")
    if result.get("found"):
        print(f"URL: {result['url']}")
        print(f"Method: {result['method']}")


# Example 2: Just get patterns - no web requests
def example_patterns_only():
    print("\n=== Example 2: Generate Patterns ===")
    patterns = generate_username_patterns("John Doe")
    print(f"Patterns for 'John Doe': {patterns}")

    # Build URLs
    urls = [build_linkedin_url(p) for p in patterns]
    for url in urls:
        print(f"  → {url}")


# Example 3: Check if specific username exists
def example_check_username():
    print("\n=== Example 3: Check Specific Username ===")
    username = "williamhgates"  # Bill Gates
    url = build_linkedin_url(username)
    exists = check_url_exists(url)
    print(f"Username '{username}': {'✅ EXISTS' if exists else '❌ NOT FOUND'}")


# Example 4: Batch processing with custom logic
def example_batch_custom():
    print("\n=== Example 4: Batch with Custom Logic ===")

    candidates = [
        ("Satya Nadella", "Microsoft"),
        ("Sundar Pichai", "Google"),
        ("Tim Cook", "Apple"),
    ]

    for name, employer in candidates:
        # First try patterns (fast)
        pattern_result = try_username_patterns(name)

        if pattern_result:
            print(
                f"✅ {name:20} → {pattern_result['url']} (pattern: {pattern_result['username']})"
            )
        else:
            # Fall back to search
            print(f"⚠️  {name:20} → pattern failed, trying search...")
            search_url = build_google_search_url(name, employer)
            print(f"   Search: {search_url}")


# Example 5: Custom workflow - fetch and parse manually
def example_manual_workflow():
    print("\n=== Example 5: Manual Workflow ===")

    name = "Reid Hoffman"
    employer = "LinkedIn"

    # Step 1: Build search URL
    search_url = build_google_search_url(name, employer)
    print(f"1. Search URL: {search_url}")

    # Step 2: Fetch content
    print("2. Fetching search results...")
    html = fetch_url(search_url)

    if html:
        # Step 3: Extract URLs
        urls = extract_linkedin_urls(html)
        print(f"3. Found {len(urls)} LinkedIn URLs")

        # Step 4: Validate each
        for url in urls[:3]:  # Check first 3
            exists = check_url_exists(url)
            status = "✅" if exists else "❌"
            print(f"   {status} {url}")
    else:
        print("   ❌ Failed to fetch")


# Example 6: Build your own composite function
def find_linkedin_with_validation(name: str, employer: str) -> dict:
    """
    Custom composite: try patterns, validate results, then search.
    """
    # Try patterns
    patterns = generate_username_patterns(name)

    for pattern in patterns:
        url = build_linkedin_url(pattern)
        if check_url_exists(url):
            return {
                "found": True,
                "url": url,
                "pattern": pattern,
                "method": "validated_pattern",
            }

    # Search
    urls = search_google_for_linkedin(name, employer)

    # Validate search results
    for url in urls:
        if check_url_exists(url):
            return {"found": True, "url": url, "method": "validated_search"}

    return {"found": False, "search_url": build_google_search_url(name, employer)}


def example_custom_composite():
    print("\n=== Example 6: Custom Composite Function ===")
    result = find_linkedin_with_validation("Mark Zuckerberg", "Meta")
    print(f"Result: {result}")


if __name__ == "__main__":
    # Run all examples
    example_simple()
    example_patterns_only()
    example_check_username()
    example_batch_custom()
    example_manual_workflow()
    example_custom_composite()

    print("\n" + "=" * 60)
    print("These examples show micro-tools are composable!")
    print("Build your own workflows by combining primitives.")
    print("=" * 60)
