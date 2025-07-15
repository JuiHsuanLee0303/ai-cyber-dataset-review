import httpx
import os
from typing import List, Dict, Any

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = "llama3"):
        self.host = host
        self.model = model
        self.client = httpx.AsyncClient(base_url=self.host, timeout=60.0)

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

# Example of how to use it (optional, for direct testing)
async def main():
    client = OllamaClient()
    response = await client.generate("Why is the sky blue?")
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 