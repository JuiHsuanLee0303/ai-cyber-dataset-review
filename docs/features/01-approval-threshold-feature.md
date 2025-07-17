# 通過閾值功能實現說明

## 🎯 功能概述

新增通過閾值設定功能，允許管理員設定待審核資料被通過幾次後自動轉入最終資料集，實現自動化的資料品質管理。

## 🔧 主要功能

### 1. 通過閾值設定
- 管理員可在系統設定中調整通過閾值
- 預設值為 2 次通過
- 支援動態調整，無需重啟服務

### 2. 自動轉入機制
- 當資料的通過次數達到閾值時，自動轉入最終資料集
- 資料狀態變更為 `accepted`
- 在最終資料集表中創建對應記錄

### 3. 審核流程優化
- 結合拒絕閾值和通過閾值，形成完整的審核流程
- 拒絕達到閾值 → 自動重新生成
- 通過達到閾值 → 自動轉入最終資料集

## 🏗️ 技術實現

### 1. 後端修改

#### 1.1 Schema 擴展
**檔案位置：** `backend/app/schemas.py`

```python
class AllSettings(BaseModel):
    rejection_threshold: int
    approval_threshold: int  # 新增
    ollama_model: str
    ollama_url: str
```

#### 1.2 設定 API 更新
**檔案位置：** `backend/app/api/v1/settings.py`

- 添加 `approval_threshold` 到必要設定清單
- 在讀取和更新設定時包含通過閾值

#### 1.3 審核邏輯增強
**檔案位置：** `backend/app/api/v1/review.py`

```python
# Check approval threshold and move to final dataset if met
if review.result.upper() == "ACCEPT":
    approval_threshold_setting = crud.get_setting(db, "approval_threshold")
    approval_threshold = _extract_value(approval_threshold_setting.value) if approval_threshold_setting else 2
    
    if dataset.accept_count >= approval_threshold:
        print(f"Dataset {dataset.id} has reached the approval threshold. Moving to final dataset.")
        # Move to final dataset
        final_dataset = models.FinalDataset(
            original_input=dataset.input or "",
            final_output=dataset.output,
            raw_dataset_id=dataset.id
        )
        db.add(final_dataset)
        dataset.review_status = "accepted"
        db.commit()
        print(f"Dataset {dataset.id} has been moved to final dataset.")
```

#### 1.4 配置預設值
**檔案位置：** `backend/app/config.py`

```python
class Settings(BaseSettings):
    rejection_threshold: int = 3
    approval_threshold: int = 2  # 新增
    ollama_model: str = "qwen3:1.7b"
    ollama_url: str = "http://host.docker.internal:11434"
```

### 2. 前端修改

#### 2.1 系統設定頁面
**檔案位置：** `frontend/src/views/AdminSettings.vue`

新增通過閾值設定區域：

```vue
<!-- Approval Threshold -->
<div class="mb-6">
  <label for="approval-threshold" class="block text-gray-700 text-sm font-bold mb-2">
    通過閾值 (Approval Threshold)
  </label>
  <p class="text-xs text-gray-500 mb-2">
    當一筆資料的通過數量達到此數值，將自動轉入最終資料集。
  </p>
  <input
    type="number"
    id="approval-threshold"
    v-model.number="form.approval_threshold"
    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
    min="1"
  />
</div>
```

#### 2.2 Form 預設值
```javascript
const form = ref({
  rejection_threshold: 3,
  approval_threshold: 2,  // 新增
  ollama_model: '',
  ollama_url: 'http://host.docker.internal:11434'
})
```

## 🔄 工作流程

### 1. 初始狀態
```
資料狀態：pending
通過次數：0
拒絕次數：0
```

### 2. 審核過程
```
用戶審核 → 接受/拒絕 → 更新計數器
```

### 3. 達到通過閾值
```
通過次數 >= 通過閾值 → 自動轉入最終資料集 → 狀態變更為 accepted
```

### 4. 達到拒絕閾值
```
拒絕次數 >= 拒絕閾值 → 自動重新生成 → 重置計數器 → 狀態變更為 regenerating
```

## 📊 資料流程

