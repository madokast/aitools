"""
人生日志 MCP 服务
"""

import requests
from mcp.server.fastmcp import FastMCP
from madokast.utils.env import get_env

# 初始化 FastMCP server
mcp = FastMCP("life-log", host="0.0.0.0", port=int(get_env("LIFE_LOG_MCP_PORT")))

IP = "localhost"
PORT = 8000

@mcp.tool("describe", description="Get the description of the life log service")
def describe() -> str:
    response = requests.post(f"http://{IP}:{PORT}/describe", json={}, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to get description: {response.status_code} {response.reason}"

@mcp.tool("add", description="Add a life log entry")
def add_log(object: dict) -> str:
    """
    添加一条人生日志
    """
    response = requests.post(f"http://{IP}:{PORT}/add", json=object, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to add log: {response.status_code} {response.reason}"
    
@mcp.tool("query", description="Query life logs by SQL. The table name is daily_log")
def query(sql: str) -> str:
    """
    查询人生日志
    """
    response = requests.post(f"http://{IP}:{PORT}/query", json={"SQL": sql}, headers={"Content-Type": "application/sql"})
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to query logs: {response.status_code} {response.reason}"

@mcp.tool("now", description="Get the current time")
def now() -> str:
    """
    获取当前时间
    """
    from datetime import datetime
    now = datetime.now()
    return now.isoformat()

if __name__ == "__main__":
    mcp.run(transport='stdio')

