# 資料集審核拒絕理由優化說明

## 🎯 優化目標

優化資料集審核方式，在拒絕時提供多個常見理由供使用者選擇，並讓使用者填寫詳細的拒絕理由，以提升審核品質和資料改進效果。

## 🔧 主要改進內容

### 1. 後端架構優化

#### 1.1 資料庫模型擴展
**檔案位置：** `backend/app/database/models.py`

新增兩個欄位到 `ReviewLog` 模型：
```python
class ReviewLog(Base):
    __tablename__ = "review_logs"
    # ... 現有欄位 ...
    common_reasons = Column(JSON, default=[])  # 新增：常見拒絕理由列表
    detailed_reason = Column(Text)  # 新增：詳細拒絕理由
```

#### 1.2 Schema 更新
**檔案位置：** `backend/app/schemas.py`

更新審核相關的 Schema：
```python
class ReviewCreate(BaseModel):
    result: str # "ACCEPT" or "REJECT"
    comment: Optional[str] = None
    common_reasons: Optional[List[str]] = None  # 新增
    detailed_reason: Optional[str] = None  # 新增

class CommonRejectionReason(BaseModel):
    id: str
    label: str
    description: str
    category: str

class RejectionInfo(BaseModel):
    id: int
    comment: Optional[str] = None
    common_reasons: Optional[List[str]] = None  # 新增
    detailed_reason: Optional[str] = None  # 新增
    timestamp: datetime
    reviewer_username: str
```

#### 1.3 CRUD 操作更新
**檔案位置：** `backend/app/crud.py`

更新 `create_review_log` 函數：
```python
def create_review_log(db: Session, dataset_id: int, reviewer_id: int, review: schemas.ReviewCreate):
    db_review_log = models.ReviewLog(
        dataset_id=dataset_id,
        reviewer_id=reviewer_id,
        result=review.result.upper(),
        comment=review.comment,
        common_reasons=review.common_reasons or [],  # 新增
        detailed_reason=review.detailed_reason  # 新增
    )
    # ... 其餘邏輯
```

#### 1.4 API 端點新增
**檔案位置：** `backend/app/api/v1/review.py`

新增常見拒絕理由 API：
```python
@router.get("/common-reasons", response_model=List[schemas.CommonRejectionReason])
def get_common_rejection_reasons():
    """
    Get list of common rejection reasons for reference.
    """
    return COMMON_REJECTION_REASONS
```

### 2. 前端界面優化

#### 2.1 拒絕模態框重新設計
**檔案位置：** `frontend/src/views/Review.vue`

新的拒絕模態框包含三個部分：

1. **常見拒絕理由選擇**
   - 網格佈局顯示所有常見理由
   - 每個理由包含標籤、描述和分類
   - 支援多選功能
   - 視覺化分類標籤

2. **詳細拒絕理由填寫**
   - 可選欄位
   - 提供具體改進建議的空間
   - 字數限制和驗證

3. **額外備註**
   - 可選欄位
   - 用於補充說明

#### 2.2 常見拒絕理由分類

| 分類 | 理由 | 描述 |
|------|------|------|
| **指令** | 指令不夠清楚 | 指令描述模糊，無法明確理解要執行什麼任務 |
| **回答** | 輸出內容不準確 | AI 回答內容有錯誤或不符合事實 |
| **回答** | 輸出內容不實用 | 回答過於理論化，缺乏實務價值 |
| **法規** | 法規依據錯誤 | 引用的法規條文不正確或已過時 |
| **法規** | 法規依據不相關 | 引用的法規與指令內容無關 |
| **輸入** | 輸入內容不適當 | 輸入內容與資安領域無關或不合適 |
| **格式** | 格式不一致 | 資料格式與其他資料不一致 |
| **內容** | 內容重複 | 與其他資料內容重複或過於相似 |
| **安全** | 包含敏感資訊 | 內容包含機密或敏感資訊 |
| **其他** | 其他原因 | 其他未列出的拒絕原因 |

#### 2.3 用戶體驗改進

1. **視覺化設計**
   - 使用不同顏色區分分類
   - 清晰的選擇狀態指示
   - 響應式佈局支援

2. **互動體驗**
   - 點擊卡片選擇理由
   - 即時驗證和錯誤提示
   - 流暢的動畫效果

3. **表單驗證**
   - 至少選擇一個常見理由
   - 詳細拒絕理由為可選
   - 清晰的錯誤訊息

### 3. 資料流程優化

#### 3.1 拒絕理由收集流程
```
用戶點擊拒絕 → 顯示模態框 → 選擇常見理由 → 填寫詳細理由 → 提交審核
```

