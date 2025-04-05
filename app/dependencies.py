from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from datetime import datetime
from app.routes.auth import active_sessions, get_current_user

async def verify_admin(request: Request):
    """
    التحقق من أن المستخدم مسجل دخوله وهو مسؤول
    يستخدم كوسيط لحماية مسارات لوحة التحكم
    """
    user = get_current_user(request)
    
    if not user:
        # إعادة توجيه إلى صفحة تسجيل الدخول
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    if user.role != "admin":
        # إذا كان المستخدم غير مصرح له بالوصول
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية الوصول لهذه الصفحة"
        )
    
    # تنظيف الجلسات منتهية الصلاحية
    expired_sessions = []
    for session_id, session_data in active_sessions.items():
        if session_data["expires"] < datetime.now():
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del active_sessions[session_id]
    
    # إضافة المستخدم إلى طلب الوصول
    request.state.user = user
    
    return user 