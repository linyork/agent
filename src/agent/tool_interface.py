from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """
    工具基礎類別 (Abstract Base Class)
    所有工具都必須繼承此類別
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        工具名稱 (例如: 'web_search')
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        工具描述 (用於 LLM 了解如何使用此工具)
        """
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """
        工具參數定義 (JSON Schema 格式)
        """
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """
        執行工具

        Args:
            **kwargs: 工具參數

        Returns:
            Any: 執行結果
        """
        pass
