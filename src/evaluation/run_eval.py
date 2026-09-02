import argparse
import json
from ragas_evaluator import evaluate_dataset

def main():
    parser = argparse.ArgumentParser(description="Run RAG Evaluation Pipeline")
    parser.add_argument("--dataset", type=str, default="src/evaluation/eval_dataset.json", help="Path to evaluation dataset")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000", help="Base URL of the RAG API")
    args = parser.parse_args()
    
    print(f"Starting evaluation using dataset {args.dataset} and API {args.api_url}...")
    output_path = evaluate_dataset(args.dataset, args.api_url)
    print(f"Evaluation complete. Results saved to {output_path}")
    
    with open(output_path, 'r') as f:
        results = json.load(f)
        
    if not results:
        print("No results found.")
        return
        
    total_relevancy = 0
    total_faithfulness = 0
    total_exact_match = 0
    
    print("\n" + "="*80)
    print(f"{'Question':<30} | {'Relevancy':<10} | {'Faithfulness':<12} | {'Exact Match':<10}")
    print("-" * 80)
    
    for res in results:
        m = res['metrics']
        q_trunc = res['question'][:27] + "..." if len(res['question']) > 30 else res['question']
        print(f"{q_trunc:<30} | {m['answer_relevancy']:<10.4f} | {m['faithfulness']:<12.4f} | {m['exact_match']:<10.4f}")
        
        total_relevancy += m['answer_relevancy']
        total_faithfulness += m['faithfulness']
        total_exact_match += m['exact_match']
        
    n = len(results)
    print("-" * 80)
    print(f"{'AVERAGES':<30} | {total_relevancy/n:<10.4f} | {total_faithfulness/n:<12.4f} | {total_exact_match/n:<10.4f}")
    print("="*80)

if __name__ == "__main__":
    main()
