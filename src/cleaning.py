"""
Data Cleaning and Structuring Module - Step 2

This module provides functions for cleaning and structuring public health data:
- Handle missing values (detection, imputation, removal)
- Convert data types (dates, numbers, categories)
- Detect and remove duplicates
- Validate data ranges
- Detect outliers
- Standardize text data
"""

from typing import Union, Optional, Dict, List, Any
import pandas as pd
import numpy as np
from scipy import stats


def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and summarize missing values in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to analyze

    Returns
    -------
    pd.DataFrame
        Summary with columns: column, missing_count, missing_percentage
    """
    if df.empty:
        return pd.DataFrame(columns=['column', 'missing_count', 'missing_percentage'])
    
    missing_data = []
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        missing_data.append({
            'column': col,
            'missing_count': missing_count,
            'missing_percentage': round(missing_pct, 2)
        })
    
    return pd.DataFrame(missing_data)


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = 'drop',
    columns: Optional[List[str]] = None,
    fill_value: Optional[Union[Any, Dict[str, Any]]] = None
) -> pd.DataFrame:
    """
    Handle missing values using various strategies.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with missing values
    strategy : str
        Strategy to handle missing values:
        - 'drop': Remove rows with missing values
        - 'mean': Fill with column mean (numeric only)
        - 'median': Fill with column median (numeric only)
        - 'mode': Fill with column mode
        - 'constant': Fill with specified constant value
        - 'ffill': Forward fill (propagate last valid value)
        - 'bfill': Backward fill (propagate next valid value)
    columns : list of str, optional
        Specific columns to apply strategy. If None, applies to all columns.
    fill_value : any or dict, optional
        Value(s) to use for 'constant' strategy

    Returns
    -------
    pd.DataFrame
        DataFrame with missing values handled
    """
    df_copy = df.copy()
    
    if columns is None:
        columns = df_copy.columns.tolist()
    
    if strategy == 'drop':
        df_copy = df_copy.dropna(subset=columns)
    
    elif strategy == 'mean':
        for col in columns:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
    
    elif strategy == 'median':
        for col in columns:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    
    elif strategy == 'mode':
        for col in columns:
            mode_val = df_copy[col].mode()
            if len(mode_val) > 0:
                df_copy[col] = df_copy[col].fillna(mode_val[0])
    
    elif strategy == 'constant':
        if isinstance(fill_value, dict):
            for col, val in fill_value.items():
                if col in columns:
                    df_copy[col] = df_copy[col].fillna(val)
        else:
            for col in columns:
                df_copy[col] = df_copy[col].fillna(fill_value)
    
    elif strategy == 'ffill':
        df_copy[columns] = df_copy[columns].ffill()
    
    elif strategy == 'bfill':
        df_copy[columns] = df_copy[columns].bfill()
    
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    return df_copy


def detect_duplicates(
    df: pd.DataFrame,
    subset: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Detect duplicate rows in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to check for duplicates
    subset : list of str, optional
        Columns to consider for identifying duplicates.
        If None, uses all columns.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only the duplicate rows
    """
    if subset is None:
        duplicates_mask = df.duplicated(keep=False)
    else:
        duplicates_mask = df.duplicated(subset=subset, keep=False)
    
    # Return duplicates, excluding the first occurrence
    return df[df.duplicated(subset=subset, keep='first')]


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[List[str]] = None,
    keep: str = 'first'
) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to remove duplicates from
    subset : list of str, optional
        Columns to consider for identifying duplicates.
        If None, uses all columns.
    keep : str, default 'first'
        Which duplicate to keep: 'first', 'last', or False (drop all)

    Returns
    -------
    pd.DataFrame
        DataFrame with duplicates removed
    """
    return df.drop_duplicates(subset=subset, keep=keep)


def convert_to_datetime(
    df: pd.DataFrame,
    column: str,
    format: Optional[str] = None,
    errors: str = 'raise'
) -> pd.DataFrame:
    """
    Convert a column to datetime type.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column
    column : str
        Name of column to convert
    format : str, optional
        Datetime format string (e.g., '%Y-%m-%d')
    errors : str, default 'raise'
        How to handle parsing errors: 'raise', 'coerce', or 'ignore'

    Returns
    -------
    pd.DataFrame
        DataFrame with converted column
    """
    df_copy = df.copy()
    df_copy[column] = pd.to_datetime(df_copy[column], format=format, errors=errors)
    return df_copy


def convert_to_numeric(
    df: pd.DataFrame,
    column: str,
    errors: str = 'raise'
) -> pd.DataFrame:
    """
    Convert a column to numeric type.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column
    column : str
        Name of column to convert
    errors : str, default 'raise'
        How to handle conversion errors: 'raise', 'coerce', or 'ignore'

    Returns
    -------
    pd.DataFrame
        DataFrame with converted column
    """
    df_copy = df.copy()
    df_copy[column] = pd.to_numeric(df_copy[column], errors=errors)
    return df_copy


def validate_range(
    df: pd.DataFrame,
    column: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> pd.Series:
    """
    Validate that values in a column fall within a specified range.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column
    column : str
        Name of column to validate
    min_value : float, optional
        Minimum acceptable value
    max_value : float, optional
        Maximum acceptable value

    Returns
    -------
    pd.Series
        Boolean series indicating which values are valid
    """
    valid_mask = pd.Series([True] * len(df), index=df.index)
    
    if min_value is not None:
        valid_mask &= (df[column] >= min_value)
    
    if max_value is not None:
        valid_mask &= (df[column] <= max_value)
    
    return valid_mask


def detect_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr',
    threshold: float = 1.5
) -> pd.Series:
    """
    Detect outliers in a numeric column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column
    column : str
        Name of column to analyze
    method : str, default 'iqr'
        Method for outlier detection:
        - 'iqr': Interquartile range method
        - 'zscore': Z-score method
    threshold : float, default 1.5
        Threshold for outlier detection:
        - For IQR: multiplier for IQR (typically 1.5)
        - For z-score: number of standard deviations (typically 3)

    Returns
    -------
    pd.Series
        Boolean series indicating which values are outliers
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    
    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        # Create a series with the same index as df
        outliers = pd.Series(False, index=df.index)
        outliers.loc[df[column].notna()] = z_scores > threshold
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return outliers


