import json
from typing import Any, Dict, List

from litellm import completion

from tools.calculator import CalculatorTool
from tools.file_system import FileReadTool, FileWriteTool
from tools.search import SearchTool

from .memory import Memory
from .tool_interface import BaseTool


class Agent:
    """
    Agent 核心類別
    負責管理記憶、工具呼叫與 LLM 互動
    """

    def __init__(self, model_name: str = "gpt-4o"):
        """
        初始化 Agent

        Args:
            model_name (str): 使用的模型名稱
        """
        self.model_name = model_name
        self.memory = Memory()
        self.tools: List[BaseTool] = [
            FileReadTool(),
            FileWriteTool(),
            SearchTool(),
            CalculatorTool(),
        ]

    def _get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        將工具轉換為 OpenAI 格式的 Schema
        """
        schemas = []
        for tool in self.tools:
            schemas.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
            )
        return schemas

    async def _execute_tool_calls(self, tool_calls: List[Any]) -> List[Dict[str, Any]]:
        """
        執行 LLM 回傳的工具呼叫請求
        """
        results = []
        for call in tool_calls:
            function_name = call.function.name
            arguments_str = call.function.arguments

            # 尋找對應的工具
            tool = next((t for t in self.tools if t.name == function_name), None)

            if tool:
                try:
                    arguments = json.loads(arguments_str)

                    # 執行工具
                    result = await tool.execute(**arguments)

                    results.append(
                        {"role": "tool", "tool_call_id": call.id, "content": str(result)}
                    )
                except Exception as e:
                    error_msg = f"工具執行錯誤: {str(e)}"
                    results.append({"role": "tool", "tool_call_id": call.id, "content": error_msg})
            else:
                results.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": f"找不到工具: {function_name}",
                    }
                )
        return results

    async def think(self, user_input: str) -> str:
        """
        思考並產生回應 (包含工具使用迴圈)

        Args:
            user_input (str): 使用者輸入的訊息

        Returns:
            str: Agent 的回應
        """
        # 1. 記錄使用者輸入到短期記憶
        self.memory.add("user", user_input)

        # 最多允許 5 次工具呼叫迴圈，避免無窮迴圈
        max_turns = 5
        current_turn = 0

        while current_turn < max_turns:
            current_turn += 1
            messages = self.memory.get_messages()
            tool_schemas = self._get_tool_schemas()

            try:
                # 呼叫 LLM（暫時抑制 Pydantic 序列化警告）
                import warnings

                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
                    response_obj = completion(
                        model=self.model_name, messages=messages, tools=tool_schemas, tool_choice="auto"
                    )

                message = response_obj.choices[0].message

                # 若沒有工具呼叫，直接回傳內容
                if not message.tool_calls:
                    response_text = message.content or ""
                    self.memory.add("assistant", response_text)
                    self.memory.save_long_term()
                    return response_text

                # 有工具呼叫，先將 Assistant 的意圖加入記憶 (必須包含 tool_calls)
                # 將 LiteLLM 的物件轉換為字典格式，避免 Pydantic 序列化警告
                tool_calls_dict = []
                if message.tool_calls:
                    for tc in message.tool_calls:
                        tool_calls_dict.append(
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                            }
                        )

                assistant_msg = {
                    "role": "assistant",
                    "content": message.content,  # 可能為 None
                    "tool_calls": tool_calls_dict,
                }
                # 直接 append 到 memory 的 short_term list 中 (繞過 add 方法的簡單字串處理)
                self.memory.short_term.append(assistant_msg)

                # 執行工具
                tool_results = await self._execute_tool_calls(message.tool_calls)

                # 將工具執行結果加入記憶
                for res in tool_results:
                    self.memory.short_term.append(res)

                # 繼續下一次迴圈 (將工具結果送回 LLM 產生最終回應)

            except Exception as e:
                error_msg = f"LLM 發生錯誤: {str(e)}"
                self.memory.add("system", error_msg)
                return error_msg

        return "達到最大工具呼叫次數限制。"
