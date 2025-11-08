"""
Configuration loader for Bond agent.
Loads environment variables from settings.json file and provides configuration access.
"""

import json
import os
from pathlib import Path


def load_config() -> dict:
    """Load configuration from settings.json file."""
    # Load settings.json file from the project root
    settings_path = Path(__file__).parent.parent / 'settings.json'

    try:
        with open(settings_path, 'r') as f:
            settings_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"settings.json not found at {settings_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in settings.json: {e}")

    env_vars = settings_data.get('env', {})

    config = {
        'auth_token': env_vars.get('ANTHROPIC_AUTH_TOKEN'),
        'base_url': env_vars.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic'),
        'model': env_vars.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
        'timeout_ms': int(env_vars.get('API_TIMEOUT_MS', 3000000)),
        'always_thinking': env_vars.get('alwaysThinkingEnabled', 'true').lower() == 'true',
    }

    # Validate required config
    if not config['auth_token']:
        raise ValueError("ANTHROPIC_AUTH_TOKEN is required in settings.json")

    return config
