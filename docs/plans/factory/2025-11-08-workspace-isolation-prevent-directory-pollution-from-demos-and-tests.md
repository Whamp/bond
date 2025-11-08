# Workspace Isolation Plan: Prevent Directory Pollution

## Problem
When Bond's LLM creates demo applications (like the Flask app), it pollutes the Bond project directory with unrelated files. This makes the project messy and requires manual cleanup.

## Solution: Multi-Layer Isolation Strategy

### **Layer 1: Dedicated Workspace Directory Structure**

Create a clear directory structure for temporary work:

```
/home/will/projects/bond/
├── bond/                    # Core Bond code (existing)
├── docs/                    # Documentation (existing)
├── .workspace/              # NEW: Isolated workspace for demos/tests
│   ├── demos/               # Demo applications created by Bond
│   │   ├── flask_demo_001/
│   │   ├── django_demo_002/
│   │   └── ...
│   ├── tests/               # Test files and outputs
│   │   ├── unit_tests/
│   │   ├── integration_tests/
│   │   └── ...
│   └── temp/                # Temporary scratch space
│       └── session_<timestamp>/
└── .gitignore              # Updated to ignore .workspace/
```

### **Layer 2: Workspace Manager Utility**

Create `bond/workspace.py` to manage isolated workspaces:

```python
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

class WorkspaceManager:
    """
    Manages isolated workspaces for demos, tests, and temporary files.
    Prevents pollution of the Bond project directory.
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize workspace manager.
        
        Args:
            base_dir: Base directory for workspaces (defaults to .workspace/)
        """
        if base_dir is None:
            # Find Bond project root (where pyproject.toml is)
            project_root = self._find_project_root()
            base_dir = project_root / ".workspace"
        
        self.base_dir = Path(base_dir)
        self.demos_dir = self.base_dir / "demos"
        self.tests_dir = self.base_dir / "tests"
        self.temp_dir = self.base_dir / "temp"
        
        # Create directories if they don't exist
        self.base_dir.mkdir(exist_ok=True)
        self.demos_dir.mkdir(exist_ok=True)
        self.tests_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    def _find_project_root(self) -> Path:
        """Find the Bond project root by looking for pyproject.toml"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists():
                return parent
        return Path.cwd()
    
    def create_demo_workspace(self, name: str) -> Path:
        """
        Create an isolated workspace for a demo application.
        
        Args:
            name: Name of the demo (e.g., "flask_app")
        
        Returns:
            Path to the demo workspace
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        demo_name = f"{name}_{timestamp}"
        demo_path = self.demos_dir / demo_name
        demo_path.mkdir(exist_ok=True)
        
        # Create a README to explain what this is
        readme = demo_path / "README.md"
        readme.write_text(
            f"# Demo: {name}\n\n"
            f"Created by Bond at {datetime.now()}\n\n"
            f"This is an isolated demo workspace.\n"
        )
        
        return demo_path
    
    def create_test_workspace(self, test_type: str) -> Path:
        """
        Create an isolated workspace for tests.
        
        Args:
            test_type: Type of test (e.g., "unit", "integration")
        
        Returns:
            Path to the test workspace
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = f"{test_type}_{timestamp}"
        test_path = self.tests_dir / test_name
        test_path.mkdir(exist_ok=True)
        return test_path
    
    def create_temp_session(self) -> Path:
        """
        Create a temporary session workspace for scratch work.
        Automatically cleaned up on exit.
        
        Returns:
            Path to temporary session directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_path = self.temp_dir / f"session_{timestamp}"
        session_path.mkdir(exist_ok=True)
        return session_path
    
    def cleanup_old_sessions(self, days: int = 7):
        """
        Clean up temporary sessions older than specified days.
        
        Args:
            days: Number of days to keep sessions
        """
        import time
        cutoff_time = time.time() - (days * 86400)
        
        for session_dir in self.temp_dir.glob("session_*"):
            if session_dir.is_dir():
                if session_dir.stat().st_mtime < cutoff_time:
                    shutil.rmtree(session_dir)
                    print(f"Cleaned up old session: {session_dir.name}")
    
    def list_demos(self) -> list[Path]:
        """List all demo workspaces"""
        return sorted(self.demos_dir.glob("*"))
    
    def list_tests(self) -> list[Path]:
        """List all test workspaces"""
        return sorted(self.tests_dir.glob("*"))
    
    def get_current_workspace(self) -> Optional[Path]:
        """Get the current working directory if it's in a workspace"""
        cwd = Path.cwd()
        try:
            cwd.relative_to(self.base_dir)
            return cwd
        except ValueError:
            return None
```

### **Layer 3: System Prompt Enhancement**

Add workspace awareness to the agent's system prompt:

```python
# In bond/agent.py

WORKSPACE_SYSTEM_PROMPT = """
IMPORTANT: Workspace Management Rules

When creating demo applications, test files, or temporary files:

1. ALWAYS use the workspace system:
   - Call get_demo_workspace(name) to get an isolated directory for demos
   - Call get_test_workspace(type) to get an isolated directory for tests
   - Call get_temp_workspace() for scratch/temporary work

2. NEVER create demo files in the Bond project root directory
   - Don't create files like app.py, requirements.txt, etc. in /home/will/projects/bond/
   - Always work in the isolated workspace provided

3. When demonstrating how to build something:
   - First get the appropriate workspace path
   - cd to that workspace
   - Then create your demo files
   - Inform the user about the workspace location

4. Example workflow:
   User: "how to set up a flask app"
   You: 
   - Get demo workspace: /home/will/projects/bond/.workspace/demos/flask_app_20251108_123456
   - cd to that directory
   - Create app.py, templates/, static/, etc. there
   - Show the user the complete demo in that isolated location

This keeps the Bond project clean and organized!
"""
```

