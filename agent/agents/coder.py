from agent.core.llm import call_llm
from agent.tools.code_runner import run_code, CODE_RUNNER_TOOL
import json

CODER_SYSTEM = """You are a Coder Agent. Your job is to:
- Write clean, efficient Python code
- Execute code and return results
- Debug errors automatically
- Always show code first, then output

Always write working, tested code."""

CODER_TOOLS = [CODE_RUNNER_TOOL]
CODER_TOOL_MAP = {"run_code": run_code}

def run_coder(task: str) -> str:
    print(f"\n💻 Coder Agent: {task}")
    messages = [
        {"role": "system", "content": CODER_SYSTEM},
        {"role": "user", "content": task}
    ]

    for _ in range(3):
        message = call_llm(messages, CODER_TOOLS)

        if message.tool_calls:
            messages.append({"role": "assistant", "content": message.content or "", "tool_calls": [
                {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in message.tool_calls
            ]})

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                result = CODER_TOOL_MAP.get(tool_name, lambda **k: "Unknown tool")(**tool_args)
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
        else:
            return message.content or "No code generated."

    return "Coding task complete."