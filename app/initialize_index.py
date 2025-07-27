from semantic import load_model, embed_texts, build_faiss_index, save_index
from parser import extract_text_blocks, clean_text
import json
import os

def get_document_metadata(filename: str) -> dict:
    """
    Dynamically extract metadata from any document filename.
    Works with any naming pattern, not just meal-related files.
    """
    base_name = filename.replace('.pdf', '')
    parts = base_name.split(' - ')
    
    metadata = {
        "document_name": filename,
        "categories": [],
        "main_type": "",
        "sub_type": "",
        "sequence": None,
        "tags": []
    }
    
    try:
        # Extract main type and categories
        metadata["main_type"] = parts[0]
        metadata["categories"] = [part.strip() for part in parts]
        
        # Handle sub-types and sequences if present
        if len(parts) > 1:
            if '_' in parts[-1]:
                sub_type, seq = parts[-1].rsplit('_', 1)
                metadata["sub_type"] = sub_type
                metadata["sequence"] = int(seq) if seq.isdigit() else None
            else:
                metadata["sub_type"] = parts[-1]
        
        # Extract potential tags from filename
        lower_name = filename.lower()
        if any(term in lower_name for term in ['manual', 'guide', 'documentation']):
            metadata["tags"].append("documentation")
        if any(term in lower_name for term in ['report', 'analysis', 'study']):
            metadata["tags"].append("report")
            
    except Exception as e:
        print(f"Warning: Error parsing metadata for {filename}: {str(e)}")
    
    return metadata

def initialize_faiss():
    """Initialize FAISS index for any document collection."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_path = os.path.join(base_dir, "input", "input.json")
        pdf_dir = os.path.join(base_dir, "input", "PDFs")
        
        # Validate input paths
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input JSON not found: {input_path}")
        if not os.path.exists(pdf_dir):
            raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

        with open(input_path, encoding='utf-8') as f:
            input_data = json.load(f)

        all_sections = []
        processed_docs = 0
        
        # Process each document
        for doc in input_data.get("documents", []):
            filename = doc.get("filename") or doc.get("file") or doc.get("name")
            if not filename:
                print("Warning: Document missing filename, skipping")
                continue
                
            pdf_path = os.path.join(pdf_dir, filename)
            if not os.path.exists(pdf_path):
                print(f"Warning: PDF not found: {pdf_path}")
                continue

            try:
                # Get metadata and extract text
                doc_metadata = get_document_metadata(filename)
                sections = extract_text_blocks(pdf_path)
                
                # Update each section with metadata
                for section in sections:
                    section.update({
                        "document": doc_metadata["document_name"],
                        "main_type": doc_metadata["main_type"],
                        "sub_type": doc_metadata["sub_type"],
                        "sequence": doc_metadata["sequence"],
                        "categories": doc_metadata["categories"],
                        "tags": doc_metadata["tags"],
                        "content": clean_text(section.get("content", ""))
                    })
                
                all_sections.extend(sections)
                processed_docs += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue

        if not all_sections:
            raise ValueError("No text sections extracted. Check PDF files and permissions.")
        if processed_docs == 0:
            raise ValueError("No documents were successfully processed.")

        # Create and save index
        model = load_model()
        embeddings = embed_texts([section["content"] for section in all_sections], model)
        index = build_faiss_index(embeddings)

        # Save outputs
        index_dir = os.path.join(base_dir, "faiss_index")
        os.makedirs(index_dir, exist_ok=True)
        index_path = os.path.join(index_dir, "index.faiss")
        metadata_path = os.path.join(base_dir, "metadata.json")
        
        save_index(index, index_path)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                "texts": all_sections,
                "stats": {
                    "total_documents": len(input_data.get("documents", [])),
                    "processed_documents": processed_docs,
                    "total_sections": len(all_sections),
                    "timestamp": datetime.now().isoformat()
                }
            }, f, indent=4, ensure_ascii=False)
        
        print(f"Successfully processed {processed_docs} documents with {len(all_sections)} sections.")
        print(f"Index and metadata saved to {index_dir}")
        
    except Exception as e:
        print(f"Error initializing FAISS index: {str(e)}")
        raise

if __name__ == "__main__":
    from datetime import datetime
    initialize_faiss()