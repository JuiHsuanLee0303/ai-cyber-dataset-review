# 專案文檔索引

歡迎來到 AI 資安資料集審核系統的文檔中心。本文檔提供了系統的完整技術文檔和使用指南。

## 📚 文檔分類

### 🚀 部署文檔 (deployment/)
部署和環境配置相關文檔

- [01-docker-deployment-fix.md](deployment/01-docker-deployment-fix.md) - Docker 部署修復說明
- [02-gpu-setup.md](deployment/02-gpu-setup.md) - Ollama Docker GPU 配置說明

### 💻 開發文檔 (development/)
開發相關的技術文檔

- [01-auth-mechanism.md](development/01-auth-mechanism.md) - 認證機制優化說明
- [02-instruction-dataset-guide.md](development/02-instruction-dataset-guide.md) - 指令資料集指南
- [03-stats-api-fix.md](development/03-stats-api-fix.md) - 統計 API 修復說明
- [04-review-api-fix.md](development/04-review-api-fix.md) - 審核 API 修復說明
- [05-dashboard-permission-update.md](development/05-dashboard-permission-update.md) - 儀表板權限更新
- [06-review-interface-improvements.md](development/06-review-interface-improvements.md) - 審核介面改進
- [07-source-display-optimization.md](development/07-source-display-optimization.md) - 來源顯示優化

### ⚡ 功能特性 (features/)
系統功能特性和改進說明

- [01-approval-threshold-feature.md](features/01-approval-threshold-feature.md) - 審核閾值功能
- [02-regulation-generation-feature.md](features/02-regulation-generation-feature.md) - 法規生成功能
- [03-batch-add-feature.md](features/03-batch-add-feature.md) - 批量新增功能
- [04-manual-regeneration.md](features/04-manual-regeneration.md) - 手動重新生成
- [05-auto-generation-improvements.md](features/05-auto-generation-improvements.md) - 自動生成改進
- [06-auto-update-optimization.md](features/06-auto-update-optimization.md) - 自動更新優化
- [07-regeneration-status-optimization.md](features/07-regeneration-status-optimization.md) - 重新生成狀態優化
- [08-regeneration-review-fix.md](features/08-regeneration-review-fix.md) - 重新生成審核修復
- [09-display-mode-and-batch-delete.md](features/09-display-mode-and-batch-delete.md) - 顯示模式和批量刪除
- [10-rejection-reason-optimization.md](features/10-rejection-reason-optimization.md) - 拒絕理由優化

### 🧪 測試文檔 (testing/)
測試相關指南和說明

- [01-testing-guide.md](testing/01-testing-guide.md) - AI 資安資料集審核系統測試工程師參考文件

### 🎨 UI/UX 文檔 (ui-ux/)
用戶界面和用戶體驗相關文檔

- [01-ui-optimization.md](ui-ux/01-ui-optimization.md) - UI 優化說明
- [02-desktop-ui-ux-optimization.md](ui-ux/02-desktop-ui-ux-optimization.md) - 桌面版 UI/UX 優化
- [03-mobile-ui-ux-optimization.md](ui-ux/03-mobile-ui-ux-optimization.md) - 移動版 UI/UX 優化
- [04-rwd-optimization.md](ui-ux/04-rwd-optimization.md) - 響應式設計優化
- [05-admin-settings-ui-ux-optimization.md](ui-ux/05-admin-settings-ui-ux-optimization.md) - 管理設定 UI/UX 優化
- [06-review-ui-optimization.md](ui-ux/06-review-ui-optimization.md) - 審核 UI 優化

## 🔍 快速查找

### 按主題查找

#### 部署相關
- Docker 部署: [deployment/01-docker-deployment-fix.md](deployment/01-docker-deployment-fix.md)
- GPU 配置: [deployment/02-gpu-setup.md](deployment/02-gpu-setup.md)

#### 認證與安全
- 認證機制: [development/01-auth-mechanism.md](development/01-auth-mechanism.md)
- 權限管理: [development/05-dashboard-permission-update.md](development/05-dashboard-permission-update.md)

#### API 開發
- 統計 API: [development/03-stats-api-fix.md](development/03-stats-api-fix.md)
- 審核 API: [development/04-review-api-fix.md](development/04-review-api-fix.md)

#### 功能特性
- 批量處理: [features/03-batch-add-feature.md](features/03-batch-add-feature.md)
- 自動生成: [features/05-auto-generation-improvements.md](features/05-auto-generation-improvements.md)
- 審核流程: [features/01-approval-threshold-feature.md](features/01-approval-threshold-feature.md)

#### 用戶界面
- 響應式設計: [ui-ux/04-rwd-optimization.md](ui-ux/04-rwd-optimization.md)
- 移動端優化: [ui-ux/03-mobile-ui-ux-optimization.md](ui-ux/03-mobile-ui-ux-optimization.md)
- 桌面端優化: [ui-ux/02-desktop-ui-ux-optimization.md](ui-ux/02-desktop-ui-ux-optimization.md)

#### 測試指南
- 完整測試指南: [testing/01-testing-guide.md](testing/01-testing-guide.md)

## 📖 閱讀建議

### 新用戶
1. 先閱讀 [deployment/02-gpu-setup.md](deployment/02-gpu-setup.md) 了解系統配置
2. 查看 [testing/01-testing-guide.md](testing/01-testing-guide.md) 了解系統功能
3. 參考 [development/01-auth-mechanism.md](development/01-auth-mechanism.md) 了解認證機制

### 開發者
1. 從 [development/01-auth-mechanism.md](development/01-auth-mechanism.md) 開始了解系統架構
2. 查看 [features/](features/) 目錄了解功能實現
3. 參考 [ui-ux/](ui-ux/) 目錄了解前端優化

### 測試工程師
1. 詳細閱讀 [testing/01-testing-guide.md](testing/01-testing-guide.md)
2. 參考 [ui-ux/](ui-ux/) 目錄了解界面測試要點
3. 查看 [features/](features/) 目錄了解功能測試範圍

## 🔄 文檔更新

本文檔會根據系統更新持續維護。如有新的文檔或更新，請：
1. 按照命名規則添加文件
2. 更新本文檔的索引
3. 確保文檔內容的準確性和完整性