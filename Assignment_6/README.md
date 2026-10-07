# Assignment 06 — Multimodal E-Commerce Search

This package contains the PDF report, editable Word report, Python prototype, product data, original sample illustrations, demonstration/evaluation output, and `ass6.vpp` with the Use Case Diagram, Task 3 Component Diagram, and Task 4 Voice-Search Sequence Diagram. The report includes the UML figures, a sample image pair, and screenshots of the Python program running in a terminal.

## Requirements

- Python 3.10 or newer (developed with Python 3.13)
- Pillow and NumPy for image representation and cosine search
- `python-docx` only if you want to regenerate the Word report

From the project root, install the packages:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py demo
python main.py text "black running shoes"
python main.py voice "find white sneakers"
python main.py image "data/query_images/query_red_backpack.png"
python main.py multimodal "black running shoes" "data/query_images/query_black_running_shoe.png"
python main.py order O001 C001
python evaluate.py
```

The `voice` argument is **already-transcribed text**. There is no microphone recording or live speech recognizer. The separate query illustrations are not identical to the stored product illustrations; the image service reads their pixels and computes a color/shape vector.

## Project structure

```text
Assignment_6/
├── A6_V2_TrungNGD.pdf               # final PDF report
├── Bao_cao_Assignment_06.docx      # editable English report
├── ass6.vpp                         # Visual Paradigm project with three UML diagrams
├── main.py                          # command-line entry point
├── evaluate.py                      # evaluation and evidence output
├── requirements.txt
├── README.md
├── VISUAL_PARADIGM_GUIDE.md         # exact diagram content to draw
├── application/                     # query, speech, image, retrieval, ranking
├── presentation/                    # SearchUI
├── data/
│   ├── product_repository.py
│   ├── order_repository.py
│   ├── vector_index.py
│   ├── products.json                 # 12 products
│   ├── orders.json
│   ├── images/                       # 12 product PNGs
│   └── query_images/                 # 2 independent query PNGs
├── results/
│   ├── demo_results.txt
│   ├── evaluation.csv
│   ├── evaluation.json
│   ├── task3_component_diagram.png       # exported Task 3 diagram
│   ├── task4_voice_search_sequence.png  # exported Task 4 diagram
│   ├── task6_text_voice_screenshot.png   # terminal screenshot: text and voice
│   ├── task6_image_screenshot.png        # terminal screenshot: image search
│   └── task6_multimodal_screenshot.png   # terminal screenshot: combined query
└── tools/
    ├── generate_sample_images.py
    └── build_report.py
```

## Architecture and method

`SearchUI` accepts the input and displays results. `QueryService` maps all modalities to a common query dictionary. `SpeechService` returns a simulated transcript. `ImageService` extracts a visual vector from image pixels. `SearchService` retrieves candidates from the repositories and `VectorIndex`; `RankingService` orders the candidates. The data layer does not call the application layer, and the presentation layer does not directly read a repository.

Text retrieval uses normalized words in name, brand, color, category, and description, plus an optional `under/below/less than` price ceiling. Image retrieval computes cosine similarity between a query image vector and stored product vectors. Ranking combines normalized relevance with a small stock signal. Multimodal ranking gives equal weight to text and image relevance and a small weight to stock.

The sample PNGs are original generated illustrations made with Pillow for this assignment. Regenerate them with `python tools/generate_sample_images.py` if needed. This overwrites the sample images, so do it only if you do not intend to preserve edits to those images.

## Submission evidence

`python evaluate.py` writes the actual demo transcript and the Top-1 evaluation to `results/`. The current result is **12/13 successful queries (92.31%)**. The failed example, “footwear for jogging,” shows the keyword search limitation. The Word report includes the three Visual Paradigm diagrams and screenshots of text, simulated voice, image, and combined searches running in a terminal. The file `VISUAL_PARADIGM_GUIDE.md` lists the exact UML content.

The PDF report is `A6_V2_TrungNGD.pdf`. The Task 4 diagram is in `ass6.vpp`; its exported image is `results/task4_voice_search_sequence.png`. Do not regenerate the Word report with `tools/build_report.py` after editing it, because that script recreates the template and would replace the inserted figures with placeholders.

## Limitations

- Voice input is simulated from transcript text.
- The image descriptor is handcrafted rather than a pretrained model. It works on the included product illustrations; performance on photos is not established.
- Text search has no semantic synonym understanding and supports only basic English word normalization.
- Data is stored in JSON and a small in-memory index, with no authentication service or persistent database.
- Order lookup requires a customer ID and returns only an order belonging to that ID; real identity verification is outside this prototype.
