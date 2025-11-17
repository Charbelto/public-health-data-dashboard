"""
Data Loader Module - Demonstration of Step 1: Data Access & Loading

This module demonstrates loading data from various sources:
- CSV files
- JSON files
- Public APIs (with mocked example)
- Database operations

This is a practical demonstration for the public health data dashboard.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from src.main import (
    load_dataset,
    load_json_dataset,
    load_to_database,
    read_from_database
)


class DataLoader:
    """
    Main data loader class for the public health dashboard.
    
    This class provides methods to load data from various sources
    and store them in a local SQLite database for further analysis.
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize the DataLoader.
        
        Parameters
        ----------
        db_path : Path, optional
            Path to the SQLite database. Defaults to 'data/health_data.db'
        """
        if db_path is None:
            db_path = Path("data/health_data.db")
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load_vaccination_data(self, csv_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Load vaccination data from CSV file.
        
        Parameters
        ----------
        csv_path : Path, optional
            Path to vaccination CSV file. Defaults to sample data.
        
        Returns
        -------
        pd.DataFrame
            Vaccination data as DataFrame
        """
        if csv_path is None:
            csv_path = Path("data/sample_vaccination_data.csv")
        
        print(f"Loading vaccination data from {csv_path}...")
        df = load_dataset(csv_path)
        print(f"[OK] Loaded {len(df)} vaccination records")
        
        # Store in database
        load_to_database(df, self.db_path, "vaccinations", if_exists="replace")
        print(f"[OK] Stored vaccination data in database: {self.db_path}")
        
        return df
    
    def load_outbreak_data(self, json_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Load disease outbreak data from JSON file.
        
        Parameters
        ----------
        json_path : Path, optional
            Path to outbreak JSON file. Defaults to sample data.
        
        Returns
        -------
        pd.DataFrame
            Outbreak data as DataFrame
        """
        if json_path is None:
            json_path = Path("data/sample_disease_outbreak.json")
        
        print(f"Loading outbreak data from {json_path}...")
        df = load_json_dataset(json_path)
        print(f"[OK] Loaded {len(df)} outbreak records")
        
        # Store in database
        load_to_database(df, self.db_path, "outbreaks", if_exists="replace")
        print(f"[OK] Stored outbreak data in database: {self.db_path}")
        
        return df
    
    def get_data_from_db(self, table_name: str, 
                         query: Optional[str] = None) -> pd.DataFrame:
        """
        Retrieve data from the database.
        
        Parameters
        ----------
        table_name : str
            Name of the table to query
        query : str, optional
            SQL query to execute. If None, returns all data.
        
        Returns
        -------
        pd.DataFrame
            Queried data
        """
        print(f"Retrieving data from table: {table_name}")
        df = read_from_database(self.db_path, table_name, query)
        print(f"[OK] Retrieved {len(df)} records")
        return df
    
    def display_summary(self):
        """
        Display a summary of all data loaded in the database.
        """
        from sqlalchemy import create_engine, inspect
        
        engine = create_engine(f'sqlite:///{self.db_path}')
        inspector = inspect(engine)
        
        print("\n" + "="*60)
        print("DATABASE SUMMARY")
        print("="*60)
        print(f"Database: {self.db_path}")
        print(f"\nTables:")
        
        for table_name in inspector.get_table_names():
            df = read_from_database(self.db_path, table_name)
            print(f"  - {table_name}: {len(df)} records, {len(df.columns)} columns")
            print(f"    Columns: {', '.join(df.columns)}")
        
        print("="*60 + "\n")


def main():
    """
    Demonstration of data loading functionality.
    """
    print("\n" + "="*60)
    print("PUBLIC HEALTH DATA DASHBOARD - DATA LOADING DEMONSTRATION")
    print("="*60 + "\n")
    
    # Initialize data loader
    loader = DataLoader()
    
    # Load vaccination data from CSV
    print("Step 1: Loading vaccination data from CSV...")
    vaccination_df = loader.load_vaccination_data()
    print(f"\nFirst few vaccination records:")
    print(vaccination_df.head(3))
    print()
    
    # Load outbreak data from JSON
    print("\n" + "-"*60)
    print("Step 2: Loading outbreak data from JSON...")
    outbreak_df = loader.load_outbreak_data()
    print(f"\nFirst few outbreak records:")
    print(outbreak_df.head(3))
    print()
    
    # Demonstrate database query
    print("\n" + "-"*60)
    print("Step 3: Querying data from database...")
    uk_vaccinations = loader.get_data_from_db(
        "vaccinations",
        query="SELECT * FROM vaccinations WHERE country = 'United Kingdom'"
    )
    print(f"\nUK Vaccination Records:")
    print(uk_vaccinations)
    print()
    
    # Display summary
    loader.display_summary()
    
    print("[SUCCESS] Data loading demonstration completed successfully!")
    print("\nAll data sources have been:")
    print("  1. [OK] Loaded from CSV files")
    print("  2. [OK] Loaded from JSON files")
    print("  3. [OK] Stored in SQLite database")
    print("  4. [OK] Retrieved and queried from database")
    print("\nReady for Step 2: Data Cleaning & Structuring")


if __name__ == "__main__":
    main()

