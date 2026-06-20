# Testing Architecture

This directory contains the deterministic, pre-deployment Python test suites for the agent. Unlike the LLM evaluations (`eval/`), these tests execute standard Python assertions without invoking the language model API, ensuring the core networking and business logic are sound.

## 1. Unit Tests (`unit/`)
- **Purpose:** Test pure, isolated Python business logic (e.g., custom data transformations, regex parsers, or complex logic inside your tools) without booting up the ADK runner or LLM.
- **Current State:** Contains `test_dummy.py` as a placeholder. Add your tool-specific unit tests here.

## 2. Integration Tests (`integration/`)
- **Purpose:** Ensure that the ADK agent, memory sessions, and FastAPI web server boot up and communicate correctly.
- **Files:**
  - `test_agent.py`: Instantiates the ADK `root_agent` purely in Python using an `InMemorySessionService`. Asserts that the ADK `Runner` executes the agent graph without crashing and successfully yields Server-Sent Events (SSE) streams.
  - `test_server_e2e.py`: A full End-to-End network test. It boots the FastAPI server (`app.fast_api_app:app`) in a background subprocess and fires real HTTP `POST` requests to `/run_sse`, `/sessions`, and `/feedback`, asserting proper `200 OK` responses, valid JSON streaming payloads, and correct `422` error handling for malformed input.

## How to Run
```bash
uv run pytest tests/unit tests/integration
```
