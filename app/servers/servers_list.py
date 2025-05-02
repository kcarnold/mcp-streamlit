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
    )
}
