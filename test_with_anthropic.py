"""Test using the anthropic package instead of zai-sdk."""

from anthropic import Anthropic
from bond.config import load_config

# Load config from .env
config = load_config()

print("=" * 70)
print("Testing with Anthropic Python Package")
print("=" * 70)
print(f"Base URL: {config['base_url']}")
print(f"Model: {config['model']}")
print(f"Auth Token: {config['auth_token'][:30] if config['auth_token'] else 'NOT FOUND'}...")
print()

try:
    # Create Anthropic client
    # Note: Anthropic client doesn't support custom base_url in the same way
    # We'll need to test if it works

    client = Anthropic(
        api_key=config['auth_token'],
        base_url=config['base_url']
    )

    print("Calling API with anthropic package...")
    response = client.messages.create(
        model=config['model'],
        max_tokens=5,
        messages=[{"role": "user", "content": "Say 'test'"}]
    )

    print("✅ SUCCESS!")
    print(f"Response: {response.content[0].text}")

except TypeError as e:
    if "base_url" in str(e):
        print("❌ Anthropic client doesn't support custom base_url parameter")
        print("This is expected - the anthropic package is for Anthropic's API only")
    else:
        raise
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Note: The anthropic package is designed for Anthropic's API,")
print("not for z.ai's Anthropic-compatible endpoint.")
print("=" * 70)
