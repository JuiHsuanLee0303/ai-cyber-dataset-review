#!/bin/bash

echo "🚀 啟動本地 HTTPS 後端服務..."

# 檢查是否在 backend 目錄
if [ ! -f "app/main.py" ]; then
    echo "❌ 請在 backend 目錄中運行此腳本"
    exit 1
fi

# 檢查 SSL 證書是否存在
if [ ! -f "../ssl/certificate.crt" ] || [ ! -f "../ssl/private.key" ]; then
    echo "🔐 SSL 證書不存在，正在生成..."
    cd ..
    chmod +x generate-ssl-certs.sh
    ./generate-ssl-certs.sh
    cd backend
fi

# 設置環境變數
export DATABASE_URL=sqlite:///./data/test.db
export OLLAMA_BASE_URL=http://localhost:11434
export CORS_ORIGINS=https://localhost:5173,https://ai-cyber-dataset-review.vercel.app
export ENVIRONMENT=development

echo "🔧 設置環境變數..."
echo "DATABASE_URL: $DATABASE_URL"
echo "CORS_ORIGINS: $CORS_ORIGINS"

# 安裝依賴（如果需要）
if [ ! -d "venv" ]; then
    echo "📦 創建虛擬環境..."
    python -m venv venv
fi

echo "📦 安裝依賴..."
source venv/bin/activate
pip install -r requirements.txt

echo "🚀 啟動 HTTPS 服務..."
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --ssl-keyfile ../ssl/private.key \
    --ssl-certfile ../ssl/certificate.crt \
    --reload

echo "✅ HTTPS 服務啟動完成！"
echo "🔒 HTTPS 地址: https://localhost:8000"
echo "🔗 API 文檔: https://localhost:8000/docs" 