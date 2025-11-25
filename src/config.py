import yaml
from dataclasses import dataclass

@dataclass
class LLMConfig:
    model: str
    temperature: float
    max_tokens: int
    language: str

@dataclass
class AppConfig:
    max_articles_per_day: int
    llm: LLMConfig

def load_config(path: str = "config/config.yaml") -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    llm_cfg = LLMConfig(
        model=data["llm"]["model"],
        temperature=float(data["llm"]["temperature"]),
        max_tokens=int(data["llm"]["max_tokens"]),
        language=data["llm"]["language"],
    )
    return AppConfig(
        max_articles_per_day=int(data["max_articles_per_day"]),
        llm=llm_cfg,
    )

def load_rss_sources(path: str = "config/sources_rss.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["feeds"]
