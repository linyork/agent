import os
from typing import Any, Dict

from agent.tool_interface import BaseTool


class FileReadTool(BaseTool):
    """
    檔案讀取工具
    """

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "讀取指定路徑的檔案內容。參數: path (絕對路徑)"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "檔案的絕對路徑"}},
            "required": ["path"],
        }

    async def execute(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                return f"錯誤: 找不到檔案 {path}"

            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"讀取檔案時發生錯誤: {e}"


class FileWriteTool(BaseTool):
    """
    檔案寫入工具
    """

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "寫入內容到指定路徑的檔案 (會覆蓋原有內容)。參數: path (絕對路徑), content (內容)"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "檔案的絕對路徑"},
                "content": {"type": "string", "description": "要寫入的內容"},
            },
            "required": ["path", "content"],
        }

    async def execute(self, path: str, content: str) -> str:
        try:
            # 確保目錄存在
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"成功寫入檔案: {path}"
        except Exception as e:
            return f"寫入檔案時發生錯誤: {e}"
