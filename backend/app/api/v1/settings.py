from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.users import get_current_admin_user

router = APIRouter()

def _extract_value(value):
    """Helper to handle both old ({'value': ...}) and new data formats."""
    # The value from the DB can be a direct value or a JSON object {'value': ...}
    if value and isinstance(value, dict) and 'value' in value:
        return value['value']
    return value

@router.get("/", response_model=schemas.AllSettings)
def read_settings(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all system settings as a single object.
    """
    settings_db = crud.get_all_settings(db)
    settings_map = {s.key: _extract_value(s.value) for s in settings_db}
    
    # Ensure all required settings are present
    required_keys = ["rejection_threshold", "approval_threshold", "ollama_model", "ollama_url"]
    if not all(key in settings_map for key in required_keys):
        raise HTTPException(status_code=500, detail="One or more system settings are missing from the database.")

    return schemas.AllSettings(
        rejection_threshold=settings_map.get("rejection_threshold"),
        approval_threshold=settings_map.get("approval_threshold"),
        ollama_model=settings_map.get("ollama_model"),
        ollama_url=settings_map.get("ollama_url"),
    )

@router.put("/", response_model=schemas.AllSettings)
def update_settings(
    settings_in: schemas.SystemSettingsUpdate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Update system settings.
    """
    crud.update_settings(db, settings_in.settings)
    
    # After updating, fetch them all to return the updated state
    updated_settings_db = crud.get_all_settings(db)
    settings_map = {s.key: _extract_value(s.value) for s in updated_settings_db}

    return schemas.AllSettings(
        rejection_threshold=settings_map.get("rejection_threshold"),
        approval_threshold=settings_map.get("approval_threshold"),
        ollama_model=settings_map.get("ollama_model"),
        ollama_url=settings_map.get("ollama_url"),
    ) 