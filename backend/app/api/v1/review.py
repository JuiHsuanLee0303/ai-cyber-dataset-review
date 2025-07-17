from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.auth import get_current_user
from app.services.regeneration import regenerate_dataset

router = APIRouter()

# 常見拒絕理由列表
COMMON_REJECTION_REASONS = [
    {
        "id": "instruction_unclear",
        "label": "指令不夠清楚",
        "description": "指令描述模糊，無法明確理解要執行什麼任務",
        "category": "instruction"
    },
    {
        "id": "output_inaccurate",
        "label": "輸出內容不準確",
        "description": "AI 回答內容有錯誤或不符合事實",
        "category": "output"
    },
    {
        "id": "output_not_helpful",
        "label": "輸出內容不實用",
        "description": "回答過於理論化，缺乏實務價值",
        "category": "output"
    },
    {
        "id": "regulation_incorrect",
        "label": "法規依據錯誤",
        "description": "引用的法規條文不正確或已過時",
        "category": "source"
    },
    {
        "id": "regulation_irrelevant",
        "label": "法規依據不相關",
        "description": "引用的法規與指令內容無關",
        "category": "source"
    },
    {
        "id": "input_inappropriate",
        "label": "輸入內容不適當",
        "description": "輸入內容與資安領域無關或不合適",
        "category": "input"
    },
    {
        "id": "format_inconsistent",
        "label": "格式不一致",
        "description": "資料格式與其他資料不一致",
        "category": "format"
    },
    {
        "id": "duplicate_content",
        "label": "內容重複",
        "description": "與其他資料內容重複或過於相似",
        "category": "content"
    },
    {
        "id": "sensitive_info",
        "label": "包含敏感資訊",
        "description": "內容包含機密或敏感資訊",
        "category": "security"
    },
    {
        "id": "other",
        "label": "其他原因",
        "description": "其他未列出的拒絕原因",
        "category": "other"
    }
]

@router.get("/common-reasons", response_model=List[schemas.CommonRejectionReason])
def get_common_rejection_reasons():
    """
    Get list of common rejection reasons for reference.
    """
    return COMMON_REJECTION_REASONS

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

    # Get review statistics from ReviewLog table
    review_stats = crud.get_dataset_review_stats(db, dataset_id)
    
    # Check approval threshold and move to final dataset if met
    if review.result.upper() == "ACCEPT":
        approval_threshold_setting = crud.get_setting(db, "approval_threshold")
        approval_threshold = _extract_value(approval_threshold_setting.value) if approval_threshold_setting else 2
        
        if review_stats["accept_count"] >= approval_threshold:
            print(f"Dataset {dataset.id} has reached the approval threshold. Moving to final dataset.")
            # Move to final dataset
            # Create a comprehensive input that includes instruction and input
            comprehensive_input = ""
            if dataset.instruction:
                comprehensive_input += f"指令: {dataset.instruction}\n"
            if dataset.input:
                comprehensive_input += f"輸入: {dataset.input}\n"
            if dataset.system:
                comprehensive_input += f"系統提示: {dataset.system}\n"
            if dataset.source:
                comprehensive_input += f"來源: {', '.join(dataset.source)}"
            
            # If no structured input, use the original input
            if not comprehensive_input.strip():
                comprehensive_input = dataset.input or dataset.instruction or ""
            
            final_dataset = models.FinalDataset(
                original_input=comprehensive_input,
                final_output=dataset.output,
                raw_dataset_id=dataset.id,
                model_name=dataset.model_name  # 新增：保存模型名稱
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

        if review_stats["reject_count"] >= rejection_threshold:
            print(f"Dataset {dataset.id} has reached the rejection threshold. Adding regeneration task to background.")
            background_tasks.add_task(regenerate_dataset, db, dataset.id, None)  # 自動重新生成時隨機選擇模型
            
    return review_log 