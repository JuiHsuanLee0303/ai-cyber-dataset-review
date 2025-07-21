# 從法規生成資料 Modal 滾動功能測試

## 概述

本文檔描述了從法規生成資料 Modal 的滾動功能測試，確保 Modal 在內容較多時可以正常滾動。

## 功能描述

### 滾動功能
- **Modal 結構**：使用 Flexbox 佈局，header 和 footer 固定，body 可滾動
- **最大高度**：限制為 `max-h-[90vh]`，確保在小螢幕上也能正常顯示
- **滾動區域**：只有 modal-body 部分可以滾動
- **滾動條樣式**：自定義滾動條樣式，提供更好的視覺體驗

### 鍵盤支援
- **ESC 鍵關閉**：按 ESC 鍵可以關閉 Modal
- **事件監聽**：組件掛載時添加事件監聽器，卸載時清理

### 視覺優化
- **Header 樣式**：漸層背景，藍色主題
- **Footer 樣式**：灰色背景，包含提示文字和關閉按鈕
- **響應式設計**：在不同螢幕尺寸下都有良好的顯示效果

## 測試步驟

### 1. 基本滾動測試

#### 步驟
1. 登入管理員帳號
2. 進入「待審核資料」頁面
3. 點擊「從法規生成資料」按鈕
4. 在 Modal 中選擇多個法規條文
5. 檢查 Modal 是否可以滾動

#### 預期結果
- Modal 打開時顯示正確的內容
- 當內容超出視窗高度時，可以滾動查看
- Header 和 footer 保持固定位置
- 滾動條樣式美觀

### 2. 鍵盤功能測試

#### 步驟
1. 打開從法規生成資料 Modal
2. 按 ESC 鍵
3. 檢查 Modal 是否關閉

#### 預期結果
- 按 ESC 鍵可以關閉 Modal
- Modal 關閉時重置所有狀態

### 3. 響應式測試

#### 步驟
1. 在不同螢幕尺寸下打開 Modal
2. 檢查 Modal 的顯示效果
3. 測試滾動功能

#### 預期結果
- 在小螢幕上 Modal 不會超出視窗
- 滾動功能在所有尺寸下都正常工作
- 內容佈局適應不同螢幕尺寸

### 4. 內容測試

#### 步驟
1. 選擇批量生成模式
2. 設定較大的生成數量（如 20 筆）
3. 選擇多個法規條文
4. 檢查 Modal 內容是否完整顯示

#### 預期結果
- 所有內容都可以通過滾動查看
- 生成按鈕始終可見
- 不會出現內容被截斷的情況

## 技術實現

### CSS 樣式
```css
.modal-content {
  @apply bg-white rounded-xl shadow-2xl w-full max-w-6xl max-h-[90vh] flex flex-col;
  animation: modalSlideIn 0.3s ease-out;
}

.modal-header {
  @apply flex justify-between items-center p-6 border-b border-gray-200 flex-shrink-0;
}

.modal-body {
  @apply p-6 overflow-y-auto flex-1;
}

.modal-footer {
  @apply flex justify-between items-center p-6 border-t border-gray-200 bg-gray-50 flex-shrink-0;
}
```

### JavaScript 功能
```javascript
// Handle ESC key to close modal
const handleKeydown = (event) => {
  if (showGenerateModal.value && event.key === 'Escape') {
    closeGenerateModal()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
```

## 注意事項

1. **滾動條樣式**：只在 Webkit 瀏覽器中生效
2. **事件監聽器**：確保在組件卸載時清理，避免記憶體洩漏
3. **響應式設計**：在不同設備上測試滾動功能
4. **內容長度**：確保在內容較長時滾動功能正常

## 相關文件

- [從法規生成資料功能](../features/12-batch-generation-feature.md)
- [Modal 滾動功能測試](../testing/03-modal-scroll-test.md)
- [UI/UX 改進文檔](../features/14-add-data-modal-ux-improvement.md) 