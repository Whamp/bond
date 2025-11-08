"""
Workspace management utilities for Bond agent.
Prevents pollution of the Bond project directory by isolating demos, tests, and temporary files.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import time


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
        # Sanitize name to be filesystem-friendly
        clean_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in name)
        demo_name = f"{clean_name}_{timestamp}"
        demo_path = self.demos_dir / demo_name
        demo_path.mkdir(exist_ok=True)
        
        # Create a README to explain what this is
        readme = demo_path / "README.md"
        readme.write_text(
            f"# Demo: {name}\n\n"
            f"Created by Bond at {datetime.now()}\n\n"
            f"This is an isolated demo workspace.\n"
            f"All files here are temporary and can be safely deleted.\n"
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
        clean_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in test_type)
        test_name = f"{clean_name}_{timestamp}"
        test_path = self.tests_dir / test_name
        test_path.mkdir(exist_ok=True)
        return test_path
    
    def create_temp_session(self) -> Path:
        """
        Create a temporary session workspace for scratch work.
        Automatically cleaned up after 7 days.
        
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
        cutoff_time = time.time() - (days * 86400)
        
        cleaned = []
        for session_dir in self.temp_dir.glob("session_*"):
            if session_dir.is_dir():
                if session_dir.stat().st_mtime < cutoff_time:
                    shutil.rmtree(session_dir)
                    cleaned.append(session_dir.name)
        
        return cleaned
    
    def list_demos(self) -> list[Path]:
        """List all demo workspaces"""
        return sorted(self.demos_dir.glob("*"))
    
    def list_tests(self) -> list[Path]:
        """List all test workspaces"""
        return sorted(self.tests_dir.glob("*"))
    
    def list_temp_sessions(self) -> list[Path]:
        """List all temporary sessions"""
        return sorted(self.temp_dir.glob("session_*"))
    
    def get_current_workspace(self) -> Optional[Path]:
        """Get the current working directory if it's in a workspace"""
        cwd = Path.cwd()
        try:
            cwd.relative_to(self.base_dir)
            return cwd
        except ValueError:
            return None
    
    def clean_all_demos(self) -> int:
        """Remove all demo workspaces"""
        demos = self.list_demos()
        for demo in demos:
            if demo.is_dir():
                shutil.rmtree(demo)
        return len(demos)
    
    def clean_all_tests(self) -> int:
        """Remove all test workspaces"""
        tests = self.list_tests()
        for test in tests:
            if test.is_dir():
                shutil.rmtree(test)
        return len(tests)


# Global workspace manager instance
_workspace_manager = None

def get_workspace_manager() -> WorkspaceManager:
    """Get or create the global workspace manager"""
    global _workspace_manager
    if _workspace_manager is None:
        _workspace_manager = WorkspaceManager()
    return _workspace_manager
