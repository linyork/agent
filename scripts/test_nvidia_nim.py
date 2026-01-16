
import os
import sys
from dotenv import load_dotenv

# 加載專案根目錄的 .env 檔案
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from litellm import completion

def test_nvidia():
    """
    測試使用 NVIDIA NIM API (透過 LiteLLM)
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key:
        print("❌ 錯誤: 未在 .env 檔案中找到 'NVIDIA_API_KEY'")
        print("請確認您已將 API Key 加入 .env 檔案中，格式如下：")
        print("NVIDIA_API_KEY=nvapi-...")
        return

    print("🚀 開始測試 NVIDIA NIM API (Meta Llama 3.1 405B)...")
    
    try:
        # 使用 openai 格式呼叫，但指向 NVIDIA 的 base_url
        response = completion(
            model="openai/meta/llama-3.1-405b-instruct", 
            api_key=api_key,
            api_base="https://integrate.api.nvidia.com/v1",
            messages=[{"role": "user", "content": "你好！請用繁體中文簡介一下你自己。"}],
            max_tokens=1024
        )
        
        print("\n✅ 測試成功！收到回應：")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)
        
    except Exception as e:
        print(f"\n❌ 操作失敗: {e}")
        print("\n除錯建議：")
        print("1. 確認 .env 中的 NVIDIA_API_KEY 是否正確")
        print("2. 確認網路連線正常")
        print("3. 確認模型名稱是否正確 (參考 build.nvidia.com)")

if __name__ == "__main__":
    test_nvidia()
