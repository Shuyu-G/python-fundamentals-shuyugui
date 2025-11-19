from __future__ import annotations

from pathlib import Path

from models.relational import ScientificArticle as SqlArticle
from models.mongo import ScientificArticle as MongoArticle
import storage.mongo_engine  # noqa: F401
from usecases.load_articles_from_csv import load_data_from_csv
from usecases.export_articles_to_mongo import export_articles_to_mongo
from usecases.search_articles import search_text_index


def run_pipeline() -> None:
    csv_path = Path("data/articles.csv")

    sql_articles: list[SqlArticle] = load_data_from_csv(csv_path)
    print(f"[STEP 1] Loaded {len(sql_articles)} articles into MariaDB.")

    mongo_articles: list[MongoArticle] = export_articles_to_mongo(sql_articles)
    print(f"[STEP 2] Exported {len(mongo_articles)} articles to MongoDB.")

    keyword = "robotic"
    results = search_text_index(keyword)
    print(
        f"[STEP 3] Text index search for '{keyword}', found {len(results)} article(s):"
    )
    for art in results:
        print(f"- {art.arxiv_id}: {art.title}")


if __name__ == "__main__":
    run_pipeline()
