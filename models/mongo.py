from __future__ import annotations

from datetime import datetime

from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    DateTimeField,
    EmbeddedDocumentField,
)


class Author(EmbeddedDocument):
    db_id: int = IntField(required=True)
    full_name: str = StringField()
    title: str = StringField()


class ScientificArticle(Document):
    meta = {
        "collection": "articles",
        "indexes": [
            "db_id",
            "arxiv_id",
            {
                "fields": ["$text"],
                "default_language": "english",
            },
        ],
    }

    db_id: int = IntField(required=True)
    title: str = StringField()
    summary: str = StringField()
    file_path: str = StringField()
    created_at: datetime = DateTimeField()
    arxiv_id: str = StringField()
    author: Author = EmbeddedDocumentField(Author)
    text: str = StringField()
