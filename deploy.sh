#!/bin/bash

echo "🚀 開始部署 AI 資安資料審核系統..."

# 檢查環境變數
if [ -z "$NGROK_URL" ]; then
    echo "❌ 請設置 NGROK_URL 環境變數"
    echo "例如: export NGROK_URL=https://your-ngrok-url.ngrok-free.app"
    exit 1
fi

echo "📝 使用 ngrok URL: $NGROK_URL"

# 創建前端環境變數文件
cat > frontend/.env << EOF
VITE_API_URL=$NGROK_URL
EOF

echo "✅ 前端環境變數已設置"

# 設置後端環境變數
export CORS_ORIGINS="$NGROK_URL,https://ai-cyber-dataset-review.vercel.app"
export ENVIRONMENT="development"

echo "🔧 設置後端 CORS 配置..."
echo "CORS_ORIGINS: $CORS_ORIGINS"

# 重新建構並啟動服務
echo "🔧 重新建構 Docker 映像..."
docker-compose down
docker-compose build --no-cache

echo "🚀 啟動服務..."
docker-compose up -d

echo "⏳ 等待服務啟動..."
sleep 10

# 檢查服務狀態
echo "📊 檢查服務狀態..."
docker-compose ps

echo "✅ 部署完成！"
echo "🌐 前端地址: https://ai-cyber-dataset-review.vercel.app"
echo "🔗 API 地址: $NGROK_URL"
echo ""
echo "📋 重要提醒："
echo "1. 確保 Vercel 專案已設置環境變數 VITE_API_URL=$NGROK_URL"
echo "2. 如果 ngrok URL 變更，請重新設置環境變數並重新部署"
echo "3. 檢查瀏覽器控制台是否有 CORS 錯誤" 