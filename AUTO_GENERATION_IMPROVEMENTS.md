# 自動生成模組改進說明

## 🎯 改進目標

根據用戶需求，對自動生成模組進行以下改進：
1. 將要重新生成的資料的 instruction、input、output、source 跟 reject 的理由一併放入 prompt 內
2. 使用 prompt engineering 來優化生成效果
3. 將生成的內容改為結構化輸出，包含 instruction、input、output

## 🔧 主要改進內容

### 1. 新增結構化生成功能

#### 檔案位置：`backend/app/services/ollama_client.py`

新增 `generate_structured_dataset()` 方法，提供以下功能：

```python
async def generate_structured_dataset(self, 
                                    instruction: str, 
                                    input_text: Optional[str] = None,
                                    system_prompt: Optional[str] = None,
                                    source: Optional[List[str]] = None,
                                    rejection_reasons: Optional[List[str]] = None) -> Dict[str, Any]:
```

**功能特點：**
- 接收完整的資料集資訊（instruction、input、system、source）
- 接收拒絕原因列表
- 返回結構化的 JSON 格式結果
- 包含完整的錯誤處理和回退機制

### 2. 優化的 Prompt Engineering

#### 結構化提示設計

新的 prompt 包含以下部分：

1. **系統角色定義**
   ```
   你是一位資安專家，專門協助生成高品質的指令微調資料集。
   你的任務是根據提供的指令和上下文，生成符合資安法規要求的訓練資料。
   ```

2. **原始需求**
   - 指令內容
   - 輸入內容（如果有）
   - 系統提示（如果有）

3. **法規依據**
   - 列出所有相關的法規條文
   - 確保生成內容符合法規要求

4. **需要改進的地方**
   - 列出所有拒絕原因
   - 提供具體的改進指導

5. **改進要求**
   ```
   請根據上述問題進行改進，確保：
   1. 內容準確且符合資安法規
   2. 實用且可執行
   3. 專業水準高
   4. 沒有錯誤或誤導性資訊
   ```

6. **輸出格式要求**
   - 明確要求 JSON 格式輸出
   - 包含 instruction、input、output 三個欄位

### 3. 結構化輸出格式

#### JSON 格式規範

```json
{
  "instruction": "改進後的指令，清楚明確且與資安相關",
  "input": "相關的輸入內容（如果需要的話）",
  "output": "高品質的輸出內容，符合資安法規要求且實用"
}
```

#### 輸出處理機制

1. **JSON 解析**：自動從回應中提取 JSON 物件
2. **格式驗證**：確保必要欄位存在
3. **錯誤回退**：如果 JSON 解析失敗，使用原始回應作為 output
4. **欄位映射**：將解析結果映射到資料集結構

### 4. 改進的重新生成流程

#### 檔案位置：`backend/app/services/regeneration.py`

**主要改進：**

1. **完整資訊傳遞**
   ```python
   structured_result = await ollama_client.generate_structured_dataset(
       instruction=dataset.instruction or "",
       input_text=dataset.input,
       system_prompt=dataset.system,
       source=dataset.source if dataset.source else [],
       rejection_reasons=reasons
   )
   ```

2. **結構化更新**
   ```python
   dataset.instruction = structured_result["instruction"]
   dataset.input = structured_result["input"]
   dataset.output = structured_result["output"]
   ```

3. **完整歷史記錄**
   ```python
   history.append({
       "instruction": dataset.instruction,
       "input": dataset.input,
       "output": dataset.output,
       "reject_count": dataset.reject_count,
       "accept_count": dataset.accept_count,
       "rejection_reasons": reasons
   })
   ```

## 🧪 測試功能

### 測試腳本：`test_structured_generation.py`

提供完整的測試功能：

1. **基本生成測試**
   - 測試程式碼安全性分析
   - 包含拒絕原因和法規依據

2. **政策生成測試**
   - 測試隱私政策生成
   - 包含系統提示和多個法規來源

3. **事件通報測試**
   - 測試資安事件通報說明
   - 驗證時限和程序說明

4. **JSON 解析測試**
   - 測試各種 JSON 格式
   - 驗證錯誤處理機制

## 🎨 Prompt Engineering 優化策略

### 1. 角色定義明確化
- 明確指定 AI 為資安專家
- 強調法規遵循要求
- 設定專業水準標準

### 2. 上下文資訊完整化
- 包含所有原始資料
- 明確列出法規依據
- 詳細說明拒絕原因

### 3. 改進指導具體化
- 提供具體的改進方向
- 設定品質標準
- 強調實用性和準確性

### 4. 輸出格式標準化
- 明確要求 JSON 格式
- 定義必要欄位
- 提供格式範例

## 🔄 工作流程

### 1. 觸發條件
- 資料被拒絕次數達到閾值
- 系統自動觸發重新生成

### 2. 資料收集
- 獲取原始資料集資訊
- 收集所有拒絕原因
- 準備法規依據

### 3. 結構化生成
- 構建優化的 prompt
- 調用 Ollama API
- 解析 JSON 回應

### 4. 資料更新
- 更新資料集內容
- 保存歷史記錄
- 重置審核狀態

## 📊 預期效果

### 1. 生成品質提升
- 更準確的資安內容
- 更實用的建議
- 更符合法規要求

### 2. 結構化程度提高
- 標準化的輸出格式
- 完整的欄位資訊
- 便於後續處理

### 3. 改進效果增強
- 基於具體拒絕原因改進
- 針對性問題解決
- 持續品質提升

### 4. 維護性改善
- 清晰的程式碼結構
- 完整的錯誤處理
- 便於測試和除錯

## 🚀 使用方式

### 1. 自動觸發
當資料被拒絕達到閾值時，系統會自動：
1. 收集拒絕原因
2. 調用結構化生成
3. 更新資料集內容
4. 重置審核狀態

### 2. 手動測試
```bash
# 運行測試腳本
python test_structured_generation.py
```

### 3. 配置調整
在系統設定中可以調整：
- 拒絕閾值
- Ollama 模型
- Ollama 服務地址

## 🔧 技術細節

### 1. 錯誤處理
- JSON 解析失敗時自動回退
- 網路錯誤時提供詳細錯誤資訊
- 模型回應異常時的處理機制

### 2. 效能優化
- 非串流生成，確保完整回應
- 60 秒超時設定
- 異步處理避免阻塞

### 3. 日誌記錄
- 詳細的生成過程日誌
- 錯誤資訊記錄
- 成功生成統計

---

*這些改進旨在提供更高品質、更結構化的自動生成功能，提升整體資料集品質和系統可用性。* 