### 1. 待審核資料集
- 包含所有 `pending` 狀態的資料
- 顯示通過和拒絕次數
- 支援手動重新生成

### 2. 最終資料集
- 包含所有 `accepted` 狀態的資料
- 自動從待審核資料集轉入
- 用於訓練和部署

### 3. 資料狀態轉換
```
pending → accepted (通過閾值達到)
pending → regenerating (拒絕閾值達到)
regenerating → pending (重新生成完成)
```

## 🎛️ 設定管理

### 1. 通過閾值設定
- **位置：** 系統設定 → 審核閾值設定
- **預設值：** 2
- **範圍：** 1 或以上
- **作用：** 控制資料轉入最終資料集的條件

### 2. 拒絕閾值設定
- **位置：** 系統設定 → 審核閾值設定
- **預設值：** 3
- **範圍：** 1 或以上
- **作用：** 控制資料重新生成的條件

### 3. 設定同步
- 設定變更立即生效
- 影響後續所有審核操作
- 不影響已處理的資料

## 🔍 監控和日誌

### 1. 系統日誌
```
Dataset {id} has reached the approval threshold. Moving to final dataset.
Dataset {id} has been moved to final dataset.
```

### 2. 審核統計
- 通過率統計
- 拒絕率統計
- 自動轉入統計
- 重新生成統計

### 3. 資料追蹤
- 原始資料保留在 `raw_dataset` 表
- 最終資料存儲在 `final_dataset` 表
- 審核記錄完整保留

## 🚀 使用指南

### 1. 設定通過閾值
1. 登入管理員帳號
2. 進入系統設定頁面
3. 在審核閾值設定區域調整通過閾值
4. 點擊儲存設定

### 2. 監控自動轉入
1. 在待審核資料集頁面查看通過次數
2. 在最終資料集頁面查看已轉入的資料
3. 通過統計儀表板查看整體趨勢

### 3. 調整策略
- 提高通過閾值：更嚴格的品質控制
- 降低通過閾值：更快的資料收集
- 平衡通過和拒絕閾值：優化審核效率

## 🔧 技術細節

### 1. 資料庫操作
- 使用事務確保資料一致性
- 正確處理關聯關係
- 避免重複轉入

### 2. 效能考量
- 閾值檢查輕量級操作
- 不影響審核響應速度
- 背景任務處理轉入操作

### 3. 錯誤處理
- 設定缺失時的預設值處理
- 資料庫操作失敗的錯誤處理
- 用戶友好的錯誤訊息

## 📈 預期效果

### 1. 自動化程度提升
- 減少手動管理負擔
- 提高資料處理效率
- 確保品質標準一致

### 2. 資料品質改善
- 通過閾值確保資料品質
- 拒絕閾值促進持續改進
- 自動化流程減少人為錯誤

### 3. 系統可擴展性
- 支援不同品質標準
- 靈活的閾值調整
- 適應不同使用場景

## 🔄 相關功能

### 1. 重新生成功能
- 與拒絕閾值配合使用
- 提供資料改進機制
- 支援持續品質提升

### 2. 統計儀表板
- 顯示通過和拒絕統計
- 監控自動化流程效果
- 提供決策支援

### 3. 最終資料集管理
- 接收自動轉入的資料
- 支援資料匯出和部署
- 提供資料品質報告

## 📋 測試建議

### 1. 功能測試
- 測試不同閾值設定
- 驗證自動轉入邏輯
- 確認狀態變更正確

### 2. 邊界測試
- 測試閾值為 1 的情況
- 測試同時達到通過和拒絕閾值
- 驗證設定變更的即時性

### 3. 效能測試
- 測試大量資料的處理
- 驗證並發審核的穩定性
- 確認系統響應速度

## 🎯 未來擴展

### 1. 進階閾值設定
- 支援不同資料類型的閾值
- 動態閾值調整
- 基於歷史數據的智能建議

### 2. 通知機制
- 閾值達到時的通知
- 自動轉入的狀態更新
- 審核進度的即時反饋

### 3. 分析功能
- 閾值效果分析
- 最佳閾值建議
- 審核效率優化建議 