def standardize_text(
    df: pd.DataFrame,
    column: str,
    lowercase: bool = False,
    strip: bool = True,
    remove_special: bool = False
) -> pd.DataFrame:
    """
    Standardize text data in a column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column
    column : str
        Name of text column to standardize
    lowercase : bool, default False
        Convert to lowercase
    strip : bool, default True
        Remove leading/trailing whitespace
    remove_special : bool, default False
        Remove special characters (keep only alphanumeric and spaces)

    Returns
    -------
    pd.DataFrame
        DataFrame with standardized text column
    """
    df_copy = df.copy()
    
    if strip:
        df_copy[column] = df_copy[column].str.strip()
    
    if lowercase:
        df_copy[column] = df_copy[column].str.lower()
    
    if remove_special:
        df_copy[column] = df_copy[column].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
    
    return df_copy


class DataCleaner:
    """
    Orchestrates data cleaning operations with method chaining support.
    
    This class provides a fluent interface for applying multiple cleaning
    operations to a DataFrame while tracking changes.
    
    Examples
    --------
    >>> df = pd.DataFrame({'country': ['UK', None, 'UK'], 'cases': [100, 200, 100]})
    >>> cleaner = DataCleaner(df)
    >>> result = (cleaner
    ...           .handle_missing(strategy='drop')
    ...           .remove_duplicates()
    ...           .get_cleaned_data())
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize DataCleaner with a DataFrame.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to clean
        """
        self.original_df = df.copy()
        self.df = df.copy()
        self.operations = []
        self.original_shape = df.shape
    
    def detect_issues(self) -> Dict[str, Any]:
        """
        Detect common data quality issues.
        
        Returns
        -------
        dict
            Dictionary containing summaries of detected issues
        """
        issues = {}
        
        # Missing values
        missing_summary = detect_missing_values(self.df)
        issues['missing_values'] = missing_summary
        
        # Duplicates
        duplicates = detect_duplicates(self.df)
        issues['duplicates_count'] = len(duplicates)
        
        # Data types
        issues['dtypes'] = self.df.dtypes.to_dict()
        
        return issues
    
    def handle_missing(
        self,
        strategy: str = 'drop',
        columns: Optional[List[str]] = None,
        fill_value: Optional[Union[Any, Dict[str, Any]]] = None
    ) -> 'DataCleaner':
        """
        Handle missing values (chainable).
        
        Parameters
        ----------
        strategy : str
            Strategy for handling missing values
        columns : list of str, optional
            Columns to apply strategy to
        fill_value : any or dict, optional
            Fill value(s) for 'constant' strategy
        
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        self.df = handle_missing_values(self.df, strategy, columns, fill_value)
        self.operations.append(f"handle_missing(strategy='{strategy}')")
        return self
    
    def remove_duplicates(
        self,
        subset: Optional[List[str]] = None,
        keep: str = 'first'
    ) -> 'DataCleaner':
        """
        Remove duplicate rows (chainable).
        
        Parameters
        ----------
        subset : list of str, optional
            Columns to consider for duplicates
        keep : str, default 'first'
            Which duplicate to keep
        
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        self.df = remove_duplicates(self.df, subset, keep)
        self.operations.append(f"remove_duplicates(keep='{keep}')")
        return self
    
    def convert_column_type(
        self,
        column: str,
        target_type: str,
        **kwargs
    ) -> 'DataCleaner':
        """
        Convert column to specified type (chainable).
        
        Parameters
        ----------
        column : str
            Column name
        target_type : str
            Target type: 'datetime' or 'numeric'
        **kwargs
            Additional arguments for conversion functions
        
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        if target_type == 'datetime':
            self.df = convert_to_datetime(self.df, column, **kwargs)
        elif target_type == 'numeric':
            self.df = convert_to_numeric(self.df, column, **kwargs)
        else:
            raise ValueError(f"Unknown target type: {target_type}")
        
        self.operations.append(f"convert_column_type('{column}', '{target_type}')")
        return self
    
    def standardize_column(
        self,
        column: str,
        **kwargs
    ) -> 'DataCleaner':
        """
        Standardize text column (chainable).
        
        Parameters
        ----------
        column : str
            Column name
        **kwargs
            Additional arguments for standardize_text
        
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        self.df = standardize_text(self.df, column, **kwargs)
        self.operations.append(f"standardize_column('{column}')")
        return self
    
    def filter_by_range(
        self,
        column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> 'DataCleaner':
        """
        Filter rows by value range (chainable).
        
        Parameters
        ----------
        column : str
            Column name
        min_value : float, optional
            Minimum value
        max_value : float, optional
            Maximum value
        
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        valid_mask = validate_range(self.df, column, min_value, max_value)
        self.df = self.df[valid_mask]
        self.operations.append(f"filter_by_range('{column}', {min_value}, {max_value})")
        return self
    
    def remove_outliers(
        self,
        column: str,
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> 'DataCleaner':
        """
        Remove outlier rows (chainable).
        
        Parameters
        ----------
        column : str
            Column name
        method : str, default 'iqr'
            Outlier detection method
        threshold : float, default 1.5
            Detection threshold
        
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        outliers = detect_outliers(self.df, column, method, threshold)
        self.df = self.df[~outliers]
        self.operations.append(f"remove_outliers('{column}', method='{method}')")
        return self
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the cleaned DataFrame.
        
        Returns
        -------
        pd.DataFrame
            Cleaned DataFrame
        """
        return self.df.copy()
    
    def get_cleaning_report(self) -> Dict[str, Any]:
        """
        Generate a report of cleaning operations performed.
        
        Returns
        -------
        dict
            Report containing:
            - original_rows: Number of rows before cleaning
            - cleaned_rows: Number of rows after cleaning
            - rows_removed: Number of rows removed
            - original_columns: Number of columns before cleaning
            - cleaned_columns: Number of columns after cleaning
            - operations: List of operations performed
        """
        report = {
            'original_rows': self.original_shape[0],
            'cleaned_rows': self.df.shape[0],
            'rows_removed': self.original_shape[0] - self.df.shape[0],
            'original_columns': self.original_shape[1],
            'cleaned_columns': self.df.shape[1],
            'operations': self.operations
        }
        return report

