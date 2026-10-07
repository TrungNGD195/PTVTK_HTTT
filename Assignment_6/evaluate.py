"""Run a small, explicit Top-1 evaluation and save submission evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from main import ROOT, build_services, run_demo


def main() -> None:
    queries, speech, search = build_services()
    black_image = ROOT / "data/query_images/query_black_running_shoe.png"
    red_image = ROOT / "data/query_images/query_red_backpack.png"
    cases = [
        ("black running shoes", "text", queries.text_query("black running shoes"), 1),
        ("red backpack", "text", queries.text_query("red backpack"), 6),
        ("Nike shoes under 100 dollars", "text", queries.text_query("Nike shoes under 100 dollars"), 1),
        ("blue cotton t-shirt", "text", queries.text_query("blue cotton t-shirt"), 7),
        ("find white sneakers", "voice", queries.voice_query(speech.transcribe("find white sneakers")), 2),
        ("find black headphones", "voice", queries.voice_query(speech.transcribe("find black headphones")), 10),
        ("find brown leather watch", "voice", queries.voice_query(speech.transcribe("find brown leather watch")), 11),
        ("red backpack query illustration", "image", queries.image_query(red_image), 6),
        ("black shoe query illustration", "image", queries.image_query(black_image), 1),
        ("black running shoes + black shoe image", "multimodal",
         queries.multimodal_query("black running shoes", black_image), 1),
        ("red backpack + red backpack image", "multimodal",
         queries.multimodal_query("red backpack", red_image), 6),
        # Intentionally probes a known limitation: no semantic synonym model.
        ("footwear for jogging", "text", queries.text_query("footwear for jogging"), 1),
    ]
    rows = []
    for label, mode, query, expected in cases:
        result = search.search(query, limit=1)
        top = result["results"][0] if result["results"] else None
        actual = top["product"]["id"] if top else None
        rows.append({
            "query": label,
            "mode": mode,
            "expected_top1_id": expected,
            "actual_top1_id": actual,
            "actual_top1_name": top["product"]["name"] if top else "No result",
            "ranking_score": top["score"] if top else "",
            "success": actual == expected,
        })
    order = search.search_order(queries.order_query("O001"), "C001")
    rows.append({
        "query": "order O001 for customer C001",
        "mode": "order",
        "expected_top1_id": "O001",
        "actual_top1_id": order["order_id"] if order else None,
        "actual_top1_name": order["status"] if order else "No result",
        "ranking_score": "N/A",
        "success": bool(order and order["order_id"] == "O001"),
    })
    count = len(rows)
    successes = sum(row["success"] for row in rows)
    summary = {
        "number_of_queries": count,
        "successful_queries": successes,
        "success_rate_percent": round(100 * successes / count, 2),
        "criterion": "Top-1 product ID equals predefined expected ID; order ID matches for order lookup",
        "incorrect_results": [row for row in rows if not row["success"]],
        "results": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "evaluation.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
    with (out / "evaluation.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (out / "demo_results.txt").write_text(run_demo() + "\n", encoding="utf-8")
    print(f"Evaluation: {successes}/{count} successes = {summary['success_rate_percent']:.2f}%")
    for failed in summary["incorrect_results"]:
        print(f"Incorrect: {failed['query']} -> {failed['actual_top1_name']}")
    print("Saved results/evaluation.csv, results/evaluation.json, results/demo_results.txt")


if __name__ == "__main__":
    main()
