from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Customer Support Platform")

app.include_router(router)

# Mount static directory for UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
