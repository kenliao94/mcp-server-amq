import boto3
from typing import List, Optional

def handle_describe_broker(broker_id: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.describe_broker(BrokerId=broker_id)
    return response

def handle_list_brokers(region: str):
    client = boto3.client("mq", region_name=region)
    response = client.list_brokers()
    return response

def handle_reboot_broker(broker_id: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.reboot_broker(BrokerId=broker_id)
    return response

def handle_list_users(broker_id: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.list_users(BrokerId=broker_id)
    return response

def handle_describe_user(broker_id: str, username: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.describe_user(BrokerId=broker_id, Username=username)
    return response

def handle_create_user(
    broker_id: str, 
    username: str, 
    password: str, 
    console_access: bool = False,
    groups: Optional[List[str]] = None,
    region: str = "us-east-1"
):
    client = boto3.client("mq", region_name=region)
    user_data = {
        "Password": password,
        "ConsoleAccess": console_access,
    }
    if groups:
        user_data["Groups"] = groups
        
    response = client.create_user(
        BrokerId=broker_id,
        Username=username,
        **user_data
    )
    return response

def handle_delete_user(broker_id: str, username: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.delete_user(BrokerId=broker_id, Username=username)
    return response

def handle_list_tags(resource_arn: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.list_tags(ResourceArn=resource_arn)
    return response
