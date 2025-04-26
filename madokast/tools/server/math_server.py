"""
测试用的工具，实现加法和乘法

运行方法 python -m madokast.tools.server.math_server
"""

from mcp.server.fastmcp import FastMCP
from madokast.utils.logging_init import logger

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    logger.debug(f"MAP calling add {a} {b}")
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    logger.debug(f"MAP calling multiply {a} {b}")
    return a * b

# @mcp.prompt()
# def configure_assistant(skills: str) -> list[dict]:
#     return [
#         {
#             "role": "assistant",
#             "content": f"You are a helpful assistant. You have the following skills: {skills}. Always use only one tool at a time.",
#         }
#     ]

if __name__ == "__main__":
    logger.debug("Start math server")
    mcp.run(transport="stdio")

