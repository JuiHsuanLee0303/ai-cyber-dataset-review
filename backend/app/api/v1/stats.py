from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.users import get_current_admin_user

router = APIRouter()

@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all statistics for the admin dashboard.
    """
    global_stats = crud.get_global_stats(db)
    review_activity = crud.get_review_activity(db, days=30)
    top_reviewers = crud.get_top_reviewers(db, limit=5)
    common_rejection_reasons = crud.get_common_rejection_reasons(db, limit=5)

    return schemas.DashboardStats(
        global_stats=global_stats,
        review_activity=review_activity,
        top_reviewers=top_reviewers,
        common_rejection_reasons=common_rejection_reasons
    ) 