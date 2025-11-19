"""
Data Filtering and Summary Analysis Module - Step 3

This module provides functions for filtering data and generating summary views:
- Filter by column values, date ranges, numeric ranges
- Calculate summary statistics (mean, min, max, count, etc.)
- Group and aggregate data
- Analyze trends over time
- Calculate growth rates and moving averages
"""

from typing import Union, Optional, List, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime


def filter_by_column(
    df: pd.DataFrame,
    column: str,
    value: Union[Any, List[Any]]
) -> pd.DataFrame:
    """
    Filter DataFrame by column value(s).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to filter
    column : str
        Column name to filter on
    value : any or list
        Single value or list of values to filter by

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame
    """
    if isinstance(value, list):
        return df[df[column].isin(value)]
    else:
        return df[df[column] == value]


def filter_by_date_range(
    df: pd.DataFrame,
    date_column: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Filter DataFrame by date range.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to filter
    date_column : str
        Name of date column
    start_date : datetime, optional
        Start date (inclusive)
    end_date : datetime, optional
        End date (inclusive)

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame
    """
    filtered = df.copy()
    
    if start_date is not None:
        filtered = filtered[filtered[date_column] >= start_date]
    
    if end_date is not None:
        filtered = filtered[filtered[date_column] <= end_date]
    
    return filtered


def filter_by_numeric_range(
    df: pd.DataFrame,
    column: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> pd.DataFrame:
    """
    Filter DataFrame by numeric range.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to filter
    column : str
        Name of numeric column
    min_value : float, optional
        Minimum value (inclusive)
    max_value : float, optional
        Maximum value (inclusive)

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame
    """
    filtered = df.copy()
    
    if min_value is not None:
        filtered = filtered[filtered[column] >= min_value]
    
    if max_value is not None:
        filtered = filtered[filtered[column] <= max_value]
    
    return filtered


def filter_by_multiple_criteria(
    df: pd.DataFrame,
    criteria: Dict[str, Any]
) -> pd.DataFrame:
    """
    Filter DataFrame by multiple criteria simultaneously.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to filter
    criteria : dict
        Dictionary mapping column names to values or lists of values

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame

    Examples
    --------
    >>> criteria = {'country': ['UK', 'USA'], 'year': 2020}
    >>> filtered = filter_by_multiple_criteria(df, criteria)
    """
    filtered = df.copy()
    
    for column, value in criteria.items():
        if isinstance(value, list):
            filtered = filtered[filtered[column].isin(value)]
        else:
            filtered = filtered[filtered[column] == value]
    
    return filtered


def calculate_summary_stats(
    df: pd.DataFrame,
    column: str
) -> Dict[str, float]:
    """
    Calculate summary statistics for a column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    column : str
        Column name to analyze

    Returns
    -------
    dict
        Dictionary with statistics: mean, median, min, max, count, sum, std
    """
    stats = {
        'mean': float(df[column].mean()),
        'median': float(df[column].median()),
        'min': float(df[column].min()),
        'max': float(df[column].max()),
        'count': int(df[column].count()),
        'sum': float(df[column].sum()),
        'std': float(df[column].std())
    }
    
    return stats


def get_column_statistics(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Get statistics for multiple columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to analyze
    columns : list of str, optional
        Specific columns to analyze. If None, analyzes all numeric columns.

    Returns
    -------
    dict
        Dictionary mapping column names to their statistics
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    stats_dict = {}
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            stats_dict[col] = calculate_summary_stats(df, col)
    
    return stats_dict


def group_and_aggregate(
    df: pd.DataFrame,
    group_by: Union[str, List[str]],
    agg_column: str,
    agg_func: Union[str, List[str]] = 'sum',
    sort_by: Optional[str] = None,
    ascending: bool = True
) -> pd.DataFrame:
    """
    Group DataFrame and apply aggregation function.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to group
    group_by : str or list of str
        Column(s) to group by
    agg_column : str
        Column to aggregate
    agg_func : str or list of str, default 'sum'
        Aggregation function(s): 'sum', 'mean', 'count', 'min', 'max', etc.
    sort_by : str, optional
        Column to sort results by
    ascending : bool, default True
        Sort order

    Returns
    -------
    pd.DataFrame
        Grouped and aggregated DataFrame
    """
    grouped = df.groupby(group_by)[agg_column].agg(agg_func).reset_index()
    
    if sort_by and sort_by in grouped.columns:
        grouped = grouped.sort_values(sort_by, ascending=ascending)
    
    # If single agg_func, ensure column name is preserved
    if isinstance(agg_func, str):
        if len(grouped.columns) == 2 and grouped.columns[1] == agg_func:
            grouped.columns = [group_by if isinstance(group_by, str) else group_by[0], agg_column]
    
    # Set index to group_by columns for easier access
    if isinstance(group_by, list):
        grouped = grouped.set_index(group_by)
    else:
        grouped = grouped.set_index(group_by)
    
    return grouped


def calculate_trends(
    df: pd.DataFrame,
    date_column: str,
    value_column: str
) -> Dict[str, float]:
    """
    Calculate trends over time.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with time series data
    date_column : str
        Name of date column
    value_column : str
        Name of value column to analyze

    Returns
    -------
    dict
        Dictionary with trend statistics:
        - total_change: Absolute change from start to end
        - percent_change: Percentage change from start to end
        - average_change: Average change per period
    """
    df_sorted = df.sort_values(date_column)
    
    first_value = df_sorted[value_column].iloc[0]
    last_value = df_sorted[value_column].iloc[-1]
    
    total_change = last_value - first_value
    percent_change = (total_change / first_value * 100) if first_value != 0 else 0
    
    # Calculate average change per period
    num_periods = len(df_sorted) - 1
    average_change = total_change / num_periods if num_periods > 0 else 0
    
    trends = {
        'total_change': float(total_change),
        'percent_change': float(percent_change),
        'average_change': float(average_change),
        'start_value': float(first_value),
        'end_value': float(last_value),
        'periods': int(num_periods + 1)
    }
    
    return trends


def calculate_growth_rate(
    df: pd.DataFrame,
    value_column: str,
    periods: int = 1
) -> pd.DataFrame:
    """
    Calculate growth rate between periods.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with time series data
    value_column : str
        Column to calculate growth rate for
    periods : int, default 1
        Number of periods to compare (1 = period-over-period)

    Returns
    -------
    pd.DataFrame
        DataFrame with additional 'growth_rate' column (percentage)
    """
    df_copy = df.copy()
    
    # Calculate period-over-period growth rate
    df_copy['growth_rate'] = df_copy[value_column].pct_change(periods=periods) * 100
    
    return df_copy


def calculate_moving_average(
    df: pd.DataFrame,
    column: str,
    window: int = 3
) -> pd.DataFrame:
    """
    Calculate moving average for a column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    column : str
        Column to calculate moving average for
    window : int, default 3
        Window size for moving average

    Returns
    -------
    pd.DataFrame
        DataFrame with additional moving average column
    """
    df_copy = df.copy()
    
    ma_column_name = f"{column}_ma_{window}"
    df_copy[ma_column_name] = df_copy[column].rolling(window=window).mean()
    
    return df_copy


class DataAnalyzer:
    """
    Orchestrates data filtering and analysis operations with method chaining.
    
    This class provides a fluent interface for filtering, grouping, and
    analyzing data while tracking operations.
    
    Examples
    --------
    >>> analyzer = DataAnalyzer(df)
    >>> result = (analyzer
    ...           .filter_by('country', 'UK')
    ...           .filter_numeric_range('cases', min_value=100)
    ...           .summarize('cases'))
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize DataAnalyzer with a DataFrame.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to analyze
        """
        self.original_df = df.copy()
        self.df = df.copy()
        self.operations = []
    
    def filter_by(
        self,
        column: str,
        value: Union[Any, List[Any]]
    ) -> 'DataAnalyzer':
        """
        Filter by column value(s) (chainable).
        
        Parameters
        ----------
        column : str
            Column to filter on
        value : any or list
            Value(s) to filter by
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = filter_by_column(self.df, column, value)
        self.operations.append(f"filter_by('{column}', {value})")
        return self
    
    def filter_date_range(
        self,
        date_column: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> 'DataAnalyzer':
        """
        Filter by date range (chainable).
        
        Parameters
        ----------
        date_column : str
            Date column name
        start_date : datetime, optional
            Start date
        end_date : datetime, optional
            End date
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = filter_by_date_range(self.df, date_column, start_date, end_date)
        self.operations.append(f"filter_date_range('{date_column}')")
        return self
    
    def filter_numeric_range(
        self,
        column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> 'DataAnalyzer':
        """
        Filter by numeric range (chainable).
        
        Parameters
        ----------
        column : str
            Numeric column name
        min_value : float, optional
            Minimum value
        max_value : float, optional
            Maximum value
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = filter_by_numeric_range(self.df, column, min_value, max_value)
        self.operations.append(f"filter_numeric_range('{column}', {min_value}, {max_value})")
        return self
    
    def summarize(self, column: str) -> Dict[str, float]:
        """
        Calculate summary statistics for current filtered data.
        
        Parameters
        ----------
        column : str
            Column to summarize
        
        Returns
        -------
        dict
            Summary statistics
        """
        return calculate_summary_stats(self.df, column)
    
    def group_by(self, columns: Union[str, List[str]]) -> 'DataAnalyzer':
        """
        Set grouping columns for subsequent aggregation (chainable).
        
        Parameters
        ----------
        columns : str or list of str
            Column(s) to group by
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self._group_by_columns = columns if isinstance(columns, list) else [columns]
        self.operations.append(f"group_by({columns})")
        return self
    
    def aggregate(
        self,
        column: str,
        func: Union[str, List[str]] = 'sum'
    ) -> pd.DataFrame:
        """
        Aggregate grouped data.
        
        Parameters
        ----------
        column : str
            Column to aggregate
        func : str or list of str
            Aggregation function(s)
        
        Returns
        -------
        pd.DataFrame
            Aggregated results
        """
        if not hasattr(self, '_group_by_columns'):
            raise ValueError("Must call group_by() before aggregate()")
        
        return group_and_aggregate(
            self.df,
            self._group_by_columns if len(self._group_by_columns) > 1 else self._group_by_columns[0],
            column,
            func
        )
    
    def analyze_trends(
        self,
        date_column: str,
        value_column: str
    ) -> Dict[str, float]:
        """
        Analyze trends in current filtered data.
        
        Parameters
        ----------
        date_column : str
            Date column
        value_column : str
            Value column
        
        Returns
        -------
        dict
            Trend statistics
        """
        return calculate_trends(self.df, date_column, value_column)
    
    def add_growth_rate(self, column: str) -> 'DataAnalyzer':
        """
        Add growth rate calculation (chainable).
        
        Parameters
        ----------
        column : str
            Column to calculate growth rate for
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = calculate_growth_rate(self.df, column)
        self.operations.append(f"add_growth_rate('{column}')")
        return self
    
    def add_moving_average(
        self,
        column: str,
        window: int = 3
    ) -> 'DataAnalyzer':
        """
        Add moving average calculation (chainable).
        
        Parameters
        ----------
        column : str
            Column to calculate moving average for
        window : int
            Window size
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = calculate_moving_average(self.df, column, window)
        self.operations.append(f"add_moving_average('{column}', {window})")
        return self
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the current filtered/analyzed DataFrame.
        
        Returns
        -------
        pd.DataFrame
            Current DataFrame
        """
        return self.df.copy()
    
    def get_analysis_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report.
        
        Returns
        -------
        dict
            Report containing:
            - total_records: Number of records
            - numeric_columns: List of numeric columns
            - summary_statistics: Statistics for numeric columns
            - operations: List of operations performed
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        report = {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'numeric_columns': numeric_cols,
            'summary_statistics': get_column_statistics(self.df),
            'operations': self.operations,
            'original_records': len(self.original_df),
            'records_filtered': len(self.original_df) - len(self.df)
        }
        
        return report
