#!/usr/bin/env python3
"""
Interactive LinkedIn search - Compose micro-tools flexibly.

This demonstrates the power of micro-tools: you control the workflow.
"""

import argparse
import json
from linkedin_tools import (
    build_google_search_url,
    search_google_for_linkedin,
    generate_username_patterns,
    check_url_exists,
    build_linkedin_url,
    find_linkedin_profile,
)


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn search with flexible workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflows:
  auto       - Automatic: try patterns, then search (default)
  patterns   - Only try username patterns
  search     - Only search Google
  url        - Build search URL only (no requests)
  check      - Check if specific username exists

Examples:
  # Automatic workflow
  python linkedin_search.py "John Doe" "Acme Corp"

  # Just show patterns to try
  python linkedin_search.py "John Doe" "Acme Corp" --workflow patterns

  # Just get search URL (no web requests)
  python linkedin_search.py "John Doe" "Acme Corp" --workflow url

  # Check specific username
  python linkedin_search.py --workflow check --username johndoe
        """,
    )

    parser.add_argument("name", nargs="?", help="Person's name")
    parser.add_argument("employer", nargs="?", help="Employer name")
    parser.add_argument(
        "--workflow",
        choices=["auto", "patterns", "search", "url", "check"],
        default="auto",
        help="Workflow to execute",
    )
    parser.add_argument(
        "--username", help="LinkedIn username to check (for 'check' workflow)"
    )
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    # Workflow: check username
    if args.workflow == "check":
        if not args.username:
            parser.error("--username required for 'check' workflow")

        url = build_linkedin_url(args.username)
        exists = check_url_exists(url)

        result = {"username": args.username, "url": url, "exists": exists}

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            status = "✅ EXISTS" if exists else "❌ NOT FOUND"
            print(f"{status}: {url}")

        return

    # Other workflows need name and employer
    if not args.name or not args.employer:
        parser.error("name and employer required for this workflow")

    # Workflow: url only
    if args.workflow == "url":
        url = build_google_search_url(args.name, args.employer)

        result = {"search_url": url, "name": args.name, "employer": args.employer}

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n🔗 Search URL:")
            print(url)

    # Workflow: patterns only
    elif args.workflow == "patterns":
        patterns = generate_username_patterns(args.name)

        result = {
            "name": args.name,
            "employer": args.employer,
            "patterns": patterns,
            "urls": [build_linkedin_url(p) for p in patterns],
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n🔍 Username patterns for: {args.name}")
            print("-" * 60)
            for pattern in patterns:
                url = build_linkedin_url(pattern)
                print(f"  • {pattern:20} → {url}")
            print("-" * 60)

    # Workflow: search only
    elif args.workflow == "search":
        urls = search_google_for_linkedin(args.name, args.employer)

        result = {
            "name": args.name,
            "employer": args.employer,
            "found": len(urls) > 0,
            "urls": urls,
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n🔍 Google search results for: {args.name} at {args.employer}")
            print("-" * 60)
            if urls:
                print("Found URLs:")
                for url in urls:
                    print(f"  • {url}")
            else:
                print("❌ No URLs found in search results")
            print("-" * 60)

    # Workflow: auto (default)
    else:
        result = find_linkedin_profile(args.name, args.employer)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n🔍 Searching for: {args.name} at {args.employer}")
            print("-" * 60)

            if result["found"]:
                print(f"✅ Found via {result['method']}: {result['url']}")
                if "all_urls" in result and len(result["all_urls"]) > 1:
                    print("\nOther matches:")
                    for url in result["all_urls"][1:]:
                        print(f"  • {url}")
            else:
                print("❌ Not found automatically")
                print(f"\nTried patterns: {', '.join(result['tried_patterns'])}")
                print(f"\nManual search: {result['search_url']}")

            print("-" * 60)


if __name__ == "__main__":
    main()
