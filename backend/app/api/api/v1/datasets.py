from fastapi import APIRouter
from app import crud, schemas
from app.database import base
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import List

router = APIRouter()

def get_db():
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/final", response_model=List[schemas.FinalDataset])
def read_final_datasets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datasets = crud.get_final_datasets(db, skip=skip, limit=limit)
    return datasets 