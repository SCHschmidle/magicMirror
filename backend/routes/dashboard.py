from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()


@router.get("/dashboard")
def read_root():
    return {"Hello": "World"}