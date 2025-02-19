# app/pipeline.py
"""
Data Pipeline Module

This module implements a complete data engineering pipeline that:
  1. Logs initial record counts.
  2. Evaluates data quality (e.g., missing values).
  3. Cleans data by dropping rows with missing critical columns.
  4. Transforms data by computing a new 'profit' column.
  5. Measures performance (elapsed time, throughput).
  6. Persists evaluation metrics and transformation logs.
  
Extensive logging and inline comments are provided for clarity.
"""

import pandas as pd
import time
import logging
import os
import json
import numpy as np  # Needed for JSON conversion in persist_pipeline_results

# Global transformation log to keep track of operations
transformation_log = []

def log_transformation(message: str):
    """
    Append a transformation message to the global log and log the operation.
    """
    transformation_log.append(message)
    logging.info(message)

def log_data_quality_metrics(df: pd.DataFrame, columns: list) -> dict:
    """
    Log data quality metrics (e.g., count of missing values) for specified columns.
    
    Parameters:
      df (pd.DataFrame): The input DataFrame.
      columns (list): List of columns to check for missing values.
      
    Returns:
      dict: A mapping of column names to their missing values count.
    """
    metrics = {}
    for col in columns:
        missing = int(df[col].isna().sum())  # Convert to native int
        metrics[col] = missing
        logging.info(f"Column '{col}' has {missing} missing values.")
    return metrics

def log_pipeline_performance(elapsed_time: float, record_count: int) -> float:
    """
    Calculate and log the throughput of the pipeline.
    
    Parameters:
      elapsed_time (float): Time taken to process the data.
      record_count (int): Number of records processed.
      
    Returns:
      float: Records processed per second.
    """
    throughput = record_count / elapsed_time if elapsed_time > 0 else 0
    logging.info(f"Processed {record_count} records in {elapsed_time:.2f} seconds ({throughput:.2f} records/sec).")
    return throughput

def persist_pipeline_results(results: dict):
    """
    Persist pipeline results and logs to disk.
    
    Creates:
      - logs/evaluation_metrics.json: JSON file with evaluation metrics.
      - logs/transformation_log.txt: Text file with the transformation log.
      
    Uses a default function to convert non-serializable objects (e.g., np.int64) to serializable types.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/evaluation_metrics.json", "w") as f:
        json.dump(
            results,
            f,
            indent=2,
            default=lambda x: int(x) if isinstance(x, (np.int64, np.int32)) else str(x)
        )
    with open("logs/transformation_log.txt", "w") as f:
        for entry in results.get("transformation_log", []):
            f.write(entry + "\n")
    logging.info("Persisted pipeline results in the 'logs' directory.")

def run_pipeline(input_df: pd.DataFrame) -> dict:
    """
    Execute the complete data pipeline:
      1. Log the initial number of records.
      2. Log data quality metrics for key columns.
      3. Clean the data by dropping rows with missing 'revenue' or 'cost'.
      4. Transform the data by computing the 'profit' column.
      5. Measure performance (elapsed time, throughput).
      6. Persist and return evaluation results.
      
    Parameters:
      input_df (pd.DataFrame): The input dataset.
      
    Returns:
      dict: A summary of pipeline execution metrics and logs.
    """
    start_time = time.time()
    initial_count = int(len(input_df))  # Convert to native int
    logging.info(f"Initial record count: {initial_count}")
    
    # Evaluate and log data quality before cleaning
    pre_clean_metrics = log_data_quality_metrics(input_df, ['revenue', 'cost'])
    log_transformation("Logged pre-cleaning data quality metrics.")
    
    # Clean the data (drop rows with missing critical values)
    df_clean = input_df.dropna(subset=['revenue', 'cost']).copy()  # .copy() to avoid SettingWithCopyWarning
    clean_count = int(len(df_clean))  # Convert to native int
    logging.info(f"Record count after cleaning: {clean_count}")
    log_transformation("Dropped rows with missing 'revenue' or 'cost'.")
    
    # Data transformation: calculate 'profit'
    df_clean['profit'] = df_clean['revenue'] - df_clean['cost']
    log_transformation("Computed 'profit' as revenue minus cost.")
    
    # Measure performance
    elapsed_time = time.time() - start_time
    throughput = log_pipeline_performance(elapsed_time, initial_count)
    
    # Aggregate all results
    results = {
        "initial_count": initial_count,
        "clean_count": clean_count,
        "elapsed_time_sec": elapsed_time,
        "throughput_records_per_sec": throughput,
        "data_quality_pre_clean": pre_clean_metrics,
        "transformation_log": transformation_log
    }
    
    # Persist results to disk
    persist_pipeline_results(results)
    return results
