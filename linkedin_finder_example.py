#!/usr/bin/env python3
"""
Example usage of linkedin_finder as a Python module.
"""

from linkedin_finder import search_linkedin_profile

# Example 1: Simple search
result = search_linkedin_profile("Satya Nadella", "Microsoft")
if result["found"]:
    print(f"Found: {result['url']}")
else:
    print("Not found")

# Example 2: Batch search
candidates = [
    ("Satya Nadella", "Microsoft"),
    ("Sundar Pichai", "Google"),
    ("Tim Cook", "Apple"),
]

for name, employer in candidates:
    result = search_linkedin_profile(name, employer)
    if result["found"]:
        print(f"{name:20} → {result['url']}")
    else:
        print(f"{name:20} → Not found")
