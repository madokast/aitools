
import anyio
from madokast.tools.mcp.word_mcp import mcp as word_mcp
from madokast.tools.mcp.life_log_mcp import mcp as life_log_mcp

# async def run():
#     """
#     启动 MCP 服务器
#     """
#     async with anyio.create_task_group() as tg:
#         tg.start_soon(word_mcp.run_sse_async)
#         tg.start_soon(life_log_mcp.run_sse_async)


anyio.run(word_mcp.run_sse_async)

