# Product Requirements Document (PRD): New Hire Onboarding Workflow

## Business Goals & Impact
This project aims to completely automate the multi-day coordination of new hire onboarding, transforming a disjointed, manual process into a seamless, asynchronous agentic workflow.

The primary business objectives and impacts are:
1. **Enable Long-Latency Human-in-the-Loop:** Seamlessly pause agent execution for hours or days while waiting on slow human actions (e.g., signing legal documents) or physical processes (e.g., shipping hardware) without breaking the workflow.
2. **Drastic Cost Savings via Scale-to-Zero:** Eliminate "sleep loops" and persistent compute. While waiting for webhooks, the underlying infrastructure can completely scale down or turn off, saving significant cloud compute and LLM token costs.
3. **Resilience & State Durability:** Guarantee zero data loss. If an instance crashes or is preempted during a multi-day onboarding, the agent can instantly hydrate its exact state from the persistent database and resume perfectly.
4. **Cross-Department Automation:** Eliminate manual HR and IT handoffs by allowing the Root Agent to autonomously delegate sub-tasks to specialized IT sub-agents.

## Non-Goals
* We are NOT building the actual internal HR/IT APIs (e.g., DocuSign, Slack, Jira, FedEx).
* We are NOT building a frontend UI.
* We are NOT implementing live database integrations for employee records.
* We are NOT deploying to cloud infrastructure in this initial phase (Prototype First).

## Constraints & Safety Rules
1. **Strict State Enforcement:** The agent must never jump from `START` to `IT_PROVISIONED` or `HARDWARE_DELIVERED` without the explicit state transitions provided by webhook events.
2. **Safe Fallbacks & Manual Overrides:** Sub-agents must return structured status payloads rather than throwing fatal exceptions. If a sub-agent fails, the system must wait for a manual webhook override. Similarly, if external waits timeout, it must transition to stalled states and wait for human overrides.
3. **Error Handling:** The agent must not enter infinite retry loops. It should handle the mock failures gracefully.

## Success Criteria & Evals
* The system must pass a Golden Evaluation dataset (`eval_dataset.json`) that simulates the entire flow, including delays for signatures and hardware delivery, proving that context is never lost and states are not skipped.
