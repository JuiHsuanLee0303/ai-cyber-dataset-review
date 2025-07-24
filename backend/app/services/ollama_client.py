import httpx
import os
import json
from typing import List, Dict, Any, Optional

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = "llama3"):
        self.host = host
        self.model = model
        self.client = httpx.AsyncClient(base_url=self.host, timeout=300.0)  # 增加到 5 分鐘

    async def generate(self, prompt: str, history: List[Dict[str, Any]] = None) -> str:
        """
        Generates content using the Ollama API.
        """
        full_prompt = prompt
        chat_history = []

        if history:
            for item in history:
                chat_history.append({
                    "role": item["role"],
                    "content": item["content"]
                })
            chat_history.append({"role": "user", "content": full_prompt})

        payload = {
            "model": self.model,
            "messages": chat_history,
            "stream": False,
            "think": False,
            "format": {
                "type": "object",
                "properties": {
                    "response": {
                        "instruction": "string",
                        "input": "string",
                        "output": "string",
                        "history": "array"
                    }
                }
            }
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

請嚴格按照以下 JSON 格式輸出，不要包含任何其他文字：
{
  "instruction": "明確的指令內容",
  "input": "輸入內容（使用者的問題或需求）",
  "output": "期望的輸出內容",
  "history": "對話紀錄（如果有的話）"
}"""
        
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
\"history\": "["什麼是資通系統、資通安全和資通安全事件？", "資通系統就是像電腦、伺服器這些用來處理資料的系統。資通安全是保護這些系統不被駭客入侵或資料被偷。資通安全事件是指系統被攻擊、出錯或造成服務中斷的情況。"]"
""")
        
        # Combine all parts
        full_prompt = "\n\n".join(prompt_parts)
        
        try:
            response = await self.generate(full_prompt)
            
            # Parse JSON response
            import json
            try:
                # Try to extract JSON from the response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = response[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback: try to parse the entire response
                    result = json.loads(response)
                
                # Ensure all required fields are present
                if "instruction" not in result:
                    result["instruction"] = instruction
                if "input" not in result:
                    result["input"] = input_text or ""
                if "output" not in result:
                    result["output"] = "無法生成輸出內容"
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {response}")
                
                # Fallback: return structured response
                return {
                    "instruction": instruction,
                    "input": input_text or "",
                    "output": response.strip(),
                    "system": system_prompt or "",
                    "history": [],
                    "source": source or []
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
\"history\": "["什麼是資通系統、資通安全和資通安全事件？", "資通系統就是像電腦、伺服器這些用來處理資料的系統。資通安全是保護這些系統不被駭客入侵或資料被偷。資通安全事件是指系統被攻擊、出錯或造成服務中斷的情況。"]"
""")

        full_prompt = "\n\n".join(prompt)
        
        try:
            response = await self.generate(full_prompt)
            print(response)
            
            # Parse JSON response
            import json
            try:
                # Try to extract JSON from the response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = response[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback: try to parse the entire response
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
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {response}")
                
                # Fallback: return structured response
                return {
                    "instruction": "請根據資安法規回答問題",
                    "input": "請提供資安相關的指導",
                    "output": response.strip(),
                    "system": "",
                    "history": [],
                    "source": article_contents
                }
            
        except Exception as e:
            print(f"Generation error: {e}")
            raise e

# Example of how to use it (optional, for direct testing)
async def main():
    client = OllamaClient()
    response = await client.generate("Why is the sky blue?")
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 