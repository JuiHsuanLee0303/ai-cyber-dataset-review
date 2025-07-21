from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_user
from app.api.v1.auth import get_current_admin_user
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
        url_setting = crud.get_setting(db, "ollama_url")
        ollama_url = url_setting.value if url_setting else "http://ollama:11434"

        # 使用指定的模型或從設定中獲取第一個可用模型
        if request.model_name:
            model_name = request.model_name
        else:
            # 從多模型設定中獲取第一個模型
            models_setting = crud.get_setting(db, "ollama_models")
            if models_setting and models_setting.value and len(models_setting.value) > 0:
                model_name = models_setting.value[0]  # 使用第一個模型作為預設
            else:
                model_name = "llama3"  # 預設模型

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
        
        # Add source and model name to the generated data
        generated_data["source"] = selected_articles
        generated_data["model_name"] = model_name
        
        return schemas.GeneratedDataset(**generated_data)
        
    except Exception as e:
        print(f"Error generating dataset: {e}")
        raise HTTPException(status_code=500, detail=f"生成資料失敗: {str(e)}")

@router.post("/batch-generate-from-regulations", response_model=schemas.BatchGeneratedDataset)
async def batch_generate_datasets_from_regulations(
    request: schemas.BatchGenerateFromRegulationsRequest,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Generate multiple datasets from selected legal regulations using Ollama.
    Supports random selection of regulations for each generation.
    Only accessible by admin users.
    """
    try:
        # Get Ollama configuration
        url_setting = crud.get_setting(db, "ollama_url")
        ollama_url = url_setting.value if url_setting else "http://ollama:11434"

        # 使用指定的模型或從設定中獲取第一個可用模型
        if request.model_name:
            model_name = request.model_name
        else:
            # 從多模型設定中獲取第一個模型
            models_setting = crud.get_setting(db, "ollama_models")
            if models_setting and models_setting.value and len(models_setting.value) > 0:
                model_name = models_setting.value[0]  # 使用第一個模型作為預設
            else:
                model_name = "llama3"  # 預設模型

        # Create Ollama client
        ollama_client = OllamaClient(host=ollama_url, model=model_name)
        
        # Get all available legal articles
        all_articles = []
        
        # 如果啟用隨機選擇且沒有選擇法規，使用所有可用的法規
        if request.random_selection and not request.selected_article_ids:
            all_available_articles = db.query(models.LegalArticle).all()
            for article in all_available_articles:
                all_articles.append({
                    'id': article.id,
                    'title': article.title,
                    'number': article.number,
                    'content': article.content
                })
        else:
            # 使用選擇的法規
            for article_id in request.selected_article_ids:
                article = db.query(models.LegalArticle).filter(models.LegalArticle.id == article_id).first()
                if article:
                    all_articles.append({
                        'id': article.id,
                        'title': article.title,
                        'number': article.number,
                        'content': article.content
                    })
        
        if not all_articles:
            raise HTTPException(status_code=400, detail="請選擇至少一個法規條文")
        
        generated_datasets = []
        success_count = 0
        failed_count = 0
        
        # Generate multiple datasets
        for i in range(request.batch_size):
            try:
                # Randomly select regulations if enabled
                if request.random_selection and len(all_articles) > 1:
                    # Randomly select 1-3 articles for each generation
                    import random
                    num_articles = random.randint(1, min(3, len(all_articles)))
                    selected_articles = random.sample(all_articles, num_articles)
                else:
                    # Use all selected articles
                    selected_articles = all_articles
                
                # Prepare article contents
                article_contents = []
                article_titles = []
                for article in selected_articles:
                    article_titles.append(f"{article['title']}第{article['number']}條")
                    article_contents.append(f"{article['title']}第{article['number']}條：{article['content']}")
                
                # Generate structured dataset
                generated_data = await ollama_client.generate_from_regulations(article_contents)
                
                # Add source and model name to the generated data
                generated_data["source"] = article_titles
                generated_data["model_name"] = model_name
                
                generated_datasets.append(schemas.GeneratedDataset(**generated_data))
                success_count += 1
                
            except Exception as e:
                print(f"Error generating dataset {i+1}: {e}")
                failed_count += 1
                continue
        
        return schemas.BatchGeneratedDataset(
            datasets=generated_datasets,
            total_generated=request.batch_size,
            success_count=success_count,
            failed_count=failed_count
        )
        
    except Exception as e:
        print(f"Error in batch generation: {e}")
        raise HTTPException(status_code=500, detail=f"批量生成資料失敗: {str(e)}")

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

@router.post("/batch-confirm-generated", response_model=List[schemas.RawDataset], status_code=status.HTTP_201_CREATED)
def batch_confirm_generated_datasets(
    datasets: List[schemas.RawDatasetCreate],
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Confirm and save multiple generated datasets to the database.
    Only accessible by admin users.
    """
    created_datasets = []
    for dataset in datasets:
        created_dataset = crud.create_raw_dataset(db=db, dataset=dataset)
        created_datasets.append(created_dataset)
    return created_datasets

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

# Final dataset routes (must come before generic /{dataset_id} routes)
@router.get("/final", response_model=List[schemas.FinalDataset])
def read_final_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all datasets that have been moved to the final dataset.
    This is for the final dataset management page.
    """
    datasets = crud.get_final_datasets(db, skip=skip, limit=limit)
    return datasets

@router.delete("/final", response_model=dict)
def delete_all_final_datasets(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete all final datasets.
    Only accessible by admin users.
    """
    count = crud.delete_all_final_datasets(db)
    return {"message": f"Successfully deleted {count} final datasets", "deleted_count": count}

@router.delete("/final/{dataset_id}", response_model=schemas.FinalDataset)
def delete_final_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete a specific final dataset.
    Only accessible by admin users.
    """
    db_dataset = crud.delete_final_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Final dataset not found")
    return db_dataset

# Generic dataset routes (must come after specific routes)
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

@router.post("/{dataset_id}/regenerate", status_code=status.HTTP_202_ACCEPTED)
def manual_regenerate_dataset(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user),
    model_name: str = None  # 新增：可選的模型參數
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
    
    # Add regeneration task to background with model parameter
    background_tasks.add_task(regenerate_dataset, db, dataset_id, model_name)
    
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
