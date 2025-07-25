from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_admin_user

router = APIRouter()

@router.post("/", response_model=List[schemas.LegalArticle], status_code=status.HTTP_201_CREATED)
def create_articles(
    articles: List[schemas.LegalArticleCreate],
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Create one or more legal articles.
    Accepts a list of articles for batch import.
    Only accessible by admin users.
    """
    return crud.create_legal_articles(db=db, articles=articles)

@router.get("/", response_model=List[schemas.LegalArticle])
def read_articles(
    skip: int = 0,
    limit: int = 10000,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all legal articles.
    Only accessible by admin users.
    """
    return crud.get_legal_articles(db=db, skip=skip)

@router.get("/search", response_model=schemas.LegalArticle)
def search_article(
    title: str,
    number: str,
    db: Session = Depends(get_db)
):
    """
    Search for a legal article by title and number.
    Accessible by all authenticated users.
    """
    article = crud.get_legal_article_by_title_and_number(db, title=title, number=number)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/{article_id}", response_model=schemas.LegalArticle)
def update_article(
    article_id: int,
    article: schemas.LegalArticleCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Update a legal article.
    """
    db_article = crud.update_legal_article(db, article_id=article_id, article_update=article)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.delete("/{article_id}", response_model=schemas.LegalArticle)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete a legal article.
    """
    db_article = crud.delete_legal_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article 