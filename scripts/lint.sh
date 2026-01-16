#!/bin/bash

# 執行程式碼風格檢查 (使用 ruff)

echo "正在執行程式碼檢查..."

# 檢查 uv 是否安裝
if ! command -v uv &> /dev/null; then
    echo "錯誤: 找不到 uv 指令，請先安裝 uv。"
    exit 1
fi

# 執行 ruff check
echo -e "\033[0;33m1. Linting (Ruff)...\033[0m"
uv run ruff check src tests

if [ $? -ne 0 ]; then
    echo -e "\033[0;31mLint 檢查失敗！\033[0m"
    exit 1
fi

# 執行 ruff format --check
echo -e "\033[0;33m2. Formatting Check...\033[0m"
uv run ruff format --check src tests

if [ $? -eq 0 ]; then
    echo -e "\033[0;32m所有檢查通過！\033[0m"
else
    echo -e "\033[0;31m格式檢查失敗。請執行 'uv run ruff format' 來自動修復。\033[0m"
    exit 1
fi
