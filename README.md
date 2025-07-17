# 🛡️ AI 資安資料集審核系統

> 🎓 本專案為國立臺北商業大學人工智慧與商業應用碩士班 **李睿軒** 之碩士學位論文研究與實作成果，旨在建構一套結合 AI 生成與資安專家審核機制的資料集建構平台。透過整合人工智慧、資安法規知識與使用者互動流程，提升資安領域指令微調資料集之品質、可信度與實用性。

---

## 📌 專案簡介

AI 資安資料集審核系統是一個專為資安法規資料集設計的智能審核平台，提供結構化的資料審核流程與可視化管理介面。系統結合 AI 模型輔助審查、使用者角色管理及統計追蹤功能，支援多方參與與流程自動化，是一套實用性與研究性兼備的解決方案。

---

## 🏗️ 系統架構

### 🔧 技術棧

| 模組     | 技術                          |
|----------|-------------------------------|
| 前端     | Vue.js 3 + Vite + Tailwind CSS |
| 後端     | FastAPI (Python)              |
| AI 模型  | Ollama（支援 GPU 加速）       |
| 資料庫   | SQLite                        |
| 圖表呈現 | Chart.js                      |
| 容器化   | Docker + Docker Compose       |

### 📂 專案結構
```

├── backend/             # FastAPI 後端服務
├── frontend/            # Vue.js 前端應用
├── data/                # 資料存儲
├── docs/                # 專案與開發文檔
└── docker-compose.yml   # Docker 編排配置

````

---

## 🚀 快速開始

### ✅ 前置需求

- Docker 28.1.1+
- NVIDIA GPU（選用）
- NVIDIA Container Toolkit（如使用 GPU）

### 📦 安裝與啟動

```bash
# 1. 克隆專案
git clone <repository-url>
cd ai-cyber-dataset-review

# 2. 啟動所有服務
docker-compose up -d
````

### 🌐 系統介面

* 前端應用：[http://localhost:5173](http://localhost:5173)
* 後端 API：[http://localhost:8000](http://localhost:8000)
* Ollama 模型：[http://localhost:11434](http://localhost:11434)

---

## 👥 用戶角色與權限

| 角色   | 功能描述                     |
| ---- | ------------------------ |
| 管理員  | 系統設定、用戶管理、資料管理、統計查看、流程控制 |
| 資安專家 | 審核資料、填寫理由、查詢紀錄、個人貢獻統計    |

---

## 🔐 認證與安全機制

* JWT 認證與權限驗證
* Token 自動刷新與安全登出
* CORS 多來源支援
* Session 管理機制

📄 詳見：[docs/development/01-auth-mechanism.md](docs/development/01-auth-mechanism.md)

---

## 📊 核心功能模組

### ✅ 資料審核模組

* AI 輔助審核
* 拒絕理由管理
* 批次操作
* 審核進度追蹤與再生成流程

### 📈 統計儀表板

* 即時統計圖表
* 拒絕原因分析
* 專家排行榜
* 法規與資料分類可視化

### 🛠 管理功能

* 用戶管理
* 權限分層控制
* 系統參數設定

### 🤖 AI 輔助功能

* 自動生成審核建議
* 查詢法規條文依據
* 法規句子再生輔助

---

## 🧪 測試說明

提供完整測試指南，涵蓋：

* 功能與流程測試
* API 響應測試
* 跨裝置 RWD 測試

📄 測試文檔：[docs/testing/01-testing-guide.md](docs/testing/01-testing-guide.md)

---

## 🧰 開發指南

### 📁 環境變數設定（.env）

```env
# FastAPI 後端
DATABASE_URL=sqlite:///./data/test.db
OLLAMA_BASE_URL=http://host.docker.internal:11434
CORS_ORIGINS=https://initially-daring-foxhound.ngrok-free.app

# Ollama AI 模型
OLLAMA_HOST=http://0.0.0.0:11434
OLLAMA_CONTEXT_LENGTH=4096
OLLAMA_DEBUG=INFO
```

### ⚙️ 本地開發模式

```bash
# 啟動 FastAPI 後端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 啟動前端 Vue 應用
cd frontend
npm install
npm run dev
```

---

## 🎓 論文研究背景

本系統為碩士論文《檢索增強生成與微調大語言模型於資安管理應用之研究》之實驗平台，主要聚焦於以下研究重點：

* 探討應用 AI 模型自動生成指令微調資料集的可行性與效益
* 建構結合 AI 模型生成與資安專家審核之高品質資料集建構流程
* 實作自動化資料再生成機制，強化資料集之完整性與正確性
* 設計具擴展性與應用潛力之審核平台，驗證研究成果的實務可行性
* 利用本平台蒐集 AI 模型生成資料之品質與審核決策相關數據，作為後續研究依據

---

## 🛠️ 故障排除 FAQ

| 問題類型        | 解法建議                                 |
| ----------- | ------------------------------------ |
| Docker 啟動失敗 | 檢查是否佔用 port、確認 Docker 服務狀態           |
| GPU 無法啟用    | 驗證 NVIDIA 驅動與 Container Toolkit 安裝狀態 |
| 認證問題        | 確認 JWT 設定與登入權限、檢查後端認證日誌              |

---

## 📁 文檔結構

```
docs/
├── deployment/          # 部署與環境設定
├── development/         # 認證、審核、統計等開發修正
├── features/            # 系統功能規劃與優化
├── testing/             # 測試計劃與流程
└── ui-ux/               # 前後台使用者體驗優化
```

---

## 📜 授權條款

本專案採用 [MIT License](https://opensource.org/licenses/MIT) 授權，歡迎學術研究與非商業用途自由使用與引用，請註明來源。

---

👨‍💻 專案作者：**李睿軒 Jui-Hsuan Lee**

🎓 所屬單位：國立臺北商業大學 人工智慧與商業應用碩士班

📘 專案類型：碩士論文實作系統《檢索增強生成與微調大語言模型於資安管理應用之研究》

如有任何問題或合作意願，歡迎透過 [GitHub Issues](https://github.com/ai-cyber-dataset-review/issues) 或其他聯絡方式與作者聯繫。
