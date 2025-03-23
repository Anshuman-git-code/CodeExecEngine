import os
from docker_executor import execute_in_container

def execute_code(code, language):
    # Security: Block dangerous imports and commands
    restricted_keywords = ["import os", "import subprocess", "exec", "eval", "open"]
    if any(keyword in code for keyword in restricted_keywords):
        return {"stdout": "", "stderr": "Restricted code detected!", "exit_code": 1}

    return execute_in_container(code, language)
