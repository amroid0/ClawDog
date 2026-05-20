from typing import Any, Optional
from pydantic import BaseModel
from utils.config import Config, LLMConfig
from utils.def_loader import DefNotFound, DefNotInvalid, parse_defination


class AgentDef(BaseModel):
    id: str
    name: str
    descreption: str
    system_prompt: str
    llm: LLMConfig


class AgentLoader:
    def __init__(self, config: Config):
        self.config = config

    def load(self, agent_id: str) -> AgentDef:
        agent_file = self.config.agent_path / agent_id / "AGENT.md"
        if not agent_file.exists():
            raise DefNotFound("agent", def_id=agent_id)
        try:
            content = agent_file.read_text()
            agent_def = parse_defination(
                content=content, def_id=agent_id, parse_fun=self.parse_agent_def
            )
        except Exception as e:
            raise DefNotInvalid("agent", agent_id, str(e))
        return agent_def

    def parse_agent_def(
        self, def_id: str, formatter: dict[str, Any], body: str
    ) -> AgentDef:
        agent_llm = formatter.get("llm")
        merged_llm = self.megre_llm_config(agent_llm)
        return AgentDef(
            id=def_id,
            name=formatter.get("name", ""),
            descreption=formatter.get("description", ""),
            system_prompt=body.strip(),
            llm=merged_llm,
        )

    def megre_llm_config(self, agent_llm: Optional[dict[str, Any]]) -> LLMConfig:
        base = self.config.llm.model_dump()
        if agent_llm:
            base = {**base, **agent_llm}
        return LLMConfig(**base)
