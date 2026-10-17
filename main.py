
from utils import *
import os
import asyncio

async def main():
    async with AsyncExitStack() as stack:
        await connect_mcp(stack)
        try:
            while True:
                user_input = await asyncio.to_thread(input, "You: ")
                print("Orchestrator: ", await chat(user_input))
        except (KeyboardInterrupt, EOFError, asyncio.CancelledError):
            print("\nExiting...")


if __name__ == "__main__":
    check_env_vars()
    asyncio.run(main())