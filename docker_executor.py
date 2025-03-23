import subprocess
import uuid
import os

# Directory to store temporary code files
SANDBOX_DIR = "/tmp/sandbox"
os.makedirs(SANDBOX_DIR, exist_ok=True)

LANGUAGE_CONFIG = {
    "python": {
        "image": "python:3.9",
        "run_cmd": "python3 /sandbox/script.py"
    },
    "c": {
        "image": "gcc:latest",
        "compile_cmd": "gcc /sandbox/script.c -o /sandbox/a.out",
        "run_cmd": "/sandbox/a.out"
    },
    "javascript": {
        "image": "node:latest",
        "run_cmd": "node /sandbox/script.js"
    }
}

# Block dangerous code
RESTRICTED_KEYWORDS = {
    "python": ["import os", "import subprocess", "exec(", "eval(", "open("],
    "c": ["system(", "popen(", "exec("],
    "javascript": ["require('fs')", "require(\"fs\")", "child_process", "process.env"]
}

def execute_in_container(code, language):
    if language not in LANGUAGE_CONFIG:
        return {"stdout": "", "stderr": f"Unsupported language: {language}", "exit_code": 1}

    # Check for restricted keywords before execution
    for keyword in RESTRICTED_KEYWORDS.get(language, []):
        if keyword in code:
            return {"stdout": "", "stderr": "Restricted code detected!", "exit_code": 1}

    file_uuid = str(uuid.uuid4())
    extension = {"python": "py", "c": "c", "javascript": "js"}[language]
    filename = f"script.{extension}"
    source_path = os.path.join(SANDBOX_DIR, filename)

    # Write code to file
    with open(source_path, "w") as f:
        f.write(code)

    # Docker container setup
    lang_config = LANGUAGE_CONFIG[language]
    container_name = f"runner_{file_uuid}"

    # Docker run command (Auto-remove container after execution)
    docker_cmd = f"docker run --rm -v {SANDBOX_DIR}:/sandbox --name {container_name} {lang_config['image']} /bin/sh -c"

    # Compilation (if needed)
    if "compile_cmd" in lang_config:
        compile_cmd = f'"{lang_config["compile_cmd"]} && {lang_config["run_cmd"]}"'
    else:
        compile_cmd = f'"{lang_config["run_cmd"]}"'

    # ✅ Try running the command with a timeout
    print(f"Executing: {docker_cmd} {compile_cmd}")  # Debugging line

    try:
        process = subprocess.run(
            f"{docker_cmd} {compile_cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        print("Execution Completed!")  # Debugging line
        print("STDOUT:", process.stdout)
        print("STDERR:", process.stderr)
        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode
        }
    except subprocess.TimeoutExpired:
        print("Execution Timed Out!")  # Debugging line
        subprocess.run(f"docker rm -f {container_name}", shell=True)
        return {"stdout": "", "stderr": "Execution timed out", "exit_code": 124}