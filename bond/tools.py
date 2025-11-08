"""
Tools that the Bond agent can use.
Each tool is a simple Python function with a well-defined purpose.

Following the Fly.io pattern:
- Simple functions with clear signatures
- Robust error handling with try/except
- String returns for simplicity
- Proper subprocess usage with text=True and stderr capture
"""

import subprocess
import os
import json
import re
from typing import Any, Dict, Optional
from urllib.parse import quote_plus
from datetime import datetime


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


# ============================================================
# Bash/System Tools
# ============================================================

def ls(path: str = ".") -> str:
    """
    List directory contents.

    Args:
        path: Directory path to list (defaults to current directory)

    Returns:
        Directory listing or error message
    """
    try:
        result = subprocess.run(
            ["ls", "-lah", path],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def pwd() -> str:
    """
    Print working directory.

    Returns:
        Current working directory path or error message
    """
    try:
        result = subprocess.run(
            ["pwd"],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"error: {e}"


def cat(filepath: str) -> str:
    """
    Display file contents.

    Args:
        filepath: Path to the file to display

    Returns:
        File contents or error message
    """
    try:
        result = subprocess.run(
            ["cat", filepath],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def grep(pattern: str, filepath: str) -> str:
    """
    Search for pattern in file.

    Args:
        pattern: Pattern to search for
        filepath: File to search in

    Returns:
        Matching lines or error message
    """
    try:
        result = subprocess.run(
            ["grep", "-n", pattern, filepath],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout if result.stdout else "No matches found"
    except Exception as e:
        return f"error: {e}"


def find(path: str, name_pattern: str = "*") -> str:
    """
    Find files matching a pattern.

    Args:
        path: Directory to search in
        name_pattern: Filename pattern to match (defaults to all files)

    Returns:
        List of matching files or error message
    """
    try:
        result = subprocess.run(
            ["find", path, "-name", name_pattern],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def df() -> str:
    """
    Display disk space usage.

    Returns:
        Disk space information or error message
    """
    try:
        result = subprocess.run(
            ["df", "-h"],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def ps() -> str:
    """
    Display running processes.

    Returns:
        Process list or error message
    """
    try:
        result = subprocess.run(
            ["ps", "aux"],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def whoami() -> str:
    """
    Display current user.

    Returns:
        Current username or error message
    """
    try:
        result = subprocess.run(
            ["whoami"],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"error: {e}"


def uname() -> str:
    """
    Display system information.

    Returns:
        System information or error message
    """
    try:
        result = subprocess.run(
            ["uname", "-a"],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"error: {e}"


def curl(url: str, options: str = "") -> str:
    """
    Fetch content from a URL.

    Args:
        url: URL to fetch
        options: Additional curl options (e.g., "-I" for headers only)

    Returns:
        Response content or error message
    """
    try:
        cmd = ["curl", "-sS"]
        if options:
            cmd.extend(options.split())
        cmd.append(url)
        
        result = subprocess.run(
            cmd,
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def which(command: str) -> str:
    """
    Locate a command in PATH.

    Args:
        command: Command name to locate

    Returns:
        Full path to command or error message
    """
    try:
        result = subprocess.run(
            ["which", command],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=5
        )
        return result.stdout.strip() if result.stdout else f"command not found: {command}"
    except Exception as e:
        return f"error: {e}"


def env() -> str:
    """
    Display environment variables.

    Returns:
        Environment variables or error message
    """
    try:
        result = subprocess.run(
            ["env"],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=5
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def head(filepath: str, lines: int = 10) -> str:
    """
    Display first N lines of a file.

    Args:
        filepath: Path to file
        lines: Number of lines to show (default 10)

    Returns:
        First N lines or error message
    """
    try:
        result = subprocess.run(
            ["head", f"-n{lines}", filepath],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def tail(filepath: str, lines: int = 10) -> str:
    """
    Display last N lines of a file.

    Args:
        filepath: Path to file
        lines: Number of lines to show (default 10)

    Returns:
        Last N lines or error message
    """
    try:
        result = subprocess.run(
            ["tail", f"-n{lines}", filepath],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def wc(filepath: str) -> str:
    """
    Count lines, words, and characters in a file.

    Args:
        filepath: Path to file

    Returns:
        Line, word, and character counts or error message
    """
    try:
        result = subprocess.run(
            ["wc", filepath],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def bash(command: str) -> str:
    """
    Execute arbitrary bash command.
    
    WARNING: Use with caution - allows arbitrary command execution.

    Args:
        command: Bash command to execute

    Returns:
        Command output or error message
    """
    try:
        result = subprocess.run(
            ["bash", "-c", command],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=60
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "error: command timed out after 60 seconds"
    except Exception as e:
        return f"error: {e}"


def tree(path: str = ".", level: int = None, options: str = "") -> str:
    """
    Display directory tree structure.

    Args:
        path: Directory path to display (defaults to current directory)
        level: Maximum depth to descend (e.g., 2 for 2 levels deep)
        options: Additional tree options (e.g., "-a" for all files, "-d" for dirs only, 
                 "--gitignore" to respect .gitignore, "-I 'pattern'" to ignore pattern)

    Returns:
        Tree structure or error message
    """
    try:
        cmd = ["tree"]
        
        # Add level limit if specified
        if level is not None:
            cmd.extend(["-L", str(level)])
        
        # Add custom options if specified
        if options:
            # Split options string and add them
            cmd.extend(options.split())
        
        # Add the path
        cmd.append(path)
        
        result = subprocess.run(
            cmd,
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def gh(command: str) -> str:
    """
    Execute GitHub CLI (gh) commands.
    
    Provides access to GitHub repositories, issues, PRs, releases, and more.
    
    Common commands:
    - "repo view" - View repository details
    - "repo list" - List user repositories  
    - "issue list" - List issues
    - "issue view <number>" - View issue details
    - "pr list" - List pull requests
    - "pr view <number>" - View PR details
    - "pr status" - Show PR status
    - "release list" - List releases
    - "status" - Show notifications and activity
    - "browse" - Open repository in browser
    - "repo clone <repo>" - Clone a repository
    
    Args:
        command: GitHub CLI command to execute (without 'gh' prefix)
                 Examples: "repo view", "issue list", "pr status"
    
    Returns:
        Command output or error message
    """
    try:
        # Build the gh command
        cmd = ["gh"] + command.split()
        
        result = subprocess.run(
            cmd,
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=60
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "error: gh command timed out after 60 seconds"
    except Exception as e:
        return f"error: {e}"


# ============================================================
# Web Search Tools (Terminal Bench Enhancement)
# ============================================================

def web_search(query: str, num_results: int = 3) -> str:
    """
    Search the web using Google with SerpAPI, extracting AI Overview and top results.
    
    Based on Apex2's breakthrough with Google AI Overview extraction.
    
    Args:
        query: Search query string
        num_results: Number of top results to fetch and analyze (default: 3)
    
    Returns:
        Formatted search results including AI overview and key findings
    """
    try:
        import os
        from serpapi import GoogleSearch
        import requests
        from bs4 import BeautifulSoup
        
        # Get API key from environment (requires SERPAPI_KEY env var)
        api_key = os.getenv("SERPAPI_KEY")
        if not api_key:
            return "error: SERPAPI_KEY environment variable not set. Please get a free key from https://serpapi.com/"
        
        # Configure search parameters
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": num_results + 5,  # Get extra results to filter through
            "hl": "en",
            "gl": "us"
        }
        
        # Perform search
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Search timeout")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(15)  # 15 second timeout
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            signal.alarm(0)  # Cancel alarm
        except TimeoutError:
            signal.alarm(0)
            return "error: Search request timed out"
        
        # Extract organic results
        organic_results = results.get("organic_results", [])
        
        if not organic_results:
            return "error: No search results found"
        
        output_parts = []
        
        # Extract AI Overview if present (key Apex2 innovation)
        ai_overview = None
        if "answer_box" in results:
            answer_box = results["answer_box"]
            if "answer" in answer_box:
                ai_overview = answer_box["answer"]
            elif "snippet" in answer_box:
                ai_overview = answer_box["snippet"]
        
        if ai_overview:
            output_parts.append(f"🤖 GOOGLE AI OVERVIEW:\n{ai_overview}\n")
        
        # Process top results
        output_parts.append(f"🔍 TOP {min(num_results, len(organic_results))} RESULTS:\n")
        
        for i, result in enumerate(organic_results[:num_results], 1):
            title = result.get("title", "No title")
            snippet = result.get("snippet", "No snippet")
            link = result.get("link", "")
            
            output_parts.append(f"{i}. {title}")
            output_parts.append(f"{snippet}")
            
            # Try to fetch content from the link for more detailed analysis
            try:
                response = requests.get(link, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract first paragraph of main content
                    content = ""
                    for tag in ['p', 'div', 'section']:
                        elements = soup.find_all(tag)
                        for elem in elements[:3]:  # First few elements
                            text = elem.get_text().strip()
                            if len(text) > 100:  # Prefer longer content
                                content = text[:500]  # Limit to 500 chars
                                break
                        if content:
                            break
                    
                    if content:
                        output_parts.append(f"📄 Content Preview: {content[:200]}...")
            except Exception as content_error:
                pass  # Silently skip content fetching on errors
            
            output_parts.append(f"🔗 Link: {link}")
            output_parts.append("")
        
        return "\n".join(output_parts)
        
    except ImportError as e:
        return f"error: Missing dependencies. Install with: uv add google-search-results requests beautifulsoup4. Error: {str(e)}"
    except Exception as e:
        return f"error: Search failed - {str(e)}"


# ============================================================
# Workspace Management Tools (Prevent Directory Pollution)
# ============================================================

def get_demo_workspace(name: str) -> str:
    """
    Get an isolated workspace directory for a demo application.
    
    Args:
        name: Name of the demo (e.g., "flask_app", "django_blog")
    
    Returns:
        Absolute path to the demo workspace
    """
    try:
        from bond.workspace import get_workspace_manager
        workspace = get_workspace_manager()
        demo_path = workspace.create_demo_workspace(name)
        return f"Demo workspace created: {demo_path}\nYou should cd to this directory before creating files."
    except Exception as e:
        return f"error: Failed to create demo workspace - {e}"

def get_test_workspace(test_type: str = "general") -> str:
    """
    Get an isolated workspace directory for tests.
    
    Args:
        test_type: Type of test (e.g., "unit", "integration", "manual")
    
    Returns:
        Absolute path to the test workspace
    """
    try:
        from bond.workspace import get_workspace_manager
        workspace = get_workspace_manager()
        test_path = workspace.create_test_workspace(test_type)
        return f"Test workspace created: {test_path}\nYou should cd to this directory before creating test files."
    except Exception as e:
        return f"error: Failed to create test workspace - {e}"

def get_temp_workspace() -> str:
    """
    Get a temporary workspace directory for scratch work.
    
    Returns:
        Absolute path to the temporary workspace
    """
    try:
        from bond.workspace import get_workspace_manager
        workspace = get_workspace_manager()
        temp_path = workspace.create_temp_session()
        return f"Temporary workspace created: {temp_path}\nThis will be auto-cleaned after 7 days."
    except Exception as e:
        return f"error: Failed to create temporary workspace - {e}"

def list_workspaces() -> str:
    """
    List all available workspaces (demos, tests, temp).
    
    Returns:
        Formatted list of workspaces
    """
    try:
        from bond.workspace import get_workspace_manager
        workspace = get_workspace_manager()
        
        output = []
        output.append("DEMO WORKSPACES:")
        demos = workspace.list_demos()
        if demos:
            for demo in demos:
                output.append(f"  • {demo.name}")
        else:
            output.append("  (none)")
        
        output.append("\nTEST WORKSPACES:")
        tests = workspace.list_tests()
        if tests:
            for test in tests:
                output.append(f"  • {test.name}")
        else:
            output.append("  (none)")
        
        output.append("\nTEMP SESSIONS:")
        temp_sessions = workspace.list_temp_sessions()
        if temp_sessions:
            for session in temp_sessions:
                # Show timestamp for better visibility
                session_age = datetime.fromtimestamp(session.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                output.append(f"  • {session.name} (created: {session_age})")
        else:
            output.append("  (none)")
        
        return "\n".join(output)
    except Exception as e:
        return f"error: Failed to list workspaces - {e}"

def cleanup_workspaces(days: int = 7) -> str:
    """
    Clean up old temporary workspaces.
    
    Args:
        days: Remove temp sessions older than this many days
    
    Returns:
        Cleanup summary
    """
    try:
        from bond.workspace import get_workspace_manager
        workspace = get_workspace_manager()
        cleaned = workspace.cleanup_old_sessions(days)
        if cleaned:
            return f"Cleaned up {len(cleaned)} temporary sessions older than {days} days:\n" + "\n".join([f"  • {name}" for name in cleaned])
        else:
            return f"No temporary sessions older than {days} days to clean up."
    except Exception as e:
        return f"error: Failed to cleanup workspaces - {e}"
