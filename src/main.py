from pathlib import Path
from datetime import datetime

from .config import load_config, load_rss_sources
from .rss_collector import collect_from_rss
from .cleaning import clean_articles
from .summarizer import summarize_articles
from .report_builder import build_html_report

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def main():
    cfg = load_config()
    feeds = load_rss_sources()

    print("Collecting RSS...")
    raw_articles = collect_from_rss(feeds)
    print(f"Collected {len(raw_articles)} raw articles")

    cleaned = clean_articles(raw_articles, max_articles=cfg.max_articles_per_day)
    print(f"After cleaning: {len(cleaned)} articles")

    if not cleaned:
        print("No recent articles found.")
        return

    print("Summarizing with LLM...")
    summaries = summarize_articles(cleaned, cfg.llm)

    print("Building HTML report...")
    html = build_html_report(summaries, date_str=today_str())

    out_dir = Path("reports/html")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"report_{today_str()}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Done. Report:", out_path)

if __name__ == "__main__":
    main()
