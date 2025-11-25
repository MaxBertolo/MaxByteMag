import yaml
from dataclasses import dataclass
from pathlib import Path

# Directory di base del progetto (la root del repo)
BASE_DIR = Path(__file__).resolve().parent.parent


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


def load_config(path: str | None = None) -> AppConfig:
    """
    Carica config.yaml usando un percorso assoluto,
    indipendente dalla cartella da cui viene lanciato Python.
    """
    if path is None:
        config_path = BASE_DIR / "config" / "config.yaml"
    else:
        config_path = (BASE_DIR / path).resolve()

    print("Loading config from:", config_path)  # debug nei log di Actions

    with open(config_path, "r", encoding="utf-8") as f:
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
    """
    Carica sources_rss.yaml usando un percorso assoluto.
    """
    rss_path = (BASE_DIR / path).resolve()
    print("Loading RSS sources from:", rss_path)  # debug

    with open(rss_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["feeds"]
