# 待審核資料集管理頁面 UI 優化說明

## 概述

本次優化針對待審核資料集管理頁面進行了全面的UI設計統一，建立了一套完整的設計系統，提升用戶體驗和視覺一致性。

## 主要優化內容

### 1. 設計系統建立

#### 1.1 按鈕系統 (Button System)
- **統一樣式類別**: `btn`, `btn-sm`, `btn-primary`, `btn-success`, `btn-secondary`, `btn-danger`, `btn-warning`
- **特點**: 
  - 統一的圓角、陰影、過渡效果
  - 一致的圖標和文字間距
  - 響應式設計支援
  - 專注狀態的環形指示器

#### 1.2 卡片系統 (Card System)
- **統一樣式類別**: `card`, `card-header`, `card-body`, `card-footer`
- **特點**:
  - 統一的邊框、陰影、圓角
  - 一致的內邊距和分隔線
  - 懸停效果和過渡動畫

#### 1.3 狀態標籤系統 (Status Badge System)
- **統一樣式類別**: `status-badge`, `status-pending`, `status-reviewing`, `status-done`, `status-regenerating`
- **特點**:
  - 統一的圓角標籤設計
  - 語義化的顏色系統
  - 一致的文字大小和字重

#### 1.4 模態框系統 (Modal System)
- **統一樣式類別**: `modal-overlay`, `modal-content`, `modal-header`, `modal-body`, `modal-footer`
- **特點**:
  - 統一的遮罩和內容區域設計
  - 一致的標題、內容、按鈕區域佈局
  - 統一的關閉按鈕設計

#### 1.5 表單系統 (Form System)
- **統一樣式類別**: `form-group`, `form-label`, `form-input`, `form-textarea`
- **特點**:
  - 統一的標籤和輸入框設計
  - 一致的聚焦狀態和驗證樣式
  - 統一的佔位符文字設計

### 2. 頁面佈局優化

#### 2.1 頁面頭部 (Header Section)
- **新增功能**:
  - 漸變背景的圖標設計
  - 頁面標題和描述文字
  - 自動更新狀態指示器
  - 統一的按鈕分組和間距

#### 2.2 主要內容區域 (Main Content)
- **優化內容**:
  - 響應式容器設計
  - 統一的載入狀態動畫
  - 優雅的空狀態設計
  - 一致的內容間距

### 3. 顯示模式優化

#### 3.1 卡片式顯示 (Card View)
- **優化內容**:
  - 統一的卡片佈局和間距
  - 一致的狀態標籤設計
  - 統一的操作按鈕樣式
  - 優化的內容截斷和顯示

#### 3.2 列表式顯示 (List View)
- **優化內容**:
  - 統一的表格設計
  - 一致的狀態標籤和按鈕
  - 優化的統計資訊顯示
  - 統一的懸停效果

### 4. 模態框優化

#### 4.1 新增/編輯模態框
- **優化內容**:
  - 統一的標題和關閉按鈕
  - 一致的表單佈局和樣式
  - 統一的錯誤訊息顯示
  - 優化的按鈕區域設計

#### 4.2 拒絕原因模態框
- **優化內容**:
  - 統一的載入狀態設計
  - 優雅的空狀態顯示
  - 一致的內容卡片設計
  - 統一的按鈕樣式

#### 4.3 批量新增模態框
- **優化內容**:
  - 統一的輸入方式切換
  - 一致的預覽和驗證設計
  - 統一的按鈕和狀態顯示

### 5. 響應式設計

#### 5.1 移動端適配
- **優化內容**:
  - 按鈕大小的響應式調整
  - 卡片內邊距的響應式變化
  - 模態框的移動端優化
  - 表格的橫向滾動支援

### 6. 動畫和過渡效果

#### 6.1 載入動畫
- **新增內容**:
  - 統一的載入旋轉動畫
  - 優雅的載入狀態指示器
  - 一致的動畫時長和緩動函數

#### 6.2 過渡效果
- **優化內容**:
  - 統一的按鈕懸停效果
  - 一致的卡片陰影過渡
  - 統一的模態框顯示動畫

## 技術實現

