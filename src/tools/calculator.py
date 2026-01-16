from typing import Any, Dict

from agent.tool_interface import BaseTool


class CalculatorTool(BaseTool):
    """
    簡單計算機工具
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "執行數學表達式計算。參數: expression (例如 '2 + 2 * 5')"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "數學表達式"}},
            "required": ["expression"],
        }

    async def execute(self, expression: str) -> str:
        try:
            # 限制可用字元以確保安全 (簡單實作)
            allowed_chars = "0123456789+-*/(). "
            if any(c not in allowed_chars for c in expression):
                return "錯誤: 僅允許基本數學運算 (0-9, +, -, *, /, (, ))"

            # 使用 eval 計算 (警告: 在生產環境請使用更安全的庫，如 asteval)
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"計算錯誤: {e}"
