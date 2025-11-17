"""
Data Cleaning Demonstration Script - Step 2

This script demonstrates all data cleaning capabilities:
- Missing value detection and handling
- Duplicate detection and removal
- Type conversion (dates, numbers)
- Data validation and outlier detection
- Text standardization
- Chained cleaning operations with DataCleaner class
"""

from pathlib import Path
import pandas as pd

from src.main import load_dataset, load_json_dataset, load_to_database
from src.cleaning import (
    detect_missing_values,
    handle_missing_values,
    detect_duplicates,
    remove_duplicates,
    convert_to_datetime,
    convert_to_numeric,
    validate_range,
    detect_outliers,
    standardize_text,
    DataCleaner
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def demonstrate_missing_values():
    """Demonstrate missing value detection and handling."""
    print_section("1. MISSING VALUE DETECTION AND HANDLING")
    
    # Load dirty data
    print("Loading dirty vaccination data...")
    df = load_dataset("data/dirty_vaccination_data.csv")
    print(f"Loaded {len(df)} records\n")
    
    # Detect missing values
    print("Detecting missing values...")
    missing_summary = detect_missing_values(df)
    print(missing_summary[missing_summary['missing_count'] > 0])
    print()
    
    # Show different handling strategies
    print("Handling strategies:")
    print("\na) Drop rows with missing values:")
    df_drop = handle_missing_values(df, strategy='drop')
    print(f"   Original rows: {len(df)}, After dropping: {len(df_drop)}")
    
    print("\nb) Fill numeric values with mean:")
    df_mean = handle_missing_values(
        df.copy(), 
        strategy='mean', 
        columns=['doses_administered', 'vaccination_rate']
    )
    print(f"   Missing values in 'vaccination_rate': {df_mean['vaccination_rate'].isna().sum()}")
    
    print("\nc) Fill with constant values:")
    df_const = handle_missing_values(
        df.copy(),
        strategy='constant',
        fill_value={'country': 'Unknown', 'year': 0}
    )
    print(f"   Missing countries filled: {(df_const['country'] == 'Unknown').sum()}")
    
    return df


def demonstrate_duplicates():
    """Demonstrate duplicate detection and removal."""
    print_section("2. DUPLICATE DETECTION AND REMOVAL")
    
    # Load dirty data
    print("Loading dirty outbreak data...")
    df = load_json_dataset("data/dirty_disease_outbreak.json")
    print(f"Loaded {len(df)} records\n")
    
    # Detect duplicates
    print("Detecting exact duplicates...")
    duplicates = detect_duplicates(df)
    print(f"Found {len(duplicates)} duplicate rows")
    if len(duplicates) > 0:
        print("\nDuplicate rows:")
        print(duplicates[['country', 'disease', 'year', 'confirmed_cases']])
    print()
    
    # Remove duplicates
    print("Removing duplicates...")
    df_clean = remove_duplicates(df)
    print(f"Original rows: {len(df)}, After removing: {len(df_clean)}")
    
    return df_clean


def demonstrate_type_conversion():
    """Demonstrate data type conversion."""
    print_section("3. DATA TYPE CONVERSION")
    
    # Load dirty data
    df = load_dataset("data/dirty_vaccination_data.csv")
    print("Original data types:")
    print(df.dtypes[['year', 'doses_administered', 'date']])
    print()
    
    # Convert year to numeric (will coerce invalid values)
    print("Converting 'year' to numeric...")
    df = convert_to_numeric(df, 'year', errors='coerce')
    print(f"Invalid years converted to NaN: {df['year'].isna().sum()}")
    print()
    
    # Convert doses_administered to numeric
    print("Converting 'doses_administered' to numeric...")
    df['doses_administered'] = df['doses_administered'].astype(str).str.strip()
    df = convert_to_numeric(df, 'doses_administered', errors='coerce')
    print(f"Data type: {df['doses_administered'].dtype}")
    print()
    
    # Convert date column
    print("Converting 'date' to datetime...")
    df = convert_to_datetime(df, 'date', errors='coerce')
    print(f"Data type: {df['date'].dtype}")
    print(f"Invalid dates converted to NaT: {df['date'].isna().sum()}")
    
    return df


def demonstrate_validation():
    """Demonstrate data validation and outlier detection."""
    print_section("4. DATA VALIDATION AND OUTLIER DETECTION")
    
    # Load outbreak data
    df = load_json_dataset("data/dirty_disease_outbreak.json")
    
    # Convert types first
    df = convert_to_numeric(df, 'confirmed_cases', errors='coerce')
    df = convert_to_numeric(df, 'deaths', errors='coerce')
    
    print("Validating data ranges...")
    print("\na) Checking for negative values in 'confirmed_cases':")
    valid_mask = validate_range(df, 'confirmed_cases', min_value=0)
    invalid_count = (~valid_mask).sum()
    print(f"   Invalid records: {invalid_count}")
    if invalid_count > 0:
        print("   Invalid rows:")
        print(df[~valid_mask][['country', 'disease', 'confirmed_cases']])
    
    print("\nb) Detecting outliers using IQR method:")
    outliers = detect_outliers(df, 'confirmed_cases', method='iqr')
    print(f"   Outliers detected: {outliers.sum()}")
    if outliers.sum() > 0:
        print("   Outlier rows:")
        print(df[outliers][['country', 'disease', 'confirmed_cases']])
    
    return df


def demonstrate_text_standardization():
    """Demonstrate text data standardization."""
    print_section("5. TEXT DATA STANDARDIZATION")
    
    # Load outbreak data
    df = load_json_dataset("data/dirty_disease_outbreak.json")
    
    print("Original country names (with spacing issues):")
    print(df['country'].unique()[:5])
    print()
    
    # Standardize country names
    print("Standardizing 'country' column...")
    df = standardize_text(df, 'country', strip=True, lowercase=False)
    print("After stripping whitespace:")
    print(df['country'].unique()[:5])
    print()
    
    # Standardize disease names
    print("Standardizing 'disease' column...")
    df = standardize_text(df, 'disease', strip=True, lowercase=True)
    print("After lowercase conversion:")
    print(df['disease'].unique())
    
    return df


def demonstrate_data_cleaner_class():
    """Demonstrate DataCleaner class with chained operations."""
    print_section("6. DATA CLEANER CLASS - CHAINED OPERATIONS")
    
    # Load dirty vaccination data
    df = load_dataset("data/dirty_vaccination_data.csv")
    
    print(f"Original data shape: {df.shape}")
    print(f"Original data types: {df.dtypes.to_dict()}")
    print()
    
    print("Applying chained cleaning operations...")
    print("1. Detect issues")
    print("2. Remove duplicates")
    print("3. Handle missing values (drop rows)")
    print("4. Convert 'year' to numeric")
    print("5. Convert 'date' to datetime")
    print("6. Standardize 'country' text")
    print("7. Filter valid vaccination rates (0-1)")
    print()
    
    # Create cleaner and chain operations
    cleaner = DataCleaner(df)
    
    # Show initial issues
    print("Initial data quality issues:")
    issues = cleaner.detect_issues()
    print(f"  - Duplicates: {issues['duplicates_count']}")
    print(f"  - Missing values in {len([col for col in issues['missing_values']['column'] if issues['missing_values'][issues['missing_values']['column'] == col]['missing_count'].values[0] > 0])} columns")
    print()
    
    # Apply chained cleaning
    cleaned_df = (cleaner
                  .remove_duplicates()
                  .handle_missing(strategy='drop')
                  .convert_column_type('year', 'numeric', errors='coerce')
                  .convert_column_type('date', 'datetime', errors='coerce')
                  .standardize_column('country', strip=True)
                  .filter_by_range('vaccination_rate', min_value=0, max_value=1)
                  .get_cleaned_data())
    
    # Generate cleaning report
    report = cleaner.get_cleaning_report()
    
    print("Cleaning report:")
    print(f"  Original rows: {report['original_rows']}")
    print(f"  Cleaned rows: {report['cleaned_rows']}")
    print(f"  Rows removed: {report['rows_removed']} ({report['rows_removed']/report['original_rows']*100:.1f}%)")
    print(f"  Operations performed: {len(report['operations'])}")
    print()
    
    print("Operations applied:")
    for i, op in enumerate(report['operations'], 1):
        print(f"  {i}. {op}")
    print()
    
    print(f"Final data shape: {cleaned_df.shape}")
    print("\nFirst few rows of cleaned data:")
    print(cleaned_df[['country', 'year', 'vaccine_type', 'vaccination_rate', 'date']].head())
    
    return cleaned_df


def save_cleaned_data(df_vaccination: pd.DataFrame, df_outbreak: pd.DataFrame):
    """Save cleaned data to database."""
    print_section("7. SAVING CLEANED DATA TO DATABASE")
    
    db_path = Path("data/health_data_cleaned.db")
    
    print(f"Saving cleaned vaccination data...")
    load_to_database(df_vaccination, db_path, "vaccinations_clean", if_exists="replace")
    print(f"[OK] Saved {len(df_vaccination)} vaccination records")
    
    print(f"\nSaving cleaned outbreak data...")
    load_to_database(df_outbreak, db_path, "outbreaks_clean", if_exists="replace")
    print(f"[OK] Saved {len(df_outbreak)} outbreak records")
    
    print(f"\n[SUCCESS] Cleaned data saved to: {db_path}")


def main():
    """Run all data cleaning demonstrations."""
    print("\n" + "="*70)
    print(" PUBLIC HEALTH DATA DASHBOARD - DATA CLEANING DEMONSTRATION")
    print(" Step 2: Data Cleaning & Structuring")
    print("="*70)
    
    # Demonstrate each capability
    demonstrate_missing_values()
    demonstrate_duplicates()
    demonstrate_type_conversion()
    demonstrate_validation()
    demonstrate_text_standardization()
    
    # Demonstrate comprehensive cleaning workflow
    cleaned_df = demonstrate_data_cleaner_class()
    
    # For the outbreak data, let's also clean it
    print_section("8. CLEANING OUTBREAK DATA WITH DATACLEANER")
    
    df_outbreak = load_json_dataset("data/dirty_disease_outbreak.json")
    print(f"Original outbreak data: {df_outbreak.shape}")
    
    cleaner_outbreak = DataCleaner(df_outbreak)
    cleaned_outbreak = (cleaner_outbreak
                       .remove_duplicates()
                       .convert_column_type('year', 'numeric', errors='coerce')
                       .convert_column_type('confirmed_cases', 'numeric', errors='coerce')
                       .convert_column_type('deaths', 'numeric', errors='coerce')
                       .handle_missing(strategy='drop')
                       .standardize_column('country', strip=True, lowercase=False)
                       .standardize_column('disease', strip=True, lowercase=True)
                       .filter_by_range('confirmed_cases', min_value=0, max_value=1000000)
                       .get_cleaned_data())
    
    report_outbreak = cleaner_outbreak.get_cleaning_report()
    print(f"\nCleaned outbreak data: {cleaned_outbreak.shape}")
    print(f"Rows removed: {report_outbreak['rows_removed']} ({report_outbreak['rows_removed']/report_outbreak['original_rows']*100:.1f}%)")
    
    # Save cleaned data
    save_cleaned_data(cleaned_df, cleaned_outbreak)
    
    # Final summary
    print_section("SUMMARY")
    print("[SUCCESS] Data cleaning demonstration completed!")
    print("\nCapabilities demonstrated:")
    print("  1. [OK] Missing value detection and handling (5 strategies)")
    print("  2. [OK] Duplicate detection and removal")
    print("  3. [OK] Type conversion (datetime, numeric)")
    print("  4. [OK] Data validation and range checking")
    print("  5. [OK] Outlier detection (IQR and Z-score methods)")
    print("  6. [OK] Text standardization")
    print("  7. [OK] Chained operations with DataCleaner class")
    print("  8. [OK] Comprehensive cleaning workflow")
    print("\nReady for Step 3: Filtering and Summary Views")
    print()


if __name__ == "__main__":
    main()

