#!/bin/bash

echo "🚀 啟動 HTTPS 後端服務..."

# 檢查 SSL 證書是否存在
if [ ! -f "ssl/certificate.crt" ] || [ ! -f "ssl/private.key" ]; then
    echo "🔐 SSL 證書不存在，正在生成..."
    chmod +x generate-ssl-certs.sh
    ./generate-ssl-certs.sh
fi

# 設置環境變數
export NGROK_URL=https://your-ngrok-url.ngrok-free.app
export CORS_ORIGINS="$NGROK_URL,https://ai-cyber-dataset-review.vercel.app"
export ENVIRONMENT="development"

echo "🔧 設置環境變數..."
echo "NGROK_URL: $NGROK_URL"
echo "CORS_ORIGINS: $CORS_ORIGINS"

# 重新建構並啟動服務
echo "🔧 重新建構 Docker 映像..."
docker-compose down
docker-compose build --no-cache

echo "🚀 啟動 HTTPS 服務..."
docker-compose up -d

echo "⏳ 等待服務啟動..."
sleep 10

# 檢查服務狀態
echo "📊 檢查服務狀態..."
docker-compose ps

echo "✅ HTTPS 服務啟動完成！"
echo "🌐 HTTP 地址: http://localhost:8000"
echo "🔒 HTTPS 地址: https://localhost:8443"
echo "🔗 API 文檔: https://localhost:8443/docs"
echo ""
echo "📋 重要提醒："
echo "1. 使用自簽名證書，瀏覽器會顯示安全警告"
echo "2. 在瀏覽器中點擊 '進階' -> '繼續前往 localhost'"
echo "3. 前端需要更新 API URL 為 https://localhost:8443" 