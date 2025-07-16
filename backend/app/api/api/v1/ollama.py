import httpx
from fastapi import APIRouter, HTTPException, Body, Depends, Query
from fastapi.responses import StreamingResponse
import json

from app.api.v1.settings import load_settings
from app.config import Settings


router = APIRouter()

@router.post("/test")
async def test_ollama_connection(payload: dict = Body(...)):
    """
    Test the connection to the Ollama service.
    Expects a payload like: {"url": "http://some-ollama-url:11434"}
    """
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Ollama URL is required.")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return {"message": "Ollama connection successful."}
        except httpx.RequestError as exc:
            raise HTTPException(status_code=400, detail=f"Failed to connect to Ollama at {url}. Error: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Received an error from Ollama at {url}. Status: {exc.response.status_code}, Response: {exc.response.text}"
            )

@router.get("/models")
async def get_ollama_models(url: str = Query(...)):
    """
    Get the list of local models from the Ollama service.
    """
    if not url:
        raise HTTPException(status_code=400, detail="Ollama URL is required.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{url}/api/tags")
            response.raise_for_status()
            return response.json().get("models", [])
        except httpx.RequestError as exc:
            raise HTTPException(status_code=400, detail=f"Failed to connect to Ollama: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Ollama API request failed: {exc.response.text}"
            )

@router.post("/pull")
async def pull_ollama_model(payload: dict = Body(...)):
    """
    Pull a model from the Ollama registry. This is a streaming response.
    Expects a payload like: {"model_name": "llama3", "url": "http://..."}
    """
    model_name = payload.get("model_name")
    url = payload.get("url")

    if not model_name or not url:
        raise HTTPException(status_code=400, detail="Model name and Ollama URL are required.")

    async def stream_generator():
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", f"{url}/api/pull", json={"name": model_name, "stream": True}, timeout=None) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except httpx.RequestError as exc:
                error_message = json.dumps({"error": f"Failed to connect to Ollama: {exc}"})
                yield error_message.encode('utf-8')
            except httpx.HTTPStatusError as exc:
                error_message = json.dumps({"error": f"Ollama API request failed: {exc.response.text}"})
                yield error_message.encode('utf-8')

    return StreamingResponse(stream_generator(), media_type="application/x-ndjson") 