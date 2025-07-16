# 顯示模式與批量刪除功能說明

## 🎯 功能概述

為待審核資料集管理頁面增加卡片式與列表式兩種顯示方式，並提供批量刪除功能，提升用戶體驗和操作效率。

## 🎨 顯示模式功能

### 1. 顯示模式切換

在頁面頂部右側提供顯示模式切換按鈕：

```html
<!-- Display Mode Toggle -->
<div class="flex items-center space-x-2">
  <span class="text-sm font-medium text-gray-700">顯示模式:</span>
  <div class="flex bg-gray-200 rounded-lg p-1">
    <button 
      @click="displayMode = 'card'"
      :class="[displayMode === 'card' ? 'bg-white text-gray-800 shadow' : 'text-gray-600']"
      class="px-3 py-1 rounded-md text-sm font-medium transition-all"
      title="卡片式顯示"
    >
      <!-- Card Icon -->
    </button>
    <button 
      @click="displayMode = 'list'"
      :class="[displayMode === 'list' ? 'bg-white text-gray-800 shadow' : 'text-gray-600']"
      class="px-3 py-1 rounded-md text-sm font-medium transition-all"
      title="列表式顯示"
    >
      <!-- List Icon -->
    </button>
  </div>
</div>
```

### 2. 卡片式顯示 (Card View)

#### 特點
- **響應式網格佈局**: 1列 (手機) → 2列 (平板) → 3列 (桌面)
- **視覺化設計**: 卡片式佈局，清晰分隔每個資料項目
- **內容預覽**: 顯示主要欄位的截斷內容
- **互動元素**: 懸停效果和選中狀態視覺反饋

#### 佈局結構
```html
<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
  <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
    <!-- Header with checkbox, ID, status, and actions -->
    <!-- Content sections with truncated text -->
    <!-- Action buttons -->
  </div>
</div>
```

#### 內容顯示
- **指令 (Instruction)**: 綠色標籤，最多3行
- **輸出 (Output)**: 藍色標籤，最多4行
- **系統提示 (System)**: 紫色標籤，最多2行
- **輸入 (Input)**: 黃色標籤，最多2行

### 3. 列表式顯示 (List View)

#### 特點
- **表格佈局**: 緊湊的表格形式，適合大量資料
- **全選功能**: 表頭提供全選/取消全選功能
- **欄位截斷**: 長文字自動截斷並顯示省略號
- **懸停效果**: 行懸停高亮顯示

#### 表格結構
```html
<table class="min-w-full divide-y divide-gray-200">
  <thead class="bg-gray-50">
    <tr>
      <th>選擇框</th>
      <th>ID</th>
      <th>狀態</th>
      <th>指令</th>
      <th>輸入</th>
      <th>輸出</th>
      <th>統計</th>
      <th>操作</th>
    </tr>
  </thead>
  <tbody>
    <!-- Data rows -->
  </tbody>
</table>
```

## 🗑️ 批量刪除功能

### 1. 選擇機制

#### 個別選擇
- 每個資料項目都有獨立的選擇框
- 選中項目會有視覺反饋（藍色邊框）

#### 全選功能
- 列表模式下表頭提供全選/取消全選
- 支援半選狀態（部分選中）
- 動態更新選擇狀態

### 2. 批量操作介面

```html
<!-- Batch Actions -->
<div v-if="selectedItems.length > 0" class="flex items-center space-x-2">
  <span class="text-sm text-gray-600">已選擇 {{ selectedItems.length }} 項</span>
  <button 
    @click="handleBatchDelete"
    class="px-3 py-1 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 flex items-center space-x-1"
  >
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
    </svg>
    <span>批量刪除</span>
  </button>
</div>
```

### 3. 批量刪除流程

```javascript
const handleBatchDelete = async () => {
  if (selectedItems.value.length === 0) {
    toast.error('請選擇要刪除的項目')
    return
  }
  
  const confirmed = await confirm(
    '批量刪除確認', 
    `確定要刪除選中的 ${selectedItems.value.length} 筆資料嗎？此操作無法復原。`
  )
  if (!confirmed) return
  
  try {
    const promises = selectedItems.value.map(id => 
      instance.delete(`/api/v1/datasets/${id}`)
    )
    
    await Promise.all(promises)
    
    toast.success(`成功刪除 ${selectedItems.value.length} 筆資料`)
    selectedItems.value = []
    await fetchDatasets() // Refresh the list
    
  } catch (err) {
    const errorMsg = `批量刪除失敗: ${err.response?.data?.detail || '未知錯誤'}`
    toast.error(errorMsg)
    console.error('批量刪除失敗:', err)
  }
}
```

