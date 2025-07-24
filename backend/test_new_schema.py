#!/usr/bin/env python3
"""
測試新的 DATASET_SCHEMA 格式
"""

import asyncio
import json
from app.services.ollama_client import OllamaClient, DATASET_SCHEMA

async def test_new_schema():
    """測試新的 schema 格式"""
    
    client = OllamaClient(model="qwen3:1.7b")
    
    print("🧪 測試新的 DATASET_SCHEMA 格式")
    print("=" * 50)
    print(f"📋 Schema 定義:")
    print(json.dumps(DATASET_SCHEMA, ensure_ascii=False, indent=2))
    print()
    
    # 測試 1: 基本結構化輸出
    print("🔍 測試 1: 基本結構化輸出")
    print("-" * 30)
    
    test_prompt = """請生成一個關於資安的問答集，格式如下：
{
  "instruction": "用戶指令（必填）",
  "input": "用戶輸入（選填）", 
  "output": "模型回答（必填）",
  "history": [
    ["第一輪指令（選填）", "第一輪回答（選填）"],
    ["第二輪指令（選填）", "第二輪回答（選填）"]
  ]
}

請生成一個關於「什麼是資安」的問答集。"""
    
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
            
            # 驗證格式
            print("\n🔍 格式驗證:")
            if "instruction" in parsed:
                print("✅ instruction 欄位存在")
            if "output" in parsed:
                print("✅ output 欄位存在")
            if "history" in parsed and isinstance(parsed["history"], list):
                print("✅ history 欄位存在且為陣列")
                for i, item in enumerate(parsed["history"]):
                    if isinstance(item, list) and len(item) == 2:
                        print(f"✅ history[{i}] 格式正確: [指令, 回答]")
                    else:
                        print(f"❌ history[{i}] 格式錯誤")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
    
    except Exception as e:
        print(f"❌ 結構化輸出測試失敗: {e}")
    
    print()
    
    # 測試 2: 使用 generate_structured_dataset 方法
    print("🔍 測試 2: generate_structured_dataset 方法")
    print("-" * 30)
    
    try:
        result = await client.generate_structured_dataset(
            instruction="請解釋什麼是資安",
            input_text="什麼是資訊安全？",
            system_prompt="你是一位資安專家",
            source=["資通安全管理法"],
            rejection_reasons=["回答太簡單", "缺乏實例"]
        )
        
        print("✅ generate_structured_dataset 成功！")
        print("📊 結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 驗證格式
        print("\n🔍 格式驗證:")
        if "instruction" in result:
            print("✅ instruction 欄位存在")
        if "output" in result:
            print("✅ output 欄位存在")
        if "history" in result and isinstance(result["history"], list):
            print("✅ history 欄位存在且為陣列")
        
    except Exception as e:
        print(f"❌ generate_structured_dataset 測試失敗: {e}")
    
    print()
    print("🎉 測試完成！")

if __name__ == "__main__":
    asyncio.run(test_new_schema()) 