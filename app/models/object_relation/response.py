from pydantic import BaseModel, Field

class ModuleItem(BaseModel):
    module_name: str

class ObjectRelationResponse(BaseModel):
    results: list[ModuleItem]

class RelationRangeResponse(BaseModel):
    results: list[ModuleItem]