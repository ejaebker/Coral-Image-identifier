# Project Architecture Diagram

The following diagram illustrates the flow of data from the initial web crawl to the final machine learning model.

```mermaid
graph TD
    subgraph "1. Data Collection (src/data/crawler.py)"
        A[Bing Image Search] -->|Scrape| B(data/raw/)
        C[Retailer Sites - Shopify/WWC] -->|Scrape| B
        D[Retailer Sites - Magento/TG] -->|Scrape| B
    end

    subgraph "2. Processing Pipeline (src/core/processor.py)"
        B --> E{Integrity Check}
        E -->|Corrupted| F[Discard]
        E -->|Valid| G[Perceptual Hash]
        G --> H{Deduplication}
        H -->|Already Seen| I[Discard]
        H -->|Unique| J[Convert to LAB Space]
        J --> K[Apply CLAHE to L-Channel]
        K --> L[Convert to RGB]
        L --> M[Resize to 224x224]
        M -->|Save| N(data/processed/)
    end

    subgraph "3. Refinement"
        N --> N1[src/data/cleaner.py]
        N1 -->|Manually Pruned| N(data/processed/)
    end

    subgraph "4. Model Training (src/training/train.py)"
        N --> O[TensorFlow Dataset Loader]
        O --> P[Data Augmentation]
        P --> Q[CNN Training Loop (Class Weights)]
        Q --> R[coral_model_best.keras]
        R --> S[TFLite Export]
    end

    subgraph "5. Evaluation (src/training/evaluator.py)"
        R --> T[Classification Report]
        R --> U[Confusion Matrix]
        R --> V[Sample Prediction Grid]
    end
```

### How to view this diagram:
*   **GitHub/VS Code**: This diagram will render automatically if viewed in the GitHub web interface or VS Code with a Markdown Preview extension.
*   **Mermaid Live**: You can copy the code block above into the [Mermaid Live Editor](https://mermaid.live/) to export it as an image (PNG/SVG) for presentations.
