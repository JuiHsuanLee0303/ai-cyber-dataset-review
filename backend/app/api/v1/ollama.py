import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.users import get_current_admin_user

router = APIRouter()

async def get_ollama_url(db: Session = Depends(get_db)):
    """Dependency to get the configured Ollama URL."""
    ollama_url_setting = crud.get_setting(db, "ollama_url")
    if not ollama_url_setting or not ollama_url_setting.value:
        raise HTTPException(status_code=500, detail="Ollama URL is not configured.")
    return ollama_url_setting.value

@router.post("/test-connection")
async def test_ollama_connection(
    test_request: schemas.OllamaTestRequest,
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Test connection to a given Ollama URL.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{test_request.url}/api/version", timeout=10.0)
            response.raise_for_status()
            return {"status": "success", "message": "Connection successful!", "version": response.json().get("version")}
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Failed to connect to Ollama: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/models")
async def get_ollama_models(
    ollama_url: str = Depends(get_ollama_url),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Get a list of local models from the configured Ollama instance.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ollama_url}/api/tags")
            response.raise_for_status()
            return response.json().get("models", [])
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch models from Ollama: {e}")

@router.post("/pull")
async def pull_ollama_model(
    pull_request: schemas.OllamaPullRequest,
    ollama_url: str = Depends(get_ollama_url),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Pull a model from the Ollama library. Streams the progress.
    """
    payload = {
        "model": pull_request.model_name,
        "stream": True
    }
    
    async def event_stream():
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", f"{ollama_url}/api/pull", json=payload, timeout=None) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        # The response from Ollama is a stream of JSON objects, separated by newlines.
                        # We yield each one as a server-sent event.
                        yield chunk
        except httpx.RequestError as e:
            error_message = json.dumps({"status": "error", "message": f"Failed to connect to Ollama: {str(e)}"})
            yield error_message.encode('utf-8')
        except httpx.HTTPStatusError as e:
            error_message = json.dumps({"status": "error", "message": f"Ollama API returned an error: {e.response.status_code}", "details": e.response.text})
            yield error_message.encode('utf-8')


    return StreamingResponse(event_stream(), media_type="application/x-ndjson") 