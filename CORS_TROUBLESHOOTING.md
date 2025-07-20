# CORS 錯誤故障排除指南

## 問題描述
當前端部署在 Vercel，後端使用 ngrok 時，可能會遇到以下 CORS 錯誤：
```
Access to XMLHttpRequest at 'https://initially-daring-foxhound.ngrok-free.app/api/v1/auth/token' 
from origin 'https://ai-cyber-dataset-review.vercel.app' has been blocked by CORS policy
```

## 解決方案

### 1. 設置環境變數

#### 後端環境變數
```bash
export NGROK_URL=https://your-ngrok-url.ngrok-free.app
export CORS_ORIGINS="$NGROK_URL,https://ai-cyber-dataset-review.vercel.app"
export ENVIRONMENT=development
```

#### 前端環境變數（Vercel）
在 Vercel 專案設置中添加環境變數：
- 名稱：`VITE_API_URL`
- 值：`https://your-ngrok-url.ngrok-free.app`

### 2. 使用自動化腳本

#### 設置 Vercel 環境變數
```bash
# 設置 NGROK_URL 環境變數
export NGROK_URL=https://your-ngrok-url.ngrok-free.app

# 運行設置腳本
./setup-vercel-env.sh
```

#### 重新部署
```bash
# 設置環境變數
export NGROK_URL=https://your-ngrok-url.ngrok-free.app

# 重新部署
./deploy.sh
```

### 3. 測試 CORS 配置
```bash
# 設置環境變數
export NGROK_URL=https://your-ngrok-url.ngrok-free.app

# 測試 CORS
./test-cors.sh
```

## 常見問題

### Q: ngrok URL 變更後怎麼辦？
A: 每次 ngrok URL 變更後，需要：
1. 更新 `NGROK_URL` 環境變數
2. 重新設置 Vercel 環境變數
3. 重新部署前端

### Q: 如何檢查環境變數是否正確設置？
A: 在瀏覽器控制台中查看：
```javascript
console.log('API URL:', import.meta.env.VITE_API_URL)
```

### Q: 後端 CORS 配置是否正確？
A: 檢查後端日誌，確認 CORS 中間件已正確載入，並且允許的來源包含您的域名。

## 手動檢查步驟

1. **檢查前端環境變數**
   - 打開瀏覽器開發者工具
   - 查看 Console 中的 API URL 日誌

2. **檢查後端 CORS 配置**
   - 查看後端啟動日誌
   - 確認 CORS 中間件已載入

3. **測試 API 連接**
   - 使用 curl 或 Postman 測試 API 端點
   - 檢查響應標頭中的 CORS 設置

## 預防措施

1. **使用固定的 ngrok 域名**（付費版）
2. **設置自動化部署腳本**
3. **定期檢查環境變數設置**
4. **監控 CORS 錯誤日誌** 