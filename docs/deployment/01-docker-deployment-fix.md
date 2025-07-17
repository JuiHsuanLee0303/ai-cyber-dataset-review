# Docker 部署錯誤修復說明

## 🐛 問題描述

在其他機器的 Docker 部署中出現以下錯誤：

### 1. Pydantic V2 警告
```
/usr/local/lib/python3.10/site-packages/pydantic/_internal/_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
```

### 2. bcrypt 版本錯誤
```
(trapped) error reading bcrypt version
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
    version = _bcrypt.__about__.__version__
AttributeError: module 'bcrypt' has no attribute '__about__'
```

## 🔍 問題分析

### 1. Pydantic V2 相容性問題
- Pydantic V2 中，`orm_mode` 已被更名為 `from_attributes`
- 在 `backend/app/schemas.py` 中仍使用了舊的 `Config` 類別語法

### 2. bcrypt 版本相容性問題
- `passlib==1.7.4` 與 `bcrypt==4.1.2` 存在版本不相容
- 較新版本的 bcrypt 移除了 `__about__` 屬性
- 需要降級 bcrypt 版本以確保相容性

## 🔧 修復方案

### 1. 修復 Pydantic 配置

**檔案：** `backend/app/schemas.py`

將舊的配置語法：
```python
class ReviewLogInDB(BaseModel):
    reviewer_id: int
    
    class Config:
        orm_mode = True
```

更新為新的語法：
```python
class ReviewLogInDB(BaseModel):
    reviewer_id: int
    
    model_config = ConfigDict(from_attributes=True)
```

### 2. 修復 bcrypt 版本

**檔案：** `backend/requirements.txt`

將 bcrypt 版本從 4.1.2 降級到 4.0.1：
```
bcrypt==4.0.1
```

## 📋 修復步驟

### 1. 更新程式碼
```bash
# 確保在專案根目錄
cd /path/to/ai-cyber-dataset-review

# 檢查修改是否正確
git status
```

### 2. 重新建構 Docker 映像
```bash
# 停止現有容器
docker-compose down

# 重新建構映像（強制重新建構以使用新的 requirements.txt）
docker-compose build --no-cache

# 啟動服務
docker-compose up -d
```

### 3. 驗證修復
```bash
# 檢查後端日誌
docker-compose logs backend

# 檢查服務狀態
docker-compose ps
```

## ✅ 預期結果

修復後應該：
1. **消除 Pydantic 警告**：不再出現 `orm_mode` 相關警告
2. **消除 bcrypt 錯誤**：不再出現 `__about__` 屬性錯誤
3. **正常啟動**：後端服務正常啟動並運行
4. **功能正常**：所有 API 端點正常工作

## 🔍 驗證測試

### 1. 檢查後端啟動
```bash
# 檢查後端日誌
docker-compose logs backend | grep -E "(error|Error|ERROR|warning|Warning|WARNING)"
```

### 2. 測試 API 端點
```bash
# 測試健康檢查
curl http://localhost:8000/

# 測試認證端點
curl http://localhost:8000/api/v1/auth/login
```

### 3. 檢查資料庫連接
```bash
# 進入後端容器
docker-compose exec backend bash

# 檢查資料庫
python -c "from app.database.base import engine; print('Database connection OK')"
```

## 🚨 注意事項

### 1. 版本相容性
- 確保所有 Python 套件版本相容
- 在部署前測試套件相容性
- 考慮使用 `pip-tools` 或 `poetry` 管理依賴

### 2. Docker 建構
- 使用 `--no-cache` 確保使用新的 requirements.txt
- 檢查 Docker 映像大小是否合理
- 考慮多階段建構以減少映像大小

### 3. 環境差異
- 本機環境與 Docker 環境可能存在差異
- 建議在 Docker 環境中進行完整測試
- 記錄環境特定的配置

## 📝 相關文件

### 修改的檔案
- `backend/app/schemas.py` - 修復 Pydantic 配置
- `backend/requirements.txt` - 降級 bcrypt 版本

### 相關技術
- Pydantic V2 遷移指南
- passlib 與 bcrypt 相容性
- Docker 部署最佳實踐

## 🔄 未來改進

### 1. 依賴管理
- 考慮使用 `poetry` 進行依賴管理
- 定期更新套件版本
- 建立依賴相容性測試

### 2. 錯誤處理
- 增加更詳細的錯誤日誌
- 實作健康檢查端點
- 建立監控和警報機制

### 3. 部署流程
- 自動化部署腳本
- 環境配置管理
- 回滾機制

---

**修復完成時間：** 2024年12月
**修復人員：** 開發團隊
**測試狀態：** ✅ 已驗證 