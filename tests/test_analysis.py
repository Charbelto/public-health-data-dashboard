"""
Tests for data filtering and summary analysis module.

Following TDD, these tests are written before implementation.
Step 3: Filtering and Summary Views
"""

from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pytest
import numpy as np

from src.analysis import (
    filter_by_column,
    filter_by_date_range,
    filter_by_multiple_conditions,
    calculate_statistics,
    calculate_summary,
    analyze_trends,
    group_and_aggregate,
    calculate_moving_average,
    compare_groups,
    DataAnalyzer
)


# ==============================================================================
# Tests for Basic Filtering
# ==============================================================================

def test_filter_by_column_single_value() -> None:
    """Test filtering by a single column value."""
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'UK', 'USA'],
        'cases': [100, 200, 300, 150, 250]
    })
    
    result = filter_by_column(df, 'country', 'UK')
    
    assert len(result) == 2
    assert all(result['country'] == 'UK')


def test_filter_by_column_multiple_values() -> None:
    """Test filtering by multiple column values."""
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'Germany'],
        'cases': [100, 200, 300, 400]
    })
    
    result = filter_by_column(df, 'country', ['UK', 'USA'])
    
    assert len(result) == 2
    assert set(result['country']) == {'UK', 'USA'}


def test_filter_by_column_returns_empty_for_no_match() -> None:
    """Test that filtering returns empty DataFrame when no matches."""
    df = pd.DataFrame({
        'country': ['UK', 'USA'],
        'cases': [100, 200]
    })
    
    result = filter_by_column(df, 'country', 'Japan')
    
    assert len(result) == 0
    assert list(result.columns) == list(df.columns)


def test_filter_by_date_range() -> None:
    """Test filtering by date range."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': range(100, 110)
    })
    
    start_date = datetime(2020, 1, 3)
    end_date = datetime(2020, 1, 7)
    
    result = filter_by_date_range(df, 'date', start_date, end_date)
    
    assert len(result) == 5  # Days 3-7 inclusive
    assert result['date'].min() >= pd.Timestamp(start_date)
    assert result['date'].max() <= pd.Timestamp(end_date)


def test_filter_by_date_range_only_start() -> None:
    """Test filtering with only start date."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': range(100, 110)
    })
    
    start_date = datetime(2020, 1, 5)
    
    result = filter_by_date_range(df, 'date', start_date=start_date)
    
    assert len(result) == 6  # Days 5-10
    assert result['date'].min() >= pd.Timestamp(start_date)


