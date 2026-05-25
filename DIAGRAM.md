# Project Architecture Diagram

The following diagram illustrates the flow of data from the initial web crawl to the final machine learning model.

```mermaid
graph TD
    subgraph "1. Data Collection (image_crawler.py)"
        A[Bing Image Search] -->|Scrape| B(data/raw/)
        C[Retailer Sites - Shopify/WWC] -->|Scrape| B
        D[Retailer Sites - Magento/TG] -->|Scrape| B
    end

    subgraph "2. Processing Pipeline (image_processor.py)"
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

    subgraph "3. Model Training (ML-backend.py)"
        N --> O[TensorFlow Dataset Loader]
        O --> P[Data Augmentation]
        P --> Q[CNN Training Loop]
        Q --> R[Model Metrics & Results]
    end
```

### How to view this diagram:
*   **GitHub/VS Code**: This diagram will render automatically if viewed in the GitHub web interface or VS Code with a Markdown Preview extension.
*   **Mermaid Live**: You can copy the code block above into the [Mermaid Live Editor](https://mermaid.live/) to export it as an image (PNG/SVG) for presentations.
