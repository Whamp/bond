# Bash Tools for Bond Agent

This document describes the bash/system tools available to the Bond agent.

## Philosophy

Following the Fly.io pattern, all tools are:
- Simple Python functions with clear signatures
- Robustly error-handled with try/except blocks
- Return strings for simplicity (or JSON-serializable objects)
- Use subprocess.run() with proper parameters:
  - `text=True` for string output
  - `stderr=subprocess.STDOUT` to capture errors
  - Appropriate timeouts to prevent hanging
  - Return `"error: {message}"` on failure

## Tool Categories

### Basic Utilities
- **ping(host)** - Test network connectivity to a host
- **echo(message)** - Echo back a message
- **calculate(operation, a, b)** - Perform basic math (add, subtract, multiply, divide)
- **get_system_info()** - Get platform, Python version, architecture info

### File System Operations
- **ls(path=".")** - List directory contents with details (-lah)
- **pwd()** - Print current working directory
- **cat(filepath)** - Display file contents
- **head(filepath, lines=10)** - Show first N lines of a file
- **tail(filepath, lines=10)** - Show last N lines of a file
- **wc(filepath)** - Count lines, words, and characters in a file
- **grep(pattern, filepath)** - Search for pattern in file (with line numbers)
- **find(path, name_pattern="*")** - Find files matching a pattern
- **tree(path=".", level=None, options="")** - Display directory tree structure
  - `level`: Limit depth (e.g., 2 for 2 levels)
  - `options`: Common options include:
    - `-a` - Show all files including hidden
    - `-d` - Show directories only
    - `--gitignore` - Respect .gitignore files
    - `-I 'pattern'` - Ignore files matching pattern
    - `-L N` - Already handled by level parameter

### System Information
- **whoami()** - Display current username
- **uname()** - Display system information (OS, kernel, etc.)
- **df()** - Display disk space usage for all filesystems
- **ps()** - Display currently running processes
- **env()** - Display environment variables
- **which(command)** - Locate a command in the system PATH

### Network Operations
- **curl(url, options="")** - Fetch content from a URL
  - Supports additional curl options (e.g., "-I" for headers)
  - 30-second timeout

### GitHub CLI
- **gh(command)** - Execute GitHub CLI commands
  - Common commands:
    - `"repo view"` - View current repository details
    - `"repo list"` - List your repositories
    - `"issue list"` - List issues in current repo
    - `"issue view <number>"` - View specific issue
    - `"pr list"` - List pull requests
    - `"pr view <number>"` - View specific PR
    - `"pr status"` - Show your PR status
    - `"release list"` - List releases
    - `"status"` - Show notifications and activity
    - `"browse"` - Open repo in browser
  - 60-second timeout
  - Requires gh CLI to be installed and authenticated

### Advanced Execution
- **bash(command)** - Execute arbitrary bash command
  - ⚠️ Use with caution - allows any command execution
  - 60-second timeout
  - Captures stdout and stderr combined

## Usage Examples

```python
from bond import tools

# File operations
content = tools.cat("README.md")
files = tools.find(".", "*.py")
first_lines = tools.head("main.py", lines=20)

# Tree structure - very useful for understanding project layout
tree_all = tools.tree(".", level=2)  # 2 levels deep
tree_dirs = tools.tree(".", level=3, options="-d")  # Directories only
tree_clean = tools.tree(".", options="--gitignore -I '__pycache__'")  # Respect .gitignore

# System info
user = tools.whoami()
os_info = tools.uname()
space = tools.df()

# Network
ping_result = tools.ping("google.com")
webpage = tools.curl("https://example.com")
headers = tools.curl("https://example.com", "-I")

# GitHub operations
repo_info = tools.gh("repo view")
my_repos = tools.gh("repo list")
issues = tools.gh("issue list")
prs = tools.gh("pr list")
pr_status = tools.gh("pr status")
releases = tools.gh("release list")
notifications = tools.gh("status")

# Advanced
result = tools.bash("ls -la | grep .py | wc -l")
```

## Error Handling

All tools return `"error: {message}"` if they fail. This allows the LLM to understand what went wrong and potentially retry or use a different approach.

Example:
```python
result = tools.cat("/nonexistent/file.txt")
# Returns: "error: cat: /nonexistent/file.txt: No such file or directory"
```

## Timeouts

All tools have appropriate timeouts to prevent hanging:
- Quick operations (pwd, whoami, which): 5 seconds
- File operations (cat, grep, ls): 10 seconds
- Search operations (find): 30 seconds
- Network operations (curl, ping): 30 seconds
- Bash execution: 60 seconds

## Security Considerations

The `bash` tool allows arbitrary command execution, which is powerful but potentially dangerous. Consider:
- The agent runs with the same permissions as the user
- Commands can modify files, install software, etc.
- No sandboxing is currently implemented
- For production use, consider restricting available commands or implementing approval workflows

## Future Enhancements

Potential additions:
- **mkdir/rmdir** - Directory creation/deletion
- **cp/mv/rm** - File operations (with safety checks)
- **git operations** - Status, diff, commit, etc.
- **ssh/scp** - Remote operations
- **docker** - Container management
- **python -m** - Python module execution
- **pipe composition** - Chain multiple tools together
