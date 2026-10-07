"""Optional order lookup restricted to the supplied customer ID."""

from __future__ import annotations

import json
from pathlib import Path

from data.product_repository import PROJECT_ROOT


class OrderRepository:
    def __init__(self, path: str | Path | None = None):
        source = Path(path) if path else PROJECT_ROOT / "data" / "orders.json"
        self.orders = json.loads(source.read_text(encoding="utf-8"))

    def find_order(self, order_id: str, customer_id: str) -> dict | None:
        return next(
            (
                order
                for order in self.orders
                if order["order_id"].upper() == order_id.upper()
                and order["customer_id"].upper() == customer_id.upper()
            ),
            None,
        )
