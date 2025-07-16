from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve statistics for the dashboard.
    - Admin users see global statistics
    - Expert users see their personal statistics
    """
    if current_user.role == models.UserRole.ADMIN:
        # 管理員看到全局統計
        global_stats = crud.get_global_stats(db)
        review_activity = crud.get_review_activity(db, days=30)
        top_reviewers = crud.get_top_reviewers(db, limit=5)
        common_rejection_reasons = crud.get_common_rejection_reasons(db, limit=5)
    else:
        # 資安專家看到個人統計
        global_stats = crud.get_user_stats(db, current_user.id)
        review_activity = crud.get_user_review_activity(db, current_user.id, days=30)
        top_reviewers = []  # 個人統計不需要顯示頂尖審核員
        common_rejection_reasons = crud.get_user_rejection_reasons(db, current_user.id, limit=5)

    return schemas.DashboardStats(
        global_stats=global_stats,
        review_activity=review_activity,
        top_reviewers=top_reviewers,
        common_rejection_reasons=common_rejection_reasons
    ) 