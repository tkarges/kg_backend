from fastapi import APIRouter, HTTPException
from ..models.module_filter import ModuleFilterRequest, ModuleFilterResponse, ModuleItem
from ..services import module_filter

router = APIRouter(prefix="/api/module-filter", tags=["module-filter"])

@router.post("/", response_model=ModuleFilterResponse)
async def run_query(data: ModuleFilterRequest) -> ModuleFilterResponse:
    try:
        output = module_filter.run_query(data.module)
        results = [ModuleItem(**item) for item in output]
        return ModuleFilterResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='Error running query')