from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse  
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
from pydantic import BaseModel
import os
import csv
import pandas as pd
import json

router = APIRouter()

csv_path = Path("storage/storage.csv")

UPLOAD_DIR = Path(__file__).parent.parent.parent / "frontend" / "magicmirror" / "public" / "media"

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

class ActiveUpdateRequest(BaseModel):
    data: list[dict]

@router.get("/dashboard", response_class=HTMLResponse )
async def main(request: Request):
     return templates.TemplateResponse("dashboard.html", {"request": request})

@router.post("/upload/single")
async def upload_single_file(file: UploadFile = File(...),duration: int = Form(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file selected")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        # Lisst das CSV aus, fügt eine neue zeile hinzu und schreibt das CSV neu
    df = pd.read_csv(csv_path)
    df.loc[len(df)] = {
        "id": len(df),
        "name": file.filename,
        "size": file.size,
        "active": False,
        "duration": duration}
    df.to_csv(csv_path, index=False)
    
  
    
    return {
        "status": 200
    }


@router.get("/filedata")
async def getdata():
    df = pd.read_csv(csv_path)
    json_df = df.to_dict(orient="records")
    return json_df


@router.post("/activeupdate")
async def activeupdate(file_data: list[dict]):
    df = pd.DataFrame(file_data)
    df.to_csv(csv_path, index=False)
    return {"status": 200}

@router.get("/display")
async def display_view():
    media_files = []
    for f in UPLOAD_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov', '.webm']:
            media_files.append(f.name)
    return JSONResponse(content={"media": media_files})

@router.get("/deletefile/{fileId}")
async def delete_file(fileId: str):
    df = pd.read_csv(csv_path)
    fileName=df.loc[int(fileId), "name"]
    path = UPLOAD_DIR / fileName
    os.remove(path)
    df = df.drop(int(fileId))
    df["id"] = range(len(df))
    df.to_csv(csv_path, index=False)

@router.get("/setdata")
def set_csv():
    filedata= []
    index=0
    folder = Path("images")
    for file in folder.glob("*"):
        filedata.append({
            'id': index,
            'name': file.name,
            'size': round(file.stat().st_size/1024/1024,3),
            'active': False,
            'duration': 30})
    index+=1
    df = pd.DataFrame(filedata)
    df.to_csv(csv_path, index=False)
    return {"status": 200}

router.mount("/media", StaticFiles(directory="images"), name="media")

def update_csv(id, key, value):
    df = pd.read_csv(csv_path)
    df.loc[id, key] = value
    df.to_csv(csv_path, index=False)