def test_filter_by_date_range_only_end() -> None:
    """Test filtering with only end date."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': range(100, 110)
    })
    
    end_date = datetime(2020, 1, 5)
    
    result = filter_by_date_range(df, 'date', end_date=end_date)
    
    assert len(result) == 5  # Days 1-5
    assert result['date'].max() <= pd.Timestamp(end_date)


def test_filter_by_multiple_conditions() -> None:
    """Test filtering with multiple conditions."""
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'UK', 'USA', 'France'],
        'year': [2020, 2020, 2021, 2021, 2020],
        'cases': [100, 200, 150, 250, 300]
    })
    
    conditions = {
        'country': 'UK',
        'year': 2021
    }
    
    result = filter_by_multiple_conditions(df, conditions)
    
    assert len(result) == 1
    assert result['country'].iloc[0] == 'UK'
    assert result['year'].iloc[0] == 2021


# ==============================================================================
# Tests for Summary Statistics
# ==============================================================================

def test_calculate_statistics_all_metrics() -> None:
    """Test calculating all statistics for a column."""
    df = pd.DataFrame({
        'cases': [100, 150, 200, 250, 300]
    })
    
    stats = calculate_statistics(df, 'cases')
    
    assert stats['mean'] == 200.0
    assert stats['median'] == 200.0
    assert stats['min'] == 100
    assert stats['max'] == 300
    assert stats['sum'] == 1000
    assert stats['count'] == 5
    assert 'std' in stats


def test_calculate_statistics_specific_metrics() -> None:
    """Test calculating specific statistics."""
    df = pd.DataFrame({
        'cases': [100, 200, 300]
    })
    
    stats = calculate_statistics(df, 'cases', metrics=['mean', 'max'])
    
    assert 'mean' in stats
    assert 'max' in stats
    assert 'min' not in stats
    assert 'median' not in stats


def test_calculate_summary_multiple_columns() -> None:
    """Test calculating summary for multiple columns."""
    df = pd.DataFrame({
        'cases': [100, 200, 300],
        'deaths': [10, 20, 30]
    })
    
    summary = calculate_summary(df, ['cases', 'deaths'])
    
    assert 'cases' in summary
    assert 'deaths' in summary
    assert summary['cases']['mean'] == 200.0
    assert summary['deaths']['sum'] == 60


def test_calculate_summary_handles_missing_values() -> None:
    """Test that summary handles missing values correctly."""
    df = pd.DataFrame({
        'cases': [100, None, 300, 400]
    })
    
    summary = calculate_summary(df, ['cases'])
    
    assert summary['cases']['count'] == 3  # Excludes NaN
    assert summary['cases']['mean'] == pytest.approx(266.67, rel=0.01)


# ==============================================================================
# Tests for Trend Analysis
# ==============================================================================

def test_analyze_trends_over_time() -> None:
    """Test analyzing trends over time."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=5, freq='D'),
        'cases': [100, 120, 140, 160, 180]
    })
    
    trends = analyze_trends(df, date_column='date', value_column='cases')
    
    assert 'total' in trends
    assert 'average' in trends
    assert 'growth_rate' in trends
    assert trends['total'] == 700
    assert trends['average'] == 140.0
    assert trends['growth_rate'] > 0  # Positive growth


def test_analyze_trends_with_grouping() -> None:
    """Test trend analysis with grouping by category."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=6, freq='D').tolist() * 2,
        'country': ['UK'] * 6 + ['USA'] * 6,
        'cases': [100, 110, 120, 130, 140, 150] + [200, 220, 240, 260, 280, 300]
    })
    
    trends = analyze_trends(
        df,
        date_column='date',
        value_column='cases',
        group_by='country'
    )
    
    assert 'UK' in trends
    assert 'USA' in trends
    assert trends['UK']['total'] == 750
    assert trends['USA']['total'] == 1500


def test_calculate_moving_average() -> None:
    """Test calculating moving average."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=10, freq='D'),
        'cases': [100, 110, 105, 115, 120, 125, 130, 135, 140, 145]
    })
    
    result = calculate_moving_average(df, 'cases', window=3)
    
    assert 'cases_ma' in result.columns
    assert pd.notna(result['cases_ma'].iloc[-1])  # Last value should be calculated
    assert result['cases_ma'].iloc[-1] == pytest.approx(140.0, rel=0.01)


def test_calculate_moving_average_custom_column_name() -> None:
    """Test moving average with custom output column name."""
    df = pd.DataFrame({
        'cases': [100, 110, 120, 130, 140]
    })
    
    result = calculate_moving_average(
        df,
        'cases',
        window=2,
        output_column='rolling_avg'
    )
    
    assert 'rolling_avg' in result.columns
    assert 'cases_ma' not in result.columns


# ==============================================================================
# Tests for Grouping and Aggregation
# ==============================================================================

def test_group_and_aggregate_single_column() -> None:
    """Test grouping by single column with aggregation."""
    df = pd.DataFrame({
        'country': ['UK', 'UK', 'USA', 'USA', 'France'],
        'cases': [100, 150, 200, 250, 300]
    })
    
    result = group_and_aggregate(
        df,
        group_by='country',
        agg_column='cases',
        agg_func='sum'
    )
    
    assert len(result) == 3
    assert result.loc['UK', 'cases'] == 250
    assert result.loc['USA', 'cases'] == 450


