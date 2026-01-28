from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "https://hrms-frontend-git-main-ajay-anands-projects-136b5f19.vercel.app"
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- EMPLOYEES ----------------

@app.post("/employees")
def add_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(models.Employee).filter(
        models.Employee.employee_id == emp.employee_id
    ).first():
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )
    if db.query(models.Employee).filter(
        models.Employee.email == emp.email
    ).first():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    employee = models.Employee(**emp.dict())
    db.add(employee)
    db.commit()
    return {"message": "Employee added successfully"}


@app.get("/employees")
def list_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted"}

# ---------------- ATTENDANCE ----------------

@app.post("/attendance")
def mark_attendance(att: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == att.employee_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance = models.Attendance(**att.dict())
    db.add(attendance)
    db.commit()
    return {"message": "Attendance marked"}

@app.get("/attendance/{employee_id}")
def get_attendance(employee_id: str, db: Session = Depends(get_db)):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).all()
