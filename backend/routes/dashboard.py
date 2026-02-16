from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse  
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
from pathlib import Path
router = APIRouter()

active = False

UPLOAD_DIR = Path("images")

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

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

@router.get("/display")
async def display_view():
    image_files = [f.name for f in UPLOAD_DIR.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]
    return JSONResponse(content={"images": image_files})
