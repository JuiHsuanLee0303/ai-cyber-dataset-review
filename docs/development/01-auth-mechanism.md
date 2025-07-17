# 認證機制優化說明

## 概述

本系統已優化認證機制，實現了前端在每次請求前自動刷新 token 的功能，確保用戶會話的安全性和連續性。

## 主要特性

### 1. 自動 Token 刷新
- **請求前刷新**: 每次發送 API 請求前，系統會自動檢查並刷新 access token
- **響應後刷新**: 如果請求返回 401 錯誤，系統會自動嘗試刷新 token 並重試請求
- **防重複刷新**: 使用 Promise 機制防止同時發起多個刷新請求

### 2. 智能請求攔截
- **請求攔截器**: 自動為每個請求添加 Authorization header
- **響應攔截器**: 處理 401 錯誤並自動重試
- **循環保護**: 避免在認證端點上觸發無限刷新循環

### 3. 狀態管理
- **本地存儲**: token 安全存儲在 localStorage 中
- **狀態同步**: 登入狀態、用戶信息與 token 狀態保持同步
- **自動清理**: 登出時自動清理所有認證相關數據

## 技術實現

### 前端 (Vue.js + Axios)

```javascript
// 請求攔截器 - 每次請求前刷新 token
instance.interceptors.request.use(async (config) => {
  // 跳過認證端點避免循環
  if (config.url && (config.url.includes('/auth/token') || config.url.includes('/auth/refresh'))) {
    return config
  }

  // 自動刷新 token
  if (state.refreshToken && !state.isRefreshing) {
    try {
      await refreshToken()
    } catch (error) {
      console.warn('Pre-request token refresh failed:', error)
    }
  }

  // 添加 Authorization header
  if (state.accessToken) {
    config.headers.Authorization = `Bearer ${state.accessToken}`
  }
  return config
})

// 響應攔截器 - 處理 401 錯誤
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true
      try {
        await refreshToken()
        error.config.headers.Authorization = `Bearer ${state.accessToken}`
        return instance(error.config)
      } catch (refreshError) {
        logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)
```

### 後端 (FastAPI + JWT)

```python
# Token 配置
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15分鐘過期
REFRESH_TOKEN_EXPIRE_DAYS = 7     # 7天過期

# 刷新端點
@router.post("/refresh", response_model=schemas.Token)
def refresh_access_token(
    refresh_request: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    payload = security.decode_refresh_token(refresh_request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    username: str = payload.get("sub")
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_request.refresh_token,
        "token_type": "bearer"
    }
```

## 使用方式

### 1. 登入
```javascript
const { login } = useAuth()
const success = await login(username, password)
if (success) {
  // 登入成功，token 已自動存儲
  router.push('/')
}
```

### 2. 發送 API 請求
```javascript
const { instance } = useAuth()

// 自動處理 token 刷新
const response = await instance.get('/api/v1/users/')
const users = response.data
```

### 3. 手動刷新 Token
```javascript
const { refreshToken } = useAuth()

try {
  await refreshToken()
  console.log('Token 刷新成功')
} catch (error) {
  console.error('Token 刷新失敗:', error)
}
```

### 4. 登出
```javascript
const { logout } = useAuth()
logout()
router.push('/login')
```

## 安全特性

1. **短期 Access Token**: 15分鐘過期，減少被盜用的風險
2. **長期 Refresh Token**: 7天過期，提供良好的用戶體驗
3. **自動刷新**: 用戶無需手動操作，系統自動維護會話
4. **安全存儲**: token 存儲在 localStorage 中，登出時自動清理
5. **錯誤處理**: 刷新失敗時自動登出並重定向到登入頁面

## 測試

在管理設定頁面提供了「測試認證機制」按鈕，可以測試：
1. 手動刷新 token
2. 發送需要認證的請求
3. 連續發送多個請求

## 配置

可以在環境變數中調整 token 過期時間：

```bash
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 注意事項

1. **避免循環**: 認證相關的端點不會觸發自動刷新
2. **並發處理**: 使用 Promise 機制防止重複刷新
3. **錯誤處理**: 刷新失敗時會自動登出用戶
4. **狀態同步**: 確保前端狀態與後端認證狀態一致 