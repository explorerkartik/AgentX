import subprocess
import tempfile
import os

def run_code(code: str, language: str = "python") -> str:
    try:
        if language.lower() == "python":
            # Temp file mein code save karo
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name

            # Run karo with timeout
            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )

            os.unlink(temp_file)  # Temp file delete karo

            output = ""
            if result.stdout:
                output += f"Output:\n{result.stdout}"
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
            
            return output if output else "Code run hua, koi output nahi."

        else:
            return f"Abhi sirf Python supported hai."

    except subprocess.TimeoutExpired:
        return "Error: Code 30 seconds mein complete nahi hua (timeout)."
    except Exception as e:
        return f"Code run error: {str(e)}"


# Tool spec for LLM
CODE_RUNNER_TOOL = {
    "type": "function",
    "function": {
        "name": "run_code",
        "description": "Write and execute Python code. Use this to solve problems, do calculations, data analysis, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute"
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