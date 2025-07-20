#!/bin/bash

echo "🔧 設置 Vercel 環境變數..."

# 檢查環境變數
if [ -z "$NGROK_URL" ]; then
    echo "❌ 請設置 NGROK_URL 環境變數"
    echo "例如: export NGROK_URL=https://your-ngrok-url.ngrok-free.app"
    exit 1
fi

echo "📝 使用 ngrok URL: $NGROK_URL"

# 檢查是否安裝了 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ 請先安裝 Vercel CLI"
    echo "npm install -g vercel"
    exit 1
fi

# 設置 Vercel 環境變數
echo "🔧 設置 Vercel 環境變數..."
vercel env add VITE_API_URL production <<< "$NGROK_URL"
vercel env add VITE_API_URL preview <<< "$NGROK_URL"

echo "✅ Vercel 環境變數設置完成！"
echo ""
echo "📋 下一步："
echo "1. 重新部署 Vercel 專案"
echo "2. 或者使用: vercel --prod"
echo "3. 檢查瀏覽器控制台是否還有 CORS 錯誤" 