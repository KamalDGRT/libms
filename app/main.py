# https://fastapi.tiangolo.com/tutorial/first-steps/
# How to run the code: uvicorn app.main:app --reload

from fastapi import FastAPI


from app.database import SQLALCHEMY_DATABASE_URL

app = FastAPI(
    title="Library Management System",
    description="API for the LibMS Swift Mini Project!",
    version="0.1.0",
    contact={
        "name": "Kamal",
        "url": "https://github.com/KamalDGRT"
    }
)


@app.get("/")
async def root():
    return {
        "message": "API is running successfully!"
    }
