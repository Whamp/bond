# Apex2 Process Flow Orchestration - Final Specification

## Implementation Details Fully Specified

### 1. Strategy Synthesis Skill (`strategy-synthesis/SKILL.md`)

**Data Ingestion Mechanism**:
- **Tools**: Read, Grep, **Execute** (added - to cat/grep skill outputs)
- **Input Sources**:
  1. Orchestrator passes findings as structured context in invocation
  2. Can read temporary files if orchestrator writes them: `/tmp/apex2-prediction.txt`
  3. Can execute: `echo "$PREDICTION_RESULTS"` if environment vars set
  4. Parses skill output from conversation history (Claude's context)

**Concrete Process**:
```markdown
1. Receive findings from orchestrator invocation message:
   "Synthesize these findings:
    Prediction: [task=ML, risk=medium, files=[train.py, model.py]]
    Web: [found pytorch example, stackoverflow solution]
    Strategy: [approach A: simple training, approach B: cross-validation]
    Environment: [pytorch installed, GPU available, 16GB RAM]"

2. Parse structured data from each source
3. Cross-reference for compatibility
4. Generate unified plan
```

**Output Format**: Structured markdown the orchestrator can parse

**Directory**: `/home/will/projects/bond/.claude/skills/strategy-synthesis/SKILL.md`

---

### 2. State Tracking - Explicit Mechanism

**Where State Lives**: 

**Option A - Orchestrator Context Memory** (Recommended):
```markdown
The orchestrator maintains state in its own conversation context:

[Apex2 State]
Phase: parallel-intelligence
Completed: {prediction: true, web: true, strategy: false, env: true}
Turn: 7
Episode: 1
Last-Synthesis: null
```

Orchestrator outputs this state block after each skill completes.
Other components read state from orchestrator's messages.

**Option B - Temporary Files**:
```bash
# Orchestrator writes state to project-level tracking file
/tmp/apex2-state.json
{
  "phase": "parallel-intelligence",
  "completed": {"prediction": true, "web": true, ...},
  "turn": 7
}
```

Skills can `cat /tmp/apex2-state.json` to check state.

**Option C - Environment Variables**:
```bash
export APEX2_PHASE="parallel-intelligence"
export APEX2_COMPLETED_PREDICTION="true"
```

Skills check with `echo $APEX2_PHASE`.

**Recommended**: **Option A (Context Memory)** because:
- No file I/O overhead
- Survives across sessions naturally
- Visible to users in conversation
- Claude Code subagents maintain separate context

**Implementation**: Orchestrator's SKILL.md includes:
```markdown
## State Management

After each skill invocation, output:

[Apex2 State: phase=X, completed={...}, turn=N]

Before next phase, verify all required skills completed.
```

---

### 3. Turn 10 Pause/Resume Mechanics

**Pause Mechanism**:
```markdown
At Turn 10:
1. Complete current atomic operation (don't leave half-written code)
2. If mid-edit: finish the file edit and save
3. If mid-command: let command complete
4. Output: "[Apex2] Pausing for mid-execution intelligence refresh..."
5. Create checkpoint: save current state/context

Checkpoint includes:
- What was just completed
- What's next in the plan
- Any in-progress work
- Current file states
```

**Refresh Process**:
```markdown
1. Re-invoke environment-observer
   → Check for: new processes, changed files, resource usage
   
2. Re-invoke web-research (if errors encountered)
   → Search for: specific errors seen, performance issues
   → Skip if execution going smoothly

3. Re-invoke deep-strategy
   → Input: progress so far, any blockers
   → Output: adjusted approach, new alternatives

4. Quick synthesis (lightweight)
   → Combine refresh findings
   → Adjust execution plan if needed
```

**Resume Process**:
```markdown
1. Output: "[Apex2] Resuming execution with updated context..."
2. Remind self of checkpoint state
3. Apply any strategy adjustments from refresh
4. Continue from where paused
```

**Fallback if Turn 10 Not Supported**:
```markdown
Orchestrator tracks turns manually:
- Count each user/assistant exchange
- At turn 10, explicitly state: "I'm at turn 10, performing refresh"
- No hooks needed, just internal counting
```

---

### 4. Hooks - Research First, Documented Fallbacks

**Research Tasks**:
1. Check if Claude Code hooks exist: `ls /home/will/projects/bond/.claude/hooks/`
2. Read Claude Code docs on hooks (if referenced in project)
3. Test simple hook: `{"hooks": {"test": {"command": "echo test"}}}`

**If Hooks Supported - Implement**:
```json
{
  "hooks": {
    "beforeTask": {
      "enabled": true,
      "command": "Invoke predictive-intelligence skill on this task"
    },
    "onError": {
      "enabled": true,
      "command": "Invoke execution-recovery skill with error: ${error}"
    },
    "beforeCompletion": {
      "enabled": true,
      "command": "Invoke validation-guardian skill before claiming done"
    }
  }
}
```

**Fallback if Hooks NOT Supported**:
```markdown
In apex2-orchestrator.md:

## Manual Triggers (Hooks Fallback)

Since lifecycle hooks aren't available:

1. Always start with: "First, I'll analyze this task..."
   → Explicitly invoke predictive-intelligence

2. On any error, immediately: "Let me recover from this error..."
   → Explicitly invoke execution-recovery

3. Before saying "done": "Let me validate this work..."
   → Explicitly invoke validation-guardian

4. At turn 10: Check turn count, trigger refresh manually
```

**Turn 10 Fallback**:
- Orchestrator includes: "Count turns. At turn 10, perform refresh."
- No automation, just explicit instruction in system prompt

---

### 5. Apex2 Orchestrator (`agents/apex2-orchestrator.md`)

**Complete Data Flow Documentation**:

```markdown
## Data Flow Between Phases

### Phase 1: Prediction
Input: User task description
Process: Invoke predictive-intelligence skill
Output: Task analysis → stored in [Apex2 State]

### Phase 2: Parallel Intelligence
Input: Task analysis from Phase 1
Process: 
  - Invoke web-research (with task context)
  - Invoke deep-strategy (with task context)
  - Invoke environment-observer (with key files from prediction)
Output: Three intelligence reports → stored in [Apex2 State]

### Phase 3: Synthesis
Input: All intelligence reports from Phase 2
Process: Invoke strategy-synthesis with structured findings
Data passed as: "Synthesize: [prediction results], [web results], ..."
Output: Unified execution plan → stored in [Apex2 State]

### Phase 4: Execution (Episode 2+)
Input: Unified execution plan from Phase 3
Process: Execute plan step-by-step, invoke recovery on errors
Output: Execution results → checkpoint state

### Phase 5: Turn 10 Refresh
Input: Current checkpoint, progress so far
Process: Re-run observer/web/strategy with updated context
Output: Updated execution plan → merge into state

### Phase 6: Validation
Input: Claimed completion state
Process: Invoke validation-guardian
Output: Pass/fail → determines task completion
```

**State Management Section**:
```markdown
## State Tracking

I maintain state in my context using this format:

[Apex2 State]
Phase: prediction|parallel|synthesis|execution|validation
Turn: <number>
Episode: 1|2|3...
Completed: {
  prediction: true|false,
  web: true|false,
  strategy: true|false,
  environment: true|false,
  synthesis: true|false
}
Findings: {
  prediction: "...",
  web: "...",
  strategy: "...",
  environment: "..."
}

I output this state block after each phase transition.
I check state before proceeding to next phase.
```

---

### 6. Apex2 Output Style (`output-styles/apex2-workflow.md`)

**Turn Counting Instructions**:
```markdown
## Turn Management

Track conversation turns manually:
- Count each user message + your response = 1 turn
- Keep running count in your responses
- At turn 10: "This is turn 10. Performing mid-execution refresh..."

Turn 10 Refresh Procedure:
[detailed refresh steps from section 3 above]
```

**Restating Auto-Triggers** (from orchestrator):
```markdown
## Automatic Behaviors

Even without hooks, enforce these behaviors:

1. ALWAYS start tasks with prediction:
   "Before I begin, let me analyze this task..."

2. ALWAYS recover from errors:
   "I encountered an error. Let me apply recovery strategies..."

3. ALWAYS validate before completion:
   "Before declaring this complete, let me validate..."

4. ALWAYS refresh at turn 10:
   "This is turn 10. Performing intelligence refresh..."
```

---

## Complete File Structure

```
/home/will/projects/bond/.claude/
├── agents/
│   └── apex2-orchestrator.md          [orchestration + data flow + state]
├── output-styles/
│   └── apex2-workflow.md              [behavioral instructions + turn tracking]
├── hooks/
│   └── hooks.json                     [after research; fallback documented]
├── skills/
│   ├── predictive-intelligence/       [EXISTING]
│   ├── deep-strategy/                 [EXISTING]
│   ├── environment-observer/          [EXISTING]
│   ├── web-research/                  [EXISTING]
│   ├── execution-recovery/            [EXISTING]
│   ├── validation-guardian/           [EXISTING]
│   └── strategy-synthesis/            [NEW - with Execute for data ingestion]
│       └── SKILL.md
└── APEX2-WORKFLOW.md                  [integration docs + all mechanisms]
```

---

## Implementation Order (Revised)

1. ✅ **Research hooks** (verify capabilities, document findings)
2. ✅ **Create strategy-synthesis skill** (with Execute tool, data ingestion)
3. ✅ **Create apex2-orchestrator** (with state tracking, data flow, turn counting)
4. ✅ **Create apex2-workflow output style** (with manual triggers, turn tracking)
5. ✅ **Implement hooks IF supported** (with documented fallbacks if not)
6. ✅ **Create APEX2-WORKFLOW.md** (document all mechanisms, state storage, data flow)
7. ✅ **Test state tracking** (verify state visible and persistent)
8. ✅ **Test Turn 10** (manually trigger, verify refresh works)
9. ✅ **Test synthesis** (verify data flows from skills to synthesis)
10. ✅ **Test complete workflow** (end-to-end validation)

---

## Resolved Issues

✅ **Synthesis has concrete data ingestion** (Execute tool + structured invocation)
✅ **State tracking explicitly documented** (Context memory with output blocks)
✅ **Turn 10 pause/resume mechanics defined** (Complete atomic ops, checkpoint, refresh, resume)
✅ **Hooks research prioritized** (Test first, document fallbacks)
✅ **Data flow fully specified** (Phase-by-phase with input/output/storage)
✅ **Naming verified** (strategy-synthesis directory included in structure)
✅ **Dependencies documented** (How Episode 1 results feed into synthesis)

Ready to implement with all mechanics fully specified?