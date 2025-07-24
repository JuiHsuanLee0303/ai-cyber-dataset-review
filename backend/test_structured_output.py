#!/usr/bin/env python3
"""
測試 Ollama 結構化輸出功能的腳本
"""

import asyncio
import json
from app.services.ollama_client import OllamaClient, DATASET_SCHEMA

async def test_structured_output():
    """測試結構化輸出功能"""
    
    # 初始化客戶端，使用支援結構化輸出的模型
    # 建議使用 llama3.1/3.2 或 qwen 系列
    client = OllamaClient(model="qwen3:1.7b")
    
    print("🧪 開始測試 Ollama 結構化輸出功能...")
    print(f"📋 使用的模型: {client.model}")
    print(f"🔗 連接地址: {client.host}")
    print()
    
    # 測試 1: 基本結構化輸出
    print("=" * 50)
    print("測試 1: 基本結構化輸出")
    print("=" * 50)
    
    test_prompt = """請根據資通安全管理法第4條生成一個問答集：

資通安全管理法第4條：為提升資通安全，政府應提供資源，整合民間及產業力量，提升全民資通安全意識，並推動下列事項：
一、資通安全專業人才之培育。
二、資通安全科技之研發、整合、應用、產學合作及國際交流合作。
三、資通安全產業之發展。
四、資通安全軟硬體技術規範、相關服務與審驗機制之發展。

請生成一個關於政府如何提升資安能力的問答集。"""
    
    try:
        response = await client.generate(test_prompt, format_schema=DATASET_SCHEMA)
        print("✅ 結構化輸出成功！")
        print("📄 原始回應:")
        print(response)
        print()
        
        # 嘗試解析 JSON
        try:
            parsed = json.loads(response)
            print("✅ JSON 解析成功！")
            print("📊 解析結果:")
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
            print("這可能表示模型沒有完全遵循 schema")
    
    except Exception as e:
        print(f"❌ 結構化輸出測試失敗: {e}")
    
    print()
    
    # 測試 2: 使用 generate_structured_dataset 方法
    print("=" * 50)
    print("測試 2: generate_structured_dataset 方法")
    print("=" * 50)
    
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
        print(f"❌ generate_structured_dataset 測試失敗: {e}")
    
    print()
    
    # 測試 3: 使用 generate_from_regulations 方法
    print("=" * 50)
    print("測試 3: generate_from_regulations 方法")
    print("=" * 50)
    
    regulations = [
        "資通安全管理法第4條：為提升資通安全，政府應提供資源，整合民間及產業力量，提升全民資通安全意識，並推動下列事項：一、資通安全專業人才之培育。二、資通安全科技之研發、整合、應用、產學合作及國際交流合作。三、資通安全產業之發展。四、資通安全軟硬體技術規範、相關服務與審驗機制之發展。"
    ]
    
    try:
        result = await client.generate_from_regulations(regulations)
        
        print("✅ generate_from_regulations 成功！")
        print("📊 結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ generate_from_regulations 測試失敗: {e}")
    
    print()
    print("🎉 測試完成！")

async def test_model_compatibility():
    """測試不同模型的結構化輸出相容性"""
    
    print("=" * 50)
    print("模型相容性測試")
    print("=" * 50)
    
    # 測試不同的模型
    models_to_test = [
        "qwen3:1.7b",
        "llama3.1:8b", 
        "llama3.2:8b",
        "gemma2:9b"
    ]
    
    test_prompt = "請生成一個簡單的 JSON 物件，包含 name 和 age 欄位"
    
    simple_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "age"]
    }
    
    for model in models_to_test:
        print(f"\n🔍 測試模型: {model}")
        try:
            client = OllamaClient(model=model)
            response = await client.generate(test_prompt, format_schema=simple_schema)
            
            try:
                parsed = json.loads(response)
                print(f"✅ {model}: 結構化輸出成功")
                print(f"   結果: {parsed}")
            except json.JSONDecodeError:
                print(f"⚠️  {model}: 結構化輸出失敗 (JSON 解析錯誤)")
                print(f"   原始回應: {response[:100]}...")
                
        except Exception as e:
            print(f"❌ {model}: 請求失敗 - {e}")

if __name__ == "__main__":
    print("🚀 啟動 Ollama 結構化輸出測試")
    print()
    
    # 運行測試
    asyncio.run(test_structured_output())
    print()
    asyncio.run(test_model_compatibility()) 