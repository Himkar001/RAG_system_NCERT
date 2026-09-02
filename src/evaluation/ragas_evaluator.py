import json
import time
import os
import requests
import re
from datetime import datetime
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    MODEL = None
    print("Warning: sentence_transformers not installed. answer_relevancy will be 0.0")

def evaluate_single(question, answer, ground_truth, retrieved_chunks):
    def normalize_text(text):
        return re.sub(r'\W+', '', str(text).lower())
    
    exact_match = 1.0 if normalize_text(answer) == normalize_text(ground_truth) else 0.0
    
    if MODEL and answer.strip():
        q_emb = MODEL.encode([question])
        a_emb = MODEL.encode([answer])
        answer_relevancy = float(cosine_similarity(q_emb, a_emb)[0][0])
    else:
        answer_relevancy = 0.0
        
    if retrieved_chunks and answer.strip():
        chunk_text = " ".join(retrieved_chunks).lower()
        answer_words = set(re.findall(r'\w+', answer.lower()))
        chunk_words = set(re.findall(r'\w+', chunk_text))
        if answer_words:
            faithfulness = len(answer_words.intersection(chunk_words)) / len(answer_words)
        else:
            faithfulness = 0.0
    else:
        faithfulness = 0.0

    return {
        "answer_relevancy": answer_relevancy,
        "faithfulness": faithfulness,
        "exact_match": exact_match
    }

def evaluate_dataset(dataset_path, api_base_url):
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
        
    results = []
    for item in dataset:
        question = item['question']
        ground_truth = item['ground_truth']
        
        # Call local API
        try:
            # Assuming a generic /query endpoint for the RAG system
            response = requests.post(f"{api_base_url}/query", json={"question": question}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                retrieved_chunks = data.get('chunks', []) # Or context
            else:
                answer = "API Error"
                retrieved_chunks = []
        except Exception as e:
            print(f"Failed to call API for question: {question} - Error: {e}")
            answer = "API Error"
            retrieved_chunks = []
            
        metrics = evaluate_single(question, answer, ground_truth, retrieved_chunks)
        
        results.append({
            "question": question,
            "ground_truth": ground_truth,
            "answer": answer,
            "metrics": metrics
        })
        
    os.makedirs('outputs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"outputs/eval_results_{timestamp}.json"
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    return output_path
