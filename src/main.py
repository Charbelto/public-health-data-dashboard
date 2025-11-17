"""
Entry point for the Public Health Data Insights Dashboard (Task 1).

Step 1: Data Access & Loading - Load data from CSV, JSON, and APIs.
"""

import json
from pathlib import Path
from typing import Union, Optional
import pandas as pd
import requests
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine


def load_dataset(path: Union[str, Path]) -> pd.DataFrame:
    """
    Load a public health dataset from a CSV file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the loaded data.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file cannot be parsed as CSV.
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")


def load_json_dataset(path: Union[str, Path]) -> pd.DataFrame:
    """
    Load a public health dataset from a JSON file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the JSON file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the loaded data.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file cannot be parsed as JSON.
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")


def load_from_api(url: str, params: Optional[dict] = None, 
                  data_key: Optional[str] = None) -> pd.DataFrame:
    """
    Load public health data from a public API.

    Parameters
    ----------
    url : str
        API endpoint URL.
    params : dict, optional
        Query parameters for the API request.
    data_key : str, optional
        Key to extract data from nested JSON response.
        If None, assumes the response is directly convertible to DataFrame.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the loaded data.

    Raises
    ------
    requests.RequestException
        If the API request fails.
    ValueError
        If the response cannot be converted to a DataFrame.
    """
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract nested data if data_key is provided
        if data_key:
            data = data.get(data_key, data)
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            # Try to find a list in the dict
            for value in data.values():
                if isinstance(value, list):
                    df = pd.DataFrame(value)
                    break
            else:
                # If no list found, create DataFrame from dict
                df = pd.DataFrame([data])
        else:
            raise ValueError("Unexpected data format from API")
        
        return df
    
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}")
    except Exception as e:
        raise ValueError(f"Error processing API response: {e}")


def load_to_database(df: pd.DataFrame, db_path: Union[str, Path], 
                    table_name: str, if_exists: str = 'replace') -> Engine:
    """
    Load a DataFrame into a SQLite database.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to load into the database.
    db_path : str or pathlib.Path
        Path to the SQLite database file.
    table_name : str
        Name of the table to create/update.
    if_exists : str, default 'replace'
        How to behave if the table exists: 'fail', 'replace', or 'append'.

    Returns
    -------
    sqlalchemy.engine.Engine
        Database engine for further operations.

    Raises
    ------
    ValueError
        If the DataFrame is empty or table_name is invalid.
    """
    if df.empty:
        raise ValueError("Cannot load empty DataFrame to database")
    
    if not table_name or not isinstance(table_name, str):
        raise ValueError("Invalid table name")
    
    # Create database engine
    db_path = Path(db_path)
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Load data to database
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    
    return engine


def read_from_database(db_path: Union[str, Path], 
                       table_name: str,
                       query: Optional[str] = None) -> pd.DataFrame:
    """
    Read data from a SQLite database table.

    Parameters
    ----------
    db_path : str or pathlib.Path
        Path to the SQLite database file.
    table_name : str
        Name of the table to read from.
    query : str, optional
        SQL query to execute. If None, reads entire table.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the data from the database.

    Raises
    ------
    FileNotFoundError
        If the database file does not exist.
    ValueError
        If the table does not exist or query is invalid.
    """
    db_path = Path(db_path)
    
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Check if table exists
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table '{table_name}' does not exist in database")
    
    # Read data
    if query:
        df = pd.read_sql_query(query, engine)
    else:
        df = pd.read_sql_table(table_name, engine)
    
    return df


def main() -> None:
    """
    Placeholder CLI entry point.

    In later steps this will:
    - Load data
    - Ask the user for filters
    - Display tables and charts
    """
    print("Public Health Data Insights Dashboard (stub)")
    # Implementation will be added in later commits.


if __name__ == "__main__":
    main()
