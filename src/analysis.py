"""
Data Filtering and Summary Analysis Module - Step 3

This module provides functions for filtering and summarizing public health data:
- Filter by columns, dates, and multiple conditions
- Calculate summary statistics (mean, min, max, count, etc.)
- Analyze trends over time
- Group and aggregate data
- Compare groups
- Moving averages
"""

from typing import Union, List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np


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
        Value(s) to filter for

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
    df_copy = df.copy()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
    
    mask = pd.Series([True] * len(df_copy), index=df_copy.index)
    
    if start_date is not None:
        mask &= (df_copy[date_column] >= pd.Timestamp(start_date))
    
    if end_date is not None:
        mask &= (df_copy[date_column] <= pd.Timestamp(end_date))
    
    return df_copy[mask]


def filter_by_multiple_conditions(
    df: pd.DataFrame,
    conditions: Dict[str, Any]
) -> pd.DataFrame:
    """
    Filter DataFrame by multiple conditions.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to filter
    conditions : dict
        Dictionary of column: value pairs

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame

    Examples
    --------
    >>> conditions = {'country': 'UK', 'year': 2020}
    >>> filtered = filter_by_multiple_conditions(df, conditions)
    """
    df_filtered = df.copy()
    
    for column, value in conditions.items():
        if isinstance(value, list):
            df_filtered = df_filtered[df_filtered[column].isin(value)]
        else:
            df_filtered = df_filtered[df_filtered[column] == value]
    
    return df_filtered


def calculate_statistics(
    df: pd.DataFrame,
    column: str,
    metrics: Optional[List[str]] = None
) -> Dict[str, float]:
    """
    Calculate summary statistics for a column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    column : str
        Column name to calculate statistics for
    metrics : list of str, optional
        List of metrics to calculate. If None, calculates all.
        Available: 'mean', 'median', 'min', 'max', 'sum', 'count', 'std'

    Returns
    -------
    dict
        Dictionary of statistic: value pairs
    """
    if metrics is None:
        metrics = ['mean', 'median', 'min', 'max', 'sum', 'count', 'std']
    
    stats = {}
    
    for metric in metrics:
        if metric == 'mean':
            stats['mean'] = df[column].mean()
        elif metric == 'median':
            stats['median'] = df[column].median()
        elif metric == 'min':
            stats['min'] = df[column].min()
        elif metric == 'max':
            stats['max'] = df[column].max()
        elif metric == 'sum':
            stats['sum'] = df[column].sum()
        elif metric == 'count':
            stats['count'] = df[column].count()
        elif metric == 'std':
            stats['std'] = df[column].std()
    
    return stats


