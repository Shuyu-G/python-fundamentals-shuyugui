from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Dict, Sequence
import json

from pydantic import BaseModel, ValidationError


class Document(BaseModel):
    id: int
    title: str
    tags: Optional[List[str]] = None
    published: Optional[bool] = None
    metadata: Optional[Dict[str, int]] = None  


def load_documents(path: str | Path) -> List[Document]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise ValueError("documents.json must contain a JSON array")

    docs: List[Document] = []
    for i, item in enumerate(raw):
        try:
            docs.append(Document(**item))
        except ValidationError as e:
            # 带定位信息的错误，便于调试数据问题
            raise ValueError(f"Invalid document at index {i}: {e}") from e
    return docs


def display_documents(docs: Sequence[Document]) -> None:
    for d in docs:
        print(f"ID={d.id} | Title={d.title}")
        print(f"  Tags: {d.tags if d.tags is not None else 'N/A'}")
        print(f"  Published: {d.published if d.published is not None else 'N/A'}")
        print(f"  Metadata: {d.metadata if d.metadata is not None else 'N/A'}")
        print("-" * 40)


def main() -> None:
    default_path = Path("data") / "documents.json"
    docs = load_documents(default_path)
    display_documents(docs)


if __name__ == "__main__":
    docs = load_documents("data/documents.json")
    display_documents(docs)
