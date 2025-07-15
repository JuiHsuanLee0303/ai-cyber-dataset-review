from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import models, base
from app.api.v1 import (
    auth as auth_v1, 
    users as users_v1, 
    datasets as datasets_v1, 
    review as review_v1,
    settings as settings_v1,
    ollama as ollama_v1,
    stats as stats_v1
)
from app import crud, schemas
from app.database.models import UserRole

def init_db():
    db = base.SessionLocal()
    
    def seed_dataset(instruction: str, input_text: str, output: str, system_prompt: str, source: list):
        dataset_in = schemas.RawDatasetCreate(
            instruction=instruction, 
            input=input_text, 
            output=output, 
            system_prompt=system_prompt,
            source=source
        )
        crud.create_raw_dataset(db, dataset=dataset_in)

    try:
        # Check if default users exist
        if not crud.get_user_by_username(db, username="admin"):
            admin_user_in = schemas.UserCreate(username="admin", password="admin", role=UserRole.ADMIN)
            crud.create_user(db=db, user=admin_user_in)
            print("Admin user created.")

        if not crud.get_user_by_username(db, username="expert"):
            expert_user_in = schemas.UserCreate(username="expert", password="expert", role=UserRole.EXPERT)
            crud.create_user(db=db, user=expert_user_in)
            print("Expert user created.")

        # Check if there is any raw data
        if db.query(models.RawDataset).count() == 0:
            print("Seeding initial dataset...")
            seed_dataset(
                instruction="Analyze the following code for potential vulnerabilities",
                input_text="function login(user, pass) {\n  let query = \"SELECT * FROM users WHERE username = '\" + user + \"' AND password = '\" + pass + \"'\";\n  // execute query\n}",
                output="The provided code snippet is vulnerable to SQL Injection...",
                system_prompt="You are a cybersecurity expert.",
                source=["Internal security audit finding #102"]
            )
            seed_dataset(
                instruction="Identify security risks in storing passwords in plaintext.",
                input_text="Our current system stores user passwords directly in the database without any hashing or encryption.",
                output="Storing passwords in plaintext is a major security risk...",
                system_prompt="You are a data protection officer.",
                source=["NIST SP 800-63B", "OWASP Top 10"]
            )
            print("Initial dataset seeded.")

        # Create default settings if they don't exist
        rejection_threshold = crud.get_setting(db, "rejection_threshold")
        if not rejection_threshold:
            crud.update_setting(db, "rejection_threshold", 3)
            print("Default setting 'rejection_threshold' created with value 3.")

        ollama_model = crud.get_setting(db, "ollama_model")
        if not ollama_model:
            crud.update_setting(db, "ollama_model", "llama3")
            print("Default setting 'ollama_model' created with value 'llama3'.")
        
        ollama_url = crud.get_setting(db, "ollama_url")
        if not ollama_url:
            crud.update_setting(db, "ollama_url", "http://ollama:11434")
            print("Default setting 'ollama_url' created with value 'http://ollama:11434'.")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    models.Base.metadata.create_all(bind=base.engine)
    init_db()
    yield
    print("Shutting down...")

app = FastAPI(
    title="AI Cybersecurity Dataset Review System API",
    description="API for managing and reviewing AI-generated cybersecurity datasets.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_v1.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_v1.router, prefix="/api/v1/users", tags=["users"])
app.include_router(datasets_v1.router, prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(review_v1.router, prefix="/api/v1/review", tags=["review"])
app.include_router(settings_v1.router, prefix="/api/v1/settings", tags=["settings"])
app.include_router(ollama_v1.router, prefix="/api/v1/ollama", tags=["ollama"])
app.include_router(stats_v1.router, prefix="/api/v1/stats", tags=["stats"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "歡迎使用 AI 資安資料審核系統 API"} 