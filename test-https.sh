#!/bin/bash

echo "🧪 測試 HTTPS 連接..."

# 檢查證書是否存在
if [ ! -f "ssl/certificate.crt" ] || [ ! -f "ssl/private.key" ]; then
    echo "❌ SSL 證書不存在，請先運行 ./generate-ssl-certs.sh"
    exit 1
fi

echo "✅ SSL 證書檢查通過"

# 測試證書有效性
echo "🔍 檢查證書詳情..."
openssl x509 -in ssl/certificate.crt -text -noout | grep -E "(Subject:|Not Before|Not After)"

echo ""
echo "🌐 測試本地 HTTPS 連接..."
echo "請確保後端服務正在運行在 HTTPS 模式"

# 測試 HTTPS 連接（如果服務正在運行）
if command -v curl &> /dev/null; then
    echo "📡 使用 curl 測試 HTTPS 連接..."
    curl -k -I https://localhost:8000/ 2>/dev/null | head -1
else
    echo "⚠️  curl 未安裝，無法自動測試連接"
fi

echo ""
echo "📋 手動測試步驟："
echo "1. 啟動 HTTPS 服務: ./start-server.sh true 8000"
echo "2. 在瀏覽器中訪問: https://localhost:8000"
echo "3. 接受安全警告並繼續"
echo "4. 檢查 API 文檔: https://localhost:8000/docs" 