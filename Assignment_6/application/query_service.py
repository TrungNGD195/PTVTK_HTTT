"""Convert every input modality to a common query dictionary."""

from __future__ import annotations

from pathlib import Path


class QueryService:
    def text_query(self, text: str) -> dict:
        return {"type": "text", "query": text.strip()}

    def voice_query(self, transcript: str) -> dict:
        return {"type": "voice", "query": transcript.strip()}

    def image_query(self, image_path: str | Path) -> dict:
        return {"type": "image", "image_path": str(image_path)}

    def multimodal_query(self, text: str, image_path: str | Path) -> dict:
        return {"type": "multimodal", "query": text.strip(), "image_path": str(image_path)}

    def order_query(self, order_id: str) -> dict:
        return {"type": "order", "order_id": order_id.strip().upper()}
