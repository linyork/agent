from typing import Any, Dict

from duckduckgo_search import DDGS

from agent.tool_interface import BaseTool


class SearchTool(BaseTool):
    """
    網路搜尋工具 (使用 DuckDuckGo)
    """

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "搜尋網際網路上的資訊。參數: query (搜尋關鍵字)"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "搜尋關鍵字"}},
            "required": ["query"],
        }

    async def execute(self, query: str) -> str:
        try:
            results = DDGS().text(query, max_results=3)

            if not results:
                return "未找到相關搜尋結果。"

            formatted_results = []
            for i, r in enumerate(results, 1):
                title = r.get("title")
                href = r.get("href")
                body = r.get("body")
                formatted_results.append(
                    f"結果 {i}:\n標題: {title}\n連結: {href}\n摘要: {body}\n"
                )

            return "\n".join(formatted_results)
        except Exception as e:
            return f"搜尋時發生錯誤: {e}"
