from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()
class Student(BaseModel):
    name: str
    age: int
    rollno: str 
    department: str

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    rollno: str 
    department: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

# In-memory storage for students
students_db = []
next_id = 1

@app.post("/student", response_model=StudentResponse)
def create_student(student: Student):
    global next_id
    student_data = StudentResponse(id=next_id, **student.dict())
    students_db.append(student_data)
    next_id += 1
    return student_data

@app.get("/student")
def read_students():
    return students_db

@app.get("/student/{id}", response_model=StudentResponse)
def read_student(id: int):
    for student in students_db:
        if student.id == id:
            return student
    return {"error": "Student not found"}

@app.put("/student/{id}", response_model=StudentResponse)
def update_student(id: int, student: Student):
    for idx, existing_student in enumerate(students_db):
        if existing_student.id == id:
            updated_student = StudentResponse(id=id, **student.dict())
            students_db[idx] = updated_student
            return updated_student
    return {"error": "Student not found"}

@app.delete("/student/{id}")
def delete_student(id: int):
    for idx, student in enumerate(students_db):
        if student.id == id:
            deleted_student = students_db.pop(idx)
            return {"message": "Student deleted", "student": deleted_student}
    return {"error": "Student not found"}


