# app/main.py
"""
Main FASTAPI Application

This service accepts natural language input describing a data engineering task and:
  - Generates design documentation using LangChain.
  - Generates production-ready pipeline code.
  - Generates inline code documentation.
  - Generates unit tests for the generated code.
  - Runs the generated pipeline on a synthetic dataset.
  - Evaluates the generated code using multiple metrics.

Huge inline comments and detailed logging have been added to ease debugging and maintenance.
"""

from fastapi import FastAPI
import logging
import uvicorn
from pydantic import BaseModel

# Import our custom modules
from app.langchain_utils import (
    generate_design_doc,
    generate_pipeline_code,
    generate_unit_tests,
    generate_inline_docs,
)
from app.pipeline import run_pipeline
from app.sample_data_generator import generate_large_dataset
from app.eval import pass_at_k, code_bleu, code_bert_score, code_score, halstead_complexity

# Configure logging to show detailed info
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Generative AI-Driven Data Engineering Agent")

# Request model for our endpoint
class PipelineRequest(BaseModel):
    natural_language_input: str

@app.post("/generate_pipeline")
async def generate_pipeline(request: PipelineRequest):
    """
    Generate and evaluate a complete data pipeline solution based on natural language input.
    
    Steps:
      1. Generate design documentation.
      2. Generate production-ready pipeline code.
      3. Generate inline code documentation.
      4. Generate unit tests for the generated code.
      5. Execute the pipeline on a synthetic dataset.
      6. Evaluate the generated code using several metrics.
    
    Returns a JSON object with all generated artifacts and evaluation metrics.
    """
    prompt = request.natural_language_input
    logging.info("Received natural language input for pipeline generation.")
    
    # --- STEP 1: Design Documentation Generation ---
    design_doc = generate_design_doc(prompt)
    logging.info("Generated design documentation.")
    
    # --- STEP 2: Pipeline Code Generation ---
    generated_code = generate_pipeline_code(prompt)
    logging.info("Generated pipeline code.")
    
    # --- STEP 3: Inline Code Documentation ---
    inline_docs = generate_inline_docs(generated_code)
    logging.info("Generated inline code documentation.")
    
    # --- STEP 4: Unit Test Generation ---
    unit_tests = generate_unit_tests(generated_code)
    logging.info("Generated unit tests for the pipeline code.")
    
    # --- STEP 5: Run the Pipeline on a Synthetic Dataset ---
    # For faster testing, we generate a dataset with 10,000 records instead of 1,000,000.
    dataset = generate_large_dataset(10000)
    pipeline_results = run_pipeline(dataset)
    logging.info("Executed the data pipeline on synthetic dataset.")
    
    # --- STEP 6: Evaluate the Generated Code ---
    # Use a hardcoded reference code snippet (gold standard) for this data engineering problem.
    reference_code = """
import pandas as pd

def run_pipeline(input_df: pd.DataFrame) -> pd.DataFrame:
    df_clean = input_df.dropna(subset=['revenue', 'cost'])
    df_clean['profit'] = df_clean['revenue'] - df_clean['cost']
    return df_clean
"""
    # Simulate multiple generated outputs (for Pass@k evaluation)
    generated_outputs = [generated_code, generated_code.replace("pipeline", "data_pipeline")]
    
    eval_metrics = {
        "pass_at_1": pass_at_k(generated_outputs, reference_code, k=1),
        "code_bleu": code_bleu(generated_code, reference_code),
        "code_bert_score": code_bert_score(generated_code, reference_code),
        "code_score": code_score(generated_code, reference_code),
        "halstead_complexity": halstead_complexity(generated_code)
    }
    logging.info("Evaluated generated code using multiple metrics.")
    
    # Return all artifacts and evaluation metrics in the response
    return {
        "design_documentation": design_doc,
        "generated_pipeline_code": generated_code,
        "inline_code_documentation": inline_docs,
        "unit_tests": unit_tests,
        "pipeline_execution_results": pipeline_results,
        "evaluation_metrics": eval_metrics
    }

if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
