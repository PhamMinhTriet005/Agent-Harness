from openai import AsyncOpenAI
import os
from tool import *
import json
from dotenv import load_dotenv
load_dotenv(override=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_API_BASE")
                    )


def check_env_vars():
    if (os.getenv("OPENAI_API_KEY") is None) or (os.getenv("OPENAI_API_BASE") is None) or (os.getenv("GPT_MODEL") is None):
        raise ValueError("Please set the OPENAI_API_KEY, OPENAI_API_BASE, and GPT_MODEL environment variables in the .env file.")

async def resolve_tool(name: str, args: dict):
    if name in TOOLS:
        return TOOLS[name](**args)
    result =  await mcp_session[name].call_tool(name,args)
    return result.content
async def chat(user_input:str) -> str: 
    messages = [
            
            {"role": "system", "content": SYSTEM_PROMPT.format(memory=load_memory())},
            {"role": "user", "content": user_input},
        ]
    while True:
        response = await client.chat.completions.create(
            messages=messages,
            model = os.getenv("GPT_MODEL"),
            tools= TOOLS_DESCRIPTION
            )
        message = response.choices[0].message
        if not message.tool_calls: 
            return message.content
        messages.append(message)
        for call in message.tool_calls:
            args =  json.loads(call.function.arguments or "{}")
            print("\033[92m {}\033[00m".format(f"Calling tool: {call.function.name} ({args})"))
            result = await resolve_tool(call.function.name, args)
            print(result)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
            