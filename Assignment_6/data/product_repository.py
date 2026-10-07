"""JSON-backed product repository."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ProductRepository:
    def __init__(self, path: str | Path | None = None):
        source = Path(path) if path else PROJECT_ROOT / "data" / "products.json"
        self.products = json.loads(source.read_text(encoding="utf-8"))
        self._by_id = {item["id"]: item for item in self.products}
        if len(self._by_id) != len(self.products):
            raise ValueError("Product IDs must be unique.")

    def all_products(self) -> list[dict]:
        return list(self.products)

    def get(self, product_id: int) -> dict | None:
        return self._by_id.get(product_id)
