"""Retrieve product candidates, then delegate their ordering to RankingService."""

from __future__ import annotations

import re
from pathlib import Path

from application.image_service import ImageService
from application.ranking_service import RankingService
from data.order_repository import OrderRepository
from data.product_repository import ProductRepository
from data.vector_index import VectorIndex


STOPWORDS = {
    "a", "an", "and", "by", "dollar", "dollars", "find", "for", "i", "in", "is",
    "me", "my", "of", "product", "products", "search", "show", "some", "the", "to",
    "want", "with", "under", "below", "less", "than", "please", "image",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    # Minimal singular normalization is enough for this controlled dataset.
    return {word[:-1] if word.endswith("s") and len(word) > 3 else word
            for word in words if word not in STOPWORDS and not word.isdigit()}


class SearchService:
    def __init__(
        self,
        repository: ProductRepository,
        vector_index: VectorIndex,
        image_service: ImageService,
        ranking_service: RankingService,
        order_repository: OrderRepository,
    ):
        self.repository = repository
        self.vector_index = vector_index
        self.image_service = image_service
        self.ranking_service = ranking_service
        self.order_repository = order_repository

    def search_order(self, query: dict, customer_id: str) -> dict | None:
        if query["type"] != "order":
            raise ValueError("Expected a normalized order query.")
        return self.order_repository.find_order(query["order_id"], customer_id)

    @staticmethod
    def _price_ceiling(query_text: str) -> float | None:
        match = re.search(r"(?:under|below|less than)\s*\$?\s*(\d+(?:\.\d+)?)", query_text, re.I)
        return float(match.group(1)) if match else None

    def _text_candidates(self, text: str) -> list[dict]:
        query_tokens = _tokens(text)
        price_ceiling = self._price_ceiling(text)
        if not query_tokens:
            return []
        candidates = []
        for product in self.repository.all_products():
            if price_ceiling is not None and product["price"] >= price_ceiling:
                continue
            title_tokens = _tokens(" ".join([product["name"], product["brand"], product["color"]]))
            other_tokens = _tokens(" ".join([product["category"], product["description"]]))
            numerator = sum(2 if token in title_tokens else 1 if token in other_tokens else 0
                            for token in query_tokens)
            if query_tokens & _tokens(product["category"]):
                numerator += 0.5
            if numerator:
                candidates.append({"product": product,
                                   "text_score": min(1.0, numerator / (2 * len(query_tokens)))})
        return candidates

    def _image_candidates(self, image_path: str | Path) -> list[dict]:
        vector = self.image_service.encode(image_path)
        return [
            {"product": self.repository.get(product_id), "image_score": max(0.0, similarity)}
            for product_id, similarity in self.vector_index.search(vector, limit=10)
        ]

    def search(self, query: dict, limit: int = 5) -> dict:
        mode = query["type"]
        if mode in ("text", "voice"):
            candidates = self._text_candidates(query["query"])
            processing = "normalize words -> retrieve keyword matches -> rank with stock signal"
        elif mode == "image":
            candidates = self._image_candidates(query["image_path"])
            processing = "read image -> extract visual vector -> cosine retrieval -> rank with stock signal"
        elif mode == "multimodal":
            text_candidates = self._text_candidates(query["query"])
            image_candidates = self._image_candidates(query["image_path"])
            merged = {item["product"]["id"]: dict(item) for item in image_candidates}
            for item in text_candidates:
                product_id = item["product"]["id"]
                merged.setdefault(product_id, {"product": item["product"]}).update(
                    text_score=item["text_score"]
                )
            candidates = list(merged.values())
            processing = "retrieve text and image candidates -> merge by product ID -> weighted ranking"
        else:
            raise ValueError(f"Unsupported product query type: {mode}")
        return {
            "query": query,
            "processing": processing,
            "candidate_count": len(candidates),
            "results": self.ranking_service.rank(candidates, mode, limit),
        }
