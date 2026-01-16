# AI Agent 專案

一個功能齊全的 AI Agent，支援工具呼叫、記憶管理與多 LLM 介面。

## 功能特色

- **統一 LLM 介面**：透過 LiteLLM 支援 OpenAI、Anthropic、Gemini 等多種模型
- **工具系統**：模組化工具架構，內建檔案操作、網路搜尋、計算等工具
- **記憶管理**：短期與長期記憶系統
- **Python 版本管理**：使用 `uv` 進行專案層級的 Python 版本管理
- **完整測試**：所有功能都有對應的單元測試
- **程式碼規範**：遵循 PEP 8，使用 Ruff 進行 Linting

## 專案結構

```
agent/
├── src/
│   ├── agent/          # Agent 核心邏輯
│   │   ├── core.py     # 主要 Agent 類別
│   │   ├── memory.py   # 記憶系統
│   │   └── tool_interface.py  # 工具介面定義
│   ├── tools/          # 工具實作
│   │   ├── file_system.py     # 檔案操作
│   │   ├── search.py          # 網路搜尋
│   │   └── calculator.py      # 計算機
│   └── main.py         # 程式進入點
├── tests/              # 測試程式碼
├── scripts/            # 開發者腳本
└── .env                # 環境變數（需自行設定）
```

## 快速開始


### 1. 前置需求

- Windows / macOS / Linux
- `uv` 已安裝（Python 版本管理工具）

如果尚未安裝 `uv`，請執行：

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 設定環境變數

編輯 `.env` 檔案，填入您的 API Key：

```env
OPENAI_API_KEY=sk-your-key-here
AGENT_MODEL=gpt-4o
```

### 3. 執行 Agent

```powershell
uv run python src/main.py
```

Agent 會啟動互動式 CLI，您可以直接與 AI 對話。

## 開發指南

### 執行測試

**Windows:**
```powershell
.\scripts\test.ps1
```

**macOS/Linux:**
```bash
./scripts/test.sh
```

### 程式碼檢查

**Windows:**
```powershell
.\scripts\lint.ps1
```

**macOS/Linux:**
```bash
./scripts/lint.sh
```

### 自動修復格式問題

```powershell
uv run ruff format src tests
```

## 新增自訂工具

1. 在 `src/tools/` 建立新的工具檔案
2. 繼承 `BaseTool` 類別
3. 實作必要的方法（`name`、`description`、`parameters`、`execute`）
4. 在 `src/agent/core.py` 中註冊工具
5. 在 `tests/tools/` 建立對應的測試

範例請參考 `src/tools/calculator.py`。


## 授權

MIT License

## 貢獻

歡迎提交 Pull Request！請確保：
- 所有測試通過
- 程式碼通過 Lint 檢查
- 新功能有對應的測試
- 註解使用繁體中文
