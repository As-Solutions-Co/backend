from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Hello": str(settings.SQLALCHEMY_DATABASE_URI),
        "type": str(type(settings.SQLALCHEMY_DATABASE_URI)),
        "message": "Archivo escrito correctamente 🚀",
    }
