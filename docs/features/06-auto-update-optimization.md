# 自動更新優化說明 - 待審核資料集管理

## 🎯 優化目標

解決重新生成完成後前端顯示狀態不自動更新的問題，讓用戶無需手動重新整理頁面即可看到最新的重新生成狀態。

## 🔄 問題描述

### 原始問題
- 當資料被拒絕達到閾值觸發重新生成時，前端會顯示「重新生成中」狀態
- 即使後端重新生成完成，前端仍會一直顯示轉圈狀態
- 用戶需要手動重新整理頁面才能看到更新後的狀態

### 影響範圍
- 用戶體驗不佳，需要頻繁手動刷新
- 無法即時了解重新生成進度
- 可能錯過重新生成完成的時機

## 🚀 解決方案

### 1. 自動輪詢機制

實現智能輪詢系統，自動檢測重新生成狀態變化：

```javascript
// 開始輪詢重新生成狀態
const startPolling = () => {
  if (isPolling.value) return
  
  isPolling.value = true
  pollingInterval.value = setInterval(async () => {
    // 每3秒檢查一次狀態變化
    const response = await instance.get('/api/v1/datasets/')
    const newDatasets = response.data
    
    // 檢查狀態變化並更新
    if (hasChanges) {
      datasets.value = newDatasets
      // 顯示完成通知
      toast.success(`${completedCount} 筆資料重新生成完成！`)
    }
  }, 3000)
}
```

### 2. 智能啟動/停止

根據資料狀態自動管理輪詢：

```javascript
const fetchDatasets = async () => {
  const response = await instance.get('/api/v1/datasets/')
  datasets.value = response.data
  
  // 檢查是否有正在重新生成的資料
  const hasRegenerating = datasets.value.some(dataset => 
    dataset.review_status === 'regenerating'
  )
  
  // 自動啟動或停止輪詢
  if (hasRegenerating && !isPolling.value) {
    startPolling()
  } else if (!hasRegenerating && isPolling.value) {
    stopPolling()
  }
}
```

### 3. 狀態變化檢測

精確檢測狀態變化，避免不必要的更新：

```javascript
// 檢查重新生成數量變化
const oldRegeneratingCount = datasets.value.filter(d => 
  d.review_status === 'regenerating'
).length
const newRegeneratingCount = newDatasets.filter(d => 
  d.review_status === 'regenerating'
).length

if (oldRegeneratingCount !== newRegeneratingCount) {
  hasChanges = true
} else {
  // 檢查個別資料狀態變化
  for (let i = 0; i < newDatasets.length; i++) {
    const newDataset = newDatasets[i]
    const oldDataset = datasets.value.find(d => d.id === newDataset.id)
    
    if (!oldDataset || oldDataset.review_status !== newDataset.review_status) {
      hasChanges = true
      break
    }
  }
}
```

## 🎨 用戶介面改進

### 1. 輪詢狀態指示器

添加視覺指示器顯示自動更新狀態：

```html
<!-- 輪詢狀態指示器 -->
<div v-if="isPolling" class="flex items-center space-x-2 text-sm text-blue-600">
  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
  <span>自動更新中...</span>
</div>
```

### 2. 手動刷新按鈕

提供手動刷新選項：

```html
<button @click="fetchDatasets" class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 flex items-center space-x-2">
  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
  </svg>
  <span>刷新</span>
</button>
```

### 3. 完成通知

重新生成完成時顯示通知：

```javascript
// 如果有重新生成完成的資料，顯示通知
if (newRegeneratingCount < oldRegeneratingCount) {
  const completedCount = oldRegeneratingCount - newRegeneratingCount
  toast.success(`${completedCount} 筆資料重新生成完成！`)
}
```

## 🔧 技術實現

### 1. 響應式狀態管理

```javascript
const datasets = ref([])
const loading = ref(true)
const error = ref(null)
const pollingInterval = ref(null)
const isPolling = ref(false)
```

### 2. 生命週期管理

```javascript
onMounted(fetchDatasets)

// 組件卸載時清理輪詢
onUnmounted(() => {
  stopPolling()
})
```

### 3. 錯誤處理

```javascript
try {
  // 輪詢邏輯
} catch (err) {
  console.error('輪詢更新失敗:', err)
  // 如果認證失敗，停止輪詢避免無限重試
  if (err.response?.status === 401 || err.response?.status === 403) {
    console.log('認證失敗，停止自動更新')
    stopPolling()
  }
}
```

## 📊 效能優化

### 1. 智能輪詢
- 只在有重新生成中資料時啟動輪詢
- 完成後自動停止，避免不必要的請求
- 3秒間隔平衡即時性和伺服器負載

### 2. 變化檢測
- 先檢查數量變化，快速判斷
- 再檢查個別狀態，精確更新
- 避免無變化的不必要更新

### 3. 資源清理
- 組件卸載時自動清理輪詢
- 避免記憶體洩漏
- 防止多個輪詢同時運行

## 🎯 使用效果

### 優化前
- 需要手動重新整理頁面
- 無法即時了解重新生成進度
- 用戶體驗不佳

### 優化後
- 自動檢測狀態變化
- 即時顯示重新生成完成通知
- 視覺指示器顯示更新狀態
- 手動刷新按鈕作為備選方案

## 🔍 監控與除錯

### 1. 控制台日誌
```javascript
console.log('開始自動更新重新生成狀態...')
console.log('檢測到狀態變化，更新資料...')
console.log(`${completedCount} 筆資料重新生成完成`)
console.log('所有重新生成完成，停止自動更新')
```

### 2. 狀態監控
- 輪詢狀態指示器
- 瀏覽器開發者工具網路面板
- 控制台錯誤日誌

## 📝 配置參數

### 輪詢間隔
```javascript
setInterval(async () => {
  // 輪詢邏輯
}, 3000) // 每3秒檢查一次
```

### 狀態檢查
```javascript
// 重新生成狀態
dataset.review_status === 'regenerating'

// 完成狀態
dataset.review_status === 'pending'
```

## 🚀 後續優化建議

1. **WebSocket 支援**：考慮使用 WebSocket 實現即時推送
2. **自適應間隔**：根據重新生成時間動態調整輪詢間隔
3. **批次更新**：支援多筆資料同時重新生成的批次處理
4. **進度顯示**：顯示重新生成的詳細進度百分比
5. **暫停/恢復**：允許用戶暫停和恢復自動更新

---

*此優化大幅提升了用戶體驗，讓重新生成狀態的監控變得自動化和即時化。* 