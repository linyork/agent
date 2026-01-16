"""
網路搜尋工具的測試

注意：此測試會實際呼叫 DuckDuckGo API，因此需要網路連線。
在 CI/CD 環境中，可考慮使用 Mock 或標記為 integration test。
"""

import pytest

from tools.search import SearchTool


@pytest.mark.asyncio
async def test_search_tool_basic():
    """
    測試搜尋工具 - 基本搜尋

    注意：這是一個整合測試，需要實際的網路連線
    """
    tool = SearchTool()

    # 使用一個應該有結果的關鍵字
    result = await tool.execute(query="Python programming")

    # 驗證回傳的是字串
    assert isinstance(result, str)

    # 驗證結果中包含預期的關鍵詞
    assert len(result) > 0
    assert "結果" in result or "未找到" in result


@pytest.mark.asyncio
async def test_search_tool_properties():
    """
    測試搜尋工具 - 屬性檢查
    """
    tool = SearchTool()

    # 檢查 name
    assert tool.name == "web_search"

    # 檢查 description 是否為繁體中文
    assert isinstance(tool.description, str)
    assert "搜尋" in tool.description

    # 檢查 parameters 結構
    params = tool.parameters
    assert params["type"] == "object"
    assert "query" in params["properties"]
    assert "query" in params["required"]
