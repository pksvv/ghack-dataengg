# Generative AI-Driven Data Engineering Agent

## Overview

This project demonstrates a generative AI-driven solution to automate the creation of data engineering pipelines directly from natural language descriptions. Leveraging FastAPI, LangChain (simulated), and several evaluation metrics, the agent performs the following tasks:

- **Natural Language Processing:** Interprets a plain language input to generate a full data pipeline solution.
- **Design Documentation:** Automatically generates comprehensive design documentation outlining the architecture and workflow.
- **Pipeline Code Generation:** Produces production-ready Python code to implement the data pipeline.
- **Inline Code Documentation:** Generates detailed inline comments within the produced code for improved maintainability.
- **Unit Test Generation:** Creates unit tests to verify the correctness and robustness of the generated pipeline.
- **Synthetic Dataset Generation:** Produces a large, synthetic dataset with simulated data quality issues for testing.
- **Pipeline Execution & Evaluation:** Executes the pipeline on the synthetic data and evaluates the generated code using various metrics including Pass@k, CodeBLEU, CodeBERTScore, CodeScore, and Halstead Complexity Measures.

## Project Structure

The project is organized as follows:

generative_data_pipeline/
├── app/
│   ├── __init__.py # Package initialization
│   ├── main.py # FastAPI application entrypoint
│   ├── langchain_utils.py # Simulated LangChain utility functions for artifact generation
│   ├── pipeline.py # Data pipeline implementation with logging and performance evaluation
│   ├── sample_data_generator.py # Module to generate a synthetic dataset with data quality issues
│   └── eval.py # Evaluation metrics for generated code (Pass@k, CodeBLEU, etc.)
└── requirements.txt # Project dependencies

## Features

- **Generative Artifacts:** Uses simulated LangChain calls to generate:
  - Design documentation
  - Production-ready pipeline code
  - Inline code documentation
  - Unit tests for the pipeline
- **Data Pipeline Execution:** Cleans and transforms a large synthetic dataset (e.g., dropping rows with missing values, computing a `profit` column).
- **Evaluation Metrics:** Evaluates generated code using multiple metrics:
  - **Pass@k:** Checks for exact code match among top generated outputs.
  - **CodeBLEU:** Uses an approximation via NLTK's BLEU score.
  - **CodeBERTScore:** Simulates semantic similarity evaluation.
  - **CodeScore:** Computes token overlap between generated and reference code.
  - **Halstead Complexity:** Quantifies code complexity based on operators and operands.
- **Extensive Logging:** Detailed logging for each step to ease debugging and ensure transparency.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd generative_data_pipeline

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. **Running the Application**

   ```bash
   Start the FastAPI server:
   uvicorn app.main\:app --reload

4. **The server will run at http://127.0.0.1:8000.**

5. **Access the API Documentation:**

6. **Open your browser and navigate to:**
   ```bash
   http://127.0.0.1:8000/docs

7. **Test the /generate_pipeline Endpoint:**

8. **Use the interactive Swagger UI** to send a POST request with the following JSON payload:

   ```bash
   {
    "natural_language_input": "I need a data pipeline that ingests raw CSV data, removes records with missing revenue or cost, computes profit as revenue minus cost, logs data quality metrics, and evaluates performance."
    }

9. **The response will include:**


- Generated design documentation
- Production-ready pipeline code
- Inline code documentation
- Generated unit tests
- Pipeline execution results (on a synthetic dataset)
- Evaluation metrics
    Code Quality & Evaluation
- Evaluation Metrics: The app/eval.py module implements metrics to assess the generated code quality. This includes:
    Pass@k: Checking for an exact match with a reference code snippet.
    CodeBLEU & CodeBERTScore: Evaluating similarity.CodeScore: Token overlap-based heuristic.
    Halstead Complexity: Measuring code complexity.
    Logging: The pipeline and data generation steps log important information (e.g., record counts, performance metrics) to help with monitoring and debugging.
