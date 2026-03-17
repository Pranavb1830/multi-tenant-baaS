from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from app.database import engine
from app import models
from app.routes import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "FastAPI backend running"}

@app.get("/health")
def health_check():
    return {"status": "UP"}