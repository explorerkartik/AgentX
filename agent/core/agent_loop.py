import json
from agent.core.llm import call_llm
from agent.core.context import ContextManager
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
from agent.tools.voice import listen_voice, speak_text, LISTEN_TOOL, SPEAK_TOOL

SYSTEM_PROMPT = (
    "You are AgentX, a powerful AI assistant that can:\n"
    "1. Search the web for current information\n"
    "2. Write and execute Python code\n"
    "3. Analyze files (PDF, Word, text, code)\n"
    "4. Fetch latest news and stock prices\n"
    "5. Get current weather for any city\n"
    "6. Summarize any website or URL\n"
    "7. Convert currencies with live rates\n"
    "8. Analyze CSV and Excel data files\n"
    "9. Remember and recall information across sessions\n"
    "10. Generate AI images from text descriptions\n"
    "11. Listen to voice input and speak responses\n\n"
    "IMPORTANT RULES:\n"
    "- Call each tool ONLY ONCE per task\n"
    "- Do NOT repeat the same tool with same arguments\n"
    "- After getting tool result, give final answer immediately\n"
    "- Be concise and direct in responses\n"
    "- When user shares personal info (name, preferences), use 'remember' tool automatically\n"
    "- When asked about past info, use 'recall' tool\n"
    "- When asked to write code, ALWAYS show code block first then output\n"
    "- NEVER explain code in prose, ALWAYS show the actual code block first\n"
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
    IMAGE_GEN_TOOL,
    LISTEN_TOOL,
    SPEAK_TOOL
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
    "generate_image": generate_image,
    "listen_voice": listen_voice,
    "speak_text": speak_text
}

MAX_ITERATIONS = 5


def run_agent(user_input: str, context: ContextManager) -> str:
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
                    result = "Tool already called with same arguments. Use the previous result."
                elif tool_name in TOOL_MAP:
                    called_tools.add(tool_key)
                    result = TOOL_MAP[tool_name](**tool_args)
                else:
                    result = f"Unknown tool: {tool_name}"

                print(f"✅ Result: {result[:200]}...")

                context.add_tool_result(tool_call.id, result)

                if tool_name in ["run_code", "convert_currency", "get_weather", "fetch_stock", "analyze_data", "remember", "recall", "forget", "generate_image", "listen_voice", "speak_text"]:
                    context.add_assistant_message(result)
                    return result

        else:
            final_response = message.content or "Koi response nahi mila."
            context.add_assistant_message(final_response)
            return final_response

    return "Max iterations reach ho gayi. Task complete nahi hua."