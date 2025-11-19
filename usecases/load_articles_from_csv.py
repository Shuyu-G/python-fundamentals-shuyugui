from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from sqlalchemy.exc import IntegrityError

from models.relational import Author, ScientificArticle
from storage.mariadb_engine import SessionLocal


def save_article(line: dict[str, str]) -> ScientificArticle | None:
    """Insert one article row from CSV into MariaDB."""
    with SessionLocal() as session:
        try:
            author = Author(
                full_name=line["author_full_name"],
                title=line["author_title"],
            )
            article = ScientificArticle(
                title=line["title"],
                summary=line["summary"],
                file_path=line["file_path"],
                arxiv_id=line["arxiv_id"],
                author=author,
            )
            session.add(article)
            session.commit()
            session.refresh(article)
            print(f"Inserted article {article.arxiv_id}")
            return article
        except IntegrityError as exc:  # duplicate arxiv_id 等
            session.rollback()
            print(f"⚠️ Duplicate or error for {line.get('arxiv_id')}: {exc}")
            return None


def load_data_from_csv(path: str | Path) -> List[ScientificArticle]:
    """Load all rows from CSV into MariaDB, return inserted articles."""
    csv_path = Path(path)
    articles: List[ScientificArticle] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            art = save_article(row)
            if art is not None:
                articles.append(art)

    return articles


if __name__ == "__main__":
    from storage.mariadb_engine import Base, engine

    Base.metadata.create_all(bind=engine)

    new_articles = load_data_from_csv("data/articles.csv")
    print(f"\nImported {len(new_articles)} articles into MariaDB.")
