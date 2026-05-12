import json
from agent.core.llm import call_llm
from agent.core.context import ContextManager
from agent.tools.web_search import web_search, WEB_SEARCH_TOOL
from agent.tools.code_runner import run_code, CODE_RUNNER_TOOL
from agent.tools.file_analyzer import analyze_file, FILE_ANALYZER_TOOL
from agent.tools.api_fetcher import fetch_news, fetch_stock, FETCH_NEWS_TOOL, FETCH_STOCK_TOOL

SYSTEM_PROMPT = (
    "You are AgentX, a powerful AI assistant that can:\n"
    "1. Search the web for current information\n"
    "2. Write and execute Python code\n"
    "3. Analyze files (PDF, Word, text, code)\n"
    "4. Fetch latest news and stock prices\n\n"
    "IMPORTANT RULES:\n"
    "- Call each tool ONLY ONCE per task\n"
    "- Do NOT repeat the same tool with same arguments\n"
    "- After getting tool result, give final answer immediately\n"
    "- Be concise and direct in responses\n"
    "- When asked to write code, ALWAYS respond in this EXACT format:\n"
    "  Here is the code:\n"
    "  ```python\n"
    "  <actual code here>\n"
    "  ```\n"
    "  Output:\n"
    "  <actual output here>\n"
    "- NEVER explain code in prose, ALWAYS show the actual code block first\n"
)

TOOLS = [
    WEB_SEARCH_TOOL,
    CODE_RUNNER_TOOL,
    FILE_ANALYZER_TOOL,
    FETCH_NEWS_TOOL,
    FETCH_STOCK_TOOL
]

TOOL_MAP = {
    "web_search": web_search,
    "run_code": run_code,
    "analyze_file": analyze_file,
    "fetch_news": fetch_news,
    "fetch_stock": fetch_stock
}

MAX_ITERATIONS = 5


def run_agent(user_input: str, context: ContextManager) -> str:
    context.add_user_message(user_input)

    for iteration in range(MAX_ITERATIONS):
        message = call_llm(context.get_messages(), TOOLS)

        if message.tool_calls:
            context.add_assistant_with_tools(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"\n🔧 Tool: {tool_name} | Args: {tool_args}")

                if tool_name in TOOL_MAP:
                    result = TOOL_MAP[tool_name](**tool_args)
                else:
                    result = f"Unknown tool: {tool_name}"

                print(f"✅ Result: {result[:200]}...")

                context.add_tool_result(tool_call.id, result)
		# Code tool result directly return karo
                if tool_name == "run_code":
                    context.add_assistant_message(result)
                    return result

        else:
            final_response = message.content or "Koi response nahi mila."
            context.add_assistant_message(final_response)
            return final_response

    return "Max iterations reach ho gayi. Task complete nahi hua."