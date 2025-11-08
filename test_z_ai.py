#!/usr/bin/env python3
"""Test script to verify z.ai Anthropic endpoint with tool calling"""

from bond.agent import BondAgent
from bond.tools import register_tools

def test_z_ai():
    """Test a simple interaction with the z.ai endpoint"""
    print("Initializing Bond agent...")
    agent = BondAgent()
    
    # Register tools
    register_tools(agent)
    
    print(f"Registered {len(agent.tools)} tools")
    print("Tool format sample:", list(agent.tools.values())[0] if agent.tools else "No tools")
    
    # Test a simple interaction
    print("\nSending message: 'hi'")
    try:
        response = agent.process("hi")
        print(f"✓ Success! Response: {response}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_z_ai()
    exit(0 if success else 1)
