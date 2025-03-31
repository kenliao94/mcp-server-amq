from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
import ssl
from .models import (
    DescribeBroker,
)
from .logger import Logger, LOG_LEVEL
from .handlers import handle_describe_broker


async def serve() -> None:
    # Setup server
    server = Server("mcp-amq")
    # Setup logger
    is_log_level_exception = False
    try:
        log_level = LOG_LEVEL[log_level]
    except Exception:
        is_log_level_exception = True
        log_level = LOG_LEVEL.WARNING
    logger = Logger("server.log", log_level)
    if is_log_level_exception:
        logger.warning("Wrong log_level received. Default to WARNING")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="describe_broker",
                description="""Describe the broker status deployed on AmazonMQ""",
                inputSchema=DescribeBroker.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str,
        arguments: dict
    ) -> list[TextContent]:
        if name == "describe_broker":
            logger.debug("Executing describe_broker tool")
            broker_id = arguments["broker_id"]
            region = arguments["region"]
            try:
                result = handle_describe_broker(broker_id=broker_id, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]
        raise ValueError(f"Tool not found: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
