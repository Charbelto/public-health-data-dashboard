"""
Tests for data filtering and summary analysis module.

Following TDD, these tests are written before implementation.
Step 3: Filtering and Summary Views
"""

from pathlib import Path
import pandas as pd
import pytest
import numpy as np
from datetime import datetime, timedelta

from src.analysis import (
    filter_by_column,
    filter_by_date_range,
    filter_by_numeric_range,
    filter_by_multiple_criteria,
    calculate_summary_stats,
    get_column_statistics,
    group_and_aggregate,
    calculate_trends,
    calculate_growth_rate,
    calculate_moving_average,
    DataAnalyzer
)


# ==============================================================================
# Tests for Filtering Functions
# ==============================================================================

def test_filter_by_column_single_value() -> None:
    """
    Test filtering DataFrame by single column value.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'UK', 'Germany'],
        'cases': [100, 200, 150, 120, 180]
    })
    
    result = filter_by_column(df, 'country', 'UK')
    
    assert len(result) == 2
    assert all(result['country'] == 'UK')


def test_filter_by_column_multiple_values() -> None:
    """
    Test filtering DataFrame by multiple column values.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'UK', 'Germany'],
        'cases': [100, 200, 150, 120, 180]
    })
    
    result = filter_by_column(df, 'country', ['UK', 'USA'])
    
    assert len(result) == 3
    assert set(result['country'].unique()) == {'UK', 'USA'}


def test_filter_by_column_no_matches() -> None:
    """
    Test filtering with no matching values returns empty DataFrame.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    
    result = filter_by_column(df, 'country', 'Canada')
    
    assert len(result) == 0


def test_filter_by_date_range() -> None:
    """
    Test filtering DataFrame by date range.
    """
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': range(100, 110)
    })
    
    start_date = datetime(2020, 1, 3)
    end_date = datetime(2020, 1, 7)
    
    result = filter_by_date_range(df, 'date', start_date, end_date)
    
    assert len(result) == 5
    assert result['date'].min() >= start_date
    assert result['date'].max() <= end_date


def test_filter_by_date_range_start_only() -> None:
    """
    Test filtering with only start date.
    """
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': range(100, 110)
    })
    
    start_date = datetime(2020, 1, 6)
    
    result = filter_by_date_range(df, 'date', start_date=start_date)
    
    assert len(result) == 5
    assert result['date'].min() >= start_date


def test_filter_by_date_range_end_only() -> None:
    """
    Test filtering with only end date.
    """
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': range(100, 110)
    })
    
    end_date = datetime(2020, 1, 5)
    
    result = filter_by_date_range(df, 'date', end_date=end_date)
    
    assert len(result) == 5
    assert result['date'].max() <= end_date


def test_filter_by_numeric_range() -> None:
    """
    Test filtering DataFrame by numeric range.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'Germany', 'Canada'],
        'cases': [100, 200, 150, 80, 250]
    })
    
    result = filter_by_numeric_range(df, 'cases', min_value=100, max_value=200)
    
    assert len(result) == 3
    assert result['cases'].min() >= 100
    assert result['cases'].max() <= 200


def test_filter_by_numeric_range_min_only() -> None:
    """
    Test filtering with only minimum value.
    """
    df = pd.DataFrame({
        'cases': [100, 200, 150, 80, 250]
    })
    
    result = filter_by_numeric_range(df, 'cases', min_value=150)
    
    assert len(result) == 3
    assert result['cases'].min() >= 150


def test_filter_by_numeric_range_max_only() -> None:
    """
    Test filtering with only maximum value.
    """
    df = pd.DataFrame({
        'cases': [100, 200, 150, 80, 250]
    })
    
    result = filter_by_numeric_range(df, 'cases', max_value=150)
    
    assert len(result) == 3
    assert result['cases'].max() <= 150


