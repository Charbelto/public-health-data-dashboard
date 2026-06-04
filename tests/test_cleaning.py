"""
Tests for data cleaning and structuring module.

Following TDD, these tests are written before implementation.
Step 2: Data Cleaning & Structuring
"""

from pathlib import Path
import pandas as pd
import pytest
import numpy as np
from datetime import datetime

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


# ==============================================================================
# Tests for Missing Value Detection and Handling
# ==============================================================================

def test_detect_missing_values_returns_summary() -> None:
    """
    Test that detect_missing_values returns a summary of missing data.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', None, 'France'],
        'cases': [100, None, 300, 400],
        'year': [2020, 2021, 2022, 2023]
    })
    
    summary = detect_missing_values(df)
    
    assert isinstance(summary, pd.DataFrame)
    assert 'column' in summary.columns
    assert 'missing_count' in summary.columns
    assert 'missing_percentage' in summary.columns
    assert summary.loc[summary['column'] == 'country', 'missing_count'].values[0] == 1
    assert summary.loc[summary['column'] == 'cases', 'missing_count'].values[0] == 1


def test_detect_missing_values_empty_dataframe() -> None:
    """
    Test that detect_missing_values handles empty DataFrame.
    """
    df = pd.DataFrame()
    summary = detect_missing_values(df)
    assert len(summary) == 0


def test_handle_missing_values_drop_rows() -> None:
    """
    Test dropping rows with missing values.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', None, 'France'],
        'cases': [100, 200, 300, 400]
    })
    
    result = handle_missing_values(df, strategy='drop')
    
    assert len(result) == 3
    assert result['country'].isna().sum() == 0


def test_handle_missing_values_fill_mean() -> None:
    """
    Test filling missing numeric values with mean.
    """
    df = pd.DataFrame({
        'cases': [100, 200, None, 400]
    })
    
    result = handle_missing_values(df, strategy='mean', columns=['cases'])
    
    assert result['cases'].isna().sum() == 0
    assert result['cases'].iloc[2] == 233.33333333333334  # mean of 100, 200, 400


def test_handle_missing_values_fill_median() -> None:
    """
    Test filling missing numeric values with median.
    """
    df = pd.DataFrame({
        'cases': [100, 200, None, 400]
    })
    
    result = handle_missing_values(df, strategy='median', columns=['cases'])
    
    assert result['cases'].isna().sum() == 0
    assert result['cases'].iloc[2] == 200.0  # median of 100, 200, 400


def test_handle_missing_values_fill_constant() -> None:
    """
    Test filling missing values with a constant.
    """
    df = pd.DataFrame({
        'country': ['UK', None, 'France'],
        'cases': [100, None, 300]
    })
    
    result = handle_missing_values(
        df, 
        strategy='constant', 
        fill_value={'country': 'Unknown', 'cases': 0}
    )
    
    assert result['country'].iloc[1] == 'Unknown'
    assert result['cases'].iloc[1] == 0


def test_handle_missing_values_forward_fill() -> None:
    """
    Test forward fill strategy for time series data.
    """
    df = pd.DataFrame({
        'date': ['2020-01', '2020-02', '2020-03', '2020-04'],
        'cases': [100, None, None, 400]
    })
    
    result = handle_missing_values(df, strategy='ffill')
    
    assert result['cases'].iloc[1] == 100
    assert result['cases'].iloc[2] == 100


# ==============================================================================
# Tests for Duplicate Detection and Removal
# ==============================================================================

def test_detect_duplicates_returns_summary() -> None:
    """
    Test that detect_duplicates identifies duplicate rows.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'France'],
        'year': [2020, 2021, 2020, 2022],
        'cases': [100, 200, 100, 300]
    })
    
    duplicates = detect_duplicates(df)
    
    assert len(duplicates) == 1  # One duplicate row
    assert duplicates['country'].iloc[0] == 'UK'


def test_detect_duplicates_subset_columns() -> None:
    """
    Test duplicate detection on subset of columns.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK'],
        'year': [2020, 2021, 2021],
        'cases': [100, 200, 150]
    })
    
    duplicates = detect_duplicates(df, subset=['country'])
    
    assert len(duplicates) == 1  # UK appears twice


