# Agent Harness - HybridRPA Orchestrator

An asynchronous Python agent harness designed to act as an intelligent orchestrator for the **HybridRPA** platform. It supports autonomous tool calling, long-term memory persistence, and standard **Model Context Protocol (MCP)** server integration.

---

## 🚀 Features

- **Asynchronous Agent Loop**: Built on Python `asyncio` and `AsyncOpenAI` for responsive multi-turn interactions.
- **Native Workspace Tools**:
  - `wd`: Get current workspace directory.
  - `read_workspace`: List all files inside the workspace.
  - `create_file`: Create and write content to files in the workspace.
  - `read_file`: Inspect contents of files in the workspace.
  - `get_datetime`: Retrieve real-time timestamp information.
- **Long-Term Memory**:
  - Automatically loads and appends user preferences, project context, and personal info to `memory.md`.
- **Model Context Protocol (MCP) Integration**:
  - Dynamically discovers and connects to external MCP servers (such as `mcp-server-fetch`) via standard `stdio` communication.
- **OpenAI-Compatible Backend**: Works with OpenAI, Groq, OpenRouter, Ollama, or any OpenAI-compatible API.

---

## 📁 Project Structure

```text
.
├── main.py              # CLI entry point and async chat session loop
├── utils.py             # Agent runtime, tool resolver, and chat handler
├── tool.py              # Tool definitions, schemas, MCP connectors, memory logic
├── memory.md            # Persistent long-term memory store
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment configuration
├── .gitignore           # Git ignore rules
└── workspace/           # Workspace directory for agent file operations
```

---

## 🛠️ Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (for running external MCP servers like `mcp-server-fetch`)

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd "Agent Harness"
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and fill in your credentials:
     ```env
     OPENAI_API_KEY=your_actual_api_key_here
     OPENAI_API_BASE=https://api.groq.com/openai/v1
     GPT_MODEL=openai/gpt-oss-120b
     ```

---

## 🏃 Usage

Run the agent via:

```bash
python main.py
```

Interact directly in the terminal:
```text
Connected to MCP server: fetch with tools: ['fetch']
You: Tạo file test.txt với nội dung Hello World
Calling tool: create_file ({'filename': 'test.txt', 'content': 'Hello World'})
File created: D:\Project\Agent Harness\workspace\test.txt
Orchestrator: Mình đã tạo file test.txt thành công trong workspace cho bạn rồi nhé!
```

To exit, press `Ctrl + C`.

