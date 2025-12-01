from fastapi import APIRouter, HTTPException
from ..models.module_properties import (
    ModuleDomainResponse,
    ModulePropertyRequest,
    ModulePropertyResponse,
    ModulePropertyItem,
    ModuleDomainItem
)
from ..services import module_property

router = APIRouter(prefix="/api/module-property", tags=["module-property"])

@router.post("/", response_model=ModulePropertyResponse)
async def run_query(data: ModulePropertyRequest) -> ModulePropertyResponse:
    try:
        output = module_property.run_query(data.relation, data.module)
        results = [ModulePropertyItem(**item) for item in output]
        return ModulePropertyResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='Error running query')
    
@router.post('/module-domains', response_model=ModuleDomainResponse)
async def get_module_domains() -> ModuleDomainResponse:
    try:
        print(f'DEBUG: Routed to get_module_domains')
        output = module_property.get_module_domain()
        results = [ModuleDomainItem(**item) for item in output]
        return ModuleDomainResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='Error obtaining relation ranges')