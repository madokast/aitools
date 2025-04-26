"""
math 调用测试服务器

运行方法 python -m madokast.tools.client.math_client
"""

# 加载 .env 中的环境变量
from dotenv import load_dotenv
load_dotenv()

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o")



async def main():
    print("Start math client")

    server_params = StdioServerParameters(
        command = r"D:\apps\python313\Scripts\uv.exe",
        # Make sure to update to the full absolute path to your math_server.py file
        args = [
            "--directory",
            r"C:\other_programs\siyuan\aitools"
            "run"
            "-m"
            "madokast.tools.server.math_server"
        ],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)

            agent_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
            print(agent_response['messages'][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

