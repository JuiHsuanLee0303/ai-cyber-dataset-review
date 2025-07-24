import httpx
import os
import json
from typing import List, Dict, Any, Optional

# OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_HOST = "http://localhost:11434"

# JSON Schema for structured outputs
DATASET_SCHEMA = {
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
            "items": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 0,
                "description": "對話歷史，格式為 [指令, 回答]"
            },
            "description": "對話紀錄（如果有的話）"
        }
    },
    "required": ["instruction", "output"]
}

class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = "llama3"):
        self.host = host
        self.model = model
        self.client = httpx.AsyncClient(base_url=self.host, timeout=300.0)  # 增加到 5 分鐘

    async def generate(self, prompt: str, history: List[Dict[str, Any]] = None, format_schema: Optional[Dict] = None) -> str:
        """
        Generates content using the Ollama API with optional structured output.
        
        Args:
            prompt: The input prompt
            history: Chat history
            format_schema: Optional JSON schema for structured output
        """
        full_prompt = prompt
        chat_history = []

        if history:
            for item in history:
                chat_history.append({
                    "role": item["role"],
                    "content": item["content"]
                })
        
        # Always add the current prompt as a user message
        chat_history.append({"role": "user", "content": full_prompt})

        payload = {
            "model": self.model,
            "messages": chat_history,
            "stream": False,
            "think": False
        }
        
        # Add format parameter if schema is provided
        if format_schema:
            payload["format"] = "json"
            payload["options"] = {
                "json_schema": format_schema
            }

        print(payload)

        try:
            print(f"Sending request to Ollama with prompt: {full_prompt[:200]}...")
            response = await self.client.post("/api/chat", json=payload)
            response.raise_for_status()
            
            data = response.json()
            print("Received response from Ollama.")
            print(data)
            
            # Extract content from the response
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()
            elif "response" in data:
                return data["response"].strip()
            else:
                return ""
            
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            # Handle specific errors if needed
            return f"Error: Could not get a response from Ollama. Status: {e.response.status_code}"
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return f"Error: Could not connect to Ollama. Details: {e}"

    async def generate_structured_dataset(self, 
                                        instruction: str, 
                                        input_text: Optional[str] = None,
                                        system_prompt: Optional[str] = None,
                                        source: Optional[List[str]] = None,
                                        rejection_reasons: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generates a structured instruction tuning dataset using optimized prompt engineering.
        Returns a dictionary with instruction, input, and output fields.
        """
        
        # Build the optimized prompt with all context
        prompt_parts = []
        
        # 1. System context and role definition
        system_context = """你是一位資安專家，專門協助生成高品質的指令微調資料集。你的任務是根據提供的指令和上下文，生成符合資安法規要求的訓練資料。

請嚴格按照指定的 JSON 格式輸出，不要包含任何其他文字。"""
        
        prompt_parts.append(system_context)
        
        # 2. Original instruction and input
        prompt_parts.append("## 原始需求")
        prompt_parts.append(f"指令: {instruction}")
        if input_text:
            prompt_parts.append(f"輸入: {input_text}")
        
        # 3. System prompt if provided
        if system_prompt:
            prompt_parts.append(f"系統提示: {system_prompt}")
        
        # 4. Source regulations
        if source and len(source) > 0:
            prompt_parts.append("## 法規依據")
            for i, src in enumerate(source, 1):
                prompt_parts.append(f"{i}. {src}")
        
        # 5. Rejection reasons if provided
        if rejection_reasons and len(rejection_reasons) > 0:
            prompt_parts.append("## 需要改進的地方")
            for i, reason in enumerate(rejection_reasons, 1):
                prompt_parts.append(f"{i}. {reason}")
        
        # 6. Final instruction
        prompt_parts.append("## 生成要求")
        prompt_parts.append("請根據上述資訊，生成一個完整的指令微調資料集項目。確保：")
        prompt_parts.append("1. 指令清楚明確，要求模型回答資安相關問題")
        prompt_parts.append("2. 輸入內容提供適當的上下文，提出與法規依據相關但不直接詢問法規內容的問題")
        prompt_parts.append("3. 輸出內容準確、實用且依照法規依據回答")
        prompt_parts.append("4. 如果提供了拒絕原因，請針對這些問題改進原始需求")
        prompt_parts.append("5. 請以繁體中文回答")

        # 7. One Shot Prompt
        prompt_parts.append("## One Shot Prompt")
        prompt_parts.append("利用資通安全管理法第4條：為提升資通安全，政府應提供資源，整合民間及產業力量，提升全民資通安全意識，並推動下列事項：\n一、資通安全專業人才之培育。\n二、資通安全科技之研發、整合、應用、產學合作及國際交流合作。\n三、資通安全產業之發展。\n四、資通安全軟硬體技術規範、相關服務與審驗機制之發展。\n前項相關事項之推動，由主管機關以國家資通安全發展方案定之。")
        prompt_parts.append("請根據上述法規，生成的指令微調資料集如下：")
        prompt_parts.append("""\"instruction\": "政府會怎麼提升大家的資安能力？",
\"input\": "政府會做什麼來保護我們的資安？",
\"output\": "政府會做的事包括：培養資安人才、推動資安技術研發、發展資安產業，以及建立資安產品與服務的標準和審查制度。",
\"history\": [
  ["什麼是資通系統、資通安全和資通安全事件？", "資通系統就是像電腦、伺服器這些用來處理資料的系統。資通安全是保護這些系統不被駭客入侵或資料被偷。資通安全事件是指系統被攻擊、出錯或造成服務中斷的情況。"]
]""")
        
        # Combine all parts
        full_prompt = "\n\n".join(prompt_parts)
        
        try:
            # Use structured output with JSON schema
            response = await self.generate(full_prompt, format_schema=DATASET_SCHEMA)
            
            # Parse JSON response
            try:
                # Try to parse the response as JSON
                result = json.loads(response)
                
                # Ensure all required fields are present
                if "instruction" not in result:
                    result["instruction"] = instruction
                if "input" not in result:
                    result["input"] = input_text or ""
                if "output" not in result:
                    result["output"] = "無法生成輸出內容"
                if "history" not in result:
                    result["history"] = []
                
                # 驗證和修正 history 格式
                if "history" in result and isinstance(result["history"], list):
                    corrected_history = []
                    for item in result["history"]:
                        if isinstance(item, list) and len(item) == 2:
                            # 正確的二維陣列格式
                            corrected_history.append(item)
                        elif isinstance(item, str):
                            # 如果是字串，可能是單一問題或回答，跳過
                            continue
                        elif isinstance(item, dict):
                            # 如果是物件，嘗試提取問題和回答
                            if "question" in item and "answer" in item:
                                corrected_history.append([item["question"], item["answer"]])
                            elif "instruction" in item and "output" in item:
                                corrected_history.append([item["instruction"], item["output"]])
                            else:
                                # 無法解析的格式，跳過
                                continue
                        else:
                            # 其他格式，跳過
                            continue
                    result["history"] = corrected_history
                else:
                    result["history"] = []
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {response}")
                
                # Fallback: return structured response
                return {
                    "instruction": instruction,
                    "input": input_text or "",
                    "output": response.strip(),
                    "history": []
                }
                
        except Exception as e:
            print(f"Generation error: {e}")
            raise e

    async def generate_from_regulations(self, article_contents: List[str]) -> Dict[str, Any]:
        """
        Generate a complete dataset from legal regulations using generate_structured_dataset.
        Returns a dictionary with instruction, input, output, system, history, and source fields.
        """
        
        prompt = []
        prompt.append("你是一位資安專家，專門協助生成高品質的指令微調資料集。你的任務是根據提供的法律條文，生成符合資安法規要求的訓練資料。")
        prompt.append("請根據以下提供的法律條文，撰寫相對應的問答集：")
        prompt.append("## 法律條文")
        for i, article in enumerate(article_contents, 1):
            prompt.append(f"{i}. {article}")
        prompt.append("## 生成要求")
        prompt.append("請根據上述資訊，生成一個完整的指令微調資料集項目。確保：")
        prompt.append("1. 指令清楚明確，要求模型回答資安相關問題")
        prompt.append("2. 輸入內容提供適當的上下文，提出與法規依據相關但不直接詢問法規內容的問題")
        prompt.append("3. 輸出內容準確、實用且依照法規依據回答")
        prompt.append("4. 如果提供了拒絕原因，請針對這些問題改進原始需求")
        prompt.append("5. 請以繁體中文回答")
        prompt.append("## One Shot Prompt")
        prompt.append("利用資通安全管理法第4條：為提升資通安全，政府應提供資源，整合民間及產業力量，提升全民資通安全意識，並推動下列事項：\n一、資通安全專業人才之培育。\n二、資通安全科技之研發、整合、應用、產學合作及國際交流合作。\n三、資通安全產業之發展。\n四、資通安全軟硬體技術規範、相關服務與審驗機制之發展。\n前項相關事項之推動，由主管機關以國家資通安全發展方案定之。")
        prompt.append("請根據上述法規，生成的指令微調資料集如下：")
        prompt.append("""\"instruction\": "政府會怎麼提升大家的資安能力？",