def test_filter_by_multiple_criteria() -> None:
    """
    Test filtering by multiple criteria simultaneously.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'UK', 'Germany'],
        'year': [2020, 2020, 2021, 2021, 2020],
        'cases': [100, 200, 150, 120, 180]
    })
    
    criteria = {
        'country': ['UK', 'USA'],
        'year': 2020
    }
    
    result = filter_by_multiple_criteria(df, criteria)
    
    assert len(result) == 2
    assert all(result['country'].isin(['UK', 'USA']))
    assert all(result['year'] == 2020)


# ==============================================================================
# Tests for Summary Statistics
# ==============================================================================

def test_calculate_summary_stats_single_column() -> None:
    """
    Test calculating summary statistics for a single column.
    """
    df = pd.DataFrame({
        'cases': [100, 200, 150, 120, 180]
    })
    
    stats = calculate_summary_stats(df, 'cases')
    
    assert 'mean' in stats
    assert 'median' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert 'count' in stats
    assert 'sum' in stats
    assert 'std' in stats
    
    assert stats['mean'] == 150.0
    assert stats['min'] == 100
    assert stats['max'] == 200
    assert stats['count'] == 5
    assert stats['sum'] == 750


def test_calculate_summary_stats_with_missing_values() -> None:
    """
    Test summary statistics handle missing values correctly.
    """
    df = pd.DataFrame({
        'cases': [100, 200, None, 120, 180]
    })
    
    stats = calculate_summary_stats(df, 'cases')
    
    assert stats['count'] == 4  # Only non-null values
    assert stats['mean'] == 150.0


def test_get_column_statistics_all_numeric() -> None:
    """
    Test getting statistics for all numeric columns.
    """
    df = pd.DataFrame({
        'cases': [100, 200, 150],
        'deaths': [10, 20, 15],
        'country': ['UK', 'USA', 'France']
    })
    
    stats = get_column_statistics(df)
    
    assert 'cases' in stats
    assert 'deaths' in stats
    assert 'country' not in stats  # Non-numeric column excluded


def test_get_column_statistics_specific_columns() -> None:
    """
    Test getting statistics for specific columns only.
    """
    df = pd.DataFrame({
        'cases': [100, 200, 150],
        'deaths': [10, 20, 15],
        'recovered': [80, 170, 130]
    })
    
    stats = get_column_statistics(df, columns=['cases', 'deaths'])
    
    assert 'cases' in stats
    assert 'deaths' in stats
    assert 'recovered' not in stats


# ==============================================================================
# Tests for Grouping and Aggregation
# ==============================================================================

def test_group_and_aggregate_single_group() -> None:
    """
    Test grouping by single column with aggregation.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'USA', 'France'],
        'cases': [100, 200, 150, 180, 120]
    })
    
    result = group_and_aggregate(df, group_by='country', agg_column='cases', agg_func='sum')
    
    assert len(result) == 3
    assert result.loc['UK', 'cases'] == 250
    assert result.loc['USA', 'cases'] == 380


def test_group_and_aggregate_multiple_groups() -> None:
    """
    Test grouping by multiple columns.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'USA', 'UK'],
        'year': [2020, 2020, 2021, 2021, 2020],
        'cases': [100, 200, 150, 180, 50]
    })
    
    result = group_and_aggregate(
        df, 
        group_by=['country', 'year'], 
        agg_column='cases', 
        agg_func='mean'
    )
    
    assert len(result) == 4
    assert result.loc[('UK', 2020), 'cases'] == 75.0


def test_group_and_aggregate_multiple_functions() -> None:
    """
    Test multiple aggregation functions simultaneously.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'USA'],
        'cases': [100, 200, 150, 180]
    })
    
    result = group_and_aggregate(
        df, 
        group_by='country', 
        agg_column='cases', 
        agg_func=['sum', 'mean', 'count']
    )
    
    assert 'sum' in result.columns or isinstance(result.columns, pd.MultiIndex)
    assert len(result) == 2


def test_group_and_aggregate_with_sorting() -> None:
    """
    Test grouping with sorted results.
    """
    df = pd.DataFrame({
        'country': ['France', 'UK', 'USA'],
        'cases': [120, 100, 200]
    })
    
    result = group_and_aggregate(
        df, 
        group_by='country', 
        agg_column='cases', 
        agg_func='sum',
        sort_by='cases',
        ascending=False
    )
    
    assert result.iloc[0]['cases'] == 200  # USA first (highest)


# ==============================================================================
# Tests for Trend Analysis
# ==============================================================================

def test_calculate_trends_over_time() -> None:
    """
    Test calculating trends over time periods.
    """
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=5, freq='ME'),
        'cases': [100, 120, 150, 180, 200]
    })
    
    trends = calculate_trends(df, date_column='date', value_column='cases')
    
    assert 'total_change' in trends
    assert 'percent_change' in trends
    assert 'average_change' in trends
    assert trends['total_change'] == 100
    assert trends['percent_change'] > 0


