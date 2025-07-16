from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List

from app import schemas
from app.database import models
from app.security import get_password_hash

# --- User CRUD ---

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

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

# --- Dataset CRUD ---

def get_raw_dataset(db: Session, dataset_id: int):
    return db.query(models.RawDataset).filter(models.RawDataset.id == dataset_id).first()

def get_raw_datasets(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.RawDataset)
        .options(joinedload(models.RawDataset.review_logs))
        .order_by(models.RawDataset.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

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
        history=dataset.history
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def get_final_datasets(db: Session):
    return db.query(models.RawDataset).filter(models.RawDataset.review_status == 'accepted').all()

# --- ReviewLog CRUD ---

def create_review_log(db: Session, dataset_id: int, reviewer_id: int, review: schemas.ReviewCreate):
    # Create the review log entry
    db_review_log = models.ReviewLog(
        dataset_id=dataset_id,
        reviewer_id=reviewer_id,
        result=review.result.upper(),
        comment=review.comment
    )
    db.add(db_review_log)

    # Update the counters on the dataset
    dataset = get_raw_dataset(db, dataset_id)
    if not dataset:
        # This should ideally not happen if we check existence in the API layer
        return None 

    if review.result.upper() == "ACCEPT":
        dataset.accept_count += 1
    elif review.result.upper() == "REJECT":
        dataset.reject_count += 1
    
    db.commit()
    db.refresh(db_review_log)
    return db_review_log

def get_rejection_reasons_for_dataset(db: Session, dataset_id: int):
    rejection_logs = (
        db.query(models.ReviewLog)
        .options(joinedload(models.ReviewLog.reviewer))
        .filter(models.ReviewLog.dataset_id == dataset_id)
        .filter(models.ReviewLog.result == "REJECT")
        .all()
    )

    # Map to schema, including reviewer's username
    results = []
    for log in rejection_logs:
        results.append(schemas.RejectionInfo(
            id=log.id,
            comment=log.comment,
            timestamp=log.timestamp,
            reviewer_username=log.reviewer.username
        ))
    return results

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

from sqlalchemy import func, Date
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta

def get_global_stats(db: Session) -> schemas.GlobalStats:
    total_datasets = db.query(func.count(models.RawDataset.id)).scalar()
    
    total_reviews = db.query(func.count(models.ReviewLog.id)).scalar()
    
    total_accepts = db.query(func.count(models.ReviewLog.id)).filter(models.ReviewLog.result == 'ACCEPT').scalar()
    
    total_rejects = db.query(func.count(models.ReviewLog.id)).filter(models.ReviewLog.result == 'REJECT').scalar()

    return schemas.GlobalStats(
        total_datasets=total_datasets,
        total_reviews=total_reviews,
        total_accepts=total_accepts,
        total_rejects=total_rejects
    )

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


# --- Legal Articles CRUD ---

def create_legal_articles(db: Session, articles: List[schemas.LegalArticleCreate]):
    db_articles = [models.LegalArticle(**article.model_dump()) for article in articles]
    db.add_all(db_articles)
    db.commit()
    # We need to refresh each object individually if we want to return them with IDs
    for article in db_articles:
        db.refresh(article)
    return db_articles

def get_legal_articles(db: Session, skip: int = 0, limit: int = 100):
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
