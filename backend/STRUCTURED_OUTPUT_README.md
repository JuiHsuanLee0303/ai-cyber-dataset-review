# Ollama 結構化輸出功能使用指南

## 概述

本專案已整合 Ollama v0.5.0+ 的結構化輸出功能，透過 JSON schema 來約束模型輸出格式，確保回應的一致性和可預測性。

## 功能特色

### ✅ 支援的模型
根據實務經驗，以下模型對結構化輸出有良好的支援：

| 模型 | 支援度 | 建議用途 |
|------|--------|----------|
| `llama3.1:8b` / `llama3.2:8b` | ⭐⭐⭐⭐⭐ | 最佳選擇，穩定可靠 |
| `qwen3:1.7b` / `qwen3:2.5b` | ⭐⭐⭐⭐ | 表現優良，中文支援好 |
| `gemma2:9b` / `phi3:3.8b` | ⭐⭐ | 較不穩定，需要驗證 |

### 🔧 核心功能

1. **JSON Schema 驗證**：使用預定義的 schema 確保輸出格式
2. **自動回退機制**：當結構化輸出失敗時，自動回退到傳統解析
3. **多種生成方法**：支援不同場景的資料集生成需求

## 使用方法

### 1. 基本結構化輸出

```python
from app.services.ollama_client import OllamaClient

# 初始化客戶端
client = OllamaClient(model="qwen3:1.7b")

# 定義自定義 schema
custom_schema = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "confidence": {"type": "number"}
    },
    "required": ["question", "answer"]
}

# 使用結構化輸出
response = await client.generate(
    "請回答什麼是資安？", 
    format_schema=custom_schema
)
```

### 2. 生成指令微調資料集

```python
# 使用預定義的資料集 schema
result = await client.generate_structured_dataset(
    instruction="請解釋政府如何提升資安能力",
    input_text="政府會做什麼來保護我們的資安？",
    system_prompt="你是一位資安專家",
    source=["資通安全管理法第4條"],
    rejection_reasons=["回答不夠具體", "缺乏實用性"]
)

print(result)
# 輸出格式：
# {
#   "instruction": "請解釋政府如何提升資安能力",
#   "input": "政府會做什麼來保護我們的資安？",
#   "output": "政府會做的事包括：培養資安人才...",
#   "history": [],
#   "system": "你是一位資安專家",
#   "source": ["資通安全管理法第4條"]
# }
```

### 3. 從法規生成資料集

```python
regulations = [
    "資通安全管理法第4條：為提升資通安全，政府應提供資源..."
]

result = await client.generate_from_regulations(regulations)
```

## 預定義 Schema

### DATASET_SCHEMA

用於生成指令微調資料集的標準 schema：

```json
{
  "type": "object",
  "properties": {
    "instruction": {
      "type": "string",
      "description": "明確的指令內容，要求模型回答資安相關問題"
    },
    "input": {
      "type": "string", 
      "description": "輸入內容（使用者的問題或需求）"
    },
    "output": {
      "type": "string",
      "description": "期望的輸出內容，準確、實用且依照法規依據回答"
    },
    "history": {
      "type": "array",
      "items": {"type": "string"},
      "description": "對話紀錄（如果有的話）"
    },
    "system": {
      "type": "string",
      "description": "系統提示詞"
    },
    "source": {
      "type": "array",
      "items": {"type": "string"},
      "description": "法規依據來源"
    }
  },
  "required": ["instruction", "input", "output"]
}
```

## 測試與驗證

### 運行測試腳本

```bash
cd backend
python test_structured_output.py
```

測試腳本會：
1. 測試基本結構化輸出功能
2. 驗證不同方法的運作
3. 測試多個模型的相容性

### 手動測試

```python
import asyncio
from app.services.ollama_client import OllamaClient

async def test():
    client = OllamaClient(model="qwen3:1.7b")
    
    # 簡單測試
    response = await client.generate(
        "生成一個包含姓名和年齡的 JSON", 
        format_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
    )
    
    print(response)

asyncio.run(test())
```

## 最佳實踐

### 1. 模型選擇
- **推薦**：使用 `llama3.1:8b` 或 `qwen3:1.7b`
- **避免**：Gemma 和 Phi 系列（除非經過測試驗證）

### 2. Schema 設計
- 保持 schema 簡潔明確
- 使用 `description` 欄位提供清晰的指導
- 只將必要欄位設為 `required`

### 3. 錯誤處理
- 總是包含 JSON 解析的錯誤處理
- 提供回退機制以處理結構化輸出失敗的情況

### 4. 提示詞優化
- 在提示詞中明確要求 JSON 格式輸出
- 提供範例來指導模型

## 故障排除

### 常見問題

1. **JSON 解析錯誤**
   - 檢查模型是否支援結構化輸出
   - 嘗試使用更簡單的 schema
   - 確認 Ollama 版本 >= v0.5.0

2. **模型回應不穩定**
   - 切換到 `llama3.1` 或 `qwen` 系列
   - 簡化 schema 結構
   - 增加提示詞的明確性

3. **連接問題**
   - 確認 Ollama 服務正在運行
   - 檢查連接地址和端口
   - 驗證模型是否已下載

### 除錯技巧

```python
# 啟用詳細日誌
import logging
logging.basicConfig(level=logging.DEBUG)

# 檢查原始回應
response = await client.generate(prompt, format_schema=schema)
print(f"原始回應: {response}")

# 驗證 JSON 格式
try:
    parsed = json.loads(response)
    print("JSON 解析成功")
except json.JSONDecodeError as e:
    print(f"JSON 解析失敗: {e}")
```

## 版本要求

- Ollama >= v0.5.0
- Python >= 3.8
- httpx >= 0.24.0

## 參考資源

- [Ollama 結構化輸出官方文檔](https://ollama.com/blog/structured-outputs)
- [JSON Schema 規範](https://json-schema.org/)
- [模型相容性討論](https://www.reddit.com/r/LocalLLaMA/comments/1jflouy/structured_outputs_with_ollama_whats_your_recipe/) 