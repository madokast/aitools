"""
数学计算的 mcp，用于测试


"""

from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP server
mcp = FastMCP("math")

mcp_config = { # type: ignore
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "--directory",
                Path(__file__).parent.absolute().as_posix(),
                "run",
                Path(__file__).name,
            ]
        }
    }
}

print(f"mcp_config: {mcp_config}")

@mcp.tool("add", description="Add two numbers")
def add(a: str, b: str) -> str:
    """
    Add two numbers
    """
    a = a.strip().replace(",", "")
    b = b.strip().replace(",", "")

    if a.isdigit() and b.isdigit():
        return str(int(a) + int(b))
    
    try:
        a_float = float(a)
    except ValueError:
        return f"Invalid number: {a}"

    try:
        b_float = float(b)
    except ValueError:
        return f"Invalid number: {b}"
    
    return str(a_float + b_float)

@mcp.tool("multiply", description="Multiply two numbers")
def multiply(a: str, b: str) -> str:
    """
    Multiply two numbers
    """
    a = a.strip().replace(",", "")
    b = b.strip().replace(",", "")

    if a.isdigit() and b.isdigit():
        return str(int(a) * int(b))
    
    try:
        a_float = float(a)
    except ValueError:
        return f"Invalid number: {a}"

    try:
        b_float = float(b)
    except ValueError:
        return f"Invalid number: {b}"
    
    return str(a_float * b_float)

if __name__ == "__main__":
    mcp.run(transport='stdio')

