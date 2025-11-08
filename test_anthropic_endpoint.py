"""Test the Anthropic endpoint with the actual working token from environment."""

import os
from zai import ZaiClient

print("=" * 70)
print("Testing Anthropic Endpoint with Working Claude Code Token")
print("=" * 70)

# Try different token sources
auth_token = os.getenv('ANTHROPIC_AUTH_TOKEN') or os.getenv('BOND_AUTH_TOKEN')
base_url = os.getenv('ANTHROPIC_BASE_URL') or 'https://api.z.ai/api/anthropic'
model = os.getenv('ANTHROPIC_MODEL') or 'GLM-4.6'

print(f"Base URL: {base_url}")
print(f"Model: {model}")
print(f"Auth Token: {auth_token[:30] if auth_token else 'NOT FOUND'}...")
print()

if not auth_token:
    print("❌ No auth token found!")
    exit(1)

try:
    # Create client
    client = ZaiClient(
        api_key=auth_token,
        base_url=base_url
    )

    print("Calling API...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5
    )

    print("\n✅ SUCCESS! Response received:")
    if response.choices:
        print(f"Content: {response.choices[0].message.content}")
    else:
        print(f"Full response: {response}")

except Exception as e:
    error_msg = str(e)
    print(f"\n❌ FAILED: {error_msg}")

    # Parse the error
    if '1113' in error_msg or 'Insufficient balance' in error_msg:
        print("\n💡 This is a credit-based error.")
        print("   Code plan should not use credits - this might be expected for this endpoint.")
    elif '1211' in error_msg or 'Unknown Model' in error_msg:
        print("\n💡 Model not found. The model name might be different.")
    elif '404' in error_msg or 'NOT_FOUND' in error_msg:
        print("\n💡 Endpoint not found. The Anthropic endpoint might need different approach.")
    elif '2003' in error_msg or '2013' in error_msg:
        print("\n💡 Parameter error. The Anthropic endpoint might require anthropic package.")

print("\n" + "=" * 70)

# Also test if we should use the MiniMax endpoint
print("\n" + "=" * 70)
print("Testing with MiniMax Endpoint (from environment)")
print("=" * 70)

minimax_base = 'https://api.minimax.io/anthropic'
minimax_model = 'MiniMax-M2'

print(f"Base URL: {minimax_base}")
print(f"Model: {minimax_model}")

try:
    client = ZaiClient(
        api_key=auth_token,
        base_url=minimax_base
    )

    response = client.chat.completions.create(
        model=minimax_model,
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5
    )

    print("\n✅ SUCCESS with MiniMax!")
    if response.choices:
        print(f"Content: {response.choices[0].message.content}")

except Exception as e:
    print(f"\n❌ MiniMax also failed: {str(e)}")

print("\n" + "=" * 70)

