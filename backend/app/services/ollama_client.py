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

    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Generates content using the Ollama API.
        """
        full_prompt = prompt
        if context:
            # Simple context formatting, can be improved
            context_str = "\n".join(f"- {k}: {v}" for k, v in context.items())
            full_prompt = f"{prompt}\n\nPlease consider the following context:\n{context_str}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,  # We want the full response at once
            "think": False,
        }

        try:
            print(f"Sending request to Ollama with prompt: {full_prompt[:200]}...")
            response = await self.client.post("/api/generate", json=payload)
            response.raise_for_status()
            
            data = response.json()
            print("Received response from Ollama.")
            return data.get("response", "").strip()
            
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
  "input": "輸入內容（如果有的話）",
  "output": "期望的輸出內容"
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
        prompt_parts.append("1. 指令清楚明確，與資安相關")
        prompt_parts.append("2. 輸入內容提供適當的上下文")
        prompt_parts.append("3. 輸出內容準確、實用且符合法規要求")
        prompt_parts.append("4. 如果提供了拒絕原因，請針對這些問題進行改進")
        
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
        
        # 構建指令內容
        instruction = "請根據提供的法律條文，撰寫相對應的問答集"
        
        # 構建輸入內容（模擬一般用戶的提問）
        input_text = "我想了解這些法律條文的具體要求和應用方式"
        
        # 構建系統提示
        system_prompt = """你是一位資安專家，專門協助解答資安相關問題。請根據提供的法律條文，為不具有資安管理專業的用戶提供清楚易懂的解釋和建議。

要求：
1. 使用簡單明瞭的語言解釋法規要求
2. 提供實用的建議和最佳實踐
3. 確保回答準確且符合法規要求
4. 不要包含思考過程，直接提供答案
5. 請以繁體中文回答"""

        # 將法律條文作為來源資訊
        source = article_contents
        
        try:
            # 使用 generate_structured_dataset 來確保結構化輸出
            result = await self.generate_structured_dataset(
                instruction=instruction,
                input_text=input_text,
                system_prompt=system_prompt,
                source=source
            )
            
            # 確保所有必要欄位都存在
            if "system" not in result:
                result["system"] = system_prompt
            if "history" not in result:
                result["history"] = []
            if "source" not in result:
                result["source"] = source
            
            return result
            
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