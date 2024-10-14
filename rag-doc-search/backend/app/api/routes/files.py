import os
import shutil
from pathlib import Path
from typing import Any
from fastapi import File, UploadFile,Form
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.api.deps import (
    CurrentUser,
    SessionDep,
)

UPLOAD_BASE_DIR = "uploads"

router = APIRouter()


@router.post(
    "/uploadfile/"
)
async def create_upload_file(
    session: SessionDep, 
    current_user: CurrentUser,
    username: str = Form(...), 
    collectionname:str = Form(...),
    upload_file: UploadFile = File(...)) -> Any:
    """
    Upload file
    """
    try:

        pacurrent_pathth = os.getcwd()
        UPLOAD_DIR = Path(pacurrent_pathth + "/" + UPLOAD_BASE_DIR + "/" + username +  "/" + collectionname)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        fileName = upload_file.filename.replace("/","_")
        save_path = UPLOAD_DIR / fileName

        with save_path.open("wb+") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return {"username":username, "collectionname":collectionname,"filename":upload_file.filename,"content_type":upload_file.content_type}

    finally:
        upload_file.file.close()
        print("api:uploadfile successful!")


@router.get(
    "/downloadfile/"
)
async def get_file(
    session: SessionDep,
    current_user: CurrentUser,
    filename: str):
    try:
            
        current_path = Path()
        file_path = current_path / UPLOAD_BASE_DIR / filename

        now = datetime.now()

        response = FileResponse(
                                path=file_path,
                                filename=f"download_{now.strftime('%Y%m%d%H%M%S')}_{filename}"
                                )

        return response

    finally:
        print("api:uploadfile successful!")

@router.get(
    "/test/"
)
async def test(
    current_user: CurrentUser):
    try:
            
        return "OK"

    finally:
        print("api:uploadfile successful!")
