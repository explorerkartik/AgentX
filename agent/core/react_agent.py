import json
from agent.core.llm import call_llm
from agent.tools.web_search import web_search
from agent.tools.code_runner import run_code
from agent.tools.api_fetcher import fetch_news, fetch_stock
from agent.tools.weather import get_weather
from agent.tools.web_summarizer import summarize_website
from agent.tools.currency import convert_currency
from agent.tools.memory import remember, recall
from agent.tools.image_gen import generate_image

TOOL_MAP = {
    "web_search": web_search,
    "run_code": run_code,
    "fetch_news": fetch_news,
    "fetch_stock": fetch_stock,
    "get_weather": get_weather,
    "summarize_website": summarize_website,
    "convert_currency": convert_currency,
    "remember": remember,
    "recall": recall,
    "generate_image": generate_image
}

REACT_SYSTEM_PROMPT = """You are AgentX, an autonomous AI agent. You solve tasks step by step using the ReAct framework.

For EVERY response, you MUST follow this EXACT format:

Thought: [What you are thinking and planning to do next]
Action: [tool_name]
Action Input: [exact input to pass to the tool]

OR if task is complete:

Thought: [Final analysis of all results]
Final Answer: [Complete, detailed final response to the user]

Available tools:
- web_search: Search the web. Input: search query string
- run_code: Execute Python code. Input: complete Python code string
- fetch_news: Get news articles. Input: topic string
- fetch_stock: Get stock price. Input: stock symbol like TSLA, AAPL
- get_weather: Get weather. Input: city name
- summarize_website: Summarize a URL. Input: full URL with https://
- convert_currency: Convert currency. Input: JSON like {"amount": 100, "from_currency": "USD", "to_currency": "INR"}
- remember: Save to memory. Input: fact string
- recall: Get from memory. Input: query string
- generate_image: Generate image. Input: image description

RULES:
- Always think before acting
- Use observations to decide next action
- Never repeat same action with same input
- Give Final Answer only when task is fully complete
- Be thorough and autonomous
"""

def parse_react_response(text: str) -> dict:
    """ReAct response parse karo — sirf PEHLA action lo"""
    result = {
        "thought": "",
        "action": None,
        "action_input": None,
        "final_answer": None
    }

    lines = text.strip().split('\n')

    thought_lines = []
    action = None
    action_input_lines = []
    final_answer_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("Thought:") and not action:
            thought_lines.append(line[8:].strip())

        elif line.startswith("Action:") and not action:
            # Sirf PEHLA action lo
            action = line[7:].strip()

        elif line.startswith("Action Input:") and action and not result["action"]:
            result["thought"] = ' '.join(thought_lines).strip()
            result["action"] = action
            # Multi-line input support
            inp = line[13:].strip()
            action_input_lines.append(inp)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.startswith("Thought:") or next_line.startswith("Action:") or next_line.startswith("Final Answer:"):
                    break
                action_input_lines.append(next_line)
                i += 1
            result["action_input"] = '\n'.join(action_input_lines).strip()
            # Backticks remove karo
            if result["action_input"].startswith("```"):
                result["action_input"] = result["action_input"].strip('`').strip()
                if result["action_input"].startswith("python"):
                    result["action_input"] = result["action_input"][6:].strip()
            return result

        elif line.startswith("Final Answer:"):
            result["thought"] = ' '.join(thought_lines).strip()
            final_answer_lines.append(line[13:].strip())
            i += 1
            while i < len(lines):
                final_answer_lines.append(lines[i])
                i += 1
            result["final_answer"] = '\n'.join(final_answer_lines).strip()
            return result

        i += 1

    result["thought"] = ' '.join(thought_lines).strip()
    return result


def execute_action(action: str, action_input: str) -> str:
    """Action execute karo"""
    action = action.strip().lower()

    if action not in TOOL_MAP:
        return f"Unknown tool: {action}. Available: {list(TOOL_MAP.keys())}"

    try:
        if action == "convert_currency":
            try:
                args = json.loads(action_input)
                return convert_currency(**args)
            except:
                return "Error: convert_currency needs JSON input like {\"amount\": 100, \"from_currency\": \"USD\", \"to_currency\": \"INR\"}"

        elif action == "run_code":
            return run_code(action_input)

        else:
            return TOOL_MAP[action](action_input)

    except Exception as e:
        return f"Tool execution error: {str(e)}"


def run_react(user_input: str, stream_callback=None) -> str:
    """
    ReAct loop — Thought → Action → Observation → repeat
    stream_callback: optional function to stream steps to UI
    """
    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    max_steps = 10
    steps_log = []
    full_log = f"🤖 **AgentX ReAct Mode**\n📋 **Task:** {user_input}\n\n"

    print(f"\n{'='*50}")
    print(f"🚀 REACT AGENT: {user_input}")
    print(f"{'='*50}")

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        response = call_llm(messages)
        text = response.content or ""

        print(f"LLM Response:\n{text}")

        parsed = parse_react_response(text)

        # Final answer mil gaya
        if parsed["final_answer"]:
            full_log += f"**✅ Task Complete!**\n\n---\n\n{parsed['final_answer']}"
            print(f"\n✅ FINAL ANSWER: {parsed['final_answer'][:100]}...")

            if stream_callback:
                stream_callback(f"\n✅ **Complete!**")

            return full_log

        # Action execute karo
        if parsed["action"] and parsed["action_input"] is not None:
            thought = parsed["thought"]
            action = parsed["action"]
            action_input = parsed["action_input"]

            step_info = f"**Step {step+1}:**\n"
            step_info += f"💭 *{thought}*\n"
            step_info += f"🔧 **Action:** `{action}`\n"
            step_info += f"📥 **Input:** `{action_input[:100]}`\n"

            print(f"Thought: {thought}")
            print(f"Action: {action}")
            print(f"Action Input: {action_input}")

            # Tool execute karo
            observation = execute_action(action, action_input)
            obs_short = observation[:300]

            step_info += f"👁️ **Result:** {obs_short}\n\n"
            full_log += step_info
            steps_log.append({
                "step": step + 1,
                "thought": thought,
                "action": action,
                "input": action_input,
                "observation": observation
            })

            print(f"Observation: {observation[:200]}...")

            if stream_callback:
                stream_callback(step_info)

            # Messages mein add karo
            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": f"Observation: {observation}\n\nContinue with next Thought/Action or give Final Answer if task is complete."
            })

        else:
            # Format sahi nahi — ek baar retry
            print("⚠️ Format issue, retrying...")
            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": "Please follow the exact format: Thought: ... Action: ... Action Input: ... OR Final Answer: ..."
            })

    return full_log + "\n\n⚠️ Max steps reached. Partial results above."