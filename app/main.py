# https://fastapi.tiangolo.com/tutorial/first-steps/
# How to run the code: uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    role,
    user,
    auth,
    book_category
)

app = FastAPI(
    title="Library Management System",
    description="API for the LibMS Swift Mini Project!",
    version="0.1.0",
    contact={
        "name": "Kamal",
        "url": "https://github.com/KamalDGRT"
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book_category.router)


@app.get("/")
async def root():
    return {
        "message": "API is running successfully!"
    }
