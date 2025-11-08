# Bond Terminal Bench Enhancement: Apex2 Intelligence Integration

## Executive Summary
Enhance Bond to prepare for Terminal Bench benchmarking by extracting and adapting Apex2's SOTA methodologies, focusing on multi-phase intelligence gathering, web search with Google AI Overview extraction, and execution optimization.

## Core Architecture: Multi-Phase Intelligence System

### Phase 1: Predictive Intelligence (New)
**Goal**: Extract task metadata before execution to guide exploration
- **Task Categorization Tool**: Analyze instruction to determine risk profile (security, ML, system, web, etc.)
- **Key File Identification Tool**: Extract filenames/paths mentioned in task description using regex/LLM parsing
- **Multimodal Assessment Tool**: Predict if visual/document analysis needed from instruction keywords

### Phase 2: Parallel Intelligence Gathering (Enhanced)
**Goal**: Gather diverse perspectives simultaneously using multiple specialized agents

#### 2.1 Web Search Tool (CRITICAL - High Token Budget)
Based on Apex2's breakthrough with Google AI Overview:

**Implementation Requirements**:
- Use SERP API or direct Google search scraping (not vendor websearch APIs)
- **Multi-round search**: 3 rounds maximum per task
- **Query Generation Strategy**:
  - Use Claude to generate low-frequency, highly specific search terms
  - Bias toward GitHub/StackOverflow/documentation sites
  - Avoid generic tutorial queries
- **Google AI Overview Extraction**: 
  - Parse Google's AI-generated summary box (appears at top of results)
  - This often contains synthesized, actionable solutions
  - Allocate 2000+ tokens for AI Overview analysis
- **Deep Link Analysis**: Fetch and analyze top 3 results per query
- **Quality Control**: Filter any Terminal Bench mentions to prevent contamination
- **Progressive refinement**: Each round uses previous findings to refine queries

**Tool Signature**:
```python
def web_search(
    query: str, 
    round_num: int = 1,
    previous_findings: Optional[str] = None,
    bias_domains: List[str] = ["github.com", "stackoverflow.com"]
) -> Dict[str, Any]:
    """
    Returns: {
        "ai_overview": str,  # Google's AI summary
        "top_links": List[Dict],  # Top 3 results with content
        "refined_query_suggestion": str  # For next round
    }
    """
```

#### 2.2 Heuristic Environment Observation Tool
**Goal**: Understand environment state systematically

**Implementation**:
```python
def observe_environment(key_files: List[str] = None) -> Dict[str, str]:
    """
    Returns: {
        "installed_packages": "pip list | grep <relevant>",
        "folder_structure": "find . -type f -name '*.py' | head -20",
        "running_processes": "ps aux | grep python",
        "system_state": "df -h && free -m",
        "key_file_contents": {file: cat(file) for file in key_files}
    }
    """
```

#### 2.3 Deep Strategy Generation Tool
**Goal**: Extract everything the LLM knows about the task

**Prompt Design** (High token budget: 1500+ tokens):
```
Given this task: {instruction}

Generate a comprehensive strategy including:
1. Knowledge extraction: What do you know about this type of task?
2. Two alternative approaches with specific command sequences
3. Risk assessment: What operations could cause irreversible damage?
4. Common failure modes and remediation strategies
5. Key unknowns that need Docker exploration
```

#### 2.4 Docker Exploration Agent (New)
**Goal**: Test hypotheses about unknowns in isolated container
- Spawn temporary Docker container matching environment
- Test specific hypotheses from strategy (e.g., "Does package X support flag Y?")
- Return findings without polluting main execution context

### Phase 3: Strategy Synthesis (New)
**Goal**: Combine all intelligence into optimized execution context

**Synthesis Tool**:
```python
def synthesize_intelligence(
    web_findings: Dict,
    env_observation: Dict,
    deep_strategy: Dict,
    docker_exploration: Dict,
    episode1_execution: Optional[str] = None
) -> str:
    """
    Returns: Optimized context prompt for main execution that:
    - Prioritizes web search solutions
    - Integrates environment constraints
    - Combines strategy alternatives
    - Adds Docker-validated facts
    - Includes Episode 1 quick wins
    """
```

