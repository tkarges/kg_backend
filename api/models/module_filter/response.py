from pydantic import BaseModel, Field

class ModuleItem(BaseModel):
    module_name: str

class ModuleFilterResponse(BaseModel):
    results: list[ModuleItem]