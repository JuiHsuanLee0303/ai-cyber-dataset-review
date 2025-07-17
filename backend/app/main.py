from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import models, base
from app.api.v1 import auth as auth_v1
from app.api.v1 import settings as settings_v1
from app.api.v1 import ollama as ollama_v1
from app.api.v1 import datasets as datasets_v1
from app.api.v1 import raw_datasets as raw_datasets_v1
from app.api.v1 import legal_articles as legal_articles_v1
from app.api.v1 import stats as stats_v1
from app.api.v1 import users as users_v1
from app.api.v1 import review as review_v1
from app import crud, schemas
from app.database.models import UserRole

import os

# CORS Middleware
def get_cors_origins():
    """動態獲取 CORS 允許的來源"""
    origins = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "https://localhost:5173",
        "https://127.0.0.1:5173",
        "https://ai-cyber-dataset-review.vercel.app"
    ]
    
    # 從環境變數獲取額外的 CORS 來源
    cors_origins = os.getenv("CORS_ORIGINS", "")
    if cors_origins:
        origins.extend(cors_origins.split(","))
    
    # 開發環境允許所有來源
    if os.getenv("ENVIRONMENT", "development") == "development":
        origins.extend(["http://*", "https://*"])
    
    return origins

def create_app() -> FastAPI:
    # --- Database Initialization ---
    def init_db():
        db = base.SessionLocal()
        try:
            # Check if default users exist
            admin_user = crud.get_user_by_username(db, username="admin")
            if not admin_user:
                admin_user_in = schemas.UserCreate(
                    username="admin",
                    password="admin",
                    role=UserRole.ADMIN
                )
                crud.create_user(db=db, user=admin_user_in)
                print("Admin user created.")

            expert_user = crud.get_user_by_username(db, username="expert")
            if not expert_user:
                expert_user_in = schemas.UserCreate(
                    username="expert",
                    password="expert",
                    role=UserRole.EXPERT
                )
                crud.create_user(db=db, user=expert_user_in)
                print("Expert user created.")
            
            # Initialize default system settings
            default_settings = {
                "rejection_threshold": 3,
                "approval_threshold": 2,
                "ollama_models": ["qwen3:1.7b"],  # 修改：支援多模型列表
                "ollama_url": "http://host.docker.internal:11434"
            }
            
            for key, value in default_settings.items():
                existing_setting = crud.get_setting(db, key)
                if not existing_setting:
                    crud.update_setting(db, key, value)
                    print(f"Default setting '{key}' initialized with value: {value}")
        finally:
            db.close()

    models.Base.metadata.create_all(bind=base.engine)
    init_db()

    app = FastAPI(
        title="AI Cybersecurity Dataset Review System API",
        description="API for managing and reviewing AI-generated cybersecurity datasets.",
        version="1.0.0",
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API Routers
    app.include_router(auth_v1.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(settings_v1.router, prefix="/api/v1/settings", tags=["System Settings"])
    app.include_router(ollama_v1.router, prefix="/api/v1/ollama", tags=["Ollama"])
    app.include_router(users_v1.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(datasets_v1.router, prefix="/api/v1/datasets", tags=["Final Datasets"])
    app.include_router(raw_datasets_v1.router, prefix="/api/v1/raw-datasets", tags=["Raw Datasets"])
    app.include_router(legal_articles_v1.router, prefix="/api/v1/legal-articles", tags=["Legal Articles"])
    app.include_router(stats_v1.router, prefix="/api/v1/stats", tags=["Statistics"])
    app.include_router(review_v1.router, prefix="/api/v1/review", tags=["Review"])

    @app.get("/", tags=["Root"])
    def read_root():
        return {"message": "歡迎使用 AI 資安資料審核系統 API"}
        
    return app

app = create_app()
