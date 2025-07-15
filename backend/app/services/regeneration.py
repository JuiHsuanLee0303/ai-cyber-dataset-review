from sqlalchemy.orm import Session
from app import crud
from app.services.ollama_client import OllamaClient

async def regenerate_dataset(db: Session, dataset_id: int):
    """
    The core logic for regenerating a dataset item.
    """
    print(f"Starting regeneration process for dataset ID: {dataset_id}")
    dataset = crud.get_raw_dataset(db, dataset_id)
    if not dataset:
        print(f"Dataset {dataset_id} not found for regeneration.")
        return

    # 1. Get all rejection reasons
    rejection_logs = crud.get_rejection_reasons_for_dataset(db, dataset_id)
    reasons = [log.comment for log in rejection_logs if log.comment]
    
    # 2. Construct a new, structured prompt
    rejection_context = "This is a retry. The previous generated output was rejected for the following reasons:\n" + "\n".join(f"- {r}" for r in reasons)
    
    # Build the prompt from new structured fields
    prompt_parts = []
    if dataset.system_prompt:
        prompt_parts.append(f"System Prompt: {dataset.system_prompt}")
    if dataset.instruction:
        prompt_parts.append(f"Instruction: {dataset.instruction}")
    if dataset.input:
        prompt_parts.append(f"Input: {dataset.input}")

    original_request = "\n".join(prompt_parts)

    full_prompt = (
        f"The user's original request was:\n---\n{original_request}\n---\n\n"
        f"{rejection_context}\n\n"
        "Please generate a new, improved response that addresses these concerns and follows the original request."
    )

    # 3. Call Ollama to get a new generation
    model_setting = crud.get_setting(db, "ollama_model")
    url_setting = crud.get_setting(db, "ollama_url")

    model_name = model_setting.value if model_setting else "llama3"
    ollama_url = url_setting.value if url_setting else "http://ollama:11434"

    ollama_client = OllamaClient(host=ollama_url, model=model_name)
    new_output = await ollama_client.generate(full_prompt)

    if new_output.startswith("Error:"):
        print(f"Failed to regenerate content for dataset {dataset_id}. Reason: {new_output}")
        # Optionally, set a specific status like 'failed'
        return

    print(f"Successfully generated new content for dataset {dataset_id}.")

    # 4. Update the dataset in the database
    # Add the old output to history
    history = list(dataset.history) if dataset.history else []
    history.append({
        "output": dataset.generated_output,
        "reject_count": dataset.reject_count,
        "accept_count": dataset.accept_count,
    })

    dataset.output = new_output
    dataset.review_status = "pending"
    dataset.accept_count = 0
    dataset.reject_count = 0
    dataset.history = history
    
    db.commit()
    print(f"Dataset {dataset_id} has been updated and reset for review.") 