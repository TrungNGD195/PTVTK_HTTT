"""Order retrieved candidates using distinct relevance and stock signals."""

from __future__ import annotations


class RankingService:
    @staticmethod
    def rank(
        candidates: list[dict], mode: str, limit: int = 5
    ) -> list[dict]:
        ranked = []
        for candidate in candidates:
            product = candidate["product"]
            text_score = candidate.get("text_score", 0.0)
            image_score = candidate.get("image_score", 0.0)
            stock_score = min(product["stock"] / 20, 1.0)
            if mode in ("text", "voice"):
                total = 0.98 * text_score + 0.02 * stock_score
            elif mode == "image":
                total = 0.98 * image_score + 0.02 * stock_score
            elif mode == "multimodal":
                total = 0.49 * text_score + 0.49 * image_score + 0.02 * stock_score
            else:
                raise ValueError(f"Unsupported ranking mode: {mode}")
            ranked.append(
                {
                    "product": product,
                    "score": round(total, 4),
                    "text_score": round(text_score, 4),
                    "image_score": round(image_score, 4),
                    "stock_score": round(stock_score, 4),
                }
            )
        return sorted(ranked, key=lambda x: (-x["score"], x["product"]["id"]))[:limit]
