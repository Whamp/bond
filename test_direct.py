"""Direct test using values from .env file."""

from zai import ZaiClient
from bond.config import load_config

# Load config from .env
config = load_config()

print("=" * 70)
print("Direct Test Using .env Values")
print("=" * 70)
print(f"Base URL: {config['base_url']}")
print(f"Model: {config['model']}")
print(f"Auth Token: {config['auth_token'][:30] if config['auth_token'] else 'NOT FOUND'}...")
print()

try:
    client = ZaiClient(
        api_key=config['auth_token'],
        base_url=config['base_url']
    )

    response = client.chat.completions.create(
        model=config['model'],
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5
    )

    if response.choices:
        print("✅ SUCCESS!")
        print(f"Response: {response.choices[0].message.content}")
    else:
        print("❌ No choices in response")
        print(f"Response: {response}")

except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

print("=" * 70)
