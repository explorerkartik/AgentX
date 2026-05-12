import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def generate_image(prompt: str) -> str:
    try:
        API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}

        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=60
        )

        if response.status_code != 200:
            return f"Image generation error: {response.text}"

        os.makedirs("static/generated", exist_ok=True)
        count = len(os.listdir("static/generated"))
        filename = f"static/generated/img_{count}.png"

        with open(filename, "wb") as f:
            f.write(response.content)

        return f"Image generated!\nSaved at: {filename}\nPrompt: {prompt}"

    except Exception as e:
        return f"Image generation error: {str(e)}"


IMAGE_GEN_TOOL = {
    "type": "function",
    "function": {
        "name": "generate_image",
        "description": "Generate an AI image from a text description/prompt.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed description of the image to generate"
                }
            },
            "required": ["prompt"]
        }
    }
}