# app/parser.py
import fitz  # PyMuPDF
import re
from typing import List, Dict, Any

def extract_text_blocks(filepath: str) -> List[Dict[str, Any]]:
    """
    Dynamically extract text sections from any PDF.
    Uses font size, block separation, and simple heuristics to chunk text.
    """
    doc = fitz.open(filepath)
    sections = []
    current_section = None
    avg_font_size = 12

    # Calculate average font size
    font_sizes = []
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.append(span["size"])
    if font_sizes:
        avg_font_size = sum(font_sizes) / len(font_sizes)

    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            block_text = " ".join(span["text"] for line in block["lines"] for span in line["spans"]).strip()
            block_font_size = max(span["size"] for line in block["lines"] for span in line["spans"]) if block["lines"] else avg_font_size

            # Heading detection: font size, all caps, or keywords
            if (block_font_size > avg_font_size * 1.2 or
                block_text.isupper() or
                re.match(r'^[A-Z][a-zA-Z\s\-]+$', block_text)):
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "section_title": block_text,
                    "content": "",
                    "page_number": page_num
                }
            elif current_section:
                current_section["content"] += " " + block_text
            else:
                current_section = {
                    "section_title": f"Page {page_num}",
                    "content": block_text,
                    "page_number": page_num
                }
    if current_section:
        sections.append(current_section)
    doc.close()
    return sections

def clean_text(text: str) -> str:
    """General text cleaning for any document type."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
