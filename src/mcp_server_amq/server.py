from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
    Resource,
)
import ssl
from .models import (
    DescribeBroker,
    ListBrokers,
    RebootBroker,
    UpdateBroker,
    CreateBroker,
    DeleteBroker,
    ListUsers,
    DescribeUser,
    CreateUser,
    DeleteUser,
    ListTags,
)
from .logger import Logger, LOG_LEVEL
from .handlers import (
    handle_describe_broker,
    handle_list_brokers,
    handle_reboot_broker,
    handle_update_broker,
    handle_create_broker,
    handle_delete_broker,
    handle_list_users,
    handle_describe_user,
    handle_create_user,
    handle_delete_user,
    handle_list_tags,
)
from .resources import read_doc_content
from pydantic.networks import AnyUrl

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


    @server.list_resources()
    async def list_resources() -> list[Resource]:
        return [
            Resource(
                uri="file:///doc/rabbitmq_sizing_guide.txt",
                name="AmazonMQ RabbitMQ sizing guide",
                mimeType="text/plain"
            ),
            Resource(
                uri="file:///doc/rabbitmq_best_practices.txt",
                name="AmazonMQ RabbitMQ best practices",
                mimeType="text/plain"
            ),
        ]


    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        if str(uri) == "file:///doc/rabbitmq_sizing_guide.txt":
            file_content = read_doc_content("rabbitmq_sizing_guide.txt")
            return file_content
        elif str(uri) == "file:///doc/rabbitmq_best_practices.txt":
            file_content = read_doc_content("rabbitmq_best_practices.txt")
            return file_content

        logger.error("Resource not found")
        raise ValueError("Resource not found")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="describe_broker",
                description="""Describe the broker status deployed on AmazonMQ""",
                inputSchema=DescribeBroker.model_json_schema(),
            ),
            Tool(
                name="list_brokers",
                description="""List all brokers in the specified region""",
                inputSchema=ListBrokers.model_json_schema(),
            ),
            Tool(
                name="create_broker",
                description="""Create a new broker in AmazonMQ""",
                inputSchema=CreateBroker.model_json_schema(),
            ),
            Tool(
                name="delete_broker",
                description="""Delete a broker from AmazonMQ""",
                inputSchema=DeleteBroker.model_json_schema(),
            ),
            Tool(
                name="reboot_broker",
                description="""Reboot a broker in AmazonMQ""",
                inputSchema=RebootBroker.model_json_schema(),
            ),
            Tool(
                name="update_broker",
                description="""Update a broker's configuration in AmazonMQ""",
                inputSchema=UpdateBroker.model_json_schema(),
            ),
            Tool(
                name="list_users",
                description="""List all users for a broker in AmazonMQ""",
                inputSchema=ListUsers.model_json_schema(),
            ),
            Tool(
                name="describe_user",
                description="""Describe a specific user of a broker in AmazonMQ""",
                inputSchema=DescribeUser.model_json_schema(),
            ),
            Tool(
                name="create_user",
                description="""Create a new user for a broker in AmazonMQ""",
                inputSchema=CreateUser.model_json_schema(),
            ),
            Tool(
                name="delete_user",
                description="""Delete a user from a broker in AmazonMQ""",
                inputSchema=DeleteUser.model_json_schema(),
            ),
            Tool(
                name="list_tags",
                description="""List all tags for a given resource in AmazonMQ""",
                inputSchema=ListTags.model_json_schema(),
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

        elif name == "list_brokers":
            logger.debug("Executing list_brokers tool")
            region = arguments["region"]
            try:
                result = handle_list_brokers(region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "create_broker":
            logger.debug("Executing create_broker tool")
            engine_type = arguments["engine_type"]
            if engine_type == "ACTIVEMQ":
                return [TextContent(type="text", text=str("Fail. Creating an ActiveMQ broker is not supported."))]
            broker_name = arguments["broker_name"]
            engine_version = arguments["engine_version"]
            host_instance_type = arguments["host_instance_type"]
            region = arguments["region"]
            deployment_mode = arguments.get("deployment_mode", "SINGLE_INSTANCE")
            publicly_accessible = arguments.get("publicly_accessible", True)
            auto_minor_version_upgrade = arguments.get("auto_minor_version_upgrade", True)
            username = arguments["username"]
            password = arguments["password"]
            
            try:
                result = handle_create_broker(
                    broker_name=broker_name,
                    engine_type=engine_type,
                    engine_version=engine_version,
                    host_instance_type=host_instance_type,
                    deployment_mode=deployment_mode,
                    publicly_accessible=publicly_accessible,
                    auto_minor_version_upgrade=auto_minor_version_upgrade,
                    region=region,
                    users=[{"Username": username, "Password": password}]
                )
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "delete_broker":
            logger.debug("Executing delete_broker tool")
            broker_id = arguments["broker_id"]
            region = arguments["region"]
            try:
                result = handle_delete_broker(broker_id=broker_id, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "reboot_broker":
            logger.debug("Executing reboot_broker tool")
            broker_id = arguments["broker_id"]
            region = arguments["region"]
            try:
                result = handle_reboot_broker(broker_id=broker_id, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "update_broker":
            logger.debug("Executing update_broker tool")
            broker_id = arguments["broker_id"]
            region = arguments["region"]
            
            # Extract optional parameters
            auto_minor_version_upgrade = arguments.get("auto_minor_version_upgrade")
            configuration_id = arguments.get("configuration_id")
            configuration_revision = arguments.get("configuration_revision")
            engine_version = arguments.get("engine_version") 
            host_instance_type = arguments.get("host_instance_type")
            security_groups = arguments.get("security_groups")
            logs_general = arguments.get("logs_general")
            logs_audit = arguments.get("logs_audit")
            
            try:
                result = handle_update_broker(
                    broker_id=broker_id,
                    region=region,
                    auto_minor_version_upgrade=auto_minor_version_upgrade,
                    configuration_id=configuration_id,
                    configuration_revision=configuration_revision,
                    engine_version=engine_version,
                    host_instance_type=host_instance_type,
                    security_groups=security_groups,
                    logs_general=logs_general,
                    logs_audit=logs_audit
                )
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "list_users":
            logger.debug("Executing list_users tool")
            broker_id = arguments["broker_id"]
            region = arguments["region"]
            try:
                result = handle_list_users(broker_id=broker_id, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "describe_user":
            logger.debug("Executing describe_user tool")
            broker_id = arguments["broker_id"]
            username = arguments["username"]
            region = arguments["region"]
            try:
                result = handle_describe_user(broker_id=broker_id, username=username, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "create_user":
            logger.debug("Executing create_user tool")
            broker_id = arguments["broker_id"]
            username = arguments["username"]
            password = arguments["password"]
            console_access = arguments.get("console_access", False)
            groups = arguments.get("groups")
            region = arguments["region"]
            try:
                result = handle_create_user(
                    broker_id=broker_id,
                    username=username,
                    password=password,
                    console_access=console_access,
                    groups=groups,
                    region=region
                )
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "delete_user":
            logger.debug("Executing delete_user tool")
            broker_id = arguments["broker_id"]
            username = arguments["username"]
            region = arguments["region"]
            try:
                result = handle_delete_user(broker_id=broker_id, username=username, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]

        elif name == "list_tags":
            logger.debug("Executing list_tags tool")
            resource_arn = arguments["resource_arn"]
            region = arguments["region"]
            try:
                result = handle_list_tags(resource_arn=resource_arn, region=region)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]
        raise ValueError(f"Tool not found: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
