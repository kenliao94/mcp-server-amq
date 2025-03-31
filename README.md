## Setup the MCP server
- Provision a user on your AWS account IAM.
- Attach **ONLY** `AmazonMQFullAccess` on the new user.
- Use `aws configure` on your environment to configure the credential (You need the access ID and access key that generated in previous steps)

TODO:
1. Make sure all APIs are taken care of https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html
2. Finish the README
3. Add resources for sizing rules and other documentation