"""
檔案系統工具的測試
"""

import os
import tempfile

import pytest

from tools.file_system import FileReadTool, FileWriteTool


@pytest.mark.asyncio
async def test_file_read_tool_success():
    """
    測試檔案讀取工具 - 成功案例
    """
    tool = FileReadTool()

    # 建立臨時檔案
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
        f.write("測試內容")
        temp_path = f.name

    try:
        # 執行讀取
        result = await tool.execute(path=temp_path)
        assert result == "測試內容"
    finally:
        # 清理
        os.unlink(temp_path)


@pytest.mark.asyncio
async def test_file_read_tool_not_found():
    """
    測試檔案讀取工具 - 檔案不存在
    """
    tool = FileReadTool()
    result = await tool.execute(path="/nonexistent/file.txt")
    assert "錯誤" in result or "找不到" in result


@pytest.mark.asyncio
async def test_file_write_tool_success():
    """
    測試檔案寫入工具 - 成功案例
    """
    tool = FileWriteTool()

    # 建立臨時目錄
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = os.path.join(tmpdir, "test_file.txt")

        # 執行寫入
        result = await tool.execute(path=temp_path, content="新內容")

        # 驗證結果訊息
        assert "成功" in result

        # 驗證檔案內容
        with open(temp_path, "r", encoding="utf-8") as f:
            assert f.read() == "新內容"


@pytest.mark.asyncio
async def test_file_write_tool_create_directory():
    """
    測試檔案寫入工具 - 自動建立目錄
    """
    tool = FileWriteTool()

    with tempfile.TemporaryDirectory() as tmpdir:
        # 不存在的子目錄
        nested_path = os.path.join(tmpdir, "subdir", "file.txt")

        result = await tool.execute(path=nested_path, content="內容")

        assert "成功" in result
        assert os.path.exists(nested_path)
