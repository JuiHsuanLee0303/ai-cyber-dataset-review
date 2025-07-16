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
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
