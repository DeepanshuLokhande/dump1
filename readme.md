
# Semantic Search and Document Analysis Project

This project implements a **semantic search system** that processes PDF documents, creates a FAISS index from their content, and performs a semantic search based on a given persona and task. The output provides extracted sections and a detailed subsection analysis.

---

## 📚 Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Working and Workflow](#working-and-workflow)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Input and Output](#input-and-output)
- [Core Components](#core-components)
- [Dependencies](#dependencies)

---

## 📁 Project Structure

```
.
├── app/
│   ├── initialize_index.py
│   ├── main.py
│   ├── parser.py
│   ├── semantic.py
│   └── utils.py
├── input/
│   ├── input.json
│   └── PDFs/
├── output/
│   └── challenge1b_output.json
├── faiss_index/
│   └── index.faiss
├── metadata.json
├── Dockerfile
├── requirements.txt
└── README.md
```

---

##  Features

-  **Dynamic PDF Text Extraction** using font-size and layout heuristics.
-  **Flexible Metadata Extraction** from filenames.
-  **Semantic Embedding** via `sentence-transformers`.
-  **FAISS Indexing** for efficient similarity search.
-  **Semantic Search** based on persona + task queries.
-  **Structured Output** in JSON with top sections and detailed analysis.
-  **Dockerized** for portability and reproducibility.

---

# Working and Workflow

The application runs in two phases:

### 1. **Initialization and Indexing** (`initialize_index.py`)
- Reads `input/input.json` for document list.
- Extracts structured text and metadata from PDFs using `parser.py`.
- Cleans text and generates sentence embeddings using `semantic.py`.
- Builds a FAISS index and saves metadata to `metadata.json`.

### 2. **Semantic Search and Output Generation** (`main.py`)
- Loads `input.json`, FAISS index, and metadata.
- Forms a semantic query using persona and task.
- Embeds the query and performs similarity search over the index.
- Returns top-k most relevant sections and outputs results to `output/challenge1b_output.json`.

---

# Setup and Installation

## Prerequisites

- [Docker](https://www.docker.com/) installed

### Building the Docker Image

1. Clone the repo or place all files in your root directory.
2. Create the input folder structure:
   ```bash
   mkdir -p input/PDFs
   ```
3. Place your PDFs inside `input/PDFs/` and update `input/input.json` accordingly.
4. Build the Docker image:
   ```bash
   docker build -t semantic-search-app .
   ```

---

##  Usage

Run the Docker container:

```bash
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output semantic-search-app
```

- `-v $(pwd)/input:/app/input`: Mounts local `input/` directory.
- `-v $(pwd)/output:/app/output`: Mounts local `output/` directory to receive the output file.

After execution, check `output/challenge1b_output.json`.

---

##  Input and Output

###  Input: `input/input.json`

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
  },
  "documents": [
    {
      "filename": "South of France - Cities.pdf",
      "title": "South of France - Cities"
    }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

###  Output: `output/challenge1b_output.json`

```json
{
  "metadata": {
    "challenge_id": "round_1b_002",
    "timestamp": "...",
    "persona": "...",
    "task": "..."
  },
  "extracted_sections": [
    {
      "document": "...",
      "section_title": "...",
      "page_number": 5,
      "importance_rank": 1
    },
    ...
  ],
  "subsection_analysis": [
    {
      "refined_text": "...",
      "document": "...",
      "page_number": 5
    },
    ...
  ]
}
```

---

##  Core Components

### `initialize_index.py`
- Reads input, extracts + cleans text via `parser.py`.
- Generates embeddings via `semantic.py`.
- Saves FAISS index and metadata.

### `main.py`
- Loads index and metadata.
- Forms semantic query and performs FAISS search.
- Saves structured result to `output/`.

### `parser.py`
- `extract_text_blocks(filepath)` – splits PDF into sections.
- `clean_text(text)` – whitespace cleanup and formatting.

### `semantic.py`
- Loads SentenceTransformer.
- `embed_texts()`, `build_faiss_index()`, `save_index()`, `load_index()`.

### `utils.py`
- Timestamp generation and helper utilities.

---

##  Dependencies

Listed in `requirements.txt`:

```
PyMuPDF
sentence-transformers
scikit-learn
faiss-cpu
tqdm
numpy
```

---

##  Notes

- Ensure PDF filenames in `input.json` match those in `input/PDFs/`.
- For different use cases, only update `input.json` — no need to reprocess PDFs unless content changes.

---

## Author

Made for the Adobe India Hackathon Round 1B – Semantic Document Understanding Challenge.


