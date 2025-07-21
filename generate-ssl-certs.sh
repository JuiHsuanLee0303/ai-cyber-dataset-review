#!/bin/bash

echo "🔐 生成自簽名 SSL 證書..."

# 創建證書目錄
mkdir -p ssl

# 生成私鑰
openssl genrsa -out ssl/private.key 2048

# 生成證書簽名請求 (CSR)
openssl req -new -key ssl/private.key -out ssl/certificate.csr -subj "/C=TW/ST=Taiwan/L=Taipei/O=AI-Cyber-Dataset-Review/CN=localhost"

# 生成自簽名證書
openssl x509 -req -days 365 -in ssl/certificate.csr -signkey ssl/private.key -out ssl/certificate.crt

# 設置權限
chmod 600 ssl/private.key
chmod 644 ssl/certificate.crt

echo "✅ SSL 證書生成完成！"
echo "📁 證書位置: ssl/certificate.crt"
echo "🔑 私鑰位置: ssl/private.key"
echo ""
echo "⚠️  注意：這是自簽名證書，瀏覽器會顯示安全警告"
echo "   在生產環境中，請使用正式的 SSL 證書" 