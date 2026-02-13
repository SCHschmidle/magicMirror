#Imports
import sys
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).parent))

from routes.display import router as display_router
from routes.dashboard import router as dashboard_router


app = FastAPI()

app.include_router(dashboard_router)
app.include_router(display_router)


