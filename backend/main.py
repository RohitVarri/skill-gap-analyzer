from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.api.analyze import router

app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(directory="backend/templates")

@app.get("/")
def home():
    return {"message": "Skill Gap Analyzer running"}