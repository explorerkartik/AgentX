class ContextManager:
    def __init__(self, system_prompt: str = None):
        self.messages = []
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

    def add_user_message(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def add_assistant_message(self, content: str):
        self.messages.append({
            "role": "assistant",
            "content": content
        })

    def add_tool_result(self, tool_call_id: str, result: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result
        })

    def add_assistant_with_tools(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in (message.tool_calls or [])
            ]
        })

    def get_messages(self) -> list:
        return self.messages

    def clear(self):
        system = self.messages[0] if self.messages and self.messages[0]["role"] == "system" else None
        self.messages = [system] if system else []