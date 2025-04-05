from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    name: str
    role: str = "admin"

# قائمة بسيطة للمستخدمين (في تطبيق حقيقي، يجب تخزين ذلك في قاعدة بيانات)
users = [
    User(id=1, username="admin", password="admin123", name="المدير", role="admin"),
]

def authenticate_user(username: str, password: str):
    """التحقق من بيانات تسجيل الدخول"""
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def get_user_by_id(user_id: int):
    """البحث عن مستخدم حسب المعرف"""
    for user in users:
        if user.id == user_id:
            return user
    return None 