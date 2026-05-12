from agent.core.llm import call_llm
from agent.agents.researcher import run_researcher
from agent.agents.writer import run_writer
from agent.agents.coder import run_coder

MANAGER_SYSTEM = """You are a Manager Agent that coordinates specialist agents.

You have access to these agents:
- RESEARCHER: For web search, news, and information gathering
- WRITER: For creating reports, summaries, and written content
- CODER: For writing and executing Python code

Based on the user task, decide which agents to use and in what order.
Respond ONLY with a JSON plan like this:

{
  "plan": [
    {"agent": "RESEARCHER", "task": "Search for X"},
    {"agent": "WRITER", "task": "Write a report on X"},
    {"agent": "CODER", "task": "Write code for X"}
  ]
}

Only include agents that are needed for the task."""

def run_manager(user_task: str) -> str:
    print(f"\n🎯 Manager Agent planning: {user_task}")

    messages = [
        {"role": "system", "content": MANAGER_SYSTEM},
        {"role": "user", "content": user_task}
    ]

    message = call_llm(messages)
    response = message.content or ""

    try:
        import json
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            return "Manager could not create a plan."

        plan_data = json.loads(json_match.group())
        steps = plan_data.get("plan", [])

        print(f"\n📋 Plan: {[s['agent'] for s in steps]}")

        results = {}
        final_output = ""

        for step in steps:
            agent = step.get("agent")
            task = step.get("task")

            if agent == "RESEARCHER":
                results["research"] = run_researcher(task)
                final_output = results["research"]

            elif agent == "WRITER":
                research = results.get("research", "")
                results["writing"] = run_writer(task, research)
                final_output = results["writing"]

            elif agent == "CODER":
                results["code"] = run_coder(task)
                final_output = results["code"]

        return final_output or "Task complete."

    except Exception as e:
        return f"Manager error: {str(e)}"