"""
Tests for the main module of the Public Health Data Insights Dashboard.

Following TDD, these tests come before the full implementation.
"""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests

from src.main import (
    load_dataset,
    load_json_dataset,
    load_from_api,
    load_to_database,
    read_from_database
)


# ==============================================================================
# Tests for CSV Loading (load_dataset)
# ==============================================================================

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


def test_load_dataset_handles_empty_csv(tmp_path: Path) -> None:
    """
    Test that load_dataset can handle an empty CSV (just headers).
    """
    csv_content = "country,year,cases\n"
    csv_path = tmp_path / "empty_data.csv"
    csv_path.write_text(csv_content)

    df = load_dataset(csv_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert list(df.columns) == ["country", "year", "cases"]


def test_load_dataset_handles_various_data_types(tmp_path: Path) -> None:
    """
    Test that load_dataset correctly loads various data types.
    """
    csv_content = "country,date,cases,rate\nUK,2020-01-01,100,0.5\nFrance,2020-01-02,200,0.75\n"
    csv_path = tmp_path / "typed_data.csv"
    csv_path.write_text(csv_content)

    df = load_dataset(csv_path)

    assert len(df) == 2
    assert df['cases'].dtype == 'int64'
    assert df['rate'].dtype == 'float64'


# ==============================================================================
# Tests for JSON Loading (load_json_dataset)
# ==============================================================================

def test_load_json_dataset_returns_dataframe(tmp_path: Path) -> None:
    """
    Test loading a valid JSON file into a DataFrame.
    """
    json_data = [
        {"country": "UK", "year": 2020, "cases": 100},
        {"country": "UK", "year": 2021, "cases": 150}
    ]
    json_path = tmp_path / "health_data.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f)

    df = load_json_dataset(json_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["country", "year", "cases"]


def test_load_json_dataset_raises_for_missing_file(tmp_path: Path) -> None:
    """
    Test that load_json_dataset raises FileNotFoundError for missing files.
    """
    missing_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_json_dataset(missing_path)


def test_load_json_dataset_raises_for_invalid_json(tmp_path: Path) -> None:
    """
    Test that load_json_dataset raises ValueError for invalid JSON.
    """
    invalid_json_path = tmp_path / "invalid.json"
    invalid_json_path.write_text("{invalid json content")

    with pytest.raises(ValueError, match="Invalid JSON format"):
        load_json_dataset(invalid_json_path)


def test_load_json_dataset_handles_empty_list(tmp_path: Path) -> None:
    """
    Test that load_json_dataset can handle an empty JSON array.
    """
    json_path = tmp_path / "empty.json"
    with open(json_path, 'w') as f:
        json.dump([], f)

    df = load_json_dataset(json_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# ==============================================================================
# Tests for API Loading (load_from_api)
# ==============================================================================

def test_load_from_api_success(mocker) -> None:
    """
    Test successful API data loading with a mocked response.
    """
    # Mock response
    mock_data = [
        {"country": "USA", "cases": 1000},
        {"country": "UK", "cases": 500}
    ]
    mock_response = Mock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None
    
    mocker.patch('requests.get', return_value=mock_response)

    df = load_from_api("https://api.example.com/health-data")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["country", "cases"]


def test_load_from_api_with_nested_data(mocker) -> None:
    """
    Test API loading with nested JSON using data_key parameter.
    """
    mock_data = {
        "status": "success",
        "data": [
            {"country": "USA", "cases": 1000},
            {"country": "UK", "cases": 500}
        ]
    }
    mock_response = Mock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None
    
    mocker.patch('requests.get', return_value=mock_response)

    df = load_from_api("https://api.example.com/health-data", data_key="data")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_load_from_api_with_params(mocker) -> None:
    """
    Test API loading with query parameters.
    """
    mock_data = [{"country": "USA", "cases": 1000}]
    mock_response = Mock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None
    
    mock_get = mocker.patch('requests.get', return_value=mock_response)

    params = {"country": "USA", "year": 2020}
    df = load_from_api("https://api.example.com/health-data", params=params)

    # Verify that requests.get was called with correct parameters
    mock_get.assert_called_once()
    assert mock_get.call_args[1]['params'] == params


def test_load_from_api_handles_request_error(mocker) -> None:
    """
    Test that load_from_api raises exception when request fails.
    """
    mocker.patch('requests.get', side_effect=requests.RequestException("Network error"))

    with pytest.raises(requests.RequestException, match="API request failed"):
        load_from_api("https://api.example.com/health-data")


def test_load_from_api_handles_dict_response(mocker) -> None:
    """
    Test API loading when response is a dictionary with nested list.
    """
    mock_data = {
        "results": [
            {"country": "USA", "cases": 1000}
        ]
    }
    mock_response = Mock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None
    
    mocker.patch('requests.get', return_value=mock_response)

    df = load_from_api("https://api.example.com/health-data")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1


# ==============================================================================
# Tests for Database Operations
# ==============================================================================

def test_load_to_database_success(tmp_path: Path) -> None:
    """
    Test successfully loading a DataFrame to SQLite database.
    """
    df = pd.DataFrame({
        "country": ["UK", "USA"],
        "year": [2020, 2020],
        "cases": [100, 200]
    })
    db_path = tmp_path / "test_health.db"
    
    engine = load_to_database(df, db_path, "health_data")
    
    assert engine is not None
    assert db_path.exists()


def test_load_to_database_raises_for_empty_dataframe(tmp_path: Path) -> None:
    """
    Test that load_to_database raises ValueError for empty DataFrame.
    """
    df = pd.DataFrame()
    db_path = tmp_path / "test.db"
    
    with pytest.raises(ValueError, match="Cannot load empty DataFrame"):
        load_to_database(df, db_path, "test_table")


def test_load_to_database_raises_for_invalid_table_name(tmp_path: Path) -> None:
    """
    Test that load_to_database raises ValueError for invalid table name.
    """
    df = pd.DataFrame({"col": [1, 2]})
    db_path = tmp_path / "test.db"
    
    with pytest.raises(ValueError, match="Invalid table name"):
        load_to_database(df, db_path, "")


def test_read_from_database_success(tmp_path: Path) -> None:
    """
    Test successfully reading data from database.
    """
    # First, create and populate a database
    df_original = pd.DataFrame({
        "country": ["UK", "USA"],
        "year": [2020, 2020],
        "cases": [100, 200]
    })
    db_path = tmp_path / "test_health.db"
    load_to_database(df_original, db_path, "health_data")
    
    # Now read it back
    df_read = read_from_database(db_path, "health_data")
    
    assert isinstance(df_read, pd.DataFrame)
    assert len(df_read) == 2
    pd.testing.assert_frame_equal(df_original, df_read)


def test_read_from_database_with_query(tmp_path: Path) -> None:
    """
    Test reading from database with a SQL query.
    """
    df_original = pd.DataFrame({
        "country": ["UK", "USA", "France"],
        "year": [2020, 2020, 2020],
        "cases": [100, 200, 150]
    })
    db_path = tmp_path / "test_health.db"
    load_to_database(df_original, db_path, "health_data")
    
    # Query for specific country
    query = "SELECT * FROM health_data WHERE country = 'UK'"
    df_filtered = read_from_database(db_path, "health_data", query=query)
    
    assert len(df_filtered) == 1
    assert df_filtered.iloc[0]["country"] == "UK"


def test_read_from_database_raises_for_missing_db(tmp_path: Path) -> None:
    """
    Test that read_from_database raises FileNotFoundError for missing database.
    """
    db_path = tmp_path / "missing.db"
    
    with pytest.raises(FileNotFoundError):
        read_from_database(db_path, "health_data")


def test_read_from_database_raises_for_missing_table(tmp_path: Path) -> None:
    """
    Test that read_from_database raises ValueError for non-existent table.
    """
    df = pd.DataFrame({"col": [1, 2]})
    db_path = tmp_path / "test.db"
    load_to_database(df, db_path, "existing_table")
    
    with pytest.raises(ValueError, match="Table 'non_existent' does not exist"):
        read_from_database(db_path, "non_existent")


def test_database_append_mode(tmp_path: Path) -> None:
    """
    Test that data can be appended to an existing table.
    """
    df1 = pd.DataFrame({"country": ["UK"], "cases": [100]})
    df2 = pd.DataFrame({"country": ["USA"], "cases": [200]})
    db_path = tmp_path / "test.db"
    
    load_to_database(df1, db_path, "health_data", if_exists='replace')
    load_to_database(df2, db_path, "health_data", if_exists='append')
    
    df_result = read_from_database(db_path, "health_data")
    
    assert len(df_result) == 2
    assert set(df_result["country"]) == {"UK", "USA"}
