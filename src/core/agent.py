from dataclasses import field
from typing import Optional

from attr import dataclass
from core.agent_loader import AgentDef
from core.session_state import SessionState
from provider.llm.base import LLMProvider
from utils.config import Config
import uuid
from datetime import datetime
from litellm.types.completion import ChatCompletionMessageParam as Message


class Agent:
    def __init__(self, agent_def: AgentDef, config: Config) -> None:

        self.agent_def = agent_def
        self.config = config
        self.llm = LLMProvider.from_config(agent_def.llm)

    def new_session(self, session_id: Optional[str]= None) -> "AgentSession":

        new_session_id = session_id or str(uuid.uuid4)
        state = SessionState(
            session_id=new_session_id,
            system_prompt=self.agent_def.system_prompt,
            messages=[],
        )
        return AgentSession(
            agent=self,
            state=state
        )

@dataclass
class AgentSession:
    agent: Agent
    state: SessionState
    started_at: datetime = field(default_factory=datetime.now)
    @property
    def session_id(self) -> str:
       return  self.state.session_id
    async def chat(self, message: str) -> str:
        user_message:Message = {"role":"user","content":message}
        self.state.addMessage(user_message)
        messages=  self.state.build_messages()
        response =  await self.agent.llm.chat(messages=messages)
        assistant_msg: Message = {"role": "assistant", "content": response}
        self.state.addMessage(assistant_msg)
        return response