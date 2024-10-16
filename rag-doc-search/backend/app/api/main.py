from fastapi import APIRouter

from app.api.routes import items, login, users, utils,files,collections,divisions,documents


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(divisions.router, prefix="/divisions", tags=["divisions"])
api_router.include_router(collections.router, prefix="/collections", tags=["collections"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
