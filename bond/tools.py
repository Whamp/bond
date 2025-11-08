"""
Tools that the Bond agent can use.
Each tool is a simple Python function with a well-defined purpose.
"""

from typing import Any, Dict


def ping() -> str:
    """
    Simple ping tool to test if the agent is working.

    Returns:
        A pong response to confirm the system is operational
    """
    return "pong"


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
