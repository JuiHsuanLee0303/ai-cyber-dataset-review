# 重新生成狀態顯示優化說明

## 🎯 優化目標

當資料達到拒絕閾值並觸發自動重新生成時，在前端清楚顯示「重新生成中」的狀態，讓用戶了解系統正在處理該筆資料。

## 🔧 主要改進內容

### 1. 資料庫模型擴展

#### 檔案位置：`backend/app/database/models.py`

新增 `REGENERATING` 狀態到 `ReviewStatus` 枚舉：

```python
class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    DONE = "done"
    REGENERATING = "regenerating"  # 新增：正在重新生成中
```

### 2. 重新生成服務改進

#### 檔案位置：`backend/app/services/regeneration.py`

在開始重新生成時立即更新狀態：

```python
# Set status to regenerating
dataset.review_status = "regenerating"
db.commit()
print(f"Dataset {dataset_id} status set to regenerating")
```

### 3. 前端審核頁面優化

#### 檔案位置：`frontend/src/views/Review.vue`

#### 3.1 狀態顯示區域
在資料卡片頂部添加狀態顯示：

```vue
<!-- Status Display -->
<div class="flex justify-between items-center pb-4 border-b border-gray-200">
  <div class="flex items-center space-x-4">
    <!-- 重新生成中狀態 -->
    <div v-if="currentItem.review_status === 'regenerating'" class="flex items-center space-x-2">
      <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
      <span class="px-3 py-1 bg-orange-100 text-orange-800 text-sm font-medium rounded-full">
        🔄 重新生成中
      </span>
    </div>
    <!-- 一般待審核狀態 -->
    <span v-else class="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
      📋 待審核
    </span>
    <span class="text-sm text-gray-500">
      資料 ID: {{ currentItem.id }}
    </span>
  </div>
  <div class="text-sm text-gray-500">
    審核統計: 通過 {{ currentItem.accept_count }} | 拒絕 {{ currentItem.reject_count }}
  </div>
</div>
```

#### 3.2 操作按鈕狀態管理
當資料正在重新生成時，禁用審核按鈕並顯示提示：

```vue
<!-- 重新生成中時顯示提示 -->
<div v-if="currentItem.review_status === 'regenerating'" class="flex items-center space-x-2">
  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
  <span class="text-orange-600 font-medium">正在重新生成中，請稍候...</span>
</div>
<!-- 正常審核按鈕 -->
<div v-else class="flex space-x-4">
  <button @click="showRejectModal = true">拒絕 (Reject)</button>
  <button @click="handleAccept">接受 (Accept)</button>
</div>
```

#### 3.3 跳過按鈕狀態管理
跳過按鈕也會根據重新生成狀態調整：

```vue
<button 
  @click="nextItem" 
  :disabled="currentItem.review_status === 'regenerating'"
  :class="[
    'px-8 py-3 font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-opacity-50 transition-colors duration-200',
    currentItem.review_status === 'regenerating' 
      ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
      : 'bg-gray-400 text-white hover:bg-gray-500 focus:ring-gray-300'
  ]"
>
  {{ currentItem.review_status === 'regenerating' ? '重新生成中...' : '跳過此筆' }}
</button>
```

### 4. 管理員原始資料頁面優化

#### 檔案位置：`frontend/src/views/AdminRawData.vue`

#### 4.1 新增狀態欄位
在表格中添加狀態欄位：

```vue
<th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">狀態</th>
```

#### 4.2 狀態顯示邏輯
根據不同狀態顯示對應的標籤：

```vue
<!-- 重新生成中狀態 -->
<div v-if="item.review_status === 'regenerating'" class="flex items-center space-x-2">
  <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-orange-500"></div>
  <span class="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">
    重新生成中
  </span>
</div>
<!-- 其他狀態 -->
<span v-else-if="item.review_status === 'pending'" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
  待審核
</span>
<span v-else-if="item.review_status === 'reviewing'" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
  審核中
</span>
<span v-else-if="item.review_status === 'done'" class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
  已完成
</span>
```

## 🎨 視覺設計特色

### 1. 動畫效果
- 使用 `animate-spin` 類別創建旋轉動畫
- 橙色主題表示處理中狀態
- 與其他狀態使用不同顏色區分

### 2. 狀態標籤設計
- 圓角標籤設計，視覺效果佳
- 不同狀態使用不同顏色主題
- 包含圖示增強可讀性

### 3. 按鈕狀態管理
- 重新生成中時禁用所有操作按鈕
- 按鈕文字動態變化
- 視覺反饋清楚明確

## 🔄 工作流程

### 1. 觸發重新生成
當資料被拒絕達到閾值時：
1. 系統立即將狀態設為 `regenerating`
2. 前端顯示「重新生成中」狀態
3. 禁用所有審核操作

### 2. 重新生成完成
當重新生成完成時：
1. 狀態恢復為 `pending`
2. 前端顯示「待審核」狀態
3. 重新啟用審核操作

### 3. 用戶體驗
- 用戶清楚知道哪些資料正在處理
- 避免重複操作或誤操作
- 提供即時的視覺反饋

## 📊 狀態對應表

| 狀態 | 顯示文字 | 顏色主題 | 操作權限 |
|------|----------|----------|----------|
| `pending` | 待審核 | 藍色 | 可審核 |
| `reviewing` | 審核中 | 黃色 | 可審核 |
| `regenerating` | 重新生成中 | 橙色 | 禁用操作 |
| `done` | 已完成 | 綠色 | 不可審核 |

## 🚀 預期效果

### 1. 用戶體驗提升
- 清楚了解資料處理狀態
- 避免操作衝突
- 提供即時反饋

### 2. 系統穩定性
- 防止重複操作
- 狀態管理更清晰
- 減少錯誤操作

### 3. 管理效率
- 管理員可清楚看到所有資料狀態
- 便於追蹤處理進度
- 提高管理效率

## 🔧 技術細節

### 1. 狀態同步
- 後端立即更新狀態
- 前端即時反映狀態變化
- 確保狀態一致性

### 2. 錯誤處理
- 重新生成失敗時狀態處理
- 網路錯誤時的狀態恢復
- 異常情況的處理機制

### 3. 效能考量
- 狀態更新不影響其他功能
- 動畫效果輕量化
- 響應式設計支援

---

*這些優化旨在提供更好的用戶體驗，讓用戶清楚了解系統的處理狀態，避免操作衝突，提高整體使用效率。* 