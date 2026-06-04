"""
Tests for CRUD (Create, Read, Update, Delete) operations.

Following TDD, these tests are written before implementation.
Step 5: Extension Features - CRUD Operations
"""

import pandas as pd
import pytest
from pathlib import Path
from sqlalchemy import create_engine, inspect

from src.crud import (
    create_record,
    create_records,
    read_records,
    read_record_by_id,
    update_record,
    update_records,
    delete_record,
    delete_records,
    get_table_info,
    list_tables,
    table_exists,
    CRUDManager
)


# ==============================================================================
# Tests for Create Operations
# ==============================================================================

def test_create_single_record(tmp_path: Path) -> None:
    """
    Test creating a single record in the database.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create initial table with some data
    df = pd.DataFrame({
        'id': [1, 2],
        'country': ['UK', 'USA'],
        'cases': [100, 200]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    # Create new record
    new_record = {'id': 3, 'country': 'France', 'cases': 150}
    result = create_record(db_path, 'health_data', new_record)
    
    assert result is True
    
    # Verify record was added
    df_result = pd.read_sql_table('health_data', engine)
    assert len(df_result) == 3
    assert df_result[df_result['id'] == 3].iloc[0]['country'] == 'France'


def test_create_multiple_records(tmp_path: Path) -> None:
    """
    Test creating multiple records at once.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create initial table
    df = pd.DataFrame({'id': [1], 'country': ['UK'], 'cases': [100]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    # Create multiple records
    new_records = [
        {'id': 2, 'country': 'USA', 'cases': 200},
        {'id': 3, 'country': 'France', 'cases': 150}
    ]
    result = create_records(db_path, 'health_data', new_records)
    
    assert result is True
    
    # Verify records were added
    df_result = pd.read_sql_table('health_data', engine)
    assert len(df_result) == 3


def test_create_record_with_missing_columns(tmp_path: Path) -> None:
    """
    Test that creating a record with missing required columns raises error.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1], 'country': ['UK'], 'cases': [100]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    # Try to create record with missing column
    incomplete_record = {'id': 2, 'country': 'USA'}  # missing 'cases'
    
    with pytest.raises(ValueError, match="Missing required columns"):
        create_record(db_path, 'health_data', incomplete_record)


def test_create_record_in_nonexistent_table(tmp_path: Path) -> None:
    """
    Test creating record in non-existent table raises error.
    """
    db_path = tmp_path / "test.db"
    
    with pytest.raises(ValueError, match="Table .* does not exist"):
        create_record(db_path, 'nonexistent_table', {'id': 1})


# ==============================================================================
# Tests for Read Operations
# ==============================================================================

def test_read_all_records(tmp_path: Path) -> None:
    """
    Test reading all records from a table.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    result = read_records(db_path, 'health_data')
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ['id', 'country', 'cases']


def test_read_records_with_filter(tmp_path: Path) -> None:
    """
    Test reading records with WHERE clause filter.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    result = read_records(db_path, 'health_data', where="country='UK'")
    
    assert len(result) == 1
    assert result.iloc[0]['country'] == 'UK'


def test_read_record_by_id(tmp_path: Path) -> None:
    """
    Test reading a single record by ID.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    result = read_record_by_id(db_path, 'health_data', 'id', 2)
    
    assert isinstance(result, dict)
    assert result['id'] == 2
    assert result['country'] == 'USA'


def test_read_nonexistent_record_by_id(tmp_path: Path) -> None:
    """
    Test reading non-existent record returns None.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2], 'country': ['UK', 'USA'], 'cases': [100, 200]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    result = read_record_by_id(db_path, 'health_data', 'id', 999)
    
    assert result is None


def test_read_records_with_limit(tmp_path: Path) -> None:
    """
    Test reading records with LIMIT clause.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': list(range(1, 11)),
        'country': ['Country' + str(i) for i in range(1, 11)],
        'cases': list(range(100, 200, 10))
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    result = read_records(db_path, 'health_data', limit=5)
    
    assert len(result) == 5


# ==============================================================================
# Tests for Update Operations
# ==============================================================================

def test_update_single_record(tmp_path: Path) -> None:
    """
    Test updating a single record.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    # Update cases for UK
    updates = {'cases': 120}
    rows_affected = update_record(db_path, 'health_data', updates, where="country='UK'")
    
    assert rows_affected == 1
    
    # Verify update
    df_result = pd.read_sql_table('health_data', engine)
    uk_cases = df_result[df_result['country'] == 'UK'].iloc[0]['cases']
    assert uk_cases == 120


def test_update_multiple_records(tmp_path: Path) -> None:
    """
    Test updating multiple records at once.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150],
        'status': ['active', 'active', 'inactive']
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    # Update all active records
    updates = {'cases': 0}
    rows_affected = update_record(db_path, 'health_data', updates, where="status='active'")
    
    assert rows_affected == 2
    
    # Verify updates
    df_result = pd.read_sql_table('health_data', engine)
    active_cases = df_result[df_result['status'] == 'active']['cases'].tolist()
    assert all(cases == 0 for cases in active_cases)


def test_update_by_id(tmp_path: Path) -> None:
    """
    Test updating a record by ID using helper function.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    updates = {'country': 'United Kingdom', 'cases': 110}
    rows_affected = update_records(db_path, 'health_data', 'id', 1, updates)
    
    assert rows_affected == 1
    
    # Verify
    df_result = pd.read_sql_table('health_data', engine)
    record = df_result[df_result['id'] == 1].iloc[0]
    assert record['country'] == 'United Kingdom'
    assert record['cases'] == 110


def test_update_nonexistent_record(tmp_path: Path) -> None:
    """
    Test updating non-existent record returns 0 rows affected.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2], 'country': ['UK', 'USA'], 'cases': [100, 200]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    rows_affected = update_record(db_path, 'health_data', {'cases': 999}, where="id=999")
    
    assert rows_affected == 0


