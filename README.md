 CodeExecEngine

A secure code execution service that runs user code in isolated Docker containers. CodeExecEngine allows users to write and execute code in Python, C, and JavaScript within a sandboxed environment.


 🌟 Features

- Secure Execution: Runs code in isolated Docker containers that are destroyed after execution
- Multi-language Support: Execute Python, C, and JavaScript code
- Real-time Output: See execution results immediately
- Security Restrictions: Prevents dangerous operations by filtering restricted keywords
- Clean UI: Simple and intuitive interface for writing and executing code

 🔧 How It Works

CodeExecEngine uses a Flask backend API that receives code from the frontend, validates it for security, and then executes it within a Docker container. The execution happens in complete isolation from the host system, ensuring security and preventing any potentially harmful operations.

The architecture consists of:
1. React Frontend: User interface for writing code and viewing results
2. Flask Backend API: Processes requests and manages code execution
3. Docker Integration: Creates isolated containers for each code execution

 📋 Requirements

- Python 3.9 or higher
- Docker engine installed and running
- Node.js 16+ (for frontend development)
- npm or yarn (for frontend package management)

 🚀 Installation

Backend Setup:

1. Clone the repository:
```bash
git clone https://github.com/Anshuman-git-code/CodeExecEngine.git
cd CodeExecEngine
```

2. Install Python requirements:
```bash
pip install -r requirements.txt
```

3. Make sure Docker is running on your system

4. Start the Flask backend:
```bash
python app.py
```

The backend will run on http://localhost:5001

Frontend Setup:

1. Navigate to the frontend directory:
```bash
cd ces-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

🔒 Security

CodeExecEngine prioritizes security through multiple layers:

1. Containerization: Each code execution occurs in a separate Docker container
2. Automatic Cleanup: Containers are removed immediately after execution
3. Keyword Filtering: Dangerous operations and imports are blocked
4. Resource Limits: Execution time and memory are limited
5. Read-only Execution: Code cannot modify the host system

💻 Usage

1. Select a programming language from the dropdown (Python, C, or JavaScript)
2. Write or paste your code in the editor
3. Click "Run Code" to execute
4. View the output in the results section
5. Copy the output if needed

📖 API Documentation

The backend exposes a simple REST API:

Execute Code
```
POST /run

Request Body:
{
  "code": "your code here",
  "language": "python|c|javascript"
}

Response:
{
  "stdout": "program output",
  "stderr": "error messages if any",
  "exit_code": 0
}
```
