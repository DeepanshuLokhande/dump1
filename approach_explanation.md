
# Approach and Methodology for Semantic Document Analysis

This project employs a robust, multi-stage methodology to enable efficient semantic search and analysis of PDF documents. The core idea is to transform unstructured text data into a semantically rich, searchable format, allowing for intelligent retrieval based on the meaning and context of a query rather than just keywords.

---

## 1. Document Ingestion and Preprocessing

The initial phase focuses on ingesting raw PDF documents and preparing their content for semantic analysis.

### 📄 Dynamic Text Extraction
The `parser.py` module is central to this. It intelligently extracts text from PDFs by analyzing the document's structure, including font sizes and block layouts. This allows it to identify and segment the document into logical "sections" (e.g., headings and their associated paragraphs), rather than simply treating the PDF as a flat stream of text. This structural awareness is crucial for maintaining context.

### 🧹 Text Cleaning
Extracted text undergoes a cleaning process to remove redundant whitespace and ensure uniformity, which is vital for effective downstream processing.

### 🏷 Metadata Enrichment
Concurrently, the `initialize_index.py` script dynamically extracts metadata directly from the PDF filenames. This flexible approach allows the system to categorize and tag documents based on their naming conventions, enriching each extracted text section with valuable contextual information like document name, main type, sub-type, and potential tags.

---

## 2. Semantic Representation (Embeddings)

Once the text is extracted and cleaned, the next step is to convert it into a numerical format that computers can understand and process for semantic similarity.

### 🔢 Sentence Embeddings
The `semantic.py` module leverages a pre-trained SentenceTransformer model (`all-MiniLM-L6-v2`). This powerful deep learning model transforms each text section into a high-dimensional vector, known as an embedding. These embeddings are designed such that texts with similar meanings are located closer together in the vector space, regardless of the exact words used. This is the cornerstone of semantic search, moving beyond simple keyword matching.

---

## 3. Efficient Indexing with FAISS

To enable rapid search across potentially large collections of document embeddings, an efficient indexing mechanism is required.

### 🧮 FAISS Index Construction
After all text sections are converted into embeddings, `initialize_index.py` utilizes FAISS (Facebook AI Similarity Search) to build an optimized index. FAISS is a library for efficient similarity search and clustering of dense vectors. A `FlatL2` index is employed, which performs a brute-force L2 (Euclidean distance) search, guaranteeing accuracy for similarity retrieval.

### 💾 Persistent Storage
The generated FAISS index (`index.faiss`) and the corresponding metadata (`metadata.json`, which maps index IDs back to original document sections and their content) are saved to disk. This allows for quick loading and querying without needing to re-process the entire document collection each time.

---

## 4. Semantic Search Execution

With the knowledge base established, the system is ready to answer queries.

### 🔍 Contextual Query Formulation
The `main.py` script constructs a semantic query by combining the user's specified "persona" and "job to be done" (task). This contextualizes the search, making it more relevant to the user's intent.

### 🧠 Query Embedding
Just like the document sections, this combined query string is also converted into a semantic embedding using the same SentenceTransformer model.

### 🚀 Similarity Search
The query embedding is then used to perform a similarity search against the FAISS index. FAISS quickly identifies the top *k* (e.g., 5) most semantically similar text sections whose embeddings are closest (most similar) to the query embedding.

---

## 5. Structured Output Generation

The final phase involves presenting the search results in a clear and actionable format.

### 📤 Comprehensive JSON Output
The `main.py` script compiles the identified relevant sections into a structured JSON file (`challenge1b_output.json`). This output includes:
- **High-level metadata** about the search
- A list of `extracted_sections` providing a summary (document, title, rank, page)
- A detailed `subsection_analysis` which includes the full `refined_text` content of each relevant section

This dual presentation allows for both a quick overview and deep dive into the retrieved information.

This methodology ensures that the system can intelligently understand and retrieve information from complex documents, providing highly relevant results based on semantic understanding rather than just keyword matching.
