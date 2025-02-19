# app/langchain_utils.py
"""
LangChain Utility Functions

This module provides helper functions that use LangChain (and an LLM like OpenAI)
to generate various artifacts from natural language prompts:
  - Design documentation.
  - Production-ready pipeline code.
  - Unit tests.
  - Inline code documentation.
  
Each function logs its operation for transparency.
"""

import logging
# Uncomment and set your OpenAI API key if you want to use the real model
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate

def generate_design_doc(prompt: str) -> str:
    """
    Generate comprehensive design documentation from a natural language description.
    
    Parameters:
      prompt (str): The natural language description of the data pipeline.
      
    Returns:
      str: Generated design documentation.
    """
    design_prompt = (
        f"Generate comprehensive design documentation for a data pipeline that ingests, cleans, transforms data, "
        f"computes derived metrics, and evaluates performance. Requirements:\n{prompt}"
    )
    logging.info("Simulating OpenAI call for design documentation generation.")
    # Simulated response (replace with actual LLM chain call if desired)
    response = (
        "Design Documentation:\n"
        "- **Data Ingestion:** Read raw data from CSV files.\n"
        "- **Data Quality Evaluation:** Log metrics (e.g., missing values) before cleaning.\n"
        "- **Data Cleaning:** Drop rows with missing critical fields ('revenue', 'cost').\n"
        "- **Data Transformation:** Calculate 'profit' as revenue minus cost.\n"
        "- **Evaluation:** Measure execution time and throughput; persist logs and evaluation metrics.\n"
        "- **Scalability:** Designed to handle millions of records with modular components."
    )
    return response

def generate_pipeline_code(prompt: str) -> str:
    """
    Generate production-ready Python code for a data pipeline from a natural language description.
    
    Parameters:
      prompt (str): The natural language description.
      
    Returns:
      str: Generated Python code implementing the data pipeline.
    """
    code_prompt = (
        f"Generate production-ready Python code for a data pipeline that reads data, drops rows with missing "
        f"critical values, computes a new column 'profit' (as revenue minus cost), and returns the cleaned data. "
        f"Requirements:\n{prompt}"
    )
    logging.info("Simulating OpenAI call for pipeline code generation.")
    # Simulated response (replace with actual LLM chain call if desired)
    code = '''
import pandas as pd

def run_pipeline(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the data pipeline:
      - Drop rows with missing 'revenue' or 'cost'
      - Compute 'profit' as revenue minus cost
    Returns the transformed DataFrame.
    """
    df_clean = input_df.dropna(subset=['revenue', 'cost']).copy()
    df_clean['profit'] = df_clean['revenue'] - df_clean['cost']
    return df_clean
'''
    return code

def generate_unit_tests(generated_code: str) -> str:
    """
    Generate unit tests for the provided pipeline code.
    
    Parameters:
      generated_code (str): The generated pipeline code.
      
    Returns:
      str: Generated Python unit tests.
    """
    test_prompt = f"Generate unit tests for the following data pipeline code:\n{generated_code}"
    logging.info("Simulating OpenAI call for unit test generation.")
    # Simulated response
    unit_tests = '''
import unittest
import pandas as pd
from pipeline import run_pipeline

class TestDataPipeline(unittest.TestCase):
    def test_run_pipeline(self):
        # Create a sample dataframe with missing values
        data = {
            'revenue': [100, 200, None],
            'cost': [50, 100, 30]
        }
        df = pd.DataFrame(data)
        result = run_pipeline(df)
        # Expect one row to be dropped due to missing 'revenue'
        self.assertEqual(len(result), 2)
        # Verify profit calculation
        self.assertTrue('profit' in result.columns)
        self.assertEqual(result.iloc[0]['profit'], 50)

if __name__ == '__main__':
    unittest.main()
'''
    return unit_tests

def generate_inline_docs(generated_code: str) -> str:
    """
    Generate inline code documentation for the provided code.
    
    Parameters:
      generated_code (str): The generated pipeline code.
      
    Returns:
      str: The same code with added inline comments.
    """
    doc_prompt = f"Generate inline documentation for the following Python code:\n{generated_code}"
    logging.info("Simulating OpenAI call for inline documentation generation.")
    # Simulated: here we simply insert a comment before the pipeline function.
    documented_code = generated_code.replace(
        "def run_pipeline",
        "# Function to execute the data pipeline: cleans data and computes profit\n\ndef run_pipeline"
    )
    return documented_code
