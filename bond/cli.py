"""
Interactive CLI for Bond agent.
Provides a command-line interface similar to Claude Code.
"""

import sys
import signal
from bond.agent import BondAgent
from bond import tools


def setup_agent(agent: BondAgent):
    """Register available tools with the agent."""
    
    # Basic utility tools
    agent.add_tool(
        name="ping",
        description="Ping some host on the internet to test connectivity",
        parameters={
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "hostname or IP address to ping"
                }
            },
            "required": ["host"],
        },
        function=tools.ping
    )

    agent.add_tool(
        name="get_system_info",
        description="Get basic system information including platform, Python version, etc.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.get_system_info
    )

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
        function=tools.echo
    )

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
        function=tools.calculate
    )

    # File system tools
    agent.add_tool(
        name="ls",
        description="List directory contents with details",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path to list (default: current directory)"
                }
            },
            "required": [],
        },
        function=tools.ls
    )

    agent.add_tool(
        name="pwd",
        description="Print current working directory path",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.pwd
    )

    agent.add_tool(
        name="cat",
        description="Display the contents of a file",
        parameters={
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file to display"
                }
            },
            "required": ["filepath"],
        },
        function=tools.cat
    )

    agent.add_tool(
        name="grep",
        description="Search for a pattern in a file",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Pattern to search for"
                },
                "filepath": {
                    "type": "string",
                    "description": "File to search in"
                }
            },
            "required": ["pattern", "filepath"],
        },
        function=tools.grep
    )

    agent.add_tool(
        name="find",
        description="Find files matching a pattern in a directory",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to search in"
                },
                "name_pattern": {
                    "type": "string",
                    "description": "Filename pattern to match (e.g., '*.py')"
                }
            },
            "required": ["path"],
        },
        function=tools.find
    )

    agent.add_tool(
        name="head",
        description="Display first N lines of a file",
        parameters={
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file"
                },
                "lines": {
                    "type": "integer",
                    "description": "Number of lines to show (default: 10)"
                }
            },
            "required": ["filepath"],
        },
        function=tools.head
    )

    agent.add_tool(
        name="tail",
        description="Display last N lines of a file",
        parameters={
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file"
                },
                "lines": {
                    "type": "integer",
                    "description": "Number of lines to show (default: 10)"
                }
            },
            "required": ["filepath"],
        },
        function=tools.tail
    )

    agent.add_tool(
        name="wc",
        description="Count lines, words, and characters in a file",
        parameters={
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file"
                }
            },
            "required": ["filepath"],
        },
        function=tools.wc
    )

    # System information tools
    agent.add_tool(
        name="whoami",
        description="Display current user name",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.whoami
    )

    agent.add_tool(
        name="uname",
        description="Display system information (OS, kernel, etc.)",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.uname
    )

    agent.add_tool(
        name="df",
        description="Display disk space usage for all filesystems",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.df
    )

    agent.add_tool(
        name="ps",
        description="Display currently running processes",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.ps
    )

    agent.add_tool(
        name="env",
        description="Display environment variables",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.env
    )

    agent.add_tool(
        name="which",
        description="Locate a command in the system PATH",
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Command name to locate"
                }
            },
            "required": ["command"],
        },
        function=tools.which
    )

    # Network tools
    agent.add_tool(
        name="curl",
        description="Fetch content from a URL",
        parameters={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch"
                },
                "options": {
                    "type": "string",
                    "description": "Additional curl options (e.g., '-I' for headers)"
                }
            },
            "required": ["url"],
        },
        function=tools.curl
    )

    # GitHub CLI tool
    agent.add_tool(
        name="gh",
        description="Execute GitHub CLI commands to interact with repositories, issues, PRs, releases, etc. Common commands: 'repo view', 'issue list', 'pr list', 'pr status', 'release list', 'status'",
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "GitHub CLI command (without 'gh' prefix). Examples: 'repo view', 'issue list', 'pr list', 'pr status', 'release list', 'status', 'browse'"
                }
            },
            "required": ["command"],
        },
        function=tools.gh
    )

    # Web search tool (Terminal Bench enhancement)
    agent.add_tool(
        name="web_search",
        description="Search the web using Google with AI Overview extraction. Essential for finding commands, frameworks, and solutions. Based on Apex2's breakthrough technique.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find solutions, commands, or documentation"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of top results to analyze (default: 3)"
                }
            },
            "required": ["query"],
        },
        function=tools.web_search
    )

    # Advanced execution tools
    agent.add_tool(
        name="tree",
        description="Display directory tree structure. Useful for visualizing project layout.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path to display (default: current directory)"
                },
                "level": {
                    "type": "integer",
                    "description": "Maximum depth to descend (e.g., 2 for 2 levels)"
                },
                "options": {
                    "type": "string",
                    "description": "Additional options: -a (all files), -d (dirs only), --gitignore (respect .gitignore), -I 'pattern' (ignore pattern)"
                }
            },
            "required": [],
        },
        function=tools.tree
    )

    agent.add_tool(
        name="bash",
        description="Execute arbitrary bash command. Use with caution.",
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Bash command to execute"
                }
            },
            "required": ["command"],
        },
        function=tools.bash
    )


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("Bond - LLM Agent with Tool Calling")
    print("=" * 60)
    print()
    print("Available tool categories:")
    print("  • Basic: ping, echo, calculate, get_system_info")
    print("  • Files: ls, pwd, cat, grep, find, head, tail, wc, tree")
    print("  • System: whoami, uname, df, ps, env, which")
    print("  • Network: curl")
    print("  • Web: web_search (Google with AI Overview) 🤖")
    print("  • GitHub: gh (repos, issues, PRs, releases)")
    print("  • Advanced: bash (execute arbitrary commands)")
    print()
    print("Type '/help' for commands, '/exit' to quit")
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
    print("  > ping 8.8.8.8")
    print("  > ping google.com")
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

            # Process with agent (using enhanced intelligence)
            try:
                response = agent.process_with_intelligence(user_input)
                print(response)
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    run_cli()