def test_update_without_where_clause_raises_error(tmp_path: Path) -> None:
    """
    Test that updating without WHERE clause raises error (safety check).
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2], 'country': ['UK', 'USA'], 'cases': [100, 200]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    with pytest.raises(ValueError, match="WHERE clause is required"):
        update_record(db_path, 'health_data', {'cases': 0}, where=None)


# ==============================================================================
# Tests for Delete Operations
# ==============================================================================

def test_delete_single_record(tmp_path: Path) -> None:
    """
    Test deleting a single record.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    rows_affected = delete_record(db_path, 'health_data', where="id=2")
    
    assert rows_affected == 1
    
    # Verify deletion
    df_result = pd.read_sql_table('health_data', engine)
    assert len(df_result) == 2
    assert 2 not in df_result['id'].values


def test_delete_multiple_records(tmp_path: Path) -> None:
    """
    Test deleting multiple records.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'country': ['UK', 'USA', 'France', 'Germany'],
        'cases': [100, 200, 150, 180],
        'status': ['active', 'inactive', 'inactive', 'active']
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    rows_affected = delete_record(db_path, 'health_data', where="status='inactive'")
    
    assert rows_affected == 2
    
    # Verify deletion
    df_result = pd.read_sql_table('health_data', engine)
    assert len(df_result) == 2
    assert all(df_result['status'] == 'active')


def test_delete_by_id(tmp_path: Path) -> None:
    """
    Test deleting a record by ID using helper function.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2, 3], 'country': ['UK', 'USA', 'France'], 'cases': [100, 200, 150]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    rows_affected = delete_records(db_path, 'health_data', 'id', 2)
    
    assert rows_affected == 1
    
    # Verify
    df_result = pd.read_sql_table('health_data', engine)
    assert 2 not in df_result['id'].values


def test_delete_nonexistent_record(tmp_path: Path) -> None:
    """
    Test deleting non-existent record returns 0 rows affected.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2], 'country': ['UK', 'USA'], 'cases': [100, 200]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    rows_affected = delete_record(db_path, 'health_data', where="id=999")
    
    assert rows_affected == 0


def test_delete_without_where_clause_raises_error(tmp_path: Path) -> None:
    """
    Test that deleting without WHERE clause raises error (safety check).
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2], 'country': ['UK', 'USA'], 'cases': [100, 200]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    with pytest.raises(ValueError, match="WHERE clause is required"):
        delete_record(db_path, 'health_data', where=None)


