from pydantic import BaseModel, Field

class ModulePropertyItem(BaseModel):
    module_property: str

class ModuleDomainItem(BaseModel):
    module_name: str

class ModulePropertyResponse(BaseModel):
    results: list[ModulePropertyItem]

class ModuleDomainResponse(BaseModel):
    results: list[ModuleDomainItem]