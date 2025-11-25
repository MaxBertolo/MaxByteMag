import yaml
from dataclasses import dataclass
from pathlib import Path

# BASE_DIR = root del repo (cartella che contiene src/, config/, ecc.)
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


def load_config() -> AppConfig:
    """
    Carica config.yaml usando un percorso assoluto,
    così non dipende da dove viene lanciato Python.
    """
    config_path = BASE_DIR / "config" / "config.yaml"
    print("[DEBUG] Loading config from:", config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")

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


def load_rss_sources() -> list[dict]:
    """
    Carica sources_rss.yaml usando un percorso assoluto.
    """
    rss_path = BASE_DIR / "config" / "sources_rss.yaml"
    print("[DEBUG] Loading RSS sources from:", rss_path)

    if not rss_path.exists():
        raise FileNotFoundError(f"RSS sources file not found at {rss_path}")

    with open(rss_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data["feeds"]
