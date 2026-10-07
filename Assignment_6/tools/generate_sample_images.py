"""Create original, simple product illustrations for the sample dataset.

These are classroom demonstration images, not photographs or licensed assets.
Run from anywhere: python tools/generate_sample_images.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "images"
QUERIES = ROOT / "data" / "query_images"


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (480, 360), "white")
    return image, ImageDraw.Draw(image)


def shoe(color: str, accent: str, variant: bool = False) -> Image.Image:
    image, draw = canvas()
    draw.ellipse((83, 290, 400, 320), fill="#ececec")
    offset = 8 if variant else 0
    draw.polygon([(74, 227), (116, 196), (218, 168 + offset), (276, 197),
                  (327, 228), (387, 241), (413, 268), (391, 286), (95, 286)],
                 fill=color, outline="#444444", width=4)
    draw.polygon([(86, 275), (397, 275), (405, 288), (390, 297), (97, 297)],
                 fill="#dddddd", outline="#666666", width=3)
    draw.polygon([(198, 179 + offset), (233, 188), (211, 230), (160, 226)],
                 fill=accent, outline="#777777", width=2)
    for index in range(4):
        x = 221 + index * 19
        y = 203 + index * 6
        draw.line((x, y, x + 25, y + 17), fill="#fafafa", width=5)
    draw.line((301, 229, 356, 246), fill=accent, width=8)
    return image


def backpack(color: str, accent: str, variant: bool = False) -> Image.Image:
    image, draw = canvas()
    draw.ellipse((130, 302, 352, 324), fill="#ececec")
    draw.rounded_rectangle((141, 92, 339, 299), radius=45, fill=color,
                           outline="#333333", width=5)
    draw.arc((201, 63, 278, 120), 180, 360, fill="#444444", width=12)
    draw.arc((110, 105, 195, 303), 70, 280, fill="#555555", width=15)
    draw.arc((287, 105, 370, 303), 260, 110, fill="#555555", width=15)
    pocket_top = 198 if variant else 207
    draw.rounded_rectangle((174, pocket_top, 307, 277), radius=18, fill=accent,
                           outline="#333333", width=4)
    draw.line((192, pocket_top + 15, 290, pocket_top + 15), fill="#dddddd", width=5)
    draw.line((182, 148, 296, 148), fill="#eeeeee", width=4)
    return image


def shirt(color: str, accent: str) -> Image.Image:
    image, draw = canvas()
    draw.ellipse((112, 309, 372, 329), fill="#eeeeee")
    draw.polygon([(176, 86), (211, 72), (269, 72), (304, 86), (371, 145),
                  (335, 194), (307, 175), (307, 294), (173, 294), (173, 175),
                  (145, 194), (109, 145)], fill=color)
    draw.line((176, 86, 109, 145, 145, 194, 173, 175, 173, 294, 307, 294,
               307, 175, 335, 194, 371, 145, 304, 86), fill="#444444", width=4)
    draw.arc((208, 63, 273, 113), 0, 180, fill=accent, width=7)
    draw.line((182, 202, 298, 202), fill=accent, width=5)
    return image


def headphones(color: str, accent: str) -> Image.Image:
    image, draw = canvas()
    draw.ellipse((108, 303, 374, 324), fill="#eeeeee")
    draw.arc((121, 60, 359, 303), 187, 353, fill=color, width=32)
    draw.arc((134, 75, 346, 280), 190, 350, fill=accent, width=7)
    draw.rounded_rectangle((115, 177, 169, 287), radius=21, fill=color,
                           outline="#333333", width=5)
    draw.rounded_rectangle((311, 177, 365, 287), radius=21, fill=color,
                           outline="#333333", width=5)
    draw.rounded_rectangle((130, 197, 166, 274), radius=13, fill=accent)
    draw.rounded_rectangle((314, 197, 350, 274), radius=13, fill=accent)
    return image


def watch(color: str, accent: str) -> Image.Image:
    image, draw = canvas()
    draw.ellipse((150, 312, 330, 332), fill="#eeeeee")
    draw.rounded_rectangle((202, 38, 278, 316), radius=17, fill=color,
                           outline="#333333", width=4)
    draw.ellipse((157, 112, 323, 278), fill=accent, outline="#444444", width=9)
    draw.ellipse((176, 131, 304, 259), fill="#f8f6ef", outline="#666666", width=3)
    draw.line((240, 194, 240, 150), fill="#333333", width=5)
    draw.line((240, 194, 281, 214), fill="#333333", width=5)
    draw.ellipse((235, 189, 245, 199), fill="#333333")
    return image


def save(name: str, image: Image.Image, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    image.save(directory / name, format="PNG", optimize=True)


def main() -> None:
    products = [
        ("01_nike_black_running_shoes.png", shoe("#26272b", "#e67523")),
        ("02_adidas_white_sneakers.png", shoe("#efefea", "#a0a0a0")),
        ("03_puma_blue_training_shoes.png", shoe("#285d9d", "#e6ebf2")),
        ("04_canvas_red_sneakers.png", shoe("#c43d42", "#f0d7b5")),
        ("05_black_leather_backpack.png", backpack("#292b30", "#4d5056")),
        ("06_red_travel_backpack.png", backpack("#bb3a3c", "#db7470")),
        ("07_blue_cotton_tshirt.png", shirt("#3f80b4", "#d5e6f3")),
        ("08_black_sports_tshirt.png", shirt("#24282d", "#f27c32")),
        ("09_silver_wireless_headphones.png", headphones("#aeb7bc", "#e8ebed")),
        ("10_black_wireless_headphones.png", headphones("#34393d", "#798188")),
        ("11_brown_leather_watch.png", watch("#704a35", "#c6a77b")),
        ("12_gold_classic_watch.png", watch("#b39644", "#dcbd69")),
    ]
    for name, image in products:
        save(name, image, OUTPUT)
    save("query_black_running_shoe.png", shoe("#27282d", "#ec7525", variant=True), QUERIES)
    save("query_red_backpack.png", backpack("#be3d40", "#df7771", variant=True), QUERIES)
    print(f"Created {len(products)} product images and 2 separate query images.")


if __name__ == "__main__":
    main()
