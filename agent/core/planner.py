import json
from agent.core.llm import call_llm

def create_plan(goal: str) -> list:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a planning AI. Break down the user's goal into clear executable steps.\n"
                "Respond ONLY with a JSON array like this:\n"
                '[\n'
                '  {"step": 1, "task": "Search Tesla latest news", "tool": "web_search", "arg": "Tesla company news 2025"},\n'
                '  {"step": 2, "task": "Fetch Tesla stock price", "tool": "fetch_stock", "arg": "TSLA"},\n'
                '  {"step": 3, "task": "Get Tesla news articles", "tool": "fetch_news", "arg": "Tesla"},\n'
                '  {"step": 4, "task": "Summarize Tesla website", "tool": "summarize_website", "arg": "https://www.tesla.com"},\n'
                '  {"step": 5, "task": "Compile final report", "tool": "none", "arg": ""}\n'
                ']\n\n'
                "RULES:\n"
                "- 'arg' must be the EXACT value to pass to the tool\n"
                "- For fetch_stock: arg must be stock symbol like TSLA, AAPL, RELIANCE.NS\n"
                "- For fetch_news: arg must be short topic like 'Tesla', 'AI', 'Cricket'\n"
                "- For web_search: arg must be a good search query\n"
                "- For summarize_website: arg must be a real URL starting with https://\n"
                "- For get_weather: arg must be city name\n"
                "- For generate_image: arg must be image description\n"
                "- For none/summarize steps: arg must be empty string\n"
                "- Keep steps between 3-6\n"
                "Available tools: web_search, fetch_news, fetch_stock, get_weather, "
                "convert_currency, summarize_website, run_code, generate_image, remember, recall, none"
            )
        },
        {
            "role": "user",
            "content": f"Create a plan to: {goal}"
        }
    ]

    response = call_llm(messages)
    text = response.content or "[]"

    try:
        start = text.find('[')
        end = text.rfind(']') + 1
        if start != -1 and end > start:
            plan = json.loads(text[start:end])
            return plan
    except:
        pass

    return [{"step": 1, "task": goal, "tool": "web_search", "arg": goal}]


def summarize_results(goal: str, results: list) -> str:
    results_text = "\n\n".join([
        f"Step {r['step']} - {r['task']}:\n{r['result']}"
        for r in results
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "You are a report writer. Compile the given step results into a "
                "clear, well-structured final report. Use markdown formatting with "
                "headers, bullet points. Be comprehensive but concise."
            )
        },
        {
            "role": "user",
            "content": f"Goal: {goal}\n\nResults:\n{results_text}\n\nWrite a detailed final report."
        }
    ]

    response = call_llm(messages)
    return response.content or "Report generate nahi hua."