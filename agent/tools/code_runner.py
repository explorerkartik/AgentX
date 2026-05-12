import subprocess
import tempfile
import os
import re

def run_code(code: str) -> str:
    try:
        # Clean code - remove markdown formatting
        code = re.sub(r'```python\n?', '', code)
        code = re.sub(r'```\n?', '', code)
        code = code.strip()
        
        # Replace input() with default value
        code = re.sub(r'input\([^)]*\)', '"10"', code)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        os.unlink(temp_file)

        if result.returncode == 0:
            return f"```python\n{code}\n```\n\nOutput: {result.stdout.strip()}" if result.stdout else f"```python\n{code}\n```\n\nCode executed successfully."
        else:
            return f"```python\n{code}\n```\n\nErrors: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "❌ Code timeout — 10 seconds se zyada lag raha hai."
    except Exception as e:
        return f"Code execution error: {str(e)}"


CODE_RUNNER_TOOL = {
    "type": "function",
    "function": {
        "name": "run_code",
        "description": "Write and execute Python code. Always use this to run Python programs.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute. Raw Python only, no markdown formatting."
                }
            },
            "required": ["code"]
        }
    }
}