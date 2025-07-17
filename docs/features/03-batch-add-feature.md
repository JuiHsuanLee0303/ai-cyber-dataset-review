# 批量新增資料功能說明

## 🎯 功能概述

在待審核資料集管理頁面中增加批量新增資料功能，支援貼上JSON格式文字或上傳JSON檔案，大幅提升資料導入效率。

## 🎨 前端實現

### 1. 批量新增按鈕

在頁面頂部添加紫色「批量新增」按鈕：

```html
<button @click="openBatchModal()" class="px-4 py-2 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 flex items-center space-x-2">
  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
  </svg>
  <span>批量新增</span>
</button>
```

### 2. 批量新增Modal

提供兩種輸入方式：

#### 文字輸入模式
- 大型文字區域，支援貼上JSON格式文字
- 提供格式範例作為placeholder
- 即時語法高亮顯示

#### 檔案上傳模式
- 支援.json檔案上傳
- 自動讀取檔案內容
- 檔案格式驗證

### 3. 資料預覽功能

```html
<!-- Preview -->
<div v-if="batchPreview.length > 0" class="mb-6">
  <h4 class="text-lg font-semibold mb-3">預覽 ({{ batchPreview.length }} 筆資料)</h4>
  <div class="max-h-64 overflow-y-auto border border-gray-200 rounded-lg p-4 bg-gray-50">
    <div v-for="(item, index) in batchPreview" :key="index" class="mb-3 p-3 bg-white rounded border">
      <div class="text-sm">
        <div class="font-medium text-gray-800">#{{ index + 1 }}</div>
        <div class="text-gray-600 mt-1">
          <div><strong>指令:</strong> {{ item.instruction || '無' }}</div>
          <div><strong>輸入:</strong> {{ item.input || '無' }}</div>
          <div><strong>輸出:</strong> {{ item.output || '無' }}</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 🔧 後端實現

### 1. 批量新增API端點

```python
@router.post("/batch", response_model=List[schemas.RawDataset], status_code=status.HTTP_201_CREATED)
def create_batch_datasets(
    datasets: List[schemas.RawDatasetCreate],
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Create multiple datasets in batch.
    Only accessible by admin users.
    """
    if not datasets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No datasets provided"
        )
    
    if len(datasets) > 100:  # Limit batch size
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Batch size cannot exceed 100 datasets"
        )
    
    created_datasets = []
    for dataset in datasets:
        try:
            created_dataset = crud.create_raw_dataset(db=db, dataset=dataset)
            created_datasets.append(created_dataset)
        except Exception as e:
            # Rollback on error
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create dataset: {str(e)}"
            )
    
    return created_datasets
```

### 2. 安全限制

- 僅管理員用戶可訪問
- 批量大小限制為100筆
- 事務回滾機制確保資料一致性

## 📋 支援的JSON格式

### 基本格式
```json
[
  {
    "instruction": "這個資安獎懲辦法是根據什麼法律訂出來的？",
    "input": "為什麼政府要特別訂資安獎懲規定？",
    "output": "這是根據《資通安全管理法》第15條與第19條訂定的，目的是讓公務機關能對人員在資安上的表現有明確的獎懲依據。",
    "system": "說明本辦法與母法的法律關係。",
    "history": [],
    "source": ["公務機關所屬人員資通安全事項獎懲辦法第1條"]
  },
  {
    "instruction": "每個機關可以自己訂獎懲標準嗎？",
    "input": "不同單位業務不一樣，可以自訂資安獎懲嗎？",
    "output": "可以。各公務機關可以依本辦法的原則，自訂符合自身業務特性的資安獎懲基準，但要報上級機關備查或核備。",
    "system": "解釋彈性規範與制度性要求兼顧原則。",
    "history": [],
    "source": ["公務機關所屬人員資通安全事項獎懲辦法第2條"]
  }
]
```

### 欄位說明
- **instruction** (可選): 指令內容
- **input** (可選): 輸入內容
- **output** (必填): 輸出內容
- **system** (可選): 系統提示
- **history** (可選): 歷史記錄，預設為空陣列
- **source** (可選): 資料來源，預設為空陣列

## 🔄 工作流程

### 1. 用戶操作流程
1. 點擊「批量新增」按鈕
2. 選擇輸入方式（文字或檔案）
3. 輸入或上傳JSON資料
4. 點擊「解析資料」進行驗證
5. 預覽解析結果
6. 確認無誤後點擊「確認新增」

### 2. 資料驗證流程
1. 檢查JSON格式正確性
2. 驗證是否為陣列格式
3. 檢查陣列是否為空
4. 驗證每筆資料的必要欄位
5. 標準化資料格式

### 3. 批量新增流程
1. 前端發送批量資料到後端
2. 後端驗證權限和資料格式
3. 逐筆創建資料集
4. 錯誤時回滾事務
5. 返回創建結果

## 🛡️ 錯誤處理

### 1. 前端錯誤處理
```javascript
const parseBatchData = () => {
  batchError.value = ''
  batchPreview.value = []
  
  if (!batchJsonText.value.trim()) {
    batchError.value = '請輸入 JSON 資料'
    return
  }
  
  try {
    const data = JSON.parse(batchJsonText.value)
    
    if (!Array.isArray(data)) {
      batchError.value = 'JSON 資料必須是陣列格式'
      return
    }
    
    // Validate each item
    for (let i = 0; i < data.length; i++) {
      const item = data[i]
      
      if (!item.output) {
        batchError.value = `第 ${i + 1} 筆資料缺少必要的 "output" 欄位`
        return
      }
    }
    
    batchPreview.value = validData
    
  } catch (err) {
    batchError.value = `JSON 格式錯誤: ${err.message}`
  }
}
```

### 2. 後端錯誤處理
- 資料格式驗證
- 批量大小限制
- 事務回滾機制
- 詳細錯誤訊息

## 🎯 功能特點

### 1. 多種輸入方式
- **文字輸入**: 直接貼上JSON文字
- **檔案上傳**: 上傳JSON檔案
- 自動格式驗證和解析

### 2. 即時預覽
- 解析後立即顯示預覽
- 顯示資料筆數和內容摘要
- 支援滾動查看大量資料

### 3. 資料驗證
- JSON格式驗證
- 必要欄位檢查
- 資料格式標準化

### 4. 效能優化
- 批量API端點減少網路請求
- 事務處理確保資料一致性
- 錯誤回滾機制

## 📊 使用場景

### 1. 大量資料導入
- 從其他系統匯出資料
- 批量導入現有資料集
- 測試資料快速建立

### 2. 資料遷移
- 系統升級時的資料遷移
- 不同格式資料的轉換導入
- 備份資料的恢復

### 3. 測試與開發
- 快速建立測試資料
- 開發環境的資料初始化
- 功能測試的資料準備

## 🔧 技術細節

### API 端點
```
POST /api/v1/datasets/batch
```

### 請求格式
```json
[
  {
    "instruction": "string",
    "input": "string",
    "output": "string",
    "system": "string",
    "history": [],
    "source": []
  }
]
```

### 響應格式
```json
[
  {
    "id": 1,
    "instruction": "string",
    "input": "string",
    "output": "string",
    "system": "string",
    "history": [],
    "source": [],
    "review_status": "pending",
    "accept_count": 0,
    "reject_count": 0
  }
]
```

## 🚀 後續優化建議

1. **進度顯示**: 大量資料新增時顯示進度條
2. **部分成功處理**: 支援部分資料新增成功的情況
3. **模板下載**: 提供JSON模板檔案下載
4. **資料驗證規則**: 可配置的資料驗證規則
5. **批次歷史**: 記錄批量新增的歷史記錄

---

*此功能大幅提升了資料導入效率，支援多種輸入方式，並提供完整的資料驗證和預覽功能。* 