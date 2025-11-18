# LinkedIn Profile Finder - Micro-Tools Approach

Composable, flexible Python utilities for finding LinkedIn profile URLs.

## Philosophy

**Micro-tools over monoliths.** Small, focused functions that do ONE thing well. Compose them as needed for maximum flexibility.

You're the captain - choose your workflow.

## Core Tools (`linkedin_tools.py`)

### Primitives

```python
from linkedin_tools import *

# Generate likely username patterns
patterns = generate_username_patterns("John Doe")
# → ['johndoe', 'john-doe', 'johnd', 'jdoe']

# Build LinkedIn URL
url = build_linkedin_url("johndoe")
# → 'https://www.linkedin.com/in/johndoe'

# Check if URL exists (HEAD request)
exists = check_url_exists(url)
# → True/False

# Build Google search URL
search_url = build_google_search_url("John Doe", "Acme Corp")
# → Google search URL

# Fetch URL content
html = fetch_url(url)
# → HTML string or None

# Extract LinkedIn URLs from HTML
urls = extract_linkedin_urls(html)
# → List of LinkedIn profile URLs
```

### Composite Workflows

```python
# Try username patterns and return first valid one
result = try_username_patterns("John Doe")
# → {'username': 'johndoe', 'url': '...'} or None

# Search Google and extract LinkedIn URLs
urls = search_google_for_linkedin("John Doe", "Acme Corp")
# → List of URLs found

# Complete workflow: patterns → search → fallback
result = find_linkedin_profile("John Doe", "Acme Corp")
# → Full result dict
```

## CLI Tools

### `linkedin_search.py` - Interactive workflows

```bash
# Automatic workflow (try patterns, then search)
python linkedin_search.py "John Doe" "Acme Corp"

# Just show patterns to try (no web requests)
python linkedin_search.py "John Doe" "Acme Corp" --workflow patterns

# Just get search URL (no requests)
python linkedin_search.py "John Doe" "Acme Corp" --workflow url

# Only search Google
python linkedin_search.py "John Doe" "Acme Corp" --workflow search

# Check if specific username exists
python linkedin_search.py --workflow check --username johndoe

# JSON output
python linkedin_search.py "John Doe" "Acme Corp" --json
```

### Legacy Scripts

- `linkedin_finder.py` - Search-based approach
- `linkedin_finder_v2.py` - Pattern-matching approach

Both are superseded by the micro-tools approach but kept for reference.

## Examples (`linkedin_examples.py`)

Run `python linkedin_examples.py` to see 6 examples of composing micro-tools:

1. **Simple search** - Let the tool decide the workflow
2. **Patterns only** - Generate patterns without web requests
3. **Check username** - Validate a specific username
4. **Batch processing** - Custom logic for multiple candidates
5. **Manual workflow** - Step-by-step control
6. **Custom composite** - Build your own workflow function

## Usage Examples

### As CLI

```bash
# Quick search
python linkedin_search.py "Satya Nadella" "Microsoft"

# See what patterns would be tried
python linkedin_search.py "Satya Nadella" "Microsoft" --workflow patterns

# Get search URL to open in browser
python linkedin_search.py "Satya Nadella" "Microsoft" --workflow url
```

### As Python Module

```python
from linkedin_tools import find_linkedin_profile

# Simple
result = find_linkedin_profile("John Doe", "Acme Corp")
if result['found']:
    print(f"LinkedIn: {result['url']}")

# Custom workflow
from linkedin_tools import (
    generate_username_patterns,
    build_linkedin_url,
    check_url_exists
)

patterns = generate_username_patterns("John Doe")
for pattern in patterns:
    url = build_linkedin_url(pattern)
    if check_url_exists(url):
        print(f"Found: {url}")
        break
```

### Batch Processing

```python
from linkedin_tools import find_linkedin_profile

candidates = [
    ("Satya Nadella", "Microsoft"),
    ("Sundar Pichai", "Google"),
    ("Tim Cook", "Apple"),
]

for name, employer in candidates:
    result = find_linkedin_profile(name, employer)
    if result['found']:
        print(f"{name}: {result['url']}")
    else:
        print(f"{name}: Manual search → {result['search_url']}")
```

## Design Principles

- **KISS** - Keep it simple
- **YAGNI** - You ain't gonna need it
- **Composability** - Small tools that combine
- **Flexibility** - Build your own workflows
- **Clear outputs** - Explicit results, no magic

## Requirements

```bash
pip install requests
```

## How It Works

1. **Pattern matching** - Generates likely LinkedIn usernames from name
2. **Validation** - Uses HTTP HEAD to check if URLs exist
3. **Search fallback** - Google search if patterns fail
4. **URL extraction** - Regex to find LinkedIn profiles in HTML
5. **Graceful degradation** - Always provides manual search URL

## Why Micro-Tools?

Instead of one tool that tries to do everything:
- **Compose** - Build workflows from primitives
- **Control** - Choose exactly what you need
- **Extend** - Add new tools easily
- **Debug** - Test each piece independently
- **Flexible** - Different use cases, different compositions

You control the workflow. The tools provide the building blocks.
