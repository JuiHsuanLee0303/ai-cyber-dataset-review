# 手動重新生成功能說明

## 🎯 功能概述

在待審核資料集管理頁面中增加手動重新生成按鈕，讓管理員可以主動觸發資料重新生成，無需等待達到拒絕閾值。

## 🔧 後端實現

### 1. API 端點

新增手動重新生成的 API 端點：

```python
@router.post("/{dataset_id}/regenerate", status_code=status.HTTP_202_ACCEPTED)
def manual_regenerate_dataset(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Manually trigger regeneration for a dataset.
    Only accessible by admin users.
    """
    # Check if dataset exists
    dataset = crud.get_raw_dataset(db, dataset_id=dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Check if dataset is already regenerating
    if dataset.review_status == "regenerating":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Dataset is already being regenerated"
        )
    
    # Add regeneration task to background
    background_tasks.add_task(regenerate_dataset, db, dataset_id)
    
    return {
        "message": f"Regeneration started for dataset {dataset_id}",
        "dataset_id": dataset_id,
        "status": "regenerating"
    }
```

### 2. 權限控制

- 僅限管理員用戶訪問
- 使用 `get_current_admin_user` 依賴進行權限驗證

### 3. 狀態檢查

- 檢查資料集是否存在
- 檢查是否已在重新生成中，避免重複觸發
- 返回 202 Accepted 狀態碼表示任務已接受

### 4. 背景任務

- 使用 FastAPI 的 `BackgroundTasks` 在背景執行重新生成
- 調用現有的 `regenerate_dataset` 函數
- 不阻塞 API 響應

## 🎨 前端實現

### 1. 手動重新生成按鈕

在每個資料卡片中添加重新生成按鈕：

```html
<!-- Manual Regenerate Button -->
<div class="mt-3 pt-3 border-t border-gray-200">
  <button 
    @click="handleManualRegenerate(item)" 
    :disabled="item.review_status === 'regenerating'"
    :class="[
      item.review_status === 'regenerating'
        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
        : 'bg-orange-50 text-orange-700 hover:bg-orange-100 border-orange-200'
    ]"
    class="w-full py-2 px-3 rounded-md border text-sm font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
  >
    <svg v-if="item.review_status === 'regenerating'" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
    </svg>
    <span>{{ item.review_status === 'regenerating' ? '重新生成中...' : '手動重新生成' }}</span>
  </button>
</div>
```

### 2. 處理函數

```javascript
const handleManualRegenerate = async (item) => {
  const confirmed = await confirm(
    '手動重新生成確認', 
    `確定要手動重新生成 ID ${item.id} 的資料嗎？此操作將使用 AI 重新生成內容。`
  )
  if (!confirmed) return
  
  try {
    const response = await instance.post(`/api/v1/datasets/${item.id}/regenerate`)
    toast.success('重新生成已開始，請稍候...')
    
    // 立即更新本地狀態為重新生成中
    const datasetIndex = datasets.value.findIndex(d => d.id === item.id)
    if (datasetIndex !== -1) {
      datasets.value[datasetIndex].review_status = 'regenerating'
    }
    
    // 如果尚未開始輪詢，則開始輪詢
    if (!isPolling.value) {
      startPolling()
    }
    
    console.log('手動重新生成已啟動:', response.data)
  } catch (err) {
    const errorMsg = `手動重新生成失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('手動重新生成失敗:', err)
  }
}
```

### 3. 視覺設計

#### 按鈕狀態
- **正常狀態**：橙色背景，可點擊
- **重新生成中**：灰色背景，禁用狀態，顯示旋轉動畫
- **懸停效果**：顏色變化過渡

#### 圖標設計
- **正常狀態**：刷新圖標
- **重新生成中**：旋轉動畫圖標

## 🔄 工作流程

### 1. 用戶操作流程
1. 管理員在待審核資料集管理頁面查看資料
2. 點擊「手動重新生成」按鈕
3. 確認對話框彈出，用戶確認操作
4. 前端發送 API 請求到後端
5. 按鈕狀態變為「重新生成中...」
6. 自動輪詢開始監控狀態變化
7. 重新生成完成後顯示通知

### 2. 後端處理流程
1. 接收手動重新生成請求
2. 驗證用戶權限（管理員）
3. 檢查資料集是否存在
4. 檢查是否已在重新生成中
5. 將重新生成任務加入背景任務隊列
6. 返回 202 Accepted 響應
7. 在背景執行重新生成邏輯

### 3. 狀態同步流程
1. 前端立即更新本地狀態為 `regenerating`
2. 開始自動輪詢（如果尚未開始）
3. 每3秒檢查狀態變化
4. 檢測到完成後更新狀態並顯示通知
5. 停止輪詢

## 🛡️ 安全與驗證

### 1. 權限控制
- 僅管理員用戶可以手動重新生成
- 使用現有的管理員權限驗證機制

### 2. 狀態驗證
- 檢查資料集是否存在
- 防止重複重新生成
- 避免無效的重新生成請求

### 3. 錯誤處理
- 完整的錯誤捕獲和顯示
- 用戶友好的錯誤訊息
- 控制台日誌記錄

## 📊 使用場景

### 1. 主動品質改進
- 管理員發現資料品質不佳時主動重新生成
- 無需等待達到拒絕閾值

### 2. 測試與驗證
- 測試重新生成功能
- 驗證 AI 模型的改進效果

### 3. 緊急修復
- 發現嚴重問題時快速重新生成
- 提高資料品質的響應速度

## 🎯 優勢特點

### 1. 靈活性
- 不受拒絕閾值限制
- 管理員可以主動控制重新生成時機

### 2. 即時性
- 立即開始重新生成
- 實時狀態更新和通知

### 3. 用戶體驗
- 直觀的按鈕設計
- 清晰的狀態指示
- 完整的操作反饋

### 4. 安全性
- 嚴格的權限控制
- 防止重複操作
- 完整的錯誤處理

## 🔧 技術細節

### API 端點
```
POST /api/v1/datasets/{dataset_id}/regenerate
```

### 請求參數
- `dataset_id` (path): 資料集 ID

### 響應格式
```json
{
  "message": "Regeneration started for dataset 123",
  "dataset_id": 123,
  "status": "regenerating"
}
```

### 錯誤響應
- `404`: 資料集不存在
- `400`: 已在重新生成中
- `401/403`: 權限不足

## 🚀 後續優化建議

1. **批次重新生成**：支援多筆資料同時重新生成
2. **重新生成原因**：記錄手動重新生成的原因
3. **進度顯示**：顯示重新生成的詳細進度
4. **取消功能**：允許取消正在進行的重新生成
5. **歷史記錄**：記錄手動重新生成的歷史

---

*此功能為管理員提供了更靈活的資料品質管理工具，提升了系統的可用性和效率。* 