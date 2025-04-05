from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging
import sys
from datetime import datetime
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Initialize FastAPI app
app = FastAPI(title="Hope Card - بطاقة الأمل")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

# MongoDB connection
db_URI = "mongodb+srv://yasserdjamel1:SOrvfCxCCsGr0qYi@cluster0.xc0fmrr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(db_URI, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
    # Ping the database to check connection
    client.admin.command('ping')
    logging.info("Successfully connected to MongoDB Atlas!")
    db = client.hope_card_db
except Exception as e:
    logging.error(f"Error connecting to MongoDB Atlas: {e}")
    raise

# Import routes
from app.routes import admin, user, auth

# Include routers
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root(request: Request):
    """الصفحة الرئيسية"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "now": datetime.now()}
    )

@app.get("/landing")
async def landing(request: Request):
    """صفحة الهبوط المحسنة"""
    return templates.TemplateResponse(
        "landing.html",
        {"request": request, "now": datetime.now()}
    )

# تعديل سلوك الوصول إلى لوحة التحكم - توجيه دائم إلى صفحة تسجيل الدخول
@app.get("/admin")
@app.get("/admin/")
async def admin_redirect():
    """توجيه المستخدم دائمًا إلى صفحة تسجيل الدخول عند محاولة الوصول إلى لوحة التحكم"""
    return RedirectResponse(url="/auth/login", status_code=HTTP_302_FOUND)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True) 