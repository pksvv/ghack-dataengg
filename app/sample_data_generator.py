# app/sample_data_generator.py
"""
Synthetic Data Generator

This module generates a large synthetic dataset with several columns (e.g., id, revenue, cost, etc.)
and introduces data quality issues (e.g., missing values) to simulate real-world conditions.
"""

import pandas as pd
import numpy as np
import logging

def log_transformation(message: str):
    """
    Dummy logging function for data generation.
    """
    logging.info(message)

def generate_large_dataset(num_records: int = 1_000_000) -> pd.DataFrame:
    """
    Generate a synthetic dataset with specified number of records.
    
    The dataset includes columns:
      - id: Unique identifier.
      - revenue: Simulated revenue (with ~1% missing values).
      - cost: Simulated cost.
      - customer_age: Age of customer.
      - purchase_amount: Purchase amount.
      - region: Categorical region (North, South, East, West).
    
    Parameters:
      num_records (int): Number of records to generate.
      
    Returns:
      pd.DataFrame: The generated dataset.
    """
    np.random.seed(42)
    data = {
        'id': np.arange(num_records),
        'revenue': np.random.randint(100, 10000, size=num_records),
        'cost': np.random.randint(50, 5000, size=num_records),
        'customer_age': np.random.randint(18, 90, size=num_records),
        'purchase_amount': np.random.randint(10, 1000, size=num_records),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=num_records)
    }
    df = pd.DataFrame(data)
    # Introduce ~1% missing values in 'revenue'
    mask = np.random.rand(num_records) < 0.01
    df.loc[mask, 'revenue'] = None
    log_transformation(f"Generated synthetic dataset with {num_records} records.")
    return df
