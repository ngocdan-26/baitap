
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    DateTime,
    ForeignKey,
    Text,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="ADMIN")
    created_at = Column(DateTime, default=datetime.utcnow)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)

    registrations = relationship(
        "Registration",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    specialty = Column(String(120), nullable=True)

    classes = relationship(
        "ClassRoom",
        back_populates="teacher",
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    duration_hours = Column(Integer, default=0)
    tuition_fee = Column(Float, default=0)

    classes = relationship(
        "ClassRoom",
        back_populates="course",
    )


class ClassRoom(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    capacity = Column(Integer, default=30)
    status = Column(String(20), default="OPEN")

    course = relationship(
        "Course",
        back_populates="classes",
    )
    teacher = relationship(
        "Teacher",
        back_populates="classes",
    )
    registrations = relationship(
        "Registration",
        back_populates="classroom",
        cascade="all, delete-orphan",
    )


class Registration(Base):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "class_id",
            name="uq_student_class",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="ACTIVE")

    student = relationship(
        "Student",
        back_populates="registrations",
    )
    classroom = relationship(
        "ClassRoom",
        back_populates="registrations",
    )
    result = relationship(
        "Result",
        back_populates="registration",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(
        Integer,
        ForeignKey("registrations.id"),
        unique=True,
        nullable=False,
    )
    score = Column(Float, nullable=True)
    grade = Column(String(20), nullable=True)
    comment = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    registration = relationship(
        "Registration",
        back_populates="result",
    )