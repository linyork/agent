import json
import os
from typing import Any, Dict, List


class Memory:
    """
    記憶系統
    負責管理 Agent 的短期與長期記憶
    """

    def __init__(self, storage_path: str = "memory.json"):
        """
        初始化記憶系統

        Args:
            storage_path (str): 長期記憶儲存檔案路徑
        """
        self.short_term: List[Dict[str, Any]] = []
        self.storage_path = storage_path
        self._load_long_term()

    def add(self, role: str, content: str):
        """
        新增一筆記憶

        Args:
            role (str): 角色 (user, assistant, system)
            content (str): 內容
        """
        message = {"role": role, "content": content}
        self.short_term.append(message)

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        取得當前對話的所有訊息 (用於 Context Window)

        Returns:
            List[Dict[str, Any]]: 訊息列表
        """
        return self.short_term

    def clear_short_term(self):
        """
        清空短期記憶
        """
        self.short_term = []

    def _load_long_term(self):
        """
        載入長期記憶 (從檔案)
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    _ = json.load(f)
            except Exception as e:
                print(f"載入長期記憶失敗: {e}")

    def save_long_term(self):
        """
        儲存長期記憶 (到檔案)
        """
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.short_term, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存長期記憶失敗: {e}")
