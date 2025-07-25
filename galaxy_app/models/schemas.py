# galaxy_app/models/schemas.py

# Import BaseModel from Pydantic to define data validation and serialization
from pydantic import BaseModel

# Schema for incoming requests to run a tool
class RunToolRequest(BaseModel):
    tool_id: str
    
# Schema for the response after running a tool
class RunToolResponse(BaseModel):
    message: str
    tool_id: str
    history_id: int
    input_dataset_id: int
    output_dataset_id: int
    output: str
