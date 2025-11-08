#!/usr/bin/env python3
"""Demo of the GitHub CLI tool"""

import sys
sys.path.insert(0, '.')
from bond import tools

print("=" * 70)
print("GitHub CLI Tool Demo")
print("=" * 70)
print()

print("1. Check gh version")
print("-" * 70)
result = tools.gh("--version")
print(result)

print("2. View current repository")
print("-" * 70)
result = tools.gh("repo view")
print(result[:600] + "..." if len(result) > 600 else result)
print()

print("3. Check status (assigned issues and PRs)")
print("-" * 70)
result = tools.gh("status")
print(result)
print()

print("4. List issues in current repo")
print("-" * 70)
result = tools.gh("issue list")
if result.strip():
    print(result)
else:
    print("No issues found")
print()

print("5. List pull requests")
print("-" * 70)
result = tools.gh("pr list")
if result.strip():
    print(result)
else:
    print("No pull requests found")
print()

print("6. List releases")
print("-" * 70)
result = tools.gh("release list")
if result.strip():
    print(result)
else:
    print("No releases found")
print()

print("=" * 70)
print("Demo complete!")
print("=" * 70)
print()
print("Other useful commands to try:")
print("  • tools.gh('repo list')              - List your repositories")
print("  • tools.gh('issue view 1')           - View issue #1")
print("  • tools.gh('pr view 1')              - View PR #1")
print("  • tools.gh('pr status')              - Check PR status")
print("  • tools.gh('browse')                 - Open repo in browser")
print("  • tools.gh('api repos/:owner/:repo') - Use GitHub API directly")
