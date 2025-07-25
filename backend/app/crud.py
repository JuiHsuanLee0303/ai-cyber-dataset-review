from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, Date
from typing import List
from datetime import datetime, timedelta

from app import schemas
from app.database import models
from app.security import get_password_hash

# --- User CRUD ---

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Update user role if provided
    if user_update.role is not None:
        db_user.role = user_update.role
        
    # Update password if provided
    if user_update.password:
        db_user.password_hash = get_password_hash(user_update.password)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
        
    db.delete(db_user)
    db.commit()
    return db_user

# --- Dataset CRUD ---

def get_raw_dataset(db: Session, dataset_id: int):
    return db.query(models.RawDataset).filter(models.RawDataset.id == dataset_id).first()

def get_raw_datasets(db: Session, skip: int = 0, limit: int = 100):
    datasets = (
        db.query(models.RawDataset)
        .options(joinedload(models.RawDataset.review_logs))
        .filter(models.RawDataset.review_status.in_(['pending', 'reviewing', 'regenerating']))
        .order_by(models.RawDataset.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Add calculated review stats to each dataset
    for dataset in datasets:
        stats = get_dataset_review_stats(db, dataset.id)
        dataset.accept_count = stats["accept_count"]
        dataset.reject_count = stats["reject_count"]
    
    return datasets

def update_raw_dataset(db: Session, dataset_id: int, dataset_update: schemas.RawDatasetUpdate):
    db_dataset = get_raw_dataset(db, dataset_id)
    if not db_dataset:
        return None
    
    update_data = dataset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dataset, key, value)

    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def delete_raw_dataset(db: Session, dataset_id: int):
    db_dataset = get_raw_dataset(db, dataset_id)
    if not db_dataset:
        return None
    
    db.delete(db_dataset)
    db.commit()
    return db_dataset

def create_raw_dataset(db: Session, dataset: schemas.RawDatasetCreate):
    db_dataset = models.RawDataset(
        instruction=dataset.instruction,
        input=dataset.input,
        output=dataset.output,
        system=dataset.system,
        source=dataset.source,
        history=dataset.history,
        model_name=dataset.model_name  # 新增：保存模型名稱
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def get_final_datasets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FinalDataset).offset(skip).limit(limit).all()

def get_final_dataset(db: Session, dataset_id: int):
    return db.query(models.FinalDataset).filter(models.FinalDataset.id == dataset_id).first()

def delete_final_dataset(db: Session, dataset_id: int):
    db_dataset = get_final_dataset(db, dataset_id)
    if not db_dataset:
        return None
    
    db.delete(db_dataset)
    db.commit()
    return db_dataset

def delete_all_final_datasets(db: Session):
    """刪除所有最終資料集"""
    count = db.query(models.FinalDataset).count()
    db.query(models.FinalDataset).delete()
    db.commit()
    return count

# --- ReviewLog CRUD ---

def create_review_log(db: Session, dataset_id: int, reviewer_id: int, review: schemas.ReviewCreate):
    dataset = get_raw_dataset(db, dataset_id)
    model_name = dataset.model_name if dataset else None
    
    db_review_log = models.ReviewLog(
        dataset_id=dataset_id,
        reviewer_id=reviewer_id,
        result=review.result.upper(),
        comment=review.comment,
        model_name=model_name
    )

    if review.result.upper() == 'REJECT' and review.rejection_reason_ids:
        reasons = db.query(models.RejectionReason).filter(models.RejectionReason.id.in_(review.rejection_reason_ids)).all()
        db_review_log.rejection_reasons.extend(reasons)

    db.add(db_review_log)
    db.commit()
    db.refresh(db_review_log)
    return db_review_log

def get_rejection_reasons_for_dataset(db: Session, dataset_id: int):
    rejection_logs = (
        db.query(models.ReviewLog)
        .options(
            joinedload(models.ReviewLog.reviewer),
            joinedload(models.ReviewLog.rejection_reasons) # Eager load reasons
        )
        .filter(models.ReviewLog.dataset_id == dataset_id)
        .filter(models.ReviewLog.result == "REJECT")
        .all()
    )

    results = []
    for log in rejection_logs:
        results.append(schemas.RejectionInfo(
            id=log.id,
            comment=log.comment,
            rejection_reasons=log.rejection_reasons, # Directly use the loaded objects
            timestamp=log.timestamp,
            reviewer_username=log.reviewer.username
        ))
    return results

def get_dataset_review_stats(db: Session, dataset_id: int) -> dict:
    """從 ReviewLog 表計算指定資料集的審核統計"""
    # 計算接受次數
    accept_count = db.query(func.count(models.ReviewLog.id)).filter(
        models.ReviewLog.dataset_id == dataset_id,
        models.ReviewLog.result == "ACCEPT"
    ).scalar()
    
    # 計算拒絕次數
    reject_count = db.query(func.count(models.ReviewLog.id)).filter(
        models.ReviewLog.dataset_id == dataset_id,
        models.ReviewLog.result == "REJECT"
    ).scalar()
    
    return {
        "accept_count": accept_count,
        "reject_count": reject_count,
        "total_reviews": accept_count + reject_count
    }

# --- System Settings CRUD ---

def get_setting(db: Session, key: str):
    return db.query(models.SystemSetting).filter(models.SystemSetting.key == key).first()

def get_all_settings(db: Session):
    return db.query(models.SystemSetting).all()

def update_setting(db: Session, key: str, value):
    db_setting = get_setting(db, key)
    if db_setting:
        db_setting.value = value
    else:
        db_setting = models.SystemSetting(key=key, value=value)
        db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

def update_settings(db: Session, settings: dict):
    for key, value in settings.items():
        update_setting(db, key, value)
    return get_all_settings(db)

# --- Stats CRUD ---

def get_global_stats(db: Session) -> schemas.GlobalStats:
    # 計算總資料集數：未被接受的 RawDataset + 所有 FinalDataset（避免重複計算）
    raw_datasets_count = db.query(func.count(models.RawDataset.id)).filter(
        models.RawDataset.review_status != models.ReviewStatus.ACCEPTED
    ).scalar()
    
    final_datasets_count = db.query(func.count(models.FinalDataset.id)).scalar()
    
    total_datasets = raw_datasets_count + final_datasets_count
    
    total_reviews = db.query(func.count(models.ReviewLog.id)).scalar()
    
    total_accepts = db.query(func.count(models.ReviewLog.id)).filter(models.ReviewLog.result == 'ACCEPT').scalar()
    
    total_rejects = db.query(func.count(models.ReviewLog.id)).filter(models.ReviewLog.result == 'REJECT').scalar()

    return schemas.GlobalStats(
        total_datasets=total_datasets,
        total_reviews=total_reviews,
        total_accepts=total_accepts,
        total_rejects=total_rejects
    )

def get_user_stats(db: Session, user_id: int) -> schemas.GlobalStats:
    """獲取特定用戶的統計數據"""
    total_reviews = db.query(func.count(models.ReviewLog.id)).filter(models.ReviewLog.reviewer_id == user_id).scalar()
    
    total_accepts = db.query(func.count(models.ReviewLog.id)).filter(
        models.ReviewLog.reviewer_id == user_id,
        models.ReviewLog.result == 'ACCEPT'
    ).scalar()
    
    total_rejects = db.query(func.count(models.ReviewLog.id)).filter(
        models.ReviewLog.reviewer_id == user_id,
        models.ReviewLog.result == 'REJECT'
    ).scalar()

    # 對於個人統計，總資料集數為該用戶審核過的資料集數
    total_datasets = db.query(func.count(func.distinct(models.ReviewLog.dataset_id))).filter(
        models.ReviewLog.reviewer_id == user_id
    ).scalar()

    return schemas.GlobalStats(
        total_datasets=total_datasets,
        total_reviews=total_reviews,
        total_accepts=total_accepts,
        total_rejects=total_rejects
    )

def get_user_review_activity(db: Session, user_id: int, days: int = 30) -> list[schemas.ReviewActivity]:
    """獲取特定用戶的審核活動"""
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    results = (
        db.query(
            func.date(models.ReviewLog.timestamp).label('date'),
            func.count(models.ReviewLog.id).label('count')
        )
        .filter(
            models.ReviewLog.reviewer_id == user_id,
            func.date(models.ReviewLog.timestamp).between(start_date, end_date)
        )
        .group_by('date')
        .order_by('date')
        .all()
    )
    
    # Create a map of dates to counts
    results_map = {str(r.date): r.count for r in results}

    # Fill in missing dates with zero counts
    activity = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        activity.append(schemas.ReviewActivity(date=date_str, count=results_map.get(date_str, 0)))
        
    return activity

def get_review_activity(db: Session, days: int = 30) -> list[schemas.ReviewActivity]:
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    results = (
        db.query(
            func.date(models.ReviewLog.timestamp).label('date'),
            func.count(models.ReviewLog.id).label('count')
        )
        .filter(func.date(models.ReviewLog.timestamp).between(start_date, end_date))
        .group_by('date')
        .order_by('date')
        .all()
    )
    
    # Create a map of dates to counts
    results_map = {str(r.date): r.count for r in results}

    # Fill in missing dates with zero counts
    activity = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        activity.append(schemas.ReviewActivity(date=date_str, count=results_map.get(date_str, 0)))
        
    return activity

def get_top_reviewers(db: Session, limit: int = 5) -> list[schemas.TopReviewer]:
    results = (
        db.query(
            models.User.username,
            func.count(models.ReviewLog.id).label('review_count')
        )
        .join(models.ReviewLog, models.User.id == models.ReviewLog.reviewer_id)
        .group_by(models.User.username)
        .order_by(func.count(models.ReviewLog.id).desc())
        .limit(limit)
        .all()
    )
    return [schemas.TopReviewer(username=r.username, review_count=r.review_count) for r in results]

def get_common_rejection_reasons(db: Session, limit: int = 5) -> list[schemas.CommonRejectionReason]:
    results = (
        db.query(
            models.ReviewLog.comment,
            func.count(models.ReviewLog.id).label('count')
        )
        .filter(models.ReviewLog.result == 'REJECT', models.ReviewLog.comment.isnot(None))
        .group_by(models.ReviewLog.comment)
        .order_by(func.count(models.ReviewLog.id).desc())
        .limit(limit)
        .all()
    )
    return [schemas.CommonRejectionReason(reason=r.comment, count=r.count) for r in results]

def get_user_rejection_reasons(db: Session, user_id: int, limit: int = 5) -> list[schemas.CommonRejectionReason]:
    """獲取特定用戶的常見拒絕理由"""
    results = (
        db.query(
            models.ReviewLog.comment,
            func.count(models.ReviewLog.id).label('count')
        )
        .filter(
            models.ReviewLog.result == 'REJECT', 
            models.ReviewLog.comment.isnot(None),
            models.ReviewLog.reviewer_id == user_id
        )
        .group_by(models.ReviewLog.comment)
        .order_by(func.count(models.ReviewLog.id).desc())
        .limit(limit)
        .all()
    )
    return [schemas.CommonRejectionReason(reason=r.comment, count=r.count) for r in results]

def get_model_stats(db: Session) -> list[schemas.ModelStats]:
    """獲取按模型分類的統計數據"""
    # 從所有相關表獲取模型名稱（RawDataset, FinalDataset, ReviewLog）
    raw_models = (
        db.query(models.RawDataset.model_name)
        .filter(models.RawDataset.model_name.isnot(None))
        .distinct()
        .all()
    )
    
    final_models = (
        db.query(models.FinalDataset.model_name)
        .filter(models.FinalDataset.model_name.isnot(None))
        .distinct()
        .all()
    )
    
    # 從 ReviewLog 也獲取模型名稱（用於歷史數據）
    review_models = (
        db.query(models.ReviewLog.model_name)
        .filter(models.ReviewLog.model_name.isnot(None))
        .distinct()
        .all()
    )
    
    # 合併所有模型名稱
    all_model_names = set()
    for model in raw_models:
        if model.model_name:
            all_model_names.add(model.model_name)
    for model in final_models:
        if model.model_name:
            all_model_names.add(model.model_name)
    for model in review_models:
        if model.model_name:
            all_model_names.add(model.model_name)
    
    model_stats = []
    for model_name in all_model_names:
        # 獲取該模型的資料集總數
        # 只計算未被接受的 RawDataset（避免與 FinalDataset 重複計算）
        raw_datasets_count = db.query(func.count(models.RawDataset.id)).filter(
            models.RawDataset.model_name == model_name,
            models.RawDataset.review_status != models.ReviewStatus.ACCEPTED
        ).scalar()
        
        final_datasets_count = db.query(func.count(models.FinalDataset.id)).filter(
            models.FinalDataset.model_name == model_name
        ).scalar()
        
        total_datasets = raw_datasets_count + final_datasets_count
        
        # 獲取該模型的審核總數（直接從 ReviewLog 表查詢，不需要 JOIN）
        total_reviews = db.query(func.count(models.ReviewLog.id)).filter(
            models.ReviewLog.model_name == model_name
        ).scalar()
        
        # 獲取該模型的接受總數
        total_accepts = db.query(func.count(models.ReviewLog.id)).filter(
            models.ReviewLog.model_name == model_name,
            models.ReviewLog.result == 'ACCEPT'
        ).scalar()
        
        # 獲取該模型的拒絕總數
        total_rejects = db.query(func.count(models.ReviewLog.id)).filter(
            models.ReviewLog.model_name == model_name,
            models.ReviewLog.result == 'REJECT'
        ).scalar()
        
        # 計算通過率
        acceptance_rate = (total_accepts / total_reviews * 100) if total_reviews > 0 else 0.0
        
        model_stats.append(schemas.ModelStats(
            model_name=model_name,
            total_datasets=total_datasets,
            total_reviews=total_reviews,
            total_accepts=total_accepts,
            total_rejects=total_rejects,
            acceptance_rate=round(acceptance_rate, 1)
        ))
    
    return model_stats

def refresh_model_stats(db: Session) -> dict:
    """重新統計模型數據，清空所有 review_log 記錄"""
    
    # 1. 獲取清空前的統計資訊
    total_review_logs_before = db.query(func.count(models.ReviewLog.id)).scalar()
    
    # 2. 清空所有 ReviewLog 記錄
    db.query(models.ReviewLog).delete()
    
    # 3. 重置所有 RawDataset 的審核狀態和計數
    raw_datasets = db.query(models.RawDataset).all()
    for dataset in raw_datasets:
        dataset.review_status = models.ReviewStatus.PENDING
        dataset.accept_count = 0
        dataset.reject_count = 0
    
    # 4. 提交清空操作
    db.commit()
    
    # 5. 重新計算統計（此時所有統計都會是 0）
    model_stats = get_model_stats(db)
    
    return {
        "message": "所有審核記錄已清空，模型統計已重置",
        "model_count": len(model_stats),
        "models": [stat.model_name for stat in model_stats],
        "cleanup_info": {
            "total_review_logs_cleared": total_review_logs_before,
            "raw_datasets_reset": len(raw_datasets)
        }
    }


# --- Legal Articles CRUD ---

def create_legal_articles(db: Session, articles: List[schemas.LegalArticleCreate]):
    db_articles = [models.LegalArticle(**article.model_dump()) for article in articles]
    db.add_all(db_articles)
    db.commit()
    # We need to refresh each object individually if we want to return them with IDs
    for article in db_articles:
        db.refresh(article)
    return db_articles

def get_legal_articles(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(models.LegalArticle).offset(skip).limit(limit).all()

def get_legal_article_by_title_and_number(db: Session, title: str, number: str):
    return db.query(models.LegalArticle).filter(
        models.LegalArticle.title == title,
        models.LegalArticle.number == number
    ).first()

def update_legal_article(db: Session, article_id: int, article_update: schemas.LegalArticleCreate):
    db_article = db.query(models.LegalArticle).filter(models.LegalArticle.id == article_id).first()
    if not db_article:
        return None
    
    update_data = article_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_article, key, value)

    db.commit()
    db.refresh(db_article)
    return db_article

def delete_legal_article(db: Session, article_id: int):
    db_article = db.query(models.LegalArticle).filter(models.LegalArticle.id == article_id).first()
    if not db_article:
        return None
        
    db.delete(db_article)
    db.commit()
    return db_article

