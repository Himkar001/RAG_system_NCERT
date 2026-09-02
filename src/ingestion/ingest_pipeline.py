import os
import glob
import json
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import sys

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.ingestion.pdf_extractor import extract_pdf
from src.chunking.semantic_chunker import create_parent_child_chunks

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    raw_dir = os.path.join(base_dir, 'data', 'raw', 'pdfs')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    chroma_dir = os.path.join(base_dir, 'chroma_db')
    
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(chroma_dir, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(raw_dir, '*.pdf'))
    print(f"Found {len(pdf_files)} PDFs in {raw_dir}")
    
    all_parents = []
    all_children = []
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        try:
            pages = extract_pdf(pdf_file)
            chunks = create_parent_child_chunks(pages)
            all_parents.extend(chunks['parents'])
            all_children.extend(chunks['children'])
        except Exception as e:
            print(f"Failed to process {pdf_file}: {e}")
            
    print(f"Total parent chunks: {len(all_parents)}")
    print(f"Total child chunks: {len(all_children)}")
    
    # Store chunks as JSON
    all_chunks = {"parents": all_parents, "children": all_children}
    chunks_path = os.path.join(processed_dir, 'all_chapters_chunks.json')
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"Saved chunks to {chunks_path}")
    
    parent_chunks_path = os.path.join(processed_dir, 'parent_chunks.json')
    with open(parent_chunks_path, 'w', encoding='utf-8') as f:
        json.dump(all_parents, f, ensure_ascii=False, indent=2)
    print(f"Saved parent chunks to {parent_chunks_path}")
    
    # Initialize embedding model
    print("Initializing embedding model...")
    embeddings = get_embeddings()
    
    # Initialize Chroma client
    client = chromadb.PersistentClient(path=chroma_dir)
    
    # Handle main collection (children)
    print("Indexing child chunks...")
    try:
        client.delete_collection(name="langchain")
    except Exception:
        pass
        
    child_docs = [
        Document(
            page_content=c["text"], 
            metadata={"chunk_id": c["chunk_id"], "parent_id": c["parent_id"], "page": c["page"], "chapter": c["chapter"]}
        ) for c in all_children
    ]
    
    child_store = Chroma.from_documents(
        documents=child_docs,
        embedding=embeddings,
        collection_name="langchain",
        persist_directory=chroma_dir
    )
    
    # Handle parents collection
    print("Indexing parent chunks...")
    try:
        client.delete_collection(name="parents")
    except Exception:
        pass
        
    parent_docs = [
        Document(
            page_content=c["text"], 
            metadata={"chunk_id": c["chunk_id"], "page": c["page"], "chapter": c["chapter"]}
        ) for c in all_parents
    ]
    
    parent_store = Chroma.from_documents(
        documents=parent_docs,
        embedding=embeddings,
        collection_name="parents",
        persist_directory=chroma_dir
    )
    
    print("Ingestion complete!")
    
if __name__ == "__main__":
    main()
