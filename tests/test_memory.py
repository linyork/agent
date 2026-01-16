"""
記憶系統的測試
"""

import os
import tempfile

from agent.memory import Memory


def test_memory_initialization():
    """
    測試記憶系統初始化
    """
    memory = Memory()

    # 短期記憶應該是空的
    assert len(memory.short_term) == 0


def test_memory_add_and_get():
    """
    測試新增與取得記憶
    """
    memory = Memory()

    # 新增訊息
    memory.add("user", "你好")
    memory.add("assistant", "您好！有什麼可以幫您的嗎？")

    # 取得訊息
    messages = memory.get_messages()

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "你好"
    assert messages[1]["role"] == "assistant"


def test_memory_clear():
    """
    測試清空短期記憶
    """
    memory = Memory()

    memory.add("user", "測試")
    memory.add("assistant", "收到")

    assert len(memory.short_term) == 2

    memory.clear_short_term()

    assert len(memory.short_term) == 0


def test_memory_save_and_load():
    """
    測試儲存與載入長期記憶
    """
    # 使用臨時檔案
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    try:
        # 建立記憶並儲存
        memory1 = Memory(storage_path=temp_path)
        memory1.add("user", "記住這個")
        memory1.save_long_term()

        # 驗證檔案存在
        assert os.path.exists(temp_path)

    finally:
        # 清理
        if os.path.exists(temp_path):
            os.unlink(temp_path)
