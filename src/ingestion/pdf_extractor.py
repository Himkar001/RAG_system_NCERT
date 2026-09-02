import pymupdf as fitz  # PyMuPDF
import re
import os

def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []
    pdf_name = os.path.basename(pdf_path)
    chapter = os.path.splitext(pdf_name)[0]

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            content_type = "paragraph"
            if re.match(r"^\d+\.\d+", line):
                content_type = "section_header"
            elif "=" in line:
                content_type = "equation"
                
            cleaned_lines.append({"text": line, "content_type": content_type})
            
        full_text = " ".join([l["text"] for l in cleaned_lines])
        
        pages_data.append({
            "page_num": page_num + 1,
            "text": full_text,
            "chapter": chapter,
            "pdf_name": pdf_name,
            "lines_meta": cleaned_lines
        })
    
    return pages_data
