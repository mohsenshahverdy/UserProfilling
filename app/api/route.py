from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.api.schemas import UserRequest 
from app.services import user_service
from app.utils.data_manager import get_data

target_users_router = APIRouter()

@target_users_router.post("/target-users/")
async def create_target_users(request: UserRequest, data=Depends(get_data)):
    try:
        result = user_service.process_user_data(request.user_data, data)
        if result is not None:
            return JSONResponse(status_code=200, content=result.to_dict())
        else:
            return JSONResponse(status_code=500, content={"message": "No result"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
