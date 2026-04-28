---
name: python-agent-engine
description: "Scaffolds a LangChain-based AI agent in Python with ReAct reasoning, tool calling, and thinking-step visualization. Use when the user wants to build an AI agent, create a LangChain chatbot, implement tool-calling workflows, scaffold a ReAct agent, or add autonomous agent capabilities to a Python project."
---

# Python Agent Engine

A plug-and-play AI Agent core for Python applications — handles LLM interaction, tool calling loops, and context management. Works with OpenAI, DeepSeek, or any OpenAI-compatible API.

## Installation

1. Copy `resources/agent_engine.py` to your project (e.g., `src/core/agent_engine.py`).
2. Install dependencies:
   ```bash
   pip install langchain-core langchain-openai python-dotenv
   ```
3. Set Environment Variables in your `.env` file:
   ```ini
   OPENAI_API_KEY=sk-...
   # Optional:
   OPENAI_BASE_URL=https://api.openai.com/v1
   ```

## Usage Example

```python
import asyncio
from langchain_core.tools import tool
from core.agent_engine import AgentEngine

# 1. Define Tools
@tool
def calculator(expression: str) -> str:
    """Calculates a math expression."""
    return str(eval(expression))

# 2. Initialize Agent
agent = AgentEngine(
    tools=[calculator],
    system_prompt="You are a helpful math assistant.",
    model_name="gpt-4o"
)

# 3. Chat
async def main():
    response = await agent.chat("What is 123 * 456?")
    
    print(f"Answer: {response.content}")
    print("\nThinking Steps:")
    for step in response.thinking_steps:
        print(f"[{step.type}] {step.content}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Verification

After setup, run a quick smoke test to confirm the agent works:

```bash
python -c "
import asyncio
from core.agent_engine import AgentEngine
agent = AgentEngine(tools=[], system_prompt='Say hello.', model_name='gpt-4o')
print(asyncio.run(agent.chat('Hi')).content)
"
```

If you see a greeting, the agent is wired up correctly. Common failures:
- `OPENAI_API_KEY` not set or invalid — check your `.env` file
- `ModuleNotFoundError` — run `pip install langchain-core langchain-openai python-dotenv`
- Connection timeout — verify `OPENAI_BASE_URL` is reachable
