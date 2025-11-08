"""
Tools that the Bond agent can use.
Each tool is a simple Python function with a well-defined purpose.
"""

import subprocess
from typing import Any, Dict


def ping(host: str) -> str:
    """
    Ping some host on the internet.

    Args:
        host: hostname or IP address to ping

    Returns:
        Ping command output or error message
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "5", host],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def get_system_info() -> Dict[str, Any]:
    """
    Get basic system information.

    Returns:
        Dictionary with system details
    """
    import platform
    import sys

    return {
        "platform": platform.platform(),
        "python_version": sys.version,
        "architecture": platform.architecture(),
        "processor": platform.processor(),
    }


def echo(message: str) -> str:
    """
    Echo back a message.

    Args:
        message: The message to echo

    Returns:
        The same message
    """
    return f"Echo: {message}"


def calculate(operation: str, a: float, b: float) -> float:
    """
    Perform a basic calculation.

    Args:
        operation: Operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number

    Returns:
        Result of the calculation
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf'),
    }

    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")

    return operations[operation](a, b)
