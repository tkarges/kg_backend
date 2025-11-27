from pydantic import BaseModel, Field

class ObjectRelationRequest(BaseModel):
    obj: str = Field(..., description='Selected value in the specified range of the selecte relation')
    relation: str = Field(..., description='Selected relation to filter modules')

class RelationRangeRequest(BaseModel):
    relation: str = Field(..., description='Returns all possible values in the range of a selected relation')