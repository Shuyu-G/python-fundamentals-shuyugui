from __future__ import annotations

from typing import List

import pymupdf4llm
from mongoengine import DoesNotExist
from sqlalchemy import select

from models.relational import Author as SqlAuthor
from models.relational import ScientificArticle as SqlArticle
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from storage.mariadb_engine import SessionLocal
import storage.mongo_engine  # noqa: F401  # ensure MongoDB connection is initialized


def _export_one_article(sql_article: SqlArticle) -> MongoArticle | None:
    """Export a single SQLAlchemy article row into MongoDB."""
    # Build embedded author document
    sql_author: SqlAuthor = sql_article.author
    m_author = MongoAuthor(
        db_id=sql_author.id,
        full_name=sql_author.full_name,
        title=sql_author.title,
    )

    # Extract PDF text as Markdown (best effort)
    md_text = ""
    try:
        md_text = pymupdf4llm.to_markdown(sql_article.file_path)
    except Exception as exc:  # pragma: no cover - best effort
        print(f"⚠️  Failed to extract PDF for {sql_article.arxiv_id}: {exc}")

    # Upsert into MongoDB by arxiv_id
    try:
        doc = MongoArticle.objects.get(arxiv_id=sql_article.arxiv_id)
        # Update existing document
        doc.db_id = sql_article.id
        doc.title = sql_article.title
        doc.summary = sql_article.summary
        doc.file_path = sql_article.file_path
        doc.created_at = sql_article.created_at
        doc.author = m_author
        doc.text = md_text
        doc.save()
        return doc
    except DoesNotExist:
        # Create new document
        doc = MongoArticle(
            db_id=sql_article.id,
            title=sql_article.title,
            summary=sql_article.summary,
            file_path=sql_article.file_path,
            created_at=sql_article.created_at,
            arxiv_id=sql_article.arxiv_id,
            author=m_author,
            text=md_text,
        )
        doc.save()
        return doc


def export_articles_to_mongo(
    sql_articles: List[SqlArticle] | None = None,
) -> List[MongoArticle]:
    """
    Export articles from MariaDB (SQLAlchemy models) into MongoDB documents.

    If `sql_articles` is None, all articles from the database are exported.
    """
    mongo_articles: List[MongoArticle] = []

    with SessionLocal() as session:
        # If caller did not pass any list, load all from DB
        if sql_articles is None:
            stmt = select(SqlArticle)
            sql_articles = list(session.scalars(stmt).all())

        for art in sql_articles:
            print(f"Exporting article {art.arxiv_id}...")
            doc = _export_one_article(art)
            if doc is not None:
                mongo_articles.append(doc)

    print(f"Exported {len(mongo_articles)} articles to MongoDB.")
    return mongo_articles


if __name__ == "__main__":
    # Manual test: export all existing SQL articles to MongoDB
    exported = export_articles_to_mongo()
    print(f"Manually exported {len(exported)} article(s) to MongoDB.")
