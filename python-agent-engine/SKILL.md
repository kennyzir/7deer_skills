---
name: python-agent-engine
description: A production-ready Python AI Agent engine using LangChain. Supports ReAct pattern, tool calling, and thinking process tracking.
---

# Python Agent Engine

A plug-and-play AI Agent core for Python applications. It handles the complexity of LLM interaction, tool calling loops, and context management.

## Features
- **ReAct Loop**: Automatically handles "Reasoning -> Tool Call -> Result -> Answer" process.
- **Thinking Process**: Returns structured "Thinking Steps" for UI visualization.
- **Model Agnostic**: Works with OpenAI, DeepSeek, or any OpenAI-compatible API.

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