def test_calculate_growth_rate() -> None:
    """
    Test calculating growth rate between periods.
    """
    df = pd.DataFrame({
        'year': [2020, 2021, 2022],
        'cases': [100, 150, 180]
    })
    
    df_with_growth = calculate_growth_rate(df, value_column='cases')
    
    assert 'growth_rate' in df_with_growth.columns
    assert pd.isna(df_with_growth['growth_rate'].iloc[0])  # First row has no previous
    assert df_with_growth['growth_rate'].iloc[1] == 50.0  # (150-100)/100 * 100


def test_calculate_growth_rate_with_zero_values() -> None:
    """
    Test growth rate handles zero values correctly.
    """
    df = pd.DataFrame({
        'year': [2020, 2021, 2022],
        'cases': [0, 100, 150]
    })
    
    df_with_growth = calculate_growth_rate(df, value_column='cases')
    
    # Growth from 0 should be handled (infinity or NaN)
    assert 'growth_rate' in df_with_growth.columns


def test_calculate_moving_average() -> None:
    """
    Test calculating moving average.
    """
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
    })
    
    df_with_ma = calculate_moving_average(df, column='cases', window=3)
    
    assert 'cases_ma_3' in df_with_ma.columns
    assert pd.isna(df_with_ma['cases_ma_3'].iloc[0])  # First values are NaN
    assert df_with_ma['cases_ma_3'].iloc[2] == 110.0  # (100+110+120)/3


def test_calculate_moving_average_different_windows() -> None:
    """
    Test moving average with different window sizes.
    """
    df = pd.DataFrame({
        'cases': list(range(1, 11))
    })
    
    df_with_ma = calculate_moving_average(df, column='cases', window=5)
    
    assert 'cases_ma_5' in df_with_ma.columns
    assert df_with_ma['cases_ma_5'].iloc[4] == 3.0  # (1+2+3+4+5)/5


# ==============================================================================
# Tests for DataAnalyzer Class
# ==============================================================================

def test_data_analyzer_initialization() -> None:
    """
    Test DataAnalyzer initialization with DataFrame.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA'],
        'cases': [100, 200]
    })
    
    analyzer = DataAnalyzer(df)
    
    assert analyzer is not None
    assert len(analyzer.df) == 2


def test_data_analyzer_filter_and_summarize() -> None:
    """
    Test chaining filter and summary operations.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'UK'],
        'year': [2020, 2020, 2021, 2021],
        'cases': [100, 200, 150, 120]
    })
    
    analyzer = DataAnalyzer(df)
    result = (analyzer
              .filter_by('country', 'UK')
              .summarize('cases'))
    
    assert 'mean' in result
    assert result['count'] == 2


def test_data_analyzer_group_analysis() -> None:
    """
    Test grouping and aggregation through DataAnalyzer.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'USA'],
        'cases': [100, 200, 150, 180]
    })
    
    analyzer = DataAnalyzer(df)
    result = analyzer.group_by('country').aggregate('cases', 'sum')
    
    assert len(result) == 2
    assert 'cases' in result.columns


def test_data_analyzer_get_filtered_data() -> None:
    """
    Test retrieving filtered data from DataAnalyzer.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    
    analyzer = DataAnalyzer(df)
    filtered = analyzer.filter_by('country', ['UK', 'USA']).get_data()
    
    assert len(filtered) == 2
    assert set(filtered['country']) == {'UK', 'USA'}


def test_data_analyzer_trend_analysis() -> None:
    """
    Test trend analysis through DataAnalyzer.
    """
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=5, freq='ME'),
        'cases': [100, 120, 150, 180, 200]
    })
    
    analyzer = DataAnalyzer(df)
    trends = analyzer.analyze_trends('date', 'cases')
    
    assert 'total_change' in trends
    assert 'percent_change' in trends


def test_data_analyzer_get_analysis_report() -> None:
    """
    Test generating comprehensive analysis report.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK'],
        'year': [2020, 2020, 2021],
        'cases': [100, 200, 150]
    })
    
    analyzer = DataAnalyzer(df)
    report = analyzer.get_analysis_report()
    
    assert 'total_records' in report
    assert 'numeric_columns' in report
    assert 'summary_statistics' in report
