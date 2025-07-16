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
        
        # 5. Rejection reasons and improvement guidance
        if rejection_reasons and len(rejection_reasons) > 0:
            prompt_parts.append("## 需要改進的地方")
            for i, reason in enumerate(rejection_reasons, 1):
                prompt_parts.append(f"{i}. {reason}")
            
            prompt_parts.append("""
## 改進要求
請根據上述問題進行改進，確保：
1. 內容準確且符合資安法規
2. 實用且可執行
3. 專業水準高
4. 沒有錯誤或誤導性資訊""")
        
        # 6. Output format requirement
        prompt_parts.append("""
## 輸出格式
請嚴格按照以下 JSON 格式輸出，確保 JSON 格式正確：

{
  "instruction": "改進後的指令，清楚明確且與資安相關",
  "input": "相關的輸入內容（如果需要的話）",
  "output": "高品質的輸出內容，符合資安法規要求且實用"
}""")
        
        full_prompt = "\n\n".join(prompt_parts)
        
        try:
            print(f"Generating structured dataset with optimized prompt...")
            response = await self.generate(full_prompt)
            
            # Try to parse JSON response
            try:
                # Clean the response to extract JSON
                response_clean = response.strip()
                
                # Find JSON object in the response
                start_idx = response_clean.find('{')
                end_idx = response_clean.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_clean[start_idx:end_idx]
                    parsed_response = json.loads(json_str)
                    
                    # Validate required fields
                    if "instruction" not in parsed_response or "output" not in parsed_response:
                        raise ValueError("Missing required fields in response")
                    
                    return {
                        "instruction": parsed_response.get("instruction", instruction),
                        "input": parsed_response.get("input", input_text),
                        "output": parsed_response.get("output", "")
                    }
                else:
                    raise ValueError("No JSON object found in response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Failed to parse JSON response: {e}")
                print(f"Raw response: {response}")
                
                # Fallback: return structured response with original instruction
                return {
                    "instruction": instruction,
                    "input": input_text,
                    "output": response
                }
                
        except Exception as e:
            print(f"Error in structured generation: {e}")
            return {
                "instruction": instruction,
                "input": input_text,
                "output": f"Error: Failed to generate structured content - {str(e)}"
            }

# Example of how to use it (optional, for direct testing)
async def main():
    client = OllamaClient()
    response = await client.generate("Why is the sky blue?")
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 