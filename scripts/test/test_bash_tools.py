#!/usr/bin/env python3
"""Test the new bash tools to ensure they work properly"""

from bond import tools

def test_tools():
    """Run a quick test of each bash tool"""
    
    print("Testing bash tools...\n")
    
    # Test pwd
    print("1. Testing pwd()...")
    result = tools.pwd()
    print(f"   Result: {result[:50]}...")
    assert not result.startswith("error"), f"pwd failed: {result}"
    
    # Test whoami
    print("2. Testing whoami()...")
    result = tools.whoami()
    print(f"   Result: {result}")
    assert not result.startswith("error"), f"whoami failed: {result}"
    
    # Test ls
    print("3. Testing ls()...")
    result = tools.ls(".")
    print(f"   Result: {result[:100]}...")
    assert not result.startswith("error"), f"ls failed: {result}"
    
    # Test which
    print("4. Testing which('python')...")
    result = tools.which("python")
    print(f"   Result: {result}")
    # which may not find python, that's ok
    
    # Test uname
    print("5. Testing uname()...")
    result = tools.uname()
    print(f"   Result: {result[:80]}...")
    assert not result.startswith("error"), f"uname failed: {result}"
    
    # Test cat on this file
    print("6. Testing cat() on this script...")
    result = tools.cat(__file__)
    print(f"   Result: {len(result)} characters")
    assert not result.startswith("error"), f"cat failed: {result}"
    assert "test_tools" in result, "cat didn't return file content"
    
    # Test head
    print("7. Testing head() on this script...")
    result = tools.head(__file__, lines=5)
    print(f"   Result: {len(result)} characters")
    assert not result.startswith("error"), f"head failed: {result}"
    
    # Test wc
    print("8. Testing wc() on this script...")
    result = tools.wc(__file__)
    print(f"   Result: {result.strip()}")
    assert not result.startswith("error"), f"wc failed: {result}"
    
    # Test find
    print("9. Testing find()...")
    result = tools.find(".", "*.py")
    print(f"   Result: Found {len(result.splitlines())} Python files")
    assert not result.startswith("error"), f"find failed: {result}"
    
    # Test bash with simple command
    print("10. Testing bash() with 'echo hello'...")
    result = tools.bash("echo hello")
    print(f"   Result: {result.strip()}")
    assert result.strip() == "hello", f"bash failed: {result}"
    
    # Test tree
    print("11. Testing tree() with level=1...")
    result = tools.tree(".", level=1, options="-d")
    print(f"   Result: {len(result.splitlines())} lines")
    assert not result.startswith("error"), f"tree failed: {result}"
    assert "directories" in result or "directory" in result, "tree didn't produce directory count"
    
    # Test gh (GitHub CLI)
    print("12. Testing gh() with --version...")
    result = tools.gh("--version")
    print(f"   Result: {result.splitlines()[0] if result else 'empty'}")
    assert not result.startswith("error"), f"gh failed: {result}"
    assert "gh version" in result, "gh didn't return version info"
    
    print("\n✅ All tools tested successfully!")
    return True

if __name__ == "__main__":
    try:
        test_tools()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