### **Layer 4: Workspace Tools for the Agent**

Add new tools to `bond/tools.py`:

```python
# In bond/tools.py

from bond.workspace import WorkspaceManager

_workspace_manager = None

def get_workspace_manager() -> WorkspaceManager:
    """Get or create the global workspace manager"""
    global _workspace_manager
    if _workspace_manager is None:
        _workspace_manager = WorkspaceManager()
    return _workspace_manager

def get_demo_workspace(name: str) -> str:
    """
    Get an isolated workspace directory for a demo application.
    
    Args:
        name: Name of the demo (e.g., "flask_app", "django_blog")
    
    Returns:
        Absolute path to the demo workspace
    """
    try:
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
        workspace = get_workspace_manager()
        workspace.cleanup_old_sessions(days)
        return f"Cleaned up temporary sessions older than {days} days"
    except Exception as e:
        return f"error: Failed to cleanup workspaces - {e}"
```

### **Layer 5: Register Workspace Tools in CLI**

Update `bond/cli.py` to register the new workspace tools:

```python
# In bond/cli.py setup_agent() function

    # Workspace management tools
    agent.add_tool(
        name="get_demo_workspace",
        description="Get an isolated workspace directory for demo applications. ALWAYS use this before creating demo files to avoid polluting the project directory.",
        parameters={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the demo (e.g., 'flask_app', 'react_todo')"
                }
            },
            "required": ["name"],
        },
        function=tools.get_demo_workspace
    )

    agent.add_tool(
        name="get_test_workspace",
        description="Get an isolated workspace directory for test files",
        parameters={
            "type": "object",
            "properties": {
                "test_type": {
                    "type": "string",
                    "description": "Type of test (e.g., 'unit', 'integration', 'manual')"
                }
            },
            "required": [],
        },
        function=tools.get_test_workspace
    )

    agent.add_tool(
        name="list_workspaces",
        description="List all demo and test workspaces",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        function=tools.list_workspaces
    )

    agent.add_tool(
        name="cleanup_workspaces",
        description="Clean up old temporary workspaces (older than specified days)",
        parameters={
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "Remove temp sessions older than this many days (default: 7)"
                }
            },
            "required": [],
        },
        function=tools.cleanup_workspaces
    )
```

### **Layer 6: Update .gitignore**

Add workspace directory to `.gitignore`:

```gitignore
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
.env

# Workspace directories (demos, tests, temp files)
.workspace/
```

### **Layer 7: Agent System Prompt Integration**

Update `bond/agent.py` to include workspace awareness:

```python
# In BondAgent.__init__()

def __init__(self):
    """Initialize the agent with configuration and empty context."""
    self.config = load_config()
    self.client = Anthropic(
        api_key=self.config['auth_token'],
        base_url=self.config['base_url']
    )
    self.context: List[Dict[str, Any]] = []
    self.tools: Dict[str, Dict[str, Any]] = {}
    self.tool_functions: Dict[str, Callable] = {}
    
    # Add workspace management system prompt to initial context
    self._add_workspace_prompt()

def _add_workspace_prompt(self):
    """Add workspace management instructions to the agent"""
    workspace_prompt = """
WORKSPACE MANAGEMENT RULES:

When creating demo applications or test files, you MUST use the workspace system:
- Call get_demo_workspace("name") before creating any demo files
- Always cd to the workspace directory before creating files
- Never create demo files in the Bond project root

Example:
User: "show me how to create a Flask app"
You:
1. Call get_demo_workspace("flask_app") → gets /path/to/.workspace/demos/flask_app_123/
2. Call bash("cd /path/to/.workspace/demos/flask_app_123")
3. Create demo files in that directory
4. Tell user where the demo was created

This keeps the Bond project directory clean!
"""
    # This will be added as a system message when processing requests
    self.workspace_prompt = workspace_prompt
```

## Implementation Summary

### Files to Create:
1. `bond/workspace.py` - WorkspaceManager class (new file, ~150 lines)
2. Add workspace tools to `bond/tools.py` (~80 lines)
3. Register tools in `bond/cli.py` (~40 lines)
4. Update `bond/agent.py` to include workspace prompt (~20 lines)
5. Update `.gitignore` (1 line)

### Benefits:
✅ Prevents directory pollution  
✅ Easy cleanup of old demos/tests  
✅ Clear organization of temporary work  
✅ LLM is guided to use workspaces automatically  
✅ User can easily find and manage demo workspaces  
✅ Git ignores all temporary work  

### Timeline:
**1 hour to implement** - Simple, self-contained feature

### Testing:
1. Ask Bond to create a Flask demo → should create in `.workspace/demos/`
2. Ask Bond to run tests → should use `.workspace/tests/`
3. Check project root stays clean
4. Test cleanup_workspaces() removes old sessions

This is a pragmatic solution that leverages the LLM's tool-calling capability to enforce good workspace hygiene!