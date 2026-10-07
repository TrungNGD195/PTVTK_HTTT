"""Print user-facing input, processing steps, products, and ranking scores."""

from __future__ import annotations

from pathlib import Path

from application.query_service import QueryService
from application.search_service import SearchService
from application.speech_service import SpeechService


class SearchUI:
    @staticmethod
    def _display_path(path: str) -> str:
        resolved = Path(path).resolve()
        try:
            return str(resolved.relative_to(Path(__file__).resolve().parents[1]))
        except ValueError:
            return str(path)

    def __init__(self, queries: QueryService, speech: SpeechService, search: SearchService):
        self.queries = queries
        self.speech = speech
        self.search_service = search

    def search_text(self, text: str, limit: int = 5) -> dict:
        return self.search_service.search(self.queries.text_query(text), limit)

    def search_voice(self, transcript_input: str, limit: int = 5) -> dict:
        text = self.speech.transcribe(transcript_input)
        return self.search_service.search(self.queries.voice_query(text), limit)

    def search_image(self, image_path: str, limit: int = 5) -> dict:
        return self.search_service.search(self.queries.image_query(image_path), limit)

    def search_multimodal(self, text: str, image_path: str, limit: int = 5) -> dict:
        return self.search_service.search(self.queries.multimodal_query(text, image_path), limit)

    def search_order(self, order_id: str, customer_id: str) -> dict | None:
        return self.search_service.search_order(self.queries.order_query(order_id), customer_id)

    @staticmethod
    def display(response: dict) -> str:
        query = response["query"]
        mode = query["type"]
        if mode == "multimodal":
            value = f"text={query['query']!r}; image={SearchUI._display_path(query['image_path'])}"
        elif mode == "image":
            value = SearchUI._display_path(query["image_path"])
        else:
            value = query.get("query", query.get("image_path", ""))
        lines = [f"Mode: {mode}", f"Input: {value}", f"Processing: {response['processing']}",
                 f"Retrieved candidates: {response['candidate_count']}"]
        if not response["results"]:
            lines.append("No matching products.")
        for rank, result in enumerate(response["results"], start=1):
            product = result["product"]
            lines.append(
                f"{rank}. [{product['id']:02d}] {product['name']} | score={result['score']:.4f} "
                f"(text={result['text_score']:.4f}, image={result['image_score']:.4f}, "
                f"stock={result['stock_score']:.4f}) | ${product['price']}"
            )
        return "\n".join(lines)