### Phase 4: Optimized Execution (Enhanced)
**Goal**: Execute with risk-aware, recovery-capable system

#### 4.1 Risk-Aware Category Prompting
Based on task category, inject specific guidance:
- **ML Tasks**: "Training may exceed 5 minutes. ALWAYS test with small parameters first (e.g., epochs=1) before full runs."
- **Security Tasks**: "Operations may be irreversible. Ground exact command sequences before execution. Verify backups."
- **System Tasks**: "Check current state before modifications. Document rollback steps."

#### 4.2 Heredoc Optimization Tool
```python
def create_file_heredoc(filepath: str, content: str) -> str:
    """
    Generate properly escaped heredoc command for file creation.
    Handles: indentation, special chars, EOF markers, quote escaping
    """
```

#### 4.3 Recovery Prompt System
Detect common execution errors and inject recovery prompts:
- Syntax errors → "Check indentation and quotes"
- Import errors → "Verify package installation and imports"
- Path errors → "Use absolute paths or verify cwd"
- Permission errors → "Check file permissions or use sudo"
- Timeout → "Operation exceeded limit, try alternative approach"

#### 4.4 Validation Tool
```python
def validate_completion(task_instruction: str, execution_log: str) -> bool:
    """
    Prevents premature completion by checking:
    - No parsing errors in output
    - No execution errors in logs  
    - Test results complete
    - Expected outputs present
    """
```

## Integration with Harbor Framework

### Bond as BaseInstalledAgent
```python
class BondInstalledAgent(BaseInstalledAgent):
    def _install_agent_template_path(self) -> Path:
        return Path(__file__).parent / "install_bond.sh"
    
    def create_run_agent_commands(self, instruction: str) -> List[ExecInput]:
        # Phase 1: Prediction
        # Phase 2: Parallel intelligence (web, env, strategy, docker)
        # Phase 3: Synthesis
        # Phase 4: Optimized execution with recovery
        return [ExecInput(command=f"bond run --instruction '{instruction}'")]
    
    def populate_context_post_run(self, context: AgentContext) -> None:
        # Parse trajectory from /logs/agent/
        pass
```

## Key Implementation Priorities

### Must Have (P0):
1. **Web Search with AI Overview** - The breakthrough innovation
2. **Multi-round search strategy** - 3 rounds with refinement
3. **Strategy synthesis** - Combining parallel intelligence
4. **Risk-aware category prompting** - Prevents failures before they happen

### Should Have (P1):
5. **Heuristic environment observation** - Context-aware execution
6. **Heredoc optimization** - Eliminates file creation errors
7. **Recovery prompt system** - Handles common failures
8. **Validation tool** - Prevents false completions

### Nice to Have (P2):
9. **Docker exploration agent** - Test hypotheses safely
10. **Predictive intelligence** - Upfront task analysis
11. **Second parallel exploration** - Mid-execution intelligence refresh

## Token Budget Allocation
Based on Apex2's finding that "larger token amounts for searching and planning was very effective":

- **Web Search**: 3000 tokens (3 rounds × 1000 each)
  - AI Overview analysis: 800 tokens per round
  - Deep link analysis: 200 tokens per link
- **Deep Strategy**: 1500 tokens
- **Strategy Synthesis**: 1000 tokens
- **Main Execution**: Remaining budget
- **Recovery/Validation**: 500 tokens

## Success Metrics
- **Primary**: Accuracy on Terminal Bench 2.0 (target: >55% with GLM-4.6)
- **Secondary**: Task completion time, token efficiency, recovery success rate

## Next Steps
1. Implement SERP-based web_search tool with AI Overview extraction
2. Build multi-round search orchestration
3. Implement strategy synthesis framework
4. Add risk-aware category detection and prompting
5. Integrate with Harbor's BaseInstalledAgent interface
6. Run baseline benchmarks on Terminal Bench 2.0
