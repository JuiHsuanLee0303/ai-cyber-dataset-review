# 多模型支援功能

## 📋 功能概述

本次重大更新為 AI 資安資料集審核系統添加了多模型支援功能，允許系統同時使用多個 Ollama 模型來生成和重新生成資料，並在資料庫中記錄每個資料所使用的模型資訊。

## 🎯 主要功能

### 1. 多模型配置
- 系統設定中支援配置多個 Ollama 模型
- 從單選模型改為多選模型勾選
- 所有勾選的模型都可以用於資料生成

### 2. 模型選擇功能
- 法規生成時可選擇使用的模型
- 手動重新生成時可選擇使用的模型
- 自動重新生成時隨機選擇可用模型

### 3. 模型資訊記錄
- 在資料庫中記錄每個資料使用的模型
- 在最終資料集中顯示生成模型
- 支援按模型分類統計

### 4. 儀表板增強
- 新增模型統計區塊
- 顯示各模型的通過率和審核次數
- 僅管理員可見

## 🔧 技術實現

### 資料庫變更
- `raw_dataset` 表新增 `model_name` 欄位
- `final_dataset` 表新增 `model_name` 欄位
- 系統設定從 `ollama_model` 改為 `ollama_models`

### 後端 API 變更
- 法規生成 API 支援 `model_name` 參數
- 重新生成 API 支援 `model_name` 參數
- 統計 API 新增模型分類統計
- 設定 API 支援多模型配置

### 前端介面變更
- 系統設定頁面改為多選模型
- 法規生成模態框新增模型選擇
- 最終資料集管理顯示模型資訊
- 儀表板新增模型統計區塊

## 📊 新增統計功能

### 模型統計
- 各模型的資料生成總數
- 各模型的審核總次數
- 各模型的通過率
- 各模型的接受/拒絕次數

## 🚀 使用指南

### 1. 配置多模型
1. 進入系統設定頁面
2. 在 Ollama 模型選擇區塊勾選要使用的模型
3. 點擊刷新列表獲取最新模型
4. 儲存設定

### 2. 法規生成
1. 在待審核資料集管理頁面點擊「從法規生成」
2. 選擇要使用的模型
3. 選擇法規條文
4. 點擊生成資料

### 3. 手動重新生成
1. 在待審核資料集管理頁面點擊「手動重新生成」
2. 系統會自動選擇可用模型
3. 確認重新生成

### 4. 查看模型資訊
1. 在最終資料集管理頁面查看生成模型
2. 在儀表板查看模型統計
3. 匯出 CSV 時包含模型資訊

## 🔄 遷移說明

### 資料庫遷移
執行遷移腳本自動更新資料庫結構：
```bash
cd backend
python migration_add_model_fields.py
```

### 設定遷移
- 原有的單一模型設定會自動轉換為模型列表
- 新系統會保持向後相容性

## ⚠️ 注意事項

1. **模型可用性**：確保所有配置的模型在 Ollama 服務中可用
2. **效能考量**：使用多個模型可能增加系統負載
3. **資料一致性**：舊資料的模型欄位為空，新資料會記錄模型資訊
4. **權限控制**：模型統計僅管理員可見

## 🎉 更新效益

1. **靈活性提升**：可根據需求選擇不同模型
2. **效能優化**：可選擇更適合的模型進行特定任務
3. **透明度增強**：清楚記錄每個資料的生成來源
4. **分析能力**：可比較不同模型的表現

## 📈 未來規劃

1. **模型效能分析**：更詳細的模型表現統計
2. **智能模型選擇**：根據任務類型自動選擇最佳模型
3. **模型版本管理**：支援模型版本控制和回滾
4. **A/B 測試**：支援模型效果對比測試 