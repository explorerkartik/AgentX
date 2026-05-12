import sys
import os

# Path fix
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core.agent_loop import run_agent
from agent.core.context import ContextManager


def main():
    print("=" * 50)
    print("🤖 Welcome to AgentX — Your Personal AI Agent")
    print("=" * 50)
    print("Commands: 'exit' to quit | 'clear' to reset chat")
    print("=" * 50)

    context = ContextManager(system_prompt=None)

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("👋 AgentX band ho raha hai. Alvida!")
                break

            if user_input.lower() == "clear":
                context = ContextManager(system_prompt=None)
                print("🗑️ Chat history clear ho gayi!")
                continue

            print("\n🤖 AgentX soch raha hai...\n")
            response = run_agent(user_input, context)
            print(f"🤖 AgentX: {response}")

        except KeyboardInterrupt:
            print("\n👋 AgentX band ho raha hai. Alvida!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()