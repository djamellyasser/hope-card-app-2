from fastapi import APIRouter, Request, HTTPException, Depends, Body, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
import json

from app.models.patient import PatientModel, PatientUpdate
from app.main import db, templates
from app.dependencies import verify_admin
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

# صفحة لوحة التحكم الرئيسية
@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request, user: User = Depends(verify_admin)):
    """صفحة لوحة التحكم الرئيسية - مطلوب تسجيل الدخول"""
    return templates.TemplateResponse(
        "admin/home.html",
        {"request": request, "user": user, "now": datetime.now()}
    )

# صفحة قائمة المرضى
@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: User = Depends(verify_admin)):
    patients = []
    for doc in db.patients.find().sort("created_at", -1):
        doc["_id"] = str(doc["_id"])
        if isinstance(doc.get("birth_date"), datetime):
            doc["birth_date"] = doc["birth_date"].isoformat()
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if isinstance(doc.get("updated_at"), datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
        patients.append(doc)
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "patients": patients,
        "user": user,
        "now": datetime.now()
    })

# صفحة الملف الشخصي
@router.get("/profile", response_class=HTMLResponse)
async def admin_profile(request: Request, user: User = Depends(verify_admin)):
    """صفحة الملف الشخصي للمستخدم - مطلوب تسجيل الدخول"""
    return templates.TemplateResponse(
        "admin/profile.html",
        {"request": request, "user": user, "now": datetime.now()}
    )

# Add new patient page
@router.get("/add", response_class=HTMLResponse)
async def add_patient_form(request: Request, user: User = Depends(verify_admin)):
    return templates.TemplateResponse("admin/add_patient.html", {
        "request": request,
        "user": user,
        "now": datetime.now()
    })

# Process add patient form
@router.post("/add")
async def create_patient(request: Request, user: User = Depends(verify_admin)):
    form_data = await request.form()
    
    # Process form data
    patient_data = {
        "patient_id": form_data.get("patient_id"),
        "full_name": form_data.get("full_name"),
        "birth_date": datetime.fromisoformat(form_data.get("birth_date")),
        "gender": form_data.get("gender"),
        "blood_type": form_data.get("blood_type"),
        "address": form_data.get("address"),
        "phone": form_data.get("phone"),
        "emergency_contact": form_data.get("emergency_contact"),
        "diagnosis": form_data.get("diagnosis"),
        "chronic_diseases": form_data.getlist("chronic_diseases") if "chronic_diseases" in form_data else [],
        "allergies": form_data.getlist("allergies") if "allergies" in form_data else [],
        "medications": form_data.getlist("medications") if "medications" in form_data else [],
        "notes": form_data.get("notes"),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Check if patient_id already exists
    if db.patients.find_one({"patient_id": patient_data["patient_id"]}):
        return templates.TemplateResponse(
            "admin/add_patient.html", 
            {
                "request": request, 
                "error": "رقم المريض موجود بالفعل", 
                "data": patient_data,
                "user": user,
                "now": datetime.now()
            }
        )
    
    # Insert patient
    result = db.patients.insert_one(patient_data)
    
    return RedirectResponse(url="/admin/dashboard", status_code=303)

# View patient details
@router.get("/patient/{patient_id}", response_class=HTMLResponse)
async def get_patient(request: Request, patient_id: str, user: User = Depends(verify_admin)):
    patient = db.patients.find_one({"patient_id": patient_id})
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient["_id"] = str(patient["_id"])
    if isinstance(patient.get("birth_date"), datetime):
        patient["birth_date"] = patient["birth_date"].isoformat().split("T")[0]
    
    return templates.TemplateResponse("admin/patient_details.html", {
        "request": request,
        "patient": patient,
        "user": user,
        "now": datetime.now()
    })

# Edit patient page
@router.get("/patient/{patient_id}/edit", response_class=HTMLResponse)
async def edit_patient_form(request: Request, patient_id: str, user: User = Depends(verify_admin)):
    patient = db.patients.find_one({"patient_id": patient_id})
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient["_id"] = str(patient["_id"])
    if isinstance(patient.get("birth_date"), datetime):
        patient["birth_date"] = patient["birth_date"].isoformat().split("T")[0]
    
    return templates.TemplateResponse("admin/edit_patient.html", {
        "request": request,
        "patient": patient,
        "user": user,
        "now": datetime.now()
    })

# Process edit patient form
@router.post("/patient/{patient_id}/edit")
async def update_patient(request: Request, patient_id: str, user: User = Depends(verify_admin)):
    form_data = await request.form()
    
    # Check if patient exists
    patient = db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Process form data
    update_data = {
        "full_name": form_data.get("full_name"),
        "birth_date": datetime.fromisoformat(form_data.get("birth_date")),
        "gender": form_data.get("gender"),
        "blood_type": form_data.get("blood_type"),
        "address": form_data.get("address"),
        "phone": form_data.get("phone"),
        "emergency_contact": form_data.get("emergency_contact"),
        "diagnosis": form_data.get("diagnosis"),
        "chronic_diseases": form_data.getlist("chronic_diseases") if "chronic_diseases" in form_data else [],
        "allergies": form_data.getlist("allergies") if "allergies" in form_data else [],
        "medications": form_data.getlist("medications") if "medications" in form_data else [],
        "notes": form_data.get("notes"),
        "updated_at": datetime.now()
    }
    
    # Update patient
    db.patients.update_one({"patient_id": patient_id}, {"$set": update_data})
    
    return RedirectResponse(url=f"/admin/patient/{patient_id}", status_code=303)

# Delete patient
@router.get("/patient/{patient_id}/delete")
async def delete_patient(patient_id: str, user: User = Depends(verify_admin)):
    # Check if patient exists
    patient = db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Delete patient
    db.patients.delete_one({"patient_id": patient_id})
    
    return RedirectResponse(url="/admin/dashboard", status_code=303)

# API endpoints for AJAX/JavaScript functionality
@router.get("/api/patients", response_model=List[PatientModel])
async def list_patients(user: User = Depends(verify_admin)):
    patients = []
    for doc in db.patients.find().sort("created_at", -1):
        patients.append(PatientModel(**doc))
    return patients

@router.get("/api/patient/{patient_id}", response_model=PatientModel)
async def get_patient_api(patient_id: str, user: User = Depends(verify_admin)):
    patient = db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientModel(**patient) 