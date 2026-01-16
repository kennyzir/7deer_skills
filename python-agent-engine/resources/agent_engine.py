import os
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

# Default System Prompt (can be overridden)
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant.
Your goal is to assist the user by answering questions and performing tasks accurately.
Usage instructions:
1. Use tools when necessary to get real-time data or perform actions.
2. If you don't know the answer, say you don't know.
"""

class ThinkingStepType(str, Enum):
    """Thinking Step Types"""
    REASONING = "reasoning"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    FINAL = "final"

@dataclass
class ThinkingStep:
    """A step in the agent's reasoning process"""
    type: ThinkingStepType
    content: str
    tool_name: Optional[str] = None
    tool_args: Optional[Dict] = None
    status: str = "pending"  # pending, running, completed, failed
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "content": self.content,
            "tool_name": self.tool_name,
            "tool_args": self.tool_args,
            "status": self.status
        }

@dataclass
class AgentResponse:
    """Complete Agent Response"""
    success: bool
    content: str
    thinking_steps: List[ThinkingStep] = field(default_factory=list)
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "content": self.content,
            "thinking_steps": [s.to_dict() for s in self.thinking_steps],
            "error": self.error
        }

class AgentEngine:
    def __init__(
        self, 
        tools: List[Any], 
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        llm: Optional[BaseChatModel] = None,
        model_name: str = "gpt-4o",
        temperature: float = 0.7
    ):
        """
        Initialize the Agent Engine.
        
        Args:
            tools: List of LangChain tools (@tool decorated functions)
            system_prompt: The persona and instructions for the agent
            llm: Optional pre-configured LangChain ChatModel. If None, one will be created.
            model_name: Model name to use if creating internal LLM (e.g. 'gpt-4o', 'deepseek-chat')
            temperature: LLM temperature
        """
        self.tools = tools
        self.tool_map = {t.name: t for t in tools}
        self.system_prompt = system_prompt
        
        if llm:
            self.llm = llm
        else:
            self.llm = self._create_default_llm(model_name, temperature)

    def _create_default_llm(self, model_name: str, temperature: float) -> BaseChatModel:
        """Create LLM instance based on environment variables"""
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        if not api_key:
            raise ValueError("No API key found. Please set OPENAI_API_KEY or DEEPSEEK_API_KEY.")
            
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature
        )

    async def chat(
        self,
        user_input: str,
        history: List[Dict[str, str]] = None
    ) -> AgentResponse:
        """
        Run a chat turn with the agent.
        """
        thinking_steps: List[ThinkingStep] = []
        
        try:
            llm_with_tools = self.llm.bind_tools(self.tools)
            messages = [SystemMessage(content=self.system_prompt)]
            
            if history:
                for msg in history[-10:]:
                    if msg.get("role") == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg.get("role") == "assistant":
                        messages.append(AIMessage(content=msg["content"]))
            
            messages.append(HumanMessage(content=user_input))
            
            # Step 1: Reasoning
            thinking_steps.append(ThinkingStep(
                type=ThinkingStepType.REASONING,
                content="Analyzing request...",
                status="running"
            ))
            
            response = await llm_with_tools.ainvoke(messages)
            thinking_steps[-1].status = "completed"
            
            # Step 2: Tool Execution (if needed)
            if response.tool_calls:
                messages.append(response)
                
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    
                    step = ThinkingStep(
                        type=ThinkingStepType.TOOL_CALL,
                        content=f"Calling tool: {tool_name}",
                        tool_name=tool_name,
                        tool_args=tool_args,
                        status="running"
                    )
                    thinking_steps.append(step)
                    
                    try:
                        tool_func = self.tool_map.get(tool_name)
                        if tool_func:
                            tool_output = await tool_func.ainvoke(tool_args)
                            step.status = "completed"
                        else:
                            tool_output = f"Error: Tool {tool_name} not found"
                            step.status = "failed"
                    except Exception as e:
                        tool_output = f"Tool Error: {str(e)}"
                        step.status = "failed"
                    
                    thinking_steps.append(ThinkingStep(
                        type=ThinkingStepType.TOOL_RESULT,
                        content=str(tool_output)[:500],
                        tool_name=tool_name,
                        status="completed"
                    ))
                    
                    messages.append(ToolMessage(
                        content=str(tool_output),
                        tool_call_id=tool_call["id"]
                    ))
                
                # Step 3: Final Response
                thinking_steps.append(ThinkingStep(
                    type=ThinkingStepType.REASONING,
                    content="Generating final answer...",
                    status="running"
                ))
                
                final_response = await llm_with_tools.ainvoke(messages)
                thinking_steps[-1].status = "completed"
                final_content = final_response.content
            else:
                final_content = response.content
            
            thinking_steps.append(ThinkingStep(
                type=ThinkingStepType.FINAL,
                content="Done",
                status="completed"
            ))
            
            return AgentResponse(
                success=True,
                content=final_content,
                thinking_steps=thinking_steps
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                content=f"Error: {str(e)}",
                thinking_steps=thinking_steps,
                error=str(e)
            )