# ==============================================================================
# Tests for Database Utility Operations
# ==============================================================================

def test_list_tables(tmp_path: Path) -> None:
    """
    Test listing all tables in database.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create multiple tables
    pd.DataFrame({'id': [1]}).to_sql('table1', engine, if_exists='replace', index=False)
    pd.DataFrame({'id': [1]}).to_sql('table2', engine, if_exists='replace', index=False)
    pd.DataFrame({'id': [1]}).to_sql('table3', engine, if_exists='replace', index=False)
    
    tables = list_tables(db_path)
    
    assert isinstance(tables, list)
    assert len(tables) == 3
    assert 'table1' in tables
    assert 'table2' in tables
    assert 'table3' in tables


def test_table_exists(tmp_path: Path) -> None:
    """
    Test checking if table exists.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    pd.DataFrame({'id': [1]}).to_sql('existing_table', engine, if_exists='replace', index=False)
    
    assert table_exists(db_path, 'existing_table') is True
    assert table_exists(db_path, 'nonexistent_table') is False


def test_get_table_info(tmp_path: Path) -> None:
    """
    Test getting table information (columns and types).
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({
        'id': [1, 2],
        'country': ['UK', 'USA'],
        'cases': [100, 200],
        'rate': [0.5, 0.75]
    })
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    info = get_table_info(db_path, 'health_data')
    
    assert isinstance(info, dict)
    assert 'columns' in info
    assert 'row_count' in info
    assert len(info['columns']) == 4
    assert info['row_count'] == 2


# ==============================================================================
# Tests for CRUDManager Class
# ==============================================================================

def test_crud_manager_initialization(tmp_path: Path) -> None:
    """
    Test CRUDManager initialization.
    """
    db_path = tmp_path / "test.db"
    manager = CRUDManager(db_path)
    
    assert manager.db_path == db_path
    assert manager.engine is not None


def test_crud_manager_create_and_read(tmp_path: Path) -> None:
    """
    Test CRUDManager create and read operations.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create initial table
    pd.DataFrame({'id': [1], 'country': ['UK'], 'cases': [100]}).to_sql(
        'health_data', engine, if_exists='replace', index=False
    )
    
    manager = CRUDManager(db_path)
    
    # Create new record
    manager.create('health_data', {'id': 2, 'country': 'USA', 'cases': 200})
    
    # Read all records
    result = manager.read('health_data')
    assert len(result) == 2


def test_crud_manager_update_and_delete(tmp_path: Path) -> None:
    """
    Test CRUDManager update and delete operations.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    df = pd.DataFrame({'id': [1, 2], 'country': ['UK', 'USA'], 'cases': [100, 200]})
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    
    manager = CRUDManager(db_path)
    
    # Update record
    manager.update('health_data', {'cases': 150}, where="id=1")
    result = manager.read('health_data', where="id=1")
    assert result.iloc[0]['cases'] == 150
    
    # Delete record
    manager.delete('health_data', where="id=2")
    result = manager.read('health_data')
    assert len(result) == 1


def test_crud_manager_get_tables(tmp_path: Path) -> None:
    """
    Test CRUDManager listing tables.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    pd.DataFrame({'id': [1]}).to_sql('table1', engine, if_exists='replace', index=False)
    pd.DataFrame({'id': [1]}).to_sql('table2', engine, if_exists='replace', index=False)
    
    manager = CRUDManager(db_path)
    tables = manager.get_tables()
    
    assert len(tables) == 2
    assert 'table1' in tables


def test_crud_manager_table_exists(tmp_path: Path) -> None:
    """
    Test CRUDManager checking table existence.
    """
    db_path = tmp_path / "test.db"
    engine = create_engine(f'sqlite:///{db_path}')
    
    pd.DataFrame({'id': [1]}).to_sql('existing', engine, if_exists='replace', index=False)
    
    manager = CRUDManager(db_path)
    
    assert manager.table_exists('existing') is True
    assert manager.table_exists('nonexistent') is False

