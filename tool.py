from pathlib import Path
import datetime

from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SYSTEM_PROMPT = (
    "You are a helpful assistant/coordinator named Orchestrator. Your goal is to create BPMN workflows, "
    "manage them, or provide support for users on our platform HybridRPA. "
    "HybridRPA is a platform that allows users to create BPMN Workflows to transform BPMN into RPA code. "
    "The default language is Vietnamese, depending on the user's input.\n\n"
    "IMPORTANT MEMORY RULE:\n"
    "- Whenever the user shares ANY personal information (name, hobbies, likes, dislikes, habits, role, or preferences), "
    "you MUST AUTOMATICALLY and IMMEDIATELY call the `save_memory` tool to save it WITHOUT asking for permission first.\n"
    "- Do NOT save information that is already present in the memory below.\n"
    "- Here is what you currently remember from the memory file:\n{memory}"
)


p = Path(__file__).parent / "workspace"
p.mkdir(parents=True, exist_ok=True)

#Memory
mem = Path(__file__).parent / "memory.md"

def load_memory() -> str:
    if mem.is_file():
        return mem.read_text(encoding="utf-8", errors="replace")
    return "Not yet"
def save_memory(content:str) -> str:
    with mem.open("a", encoding="utf-8", errors="replace") as f:
        f.write(content + "\n")
    return f"Memory saved: {content}"
#MCP 
MCP_SERVER = {
    "fetch": StdioServerParameters(command="uvx", args=["mcp-server-fetch"])
}
mcp_session: dict[str, ClientSession] = {}
async def connect_mcp(stack: AsyncExitStack):
    for name,params in MCP_SERVER.items():
        read,write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()

        tools = (await session.list_tools()).tools
        for tool in tools:
            mcp_session[tool.name] = session
            TOOLS_DESCRIPTION.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema
                    }
                }
            )
        print(f"Connected to MCP server: {name} with tools: {[tool.name for tool in tools]}")

#Tool
def wd():
    return str(p)
def read_workspace():
    files = []
    for f in p.iterdir():
        if f.is_file():
            files.append(f.name)
    return files

def create_file(filename, content):
    filepath = p / filename
    with open(filepath, "w", encoding="utf-8", errors="replace") as f:
        f.write(content or "")
    return f"File created: {filepath}"   
def read_file(filename): 
    filepath = p / filename
    
    if filepath.exists() and filepath.is_file():
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    else:
        return None
def get_datetime():
    return datetime.datetime.now()

#Tool Content

TOOLS = {
    "wd": wd,
    "read_workspace": read_workspace,
    "create_file": create_file,
    "read_file": read_file,
    "get_datetime": get_datetime,
    "save_memory": save_memory
}

TOOLS_DESCRIPTION = [
    {
        "type": "function",
        "function": {
            "name": "wd",
            "description": "Returns the current working directory of the workspace.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_workspace",
            "description": "Reads all files in the workspace and returns their contents.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Creates a new file in the workspace with the specified content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to create."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file."
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specific file in the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Returns the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "Saves content to the memory file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to save."
                    }
                },
                "required": ["content"]
            }
        }
    }
]
        


