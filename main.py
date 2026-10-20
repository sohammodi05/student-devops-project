
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="Student Management API",
    description="DevOps portfolio project using FastAPI",
    version="1.0.0",
)


class Student(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


students: dict[int, Student] = {}


@app.get("/")
def home():
    return {
        "message": "Student Management API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/students", status_code=201)
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(
            status_code=409,
            detail="Student ID already exists",
        )

    students[student.id] = student
    return student


@app.get("/students")
def get_students():
    return list(students.values())


@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return students[student_id]


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    if student.id != student_id:
        raise HTTPException(
            status_code=400,
            detail="URL ID and student ID must match",
        )

    students[student_id] = student
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    del students[student_id]
    return {"message": "Student deleted successfully"}
