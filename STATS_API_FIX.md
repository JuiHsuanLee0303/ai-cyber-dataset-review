# Stats API 修正說明

## 問題描述

前端在訪問 Dashboard 頁面時遇到以下錯誤：

1. **CORS 錯誤**：`Access to XMLHttpRequest at 'http://localhost:8000/api/v1/stats/' from origin 'http://localhost:5173' has been blocked by CORS policy`
2. **後端 500 錯誤**：`AttributeError: module 'app.crud' has no attribute 'get_user_rejection_reasons'`

## 根本原因

在 `backend/app/api/v1/stats.py` 中，程式碼嘗試調用 `crud.get_user_rejection_reasons` 函數，但這個函數在 `backend/app/crud.py` 中並不存在。

## 解決方案

### 1. 新增缺失的函數

在 `backend/app/crud.py` 中新增了 `get_user_rejection_reasons` 函數：

```python
def get_user_rejection_reasons(db: Session, user_id: int, limit: int = 5) -> list[schemas.CommonRejectionReason]:
    """獲取特定用戶的常見拒絕理由"""
    results = (
        db.query(
            models.ReviewLog.comment,
            func.count(models.ReviewLog.id).label('count')
        )
        .filter(
            models.ReviewLog.result == 'REJECT', 
            models.ReviewLog.comment.isnot(None),
            models.ReviewLog.reviewer_id == user_id
        )
        .group_by(models.ReviewLog.comment)
        .order_by(func.count(models.ReviewLog.id).desc())
        .limit(limit)
        .all()
    )
    return [schemas.CommonRejectionReason(reason=r.comment, count=r.count) for r in results]
```

### 2. 函數功能說明

這個函數的功能是：
- 獲取特定用戶的拒絕理由統計
- 按拒絕理由分組並計算出現次數
- 按出現次數降序排列
- 限制返回結果數量（預設 5 個）

### 3. 重新啟動服務

修正後重新啟動了後端和前端服務：

```bash
docker-compose restart backend
docker-compose restart frontend
```

## 驗證結果

### API 測試

使用 curl 測試 stats API：

```bash
# 獲取 token
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"

# 測試 stats API
curl -X GET "http://localhost:8000/api/v1/stats/" \
  -H "Authorization: Bearer <token>"
```

API 正常返回統計數據，包含：
- 全局統計（總資料集數、總審核數、接受數、拒絕數）
- 審核活動（30天內的每日審核數量）
- 頂尖審核員
- 常見拒絕理由

## 影響範圍

- ✅ Dashboard 頁面可以正常載入統計數據
- ✅ 管理員和專家用戶都能看到對應的統計信息
- ✅ 前端不再出現 CORS 和 500 錯誤

## 注意事項

1. 確保後端服務正常運行
2. 確保資料庫中有相應的審核記錄
3. 如果沒有拒絕記錄，`common_rejection_reasons` 會返回空陣列 