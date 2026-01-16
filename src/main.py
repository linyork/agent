import os
import warnings

# 隱藏 LiteLLM 與 Gemini API 互動時產生的 Pydantic 序列化警告
# 這些警告源於外部函式庫欄位定義不一，不影響程式功能
warnings.filterwarnings("ignore", message="PydanticSerializationUnexpectedValue")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt

from agent.core import Agent

# 載入環境變數
load_dotenv()

# 初始化 Rich Console 用於美化輸出
console = Console()


async def main():
    """
    主程式進入點
    """
    console.print("[bold green]Agent 系統初始化中...[/bold green]")

    # 初始化 Agent
    # 預設使用 gpt-4o，可以從環境變數讀取
    model = os.getenv("AGENT_MODEL", "gpt-4o")
    agent = Agent(model_name=model)

    console.print(f"[bold blue]系統準備就緒。使用模型: {model}[/bold blue]")
    console.print("[dim]輸入 'exit' 或 'quit' 離開程式[/dim]")

    while True:
        try:
            user_input = Prompt.ask("[bold yellow]User[/bold yellow]")

            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold green]再見！[/bold green]")
                break

            if not user_input.strip():
                continue

            with console.status("[bold green]Agent 思考中...[/bold green]"):
                response = await agent.think(user_input)

            console.print(f"[bold cyan]Agent[/bold cyan]: {response}")

        except KeyboardInterrupt:
            console.print("\n[bold red]程式已由使用者終止。[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]發生未預期的錯誤：{e}[/bold red]")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold green]程式已結束。[/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]程式異常終止：{e}[/bold red]")
