from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app import crud, schemas
from app.database import base

router = APIRouter()

def get_db():
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.LegalArticle)
def create_legal_article(article: schemas.LegalArticleCreate, db: Session = Depends(get_db)):
    return crud.create_legal_article(db=db, article=article)

@router.post("/bulk", response_model=List[schemas.LegalArticle])
def create_legal_articles(articles: List[schemas.LegalArticleCreate], db: Session = Depends(get_db)):
    return crud.create_legal_articles(db=db, articles=articles)

@router.get("/", response_model=List[schemas.LegalArticle])
def read_legal_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_legal_articles(db, skip=skip, limit=limit)
    return articles

@router.put("/{article_id}", response_model=schemas.LegalArticle)
def update_legal_article(article_id: int, article: schemas.LegalArticleUpdate, db: Session = Depends(get_db)):
    db_article = crud.update_legal_article(db, article_id=article_id, article_in=article)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.delete("/{article_id}", response_model=schemas.LegalArticle)
def delete_legal_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.delete_legal_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article 