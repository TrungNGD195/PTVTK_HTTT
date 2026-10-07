# Visual Paradigm diagrams

The Use Case Diagram, Task 3 three-layer Component Diagram, and Task 4 Voice-Search Sequence Diagram are in `ass6.vpp`. Exported images are `results/task3_component_diagram.png` and `results/task4_voice_search_sequence.png`. All three diagrams are already inserted into the Word report.

The requested `vp-mcp` plugin was installed for Visual Paradigm 18.1. When Visual Paradigm starts, this local build listens on `127.0.0.1:2026`. The exported PNG carries Visual Paradigm's Evaluation Copy watermark; the editable diagram is in `ass6.vpp`.

## 1. Use Case Diagram

- System boundary: **Multimodal E-Commerce Search System**.
- Actor: **Customer**.
- Use cases (exact assignment names): **Search Product**, **Search by Keyword**, **Search by Voice**, **Search by Image**, **Search Order**, **View Product**, **View Order**.
- Associate Customer with Search by Keyword, Search by Voice, Search by Image, Search Order, View Product, and View Order.
- Model Search by Keyword, Search by Voice, and Search by Image as specialized forms of Search Product using UML generalization arrows toward Search Product. This expresses the three alternative modes without claiming that all three must run each time.
- Model View Product as an optional `<<extend>>` of Search Product and View Order as an optional `<<extend>>` of Search Order. If preferred, use plain actor associations only; do not use `<<include>>` for optional viewing.

## 2. Three-Layer Component Diagram with Packages

Create one **Component Diagram** in Visual Paradigm. Sections 8.2 and 20 (Task 3) of the handout require a three-layer component/package diagram, with these UML packages:

1. **Presentation Layer**
2. **Application / Intelligence Layer**
3. **Data Layer**

### Components to draw

| Package | Components | Responsibility |
|---|---|---|
| Presentation Layer | `SearchUI`, `VoiceInput`, `ImageUpload`, `SearchResultView` | Accept input and present results |
| Application / Intelligence Layer | `QueryService`, `SpeechService`, `ImageService`, `SearchService`, `RankingService` | Normalize input, retrieve candidates, rank results |
| Data Layer | `ProductRepository`, `OrderRepository`, `VectorIndex`, `ProductDatabase`, `OrderDatabase`, `ImageStorage` | Store and retrieve product, order, image, and vector data |

### Relationships to draw

- `VoiceInput` and `ImageUpload` feed `SearchUI`; `SearchUI` sends output to `SearchResultView`.
- `SearchUI` uses `QueryService`, `SpeechService`, and `SearchService`.
- `SearchService` uses `ImageService`, `RankingService`, `ProductRepository`, `OrderRepository`, and `VectorIndex`.
- `ProductRepository` accesses `ProductDatabase`; `OrderRepository` accesses `OrderDatabase`; `ImageService` accesses `ImageStorage`.
- Cross-layer dependencies flow **Presentation ? Application / Intelligence ? Data**. No Presentation component accesses Data directly.

This is an architecture view. `VoiceInput`, `ImageUpload`, `SearchResultView`, `ProductDatabase`, `OrderDatabase`, and `ImageStorage` are conceptual roles or storage elements rather than separate Python classes. The Python implementation details belong in the report's implementation section. The code's `main.py` builds the services; it is not a fourth architecture layer.

## 3. Voice-Search Sequence Diagram

Actor: **Customer** (`InteractionActor` in Visual Paradigm). The six system lifelines are **SearchUI**, **SpeechService**, **QueryService**, **SearchService**, **ProductRepository**, and **RankingService**. Apply `«boundary»` to SearchUI, `«control»` to SpeechService, QueryService, SearchService, and RankingService, and `«entity»` to ProductRepository.

1. Customer -> SearchUI: `provideVoiceInput(transcriptText)`.
2. SearchUI -> SpeechService: `transcribe(transcriptText)`.
3. SpeechService --> SearchUI: `recognizedText` (simulated).
4. SearchUI -> QueryService: `voice_query(recognizedText)`.
5. QueryService --> SearchUI: `query{type=voice, text=recognizedText}`.
6. SearchUI -> SearchService: `search(query, limit)`.
7. SearchService -> ProductRepository: `all_products()`.
8. ProductRepository --> SearchService: `productList`.
9. SearchService -> RankingService: `rank(candidates, voice, limit)`.
10. RankingService --> SearchService: `rankedResults`.
11. SearchService --> SearchUI: `response{products, scores}`.
12. SearchUI --> Customer: `displayResults(names, scores)`.

You may show QueryService and SpeechService as application components even though SearchUI coordinates the calls; this matches the code in `presentation/search_ui.py`.

## Figures included in the report

1. Use Case Diagram in Section 3.
2. Three-Layer Component Diagram with Packages in Section 4.
3. Voice-Search Sequence Diagram in Section 5.
4. A stored product illustration and separate image-query illustration in Section 6.
5. Program output for text, simulated voice, and image search in Section 8.2; combined text-and-image output in Section 9.
