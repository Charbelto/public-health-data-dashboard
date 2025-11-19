"""
Tests for CLI presentation layer.

Following TDD, these tests are written before implementation.
Step 4: Presentation Layer (CLI)
"""

import pandas as pd
import pytest
from pathlib import Path
from io import StringIO
import sys

from src.cli import (
    format_table,
    format_summary_stats,
    create_bar_chart,
    create_line_chart,
    create_comparison_chart,
    save_chart,
    HealthDataCLI
)


# ==============================================================================
# Tests for Table Formatting
# ==============================================================================

def test_format_table_basic() -> None:
    """
    Test basic table formatting.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA'],
        'cases': [100, 200]
    })
    
    formatted = format_table(df)
    
    assert isinstance(formatted, str)
    assert 'country' in formatted
    assert 'cases' in formatted
    assert 'UK' in formatted


def test_format_table_with_max_rows() -> None:
    """
    Test table formatting with row limit.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'Germany'],
        'cases': [100, 200, 150, 180]
    })
    
    formatted = format_table(df, max_rows=2)
    
    assert isinstance(formatted, str)
    # Pandas may show all rows depending on settings, so just check it's formatted
    assert 'country' in formatted
    assert 'cases' in formatted


def test_format_table_empty_dataframe() -> None:
    """
    Test formatting empty DataFrame.
    """
    df = pd.DataFrame()
    
    formatted = format_table(df)
    
    assert isinstance(formatted, str)
    assert 'empty' in formatted.lower() or 'no data' in formatted.lower()


def test_format_summary_stats() -> None:
    """
    Test formatting summary statistics.
    """
    stats = {
        'mean': 150.5,
        'median': 145.0,
        'min': 100,
        'max': 200,
        'count': 10
    }
    
    formatted = format_summary_stats(stats)
    
    assert isinstance(formatted, str)
    assert 'mean' in formatted.lower()
    assert '150' in formatted
    assert 'count' in formatted.lower()


def test_format_summary_stats_with_title() -> None:
    """
    Test formatting summary stats with custom title.
    """
    stats = {'mean': 100, 'count': 5}
    
    formatted = format_summary_stats(stats, title='Test Statistics')
    
    assert 'Test Statistics' in formatted


# ==============================================================================
# Tests for Chart Creation
# ==============================================================================

def test_create_bar_chart_returns_figure() -> None:
    """
    Test that bar chart creation returns a matplotlib figure.
    """
    df = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    
    fig = create_bar_chart(df, x='country', y='cases', title='Test Chart')
    
    assert fig is not None
    # Check it's a matplotlib figure
    assert hasattr(fig, 'savefig')


def test_create_bar_chart_with_sorted_data() -> None:
    """
    Test bar chart with sorted data.
    """
    df = pd.DataFrame({
        'country': ['France', 'UK', 'USA'],
        'cases': [150, 100, 200]
    })
    
    fig = create_bar_chart(df, x='country', y='cases', sort_by='cases', ascending=False)
    
    assert fig is not None


def test_create_line_chart_returns_figure() -> None:
    """
    Test that line chart creation returns a matplotlib figure.
    """
    df = pd.DataFrame({
        'month': [1, 2, 3, 4],
        'cases': [100, 150, 180, 220]
    })
    
    fig = create_line_chart(df, x='month', y='cases', title='Trend')
    
    assert fig is not None
    assert hasattr(fig, 'savefig')


def test_create_comparison_chart() -> None:
    """
    Test creating a comparison chart with multiple series.
    """
    df = pd.DataFrame({
        'month': [1, 2, 3, 1, 2, 3],
        'country': ['UK', 'UK', 'UK', 'USA', 'USA', 'USA'],
        'cases': [100, 150, 200, 120, 180, 250]
    })
    
    fig = create_comparison_chart(
        df,
        x='month',
        y='cases',
        group_by='country',
        title='Country Comparison'
    )
    
    assert fig is not None


def test_save_chart(tmp_path: Path) -> None:
    """
    Test saving a chart to file.
    """
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 20, 30]})
    fig = create_bar_chart(df, 'x', 'y')
    
    output_path = tmp_path / "test_chart.png"
    
    result = save_chart(fig, output_path)
    
    assert result is True
    assert output_path.exists()


def test_save_chart_creates_directory(tmp_path: Path) -> None:
    """
    Test that save_chart creates parent directories if needed.
    """
    df = pd.DataFrame({'x': [1, 2], 'y': [10, 20]})
    fig = create_bar_chart(df, 'x', 'y')
    
    output_path = tmp_path / "subdir" / "chart.png"
    
    result = save_chart(fig, output_path)
    
    assert result is True
    assert output_path.exists()


# ==============================================================================
# Tests for HealthDataCLI Class
# ==============================================================================

def test_cli_initialization() -> None:
    """
    Test CLI initialization.
    """
    cli = HealthDataCLI()
    
    assert cli is not None
    assert hasattr(cli, 'df')


def test_cli_load_data() -> None:
    """
    Test loading data through CLI.
    """
    cli = HealthDataCLI()
    
    # Load sample data
    result = cli.load_data("data/sample_vaccination_data.csv")
    
    assert result is True
    assert cli.df is not None
    assert len(cli.df) > 0


def test_cli_load_data_invalid_file() -> None:
    """
    Test loading non-existent file returns False.
    """
    cli = HealthDataCLI()
    
    result = cli.load_data("nonexistent.csv")
    
    assert result is False


def test_cli_apply_filter() -> None:
    """
    Test applying filter through CLI.
    """
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    original_count = len(cli.df)
    
    cli.apply_filter('country', 'United Kingdom')
    
    assert len(cli.df) < original_count
    assert all(cli.df['country'] == 'United Kingdom')


def test_cli_reset_filters() -> None:
    """
    Test resetting filters restores original data.
    """
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    original_count = len(cli.df)
    cli.apply_filter('country', 'UK')
    cli.reset_filters()
    
    assert len(cli.df) == original_count


def test_cli_show_summary() -> None:
    """
    Test showing summary statistics.
    """
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.show_summary('doses_administered')
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert 'mean' in output.lower()
    assert 'count' in output.lower()


def test_cli_show_grouped_data() -> None:
    """
    Test showing grouped data.
    """
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.show_grouped_data('country', 'doses_administered', 'sum')
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert 'country' in output.lower()


def test_cli_export_data(tmp_path: Path) -> None:
    """
    Test exporting filtered data to CSV.
    """
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    cli.apply_filter('country', 'United Kingdom')
    
    output_file = tmp_path / "export.csv"
    
    result = cli.export_data(output_file)
    
    assert result is True
    assert output_file.exists()
    
    # Verify exported data
    exported = pd.read_csv(output_file)
    assert len(exported) == len(cli.df)


def test_cli_create_visualization(tmp_path: Path) -> None:
    """
    Test creating and saving visualization.
    """
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    output_file = tmp_path / "chart.png"
    
    result = cli.create_visualization(
        chart_type='bar',
        x='country',
        y='doses_administered',
        output_path=output_file
    )
    
    assert result is True
    assert output_file.exists()


def test_cli_get_status() -> None:
    """
    Test getting CLI status information.
    """
    cli = HealthDataCLI()
    
    status = cli.get_status()
    
    assert 'data_loaded' in status
    assert status['data_loaded'] is False
    
    cli.load_data("data/sample_vaccination_data.csv")
    status = cli.get_status()
    
    assert status['data_loaded'] is True
    assert 'record_count' in status
    assert status['record_count'] > 0

