from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional
from pydantic import BaseModel

# FastAPI app
app = FastAPI()


# Database setup (Replace with your actual database URL)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)


# Employee Model
class Employee(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    title: str = Field(index=True)
    manager_id: int | None = Field(
        default=None, foreign_key="employee.id", index=True)


# Create tables
SQLModel.metadata.create_all(engine)


# Get a database session
def get_session():
    with Session(engine) as session:
        yield session


# Response Model
class EmployeeResponse(BaseModel):
    id: int
    name: str
    title: str
    manager_id: Optional[int]
    direct_reports: List["EmployeeResponse"] = []

    class Config:
        from_attributes = True


# Request body model
class UpdateManagerRequest(BaseModel):
    employee_id: int
    manager_id: int | None


# Get all Employees
@app.get("/employees", response_model=List[EmployeeResponse])
def get_employees(session: Session = Depends(get_session)):
    employees = session.exec(select(Employee)).all()

    # Build employee response with direct reports
    employee_responses = {}
    for emp in employees:
        emp_response = EmployeeResponse(
            id=emp.id, name=emp.name, title=emp.title, manager_id=emp.manager_id
        )
        employee_responses[emp.id] = emp_response

    # Assign direct reports
    for emp in employees:
        if emp.manager_id in employee_responses:
            employee_responses[emp.manager_id].direct_reports.append(
                employee_responses[emp.id])

    # Return only top-level employees (those without a manager)
    return [emp for emp in employee_responses.values() if emp.manager_id is None]


# Update Manager ID for Employees
@app.post("/managers/update")
def update_manager_id(data: UpdateManagerRequest, session: Session = Depends(get_session)):
    # Fetch the employee
    employee = session.get(Employee, data.employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Validate manager existence (if not None)
    if data.manager_id is not None:
        manager = session.get(Employee, data.manager_id)
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")

    # Prevent self-referencing
    if data.employee_id == data.manager_id:
        raise HTTPException(
            status_code=400, detail="Employee cannot be their own manager")

    # Update manager_id
    employee.manager_id = data.manager_id
    session.add(employee)
    session.commit()
    session.refresh(employee)

    return {"message": "Manager updated successfully", "employee": employee}


# Default routes
@app.get("/")
def read_root():
    return {"message": "Welcome to Org-Tree"}


# Seed DB with Employee Data
@app.get("/seed-employees")
def seed_employees(session: Session = Depends(get_session)):
    existing_employees = session.exec(select(Employee)).all()

    if existing_employees:
        return {"message": "Employees already seeded"}

    # Create the Root Employee (CEO)
    boss = Employee(name="Alice Johnson", title="CEO", manager_id=None)
    session.add(boss)
    session.commit()
    session.refresh(boss)

    # Managers under the CEO
    manager_1 = Employee(
        name="Bob Smith", title="Engineering Manager", manager_id=boss.id)
    manager_2 = Employee(name="Catherine Lee",
                         title="Marketing Manager", manager_id=boss.id)

    session.add_all([manager_1, manager_2])
    session.commit()
    session.refresh(manager_1)
    session.refresh(manager_2)

    # Employees under each manager
    employees = [
        Employee(name="David Brown", title="Software Engineer",
                 manager_id=manager_1.id),
        Employee(name="Ella Davis", title="Software Engineer",
                 manager_id=manager_1.id),
        Employee(name="Frank Wilson", title="Marketing Specialist",
                 manager_id=manager_2.id),
        Employee(name="Grace Miller", title="Marketing Specialist",
                 manager_id=manager_2.id),
        Employee(name="Hank White", title="HR Specialist",
                 manager_id=boss.id)
    ]

    session.add_all(employees)
    session.commit()

    return {"message": "Employees seeded successfully"}
