from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import base

router = APIRouter()

def get_db():
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.RawDataset])
def read_raw_datasets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    raw_datasets = crud.get_raw_datasets(db, skip=skip, limit=limit)
    return raw_datasets

@router.put("/{dataset_id}", response_model=schemas.RawDataset)
def update_raw_dataset(dataset_id: int, dataset: schemas.RawDatasetUpdate, db: Session = Depends(get_db)):
    db_dataset = crud.update_raw_dataset(db, dataset_id=dataset_id, dataset_in=dataset)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset

@router.post("/{dataset_id}/review")
def review_raw_dataset(dataset_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review_for_dataset(db=db, dataset_id=dataset_id, review=review) 