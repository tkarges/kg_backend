from pydantic import BaseModel, Field

class ModuleFilterRequest(BaseModel):
    module: str = Field(..., description='Name of the study program for which available modules should be listed')