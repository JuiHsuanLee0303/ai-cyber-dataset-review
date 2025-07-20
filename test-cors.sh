#!/bin/bash

echo "🧪 測試 CORS 配置..."

# 檢查環境變數
if [ -z "$NGROK_URL" ]; then
    echo "❌ 請設置 NGROK_URL 環境變數"
    echo "例如: export NGROK_URL=https://your-ngrok-url.ngrok-free.app"
    exit 1
fi

echo "📝 測試 URL: $NGROK_URL"

# 測試 CORS 預檢請求
echo "🔍 測試 CORS 預檢請求..."
curl -X OPTIONS \
  -H "Origin: https://ai-cyber-dataset-review.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v "$NGROK_URL/api/v1/auth/token"

echo ""
echo "🔍 測試實際 API 請求..."
curl -X GET \
  -H "Origin: https://ai-cyber-dataset-review.vercel.app" \
  -v "$NGROK_URL/"

echo ""
echo "✅ CORS 測試完成！"
echo "📋 檢查上面的響應是否包含正確的 CORS 標頭："
echo "   - Access-Control-Allow-Origin"
echo "   - Access-Control-Allow-Methods"
echo "   - Access-Control-Allow-Headers" 