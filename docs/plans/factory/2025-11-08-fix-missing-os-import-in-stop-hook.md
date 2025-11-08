## Fix: Add Missing `import os` to Stop Hook

### Problem
The Stop hook in `.claude/hooks/hooks.json` (line ~128-145) uses `os.path.exists('/tmp/apex2-hooks.log')` without importing the `os` module, causing a `NameError` on every Stop event.

### Solution
Add `import os` at the top of the Stop hook's Python snippet, right after the opening quotes.

### Changes Required
**File**: `/home/will/projects/bond/.claude/hooks/hooks.json`

In the `Stop` hook section, change:
```python
python3 -c "
try:
  # Check if validation should be triggered
  ...
```

To:
```python
python3 -c "
import os
try:
  # Check if validation should be triggered
  ...
```

This preserves all existing log behavior while fixing the import error that prevents the hook from functioning.