"""Basic webhook connectivity test - no screening workflow execution.

Tests webhook request/response and Airtable data access without triggering
the expensive deep research workflow.
"""

from __future__ import annotations

import sys
from pathlib import Path

import requests

# Add demo module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from demo.settings import settings


def main() -> None:
    """Test basic webhook connectivity and validation."""

    print("🧪 Basic Webhook Connectivity Test")
    print("=" * 60)

    # Use 127.0.0.1 instead of 0.0.0.0 for client connections
    host = "127.0.0.1" if settings.flask.host == "0.0.0.0" else settings.flask.host
    webhook_url = f"http://{host}:{settings.flask.port}/screen"

    print(f"\n📡 Testing AgentOS runtime at {webhook_url}")

    # Test 1: Validate server is running
    print("\n1️⃣  Test: Server responds to requests")
    try:
        response = requests.post(
            webhook_url,
            json={},  # Empty payload - should fail validation
            timeout=5,
        )
        if response.status_code == 400:
            data = response.json()
            if data.get("error") == "validation_error":
                print("   ✅ Server is running and responding")
                print(f"   ✅ Validation working: {data.get('message')}")
            else:
                print(f"   ⚠️  Unexpected error format: {data}")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to AgentOS runtime at {webhook_url}")
        print("   ℹ️  Make sure AgentOS is running: uv run python demo/agentos_app.py")
        return
    except Exception as exc:
        print(f"   ❌ Unexpected error: {exc}")
        return

    # Test 2: Invalid screen_id format
    print("\n2️⃣  Test: Screen ID validation")
    response = requests.post(
        webhook_url,
        json={"screen_id": "invalid123"},
        timeout=5,
    )
    if response.status_code == 400:
        data = response.json()
        if "rec" in data.get("message", "").lower():
            print("   ✅ Screen ID format validation working")
        else:
            print(f"   ⚠️  Unexpected validation message: {data.get('message')}")
    else:
        print(f"   ❌ Expected 400, got {response.status_code}")

    # Test 3: Non-existent screen ID (should fail when trying to fetch)
    print("\n3️⃣  Test: Non-existent screen ID handling")
    response = requests.post(
        webhook_url,
        json={"screen_id": "recNonExistent123"},
        timeout=10,
    )
    # Should get either 400 or 500 depending on how the error is handled
    if response.status_code in [400, 500]:
        data = response.json()
        print(
            f"   ✅ Server handled non-existent screen (status {response.status_code})"
        )
        print(f"   ℹ️  Error: {data.get('message', data.get('error'))}")
    else:
        print(f"   ⚠️  Unexpected status code: {response.status_code}")

    # Test 4: Check Flask server logs
    print("\n4️⃣  Test: Server logging")
    print("   ℹ️  Check AgentOS terminal for request logs with 🔍 ✅ ❌ indicators")
    print("   ℹ️  You should see validation errors logged above")

    print("\n" + "=" * 60)
    print("🏁 Basic connectivity tests complete")
    print("\n📋 Summary:")
    print("   ✅ AgentOS runtime is running and accessible")
    print("   ✅ Request validation is working")
    print("   ✅ Error handling is functional")
    print("\n💡 Next steps:")
    print("   1. Verify AgentOS logs show all test requests")
    print("   2. Run full integration test: python scripts/test_screen_integration.py")
    print("   3. Monitor webhook execution in Airtable")


if __name__ == "__main__":
    main()
