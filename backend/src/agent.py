from typing import List, Optional, Callable, Dict, Any
from os import environ as env
import json
import logging
import re

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolMessageParam
from openai.types.chat.chat_completion_message import FunctionCall
import httpx

logger = logging.getLogger(__name__)

# Try to import Google Generative AI (new library)
try:
    import google.genai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    try:
        import google.generativeai as genai
        GOOGLE_AI_AVAILABLE = True
        GOOGLE_AI_LEGACY = True
    except ImportError:
        GOOGLE_AI_AVAILABLE = False
        logger.warning("Google Generative AI not available. Install google-genai to use Gemini.")


def _extract_json_from_text(text: str) -> Optional[dict]:
    """Try to find the first JSON object in text and return it as dict."""
    if not text:
        return None
    start = text.find("{")
    if start == -1:
        return None
    end = text.rfind("}")
    if end == -1 or end <= start:
        return None
    candidate = text[start:end+1]
    try:
        return json.loads(candidate)
    except Exception:
        stack = []
        for i, ch in enumerate(text[start:], start):
            if ch == '{':
                stack.append(i)
            elif ch == '}':
                stack.pop()
                if not stack:
                    candidate = text[start:i+1]
                    try:
                        return json.loads(candidate)
                    except Exception:
                        return None
        return None


