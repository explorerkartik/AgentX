import subprocess
import tempfile
import os

def run_code(code: str) -> str:
    try:
        import re
        # Replace input() with default values
        code = re.sub(r'input\([^)]*\)', '"10"', code)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
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
            return f"Output: {result.stdout}" if result.stdout else "Code executed successfully."
        else:
            return f"Output: {result.stdout}\nErrors: {result.stderr}"

    except Exception as e:
        return f"Code execution error: {str(e)}"

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