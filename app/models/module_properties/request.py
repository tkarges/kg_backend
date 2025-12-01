from pydantic import BaseModel, Field

class ModulePropertyRequest(BaseModel):
    module: str = Field(..., description='Selected module for which properties are wanted')
    relation: str = Field(..., description='Selected relation to filter modules')