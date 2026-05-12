from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

def call_llm(messages, tools=None):
    for model in MODELS:
        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": 1024,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"

            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message
        except Exception as e:
            if "rate_limit" in str(e).lower():
                print(f"⚠️ {model} rate limited, trying next model...")
                continue
            raise e
    raise Exception("All models rate limited. Wait karo ya kal try karo.")