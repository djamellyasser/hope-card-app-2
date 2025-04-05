from pydantic import BaseModel, Field
from typing import List, Optional, Annotated, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, __core_schema, field_schema):
        field_schema.update(type="string")
        return field_schema

class PatientModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    patient_id: str = Field(..., description="Unique patient identifier")
    full_name: str = Field(..., description="Full name of the patient")
    birth_date: datetime = Field(..., description="Birth date of the patient")
    gender: str = Field(..., description="Gender of the patient")
    blood_type: str = Field(..., description="Blood type of the patient")
    address: str = Field(..., description="Home address of the patient")
    phone: str = Field(..., description="Contact phone number")
    emergency_contact: str = Field(..., description="Emergency contact information")
    diagnosis: str = Field(..., description="Main medical diagnosis")
    chronic_diseases: List[str] = Field(default=[], description="List of chronic diseases")
    allergies: List[str] = Field(default=[], description="List of allergies")
    medications: List[str] = Field(default=[], description="Current medications")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "patient_id": "P12345",
                "full_name": "محمد أحمد",
                "birth_date": "1980-01-01T00:00:00",
                "gender": "ذكر",
                "blood_type": "A+",
                "address": "شارع الأمل، المدينة",
                "phone": "0123456789",
                "emergency_contact": "أحمد محمد - 0987654321",
                "diagnosis": "ارتفاع ضغط الدم",
                "chronic_diseases": ["السكري", "الربو"],
                "allergies": ["البنسلين"],
                "medications": ["دواء ضغط الدم", "الأنسولين"],
                "notes": "يحتاج إلى متابعة دورية"
            }
        }

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    diagnosis: Optional[str] = None
    chronic_diseases: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    notes: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 