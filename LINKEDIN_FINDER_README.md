# LinkedIn URL Finder

Two simple, elegant Python scripts for finding LinkedIn profile URLs.

## Scripts

### linkedin_finder_v2.py (Recommended)

Pattern-matching approach - fast and reliable.

**Strategy:**
1. Generates likely LinkedIn username patterns from the person's name
2. Validates each pattern with HTTP HEAD requests
3. Returns first valid URL or provides search fallback

**Pros:**
- Fast (no search scraping)
- Reliable (direct URL validation)
- Shows tried patterns for manual verification

**Usage:**
```bash
# Positional arguments
python linkedin_finder_v2.py "John Doe" "Acme Corp"

# Named arguments
python linkedin_finder_v2.py -n "Jane Smith" -e "Tech Inc"

# JSON output
python linkedin_finder_v2.py "Bob Jones" "StartupXYZ" --json
```

**As a module:**
```python
from linkedin_finder_v2 import find_linkedin_profile

result = find_linkedin_profile("John Doe", "Acme Corp")
if result["found"]:
    print(f"LinkedIn: {result['url']}")
else:
    print(f"Try patterns: {result['tried_patterns']}")
    print(f"Search: {result['search_url']}")
```

### linkedin_finder.py

Search-based approach using DuckDuckGo and Google.

**Strategy:**
1. Searches multiple search engines for LinkedIn profiles
2. Extracts LinkedIn URLs from search results
3. Returns matched URLs

**Pros:**
- Can find profiles even with non-standard usernames
- Returns multiple potential matches

**Cons:**
- Subject to search engine blocking/rate limiting
- Slower than pattern matching

**Usage:** Same as v2

## Requirements

```bash
pip install requests
```

## Which to Use?

- **Start with v2** - faster and more reliable for most cases
- **Try v1** if v2 doesn't find the profile (handles non-standard usernames)
- Both provide search URLs as fallback

## Example Output

```bash
$ python linkedin_finder_v2.py "Satya Nadella" "Microsoft"

🔍 Searching for: Satya Nadella at Microsoft
------------------------------------------------------------
❌ Not found via pattern matching

   Tried patterns: satyanadella, satya-nadella, satyan, snadella

   Manual search: https://www.google.com/search?q=Satya+Nadella+Microsoft+linkedin

   💡 Tip: Check the tried patterns - one might be correct with slight variation
------------------------------------------------------------
```

## Design Principles

- **KISS** - Simple, focused functionality
- **YAGNI** - No unnecessary features
- **Flexible** - Works as script or module
- **Clear** - Explicit outputs and error handling
- **Robust** - Multiple strategies and graceful fallbacks
