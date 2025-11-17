"""
Tests for the main module of the Public Health Data Insights Dashboard.

Following TDD, these tests come before the full implementation.
"""

from pathlib import Path

import pandas as pd
import pytest

from src.main import load_dataset


def test_load_dataset_returns_dataframe(tmp_path: Path) -> None:
    """
    Given a small CSV file, load_dataset should return a pandas DataFrame
    with the correct columns and number of rows.
    """
    # Arrange: create a temporary CSV representing a tiny public health dataset
    csv_content = "country,year,cases\nUK,2020,100\nUK,2021,150\n"
    csv_path = tmp_path / "sample_health_data.csv"
    csv_path.write_text(csv_content)

    # Act
    df = load_dataset(csv_path)

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["country", "year", "cases"]
    assert len(df) == 2


def test_load_dataset_raises_for_missing_file(tmp_path: Path) -> None:
    """
    If the CSV file does not exist, load_dataset should raise FileNotFoundError.
    """
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_dataset(missing_path)
