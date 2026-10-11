from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import Base, engine
import app.models
from app.routers import (
    auth, student, teacher, course,
    classroom, registration, result, dashboard
)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Training Center Management API",
    description="API quản lý trung tâm đào tạo",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def home():
    return {
        "message": "Training Center API is running",
        "docs": "/docs"
    }


app.include_router(auth.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(course.router)
app.include_router(classroom.router)
app.include_router(registration.router)
app.include_router(result.router)
app.include_router(dashboard.router)
