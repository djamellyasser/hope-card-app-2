from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from app.models.patient import PatientModel
from app.main import db, templates

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

# User home page with search form
@router.get("/", response_class=HTMLResponse)
async def user_home(request: Request):
    return templates.TemplateResponse("user/home.html", {"request": request})

# Search patient by ID
@router.post("/search", response_class=HTMLResponse)
async def search_patient(request: Request):
    form_data = await request.form()
    patient_id = form_data.get("patient_id")
    
    # Redirect to patient details page
    return RedirectResponse(url=f"/user/patient/{patient_id}", status_code=303)

# View patient details
@router.get("/patient/{patient_id}", response_class=HTMLResponse)
async def get_patient(request: Request, patient_id: str):
    patient = db.patients.find_one({"patient_id": patient_id})
    
    if not patient:
        return templates.TemplateResponse(
            "user/home.html", 
            {"request": request, "error": "المريض غير موجود"}
        )
    
    patient["_id"] = str(patient["_id"])
    if isinstance(patient.get("birth_date"), datetime):
        patient["birth_date"] = patient["birth_date"].isoformat().split("T")[0]
    
    return templates.TemplateResponse("user/patient_details.html", {
        "request": request,
        "patient": patient
    })

# API endpoint for AJAX search
@router.get("/api/patient/{patient_id}")
async def get_patient_api(patient_id: str):
    patient = db.patients.find_one({"patient_id": patient_id})
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient["_id"] = str(patient["_id"])
    if isinstance(patient.get("birth_date"), datetime):
        patient["birth_date"] = patient["birth_date"].isoformat().split("T")[0]
    if isinstance(patient.get("created_at"), datetime):
        patient["created_at"] = patient["created_at"].isoformat()
    if isinstance(patient.get("updated_at"), datetime):
        patient["updated_at"] = patient["updated_at"].isoformat()
    
    return patient 