def test_remove_duplicates_keeps_first() -> None:
    """
    Test removing duplicates keeps the first occurrence.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'France'],
        'year': [2020, 2021, 2020, 2022],
        'cases': [100, 200, 100, 300]
    })
    
    result = remove_duplicates(df, keep='first')
    
    assert len(result) == 3
    assert result['country'].tolist() == ['UK', 'USA', 'France']


def test_remove_duplicates_keeps_last() -> None:
    """
    Test removing duplicates keeps the last occurrence.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK'],
        'year': [2020, 2021, 2022],
        'cases': [100, 200, 300]
    })
    
    result = remove_duplicates(df, subset=['country'], keep='last')
    
    assert len(result) == 2
    assert result[result['country'] == 'UK']['year'].values[0] == 2022


# ==============================================================================
# Tests for Type Conversion
# ==============================================================================

def test_convert_to_datetime_from_string() -> None:
    """
    Test converting string columns to datetime.
    """
    df = pd.DataFrame({
        'date': ['2020-01-01', '2020-02-01', '2020-03-01']
    })
    
    result = convert_to_datetime(df, 'date')
    
    assert pd.api.types.is_datetime64_any_dtype(result['date'])
    assert result['date'].iloc[0] == pd.Timestamp('2020-01-01')


def test_convert_to_datetime_multiple_formats() -> None:
    """
    Test datetime conversion with specified format.
    """
    df = pd.DataFrame({
        'date': ['01/01/2020', '02/01/2020', '03/01/2020']
    })
    
    result = convert_to_datetime(df, 'date', format='%d/%m/%Y')
    
    assert pd.api.types.is_datetime64_any_dtype(result['date'])
    assert result['date'].iloc[0].day == 1
    assert result['date'].iloc[0].month == 1


def test_convert_to_datetime_handles_errors() -> None:
    """
    Test datetime conversion with invalid dates.
    """
    df = pd.DataFrame({
        'date': ['2020-01-01', 'invalid', '2020-03-01']
    })
    
    result = convert_to_datetime(df, 'date', errors='coerce')
    
    assert pd.isna(result['date'].iloc[1])
    assert pd.api.types.is_datetime64_any_dtype(result['date'])


def test_convert_to_numeric_from_string() -> None:
    """
    Test converting string numbers to numeric.
    """
    df = pd.DataFrame({
        'cases': ['100', '200', '300']
    })
    
    result = convert_to_numeric(df, 'cases')
    
    assert pd.api.types.is_numeric_dtype(result['cases'])
    assert result['cases'].iloc[0] == 100


def test_convert_to_numeric_handles_errors() -> None:
    """
    Test numeric conversion with invalid values.
    """
    df = pd.DataFrame({
        'cases': ['100', 'invalid', '300']
    })
    
    result = convert_to_numeric(df, 'cases', errors='coerce')
    
    assert pd.isna(result['cases'].iloc[1])
    assert result['cases'].iloc[0] == 100
    assert result['cases'].iloc[2] == 300


def test_convert_to_numeric_with_comma_separator() -> None:
    """
    Test numeric conversion with comma thousands separator.
    """
    df = pd.DataFrame({
        'cases': ['1,000', '2,500', '3,750']
    })
    
    # First remove commas
    df['cases'] = df['cases'].str.replace(',', '')
    result = convert_to_numeric(df, 'cases')
    
    assert result['cases'].iloc[0] == 1000
    assert result['cases'].iloc[1] == 2500


# ==============================================================================
# Tests for Data Validation
# ==============================================================================

def test_validate_range_returns_valid_mask() -> None:
    """
    Test that validate_range identifies values outside specified range.
    """
    df = pd.DataFrame({
        'cases': [100, -50, 300, 1000000]
    })
    
    valid_mask = validate_range(df, 'cases', min_value=0, max_value=100000)
    
    assert valid_mask[0] == True
    assert valid_mask[1] == False  # negative
    assert valid_mask[2] == True
    assert valid_mask[3] == False  # too large


def test_validate_range_min_only() -> None:
    """
    Test validation with only minimum value.
    """
    df = pd.DataFrame({
        'year': [2018, 2019, 2020, 2021]
    })
    
    valid_mask = validate_range(df, 'year', min_value=2019)
    
    assert valid_mask[0] == False
    assert all(valid_mask[1:])