class AIAgent:
    def __init__(self, model: str = "gpt-4", openai_api_key: str = None):
        # Prefer an explicit GEMINI_API_KEY, then OPENAI_API_KEY for backward compatibility.
        if openai_api_key is None:
            openai_api_key = env.get("GEMINI_API_KEY") or env.get("OPENAI_API_KEY")
        
        self.api_key = openai_api_key
        
        # Check if we have a real OpenAI key (starts with sk-) or Gemini key (starts with AIza)
        if not openai_api_key:
            raise ValueError("No API key found. Set GEMINI_API_KEY or OPENAI_API_KEY in the environment.")
        elif openai_api_key.startswith("sk-your-openai-api-key-here") or openai_api_key == "sk-your-openai-api-key-here":
            # Mock mode for development
            self.provider = "mock"
            self.client = None
        elif env.get("GEMINI_API_KEY") or openai_api_key.startswith("AIza"):
            self.provider = "google"
            if GOOGLE_AI_AVAILABLE:
                try:
                    # Try new google.genai first
                    if 'google.genai' in str(genai):
                        self.client = genai.Client(api_key=openai_api_key)
                        self.model_name = "gemini-2.5-flash"  # Use 2.5-flash which should be available
                    else:
                        # Legacy google.generativeai
                        genai.configure(api_key=openai_api_key)
                        self.model_name = "gemini-1.5-flash"  # Updated model name
                        self.client = None
                except Exception as e:
                    logger.warning(f"Google AI setup failed: {e}, falling back to mock mode")
                    self.provider = "mock"
                    self.client = None
            else:
                logger.warning("Google AI not available, falling back to mock mode")
                self.provider = "mock"
                self.client = None
        else:
            self.provider = "openai"
            self.client = OpenAI(api_key=openai_api_key)

        self.model = model
        self.messages: List[ChatCompletionMessageParam] = []
        self.tool_map: Dict[str, Callable] = {}  # Map tool names to functions
        self.openai_tools = []  # List of OpenAI tool definitions
        self.google_tool_instructions: List[str] = []  # Human-readable tool descriptions for Gemini

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def register_tool(self, tool_name: str, tool_function: Callable, tool_openai_definition: Dict[str, Any]):
        """Register a tool for both OpenAI and Google flows.

        For OpenAI we keep the tool definition as-is. For Google we build a short textual
        description and parameter schema so the Gemini model can be instructed to emit
        a JSON tool-call when appropriate.
        """
        self.tool_map[tool_name] = tool_function
        self.openai_tools.append(tool_openai_definition)

        try:
            fn = tool_openai_definition.get("function", {})
            name = fn.get("name", tool_name)
            desc = fn.get("description", "")
            params = fn.get("parameters", {})
            params_text = json.dumps(params)
            instr = f"TOOL: {name}\nDESCRIPTION: {desc}\nPARAMETERS_SCHEMA: {params_text}"
            self.google_tool_instructions.append(instr)
        except Exception:
            self.google_tool_instructions.append(f"TOOL: {tool_name}")

    def _call_google_generate(self, prompt_text: str, max_tokens: int = 512) -> str:
        model_name = self.model_name  # Use the configured Gemini model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        body = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": max_tokens,
            }
        }
        r = httpx.post(url, params={"key": self.api_key}, json=body, timeout=60.0)
        r.raise_for_status()
        jr = r.json()
        ai_text = None
        if "candidates" in jr and jr["candidates"]:
            cand = jr["candidates"][0]
            if isinstance(cand, dict) and "content" in cand:
                content = cand["content"]
                if isinstance(content, dict) and "parts" in content and content["parts"]:
                    ai_text = content["parts"][0].get("text", "")
            elif isinstance(cand, dict):
                ai_text = cand.get("content") or cand.get("output") or cand.get("text")
                if isinstance(ai_text, dict) and "text" in ai_text:
                    ai_text = ai_text["text"]
            else:
                ai_text = str(cand)
        if not ai_text:
            ai_text = jr.get("output") or jr.get("text") or json.dumps(jr)
        if isinstance(ai_text, dict):
            ai_text = ai_text.get("text") or json.dumps(ai_text)
        return ai_text

    def run(self) -> str:
        if not self.messages:
            return "No messages to process."

        if self.provider == "mock":
            return self._run_mock_mode()

        if self.provider == "google":
            return self._run_google_http_api()

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.openai_tools if self.openai_tools else None,
            )
            assistant_message = response.choices[0].message
            self.messages.append(assistant_message)

            tool_calls = (
                assistant_message.get("tool_calls")
                if isinstance(assistant_message, dict)
                else getattr(assistant_message, "tool_calls", None)
            )
            if tool_calls:
                logger.info(f"Tool calls detected: {tool_calls}")
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args_str = tool_call.function.arguments
                    if function_name in self.tool_map:
                        try:
                            function_args = json.loads(function_args_str)
                            logger.info(f"Executing tool {function_name} with args: {function_args}")
                            tool_output = self.tool_map[function_name](**function_args)
                            logger.info(f"Tool {function_name} output: {tool_output}")
                            self.messages.append(
                                ChatCompletionToolMessageParam(
                                    tool_call_id=tool_call.id,
                                    role="tool",
                                    content=json.dumps(tool_output),
                                )
                            )
                            second_response = self.client.chat.completions.create(
                                model=self.model, messages=self.messages
                            )
                            second_assistant_message = second_response.choices[0].message
                            self.messages.append(second_assistant_message)
                            return second_assistant_message.content or ""
                        except json.JSONDecodeError:
                            logger.error(
                                f"Error: Invalid JSON arguments for tool {function_name}"
                            )
                            return f"Error: Invalid JSON arguments for tool {function_name}"
                        except Exception as e:
                            logger.error(f"Error executing tool {function_name}: {e}")
                            return f"Error executing tool {function_name}: {e}"
                    else:
                        logger.error(f"Error: Tool {function_name} not found.")
                        return f"Error: Tool {function_name} not found."

            return assistant_message.content or ""

        return "Unknown provider"

    def _run_mock_mode(self) -> str:
        """Run in mock mode for development"""
        last_message = self.messages[-1] if self.messages else {}
        user_message = last_message.get("content", "")
        user_message_lower = user_message.lower()
        
        # Check if user wants to add a task
        if "add" in user_message_lower and ("task" in user_message_lower or "todo" in user_message_lower):
            # Extract task name/description more carefully
            task_description = user_message
            
            # Look for patterns like "add task X" or "add a task called X"
            patterns = [
                r"add.*?task\s+called\s+(.+)",
                r"add.*?task\s+(.+)",
                r"add.*?todo\s+called\s+(.+)",
                r"add.*?todo\s+(.+)",
                r"create.*?task\s+called\s+(.+)",
                r"create.*?task\s+(.+)",
                r"new.*?task\s+called\s+(.+)",
                r"new.*?task\s+(.+)"
            ]
            
            extracted = None
            for pattern in patterns:
                match = re.search(pattern, user_message_lower)
                if match:
                    extracted = match.group(1).strip()
                    break
            
            if extracted:
                task_description = extracted
            else:
                # Fallback: just use the original message
                task_description = "New task from chat"
            
            # Simulate tool call
            if "add_task" in self.tool_map:
                try:
                    result = self.tool_map["add_task"](description=task_description, title=task_description)
                    response = f"I've successfully added the task: '{task_description}'. Task ID: {result.get('task_id', 'unknown')}"
                except Exception as e:
                    response = f"I tried to add the task but encountered an error: {e}"
            else:
                response = "I'd like to help you add a task, but the task management system isn't properly configured."
        
        elif "list" in user_message_lower and ("task" in user_message_lower or "todo" in user_message_lower):
            # Get tasks
            if "get_tasks" in self.tool_map:
                try:
                    result = self.tool_map["get_tasks"]()
                    tasks = result.get("tasks", [])
                    if tasks:
                        task_list = "\n".join([f"- {task['title']}: {task['description']}" for task in tasks])
                        response = f"Here are your current tasks:\n{task_list}"
                    else:
                        response = "You don't have any tasks yet. Would you like me to add one?"
                except Exception as e:
                    response = f"I tried to get your tasks but encountered an error: {e}"
            else:
                response = "I'd like to help you list your tasks, but the task management system isn't properly configured."
        
        else:
            response = f"I'm a helpful assistant! I can help you manage your tasks. Try saying 'add task [description]' or 'list my tasks'. You said: {user_message}"
        
        assistant_message = {"role": "assistant", "content": response}
        self.messages.append(assistant_message)
        return response

    def _run_google_http_api(self) -> str:
        """Fallback to old HTTP API"""
        tool_section = "\n\n".join(self.google_tool_instructions) if self.google_tool_instructions else ""
        conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in self.messages])
        guidance = (
            "If you want to call one of the tools, return exactly a JSON object anywhere in the"
            " assistant response with the shape: {\"tool_call\": {\"name\": \"tool_name\", \"arguments\": { ... } }}."
            " Otherwise, respond normally with plain text."
        )
        prompt_text = "\n\n".join(x for x in [tool_section, guidance, conversation_text] if x)

        try:
            ai_text = self._call_google_generate(prompt_text)
        except Exception as e:
            logger.error(f"Google Generative API error: {e}")
            logger.info("Falling back to mock mode")
            return self._run_mock_mode()

        assistant_message = {"role": "assistant", "content": ai_text}
        self.messages.append(assistant_message)

        parsed = _extract_json_from_text(ai_text)
        if parsed and isinstance(parsed, dict) and "tool_call" in parsed:
            tc = parsed["tool_call"]
            name = tc.get("name")
            args = tc.get("arguments") or {}
            if name and name in self.tool_map:
                try:
                    logger.info(f"Executing Google tool {name} with args: {args}")
                    tool_output = self.tool_map[name](**args)
                    logger.info(f"Tool {name} output: {tool_output}")
                    tool_message_text = json.dumps({"tool": name, "output": tool_output})
                    self.messages.append({"role": "tool", "content": tool_message_text})

                    conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in self.messages])
                    prompt_text = "\n\n".join(x for x in [tool_section, guidance, conversation_text] if x)
                    try:
                        final_text = self._call_google_generate(prompt_text)
                    except Exception as e:
                        logger.error(f"Google Generative API second pass error: {e}")
                        return f"Tool executed successfully: {tool_output}"
                    final_assistant_message = {"role": "assistant", "content": final_text}
                    self.messages.append(final_assistant_message)
                    return final_text or ""
                except Exception as e:
                    logger.error(f"Error executing tool {name}: {e}")
                    return f"Error executing tool {name}: {e}"
            else:
                logger.error(f"Tool {name} not found or invalid tool call format.")
                return f"Error: Tool {name} not found or invalid tool call format."

        return ai_text or ""