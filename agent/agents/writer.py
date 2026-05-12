from agent.core.llm import call_llm

WRITER_SYSTEM = """You are a Writer Agent. Your job is to:
- Take research data and write clear, professional content
- Create well-structured reports, summaries, and articles
- Use proper headings, bullet points, and formatting
- Make content engaging and easy to read

Always produce high-quality, well-formatted written content."""

def run_writer(task: str, research_data: str) -> str:
    print(f"\n✍️ Writer Agent: Writing content...")
    messages = [
        {"role": "system", "content": WRITER_SYSTEM},
        {"role": "user", "content": f"Task: {task}\n\nResearch Data:\n{research_data}\n\nWrite a detailed, well-structured response based on this research."}
    ]

    message = call_llm(messages)
    return message.content or "No content generated."