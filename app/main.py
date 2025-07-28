# app/main.py
import json
import numpy as np
from semantic import load_model, embed_texts, load_index
from utils import get_timestamp

def load_metadata(path="metadata.json"):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Metadata file not found at: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in metadata file: {path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Error reading file encoding. Make sure {path} is saved as UTF-8")

def load_input(path="input/input.json"):
    with open(path) as f:
        return json.load(f)

def semantic_search(query_vector, index, k=5):
    D, I = index.search(np.array([query_vector]), k)
    return I[0]

def main():
    # Load input
    input_data = load_input()
    persona = input_data["persona"]["role"]
    task = input_data["job_to_be_done"]["task"]
    input_docs = [doc["filename"] for doc in input_data["documents"]]

    # Construct semantic query
    query = f"As a {persona}, I need to {task}"

    # Load embedding model
    model = load_model()
    query_vec = embed_texts([query], model)[0]

    # Load FAISS index and metadata
    index = load_index("faiss_index/index.faiss")
    metadata = load_metadata()

    # Perform semantic search
    top_k_indices = semantic_search(query_vec, index, k=5)

    # Build output JSON with modified structure for subsection analysis
    output = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": task,
            "processing_timestamp": get_timestamp()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for rank, idx in enumerate(top_k_indices, start=1):
        section = metadata["texts"][int(idx)]
        
        # Add to extracted sections
        output["extracted_sections"].append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": rank,
            "page_number": section["page_number"]
        })

        # Add to subsection analysis with full content
        output["subsection_analysis"].append({
            "document": section["document"],
            "refined_text": section["content"],  # Use full content instead of just title
            "page_number": section["page_number"]
        })

    # Save output with UTF-8 encoding
    with open("/app/output/challenge1b_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
