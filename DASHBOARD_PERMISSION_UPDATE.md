# 儀表板權限更新說明

## 🎯 更新目標

修改儀表板設定，讓資安專家可以看到自己的統計數據，而系統管理員可以看到所有人的統計數據，解決資安專家訪問儀表板時遇到的 403 Forbidden 錯誤。

## 🔧 主要修改

### 1. 後端 API 修改

#### 修改文件：`backend/app/api/v1/stats.py`

**原來的問題：**
- 只允許管理員訪問統計 API
- 使用 `get_current_admin_user` 依賴，導致資安專家被拒絕訪問

**修改內容：**
```python
# 修改前
@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)  # 只允許管理員
):

# 修改後
@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 允許所有已登入用戶
):
    """
    Retrieve statistics for the dashboard.
    - Admin users see global statistics
    - Expert users see their personal statistics
    """
    if current_user.role == models.UserRole.ADMIN:
        # 管理員看到全局統計
        global_stats = crud.get_global_stats(db)
        review_activity = crud.get_review_activity(db, days=30)
        top_reviewers = crud.get_top_reviewers(db, limit=5)
        common_rejection_reasons = crud.get_common_rejection_reasons(db, limit=5)
    else:
        # 資安專家看到個人統計
        global_stats = crud.get_user_stats(db, current_user.id)
        review_activity = crud.get_user_review_activity(db, current_user.id, days=30)
        top_reviewers = []  # 個人統計不需要顯示頂尖審核員
        common_rejection_reasons = crud.get_user_rejection_reasons(db, current_user.id, limit=5)
```

### 2. 新增 CRUD 函數

#### 修改文件：`backend/app/crud.py`

**新增的函數：**

1. **`get_user_stats(db: Session, user_id: int)`**
   - 獲取特定用戶的統計數據
   - 包括該用戶的審核次數、通過次數、拒絕次數等

2. **`get_user_review_activity(db: Session, user_id: int, days: int = 30)`**
   - 獲取特定用戶的審核活動時間序列
   - 用於生成個人審核活動圖表

3. **`get_user_rejection_reasons(db: Session, user_id: int, limit: int = 5)`**
   - 獲取特定用戶的拒絕理由統計
   - 用於顯示個人拒絕理由分析

### 3. 前端界面修改

#### 修改文件：`frontend/src/views/Dashboard.vue`

**主要修改：**

1. **動態標題**
   ```vue
   <h1 class="text-3xl font-bold text-gray-800 mb-6">
     {{ isAdmin ? '系統統計儀表板' : '個人統計儀表板' }}
   </h1>
   ```

2. **動態 KPI 標籤**
   ```vue
   <h3 class="text-sm font-medium text-gray-500">
     {{ isAdmin ? '資料總筆數' : '已審核資料筆數' }}
   </h3>
   ```

3. **條件顯示頂尖審核員**
   ```vue
   <!-- Top Reviewers (only for admin) -->
   <div v-if="isAdmin" class="bg-white p-6 rounded-lg shadow-md">
   ```

4. **動態圖表標籤**
   ```vue
   <h3 class="text-lg font-medium text-gray-800 mb-4">
     {{ isAdmin ? '過去 30 天審核活動' : '過去 30 天我的審核活動' }}
   </h3>
   ```

## 📊 數據差異

### 管理員看到的數據：
- **資料總筆數**：系統中所有待審核資料的總數
- **總審核次數**：所有用戶的審核次數總和
- **通過率/拒絕率**：全局的通過率和拒絕率
- **審核活動**：所有用戶的審核活動
- **頂尖審核員**：審核次數最多的用戶排名
- **常見拒絕理由**：所有用戶的拒絕理由統計

### 資安專家看到的數據：
- **已審核資料筆數**：該專家審核過的資料集數量
- **我的審核次數**：該專家的個人審核次數
- **我的通過率/拒絕率**：該專家的個人通過率和拒絕率
- **我的審核活動**：該專家的個人審核活動時間序列
- **我的拒絕理由**：該專家的個人拒絕理由統計
- **不顯示頂尖審核員**：個人統計不需要顯示排名

## 🔐 權限控制

### 訪問控制：
- **所有已登入用戶**：都可以訪問 `/api/v1/stats/` 端點
- **數據隔離**：根據用戶角色返回不同的數據範圍
- **安全性**：用戶只能看到自己有權限的數據

### 角色區分：
- **管理員 (ADMIN)**：看到全局統計數據
- **資安專家 (EXPERT)**：看到個人統計數據

## 🎯 用戶體驗改進

### 1. 解決 403 錯誤
- 資安專家現在可以正常訪問儀表板
- 不再出現權限不足的錯誤

### 2. 個性化體驗
- 管理員：看到系統整體狀況，便於管理決策
- 資安專家：看到個人工作成果，便於自我評估

### 3. 數據相關性
- 每個用戶看到的數據都與自己的工作相關
- 提高數據的實用性和參考價值

## 🧪 測試驗證

### 1. 管理員測試
```bash
# 使用管理員帳號登入
curl -X GET "http://localhost:8000/api/v1/stats/" \
  -H "Authorization: Bearer {admin_token}"
# 應該返回全局統計數據
```

### 2. 資安專家測試
```bash
# 使用資安專家帳號登入
curl -X GET "http://localhost:8000/api/v1/stats/" \
  -H "Authorization: Bearer {expert_token}"
# 應該返回個人統計數據
```

### 3. 前端測試
- 管理員登入：顯示「系統統計儀表板」
- 資安專家登入：顯示「個人統計儀表板」
- 數據內容：根據角色顯示相應的統計信息

## 📋 相關文件

### 修改的文件：
1. `backend/app/api/v1/stats.py` - API 端點修改
2. `backend/app/crud.py` - 新增個人統計 CRUD 函數
3. `frontend/src/views/Dashboard.vue` - 前端界面修改

### 相關功能：
- 用戶認證系統
- 審核記錄系統
- 統計數據計算

## ✅ 完成狀態

- [x] 修改後端 API 權限控制
- [x] 新增個人統計 CRUD 函數
- [x] 修改前端界面顯示邏輯
- [x] 重新啟動服務
- [x] 創建說明文檔

現在資安專家可以正常訪問儀表板，看到自己的個人統計數據，而管理員仍然可以看到全局統計數據。 