### CSS 類別系統
```css
/* 按鈕系統 */
.btn { /* 基礎按鈕樣式 */ }
.btn-sm { /* 小尺寸按鈕 */ }
.btn-primary { /* 主要按鈕 */ }
.btn-success { /* 成功按鈕 */ }
.btn-secondary { /* 次要按鈕 */ }
.btn-danger { /* 危險按鈕 */ }
.btn-warning { /* 警告按鈕 */ }

/* 卡片系統 */
.card { /* 基礎卡片樣式 */ }
.card-header { /* 卡片頭部 */ }
.card-body { /* 卡片內容 */ }
.card-footer { /* 卡片底部 */ }

/* 狀態標籤系統 */
.status-badge { /* 基礎狀態標籤 */ }
.status-pending { /* 待審核狀態 */ }
.status-reviewing { /* 審核中狀態 */ }
.status-done { /* 已完成狀態 */ }
.status-regenerating { /* 重新生成中狀態 */ }

/* 模態框系統 */
.modal-overlay { /* 模態框遮罩 */ }
.modal-content { /* 模態框內容 */ }
.modal-header { /* 模態框頭部 */ }
.modal-body { /* 模態框內容區域 */ }
.modal-footer { /* 模態框底部 */ }

/* 表單系統 */
.form-group { /* 表單組 */ }
.form-label { /* 表單標籤 */ }
.form-input { /* 輸入框 */ }
.form-textarea { /* 文字區域 */ }
```

### 響應式設計
```css
@media (max-width: 640px) {
  .btn-sm {
    @apply px-2 py-1 text-xs;
  }
  
  .card-header,
  .card-body,
  .card-footer {
    @apply p-3;
  }
}
```

## 使用指南

### 1. 按鈕使用
```html
<!-- 主要按鈕 -->
<button class="btn btn-primary">
  <svg class="w-4 h-4">...</svg>
  <span>按鈕文字</span>
</button>

<!-- 小尺寸按鈕 -->
<button class="btn btn-primary btn-sm">
  <svg class="w-3 h-3">...</svg>
  <span>按鈕文字</span>
</button>
```

### 2. 卡片使用
```html
<div class="card">
  <div class="card-header">
    <!-- 卡片頭部內容 -->
  </div>
  <div class="card-body">
    <!-- 卡片內容 -->
  </div>
  <div class="card-footer">
    <!-- 卡片底部內容 -->
  </div>
</div>
```

### 3. 狀態標籤使用
```html
<span :class="getStatusBadgeClass(item.review_status)" class="status-badge">
  {{ getStatusText(item.review_status) }}
</span>
```

### 4. 模態框使用
```html
<div class="modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <!-- 模態框標題和關閉按鈕 -->
    </div>
    <div class="modal-body">
      <!-- 模態框內容 -->
    </div>
    <div class="modal-footer">
      <!-- 模態框按鈕 -->
    </div>
  </div>
</div>
```

## 效果展示

### 優化前後對比

#### 1. 頁面頭部
- **優化前**: 簡單的標題和按鈕排列
- **優化後**: 漸變圖標、描述文字、狀態指示器的完整設計

#### 2. 卡片顯示
- **優化前**: 基礎的白色卡片設計
- **優化後**: 統一的卡片系統、狀態標籤、操作按鈕的完整佈局

#### 3. 模態框
- **優化前**: 簡單的彈窗設計
- **優化後**: 統一的模態框系統、完整的表單設計、優雅的狀態顯示

## 維護指南

### 1. 新增按鈕樣式
在 CSS 中添加新的按鈕變體：
```css
.btn-info {
  @apply bg-cyan-600 text-white hover:bg-cyan-700 focus:ring-cyan-500 shadow-sm;
}
```

### 2. 新增狀態標籤
在 JavaScript 中添加新的狀態處理：
```javascript
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待審核',
    'reviewing': '審核中',
    'done': '已完成',
    'regenerating': '重新生成中',
    'new_status': '新狀態' // 新增狀態
  }
  return statusMap[status] || status
}
```

### 3. 擴展設計系統
根據需要擴展現有的設計系統，保持一致的命名規範和樣式結構。

## 總結

本次UI優化建立了完整的設計系統，實現了：
- **視覺一致性**: 統一的顏色、字體、間距設計
- **用戶體驗提升**: 優雅的動畫、清晰的狀態指示
- **維護性改善**: 模組化的CSS類別系統
- **響應式支援**: 完整的移動端適配
- **可擴展性**: 易於擴展和維護的設計架構

這些優化為後續的功能開發和UI改進奠定了堅實的基礎。 