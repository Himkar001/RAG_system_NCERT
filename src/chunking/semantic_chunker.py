import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_parent_child_chunks(pages):
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, # ~400 tokens roughly
        chunk_overlap=150
    )
    
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, # ~100 tokens roughly
        chunk_overlap=50
    )
    
    parents = []
    children = []
    
    for page in pages:
        text = page["text"]
        parent_chunks = parent_splitter.split_text(text)
        
        for p_text in parent_chunks:
            parent_id = str(uuid.uuid4())
            parents.append({
                "text": p_text,
                "chunk_id": parent_id,
                "parent_id": None,
                "page": page["page_num"],
                "chapter": page["chapter"],
                "content_type": "mixed",
                "chunk_type": "parent"
            })
            
            child_chunks = child_splitter.split_text(p_text)
            for c_text in child_chunks:
                children.append({
                    "text": c_text,
                    "chunk_id": str(uuid.uuid4()),
                    "parent_id": parent_id,
                    "page": page["page_num"],
                    "chapter": page["chapter"],
                    "content_type": "mixed",
                    "chunk_type": "child"
                })
                
    return {"parents": parents, "children": children}
