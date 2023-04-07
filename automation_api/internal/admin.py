from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBasic()


@router.get("/")
async def admin_demo(credentials: HTTPBasicCredentials = Depends(security)):  # noqa
    return {"username": credentials.username, "password": credentials.password}
