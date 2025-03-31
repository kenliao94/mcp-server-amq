## Setup the MCP server
- Provision a user on your AWS account IAM.
- Attach **ONLY** `AmazonMQFullAccess` on the new user.
- Use `aws configure` on your environment to configure the credential (You need the access ID and access key that generated in previous steps)

### Manual Installation
1. Clone this repository.
2. Add the following to your `claude_desktop_config.json` file:
- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```
{
    "mcpServers": {
      "amq": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/repo/mcp-server-amq", 
            "run", 
            "mcp-server-amq"
        ]
      }
    }
}


TODO:
1. Make sure all APIs are taken care of https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html