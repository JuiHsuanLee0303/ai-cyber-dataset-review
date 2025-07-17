from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        if current_user.role == models.UserRole.ADMIN:
            global_stats = crud.get_global_stats(db)
            review_activity = crud.get_review_activity(db, days=30)
            top_reviewers = crud.get_top_reviewers(db, limit=5)
            common_rejection_reasons = crud.get_common_rejection_reasons(db, limit=5)
            model_stats = crud.get_model_stats(db)  # 新增：獲取模型統計
        else:
            global_stats = crud.get_user_stats(db, current_user.id)
            review_activity = crud.get_user_review_activity(db, current_user.id, days=30)
            top_reviewers = []
            common_rejection_reasons = crud.get_user_rejection_reasons(db, current_user.id, limit=5)
            model_stats = []  # 專家用戶不顯示模型統計

        return schemas.DashboardStats(
            global_stats=global_stats,
            review_activity=review_activity,
            top_reviewers=top_reviewers,
            common_rejection_reasons=common_rejection_reasons,
            model_stats=model_stats  # 新增：模型統計
        )
    except Exception as e:
        print(f"Error in get_dashboard_stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/models", response_model=list[schemas.ModelStats])
def get_model_statistics(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    獲取詳細的模型統計數據
    僅管理員可訪問
    """
    try:
        model_stats = crud.get_model_stats(db)
        return model_stats
    except Exception as e:
        print(f"Error in get_model_statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/models/refresh", response_model=dict)
def refresh_model_statistics(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    重新統計模型數據，清空所有審核記錄
    僅管理員可訪問
    """
    try:
        # 清空所有審核記錄並重置統計
        result = crud.refresh_model_stats(db)
        return result
    except Exception as e:
        print(f"Error in refresh_model_statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 