#### 3.2 資料存儲結構
```json
{
  "result": "REJECT",
  "comment": "選擇的拒絕理由：指令不夠清楚、輸出內容不準確\n\n詳細說明：指令描述過於模糊...\n\n額外備註：建議...",
  "common_reasons": ["instruction_unclear", "output_inaccurate"],
  "detailed_reason": "指令描述過於模糊，無法明確理解要執行什麼任務..."
}
```

#### 3.3 重新生成改進
拒絕理由將被傳遞給重新生成服務，用於改進資料品質：
- 常見理由幫助識別問題類型
- 詳細理由提供具體改進方向
- 歷史記錄保留完整的拒絕原因

## 🎨 界面設計特色

### 1. 模態框設計
- **尺寸優化**：`max-w-2xl` 提供足夠空間
- **滾動支援**：`max-h-[90vh] overflow-y-auto` 處理長內容
- **響應式佈局**：手機版和桌面版適配

### 2. 理由選擇卡片
- **視覺狀態**：選中時藍色邊框和背景
- **互動反饋**：懸停效果和點擊動畫
- **信息層次**：標籤、描述、分類標籤

### 3. 分類標籤系統
- **顏色編碼**：不同分類使用不同顏色
- **視覺識別**：快速識別問題類型
- **一致性**：統一的標籤設計

## 🔄 工作流程

### 1. 審核流程
1. 用戶審核資料
2. 點擊拒絕按鈕
3. 選擇常見拒絕理由（必選）
4. 可選填寫詳細拒絕理由
5. 可選填寫額外備註
6. 提交審核

### 2. 資料處理流程
1. 前端收集拒絕理由
2. 構建完整的拒絕說明
3. 發送到後端 API
4. 存儲到資料庫
5. 更新審核計數器
6. 觸發重新生成（如需要）

### 3. 重新生成改進
1. 收集拒絕理由歷史
2. 分析常見問題類型
3. 針對性改進生成策略
4. 產生更高品質的資料

## 📊 預期效果

### 1. 審核品質提升
- **標準化拒絕理由**：減少主觀判斷差異
- **詳細反饋**：提供具體的改進方向
- **分類統計**：便於分析問題趨勢

### 2. 資料改進效果
- **針對性改進**：根據拒絕理由調整生成策略
- **問題識別**：快速識別常見問題類型
- **持續優化**：基於反饋持續改進

### 3. 用戶體驗改善
- **操作簡化**：預設選項減少輸入負擔
- **視覺清晰**：分類和標籤提升可讀性
- **流程優化**：結構化的拒絕流程

## 🔧 技術實現細節

### 1. 前端技術
- **Vue 3 Composition API**：響應式狀態管理
- **Tailwind CSS**：現代化樣式設計
- **Vue Toastification**：用戶反饋提示

### 2. 後端技術
- **FastAPI**：高效能 API 框架
- **SQLAlchemy**：ORM 資料庫操作
- **Pydantic**：資料驗證和序列化

### 3. 資料庫設計
- **JSON 欄位**：存儲常見理由列表
- **Text 欄位**：存儲詳細拒絕理由
- **向後兼容**：保持現有資料結構

## 🚀 使用指南

### 1. 審核人員操作
1. 登入系統進入審核頁面
2. 審核資料內容
3. 如需要拒絕，點擊拒絕按鈕
4. 在模態框中選擇相關的常見理由
5. 可選填寫詳細的拒絕說明
6. 可選填寫額外備註
7. 點擊確認拒絕

### 2. 管理員查看
1. 進入管理頁面
2. 查看審核統計
3. 分析拒絕理由趨勢
4. 調整系統設定

## 📈 後續優化建議

### 1. 功能擴展
- **自定義拒絕理由**：允許管理員添加新的常見理由
- **拒絕理由統計**：提供詳細的拒絕原因分析
- **智能建議**：根據內容自動推薦拒絕理由

### 2. 用戶體驗
- **快速選擇**：常用理由的快速選擇功能
- **模板功能**：預設的詳細理由模板
- **批量操作**：支援批量拒絕相似資料

### 3. 資料分析
- **趨勢分析**：拒絕理由的時間趨勢
- **品質指標**：基於拒絕理由的品質評估
- **改進建議**：自動生成改進建議

## 總結

本次優化成功實現了結構化的拒絕理由收集系統，通過常見理由選擇和詳細說明填寫，大幅提升了審核的標準化和資料改進的針對性。新的界面設計提供了良好的用戶體驗，同時為後續的資料分析和系統改進奠定了堅實的基礎。 