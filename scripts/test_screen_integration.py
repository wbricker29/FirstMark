"""Integration test for /screen webhook with real Airtable data.

Creates a test Screen record, triggers the webhook, and verifies results.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import requests
from pyairtable import Api

# Add demo module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from demo.airtable_client import AirtableClient
from demo.settings import settings


def main() -> None:
    """Run integration test for /screen webhook."""

    print("🧪 Screen Webhook Integration Test")
    print("=" * 60)

    # Initialize Airtable client
    api_key = settings.airtable.api_key
    base_id = settings.airtable.base_id

    if not api_key or not base_id:
        print("❌ Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID")
        sys.exit(1)

    # Clean base ID (remove table suffix if present)
    clean_base_id = base_id.split("/")[0]

    client = AirtableClient(api_key, base_id)
    api = Api(api_key)

    # Step 1: Find existing data for test
    print("\n📋 Step 1: Finding existing test data...")

    # Find a search record with a role spec
    searches_table = api.table(clean_base_id, "Platform-Searches")
    searches = searches_table.all()

    search_id = None
    role_spec_id = None
    for search in searches:
        fields = search.get("fields", {})
        role_spec_links = fields.get("Role Spec", [])
        if role_spec_links:
            search_id = search["id"]
            role_spec_id = role_spec_links[0]
            search_name = fields.get("Name", search_id)
            print(f"   ✓ Found Search: {search_name} ({search_id})")
            print(f"   ✓ Linked Role Spec: {role_spec_id}")
            break

    if not search_id or not role_spec_id:
        print("   ❌ No Search record found with a linked Role Spec")
        sys.exit(1)

    # Verify role spec has markdown content
    role_spec = client.get_role_spec(role_spec_id)
    if not role_spec.get("structured_spec_markdown"):
        print(f"   ❌ Role Spec {role_spec_id} missing markdown content")
        sys.exit(1)

    role_title = role_spec.get("fields", {}).get("Role Title", "Unknown")
    print(f"   ✓ Role Spec verified: {role_title}")

    # Find candidate records
    people_table = api.table(clean_base_id, "People")
    people = people_table.all(max_records=5)

    if not people:
        print("   ❌ No candidate records found in People table")
        sys.exit(1)

    candidate_ids = [p["id"] for p in people[:2]]  # Take first 2 candidates
    candidate_names = [
        p.get("fields", {}).get("Full Name", p["id"]) for p in people[:2]
    ]
    print(f"   ✓ Found {len(candidate_ids)} candidates:")
    for name, cid in zip(candidate_names, candidate_ids):
        print(f"      - {name} ({cid})")

    # Step 2: Find or use existing Screen record
    print("\n📝 Step 2: Finding existing Screen record for testing...")

    screens_table = api.table(clean_base_id, "Platform-Screens")
    screens = screens_table.all(max_records=10)

    screen_id = None
    for screen in screens:
        fields = screen.get("fields", {})
        # Look for a screen that has candidates linked
        if fields.get("Candidates") and fields.get("Search"):
            screen_id = screen["id"]
            screen_status = fields.get("Status", "Unknown")
            print(f"   ✓ Found Screen: {screen_id}")
            print(f"   ✓ Current Status: {screen_status}")
            break

    if not screen_id:
        print("   ❌ No suitable Screen record found")
        print("   ℹ️  Please create a Screen record manually in Airtable with:")
        print("      - Status: Any value")
        print("      - Search: Linked to a search with role spec")
        print("      - Candidates: At least one candidate linked")
        sys.exit(1)

    # Step 3: Trigger webhook
    print("\n🔔 Step 3: Triggering /screen webhook...")

    # Use 127.0.0.1 instead of 0.0.0.0 for client connections
    host = "127.0.0.1" if settings.flask.host == "0.0.0.0" else settings.flask.host
    webhook_url = f"http://{host}:{settings.flask.port}/screen"
    print(f"   Webhook URL: {webhook_url}")
    print(f"   Payload: {{'screen_id': '{screen_id}'}}")

    try:
        response = requests.post(
            webhook_url,
            json={"screen_id": screen_id},
            timeout=300,  # 5 minute timeout for deep research
        )

        print(f"\n   Response Status: {response.status_code}")

        if response.status_code == 200:
            result_data = response.json()
            print(f"   ✓ Status: {result_data.get('status')}")
            print(f"   ✓ Candidates Total: {result_data.get('candidates_total')}")
            print(
                f"   ✓ Candidates Processed: {result_data.get('candidates_processed')}"
            )
            print(f"   ✓ Candidates Failed: {result_data.get('candidates_failed')}")
            print(f"   ✓ Execution Time: {result_data.get('execution_time_seconds')}s")

            if result_data.get("errors"):
                print("\n   ⚠️ Errors encountered:")
                for error in result_data["errors"]:
                    print(f"      - {error.get('candidate_id')}: {error.get('error')}")

            # Step 4: Verify Assessment records
            print("\n✅ Step 4: Verifying Assessment records created...")

            results = result_data.get("results", [])
            if not results:
                print("   ❌ No assessment results returned")
                return

            for i, result in enumerate(results, 1):
                assessment_id = result["assessment_id"]
                candidate_id = result["candidate_id"]

                print(f"\n   Assessment {i}:")
                print(f"   ✓ Assessment ID: {assessment_id}")
                print(f"   ✓ Candidate ID: {candidate_id}")
                print(f"   ✓ Overall Score: {result['overall_score']}")
                print(f"   ✓ Confidence: {result['confidence']}")
                print(f"   ✓ Summary: {result['summary'][:100]}...")

                # Fetch full assessment record from Airtable
                assessments_table = api.table(clean_base_id, "Platform-Assessments")
                assessment_record = assessments_table.get(assessment_id)

                # Validate fields
                fields = assessment_record.get("fields", {})

                print(f"\n   Validating Airtable fields for {assessment_id}:")

                # Required field checks
                checks: dict[str, Any] = {
                    "Screen Link": fields.get("Screen"),
                    "Candidate Link": fields.get("Candidate"),
                    "Status": fields.get("Status"),
                    "Overall Score": fields.get("Overall Score"),
                    "Overall Confidence": fields.get("Overall Confidence"),
                    "Topline Summary": fields.get("Topline Summary"),
                    "Assessment JSON": fields.get("Assessment JSON"),
                    "Assessment Model": fields.get("Assessment Model"),
                    "Assessment Timestamp": fields.get("Assessment Timestamp"),
                }

                all_valid = True
                for field_name, field_value in checks.items():
                    if field_value is None or field_value == "":
                        print(f"      ❌ {field_name}: Missing")
                        all_valid = False
                    elif field_name == "Screen Link":
                        if screen_id in field_value:
                            print(f"      ✓ {field_name}: {field_value}")
                        else:
                            print(f"      ❌ {field_name}: Wrong value {field_value}")
                            all_valid = False
                    elif field_name == "Candidate Link":
                        if candidate_id in field_value:
                            print(f"      ✓ {field_name}: {field_value}")
                        else:
                            print(f"      ❌ {field_name}: Wrong value {field_value}")
                            all_valid = False
                    elif field_name == "Assessment JSON":
                        try:
                            json_data = json.loads(field_value)
                            print(
                                f"      ✓ {field_name}: Valid JSON ({len(json_data)} keys)"
                            )
                        except json.JSONDecodeError:
                            print(f"      ❌ {field_name}: Invalid JSON")
                            all_valid = False
                    else:
                        value_preview = str(field_value)[:50]
                        if len(str(field_value)) > 50:
                            value_preview += "..."
                        print(f"      ✓ {field_name}: {value_preview}")

                if all_valid:
                    print(
                        f"\n   ✅ All fields validated for Assessment {assessment_id}"
                    )
                else:
                    print(
                        f"\n   ❌ Some fields missing or invalid for Assessment {assessment_id}"
                    )

        else:
            print(f"   ❌ Webhook failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"\n   ❌ Could not connect to AgentOS runtime at {webhook_url}")
        print("   ℹ️  Make sure the AgentOS server is running:")
        print("      uv run python demo/agentos_app.py")
    except requests.exceptions.Timeout:
        print("\n   ❌ Webhook request timed out (exceeded 5 minutes)")
    except Exception as exc:
        print(f"\n   ❌ Unexpected error: {exc}")

    print("\n" + "=" * 60)
    print("🏁 Integration test complete")
    print(f"   Screen ID: {screen_id}")
    print("   Check Airtable for full results")


if __name__ == "__main__":
    main()