\"input\": "政府會做什麼來保護我們的資安？",
\"output\": "政府會做的事包括：培養資安人才、推動資安技術研發、發展資安產業，以及建立資安產品與服務的標準和審查制度。",
\"history\": [
  ["什麼是資通系統、資通安全和資通安全事件？", "資通系統就是像電腦、伺服器這些用來處理資料的系統。資通安全是保護這些系統不被駭客入侵或資料被偷。資通安全事件是指系統被攻擊、出錯或造成服務中斷的情況。"]
]""")

        full_prompt = "\n\n".join(prompt)
        
        try:
            # Use structured output with JSON schema
            response = await self.generate(full_prompt, format_schema=DATASET_SCHEMA)
            print(response)
            
            # Parse JSON response
            try:
                # Try to parse the response as JSON
                result = json.loads(response)
                
                # Ensure all required fields are present
                if "instruction" not in result:
                    result["instruction"] = "請根據資安法規回答問題"
                if "input" not in result:
                    result["input"] = "請提供資安相關的指導"
                if "output" not in result:
                    result["output"] = "無法生成輸出內容"
                if "history" not in result:
                    result["history"] = []
                
                # 驗證和修正 history 格式
                if "history" in result and isinstance(result["history"], list):
                    corrected_history = []
                    for item in result["history"]:
                        if isinstance(item, list) and len(item) == 2:
                            # 正確的二維陣列格式
                            corrected_history.append(item)
                        elif isinstance(item, str):
                            # 如果是字串，可能是單一問題或回答，跳過
                            continue
                        elif isinstance(item, dict):
                            # 如果是物件，嘗試提取問題和回答
                            if "question" in item and "answer" in item:
                                corrected_history.append([item["question"], item["answer"]])
                            elif "instruction" in item and "output" in item:
                                corrected_history.append([item["instruction"], item["output"]])
                            else:
                                # 無法解析的格式，跳過
                                continue
                        else:
                            # 其他格式，跳過
                            continue
                    result["history"] = corrected_history
                else:
                    result["history"] = []
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {response}")
                
                # Fallback: return structured response
                return {
                    "instruction": "請根據資安法規回答問題",
                    "input": "請提供資安相關的指導",
                    "output": response.strip(),
                    "history": []
                }
            
        except Exception as e:
            print(f"Generation error: {e}")
            raise e

# Example of how to use it (optional, for direct testing)
async def main():
    client = OllamaClient(model="qwen3:1.7b")
    
    print("🚀 開始測試 Ollama 客戶端所有功能")
    print("=" * 60)
    
    # 測試 1: 基本對話（無結構化輸出）
    print("\n🔍 測試 1: 基本對話（無結構化輸出）")
    print("-" * 40)
    try:
        response = await client.generate("Why is the sky blue?")
        print(f"✅ 基本對話成功")
        print(f"回應: {response[:100]}...")
    except Exception as e:
        print(f"❌ 基本對話失敗: {e}")
    
    # 測試 2: 結構化輸出
    print("\n🔍 測試 2: 結構化輸出")
    print("-" * 40)
    simple_schema = {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "問題內容"
            },
            "answer": {
                "type": "string", 
                "description": "答案內容"
            },
            "explanation": {
                "type": "string",
                "description": "詳細解釋"
            }
        },
        "required": ["question", "answer", "explanation"]
    }
    
    try:
        structured_response = await client.generate(
            "請用繁體中文回答：天空為什麼是藍色的？請提供問題、答案和詳細解釋。",
            format_schema=simple_schema
        )
        print(f"✅ 結構化輸出請求成功")
        print(f"原始回應: {structured_response}")
        
        # 嘗試解析 JSON
        try:
            parsed = json.loads(structured_response)
            print("✅ JSON 解析成功！")
            print("📊 解析結果:")
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
            print("這可能表示模型沒有完全遵循 schema")
    except Exception as e:
        print(f"❌ 結構化輸出失敗: {e}")
    
    # 測試 3: generate_structured_dataset 方法
    print("\n🔍 測試 3: generate_structured_dataset 方法")
    print("-" * 40)
    try:
        result = await client.generate_structured_dataset(
            instruction="請解釋政府如何提升資安能力",
            input_text="政府會做什麼來保護我們的資安？",
            system_prompt="你是一位資安專家",
            source=["資通安全管理法第4條"],
            rejection_reasons=["回答不夠具體", "缺乏實用性"]
        )
        print("✅ generate_structured_dataset 成功！")
        print("📊 結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ generate_structured_dataset 失敗: {e}")
    
    # 測試 4: generate_from_regulations 方法
    print("\n🔍 測試 4: generate_from_regulations 方法")
    print("-" * 40)
    regulations = [
        "資通安全管理法第4條：為提升資通安全，政府應提供資源，整合民間及產業力量，提升全民資通安全意識，並推動下列事項：一、資通安全專業人才之培育。二、資通安全科技之研發、整合、應用、產學合作及國際交流合作。三、資通安全產業之發展。四、資通安全軟硬體技術規範、相關服務與審驗機制之發展。"
    ]
    
    try:
        result = await client.generate_from_regulations(regulations)
        print("✅ generate_from_regulations 成功！")
        print("📊 結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ generate_from_regulations 失敗: {e}")
    
    # 測試 5: 帶歷史記錄的結構化對話
    print("\n🔍 測試 5: 帶歷史記錄的結構化對話")
    print("-" * 40)
    
    # 準備歷史記錄
    history = [
        {"role": "user", "content": "什麼是資安？"},
        {"role": "assistant", "content": "資安是資訊安全的簡稱，指保護資訊系統、網路和資料免受未經授權的存取、使用、揭露、中斷、修改或破壞。"},
        {"role": "user", "content": "資安有哪些主要威脅？"},
        {"role": "assistant", "content": "資安主要威脅包括：惡意軟體、網路釣魚、資料外洩、DDoS攻擊、內部威脅等。"}
    ]
    
    # 創建專門的 schema 來處理帶歷史記錄的結構化輸出
    history_schema = {
        "type": "object",
        "properties": {
            "instruction": {
                "type": "string",
                "description": "當前用戶的指令"
            },
            "input": {
                "type": "string", 
                "description": "當前用戶的輸入"
            },
            "output": {
                "type": "string",
                "description": "模型的回答"
            },
            "history": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "歷史對話，格式為 [用戶問題, 助手回答]"
                },
                "description": "之前的對話記錄"
            },
            "context_summary": {
                "type": "string",
                "description": "基於歷史記錄的上下文摘要"
            }
        },
        "required": ["instruction", "output", "history"]
    }
    
    try:
        response = await client.generate(
            "基於我們之前的對話，請詳細說明資安的重要性，並提供具體的防護建議。",
            history=history,
            format_schema=history_schema
        )
        print("✅ 帶歷史記錄的結構化對話成功！")
        print("📄 原始回應:")
        print(response)
        print()
        
        # 嘗試解析 JSON
        try:
            parsed = json.loads(response)
            print("✅ JSON 解析成功！")
            print("📊 解析結果:")
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
            
            # 驗證歷史記錄格式
            print("\n🔍 歷史記錄驗證:")
            if "history" in parsed and isinstance(parsed["history"], list):
                print(f"✅ 歷史記錄數量: {len(parsed['history'])}")
                for i, item in enumerate(parsed["history"]):
                    if isinstance(item, list) and len(item) == 2:
                        print(f"✅ history[{i}]: [問題, 回答] 格式正確")
                        print(f"   問題: {item[0][:50]}...")
                        print(f"   回答: {item[1][:50]}...")
                    else:
                        print(f"❌ history[{i}] 格式錯誤")
            
            # 驗證上下文摘要
            if "context_summary" in parsed:
                print(f"✅ 上下文摘要: {parsed['context_summary'][:100]}...")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
            print("這可能表示模型沒有完全遵循 schema")
    
    except Exception as e:
        print(f"❌ 帶歷史記錄的結構化對話失敗: {e}")
    
    # 測試 5.1: 使用 DATASET_SCHEMA 的歷史記錄測試
    print("\n🔍 測試 5.1: 使用 DATASET_SCHEMA 的歷史記錄測試")
    print("-" * 40)
    
    try:
        response = await client.generate(
            "請根據我們的對話歷史，生成一個完整的資安問答集。",
            history=history,
            format_schema=DATASET_SCHEMA
        )
        print("✅ DATASET_SCHEMA 歷史記錄測試成功！")
        print("📄 原始回應:")
        print(response)
        print()
        
        # 嘗試解析 JSON
        try:
            parsed = json.loads(response)
            print("✅ JSON 解析成功！")
            print("📊 解析結果:")
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
            
            # 驗證 DATASET_SCHEMA 格式
            print("\n🔍 DATASET_SCHEMA 格式驗證:")
            required_fields = ["instruction", "output"]
            for field in required_fields:
                if field in parsed:
                    print(f"✅ {field} 欄位存在")
                else:
                    print(f"❌ {field} 欄位缺失")
            
            if "history" in parsed and isinstance(parsed["history"], list):
                print(f"✅ history 欄位存在，包含 {len(parsed['history'])} 個歷史記錄")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
    
    except Exception as e:
        print(f"❌ DATASET_SCHEMA 歷史記錄測試失敗: {e}")
    
    
    print("\n" + "=" * 60)
    print("🎉 所有測試完成！")
    print("=" * 60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 