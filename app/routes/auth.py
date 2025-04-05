from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_302_FOUND
from datetime import datetime, timedelta
import secrets
from app.models.user import authenticate_user, get_user_by_id

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")
security = HTTPBasic()

# لتخزين الجلسات النشطة (في تطبيق حقيقي، يجب استخدام حل أفضل مثل Redis)
active_sessions = {}

def get_current_user(request: Request):
    """استرجاع المستخدم الحالي من الجلسة"""
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in active_sessions:
        return None
    
    user_id = active_sessions[session_id]["user_id"]
    if not user_id:
        return None
    
    return get_user_by_id(user_id)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    """عرض صفحة تسجيل الدخول"""
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request, "error": error, "now": datetime.now()}
    )

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """معالجة تسجيل الدخول"""
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "اسم المستخدم أو كلمة المرور غير صحيحة", "now": datetime.now()}
        )
    
    # إنشاء معرف جلسة عشوائي
    session_id = secrets.token_hex(16)
    
    # تخزين معلومات الجلسة
    active_sessions[session_id] = {
        "user_id": user.id,
        "expires": datetime.now() + timedelta(hours=24)
    }
    
    # إعادة توجيه إلى لوحة التحكم مع ضبط ملف تعريف الارتباط
    response = RedirectResponse(url="/admin/", status_code=HTTP_302_FOUND)
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=86400) # صالح لمدة 24 ساعة
    
    return response

@router.get("/logout")
async def logout(request: Request):
    """تسجيل الخروج"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in active_sessions:
        del active_sessions[session_id]
    
    # إعادة توجيه إلى صفحة تسجيل الدخول وحذف ملف تعريف الارتباط
    response = RedirectResponse(url="/auth/login", status_code=HTTP_302_FOUND)
    response.delete_cookie(key="session_id")
    
    return response 