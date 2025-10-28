from typing import List, Dict, Any
import pandas as pd

def process_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Process input data for the Sankey diagram.

    Args:
        data (List[Dict[str, Any]]): Input data containing nodes and edges.

    Returns:
        pd.DataFrame: Processed DataFrame ready for visualization.
    """
    df = pd.DataFrame(data)
    # Additional processing logic can be added here
    return df

def filter_data(df: pd.DataFrame, filter_criteria: Dict[str, Any]) -> pd.DataFrame:
    """
    Filter the DataFrame based on user-defined criteria.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        filter_criteria (Dict[str, Any]): Criteria for filtering.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    for key, value in filter_criteria.items():
        df = df[df[key] == value]
    return df

def adjust_metrics(df: pd.DataFrame, metric_column: str, adjustment_factor: float) -> pd.DataFrame:
    """
    Adjust metrics for node sizes or edge distributions.

    Args:
        df (pd.DataFrame): The DataFrame containing metrics.
        metric_column (str): The column to adjust.
        adjustment_factor (float): Factor by which to adjust the metrics.

    Returns:
        pd.DataFrame: DataFrame with adjusted metrics.
    """
    df[metric_column] *= adjustment_factor
    return df