def test_validate_range_max_only() -> None:
    """
    Test validation with only maximum value.
    """
    df = pd.DataFrame({
        'age': [10, 25, 50, 75, 100, 150]
    })
    
    valid_mask = validate_range(df, 'age', max_value=100)
    
    assert all(valid_mask.iloc[:-1])
    assert valid_mask.iloc[-1] == False


def test_detect_outliers_iqr_method() -> None:
    """
    Test outlier detection using IQR method.
    """
    df = pd.DataFrame({
        'cases': [100, 105, 110, 115, 120, 1000]  # 1000 is an outlier
    })
    
    outlier_mask = detect_outliers(df, 'cases', method='iqr')
    
    assert outlier_mask.iloc[-1] == True  # Last value is outlier
    assert not any(outlier_mask.iloc[:-1])  # Others are not


def test_detect_outliers_zscore_method() -> None:
    """
    Test outlier detection using z-score method.
    """
    df = pd.DataFrame({
        'cases': [100, 102, 98, 105, 95, 500]  # 500 is an outlier
    })
    
    outlier_mask = detect_outliers(df, 'cases', method='zscore', threshold=2)
    
    assert outlier_mask.iloc[-1] == True


# ==============================================================================
# Tests for Text Standardization
# ==============================================================================

def test_standardize_text_lowercase() -> None:
    """
    Test converting text to lowercase.
    """
    df = pd.DataFrame({
        'country': ['United Kingdom', 'UNITED STATES', 'FrAnCe']
    })
    
    result = standardize_text(df, 'country', lowercase=True)
    
    assert result['country'].iloc[0] == 'united kingdom'
    assert result['country'].iloc[1] == 'united states'


def test_standardize_text_strip_whitespace() -> None:
    """
    Test removing leading/trailing whitespace.
    """
    df = pd.DataFrame({
        'country': ['  UK  ', ' USA', 'France  ']
    })
    
    result = standardize_text(df, 'country', strip=True)
    
    assert result['country'].iloc[0] == 'UK'
    assert result['country'].iloc[1] == 'USA'


def test_standardize_text_remove_special_chars() -> None:
    """
    Test removing special characters.
    """
    df = pd.DataFrame({
        'disease': ['COVID-19', 'H1N1 (Swine Flu)', 'Influenza A/B']
    })
    
    result = standardize_text(df, 'disease', remove_special=True)
    
    assert '-' not in result['disease'].iloc[0]
    assert '(' not in result['disease'].iloc[1]


# ==============================================================================
# Tests for DataCleaner Class
# ==============================================================================

def test_data_cleaner_initialization() -> None:
    """
    Test DataCleaner initialization with a DataFrame.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA'],
        'cases': [100, 200]
    })
    
    cleaner = DataCleaner(df)
    
    assert cleaner is not None
    assert len(cleaner.df) == 2


def test_data_cleaner_chain_operations() -> None:
    """
    Test chaining multiple cleaning operations.
    """
    df = pd.DataFrame({
        'country': ['UK', None, 'UK', 'France'],
        'cases': [100, 200, 100, 300],
        'year': ['2020', '2021', '2020', '2022']
    })
    
    cleaner = DataCleaner(df)
    result = (cleaner
              .handle_missing(strategy='drop')
              .remove_duplicates()
              .convert_column_type('year', 'numeric')
              .get_cleaned_data())
    
    assert len(result) == 2  # After dropping missing and duplicates
    assert pd.api.types.is_numeric_dtype(result['year'])


def test_data_cleaner_get_cleaning_report() -> None:
    """
    Test that DataCleaner generates a cleaning report.
    """
    df = pd.DataFrame({
        'country': ['UK', None, 'UK'],
        'cases': [100, 200, 100]
    })
    
    cleaner = DataCleaner(df)
    cleaner.handle_missing(strategy='drop')
    
    report = cleaner.get_cleaning_report()
    
    assert 'original_rows' in report
    assert 'cleaned_rows' in report
    assert 'rows_removed' in report
    assert report['original_rows'] == 3
    assert report['cleaned_rows'] == 2

