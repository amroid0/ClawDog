import asyncio
from typing import Optional
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markdown import Markdown
import typer
from core.agent import Agent
from core.agent_loader import AgentLoader
from utils.config import Config


class ChatLoop:
    def __init__(self, config: Config, agent_id: Optional[str]):
        self.config = config
        self.console = Console()
        loader = AgentLoader(config)
        self.agent_id = agent_id or config.default_agent
        self.agent_def = loader.load(self.agent_id)
        self.agent = Agent(self.agent_def, self.config)
        self.session = self.agent.new_session()

    def get_user_iput(self) -> str:
        return Prompt.ask(Text("You", style="cyan"), console=self.console).strip()

    def show_agent_result(self, result: str):
        self.console.print(Text(self.agent_id), end="")
        md = Markdown(result)
        self.console.print(md)

    async def run(self):
        dog_art = r"""
       __
      /  \__
     (    @ \___
     /         O
    /   (_____/
   /_____/   U
  
   "Woof! Ready to code!"
    """
        self.console.print(
            Panel(
                Group(
                Text("welome to your loyal AI Assistants", style="bold cyan"),
                Text(dog_art)
                ),
                title="chat",
                border_style="cyan",
            )
        )
        self.console.print("Type 'quit' or 'exit' to end the session.\n")
        try:
            while True:
                user_input = await asyncio.to_thread(self.get_user_iput)
                if user_input.lower() in ["quit", "exit", "q"]:
                    self.console.print(Text("goodbye", style="yellow"))
                    break
                if not user_input:
                    continue
                try:
                    result = await self.session.chat(user_input)
                    self.show_agent_result(result=result)
                except Exception as e:
                    self.console.print(f"\n[bold red]Error:[/bold red] {e}\n")

        except (KeyboardInterrupt, EOFError):
            self.console.print(Text("goodbye", style="yellow"))


def chat_command(context: typer.Context, agent_id: str | None = None):
    config = context.obj.get("config")
    chat_loop = ChatLoop(config, agent_id)
    asyncio.run(chat_loop.run())
