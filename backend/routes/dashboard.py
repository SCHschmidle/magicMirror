from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse  
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
from pydantic import BaseModel

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
                         'active': active})
    index+=1


UPLOAD_DIR = Path(__file__).parent.parent.parent / "frontend" / "magicmirror" / "public" / "media"

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

class ActiveUpdateRequest(BaseModel):
    key: int



@router.get("/dashboard", response_class=HTMLResponse )
async def main(request: Request):
     return templates.TemplateResponse("dashboard.html", {"request": request})

@router.post("/upload/single")
async def upload_single_file(file: UploadFile = File(...)):
    active = False
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file selected")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
        "location": str(file_path),
        "active": active,
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
                         'active': filedata_storage[index]['active']})
    return filedata_storage

@router.post("/activeupdate")
async def activeupdate(request: ActiveUpdateRequest):
    key = request.key
    global filedata_storage
    filedata_storage[key]['active']= not(filedata_storage[key]['active'])
    return f"updated {key} to {filedata_storage[key]['active']}"

@router.get("/display")
async def display_view():
    media_files = []
    for f in UPLOAD_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov', '.webm']:
            media_files.append(f.name)
    return JSONResponse(content={"media": media_files})
