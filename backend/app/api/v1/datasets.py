from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_user
from app.api.v1.users import get_current_admin_user
from app.services.regeneration import regenerate_dataset
from app.services.ollama_client import OllamaClient

router = APIRouter()

@router.post("/", response_model=schemas.RawDataset, status_code=status.HTTP_201_CREATED)
def create_raw_dataset(
    dataset: schemas.RawDatasetCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    return crud.create_raw_dataset(db=db, dataset=dataset)

@router.post("/generate-from-regulations", response_model=schemas.GeneratedDataset)
async def generate_dataset_from_regulations(
    request: schemas.GenerateFromRegulationsRequest,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Generate a new dataset from selected legal regulations using Ollama.
    Only accessible by admin users.
    """
    try:
        # Get Ollama configuration
        model_setting = crud.get_setting(db, "ollama_model")
        url_setting = crud.get_setting(db, "ollama_url")

        model_name = model_setting.value if model_setting else "llama3"
        ollama_url = url_setting.value if url_setting else "http://ollama:11434"

        # Create Ollama client
        ollama_client = OllamaClient(host=ollama_url, model=model_name)
        
        # Get selected legal articles with full content
        selected_articles = []
        article_contents = []
        for article_id in request.selected_article_ids:
            article = db.query(models.LegalArticle).filter(models.LegalArticle.id == article_id).first()
            if article:
                selected_articles.append(f"{article.title}第{article.number}條")
                article_contents.append(f"{article.title}第{article.number}條：{article.content}")
        
        if not selected_articles:
            raise HTTPException(status_code=400, detail="請選擇至少一個法規條文")
        
        # Generate structured dataset with new prompt
        generated_data = await ollama_client.generate_from_regulations(article_contents)
        
        # Add source to the generated data
        generated_data["source"] = selected_articles
        
        return schemas.GeneratedDataset(**generated_data)
        
    except Exception as e:
        print(f"Error generating dataset: {e}")
        raise HTTPException(status_code=500, detail=f"生成資料失敗: {str(e)}")

@router.post("/confirm-generated", response_model=schemas.RawDataset, status_code=status.HTTP_201_CREATED)
def confirm_generated_dataset(
    dataset: schemas.RawDatasetCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Confirm and save a generated dataset to the database.
    Only accessible by admin users.
    """
    return crud.create_raw_dataset(db=db, dataset=dataset)

@router.get("/", response_model=List[schemas.RawDatasetWithStats])
def read_raw_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    datasets = crud.get_raw_datasets(db, skip=skip, limit=limit)
    return datasets

@router.get("/{dataset_id}/rejections", response_model=List[schemas.RejectionInfo])
def get_rejection_reasons(
    dataset_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all rejection reasons for a specific dataset.
    Only accessible by admin users.
    """
    reasons = crud.get_rejection_reasons_for_dataset(db=db, dataset_id=dataset_id)
    if not reasons:
        # Return empty list if no rejections, or 404 if dataset does not exist?
        # Let's check if dataset exists first.
        db_dataset = crud.get_raw_dataset(db, dataset_id=dataset_id)
        if db_dataset is None:
            raise HTTPException(status_code=404, detail="Dataset not found")
    return reasons

@router.put("/{dataset_id}", response_model=schemas.RawDataset)
def update_raw_dataset(
    dataset_id: int,
    dataset_update: schemas.RawDatasetUpdate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    db_dataset = crud.update_raw_dataset(db, dataset_id=dataset_id, dataset_update=dataset_update)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset

@router.delete("/{dataset_id}", response_model=schemas.RawDataset)
def delete_raw_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    db_dataset = crud.delete_raw_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset

@router.get("/final", response_model=List[schemas.RawDataset])
def read_final_datasets(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all datasets that have been marked as 'accepted'.
    This is for the final dataset management page.
    """
    datasets = crud.get_final_datasets(db)
    return datasets

@router.post("/{dataset_id}/regenerate", status_code=status.HTTP_202_ACCEPTED)
def manual_regenerate_dataset(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Manually trigger regeneration for a dataset.
    Only accessible by admin users.
    """
    # Check if dataset exists
    dataset = crud.get_raw_dataset(db, dataset_id=dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Check if dataset is already regenerating
    if dataset.review_status == "regenerating":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Dataset is already being regenerated"
        )
    
    # Add regeneration task to background
    background_tasks.add_task(regenerate_dataset, db, dataset_id)
    
    return {
        "message": f"Regeneration started for dataset {dataset_id}",
        "dataset_id": dataset_id,
        "status": "regenerating"
    }

@router.post("/batch", response_model=List[schemas.RawDataset], status_code=status.HTTP_201_CREATED)
def create_batch_datasets(
    datasets: List[schemas.RawDatasetCreate],
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Create multiple datasets in batch.
    Only accessible by admin users.
    """
    if not datasets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No datasets provided"
        )
    
    if len(datasets) > 100:  # Limit batch size
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Batch size cannot exceed 100 datasets"
        )
    
    created_datasets = []
    for dataset in datasets:
        try:
            created_dataset = crud.create_raw_dataset(db=db, dataset=dataset)
            created_datasets.append(created_dataset)
        except Exception as e:
            # Rollback on error
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create dataset: {str(e)}"
            )
    
    return created_datasets
