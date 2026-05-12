from pathlib import Path
from pydantic import BaseModel, Field, field_validator, model_validator
import yaml


class LLMConfig(BaseModel):
    provider: str
    model: str
    api_base_url: str
    api_key: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=0)

    @field_validator("api_base_url")
    @classmethod
    def vailate_api_base_url(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith(("https://", "http://")):
            raise ValueError("wrong base api uri ")
        return value


class Config(BaseModel):
    workspace: Path
    default_agent: str
    agent_path: Path = Field(default=Path("agents"))
    llm: LLMConfig

    @model_validator(mode="after")
    def resolve_path(self) -> "Config":
        if self.agent_path and not self.agent_path.is_absolute():
            self.agent_path = self.workspace / self.agent_path
        return self

    @classmethod
    def load(cls, workspacePath: Path, config_file: Path) -> "Config":
        config_data = {}
        if config_file.exists():
            with open(config_file) as f:
                config_data = yaml.safe_load(f) or {}
        config_data["workspace"] = workspacePath
        return cls.model_validate(config_data)
