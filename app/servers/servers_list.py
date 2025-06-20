import os

from mcp import StdioServerParameters


server_list = {
    "weather": StdioServerParameters(
        command="python",
        args=["app/servers/weather_server.py"],
        env=None
    ),
    "mcp_server_fetch": StdioServerParameters(
        command="python",
        args=["-m", "mcp_server_fetch"],
        env=None,
    ),
    "github": StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-github"
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
        }
    ),
}
