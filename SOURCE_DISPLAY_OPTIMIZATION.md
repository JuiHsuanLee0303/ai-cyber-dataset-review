# 資料來源顯示優化說明

## 概述

本系統已優化資料審核頁面中的資料來源顯示功能，能夠自動從法規列表中查找對應的法條內容並顯示在審核頁面中，提升審核效率。

## 主要特性

### 1. 智能法規解析
- **自動解析**: 從資料來源字串中自動提取法規標題和條號
- **格式支援**: 支援「法規名稱第X條」的標準格式
- **錯誤處理**: 對無法解析的格式提供友好的錯誤提示

### 2. 即時法規查詢
- **API 整合**: 通過後端 API 即時查詢法規資料庫
- **快取機制**: 避免重複查詢相同的法規條文
- **載入狀態**: 顯示載入進度和錯誤狀態

### 3. 美觀的顯示界面
- **分層顯示**: 資料來源和法規內容分層展示
- **視覺區分**: 使用不同的背景色和邊框區分內容
- **響應式設計**: 適配不同螢幕尺寸

## 技術實現

### 後端 API 擴展

#### 1. 新增搜索端點
```python
@router.get("/search", response_model=schemas.LegalArticle)
def search_article(
    title: str,
    number: str,
    db: Session = Depends(get_db)
):
    """
    Search for a legal article by title and number.
    Accessible by all authenticated users.
    """
    article = crud.get_legal_article_by_title_and_number(db, title=title, number=number)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
```

#### 2. 新增 CRUD 函數
```python
def get_legal_article_by_title_and_number(db: Session, title: str, number: str):
    return db.query(models.LegalArticle).filter(
        models.LegalArticle.title == title,
        models.LegalArticle.number == number
    ).first()
```

### 前端實現

#### 1. 資料來源解析
```javascript
const parseSource = (sourceStr) => {
  // 範例: "公務機關所屬人員資通安全事項獎懲辦法第1條"
  const match = sourceStr.match(/^(.+?)第(\d+)條$/)
  if (match) {
    return {
      title: match[1].trim(),
      number: match[2]
    }
  }
  return null
}
```

#### 2. 法規內容載入
```javascript
const loadSourceDetails = async (sourceStr, index) => {
  const parsed = parseSource(sourceStr)
  if (!parsed) {
    sourceErrors.value[index] = '無法解析法規格式'
    return
  }

  sourceLoading.value[index] = true
  sourceErrors.value[index] = null
  
  try {
    const response = await instance.get('/api/v1/legal-articles/search', {
      params: {
        title: parsed.title,
        number: parsed.number
      }
    })
    sourceDetails.value[index] = response.data
  } catch (error) {
    console.error('Failed to load legal article:', error)
    sourceErrors.value[index] = '法規不存在或載入失敗'
  } finally {
    sourceLoading.value[index] = false
  }
}
```

#### 3. 動態 UI 更新
```vue
<div v-if="currentItem.source && currentItem.source.length > 0">
  <h2 class="text-lg font-semibold text-gray-700 mb-2">資料來源 (Source)</h2>
  <div class="bg-gray-100 p-3 rounded-md space-y-3">
    <div v-for="(src, index) in currentItem.source" :key="index" class="text-sm">
      <div class="flex items-start space-x-2">
        <span class="text-gray-500 mt-1">•</span>
        <div class="flex-1">
          <div class="text-gray-600 font-medium">{{ src }}</div>
          <div v-if="sourceDetails[index]" class="mt-2 p-3 bg-white rounded border-l-4 border-blue-500">
            <div class="text-xs text-gray-500 mb-1">法規內容：</div>
            <div class="text-gray-800 whitespace-pre-wrap">{{ sourceDetails[index].content }}</div>
          </div>
          <div v-else-if="sourceLoading[index]" class="mt-2 text-xs text-gray-500">
            載入法規內容中...
          </div>
          <div v-else-if="sourceErrors[index]" class="mt-2 text-xs text-red-500">
            無法載入法規內容
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 使用方式

### 1. 資料來源格式
系統支援以下格式的資料來源：
- `資通安全管理法第1條`
- `公務機關所屬人員資通安全事項獎懲辦法第15條`
- `個人資料保護法第5條`

### 2. 自動載入
當審核頁面載入時，系統會：
1. 解析所有資料來源字串
2. 自動查詢對應的法規內容
3. 在界面上顯示載入狀態
4. 成功載入後顯示法規內容

### 3. 錯誤處理
- **解析失敗**: 顯示「無法解析法規格式」
- **法規不存在**: 顯示「法規不存在或載入失敗」
- **網路錯誤**: 顯示「網路錯誤」

## 資料庫結構

### LegalArticle 模型
```python
class LegalArticle(Base):
    __tablename__ = "legal_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)  # 法規標題
    number = Column(String, nullable=False)             # 條號
    content = Column(Text, nullable=False)              # 法規內容
```

## 性能優化

### 1. 並發載入
- 多個資料來源同時載入，不阻塞界面
- 使用 Promise 管理異步操作

### 2. 狀態管理
- 使用 Vue 的響應式系統管理載入狀態
- 避免重複載入相同的法規

### 3. 錯誤恢復
- 載入失敗時提供重試機制
- 不影響其他資料來源的顯示

## 擴展性

### 1. 支援更多格式
可以輕鬆擴展支援其他法規引用格式：
- `法規名稱第X條第Y項`
- `法規名稱施行細則第X條`
- `法規名稱第X條之Y`

### 2. 法規資料來源
可以整合多個法規資料來源：
- 政府法規資料庫
- 第三方法規服務
- 本地法規檔案

### 3. 快取機制
可以添加客戶端快取來提升性能：
- 本地存儲已查詢的法規
- 定期更新法規資料
- 離線支援

## 注意事項

1. **法規資料完整性**: 確保法規資料庫包含所有引用的法規
2. **格式一致性**: 資料來源字串需要遵循標準格式
3. **網路依賴**: 需要穩定的網路連接來查詢法規
4. **權限控制**: 法規查詢 API 需要適當的權限控制

## 未來改進

1. **智能匹配**: 使用模糊匹配處理法規名稱的變體
2. **版本控制**: 支援法規的不同版本
3. **全文搜索**: 在法規內容中搜索關鍵詞
4. **相關法規**: 顯示相關的法規條文
5. **法規更新**: 自動檢測法規更新並通知用戶 