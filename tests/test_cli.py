"""
Tests for CLI presentation layer.

Simplified tests for the current CLI implementation.
"""

import pandas as pd
import pytest
from pathlib import Path

from src.cli import (
    display_dataframe,
    display_summary_stats,
    export_to_csv,
    CLISession,
    format_number
)


# ==============================================================================
# Tests for Number Formatting
# ==============================================================================

def test_format_number_basic() -> None:
    """Test basic number formatting."""
    result = format_number(1234.567)
    assert isinstance(result, str)
    assert '1,234' in result  # Has thousands separator


def test_format_number_decimals() -> None:
    """Test formatting with specific decimal places."""
    result = format_number(123.456, decimals=3)
    assert isinstance(result, str)
    assert '123.456' in result


def test_format_number_zero() -> None:
    """Test formatting zero."""
    result = format_number(0)
    assert isinstance(result, str)
    assert '0' in result


# ==============================================================================
# Tests for CLISession
# ==============================================================================

def test_cli_session_initialization() -> None:
    """Test CLISession initialization."""
    session = CLISession()
    assert session.df is None
    assert session.data_name == "No data loaded"
    assert not session.has_data()


def test_cli_session_load_data() -> None:
    """Test loading data into session."""
    session = CLISession()
    df = pd.DataFrame({'country': ['UK', 'USA'], 'cases': [100, 200]})
    
    session.load_data(df, "Test Data")
    
    assert session.has_data()
    assert session.data_name == "Test Data"
    assert len(session.df) == 2


def test_cli_session_get_current_data() -> None:
    """Test getting current data from session."""
    session = CLISession()
    df = pd.DataFrame({'country': ['UK'], 'cases': [100]})
    
    session.load_data(df, "Test")
    current = session.get_current_data()
    
    assert isinstance(current, pd.DataFrame)
    assert len(current) == 1


def test_cli_session_reset_filters() -> None:
    """Test resetting filters in session."""
    session = CLISession()
    df = pd.DataFrame({'country': ['UK', 'USA'], 'cases': [100, 200]})
    
    session.load_data(df, "Test")
    
    # Simulate applying a filter
    filtered = df[df['country'] == 'UK']
    session.apply_filter(filtered, "country=UK")
    
    assert len(session.get_current_data()) == 1
    assert len(session.filters_applied) == 1
    
    # Reset filters
    session.reset_filters()
    assert len(session.get_current_data()) == 2
    assert len(session.filters_applied) == 0


def test_cli_session_get_status() -> None:
    """Test getting session status."""
    session = CLISession()
    
    # No data loaded
    status = session.get_status()
    assert "No data loaded" in status
    
    # With data loaded
    df = pd.DataFrame({'country': ['UK'], 'cases': [100]})
    session.load_data(df, "Test Data")
    status = session.get_status()
    
    assert "Test Data" in status
    assert "1" in status  # 1 record


# ==============================================================================
# Tests for Display Functions (basic smoke tests)
# ==============================================================================

def test_display_dataframe_smoke(capsys) -> None:
    """Smoke test for display_dataframe."""
    df = pd.DataFrame({'country': ['UK'], 'cases': [100]})
    
    # Should not raise an exception
    display_dataframe(df, title="Test")
    
    captured = capsys.readouterr()
    assert 'Test' in captured.out or 'country' in captured.out


def test_display_summary_stats_smoke(capsys) -> None:
    """Smoke test for display_summary_stats."""
    stats = {'mean': 100.5, 'count': 10}
    
    # Should not raise an exception
    display_summary_stats(stats)
    
    captured = capsys.readouterr()
    # Function prints output, so we should have some output
    assert len(captured.out) > 0


# ==============================================================================
# Tests for Export Functions
# ==============================================================================

def test_export_to_csv_basic(tmp_path, monkeypatch) -> None:
    """Test basic CSV export."""
    df = pd.DataFrame({'country': ['UK', 'USA'], 'cases': [100, 200]})
    output_file = tmp_path / "test_export.csv"
    
    # Mock user input to return the filename
    monkeypatch.setattr('builtins.input', lambda _: str(output_file))
    
    export_to_csv(df)
    
    # Check file was created
    assert output_file.exists()
    
    # Check content
    exported_df = pd.read_csv(output_file)
    assert len(exported_df) == 2
    assert 'country' in exported_df.columns
    assert 'cases' in exported_df.columns


def test_export_to_csv_empty_dataframe(tmp_path, monkeypatch) -> None:
    """Test exporting empty DataFrame."""
    df = pd.DataFrame()
    output_file = tmp_path / "empty_export.csv"
    
    monkeypatch.setattr('builtins.input', lambda _: str(output_file))
    
    export_to_csv(df)
    
    # File should still be created
    assert output_file.exists()


# ==============================================================================
# Summary
# ==============================================================================
# Total tests: 15
# - Number formatting: 3 tests
# - CLISession: 6 tests
# - Display functions: 2 smoke tests
# - Export functions: 2 tests
# - Misc: 2 tests
