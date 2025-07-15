from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_user
from app.services.regeneration import regenerate_dataset

router = APIRouter()

def _extract_value(value):
    """Helper to handle both old ({'value': ...}) and new data formats."""
    if isinstance(value, dict) and 'value' in value:
        return value['value']
    return value

@router.post("/{dataset_id}", status_code=status.HTTP_201_CREATED)
def submit_review(
    dataset_id: int,
    review: schemas.ReviewCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Submit a review (Accept/Reject) for a dataset item.
    """
    dataset = crud.get_raw_dataset(db, dataset_id=dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="找不到指定的資料集")

    # Check if user has already reviewed this item
    for log in dataset.review_logs:
        if log.reviewer_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="您已經審核過這筆資料了"
            )
    
    review_log = crud.create_review_log(
        db=db, 
        dataset_id=dataset_id, 
        reviewer_id=current_user.id, 
        review=review
    )

    # Trigger auto-regeneration if rejection threshold is met
    if review.result.upper() == "REJECT":
        threshold_setting = crud.get_setting(db, "rejection_threshold")
        # Use a default if not set, although init_db should handle it
        threshold = _extract_value(threshold_setting.value) if threshold_setting else 3
        
        # We need to refresh the dataset object to get the updated reject_count
        db.refresh(dataset)

        if dataset.reject_count >= threshold:
            print(f"Dataset {dataset.id} has reached the rejection threshold. Adding regeneration task to background.")
            background_tasks.add_task(regenerate_dataset, db, dataset.id)
            
    return review_log 