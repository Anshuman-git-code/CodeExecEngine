from flask import Flask, request, jsonify
from flask_cors import CORS
from runner import execute_code
import re

app = Flask(__name__)
CORS(app)

# Security: Block dangerous patterns
restricted_patterns = [
    r"import os",
    r"import subprocess",
    r"exec\(.*\)",
    r"eval\(.*\)",
    r"open\(.*\)",
    r"dns",
    r"process.env",
]

@app.route("/run", methods=["POST"])
def run_code():
    print("📥 Received a request at /run")  # Debugging step 1

    data = request.get_json()
    print(f"🔍 Raw request data: {data}")  # Debugging step 2

    if not data or "code" not in data or "language" not in data:
        print("⚠️ Invalid request data")  # Debugging step 3
        return jsonify({"stderr": "Invalid request"}), 400

    code = data["code"]
    language = data["language"]

    print(f"✅ Extracted code:\n{code}")  # Debugging step 4
    print(f"✅ Extracted language: {language}")  # Debugging step 5

    # Block dangerous code
    for pattern in restricted_patterns:
        if re.search(pattern, code):
            print("🚫 Restricted code detected!")  # Debugging step 6
            return jsonify({"stderr": "Restricted code detected!"}), 400

    print("🚀 Sending code for execution...")  # Debugging step 7
    result = execute_code(code, language)

    print(f"🎯 Execution Result: {result}")  # Debugging step 8
    return jsonify(result)

if __name__ == "__main__":
    print("🔥 Flask server is starting...")
    app.run(host="0.0.0.0", port=5001)