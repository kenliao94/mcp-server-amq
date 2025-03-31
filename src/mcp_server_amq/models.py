from typing import Annotated, Optional, List, Dict, Any
from pydantic import BaseModel, Field

class DescribeBroker(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID to describe")]
    region: Annotated[str, Field(description="The region of the broker")]

class ListBrokers(BaseModel):
    region: Annotated[str, Field(description="The region to list brokers from")]

class RebootBroker(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID to reboot")]
    region: Annotated[str, Field(description="The region of the broker")]

class UpdateBroker(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID to update")]
    region: Annotated[str, Field(description="The region of the broker")]
    auto_minor_version_upgrade: Annotated[Optional[bool], Field(description="Enables automatic upgrades to new minor versions")] = None
    configuration_id: Annotated[Optional[str], Field(description="The configuration ID for the broker")] = None
    configuration_revision: Annotated[Optional[int], Field(description="The revision number of the configuration")] = None
    engine_version: Annotated[Optional[str], Field(description="The broker engine version to upgrade to")] = None
    host_instance_type: Annotated[Optional[str], Field(description="The broker's instance type (e.g., mq.t3.micro)")] = None
    security_groups: Annotated[Optional[List[str]], Field(description="List of security group IDs")] = None
    logs_general: Annotated[Optional[bool], Field(description="Enables general logging")] = None
    logs_audit: Annotated[Optional[bool], Field(description="Enables audit logging")] = None

class ListUsers(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID to list users from")]
    region: Annotated[str, Field(description="The region of the broker")]

class DescribeUser(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID the user belongs to")]
    username: Annotated[str, Field(description="The username to describe")]
    region: Annotated[str, Field(description="The region of the broker")]

class CreateUser(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID to create user for")]
    username: Annotated[str, Field(description="The username to create")]
    password: Annotated[str, Field(description="The password for the new user")]
    console_access: Annotated[bool, Field(description="Whether the user has console access")] = False
    groups: Annotated[Optional[List[str]], Field(description="Optional groups to add the user to")] = None
    region: Annotated[str, Field(description="The region of the broker")]

class DeleteUser(BaseModel):
    broker_id: Annotated[str, Field(description="The broker ID the user belongs to")]
    username: Annotated[str, Field(description="The username to delete")]
    region: Annotated[str, Field(description="The region of the broker")]

class ListTags(BaseModel):
    resource_arn: Annotated[str, Field(description="The ARN of the resource to list tags for")]
    region: Annotated[str, Field(description="The region of the resource")]
