# app/eval.py
"""
Evaluation Metrics for Code Generation

This module provides several metrics to evaluate generated code:
  - Pass@k: Checks if at least one of the top k generated outputs exactly matches the reference.
  - CodeBLEU: A code-specific extension of BLEU (simulated using nltk BLEU).
  - CodeBERTScore: Evaluates semantic similarity (simulated).
  - CodeScore: Heuristic based on token overlap between generated and reference code.
  - Halstead Complexity Measures: Quantifies code complexity.

Each function is extensively commented and logs key operations.
"""

import random
import math
from nltk.translate.bleu_score import sentence_bleu

def pass_at_k(outputs, reference, k=1):
    """
    Pass@k Metric:
    
    Evaluates if any of the top k generated outputs exactly matches the reference code.
    
    Parameters:
      outputs (list of str): Generated code outputs.
      reference (str): Gold standard reference code.
      k (int): Number of attempts to consider.
      
    Returns:
      float: 1.0 if any output among top k is exactly correct; otherwise, 0.0.
    """
    top_k = outputs[:k]
    for output in top_k:
        if output.strip() == reference.strip():
            return 1.0
    return 0.0

def code_bleu(generated, reference):
    """
    CodeBLEU Metric (Simplified):
    
    Uses nltk's BLEU score as a proxy for code similarity.
    
    Parameters:
      generated (str): Generated code.
      reference (str): Reference code.
      
    Returns:
      float: BLEU score between 0.0 and 1.0.
    """
    gen_tokens = generated.split()
    ref_tokens = reference.split()
    score = sentence_bleu([ref_tokens], gen_tokens)
    return score

def code_bert_score(generated, reference):
    """
    CodeBERTScore Metric (Simulated):
    
    Simulates semantic similarity using a random score between 0.5 and 1.0.
    
    Parameters:
      generated (str): Generated code.
      reference (str): Reference code.
      
    Returns:
      float: Simulated CodeBERTScore.
    """
    return random.uniform(0.5, 1.0)

def code_score(generated, reference):
    """
    CodeScore Metric (Simplified):
    
    Estimates functional correctness by computing token overlap between generated and reference code.
    
    Parameters:
      generated (str): Generated code.
      reference (str): Reference code.
      
    Returns:
      float: Ratio of common tokens.
    """
    gen_tokens = set(generated.split())
    ref_tokens = set(reference.split())
    if not ref_tokens:
        return 0.0
    common = gen_tokens.intersection(ref_tokens)
    return len(common) / len(ref_tokens)

def halstead_complexity(code):
    """
    Halstead Complexity Measures:
    
    Computes a simplified version of Halstead metrics:
      - n1: Number of distinct operators.
      - n2: Number of distinct operands.
      - N1: Total operator count.
      - N2: Total operand count.
      - Vocabulary: n1 + n2.
      - Length: N1 + N2.
      - Volume: Length * log2(Vocabulary).
      
    Parameters:
      code (str): Code snippet to evaluate.
      
    Returns:
      dict: Halstead metrics.
    """
    tokens = code.split()
    operators = set(['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '=', '+=', '-=', '*=', '/=', '%=', 'and', 'or', 'not'])
    op_tokens = []
    operand_tokens = []
    
    for token in tokens:
        if token in operators:
            op_tokens.append(token)
        else:
            operand_tokens.append(token)
    
    n1 = len(set(op_tokens))
    n2 = len(set(operand_tokens))
    N1 = len(op_tokens)
    N2 = len(operand_tokens)
    vocabulary = n1 + n2
    length = N1 + N2
    volume = length * (math.log2(vocabulary) if vocabulary > 0 else 0)
    
    return {
        "n1": n1,
        "n2": n2,
        "N1": N1,
        "N2": N2,
        "Vocabulary": vocabulary,
        "Length": length,
        "Volume": volume
    }

# -------------------------
# Example Usage (for local testing)
# -------------------------
if __name__ == "__main__":
    # Example reference code snippet
    reference_code = """
def add(a, b):
    return a + b
"""
    generated_outputs = [
        """
def add(a, b):
    return a + b
""",
        """
def add_numbers(x, y):
    return x + y
""",
        """
def sum_values(a, b):
    return a - b
"""
    ]
    
    k = 1
    print("Evaluating Pass@k...")
    pass1 = pass_at_k(generated_outputs, reference_code, k)
    print(f"Pass@{k}: {pass1}")
    
    print("\nEvaluating CodeBLEU...")
    bleu = code_bleu(generated_outputs[0], reference_code)
    print(f"CodeBLEU score: {bleu:.2f}")
    
    print("\nEvaluating CodeBERTScore (simulated)...")
    bert_score = code_bert_score(generated_outputs[0], reference_code)
    print(f"CodeBERTScore: {bert_score:.2f}")
    
    print("\nEvaluating CodeScore...")
    cscore = code_score(generated_outputs[0], reference_code)
    print(f"CodeScore: {cscore:.2f}")
    
    print("\nCalculating Halstead Complexity Measures...")
    halstead = halstead_complexity(generated_outputs[0])
    print("Halstead Complexity Measures:", halstead)
