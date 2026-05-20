from math import fabs
from operator import truediv
from pathlib import Path
from typing import Any, Callable, List, Optional, TypeVar
import logging
import yaml


T = TypeVar("T")
logger = logging.getLogger(__name__)


class DefNotFound(Exception):
    def __init__(self, kind: str, def_id:str) -> None:
        super().__init__(f"{kind.capitalize} not found:{def_id}")


class DefNotInvalid(Exception):
    def __init__(self, kind: str, def_id:str, reason: str) -> None:
        super().__init__(f"Invalid {kind} '{def_id}': {reason}")


def parse_defination(
    content: str, def_id: str, parse_fun: Callable[[str, dict[str, Any], str], T]
) -> T:

    if not content.startswith("---\n"):
        return parse_fun(def_id, {}, content)
    end_delimter = content.find("\n---\n", 4)
    if end_delimter == -1:
        return parse_fun(def_id, {}, content)
    formatted_text = content[4:end_delimter]
    body = content[end_delimter + 5 :]
    raw_dict = yaml.safe_load(formatted_text)
    return parse_fun(def_id, raw_dict, body)


def discover_definations(
    path: Path,
    file_name: str,
    parse_fun: Callable[[str, dict[str, Any], str], Optional[T]],
) -> list[T]:
    if not path.exists():
        logger.warning("path not found")
        return []
    results = []
    for def_dir in path.iterdir():
        if not def_dir.is_dir():
            continue
        def_file = def_dir / file_name

        if not def_file.exists():
            continue
        try:
            content = def_file.read_text()
            result = parse_defination(content, def_dir.name, parse_fun)
            if result is not None:
                results.append(result)

        except Exception as e:
            logger.warning("defination parsing error")
            continue
    return results


def write_defination(
    def_id: str, formatter: dict[str, Any], body: str, path: Path, file_name: str
) -> Path:
    def_dir = path / def_id
    def_dir.mkdir(parents=True, exist_ok=True)
    yaml_conent = yaml.dump(formatter, default_flow_style=False, sort_keys=False)
    content = f"---\n{yaml_conent}---\n\n{body.strip()}\n"
    def_file = def_dir / file_name
    def_file.write_text(content)
    return def_file
