from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.dependencies import verify_admin
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request, user: User = Depends(verify_admin)):
    """صفحة لوحة التحكم الرئيسية - مطلوب تسجيل الدخول"""
    return templates.TemplateResponse(
        "admin/home.html",
        {"request": request, "user": user, "now": datetime.now()}
    )

@router.get("/profile", response_class=HTMLResponse)
async def admin_profile(request: Request, user: User = Depends(verify_admin)):
    """صفحة الملف الشخصي للمستخدم - مطلوب تسجيل الدخول"""
    return templates.TemplateResponse(
        "admin/profile.html",
        {"request": request, "user": user, "now": datetime.now()}
    ) 