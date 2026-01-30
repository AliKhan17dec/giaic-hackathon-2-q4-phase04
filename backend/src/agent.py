from typing import List, Optional, Callable, Dict, Any
from os import environ as env
import json
import logging # Import logging

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolMessageParam
from openai.types.chat.chat_completion_message import FunctionCall

logger = logging.getLogger(__name__) # Initialize logger

class AIAgent:
    def __init__(self, model: str = "gpt-4", openai_api_key: str = None):
        if openai_api_key is None:
            openai_api_key = env.get("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
        self.messages: List[ChatCompletionMessageParam] = []
        self.tool_map: Dict[str, Callable] = {} # Map tool names to functions
        self.openai_tools = [] # List of OpenAI tool definitions

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def register_tool(self, tool_name: str, tool_function: Callable, tool_openai_definition: Dict[str, Any]):
        self.tool_map[tool_name] = tool_function
        self.openai_tools.append(tool_openai_definition)

    def run(self) -> str:
        if not self.messages:
            return "No messages to process."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.openai_tools if self.openai_tools else None
        )
        assistant_message = response.choices[0].message
        self.messages.append(assistant_message)

        if assistant_message.tool_calls:
            logger.info(f"Tool calls detected: {assistant_message.tool_calls}") # Log tool calls
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args_str = tool_call.function.arguments
                
                if function_name in self.tool_map:
                    try:
                        function_args = json.loads(function_args_str)
                        logger.info(f"Executing tool {function_name} with args: {function_args}") # Log tool execution
                        tool_function = self.tool_map[function_name]
                        tool_output = tool_function(**function_args)
                        logger.info(f"Tool {function_name} output: {tool_output}") # Log tool output
                        self.messages.append(
                            ChatCompletionToolMessageParam(
                                tool_call_id=tool_call.id,
                                role="tool",
                                content=json.dumps(tool_output)
                            )
                        )
                        second_response = self.client.chat.completions.create(
                            model=self.model,
                            messages=self.messages
                        )
                        second_assistant_message = second_response.choices[0].message
                        self.messages.append(second_assistant_message)
                        return second_assistant_message.content if second_assistant_message.content else ""
                    except json.JSONDecodeError:
                        logger.error(f"Error: Invalid JSON arguments for tool {function_name}") # Log error
                        return f"Error: Invalid JSON arguments for tool {function_name}"
                    except Exception as e:
                        logger.error(f"Error executing tool {function_name}: {e}") # Log error
                        return f"Error executing tool {function_name}: {e}"
                else:
                    logger.error(f"Error: Tool {function_name} not found.") # Log error
                    return f"Error: Tool {function_name} not found."
        
        return assistant_message.content if assistant_message.content else ""