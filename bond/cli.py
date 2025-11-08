"""
Interactive CLI for Bond agent.
Provides a command-line interface similar to Claude Code.
"""

import sys
import signal
from bond.agent import BondAgent
from bond.tools import ping, get_system_info, echo, calculate


def setup_agent(agent: BondAgent):
    """Register available tools with the agent."""
    # Ping tool
    agent.add_tool(
        name="ping",
        description="Test if the agent is working. Returns 'pong'.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=ping
    )

    # System info tool
    agent.add_tool(
        name="get_system_info",
        description="Get basic system information including platform, Python version, etc.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=get_system_info
    )

    # Echo tool
    agent.add_tool(
        name="echo",
        description="Echo back a message",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo"
                }
            },
            "required": ["message"],
        },
        function=echo
    )

    # Calculate tool
    agent.add_tool(
        name="calculate",
        description="Perform a basic mathematical calculation",
        parameters={
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "Operation to perform (add, subtract, multiply, divide)"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"],
        },
        function=calculate
    )


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("Bond - LLM Agent with Tool Calling")
    print("=" * 60)
    print()
    print("Available tools: ping, get_system_info, echo, calculate")
    print("Type '/help' for commands, '/exit' to quit")
    print()
    print("-" * 60)
    print()


def print_help():
    """Print help information."""
    print()
    print("Commands:")
    print("  /help      - Show this help message")
    print("  /exit      - Exit the agent")
    print("  /reset     - Clear conversation context")
    print("  /context   - Show conversation history")
    print()
    print("Examples:")
    print("  > ping the system")
    print("  > what's my system info?")
    print("  > echo 'Hello Bond'")
    print("  > calculate 2 + 2")
    print("  > calculate 10 * 5")
    print()


def print_context(agent: BondAgent):
    """Print the current conversation context."""
    print()
    print("Conversation Context:")
    print("-" * 60)
    for i, message in enumerate(agent.get_context(), 1):
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        print(f"{i}. [{role}] {content}")
    print("-" * 60)
    print()


def run_cli():
    """Run the interactive CLI."""
    # Setup signal handler for clean exit
    def signal_handler(sig, frame):
        print("\nGoodbye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Initialize agent
    print("Initializing Bond agent...")
    agent = BondAgent()
    setup_agent(agent)

    # Print banner
    print_banner()

    # Main interaction loop
    try:
        while True:
            # Get user input
            try:
                user_input = input("> ").strip()
            except EOFError:
                print()
                break

            # Handle commands
            if user_input.lower() in ['/exit', '/quit']:
                print("Goodbye!")
                break
            elif user_input.lower() == '/help':
                print_help()
                continue
            elif user_input.lower() == '/reset':
                agent.reset_context()
                print("Context cleared.")
                continue
            elif user_input.lower() == '/context':
                print_context(agent)
                continue
            elif user_input == '':
                continue

            # Process with agent
            try:
                response = agent.process(user_input)
                print(response)
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    run_cli()
