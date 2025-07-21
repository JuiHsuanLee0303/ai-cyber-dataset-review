# HTTPS 設置指南

## 概述

本指南說明如何為 AI 資安資料審核系統的後端啟用 HTTPS 支援。

## 快速開始

### 1. 生成 SSL 證書

```bash
# 生成自簽名 SSL 證書
chmod +x generate-ssl-certs.sh
./generate-ssl-certs.sh
```

### 2. 啟動 HTTPS 服務

#### 使用 Docker（推薦）
```bash
# 啟動 HTTPS 服務
chmod +x start-https.sh
./start-https.sh
```

#### 本地開發
```bash
cd backend
chmod +x start-server.sh

# 啟動 HTTPS 服務
./start-server.sh true 8000

# 或啟動 HTTP 服務
./start-server.sh false 8000
```

## 配置選項

### 環境變數

| 變數名 | 預設值 | 說明 |
|--------|--------|------|
| `USE_HTTPS` | `false` | 是否啟用 HTTPS |
| `SSL_CERT_FILE` | `ssl/certificate.crt` | SSL 證書檔案路徑 |
| `SSL_KEY_FILE` | `ssl/private.key` | SSL 私鑰檔案路徑 |
| `HTTPS_PORT` | `8000` | HTTPS 服務端口 |

### Docker 配置

Docker 容器會自動檢測 SSL 證書並啟用 HTTPS：

```yaml
# docker-compose.yml
services:
  backend:
    ports:
      - "8000:8000"   # HTTP
      - "8443:8000"   # HTTPS
    volumes:
      - ./ssl:/app/ssl  # 掛載 SSL 證書
```

## 訪問地址

啟動服務後，可以通過以下地址訪問：

- **HTTP**: http://localhost:8000
- **HTTPS**: https://localhost:8443 (Docker) 或 https://localhost:8000 (本地)
- **API 文檔**: https://localhost:8000/docs

## 瀏覽器安全警告

使用自簽名證書時，瀏覽器會顯示安全警告：

1. 點擊「進階」
2. 點擊「繼續前往 localhost」
3. 或點擊「接受風險並繼續」

## 生產環境

在生產環境中，建議使用正式的 SSL 證書：

### 使用 Let's Encrypt

```bash
# 安裝 certbot
sudo apt install certbot

# 獲取證書
sudo certbot certonly --standalone -d your-domain.com

# 複製證書到專案目錄
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/certificate.crt
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/private.key
```

### 使用其他 CA 證書

將您的證書檔案放置到 `ssl/` 目錄：
- `ssl/certificate.crt` - 證書檔案
- `ssl/private.key` - 私鑰檔案

## 故障排除

### 證書權限問題

```bash
# 設置正確的檔案權限
chmod 600 ssl/private.key
chmod 644 ssl/certificate.crt
```

### 端口被佔用

```bash
# 檢查端口使用情況
netstat -tulpn | grep :8000

# 或使用不同端口
./start-server.sh true 8443
```

### CORS 錯誤

確保 CORS 配置包含 HTTPS 地址：

```python
# backend/app/main.py
origins = [
    "https://localhost:5173",
    "https://your-domain.com"
]
```

## 安全建議

1. **定期更新證書**: 自簽名證書有效期為 365 天
2. **使用強密鑰**: 生成 2048 位或更強的 RSA 密鑰
3. **限制訪問**: 在生產環境中配置防火牆規則
4. **監控日誌**: 定期檢查伺服器日誌

## 腳本說明

| 腳本 | 用途 |
|------|------|
| `generate-ssl-certs.sh` | 生成自簽名 SSL 證書 |
| `start-https.sh` | 使用 Docker 啟動 HTTPS 服務 |
| `start-local-https.sh` | 本地啟動 HTTPS 服務 |
| `start-server.sh` | 智能啟動腳本（支援 HTTP/HTTPS）| 