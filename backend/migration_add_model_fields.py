#!/usr/bin/env python3
"""
資料庫遷移腳本：為 RawDataset 和 FinalDataset 表添加 model_name 欄位
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """執行資料庫遷移"""
    
    # 獲取資料庫文件路徑
    db_path = Path("data/database.db")
    
    if not db_path.exists():
        print(f"資料庫文件不存在: {db_path}")
        return False
    
    try:
        # 連接資料庫
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("開始執行資料庫遷移...")
        
        # 檢查 RawDataset 表是否存在 model_name 欄位
        cursor.execute("PRAGMA table_info(raw_dataset)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'model_name' not in columns:
            print("為 RawDataset 表添加 model_name 欄位...")
            cursor.execute("ALTER TABLE raw_dataset ADD COLUMN model_name TEXT")
            print("✓ RawDataset 表遷移完成")
        else:
            print("✓ RawDataset 表已存在 model_name 欄位")
        
        # 檢查 FinalDataset 表是否存在 model_name 欄位
        cursor.execute("PRAGMA table_info(final_dataset)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'model_name' not in columns:
            print("為 FinalDataset 表添加 model_name 欄位...")
            cursor.execute("ALTER TABLE final_dataset ADD COLUMN model_name TEXT")
            print("✓ FinalDataset 表遷移完成")
        else:
            print("✓ FinalDataset 表已存在 model_name 欄位")
        
        # 更新系統設定：將 ollama_model 改為 ollama_models
        cursor.execute("SELECT key, value FROM settings WHERE key = 'ollama_model'")
        model_setting = cursor.fetchone()
        
        if model_setting:
            print("更新系統設定：將 ollama_model 改為 ollama_models...")
            # 將單一模型轉換為模型列表
            old_model = model_setting[1]
            new_models = [old_model] if old_model else []
            
            # 刪除舊設定
            cursor.execute("DELETE FROM settings WHERE key = 'ollama_model'")
            
            # 插入新設定
            cursor.execute("INSERT INTO settings (key, value) VALUES (?, ?)", 
                         ('ollama_models', str(new_models)))
            print("✓ 系統設定更新完成")
        else:
            print("✓ 系統設定無需更新")
        
        # 提交變更
        conn.commit()
        print("\n🎉 資料庫遷移完成！")
        
        # 顯示遷移結果
        print("\n遷移結果摘要：")
        cursor.execute("PRAGMA table_info(raw_dataset)")
        raw_columns = [column[1] for column in cursor.fetchall()]
        print(f"- RawDataset 表欄位: {raw_columns}")
        
        cursor.execute("PRAGMA table_info(final_dataset)")
        final_columns = [column[1] for column in cursor.fetchall()]
        print(f"- FinalDataset 表欄位: {final_columns}")
        
        cursor.execute("SELECT key, value FROM settings WHERE key = 'ollama_models'")
        models_setting = cursor.fetchone()
        if models_setting:
            print(f"- 系統設定 ollama_models: {models_setting[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 遷移失敗: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("AI 資安資料集審核系統 - 資料庫遷移工具")
    print("=" * 50)
    
    success = migrate_database()
    
    if success:
        print("\n✅ 遷移成功！系統現在支援多模型功能。")
        print("\n注意事項：")
        print("1. 請重新啟動後端服務以應用變更")
        print("2. 在系統設定中配置可用的 Ollama 模型")
        print("3. 新生成的資料將包含模型資訊")
    else:
        print("\n❌ 遷移失敗！請檢查錯誤訊息並重試。")
    
    print("=" * 50) 