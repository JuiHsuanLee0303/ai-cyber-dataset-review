import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
import os

from app import crud, schemas
from app.database import models
from app.database.base import get_db
from app.api.v1.users import get_current_admin_user

router = APIRouter()

async def get_ollama_url(db: Session = Depends(get_db)):
    """
    Dependency to get the configured Ollama URL.
    Priority: Environment Variable > DB Setting
    """
    env_url = os.environ.get("OLLAMA_BASE_URL")
    if env_url:
        return env_url
    
    ollama_url_setting = crud.get_setting(db, "ollama_url")
    if not ollama_url_setting or not ollama_url_setting.value:
        raise HTTPException(status_code=500, detail="Ollama URL is not configured in settings or environment variables.")
    return ollama_url_setting.value

@router.post("/test")
async def test_ollama_connection(
    test_request: schemas.OllamaTestRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Test connection to a given Ollama URL.
    """
    try:
        # 驗證 URL 格式
        if not test_request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
        
        async with httpx.AsyncClient() as client:
            # 測試 Ollama 版本端點
            response = await client.get(f"{test_request.url}/api/version", timeout=10.0)
            response.raise_for_status()
            
            version_data = response.json()
            return {
                "status": "success", 
                "message": "連線成功！", 
                "version": version_data.get("version", "未知版本")
            }
    except httpx.ConnectError as e:
        raise HTTPException(status_code=400, detail=f"無法連接到 Ollama 服務: {str(e)}")
    except httpx.TimeoutException as e:
        raise HTTPException(status_code=400, detail=f"連線超時: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Ollama 服務回應錯誤: {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"發生未預期的錯誤: {str(e)}")

@router.get("/models")
async def get_ollama_models(
    ollama_url: str = Depends(get_ollama_url),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Get a list of local models from the configured Ollama instance.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ollama_url}/api/tags", timeout=10.0)
            response.raise_for_status()
            models_data = response.json()
            return models_data.get("models", [])
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"無法從 Ollama 獲取模型列表: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取模型列表時發生錯誤: {str(e)}")

@router.post("/pull")
async def pull_ollama_model(
    pull_request: schemas.OllamaPullRequest,
    ollama_url: str = Depends(get_ollama_url),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Pull a model from the Ollama library. Streams the progress.
    """
    payload = {
        "name": pull_request.model_name,  # 修正：使用 "name" 而不是 "model"
        "stream": True
    }
    
    async def event_stream(url: str):
        try:
            json_payload = json.dumps(payload)
            headers = {'Content-Type': 'application/json'}

            async with httpx.AsyncClient() as client:
                async with client.stream(
                    method="POST", 
                    url=f"{url}/api/pull", 
                    content=json_payload, 
                    headers=headers, 
                    timeout=None
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk
        except httpx.RequestError as e:
            error_message = json.dumps({
                "status": "error", 
                "message": f"無法連接到 Ollama: {str(e)}"
            })
            yield error_message.encode('utf-8')
        except httpx.HTTPStatusError as e:
            error_message = json.dumps({
                "status": "error", 
                "message": f"Ollama API 回應錯誤: {e.response.status_code}", 
                "details": e.response.text
            })
            yield error_message.encode('utf-8')
        except Exception as e:
            error_message = json.dumps({
                "status": "error", 
                "message": f"下載過程中發生未預期錯誤: {str(e)}"
            })
            yield error_message.encode('utf-8')

    return StreamingResponse(event_stream(url=ollama_url), media_type="application/x-ndjson") 