from pathlib import Path
from datetime import datetime

from .rss_collector import collect_from_rss
from .cleaning import clean_articles
from .summarizer import summarize_articles
from .report_builder import build_html_report
from .pdf_export import html_to_pdf

from dataclasses import dataclass

# --- CONFIG HARDCODATA QUI ---

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


def get_config() -> AppConfig:
    # equivalente del tuo config.yaml
    return AppConfig(
        max_articles_per_day=10,
        llm=LLMConfig(
            model="gpt-4.1-mini",
            temperature=0.3,
            max_tokens=600,
            language="it",
        ),
    )


def get_rss_sources() -> list[dict]:
    # equivalente del tuo sources_rss.yaml
    return [
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml",
        },
    ]
# --- FINE CONFIG HARDCODATA ---


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def main():
    cfg = get_config()
    feeds = get_rss_sources()


    print("Collecting RSS...")
    raw_articles = collect_from_rss(feeds)
    print(f"Collected {len(raw_articles)} raw articles")

    cleaned = clean_articles(raw_articles, max_articles=cfg.max_articles_per_day)
    print(f"After cleaning: {len(cleaned)} articles")

    if not cleaned:
        print("No recent articles found. Exiting.")
        return

    print("Summarizing with LLM...")
    summaries = summarize_articles(cleaned, cfg.llm)

    print("Building HTML report...")
    date_str = today_str()
    html = build_html_report(summaries, date_str=date_str)

    # Salva HTML
    html_dir = Path("reports/html")
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / f"report_{date_str}.html"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML report saved at:", html_path)

    # Genera PDF
    pdf_dir = Path("reports/pdf")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = pdf_dir / f"report_{date_str}.pdf"

    print("Converting HTML to PDF...")
    html_to_pdf(html, str(pdf_path))
    print("PDF report saved at:", pdf_path)


if __name__ == "__main__":
    main()
