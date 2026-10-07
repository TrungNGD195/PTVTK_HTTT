"""Entry point for the three-layer multimodal e-commerce search prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

from application.image_service import ImageService
from application.query_service import QueryService
from application.ranking_service import RankingService
from application.search_service import SearchService
from application.speech_service import SpeechService
from data.order_repository import OrderRepository
from data.product_repository import ProductRepository
from data.vector_index import VectorIndex
from presentation.search_ui import SearchUI


ROOT = Path(__file__).resolve().parent


def build_services() -> tuple[QueryService, SpeechService, SearchService]:
    repository = ProductRepository()
    image_service = ImageService()
    vectors = {product["id"]: image_service.encode(ROOT / product["image"])
               for product in repository.all_products()}
    return (
        QueryService(),
        SpeechService(),
        SearchService(repository, VectorIndex(vectors),
                      image_service, RankingService(), OrderRepository()),
    )


def run_demo() -> str:
    ui = SearchUI(*build_services())
    examples = [
        ("TEXT SEARCH", ui.search_text("black running shoes", limit=3)),
        ("VOICE SEARCH (SIMULATED)", ui.search_voice("find white sneakers", limit=3)),
        ("IMAGE SEARCH", ui.search_image(str(ROOT / "data/query_images/query_red_backpack.png"), limit=3)),
        ("MULTIMODAL SEARCH", ui.search_multimodal(
            "black running shoes", str(ROOT / "data/query_images/query_black_running_shoe.png"), limit=3)),
    ]
    sections = ["=== E-COMMERCE MULTIMODAL SEARCH DEMO ==="]
    for title, response in examples:
        sections.append(f"\n--- {title} ---\n{ui.display(response)}")
    order = ui.search_order("O001", "C001")
    sections.append("\n--- OPTIONAL ORDER LOOKUP ---\n"
                    f"Input: order=O001, customer=C001\n"
                    f"Result: {order['order_id']} | {order['status']} | ${order['total']}")
    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("demo", help="run the assignment demonstration")
    for mode in ("text", "voice", "image"):
        command = sub.add_parser(mode)
        command.add_argument("input", help="query text, transcript text, or image path")
    both = sub.add_parser("multimodal")
    both.add_argument("text")
    both.add_argument("image")
    order = sub.add_parser("order")
    order.add_argument("order_id")
    order.add_argument("customer_id")
    arguments = parser.parse_args()

    if arguments.mode == "demo":
        print(run_demo())
        return
    ui = SearchUI(*build_services())
    if arguments.mode == "text":
        response = ui.search_text(arguments.input)
    elif arguments.mode == "voice":
        response = ui.search_voice(arguments.input)
    elif arguments.mode == "image":
        response = ui.search_image(arguments.input)
    elif arguments.mode == "multimodal":
        response = ui.search_multimodal(arguments.text, arguments.image)
    else:
        result = ui.search_order(arguments.order_id, arguments.customer_id)
        print(result if result else "Order not found for this customer.")
        return
    print(ui.display(response))


if __name__ == "__main__":
    main()
