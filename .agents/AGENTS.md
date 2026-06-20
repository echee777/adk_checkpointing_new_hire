# Project Rules

<RULE>
## Strict Spec Iteration
Before writing any implementation code or executing project scaffolds, you MUST be extremely disciplined about iterating on the specification (`.agents-cli-spec.md` or equivalent). Do not rush to the code generation phase. You must aggressively question the user, clarify business goals, define architectural edge cases, and establish clear non-goals.

**CRITICAL BEHAVIOR:** You are FORBIDDEN from asking the user if they are "ready to code", "ready to execute", or prompting them to use the `/goal` command. Your default assumption must always be that the spec is incomplete. At the end of your turns, you must actively probe for missing requirements (e.g., "What edge cases are we missing?" or "What else should we clarify?") until the user explicitly, unprompted, gives you the green light to proceed to code generation.
</RULE>

<RULE>
## Verify Plumbing, Don't Theorize
When answering deep architectural questions or making assertions about underlying framework mechanics (especially ADK plumbing like sub-agent delegation, async event loops, or state hydration), you MUST NOT hallucinate or over-extrapolate based on high-level design philosophies. 
Instead, you must empirically verify the implementation details by:
1. Using `grep_search` to read the exact code patterns in your loaded skill files (`~/.gemini/config/skills/`).
2. Executing python scripts in the sandbox to dynamically inspect the live library (e.g., `import google.adk; help(...)`).
Only make architectural assertions once you have grounded them in physical code behavior.
</RULE>

<RULE>
## ADK Architectural Axioms & Phase-Gate Forcing Functions

To prevent context-window bloat while ensuring high-quality engineering, you must adhere to the following absolute axioms and conditionally load context via Phase-Gate forcing functions.

### Stop-the-Line Architectural Axioms (Unconditional)
1. **ADK 2.0 Workflow Standard:** All orchestrators MUST use the ADK 2.0 `Workflow` API. Legacy `SequentialAgent` constructs are banned.
2. **Schema Enforcement:** Any `LlmAgent` sub-agent MUST have a strict Pydantic `output_schema`. No raw dicts.
3. **No Pytest for LLM Outputs:** NEVER write pytest tests that assert on LLM output content. Pytest is strictly for deterministic code correctness.
4. **Code Preservation:** NEVER change the agent's model version or rewrite core instructions unless explicitly requested.
5. **Eval-Driven Development (TDD):** After running the scaffolding command, you MUST stop and write the Golden Evaluation Dataset (`tests/eval/datasets/eval_dataset.json`). You are FORBIDDEN from writing agent implementation code (`app/agent.py`) until the user approves the evaluation dataset.

### Phase-Gate Skill Forcing Functions (JIT Context Loading)
To execute work in specific phases, you MUST read the respective skill document *before* generating logic or executing commands:
* **Scaffolding/Project Setup:** You MUST read the `google-agents-cli-scaffold` skill.
* **Agent Implementation/Coding:** You MUST read the `google-agents-cli-adk-code` skill.
* **Writing/Running Evaluations:** You MUST read the `google-agents-cli-eval` skill.
* **Deployment Setup:** You MUST read the `google-agents-cli-deploy` skill.
</RULE>

<RULE>
## Strategic Execution Logging (NOTES.md)
Whenever a major strategic milestone, architectural decision, or phase transition occurs, you MUST append a semantic summary of the progress to `docs/NOTES.md`. The goal of this log is to capture the "big strokes" of *how* the project was executed (the methodology, the vibe coding sequence) so that a developer returning years later can instantly understand the strategic trajectory of the project.
</RULE>

<RULE>
## Cloud-Native & 12-Factor Architecture
You MUST architect all applications following strict 12-Factor App principles to ensure they are platform-agnostic and container-ready:

1. **Observability (Stdout Only):** Never use proprietary cloud SDKs (e.g., `google-cloud-logging`) for transporting logs or traces if a standard protocol exists. Emit structured JSON to `stdout` and rely the container orchestrator to capture it.
2. **Configuration (Environment Isolation):** All configuration must be injected via environment variables. You are FORBIDDEN from writing environment-checking logic (e.g., `if env == "prod"`) deep inside business logic or routes.
3. **Stateless Processes:** The application must execute as one or more stateless processes. Never rely on the local filesystem or sticky memory (global variables) for anything other than a brief single-request cache.
4. **Backing Services:** Treat all external APIs, databases, and LLM providers as attached resources. Their credentials and connection URIs must be injected, never hardcoded or implicitly assumed by the codebase.
</RULE>
