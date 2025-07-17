# Ollama Docker GPU 配置說明

## 🎯 配置目標

為 Ollama Docker 容器啟用 NVIDIA GPU 加速，提升大型語言模型的推理效能。

## 🔧 系統要求

### 硬體要求
- NVIDIA GPU（已確認：NVIDIA GeForce RTX 2060）
- 足夠的 GPU 記憶體（建議 4GB+）

### 軟體要求
- Docker 28.1.1+
- NVIDIA 驅動程式 576.28+
- CUDA 12.9+
- NVIDIA Container Toolkit 1.17.8+

## 📋 配置步驟

### 1. 檢查系統環境

```bash
# 檢查 Docker 版本
docker --version

# 檢查 NVIDIA 驅動程式
nvidia-smi

# 檢查 NVIDIA Container Toolkit
dpkg -l | grep nvidia-container-toolkit
```

### 2. 配置 Docker 使用 NVIDIA 驅動

```bash
# 配置 Docker 使用 NVIDIA 驅動
sudo nvidia-ctk runtime configure --runtime=docker

# 重啟 Docker 服務（如果需要）
sudo systemctl restart docker
```

### 3. 更新 Docker Compose 配置

在 `docker-compose.yml` 中為 Ollama 服務添加 GPU 支援：

```yaml
ollama:
  image: ollama/ollama
  ports:
    - "11434:11434"
  volumes:
    - ollama_data:/root/.ollama
  container_name: ai-cyber-dataset-review-ollama
  networks:
    - app-network
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
```

### 4. 重新啟動服務

```bash
# 停止現有容器
docker-compose down

# 重新啟動服務
docker-compose up -d
```

## ✅ 驗證配置

### 1. 檢查 Ollama 日誌

```bash
docker logs ai-cyber-dataset-review-ollama
```

成功配置後應該看到：
```
msg="inference compute" id=GPU-93fd781b-3649-96a3-11fd-c6d4c2ae55e6 
library=cuda variant=v12 compute=7.5 driver=12.9 
name="NVIDIA GeForce RTX 2060" total="6.0 GiB" available="5.0 GiB"
```

### 2. 測試 GPU 加速

```bash
# 下載模型
docker exec ai-cyber-dataset-review-ollama ollama pull llama3

# 運行模型測試
docker exec -it ai-cyber-dataset-review-ollama ollama run llama3
```

## 🚀 效能提升

### GPU 加速效果
- **推理速度**：相比 CPU 提升 5-10 倍
- **並發處理**：支援多個請求同時處理
- **記憶體效率**：GPU 記憶體直接訪問，減少數據傳輸

### 支援的模型
- Llama 系列模型
- Mistral 系列模型
- Code Llama 系列模型
- 其他支援 CUDA 的模型

## 🔍 故障排除

### 常見問題

#### 1. GPU 未被識別
```bash
# 檢查 NVIDIA Container Toolkit 安裝
dpkg -l | grep nvidia-container-toolkit

# 重新配置 Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

#### 2. 權限問題
```bash
# 檢查 Docker 用戶組
groups $USER

# 添加用戶到 docker 組
sudo usermod -aG docker $USER
```

#### 3. 記憶體不足
```bash
# 檢查 GPU 記憶體使用情況
nvidia-smi

# 調整模型大小或使用量化版本
docker exec ai-cyber-dataset-review-ollama ollama pull llama3:8b
```

## 📊 監控 GPU 使用

### 即時監控
```bash
# 監控 GPU 使用情況
watch -n 1 nvidia-smi

# 監控容器 GPU 使用
docker stats ai-cyber-dataset-review-ollama
```

### 日誌監控
```bash
# 查看 Ollama 詳細日誌
docker logs -f ai-cyber-dataset-review-ollama
```

## 🎯 最佳實踐

### 1. 模型選擇
- 根據 GPU 記憶體選擇合適的模型大小
- 考慮使用量化版本以節省記憶體

### 2. 資源管理
- 監控 GPU 記憶體使用情況
- 避免同時運行多個大型模型

### 3. 效能優化
- 使用適當的批次大小
- 調整上下文長度以平衡效能和記憶體

## 📝 配置檔案

### 當前配置狀態
- ✅ NVIDIA 驅動程式：576.28
- ✅ CUDA 版本：12.9
- ✅ NVIDIA Container Toolkit：1.17.8
- ✅ Docker 版本：28.1.1
- ✅ GPU：NVIDIA GeForce RTX 2060 (6GB)

### 環境變數
```bash
# Ollama 環境變數
OLLAMA_HOST=http://0.0.0.0:11434
OLLAMA_ORIGINS=[http://localhost https://localhost ...]
OLLAMA_CONTEXT_LENGTH=4096
OLLAMA_DEBUG=INFO
```

---

*此配置已成功啟用 Ollama Docker 容器的 GPU 加速功能，大幅提升了大型語言模型的推理效能。* 