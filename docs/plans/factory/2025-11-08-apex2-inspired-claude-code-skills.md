# Apex2-Inspired Claude Code Skills

Creating 6 specialized skills in `/home/will/projects/bond/.claude/skills/` that implement Apex2's SOTA Terminal Bench patterns.

## Directory Structure
```
/home/will/projects/bond/.claude/skills/
├── predictive-intelligence/
│   └── SKILL.md
├── deep-strategy/
│   └── SKILL.md
├── environment-observer/
│   └── SKILL.md
├── web-research/
│   └── SKILL.md
├── execution-recovery/
│   └── SKILL.md
└── validation-guardian/
    └── SKILL.md
```

## Skills Overview

### 1. Predictive Intelligence
- Analyzes tasks before execution
- Categorizes by type (ML, security, web, data, etc.)
- Identifies key files and risk factors
- **Tools**: Read, Grep, Glob (read-only)

### 2. Deep Strategy
- Extracts comprehensive knowledge upfront
- Generates alternative approaches
- Identifies failure modes and remediation
- **Tools**: Read, Grep, Glob (read-only)

### 3. Environment Observer
- Discovers system state heuristically
- Checks packages, processes, structure
- Provides context for execution
- **Tools**: Execute, Read, Grep, Glob

### 4. Web Research
- Multi-round search with specific queries
- Prioritizes GitHub/StackOverflow
- Extracts actionable insights
- **Tools**: WebSearch, Read

### 5. Execution Recovery
- Handles common execution failures
- Syntax, import, path, permission errors
- Implements fixes automatically
- **Tools**: Read, Edit, Execute, Grep

### 6. Validation Guardian
- Prevents premature completion
- Checks for errors in output/logs
- Verifies expected results exist
- **Tools**: Read, Execute, Grep

## Key Benefits
- **Upfront intelligence**: Understand before executing (Apex2's prediction phase)
- **Parallel exploration**: Multiple perspectives simultaneously
- **Risk awareness**: Category-specific guidance
- **Robust recovery**: Handle failures gracefully
- **Quality gates**: Validation before completion

All work stays within `/home/will/projects/bond/.claude/` - no changes to Bond project code itself.

Ready to proceed?