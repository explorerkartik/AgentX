from agent.core.llm import call_llm
from agent.tools.web_search import web_search, WEB_SEARCH_TOOL
from agent.tools.api_fetcher import fetch_news, FETCH_NEWS_TOOL
from agent.tools.web_summarizer import summarize_website, WEB_SUMMARIZER_TOOL
import json

RESEARCHER_SYSTEM = """You are a Research Agent. Your job is to:
- Search the web for information
- Fetch latest news
- Summarize websites
- Return detailed, factual research results

Always return comprehensive research data. Be thorough and detailed."""

RESEARCHER_TOOLS = [WEB_SEARCH_TOOL, FETCH_NEWS_TOOL, WEB_SUMMARIZER_TOOL]

RESEARCHER_TOOL_MAP = {
    "web_search": web_search,
    "fetch_news": fetch_news,
    "summarize_website": summarize_website
}

def run_researcher(task: str) -> str:
    print(f"\n🔍 Researcher Agent: {task}")
    messages = [
        {"role": "system", "content": RESEARCHER_SYSTEM},
        {"role": "user", "content": task}
    ]

    for _ in range(3):
        message = call_llm(messages, RESEARCHER_TOOLS)

        if message.tool_calls:
            messages.append({"role": "assistant", "content": message.content or "", "tool_calls": [
                {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in message.tool_calls
            ]})

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                result = RESEARCHER_TOOL_MAP.get(tool_name, lambda **k: "Unknown tool")(**tool_args)
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
        else:
            return message.content or "No research found."

    return "Research complete."