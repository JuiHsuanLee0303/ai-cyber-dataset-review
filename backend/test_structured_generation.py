#!/usr/bin/env python3
"""
測試結構化生成功能的腳本
"""

import asyncio
import sys
import os

# 添加後端目錄到 Python 路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ollama_client import OllamaClient

async def test_structured_generation():
    """測試結構化生成功能"""
    
    print("🧪 測試結構化生成功能")
    print("=" * 50)
    
    # 創建 Ollama 客戶端 - 使用 Docker 網路地址
    client = OllamaClient(host="http://ollama:11434", model="llama3")
    
    # 測試案例 1: 基本生成
    print("\n📝 測試案例 1: 基本資安指令生成")
    print("-" * 30)
    
    result1 = await client.generate_structured_dataset(
        instruction="根據資通安全管理法分析這段程式碼的安全性",
        input_text="""```python
def process_user_data(user_input):
    query = f"INSERT INTO users (data) VALUES ('{user_input}')"
    execute_query(query)
    return "資料已儲存"
```""",
        source=["資通安全管理法第18條"],
        rejection_reasons=["內容過於簡單，缺乏具體的資安風險分析", "沒有提供實用的改善建議"]
    )
    
    print("✅ 生成結果:")
    print(f"指令: {result1['instruction']}")
    print(f"輸入: {result1['input'][:100]}..." if result1['input'] else "輸入: 無")
    print(f"輸出: {result1['output'][:200]}...")
    
    # 測試案例 2: 政策生成
    print("\n📝 測試案例 2: 資安政策生成")
    print("-" * 30)
    
    result2 = await client.generate_structured_dataset(
        instruction="生成符合個人資料保護法要求的隱私政策",
        system_prompt="你是一位資安專家，專門協助制定符合法規的資安政策",
        source=["個人資料保護法第8條", "個人資料保護法第9條"],
        rejection_reasons=["政策內容不夠具體", "缺乏實作指引"]
    )
    
    print("✅ 生成結果:")
    print(f"指令: {result2['instruction']}")
    print(f"輸入: {result2['input'][:100]}..." if result2['input'] else "輸入: 無")
    print(f"輸出: {result2['output'][:200]}...")
    
    # 測試案例 3: 事件通報
    print("\n📝 測試案例 3: 資安事件通報")
    print("-" * 30)
    
    result3 = await client.generate_structured_dataset(
        instruction="解釋資安事件通報的時限要求和程序",
        source=["資通安全事件通報及應變辦法第4條"],
        rejection_reasons=["時限說明不夠清楚", "缺少具體的通報程序步驟"]
    )
    
    print("✅ 生成結果:")
    print(f"指令: {result3['instruction']}")
    print(f"輸入: {result3['input'][:100]}..." if result3['input'] else "輸入: 無")
    print(f"輸出: {result3['output'][:200]}...")
    
    print("\n🎉 所有測試完成！")

async def test_json_parsing():
    """測試 JSON 解析功能"""
    
    print("\n🔧 測試 JSON 解析功能")
    print("=" * 50)
    
    client = OllamaClient()
    
    # 測試各種 JSON 格式
    test_responses = [
        # 標準 JSON
        '{"instruction": "測試指令", "input": "測試輸入", "output": "測試輸出"}',
        
        # 帶有額外文字的 JSON
        '這是一個測試回應。{"instruction": "測試指令", "input": "測試輸入", "output": "測試輸出"} 這是結尾。',
        
        # 多行 JSON
        '''{
  "instruction": "測試指令",
  "input": "測試輸入", 
  "output": "測試輸出"
}''',
        
        # 無效 JSON（應該回退到原始回應）
        '這不是有效的 JSON 格式'
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n📝 測試案例 {i}:")
        print(f"原始回應: {response[:100]}...")
        
        try:
            # 模擬解析過程
            response_clean = response.strip()
            start_idx = response_clean.find('{')
            end_idx = response_clean.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_clean[start_idx:end_idx]
                import json
                parsed = json.loads(json_str)
                print(f"✅ 成功解析 JSON: {parsed}")
            else:
                print("❌ 未找到 JSON 物件，使用原始回應")
        except Exception as e:
            print(f"❌ JSON 解析失敗: {e}")

if __name__ == "__main__":
    print("🚀 開始測試結構化生成功能")
    
    # 檢查 Ollama 服務是否可用
    import httpx
    
    async def check_ollama():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://ollama:11434/api/version", timeout=5.0)
                if response.status_code == 200:
                    print("✅ Ollama 服務可用")
                    return True
                else:
                    print("❌ Ollama 服務回應異常")
                    return False
        except Exception as e:
            print(f"❌ 無法連接到 Ollama 服務: {e}")
            print("請確保 Ollama 服務正在運行在 http://ollama:11434")
            return False
    
    async def main():
        if await check_ollama():
            await test_structured_generation()
            await test_json_parsing()
        else:
            print("❌ 跳過測試，因為 Ollama 服務不可用")
    
    asyncio.run(main()) 