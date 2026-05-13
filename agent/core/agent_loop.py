import json
from agent.core.llm import call_llm
from agent.core.context import ContextManager
from agent.core.planner import create_plan, summarize_results
from agent.tools.web_search import web_search, WEB_SEARCH_TOOL
from agent.tools.code_runner import run_code, CODE_RUNNER_TOOL
from agent.tools.file_analyzer import analyze_file, FILE_ANALYZER_TOOL
from agent.tools.api_fetcher import fetch_news, fetch_stock, FETCH_NEWS_TOOL, FETCH_STOCK_TOOL
from agent.tools.weather import get_weather, WEATHER_TOOL
from agent.tools.web_summarizer import summarize_website, WEB_SUMMARIZER_TOOL
from agent.tools.currency import convert_currency, CURRENCY_TOOL
from agent.tools.data_analysis import analyze_data, DATA_ANALYSIS_TOOL
from agent.tools.memory import remember, recall, forget, REMEMBER_TOOL, RECALL_TOOL, FORGET_TOOL
from agent.tools.image_gen import generate_image, IMAGE_GEN_TOOL

SYSTEM_PROMPT = (
    "You are AgentX, a powerful autonomous AI agent that can:\n"
    "1. Search the web for current information\n"
    "2. Write and execute Python code\n"
    "3. Analyze files (PDF, Word, text, code)\n"
    "4. Fetch latest news and stock prices\n"
    "5. Get current weather for any city\n"
    "6. Summarize any website or URL\n"
    "7. Convert currencies with live rates\n"
    "8. Analyze CSV and Excel data files\n"
    "9. Remember and recall information across sessions\n"
    "10. Generate AI images from text descriptions\n\n"
    "IMPORTANT RULES:\n"
    "- Call each tool ONLY ONCE per task\n"
    "- Do NOT repeat the same tool with same arguments\n"
    "- After getting tool result, give final answer immediately\n"
    "- Be concise and direct in responses\n"
    "- When user shares personal info, use 'remember' tool automatically\n"
    "- When asked about past info, use 'recall' tool\n"
    "- When asked to write code, ALWAYS show code block first then output\n"
)

TOOLS = [
    WEB_SEARCH_TOOL,
    CODE_RUNNER_TOOL,
    FILE_ANALYZER_TOOL,
    FETCH_NEWS_TOOL,
    FETCH_STOCK_TOOL,
    WEATHER_TOOL,
    WEB_SUMMARIZER_TOOL,
    CURRENCY_TOOL,
    DATA_ANALYSIS_TOOL,
    REMEMBER_TOOL,
    RECALL_TOOL,
    FORGET_TOOL,
    IMAGE_GEN_TOOL
]

TOOL_MAP = {
    "web_search": web_search,
    "run_code": run_code,
    "analyze_file": analyze_file,
    "fetch_news": fetch_news,
    "fetch_stock": fetch_stock,
    "get_weather": get_weather,
    "summarize_website": summarize_website,
    "convert_currency": convert_currency,
    "analyze_data": analyze_data,
    "remember": remember,
    "recall": recall,
    "forget": forget,
    "generate_image": generate_image
}

MAX_ITERATIONS = 5

AGENTIC_KEYWORDS = [
    "research", "analyze", "report", "investigate", "find out everything",
    "full analysis", "complete report", "detailed", "comprehensive",
    "step by step", "plan", "automate", "do everything", "handle this"
]


def is_agentic_task(user_input: str) -> bool:
    lower = user_input.lower()
    return any(keyword in lower for keyword in AGENTIC_KEYWORDS)


def execute_tool(tool_name: str, task: str, arg: str = "") -> str:
    try:
        query = arg if arg else task
        if tool_name == "web_search":
            return web_search(query)
        elif tool_name == "fetch_news":
            return fetch_news(query)
        elif tool_name == "fetch_stock":
            return fetch_stock(query)
        elif tool_name == "get_weather":
            return get_weather(query)
        elif tool_name == "summarize_website":
            if query.startswith("http"):
                return summarize_website(query)
            return web_search(query)
        elif tool_name == "run_code":
            return run_code(query)
        elif tool_name == "generate_image":
            return generate_image(query)
        elif tool_name == "remember":
            return remember(query)
        elif tool_name == "recall":
            return recall(query)
        else:
            return f"Step completed: {task}"
    except Exception as e:
        return f"Tool error: {str(e)}"


def run_agentic(user_input: str) -> str:
    print(f"\n🧠 AGENTIC MODE: Planning for '{user_input}'")

    plan = create_plan(user_input)
    print(f"📋 Plan: {json.dumps(plan, indent=2)}")

    results = []
    progress = f"🧠 **AgentX Autonomous Mode**\n📋 **Goal:** {user_input}\n\n"
    progress += f"**Plan ({len(plan)} steps):**\n"

    for step in plan:
        progress += f"  {step['step']}. {step['task']}\n"

    progress += "\n**Executing...**\n\n"

    for step in plan:
        step_num = step.get('step', '?')
        task = step.get('task', '')
        tool = step.get('tool', 'web_search')
        arg = step.get('arg', '')

        print(f"\n⚡ Step {step_num}: {task} (tool: {tool}, arg: {arg})")
        progress += f"**Step {step_num}:** {task}\n"

        if tool == "none":
            result = f"Analysis step: {task}"
        else:
            result = execute_tool(tool, task, arg)

        results.append({
            "step": step_num,
            "task": task,
            "tool": tool,
            "result": result[:500]
        })

        progress += f"✅ Done\n\n"
        print(f"✅ Result: {result[:100]}...")

    print("\n📝 Generating final report...")
    final_report = summarize_results(user_input, results)

    return progress + "---\n\n" + final_report


def run_agent(user_input: str, context: ContextManager) -> str:
    if is_agentic_task(user_input):
        return run_agentic(user_input)

    context.add_user_message(user_input)
    called_tools = set()

    for iteration in range(MAX_ITERATIONS):
        message = call_llm(context.get_messages(), TOOLS)

        if message.tool_calls:
            context.add_assistant_with_tools(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"\n🔧 Tool: {tool_name} | Args: {tool_args}")

                tool_key = f"{tool_name}_{str(tool_args)}"
                if tool_key in called_tools:
                    result = "Tool already called with same arguments."
                elif tool_name in TOOL_MAP:
                    called_tools.add(tool_key)
                    result = TOOL_MAP[tool_name](**tool_args)
                else:
                    result = f"Unknown tool: {tool_name}"

                print(f"✅ Result: {result[:200]}...")
                context.add_tool_result(tool_call.id, result)

                if tool_name in ["run_code", "convert_currency", "get_weather",
                                  "fetch_stock", "analyze_data", "remember",
                                  "recall", "forget", "generate_image"]:
                    context.add_assistant_message(result)
                    return result

        else:
            final_response = message.content or "Koi response nahi mila."
            context.add_assistant_message(final_response)
            return final_response

    return "Max iterations reach ho gayi."