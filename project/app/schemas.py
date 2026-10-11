
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LoginInput(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str = Field(min_length=8)


class StudentIn(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    date_of_birth: date | None = None
    address: str | None = None


class StudentOut(ORMModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    date_of_birth: date | None
    address: str | None


class TeacherIn(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    specialty: str | None = None


class TeacherOut(ORMModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    specialty: str | None


class CourseIn(BaseModel):
    name: str
    description: str | None = None
    duration_hours: int = Field(default=0, ge=0)
    tuition_fee: float = Field(default=0, ge=0)


class CourseOut(ORMModel):
    id: int
    name: str
    description: str | None
    duration_hours: int
    tuition_fee: float


class ClassIn(BaseModel):
    name: str
    course_id: int
    teacher_id: int
    start_date: date | None = None
    end_date: date | None = None
    capacity: int = Field(default=30, ge=1)
    status: str = "OPEN"


class ClassOut(ORMModel):
    id: int
    name: str
    course_id: int
    teacher_id: int
    start_date: date | None
    end_date: date | None
    capacity: int
    status: str


class RegistrationIn(BaseModel):
    student_id: int
    class_id: int


class RegistrationOut(ORMModel):
    id: int
    student_id: int
    class_id: int
    registered_at: datetime
    status: str


class ResultIn(BaseModel):
    registration_id: int
    score: float | None = Field(default=None, ge=0, le=10)
    grade: str | None = None
    comment: str | None = None


class ResultOut(ORMModel):
    id: int
    registration_id: int
    score: float | None
    grade: str | None
    comment: str | None
    updated_at: datetime
