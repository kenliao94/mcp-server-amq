import boto3
from typing import List, Optional, Dict, Any

def handle_describe_broker(broker_id: str, region: str):
    client = boto3.client("mq", region_name=region)
    response = client.describe_broker(BrokerId=broker_id)
    return response

def handle_list_brokers(region: str):
    client = boto3.client("mq", region_name=region)
    response = client.list_brokers()
    return response

def handle_create_broker(
    broker_name: str,
    engine_type: str,
    engine_version: str,
    host_instance_type: str,
    deployment_mode: str,
    publicly_accessible: bool,
    auto_minor_version_upgrade: bool,
    users: List[Dict[str, str]],
    region: str = "us-east-1",
):
    client = boto3.client("mq", region_name=region)
    
    # Build create parameters
    create_params = {
        'BrokerName': broker_name,
        'EngineType': engine_type,
        'EngineVersion': engine_version,
        'HostInstanceType': host_instance_type,
        'DeploymentMode': deployment_mode,
        'PubliclyAccessible': publicly_accessible,
        'AutoMinorVersionUpgrade': auto_minor_version_upgrade,
        'Users': users,
    }
    
    response = client.create_broker(**create_params)
    return response

def handle_update_broker(
    broker_id: str,
    region: str,
    auto_minor_version_upgrade: Optional[bool] = None,
    configuration_id: Optional[str] = None,
    configuration_revision: Optional[int] = None,
    engine_version: Optional[str] = None,
    host_instance_type: Optional[str] = None,
    security_groups: Optional[List[str]] = None,
    logs_general: Optional[bool] = None,
    logs_audit: Optional[bool] = None
):
    client = boto3.client("mq", region_name=region)
    
    # Build update parameters dynamically based on provided arguments
    update_params = {'BrokerId': broker_id}
    
    if auto_minor_version_upgrade is not None:
        update_params['AutoMinorVersionUpgrade'] = auto_minor_version_upgrade
    
    if configuration_id is not None and configuration_revision is not None:
        update_params['Configuration'] = {
            'Id': configuration_id,
            'Revision': configuration_revision
        }
    
    if engine_version is not None:
        update_params['EngineVersion'] = engine_version
    
    if host_instance_type is not None:
        update_params['HostInstanceType'] = host_instance_type
    
    if security_groups is not None:
        update_params['SecurityGroups'] = security_groups
    
    # Handle logs configuration if either log setting is provided
    if logs_general is not None or logs_audit is not None:
        logs_config = {}
        if logs_general is not None:
            logs_config['General'] = logs_general
        if logs_audit is not None:
            logs_config['Audit'] = logs_audit
        update_params['Logs'] = logs_config
    
    response = client.update_broker(**update_params)
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