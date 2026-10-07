"""Small in-memory vector index built from product image files."""

from __future__ import annotations

import numpy as np


class VectorIndex:
    def __init__(self, vectors: dict[int, np.ndarray]):
        self.vectors = dict(vectors)

    def search(self, query_vector: np.ndarray, limit: int = 10) -> list[tuple[int, float]]:
        scores = [
            (product_id, float(np.dot(query_vector, vector)))
            for product_id, vector in self.vectors.items()
        ]
        return sorted(scores, key=lambda item: (-item[1], item[0]))[:limit]
