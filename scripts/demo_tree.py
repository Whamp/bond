#!/usr/bin/env python3
"""Demo of the tree tool with various options"""

from bond import tools

print("=" * 60)
print("Tree Tool Demo")
print("=" * 60)
print()

print("1. Basic tree - 2 levels deep")
print("-" * 60)
print(tools.tree(".", level=2))
print()

print("2. Directories only - 3 levels")
print("-" * 60)
print(tools.tree(".", level=3, options="-d"))
print()

print("3. Bond package with all files (including hidden)")
print("-" * 60)
print(tools.tree("bond", options="-a"))
print()

print("4. Respecting .gitignore, ignoring __pycache__")
print("-" * 60)
print(tools.tree(".", level=2, options="--gitignore -I '__pycache__'"))
print()

print("5. Docs directory only - full depth")
print("-" * 60)
print(tools.tree("docs"))
