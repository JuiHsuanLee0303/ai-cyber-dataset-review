import json
from fastapi import APIRouter, HTTPException, Body
from app.config import settings, Settings
from typing import Dict

router = APIRouter()

SETTINGS_FILE = "data/settings.json"

def load_settings() -> Settings:
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            return Settings(**data)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty/corrupt, return default settings
        return Settings()

def save_settings(s: Settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s.model_dump(), f, indent=4)

# Update the global settings object on startup
settings = load_settings()


@router.get("/", response_model=Settings)
async def get_settings():
    """
    Retrieve the current system settings.
    """
    return load_settings()

@router.put("/", response_model=Settings)
async def update_settings(new_settings: Dict = Body(..., embed=True)):
    """
    Update the system settings.
    """
    global settings
    try:
        # Get current settings
        current_settings_data = load_settings().model_dump()
        # Update with new data
        current_settings_data.update(new_settings.get("settings", {}))
        
        updated_settings = Settings(**current_settings_data)
        save_settings(updated_settings)
        
        # Update the in-memory settings object
        settings = updated_settings
        
        return updated_settings
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update settings: {e}") 