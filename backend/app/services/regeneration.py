from sqlalchemy.orm import Session
from app import crud
from app.services.ollama_client import OllamaClient
import json
import random

async def regenerate_dataset(db: Session, dataset_id: int, model_name: str = None):
    """
    The core logic for regenerating a dataset item using optimized prompt engineering.
    """
    print(f"Starting regeneration process for dataset ID: {dataset_id}")
    dataset = crud.get_raw_dataset(db, dataset_id)
    if not dataset:
        print(f"Dataset {dataset_id} not found for regeneration.")
        return
    
    # Set status to regenerating
    dataset.review_status = "regenerating"
    db.commit()
    print(f"Dataset {dataset_id} status set to regenerating")

    # 1. Get all rejection reasons
    rejection_logs = crud.get_rejection_reasons_for_dataset(db, dataset_id)
    reasons = [log.comment for log in rejection_logs if log.comment]
    
    print(f"Found {len(reasons)} rejection reasons for dataset {dataset_id}")
    
    # 2. Get Ollama configuration
    url_setting = crud.get_setting(db, "ollama_url")
    ollama_url = url_setting.value if url_setting else "http://ollama:11434"

    # 3. 決定使用的模型
    if model_name:
        # 使用指定的模型
        selected_model = model_name
    else:
        # 從設定中隨機選擇一個模型
        models_setting = crud.get_setting(db, "ollama_models")
        if models_setting and models_setting.value and len(models_setting.value) > 0:
            selected_model = random.choice(models_setting.value)
        else:
            selected_model = "llama3"  # 預設模型
    
    print(f"Using model: {selected_model} for regeneration")

    # 4. Create Ollama client and generate structured content
    ollama_client = OllamaClient(host=ollama_url, model=selected_model)
    
    try:
        # Use the new structured generation method
        structured_result = await ollama_client.generate_structured_dataset(
            instruction=dataset.instruction or "",
            input_text=dataset.input,
            system_prompt=dataset.system,
            source=dataset.source if dataset.source else [],
            rejection_reasons=reasons
        )
        
        # Check if generation was successful
        if structured_result["output"].startswith("Error:"):
            print(f"Failed to regenerate content for dataset {dataset_id}. Reason: {structured_result['output']}")
            return
        
        print(f"Successfully generated new structured content for dataset {dataset_id}")
        print(f"New instruction: {structured_result['instruction'][:100]}...")
        print(f"New output: {structured_result['output'][:100]}...")
        
        # 4. Update the dataset in the database
        # Add the old output to history
        history = list(dataset.history) if dataset.history else []
        
        # Get current review stats before clearing logs
        current_stats = crud.get_dataset_review_stats(db, dataset_id)
        
        # 修正：將歷史記錄轉換為二維陣列格式 [指令, 回答]
        if dataset.instruction and dataset.output:
            history.append([dataset.instruction, dataset.output])
        
        # 保存額外的元資料到系統欄位（如果需要）
        system_info = {
            "reject_count": current_stats["reject_count"],
            "accept_count": current_stats["accept_count"],
            "rejection_reasons": reasons,
            "previous_input": dataset.input
        }

        # Update with new structured content
        dataset.instruction = structured_result["instruction"]
        dataset.input = structured_result["input"]
        dataset.output = structured_result["output"]
        dataset.system = json.dumps(system_info) if system_info else None  # 保存元資料到系統欄位
        dataset.model_name = selected_model  # 新增：保存使用的模型名稱
        dataset.review_status = "pending"
        dataset.history = history
        
        # Clear all review logs for this dataset to allow re-review
        for review_log in dataset.review_logs:
            db.delete(review_log)
        
        db.commit()
        print(f"Dataset {dataset_id} has been updated with new structured content and reset for review.")
        
    except Exception as e:
        print(f"Error during regeneration process for dataset {dataset_id}: {e}")
        # Optionally, set a specific status like 'failed'
        return 