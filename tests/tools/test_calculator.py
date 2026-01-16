"""
計算機工具的測試
"""

import pytest

from tools.calculator import CalculatorTool


@pytest.mark.asyncio
async def test_calculator_basic_operations():
    """
    測試計算機工具 - 基本運算
    """
    tool = CalculatorTool()

    # 加法
    result = await tool.execute(expression="2 + 3")
    assert result == "5"

    # 減法
    result = await tool.execute(expression="10 - 4")
    assert result == "6"

    # 乘法
    result = await tool.execute(expression="3 * 7")
    assert result == "21"

    # 除法
    result = await tool.execute(expression="20 / 4")
    assert result == "5.0"


@pytest.mark.asyncio
async def test_calculator_complex_expression():
    """
    測試計算機工具 - 複雜運算式
    """
    tool = CalculatorTool()

    result = await tool.execute(expression="(2 + 3) * 4")
    assert result == "20"

    result = await tool.execute(expression="10 / 2 + 3")
    assert result == "8.0"


@pytest.mark.asyncio
async def test_calculator_invalid_characters():
    """
    測試計算機工具 - 不允許的字元
    """
    tool = CalculatorTool()

    result = await tool.execute(expression="import os")
    assert "錯誤" in result

    result = await tool.execute(expression="2 + a")
    assert "錯誤" in result


@pytest.mark.asyncio
async def test_calculator_division_by_zero():
    """
    測試計算機工具 - 除以零
    """
    tool = CalculatorTool()

    result = await tool.execute(expression="5 / 0")
    assert "錯誤" in result
