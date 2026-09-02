"""
render_pages.py — Renders all NCERT PDF pages as PNG images and rebuilds image_metadata.json.

For each PDF in data/raw/pdfs/:
  - Renders every page at 150 DPI as a PNG
  - Extracts text from the page (used as searchable OCR proxy)
  - Saves to data/processed/rendered_pages/{chapter}_page{N}.png
  - Builds image_metadata.json: [{page, image_path, pdf_name, chapter, ocr_text, has_diagram}]
"""

import os
import json
import glob
import re
import pymupdf as fitz

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
PDF_DIR = os.path.join(BASE_DIR, "data", "raw", "pdfs")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed", "rendered_pages")
META_PATH = os.path.join(BASE_DIR, "data", "processed", "image_metadata.json")

os.makedirs(OUT_DIR, exist_ok=True)

# Keywords that suggest a page has a diagram / figure
DIAGRAM_KEYWORDS = [
    "fig.", "figure", "diagram", "illustration", "chart",
    "graph", "schematic", "experiment", "apparatus", "setup",
    "shows", "depicted", "drawn", "represented"
]

def has_diagram_on_page(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in DIAGRAM_KEYWORDS)

def chapter_name_from_pdf(pdf_path: str) -> str:
    name = os.path.splitext(os.path.basename(pdf_path))[0]
    # Make it filesystem-safe and human-readable
    return name.replace(" ", "_")

def render_pdf(pdf_path: str, metadata: list):
    chapter = chapter_name_from_pdf(pdf_path)
    pdf_name = os.path.basename(pdf_path)
    doc = fitz.open(pdf_path)

    print(f"  Rendering {pdf_name} ({len(doc)} pages)...")
    page_data = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Render at 150 DPI
        mat = fitz.Matrix(150 / 72, 150 / 72)
        pix = page.get_pixmap(matrix=mat)

        # Save pixmap bytes while doc is still open
        img_filename = f"{chapter}_page{page_num + 1}.png"
        img_path = os.path.join(OUT_DIR, img_filename)
        pix.save(img_path)
        pix = None  # release pixmap memory

        # Extract text from page (OCR proxy)
        text = page.get_text("text").strip()
        ocr_text = " ".join(text.split())

        page_data.append({
            "page": page_num + 1,
            "image_path": f"data/processed/rendered_pages/{img_filename}",
            "image_filename": img_filename,
            "pdf_name": pdf_name,
            "chapter": chapter,
            "ocr_text": ocr_text[:2000],
            "has_diagram": has_diagram_on_page(text)
        })

    doc.close()
    metadata.extend(page_data)
    print(f"    Done: {len(page_data)} pages rendered.")


def main():
    pdf_files = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))
    if not pdf_files:
        print("No PDFs found in", PDF_DIR)
        return

    print(f"Found {len(pdf_files)} PDFs. Rendering pages...")
    metadata = []

    for pdf_path in pdf_files:
        try:
            render_pdf(pdf_path, metadata)
        except Exception as e:
            print(f"  ERROR rendering {pdf_path}: {e}")

    # Save metadata
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    diagram_pages = sum(1 for m in metadata if m["has_diagram"])
    print(f"\nDone!")
    print(f"  Total pages rendered : {len(metadata)}")
    print(f"  Pages with diagrams  : {diagram_pages}")
    print(f"  Metadata saved to    : {META_PATH}")


if __name__ == "__main__":
    main()
