#!/bin/bash

# 執行專案的所有測試 (使用 pytest)

echo "正在執行測試..."

# 檢查 uv 是否安裝
if ! command -v uv &> /dev/null; then
    echo "錯誤: 找不到 uv 指令，請先安裝 uv。"
    exit 1
fi

# 執行 pytest
uv run pytest -v --tb=short

if [ $? -eq 0 ]; then
    echo -e "\033[0;32m所有測試通過！\033[0m"
else
    echo -e "\033[0;31m測試失敗，請檢查錯誤訊息。\033[0m"
    exit 1
fi
