#!/usr/bin/env python3
"""
Demo: How an AI agent can use micro-tools flexibly.

This shows the power of composable tools - the agent can choose
the right strategy based on the situation.
"""

from linkedin_tools import (
    generate_username_patterns,
    build_linkedin_url,
    build_google_search_url,
    search_google_for_linkedin,
)


class LinkedInAgent:
    """
    AI agent that intelligently uses micro-tools to find LinkedIn profiles.

    The agent can:
    1. Try fast patterns first
    2. Fall back to search if needed
    3. Provide manual fallback
    4. Adapt strategy based on results
    """

    def find_profile(self, name: str, employer: str, strategy: str = "smart") -> dict:
        """
        Find LinkedIn profile using chosen strategy.

        Strategies:
        - 'fast': Only try patterns (no web search)
        - 'thorough': Only web search
        - 'smart': Try patterns first, then search (default)
        """

        print(f"\n🤖 Agent searching for: {name} at {employer}")
        print(f"   Strategy: {strategy}")

        # Strategy: Fast (patterns only)
        if strategy == "fast":
            return self._try_patterns_only(name)

        # Strategy: Thorough (search only)
        elif strategy == "thorough":
            return self._search_only(name, employer)

        # Strategy: Smart (adaptive)
        else:
            # Step 1: Quick pattern check
            print("   → Trying pattern matching (fast)...")
            patterns = generate_username_patterns(name)

            for i, pattern in enumerate(patterns):
                url = build_linkedin_url(pattern)
                # In real scenario, we'd check, but HEAD requests may be blocked
                # So we just show what the agent would do
                print(f"     • Would check: {url}")

                if i == 0:  # For demo, assume first pattern works
                    print(f"   ✅ Found via pattern: {url}")
                    return {
                        "found": True,
                        "method": "pattern",
                        "url": url,
                        "pattern": pattern,
                    }

            # Step 2: Fall back to search
            print("   → Patterns didn't work, trying search...")
            urls = search_google_for_linkedin(name, employer)

            if urls:
                print(f"   ✅ Found via search: {urls[0]}")
                return {
                    "found": True,
                    "method": "search",
                    "url": urls[0],
                    "all_urls": urls,
                }

            # Step 3: Provide manual fallback
            print("   ⚠️  No automatic match, providing manual search URL")
            search_url = build_google_search_url(name, employer)
            return {
                "found": False,
                "search_url": search_url,
                "tried_patterns": patterns,
                "suggestion": "Try manual search or verify name spelling",
            }

    def _try_patterns_only(self, name: str) -> dict:
        """Fast strategy - patterns only."""
        print("   → Pattern matching only (no web requests)...")
        patterns = generate_username_patterns(name)
        urls = [build_linkedin_url(p) for p in patterns]

        return {
            "found": None,  # Unknown without validation
            "method": "patterns_suggested",
            "patterns": patterns,
            "urls": urls,
            "note": "Validation skipped - check URLs manually",
        }

    def _search_only(self, name: str, employer: str) -> dict:
        """Thorough strategy - search only."""
        print("   → Web search only (thorough but slower)...")
        urls = search_google_for_linkedin(name, employer)

        if urls:
            return {"found": True, "method": "search", "url": urls[0], "all_urls": urls}
        else:
            return {
                "found": False,
                "search_url": build_google_search_url(name, employer),
            }

    def batch_search(self, candidates: list, strategy: str = "smart") -> list:
        """Process multiple candidates efficiently."""
        print(f"\n🤖 Agent processing {len(candidates)} candidates")
        results = []

        for name, employer in candidates:
            result = self.find_profile(name, employer, strategy)
            results.append({"name": name, "employer": employer, **result})

        return results


if __name__ == "__main__":
    # Demo the agent
    agent = LinkedInAgent()

    # Example 1: Single search
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Single Search")
    print("=" * 70)
    result = agent.find_profile("Reid Hoffman", "LinkedIn", strategy="smart")
    print(f"\nResult: {result}")

    # Example 2: Batch processing
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Batch Processing")
    print("=" * 70)
    candidates = [
        ("Satya Nadella", "Microsoft"),
        ("Sundar Pichai", "Google"),
        ("Tim Cook", "Apple"),
    ]
    results = agent.batch_search(candidates, strategy="fast")

    print("\n📊 Batch Results:")
    for r in results:
        status = "✅" if r.get("found") else "⚠️"
        print(
            f"{status} {r['name']:20} → {r.get('patterns', ['N/A'])[0] if 'patterns' in r else r.get('url', 'Not found')}"
        )

    print("\n" + "=" * 70)
    print("The agent adapts its strategy based on the situation!")
    print("Micro-tools = Maximum flexibility")
    print("=" * 70)
