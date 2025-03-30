from typing import Annotated
from pydantic import BaseModel, Field

class DescribeBroker(BaseModel):
    broker_id: Annotated[str, Field(description="The message to publish")]