## 🔧 技術實現

### 1. 響應式變數

```javascript
// For Display Mode and Batch Operations
const displayMode = ref('card') // 'card' or 'list'
const selectedItems = ref([])
```

### 2. 全選功能

```javascript
const toggleSelectAll = () => {
  if (selectedItems.value.length === datasets.value.length) {
    selectedItems.value = []
  } else {
    selectedItems.value = datasets.value.map(item => item.id)
  }
}
```

### 3. 狀態輔助函數

```javascript
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待審核',
    'reviewing': '審核中',
    'done': '已完成',
    'regenerating': '重新生成中'
  }
  return statusMap[status] || status
}

const getStatusBadgeClass = (status) => {
  const classMap = {
    'pending': 'bg-blue-100 text-blue-800',
    'reviewing': 'bg-yellow-100 text-yellow-800',
    'done': 'bg-green-100 text-green-800',
    'regenerating': 'bg-orange-100 text-orange-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}
```

## 🎨 視覺設計

### 1. 卡片式設計

#### 選中狀態
```css
.ring-2.ring-blue-500 {
  /* 藍色邊框表示選中 */
}
```

#### 懸停效果
```css
.hover\:shadow-lg {
  /* 懸停時陰影加深 */
}
```

### 2. 列表式設計

#### 表格樣式
```css
.hover\:bg-gray-50 {
  /* 行懸停背景色 */
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

### 3. 狀態標籤

#### 顏色系統
- **待審核**: 藍色 (`bg-blue-100 text-blue-800`)
- **審核中**: 黃色 (`bg-yellow-100 text-yellow-800`)
- **已完成**: 綠色 (`bg-green-100 text-green-800`)
- **重新生成中**: 橙色 (`bg-orange-100 text-orange-800`)

## 📱 響應式設計

### 1. 卡片佈局響應式

```css
.grid-cols-1          /* 手機: 1列 */
.lg\:grid-cols-2      /* 平板: 2列 */
.xl\:grid-cols-3      /* 桌面: 3列 */
```

### 2. 表格響應式

```html
<div class="overflow-x-auto">
  <table class="min-w-full">
    <!-- 表格內容 -->
  </table>
</div>
```

## 🔄 用戶體驗優化

### 1. 視覺反饋

- **選中狀態**: 藍色邊框和背景高亮
- **懸停效果**: 陰影加深和背景色變化
- **載入狀態**: 旋轉動畫和載入文字

### 2. 操作確認

- **批量刪除**: 二次確認對話框
- **操作結果**: Toast 通知成功/失敗訊息
- **錯誤處理**: 詳細的錯誤訊息顯示

### 3. 效能優化

- **並行刪除**: 使用 Promise.all 並行處理批量刪除
- **即時更新**: 操作完成後立即刷新資料
- **狀態管理**: 選中狀態的即時同步

## 🎯 功能特點

### 1. 雙模式顯示
- **卡片式**: 視覺化強，適合瀏覽和預覽
- **列表式**: 緊湊高效，適合大量資料管理

### 2. 智能選擇
- **個別選擇**: 精確選擇特定項目
- **全選功能**: 快速選擇所有項目
- **半選狀態**: 清楚顯示部分選中狀態

### 3. 批量操作
- **安全確認**: 二次確認防止誤操作
- **並行處理**: 高效處理大量資料
- **結果反饋**: 即時顯示操作結果

### 4. 響應式設計
- **多設備支援**: 手機、平板、桌面適配
- **觸控友好**: 適合觸控設備操作
- **鍵盤支援**: 支援鍵盤快捷鍵操作

## 🚀 使用場景

### 1. 資料瀏覽
- **卡片式**: 快速瀏覽資料內容和狀態
- **列表式**: 快速查看大量資料概覽

### 2. 資料管理
- **批量選擇**: 選擇多個相似資料進行操作
- **批量刪除**: 快速清理不需要的資料

### 3. 狀態監控
- **視覺化狀態**: 清楚顯示每個資料的審核狀態
- **統計資訊**: 快速查看通過/拒絕統計

---

*此功能提供了靈活的顯示方式和高效的批量操作，大幅提升了資料管理的用戶體驗和操作效率。* 