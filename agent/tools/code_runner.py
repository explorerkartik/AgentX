import subprocess
import tempfile
import os

def run_code(code: str, language: str = "python") -> str:
    try:
        if language.lower() == "python":
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )

            os.unlink(temp_file)

            output = result.stdout if result.stdout else "No output"
            error = result.stderr if result.stderr else ""

            # Code aur output dono return karo
            response = f"```python\n{code}\n```\n\nOutput:\n{output}"
            if error:
                response += f"\nErrors:\n{error}"

            return response
        else:
            return "Abhi sirf Python supported hai."

    except subprocess.TimeoutExpired:
        return "Error: Code 30 seconds mein complete nahi hua (timeout)."
    except Exception as e:
        return f"Code run error: {str(e)}"


CODE_RUNNER_TOOL = {
    "type": "function",
    "function": {
        "name": "run_code",
        "description": "Write and execute Python code. Always write complete working code.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Complete Python code to execute"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language (default: python)",
                    "default": "python"
                }
            },
            "required": ["code"]
        }
    }
}