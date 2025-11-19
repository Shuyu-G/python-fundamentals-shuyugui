from __future__ import annotations

from typing import List

from models.mongo import ScientificArticle


def search_text(keyword: str) -> List[ScientificArticle]:
    """Simple substring search without using a full-text index."""
    return list(ScientificArticle.objects(text__icontains=keyword))


def search_text_index(keyword: str) -> List[ScientificArticle]:
    """Full-text search using MongoDB's text index."""
    return list(ScientificArticle.objects.search_text(keyword))


if __name__ == "__main__":
    kw = "quantum"
    results = search_text_index(kw)
    print(f"Text index search for '{kw}', found {len(results)} article(s):")
    for art in results:
        print(f"- {art.arxiv_id}: {art.title}")
