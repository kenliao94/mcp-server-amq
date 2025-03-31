import boto3

def handle_describe_broker(broker_id: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.describe_broker(BrokerId=broker_id)
    return response