def calculate_summary(
    df: pd.DataFrame,
    columns: List[str],
    metrics: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Calculate summary statistics for multiple columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    columns : list of str
        Column names to calculate statistics for
    metrics : list of str, optional
        List of metrics to calculate

    Returns
    -------
    dict
        Nested dictionary: {column: {metric: value}}
    """
    summary = {}
    
    for column in columns:
        summary[column] = calculate_statistics(df, column, metrics)
    
    return summary


def analyze_trends(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
    group_by: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze trends over time.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing time series data
    date_column : str
        Name of date column
    value_column : str
        Name of value column to analyze
    group_by : str, optional
        Column to group by before analyzing trends

    Returns
    -------
    dict
        Dictionary containing trend metrics:
        - total: Sum of all values
        - average: Mean value
        - growth_rate: Percentage growth (first to last)
        - trend: 'increasing', 'decreasing', or 'stable'
        
        If group_by is provided, returns nested dict: {group: metrics}
    """
    df_copy = df.copy()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
    
    # Sort by date
    df_copy = df_copy.sort_values(date_column)
    
    if group_by is None:
        return _calculate_trend_metrics(df_copy, value_column)
    else:
        # Group by and calculate trends for each group
        trends = {}
        for group_name, group_df in df_copy.groupby(group_by):
            trends[group_name] = _calculate_trend_metrics(group_df, value_column)
        return trends


def _calculate_trend_metrics(df: pd.DataFrame, value_column: str) -> Dict[str, Any]:
    """Helper function to calculate trend metrics."""
    total = df[value_column].sum()
    average = df[value_column].mean()
    
    # Calculate growth rate
    first_value = df[value_column].iloc[0]
    last_value = df[value_column].iloc[-1]
    
    if first_value != 0:
        growth_rate = ((last_value - first_value) / first_value) * 100
    else:
        growth_rate = 0.0
    
    # Determine trend direction
    if growth_rate > 5:
        trend = 'increasing'
    elif growth_rate < -5:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    return {
        'total': total,
        'average': average,
        'growth_rate': growth_rate,
        'trend': trend,
        'first_value': first_value,
        'last_value': last_value
    }


def calculate_moving_average(
    df: pd.DataFrame,
    column: str,
    window: int = 7,
    output_column: Optional[str] = None
) -> pd.DataFrame:
    """
    Calculate moving average for a column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    column : str
        Column to calculate moving average for
    window : int, default 7
        Window size for moving average
    output_column : str, optional
        Name for output column. Defaults to '{column}_ma'

    Returns
    -------
    pd.DataFrame
        DataFrame with added moving average column
    """
    df_copy = df.copy()
    
    if output_column is None:
        output_column = f'{column}_ma'
    
    df_copy[output_column] = df_copy[column].rolling(window=window).mean()
    
    return df_copy


def group_and_aggregate(
    df: pd.DataFrame,
    group_by: Union[str, List[str]],
    agg_column: str,
    agg_func: Union[str, List[str]] = 'sum'
) -> pd.DataFrame:
    """
    Group data and apply aggregation function(s).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to group and aggregate
    group_by : str or list of str
        Column(s) to group by
    agg_column : str
        Column to aggregate
    agg_func : str or list of str, default 'sum'
        Aggregation function(s): 'sum', 'mean', 'count', 'min', 'max', etc.

    Returns
    -------
    pd.DataFrame
        Grouped and aggregated DataFrame
    """
    if isinstance(agg_func, str):
        result = df.groupby(group_by)[agg_column].agg(agg_func).reset_index()
    else:
        result = df.groupby(group_by)[agg_column].agg(agg_func).reset_index()
    
    # If single group_by column, set as index for easier access
    if isinstance(group_by, str):
        result = result.set_index(group_by)
    
    return result


def compare_groups(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
    metrics: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Compare statistics across different groups.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    group_column : str
        Column to group by
    value_column : str
        Column to calculate statistics for
    metrics : list of str, optional
        Metrics to calculate for comparison

    Returns
    -------
    dict
        Nested dictionary: {group: {metric: value}}
    """
    comparison = {}
    
    for group_name, group_df in df.groupby(group_column):
        comparison[group_name] = calculate_statistics(
            group_df,
            value_column,
            metrics
        )
    
    return comparison


class DataAnalyzer:
    """
    Comprehensive data analysis class with method chaining support.
    
    This class provides a fluent interface for filtering, summarizing,
    and analyzing public health data.
    
    Examples
    --------
    >>> analyzer = DataAnalyzer(df)
    >>> result = (analyzer
    ...           .filter_by('country', 'UK')
    ...           .filter_by_date('date', start_date, end_date)
    ...           .get_summary(['cases', 'deaths']))
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
            Column name to filter on
        value : any or list
            Value(s) to filter for
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = filter_by_column(self.df, column, value)
        self.operations.append(f"filter_by('{column}', {value})")
        return self
    
    def filter_by_date(
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
            Name of date column
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
        self.operations.append(f"filter_by_date('{date_column}')")
        return self
    
    def filter_by_conditions(
        self,
        conditions: Dict[str, Any]
    ) -> 'DataAnalyzer':
        """
        Filter by multiple conditions (chainable).
        
        Parameters
        ----------
        conditions : dict
            Dictionary of column: value pairs
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = filter_by_multiple_conditions(self.df, conditions)
        self.operations.append(f"filter_by_conditions({conditions})")
        return self
    
    def group_by(
        self,
        column: Union[str, List[str]]
    ) -> 'DataAnalyzer':
        """
        Set grouping for subsequent aggregation (chainable).
        
        Parameters
        ----------
        column : str or list of str
            Column(s) to group by
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self._group_by = column
        self.operations.append(f"group_by('{column}')")
        return self
    
    def aggregate(
        self,
        column: str,
        func: Union[str, List[str]] = 'sum'
    ) -> 'DataAnalyzer':
        """
        Aggregate grouped data (chainable).
        
        Parameters
        ----------
        column : str
            Column to aggregate
        func : str or list of str
            Aggregation function(s)
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        if hasattr(self, '_group_by'):
            self.df = group_and_aggregate(self.df, self._group_by, column, func)
            del self._group_by
        self.operations.append(f"aggregate('{column}', '{func}')")
        return self
    
    def calculate_moving_avg(
        self,
        column: str,
        window: int = 7
    ) -> 'DataAnalyzer':
        """
        Calculate moving average (chainable).
        
        Parameters
        ----------
        column : str
            Column to calculate moving average for
        window : int, default 7
            Window size
        
        Returns
        -------
        DataAnalyzer
            Self for method chaining
        """
        self.df = calculate_moving_average(self.df, column, window)
        self.operations.append(f"calculate_moving_avg('{column}', {window})")
        return self
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the current DataFrame.
        
        Returns
        -------
        pd.DataFrame
            Current DataFrame after all operations
        """
        return self.df.copy()
    
    def get_summary(
        self,
        columns: List[str],
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Get summary statistics for columns.
        
        Parameters
        ----------
        columns : list of str
            Columns to summarize
        metrics : list of str, optional
            Metrics to calculate
        
        Returns
        -------
        dict
            Summary statistics
        """
        return calculate_summary(self.df, columns, metrics)
    
    def get_trends(
        self,
        date_column: str,
        value_column: str,
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze trends over time.
        
        Parameters
        ----------
        date_column : str
            Date column name
        value_column : str
            Value column to analyze
        group_by : str, optional
            Column to group by
        
        Returns
        -------
        dict
            Trend analysis results
        """
        return analyze_trends(self.df, date_column, value_column, group_by)
    
    def compare(
        self,
        group_column: str,
        value_column: str,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare statistics across groups.
        
        Parameters
        ----------
        group_column : str
            Column to group by
        value_column : str
            Column to compare
        metrics : list of str, optional
            Metrics to calculate
        
        Returns
        -------
        dict
            Comparison results
        """
        return compare_groups(self.df, group_column, value_column, metrics)
    
    def reset(self) -> 'DataAnalyzer':
        """
        Reset to original DataFrame.
        
        Returns
        -------
        DataAnalyzer
            Self with reset data
        """
        self.df = self.original_df.copy()
        self.operations = []
        return self
    
    def get_operations_log(self) -> List[str]:
        """
        Get list of operations performed.
        
        Returns
        -------
        list of str
            List of operation descriptions
        """
        return self.operations.copy()

