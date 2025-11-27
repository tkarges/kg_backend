from fastapi import APIRouter, HTTPException
from ..models.object_relation import (
    ObjectRelationRequest, 
    ObjectRelationResponse, 
    RelationRangeRequest,
    RelationRangeResponse,
    ModuleItem
)
from ..services import object_relation

router = APIRouter(prefix="/api/object-relation", tags=["object-relation"])

@router.post("/", response_model=ObjectRelationResponse)
async def run_query(data: ObjectRelationRequest) -> ObjectRelationResponse:
    try:
        output = object_relation.run_query(data.relation, data.obj)
        results = [ModuleItem(**item) for item in output]
        return ObjectRelationResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='Error running query')
    
@router.post('/relation-ranges', response_model=RelationRangeResponse)
async def get_relation_ranges(data: RelationRangeRequest) -> RelationRangeResponse:
    try:
        output = object_relation.get_relation_range(data.relation)
        results = [ModuleItem(**item) for item in output]
        return ObjectRelationResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='Error obtaining relation ranges')