def test_group_and_aggregate_multiple_columns() -> None:
    """Test grouping by multiple columns."""
    df = pd.DataFrame({
        'country': ['UK', 'UK', 'USA', 'USA'],
        'year': [2020, 2021, 2020, 2021],
        'cases': [100, 150, 200, 250]
    })
    
    result = group_and_aggregate(
        df,
        group_by=['country', 'year'],
        agg_column='cases',
        agg_func='sum'
    )
    
    assert len(result) == 4


def test_group_and_aggregate_multiple_functions() -> None:
    """Test aggregation with multiple functions."""
    df = pd.DataFrame({
        'country': ['UK', 'UK', 'USA', 'USA'],
        'cases': [100, 150, 200, 250]
    })
    
    result = group_and_aggregate(
        df,
        group_by='country',
        agg_column='cases',
        agg_func=['sum', 'mean', 'count']
    )
    
    assert 'sum' in result.columns or result.columns.nlevels > 1
    # Check that multiple aggregations were performed


def test_compare_groups() -> None:
    """Test comparing statistics across groups."""
    df = pd.DataFrame({
        'country': ['UK', 'UK', 'USA', 'USA', 'France', 'France'],
        'cases': [100, 150, 200, 250, 300, 350]
    })
    
    comparison = compare_groups(df, group_column='country', value_column='cases')
    
    assert 'UK' in comparison
    assert 'USA' in comparison
    assert 'France' in comparison
    assert comparison['UK']['mean'] == 125.0
    assert comparison['USA']['mean'] == 225.0
    assert comparison['France']['mean'] == 325.0


# ==============================================================================
# Tests for DataAnalyzer Class
# ==============================================================================

def test_data_analyzer_initialization() -> None:
    """Test DataAnalyzer initialization."""
    df = pd.DataFrame({
        'country': ['UK', 'USA'],
        'cases': [100, 200]
    })
    
    analyzer = DataAnalyzer(df)
    
    assert analyzer is not None
    assert len(analyzer.df) == 2


def test_data_analyzer_filter_method() -> None:
    """Test DataAnalyzer filter method."""
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 300]
    })
    
    analyzer = DataAnalyzer(df)
    result = analyzer.filter_by('country', 'UK').get_data()
    
    assert len(result) == 1
    assert result['country'].iloc[0] == 'UK'


def test_data_analyzer_chain_operations() -> None:
    """Test chaining multiple analysis operations."""
    df = pd.DataFrame({
        'country': ['UK', 'UK', 'USA', 'USA', 'France'],
        'year': [2020, 2021, 2020, 2021, 2020],
        'cases': [100, 150, 200, 250, 300]
    })
    
    analyzer = DataAnalyzer(df)
    result = (analyzer
              .filter_by('year', 2020)
              .group_by('country')
              .aggregate('cases', 'sum')
              .get_data())
    
    assert len(result) <= 3  # Filtered by year first


def test_data_analyzer_get_summary() -> None:
    """Test getting summary statistics."""
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 300]
    })
    
    analyzer = DataAnalyzer(df)
    summary = analyzer.get_summary(['cases'])
    
    assert 'cases' in summary
    assert 'mean' in summary['cases']
    assert summary['cases']['mean'] == 200.0


def test_data_analyzer_reset() -> None:
    """Test resetting analyzer to original data."""
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 300]
    })
    
    analyzer = DataAnalyzer(df)
    analyzer.filter_by('country', 'UK')
    
    assert len(analyzer.get_data()) == 1
    
    analyzer.reset()
    
    assert len(analyzer.get_data()) == 3


def test_data_analyzer_get_trends() -> None:
    """Test trend analysis through analyzer."""
    df = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=5, freq='D'),
        'country': ['UK'] * 5,
        'cases': [100, 110, 120, 130, 140]
    })
    
    analyzer = DataAnalyzer(df)
    trends = analyzer.get_trends(date_column='date', value_column='cases')
    
    assert 'total' in trends
    assert 'average' in trends
    assert trends['growth_rate'] > 0

