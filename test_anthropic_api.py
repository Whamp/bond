"""Test if we should use anthropic package instead of zai-sdk for the Anthropic endpoint."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

print("=" * 70)
print("Testing API Access Methods")
print("=" * 70)

# Test 1: Using zai-sdk with Anthropic endpoint
print("\n--- Test 1: zai-sdk with Anthropic endpoint ---")
try:
    from zai import ZaiClient

    client = ZaiClient(
        api_key=os.getenv('BOND_AUTH_TOKEN'),
        base_url=os.getenv('BOND_BASE_URL')
    )

    response = client.chat.completions.create(
        model='GLM-4.6',
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5
    )

    if response.choices:
        print(f"✅ zai-sdk: SUCCESS")
        print(f"Response: {response.choices[0].message.content}")
    else:
        print(f"❌ zai-sdk: No choices in response")
        print(f"Full response: {response}")

except Exception as e:
    print(f"❌ zai-sdk: FAILED - {str(e)}")

# Test 2: Check if anthropic package is available
print("\n--- Test 2: Using anthropic package ---")
try:
    from anthropic import Anthropic

    # Try with Anthropic client
    client = Anthropic(
        api_key=os.getenv('BOND_AUTH_TOKEN'),
        base_url=os.getenv('BOND_BASE_URL')
    )

    # Note: This might not work as anthropic has its own API structure
    print("✅ anthropic package is available")
    print("   (But uses different API structure - not OpenAI compatible)")

except ImportError:
    print("ℹ️  anthropic package not installed")
except Exception as e:
    print(f"❌ anthropic package: FAILED - {str(e)}")

# Test 3: Check what environment variables zai-sdk actually uses
print("\n--- Test 3: Environment variable check ---")
print(f"BOND_AUTH_TOKEN: {os.getenv('BOND_AUTH_TOKEN', 'NOT SET')[:20]}...")
print(f"BOND_BASE_URL: {os.getenv('BOND_BASE_URL', 'NOT SET')}")
print(f"BOND_MODEL: {os.getenv('BOND_MODEL', 'NOT SET')}")

# Test if ANTHROPIC_* variables would work better
print(f"\nANTHROPIC_AUTH_TOKEN: {os.getenv('ANTHROPIC_AUTH_TOKEN', 'NOT SET')}")
print(f"ANTHROPIC_BASE_URL: {os.getenv('ANTHROPIC_BASE_URL', 'NOT SET')}")
print(f"ANTHROPIC_MODEL: {os.getenv('ANTHROPIC_MODEL', 'NOT SET')}")

print("\n" + "=" * 70)
print("Testing Complete")
print("=" * 70)
