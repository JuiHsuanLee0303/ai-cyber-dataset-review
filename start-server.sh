#!/bin/bash

echo "🚀 AI 資安資料審核系統 - 伺服器啟動腳本"
echo "=========================================="

# 檢查參數
USE_HTTPS=${1:-false}
PORT=${2:-8000}

echo "🔧 配置選項："
echo "   HTTPS: $USE_HTTPS"
echo "   端口: $PORT"

# 檢查是否在正確的目錄
if [ ! -f "app/main.py" ]; then
    echo "❌ 請在 backend 目錄中運行此腳本"
    exit 1
fi

# 設置環境變數
export DATABASE_URL=sqlite:///./data/test.db
export OLLAMA_BASE_URL=http://localhost:11434
export CORS_ORIGINS=https://localhost:5173,https://ai-cyber-dataset-review.vercel.app
export ENVIRONMENT=development

if [ "$USE_HTTPS" = "true" ]; then
    echo "🔐 啟用 HTTPS 模式..."
    
    # 檢查 SSL 證書
    if [ ! -f "../ssl/certificate.crt" ] || [ ! -f "../ssl/private.key" ]; then
        echo "🔐 SSL 證書不存在，正在生成..."
        cd ..
        chmod +x generate-ssl-certs.sh
        ./generate-ssl-certs.sh
        cd backend
    fi
    
    export USE_HTTPS=true
    export SSL_CERT_FILE=../ssl/certificate.crt
    export SSL_KEY_FILE=../ssl/private.key
    
    echo "🔒 使用 HTTPS 證書："
    echo "   證書: $SSL_CERT_FILE"
    echo "   私鑰: $SSL_KEY_FILE"
else
    echo "🌐 使用 HTTP 模式..."
    export USE_HTTPS=false
fi

# 安裝依賴（如果需要）
if [ ! -d "venv" ]; then
    echo "📦 創建虛擬環境..."
    python -m venv venv
fi

echo "📦 安裝依賴..."
source venv/bin/activate
pip install -r requirements.txt

# 啟動服務
echo "🚀 啟動服務..."
if [ "$USE_HTTPS" = "true" ]; then
    echo "🔒 啟動 HTTPS 服務..."
    uvicorn app.main:app \
        --host 0.0.0.0 \
        --port $PORT \
        --ssl-keyfile $SSL_KEY_FILE \
        --ssl-certfile $SSL_CERT_FILE \
        --reload
else
    echo "🌐 啟動 HTTP 服務..."
    uvicorn app.main:app \
        --host 0.0.0.0 \
        --port $PORT \
        --reload
fi

echo "✅ 服務啟動完成！"
if [ "$USE_HTTPS" = "true" ]; then
    echo "🔒 HTTPS 地址: https://localhost:$PORT"
else
    echo "🌐 HTTP 地址: http://localhost:$PORT"
fi
echo "🔗 API 文檔: http://localhost:$PORT/docs" 