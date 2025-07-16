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

    # We need to refresh the dataset object to get the updated counts
    db.refresh(dataset)
    
    # Check approval threshold and move to final dataset if met
    if review.result.upper() == "ACCEPT":
        approval_threshold_setting = crud.get_setting(db, "approval_threshold")
        approval_threshold = _extract_value(approval_threshold_setting.value) if approval_threshold_setting else 2
        
        if dataset.accept_count >= approval_threshold:
            print(f"Dataset {dataset.id} has reached the approval threshold. Moving to final dataset.")
            # Move to final dataset
            final_dataset = models.FinalDataset(
                original_input=dataset.input or "",
                final_output=dataset.output,
                raw_dataset_id=dataset.id
            )
            db.add(final_dataset)
            dataset.review_status = "accepted"
            db.commit()
            print(f"Dataset {dataset.id} has been moved to final dataset.")
    
    # Trigger auto-regeneration if rejection threshold is met
    elif review.result.upper() == "REJECT":
        rejection_threshold_setting = crud.get_setting(db, "rejection_threshold")
        # Use a default if not set, although init_db should handle it
        rejection_threshold = _extract_value(rejection_threshold_setting.value) if rejection_threshold_setting else 3

        if dataset.reject_count >= rejection_threshold:
            print(f"Dataset {dataset.id} has reached the rejection threshold. Adding regeneration task to background.")
            background_tasks.add_task(regenerate_dataset, db, dataset.id)
            
    return review_log 