import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

from deepler.constants import DEFAULT_CONFIG_FILE_NAME, DEFAULT_COUNTS_FILE_NAME


@dataclass
class Config:
    ignores: list[str] = field(default_factory=list)
    hist_file: str = DEFAULT_COUNTS_FILE_NAME
    min_length: int = 4
    source_lang: str = "EN"
    target_lang: str = "JA"
    count_lang: str = "EN"

    @classmethod
    def load(cls, config_file: str = DEFAULT_CONFIG_FILE_NAME) -> "Config":
        if not config_file:
            config_file = DEFAULT_CONFIG_FILE_NAME

        config_path = Path(config_file).expanduser()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return cls(**config)
        except FileNotFoundError:
            return cls()

    def save(self, config_file: str = DEFAULT_CONFIG_FILE_NAME) -> None:
        if not config_file:
            config_file = DEFAULT_CONFIG_FILE_NAME

        config_path = Path(config_file).expanduser()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            f.write(self.dump())

    def to_json(self) -> dict:
        return asdict(self)

    def dump(self) -> str:
        return json.dumps(self.to_json(), ensure_ascii=False, indent=2)


def update(
    config_file: str,
    ignore_add: Iterable[str],
    ignore_delete: Iterable[str],
    min_length: Optional[int],
    source_lang: Optional[str],
    target_lang: Optional[str],
    count_lang: Optional[str],
) -> Config:
    config = Config.load(config_file)
    config.ignores = list((set(config.ignores) | set(ignore_add)) - set(ignore_delete))
    if min_length is not None:
        config.min_length = min_length
    if source_lang is not None:
        config.source_lang = source_lang
    if target_lang is not None:
        config.target_lang = target_lang
    if count_lang is not None:
        config.count_lang = count_lang

    config.save(config_file)
    return config
