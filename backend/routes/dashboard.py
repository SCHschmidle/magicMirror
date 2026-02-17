from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse  
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
from pydantic import BaseModel
import os

router = APIRouter()

active = False
filedata_storage= []
index=0
filedata_storage.clear()
folder = Path("../frontend/magicmirror/public/media")
for file in folder.glob("*"):
    filedata_storage.append({'id': index,
                         'name': file.name,
                         'size': round(file.stat().st_size/1024/1024,3),
                         'active': active,
                         'duration': 30})
    index+=1


UPLOAD_DIR = Path(__file__).parent.parent.parent / "frontend" / "magicmirror" / "public" / "media"

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

class ActiveUpdateRequest(BaseModel):
    data: list[dict]

@router.get("/dashboard", response_class=HTMLResponse )
async def main(request: Request):
     return templates.TemplateResponse("dashboard.html", {"request": request})

@router.post("/upload/single")
async def upload_single_file(file: UploadFile = File(...),duration: int = Form(...)):
    active = False
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file selected")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    filedata_storage.append({"name": file.filename,
        "size": file.size,
        "active": False,
        "duration": duration})
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
        "location": str(file_path),
        "active": active,
        "duration": duration
    }


@router.get("/filedata")
async def getdata():
    global filedata_storage 
    filedata= []
    folder = Path("../frontend/magicmirror/public/media")
    for index, file in enumerate(folder.glob("*")):
        filedata.append({'id':index,
                         'name': file.name,
                         'size': round(file.stat().st_size/1024/1024,3),
                         'active': filedata_storage[index]['active'],
                         'duration': filedata_storage[index]['duration']})
    filedata_storage=filedata
    return filedata

@router.post("/activeupdate")
async def activeupdate(file_data: list[dict]):
    global filedata_storage
    for index, file in enumerate(file_data):
        filedata_storage[index]['active']= file['active']
        filedata_storage[index]['duration']= file['duration']
    return f"Updated {index} to {filedata_storage[index]['active']}"

@router.get("/display")
async def display_view():
    media_files = []
    for f in UPLOAD_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov', '.webm']:
            media_files.append(f.name)
    return JSONResponse(content={"media": media_files})

@router.get("/deletefile/{fileId}")
async def delete_file(fileId: str):
    path = UPLOAD_DIR / fileId
    os.remove(path)