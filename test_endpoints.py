"""Test different API endpoints for code plan subscription."""

from zai import ZaiClient
from bond.config import load_config
import json

# Load config
config = load_config()

# Different endpoints to test
endpoints_to_test = [
    ('https://api.z.ai/api/paas/v4/', 'Standard PaaS v4'),
    ('https://api.z.ai/api/anthropic', 'Anthropic-compatible'),
    ('https://api.z.ai/api/v1/', 'API v1'),
    ('https://api.z.ai/api/', 'API Root'),
    ('https://open.bigmodel.cn/api/paas/v4/', 'Legacy BigModel'),
    ('https://open.bigmodel.cn/api/paas/v3/', 'Legacy BigModel v3'),
]

# Different models to test
models_to_test = [
    'glm-4-plus',
    'GLM-4-plus',
    'glm-4',
    'GLM-4',
    'glm-4.6',
    'GLM-4.6',
    'glm-4-8k',
    'GLM-4-8k',
    'glm-4-32k',
    'GLM-4-32k',
    'glm-4-flash',
    'GLM-4-flash',
]

print("=" * 70)
print("Testing API Endpoints with Code Plan Subscription")
print("=" * 70)
print(f"Auth Token: {config['auth_token'][:20]}...")
print()

# Test each endpoint
for base_url, description in endpoints_to_test:
    print(f"\n{'=' * 70}")
    print(f"Testing: {description}")
    print(f"Base URL: {base_url}")
    print(f"{'=' * 70}")

    try:
        client = ZaiClient(
            api_key=config['auth_token'],
            base_url=base_url
        )

        # Try a simple API call
        response = client.chat.completions.create(
            model=models_to_test[0],
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=5
        )

        print(f"✅ SUCCESS! Response received")
        if response.choices:
            print(f"Content: {response.choices[0].message.content}")
        else:
            print(f"Full response: {response}")
        break

    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED: {error_msg}")

        # Parse error to see if it's an auth issue or endpoint issue
        if '404' in error_msg or 'NOT_FOUND' in error_msg:
            print(f"   → Endpoint not found")
        elif '401' in error_msg or '403' in error_msg or 'Unauthorized' in error_msg:
            print(f"   → Authentication failed")
        elif 'Insufficient balance' in error_msg:
            print(f"   → Endpoint valid but insufficient balance (this is OK!)")
            break
        elif 'Unknown Model' in error_msg or '1211' in error_msg:
            print(f"   → Endpoint valid, wrong model. Trying other models...")
            # Try other models
            found_working_model = None
            for model in models_to_test[1:]:
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": "Say 'test'"}],
                        max_tokens=5
                    )
                    print(f"   ✅ Found working model: {model}")
                    if response.choices:
                        print(f"   Content: {response.choices[0].message.content}")
                        found_working_model = model
                    else:
                        print(f"   Full response: {response}")
                        found_working_model = model
                    break
                except Exception as model_error:
                    if '1211' not in str(model_error) and 'Unknown Model' not in str(model_error):
                        print(f"   Trying {model}: {model_error}")
            if found_working_model:
                print(f"\n🎉 SUCCESS! Working configuration:")
                print(f"   Base URL: {base_url}")
                print(f"   Model: {found_working_model}")
                break
        else:
            # Extract error code if present
            if 'code' in error_msg:
                try:
                    error_json = json.loads(error_msg)
                    if 'code' in error_json:
                        print(f"   → Error code: {error_json['code']}")
                        print(f"   → Error message: {error_json.get('message', 'N/A')}")
                except:
                    pass

print(f"\n{'=' * 70}")
print("Testing Complete")
print(f"{'=' * 70}")
