from sqlalchemy.orm import Session
from app import crud
from app.services.ollama_client import OllamaClient

async def regenerate_dataset(db: Session, dataset_id: int):
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
    model_setting = crud.get_setting(db, "ollama_model")
    url_setting = crud.get_setting(db, "ollama_url")

    model_name = model_setting.value if model_setting else "llama3"
    ollama_url = url_setting.value if url_setting else "http://ollama:11434"

    # 3. Create Ollama client and generate structured content
    ollama_client = OllamaClient(host=ollama_url, model=model_name)
    
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
        history.append({
            "instruction": dataset.instruction,
            "input": dataset.input,
            "output": dataset.output,
            "reject_count": dataset.reject_count,
            "accept_count": dataset.accept_count,
            "rejection_reasons": reasons
        })

        # Update with new structured content
        dataset.instruction = structured_result["instruction"]
        dataset.input = structured_result["input"]
        dataset.output = structured_result["output"]
        dataset.review_status = "pending"
        dataset.accept_count = 0
        dataset.reject_count = 0
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