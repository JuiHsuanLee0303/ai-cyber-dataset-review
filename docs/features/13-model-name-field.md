# Model Name 欄位功能說明

## 🎯 功能概述

為待審核資料集管理中的新增資料與批量新增功能增加 `model_name` 欄位，用於記錄生成資料所使用的AI模型名稱，提升資料追蹤和管理能力。

## 🚀 主要功能

### 1. 新增資料模態框
- **模型名稱欄位**：新增可選的模型名稱輸入欄位
- **輸入驗證**：支援自由文字輸入，無格式限制
- **提示說明**：提供清楚的使用說明和範例

### 2. 批量新增功能
- **JSON格式支援**：在批量新增的JSON格式中支援 `model_name` 欄位
- **預覽顯示**：在批量預覽中顯示模型名稱
- **範例更新**：更新JSON範例包含模型名稱

### 3. 資料顯示
- **卡片視圖**：在資料卡片中顯示模型名稱（如果存在）
- **列表視圖**：在表格中新增模型欄位
- **響應式設計**：在不同螢幕尺寸下適當顯示

## 🔧 技術實現

### 前端變更

#### 1. 新增資料模態框
```vue
<div class="form-group">
  <label class="form-label">模型名稱 (Model Name) - 選填</label>
  <input v-model="form.model_name" type="text" class="form-input" placeholder="例如：llama3, qwen2.5, gemma2" />
  <p class="text-xs text-gray-500 mt-1">記錄生成此資料所使用的AI模型名稱</p>
</div>
```

#### 2. 表單初始化
```javascript
const getInitialForm = () => ({
  instruction: '',
  input: '',
  output: '',
  system: '',
  source: '',
  history: '[]',
  model_name: '' // 新增模型名稱欄位
});
```

#### 3. 批量新增JSON範例
```json
[
  {
    "instruction": "這個資安獎懲辦法是根據什麼法律訂出來的？",
    "input": "為什麼政府要特別訂資安獎懲規定？",
    "output": "這是根據《資通安全管理法》第15條與第19條訂定的...",
    "system": "說明本辦法與母法的法律關係。",
    "history": [],
    "source": ["公務機關所屬人員資通安全事項獎懲辦法第1條"],
    "model_name": "llama3"
  }
]
```

#### 4. 資料顯示
```vue
<!-- 卡片視圖 -->
<div v-if="item.model_name">
  <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
    <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-indigo-500 rounded-full mr-2"></span>
    模型 (Model)
  </h4>
  <div class="bg-gray-50 rounded-md p-2 sm:p-3">
    <p class="text-xs sm:text-sm text-gray-800">{{ item.model_name }}</p>
  </div>
</div>

<!-- 列表視圖 -->
<th class="hidden md:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">模型</th>
<td class="hidden md:table-cell px-6 py-4 text-xs sm:text-sm text-gray-900">
  <div class="truncate" :title="item.model_name">{{ item.model_name || '-' }}</div>
</td>
```

### 後端支援

#### 1. Schema 定義
```python
class RawDatasetBase(BaseModel):
    instruction: Optional[str] = None
    input: Optional[str] = None
    output: str
    system: Optional[str] = None
    source: Optional[List[str]] = []
    history: Optional[List[Any]] = []
    model_name: Optional[str] = None  # 新增：生成使用的模型名稱
```

#### 2. 資料庫模型
```python
class RawDataset(Base):
    __tablename__ = "raw_dataset"
    
    id = Column(Integer, primary_key=True, index=True)
    instruction = Column(Text, nullable=True)
    input = Column(Text, nullable=True)
    output = Column(Text, nullable=False)
    system = Column(Text, nullable=True)
    source = Column(JSON, nullable=True)
    history = Column(JSON, nullable=True)
    model_name = Column(String, nullable=True)  # 新增模型名稱欄位
    review_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### 3. CRUD 操作
```python
def create_raw_dataset(db: Session, dataset: schemas.RawDatasetCreate):
    db_dataset = models.RawDataset(
        instruction=dataset.instruction,
        input=dataset.input,
        output=dataset.output,
        system=dataset.system,
        source=dataset.source,
        history=dataset.history,
        model_name=dataset.model_name  # 保存模型名稱
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset
```

## 📊 使用流程

### 1. 新增單筆資料
1. 點擊「新增資料」按鈕
2. 填寫必要欄位（指令、輸出）
3. 填寫可選欄位（輸入、系統提示、歷史紀錄、資料來源）
4. **新增：填寫模型名稱（選填）**
5. 點擊「新增」按鈕

### 2. 批量新增資料
1. 點擊「批量新增」按鈕
2. 選擇輸入方式（文字或檔案）
3. 準備JSON格式資料，包含 `model_name` 欄位
4. 點擊「解析資料」進行驗證
5. 預覽資料，確認模型名稱正確顯示
6. 點擊「確認新增」

### 3. 查看資料
1. 在資料列表中查看模型欄位
2. 在卡片視圖中查看模型資訊
3. 使用篩選功能按模型分類

## 🎨 界面特色

### 1. 直觀的輸入設計
- 清晰的標籤和說明
- 適當的佔位符文字
- 即時的視覺反饋

### 2. 響應式顯示
- 桌面版：完整的表格顯示
- 平板版：適中的欄位顯示
- 手機版：卡片式顯示

### 3. 一致的視覺風格
- 與其他欄位保持一致的設計
- 適當的顏色和圖示
- 清楚的層次結構

## 🔍 資料追蹤

### 1. 模型使用統計
- 記錄每個資料使用的模型
- 支援按模型分類統計
- 追蹤模型效能表現

### 2. 品質分析
- 比較不同模型的生成品質
- 分析模型偏好和趨勢
- 優化模型選擇策略

### 3. 審核追蹤
- 審核記錄包含模型資訊
- 追蹤模型相關的審核結果
- 支援模型效能評估

## 🚨 注意事項

### 1. 欄位特性
- **選填欄位**：模型名稱為可選欄位，不填寫不影響資料新增
- **自由格式**：支援任意文字輸入，無特定格式要求
- **長度限制**：建議使用簡潔的模型名稱

### 2. 相容性
- **向後相容**：現有資料不包含模型名稱仍可正常顯示
- **API相容**：所有現有API端點保持相容
- **資料庫相容**：現有資料庫結構無需變更

### 3. 使用建議
- 使用標準的模型名稱（如：llama3, qwen2.5, gemma2）
- 保持命名一致性
- 定期更新模型資訊

## 🔮 未來擴展

### 1. 模型管理
- 模型名稱自動完成
- 模型版本管理
- 模型效能追蹤

### 2. 智能分析
- 模型效能分析
- 自動模型推薦
- 品質預測

### 3. 整合功能
- 與模型管理系統整合
- 自動模型資訊同步
- 模型效能報告

這個新功能為資料集管理提供了更完整的模型追蹤能力，有助於提升資料品質和系統管理效率。 