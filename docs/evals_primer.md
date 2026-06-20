# ADK Evaluations Primer: Eval-Driven Development

In the world of AI agents, you do not write pytest assertions to check if an LLM returned the exact string "Hello". Because LLMs are non-deterministic, exact string matching is brittle. Instead, ADK uses **Semantic Evaluation (LLM-as-a-Judge)** and structured trajectory analysis.

## Pillar 1: The Input Dataset (What are we testing?)

There are two shapes of evaluation datasets in ADK, both living inside an `EvaluationDataset` JSON structure:

1. **Single-Turn (`prompt`)**: You pass a single prompt, and the agent responds. This is for simple bots (e.g., QA or summarization).
2. **Multi-Turn Trajectory (`agent_data`)**: The heavyweight champion for stateful agents. Because agents often handle multi-day processes with asynchronous webhooks, testing a single prompt is useless. We feed the agent an entire sequence of `events` and `turns` to see how it navigates a state machine over time.

**Key Insight:** For asynchronous events (like webhooks), you inject them as `author: "user"` text events in the `turns` array, exactly as an external system integration would dispatch them to the session.

## Pillar 2: The Metrics (How do we score it?)

Metrics are configured in `tests/eval/eval_config.yaml`. There are three categories of metrics:

### A. Built-in LLM-as-a-Judge Metrics (The Gold Standard)
ADK provides managed evaluators that use an LLM to semantically grade your agent's trace.
* `multi_turn_task_success`: Did the agent ultimately achieve the user's goal?
* `multi_turn_trajectory_quality`: Did the agent take a logical path? Did it wait for the right webhooks before calling downstream tools?
* `multi_turn_tool_use_quality`: Did it pass the correct arguments to the simulated tools without hallucinating parameters?

### B. Custom LLM Metrics
If built-in metrics aren't specific enough, define a custom `prompt_template` in your config.
Example: *"Review this trace and ensure the agent maintained a highly empathetic HR tone throughout."*

### C. Custom CodeExecution Metrics
When you need deterministic, pure Python checks, you write a `custom_function`. 
Example: *Fail the test if the conversation exceeded 10 turns, or if a specific string wasn't emitted.*

## Pillar 3: The Quality Flywheel (The Workflow)

The iterative loop for improving agent quality relies on a 5-step CLI flywheel:

1. **Prepare Data (`eval dataset synthesize`)**: Write your `eval_dataset.json` manually (for TDD) or use the synthesize command to have an LLM simulate a user and auto-generate traces against your live agent.
2. **Generate (`agents-cli eval generate`)**: The framework runs your agent through the dataset and writes a raw `.json` trace file in `artifacts/traces/`.
3. **Grade (`agents-cli eval grade`)**: The framework scores the traces against your `eval_config.yaml` metrics and outputs an HTML report detailing why the judge passed or failed each case. *(Shortcut: `agents-cli eval run` does generate + grade in one shot).*
4. **Analyze (`agents-cli eval analyze`)**: If you have many failing tests, this command clusters the failures and diagnoses the root cause across the dataset.
5. **Optimize (`agents-cli eval optimize`)**: If your prompt is the issue, this runs the ADK GEPA optimizer to auto-rewrite your agent's instructions to pass the failing metric.

## Summary of the Eval-Driven Workflow

1. Write the Golden Evaluation Dataset (`eval_dataset.json`).
2. Run `agents-cli eval run` (it will fail).
3. Implement the agent logic (`app/agent.py`).
4. Rerun `agents-cli eval run` and inspect `results.html` until all metrics pass.
5. If a regression occurs, run `agents-cli eval compare baseline.json new.json` to prove your fix worked mathematically.
