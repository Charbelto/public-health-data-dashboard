"""
CRUD (Create, Read, Update, Delete) operations for database management.

Part 5: Extension Features - Database CRUD Operations
"""

from pathlib import Path
from typing import Union, Optional, Dict, List, Any
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


def _get_engine(db_path: Union[str, Path]) -> Engine:
    """
    Create and return a database engine.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    
    Returns
    -------
    Engine
        SQLAlchemy engine instance.
    """
    db_path = Path(db_path)
    return create_engine(f'sqlite:///{db_path}')


def _validate_table_exists(engine: Engine, table_name: str) -> None:
    """
    Validate that a table exists in the database.
    
    Parameters
    ----------
    engine : Engine
        SQLAlchemy engine instance.
    table_name : str
        Name of the table to check.
    
    Raises
    ------
    ValueError
        If the table does not exist.
    """
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table '{table_name}' does not exist in database")


def create_record(db_path: Union[str, Path], table_name: str, record: Dict[str, Any]) -> bool:
    """
    Create (insert) a single record in the database table.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to insert into.
    record : dict
        Dictionary containing column names and values.
    
    Returns
    -------
    bool
        True if the record was successfully created.
    
    Raises
    ------
    ValueError
        If the table doesn't exist or record has missing columns.
    
    Examples
    --------
    >>> create_record("data/health.db", "patients", 
    ...               {"id": 1, "name": "John", "age": 30})
    True
    """
    engine = _get_engine(db_path)
    _validate_table_exists(engine, table_name)
    
    # Get existing columns to validate
    inspector = inspect(engine)
    existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
    
    # Check if record has all required columns (excluding auto-increment)
    missing_cols = set(existing_columns) - set(record.keys())
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Convert record to DataFrame and append
    df = pd.DataFrame([record])
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
    return True


def create_records(db_path: Union[str, Path], table_name: str, records: List[Dict[str, Any]]) -> bool:
    """
    Create (insert) multiple records in the database table.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to insert into.
    records : list of dict
        List of dictionaries, each containing column names and values.
    
    Returns
    -------
    bool
        True if all records were successfully created.
    
    Raises
    ------
    ValueError
        If the table doesn't exist or records have missing columns.
    
    Examples
    --------
    >>> records = [
    ...     {"id": 1, "name": "John", "age": 30},
    ...     {"id": 2, "name": "Jane", "age": 25}
    ... ]
    >>> create_records("data/health.db", "patients", records)
    True
    """
    engine = _get_engine(db_path)
    _validate_table_exists(engine, table_name)
    
    # Convert records to DataFrame and append
    df = pd.DataFrame(records)
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
    return True


def read_records(db_path: Union[str, Path], 
                 table_name: str,
                 where: Optional[str] = None,
                 columns: Optional[List[str]] = None,
                 limit: Optional[int] = None,
                 order_by: Optional[str] = None) -> pd.DataFrame:
    """
    Read records from the database table.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to read from.
    where : str, optional
        WHERE clause (without 'WHERE' keyword), e.g., "age > 25".
    columns : list of str, optional
        Specific columns to retrieve. If None, retrieves all columns.
    limit : int, optional
        Maximum number of records to return.
    order_by : str, optional
        ORDER BY clause (without 'ORDER BY' keyword), e.g., "age DESC".
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing the retrieved records.
    
    Raises
    ------
    ValueError
        If the table doesn't exist.
    
    Examples
    --------
    >>> read_records("data/health.db", "patients")  # Read all
    >>> read_records("data/health.db", "patients", where="age > 25", limit=10)
    """
    engine = _get_engine(db_path)
    _validate_table_exists(engine, table_name)
    
    # Build SQL query
    cols = ', '.join(columns) if columns else '*'
    query = f"SELECT {cols} FROM {table_name}"
    
    if where:
        query += f" WHERE {where}"
    
    if order_by:
        query += f" ORDER BY {order_by}"
    
    if limit:
        query += f" LIMIT {limit}"
    
    # Execute query
    df = pd.read_sql_query(query, engine)
    return df


def read_record_by_id(db_path: Union[str, Path], 
                      table_name: str,
                      id_column: str,
                      id_value: Any) -> Optional[Dict[str, Any]]:
    """
    Read a single record by its ID value.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to read from.
    id_column : str
        Name of the ID column.
    id_value : any
        Value of the ID to search for.
    
    Returns
    -------
    dict or None
        Dictionary containing the record, or None if not found.
    
    Examples
    --------
    >>> read_record_by_id("data/health.db", "patients", "id", 1)
    {'id': 1, 'name': 'John', 'age': 30}
    """
    df = read_records(db_path, table_name, where=f"{id_column}={id_value}", limit=1)
    
    if df.empty:
        return None
    
    return df.iloc[0].to_dict()


def update_record(db_path: Union[str, Path],
                  table_name: str,
                  updates: Dict[str, Any],
                  where: Optional[str] = None) -> int:
    """
    Update records in the database table.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to update.
    updates : dict
        Dictionary containing column names and new values.
    where : str
        WHERE clause (without 'WHERE' keyword), e.g., "id=1".
        REQUIRED for safety - prevents accidental update of all records.
    
    Returns
    -------
    int
        Number of rows affected.
    
    Raises
    ------
    ValueError
        If WHERE clause is not provided or table doesn't exist.
    
    Examples
    --------
    >>> update_record("data/health.db", "patients", 
    ...               {"age": 31}, where="id=1")
    1
    """
    if where is None:
        raise ValueError("WHERE clause is required for UPDATE operations (safety check)")
    
    engine = _get_engine(db_path)
    _validate_table_exists(engine, table_name)
    
    # Build UPDATE statement
    set_clause = ', '.join([f"{col}=:{col}" for col in updates.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
    
    # Execute update
    with engine.connect() as conn:
        result = conn.execute(text(query), updates)
        conn.commit()
        return result.rowcount


def update_records(db_path: Union[str, Path],
                   table_name: str,
                   id_column: str,
                   id_value: Any,
                   updates: Dict[str, Any]) -> int:
    """
    Update a specific record by its ID (convenience wrapper).
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to update.
    id_column : str
        Name of the ID column.
    id_value : any
        Value of the ID to update.
    updates : dict
        Dictionary containing column names and new values.
    
    Returns
    -------
    int
        Number of rows affected (should be 1 if successful).
    
    Examples
    --------
    >>> update_records("data/health.db", "patients", "id", 1, 
    ...                {"age": 31, "name": "John Smith"})
    1
    """
    where = f"{id_column}={id_value}"
    return update_record(db_path, table_name, updates, where=where)


def delete_record(db_path: Union[str, Path],
                  table_name: str,
                  where: Optional[str] = None) -> int:
    """
    Delete records from the database table.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to delete from.
    where : str
        WHERE clause (without 'WHERE' keyword), e.g., "id=1".
        REQUIRED for safety - prevents accidental deletion of all records.
    
    Returns
    -------
    int
        Number of rows affected (deleted).
    
    Raises
    ------
    ValueError
        If WHERE clause is not provided or table doesn't exist.
    
    Examples
    --------
    >>> delete_record("data/health.db", "patients", where="id=1")
    1
    """
    if where is None:
        raise ValueError("WHERE clause is required for DELETE operations (safety check)")
    
    engine = _get_engine(db_path)
    _validate_table_exists(engine, table_name)
    
    # Build DELETE statement
    query = f"DELETE FROM {table_name} WHERE {where}"
    
    # Execute delete
    with engine.connect() as conn:
        result = conn.execute(text(query))
        conn.commit()
        return result.rowcount


def delete_records(db_path: Union[str, Path],
                   table_name: str,
                   id_column: str,
                   id_value: Any) -> int:
    """
    Delete a specific record by its ID (convenience wrapper).
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to delete from.
    id_column : str
        Name of the ID column.
    id_value : any
        Value of the ID to delete.
    
    Returns
    -------
    int
        Number of rows affected (should be 1 if successful).
    
    Examples
    --------
    >>> delete_records("data/health.db", "patients", "id", 1)
    1
    """
    where = f"{id_column}={id_value}"
    return delete_record(db_path, table_name, where=where)


def list_tables(db_path: Union[str, Path]) -> List[str]:
    """
    List all tables in the database.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    
    Returns
    -------
    list of str
        List of table names.
    
    Examples
    --------
    >>> list_tables("data/health.db")
    ['patients', 'vaccinations', 'outbreaks']
    """
    engine = _get_engine(db_path)
    inspector = inspect(engine)
    return inspector.get_table_names()


def table_exists(db_path: Union[str, Path], table_name: str) -> bool:
    """
    Check if a table exists in the database.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table to check.
    
    Returns
    -------
    bool
        True if the table exists, False otherwise.
    
    Examples
    --------
    >>> table_exists("data/health.db", "patients")
    True
    """
    tables = list_tables(db_path)
    return table_name in tables


def get_table_info(db_path: Union[str, Path], table_name: str) -> Dict[str, Any]:
    """
    Get information about a table (columns, types, row count).
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    table_name : str
        Name of the table.
    
    Returns
    -------
    dict
        Dictionary containing table information:
        - 'columns': list of column dictionaries with 'name' and 'type'
        - 'row_count': number of rows in the table
    
    Raises
    ------
    ValueError
        If the table doesn't exist.
    
    Examples
    --------
    >>> get_table_info("data/health.db", "patients")
    {
        'columns': [
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': 'TEXT'},
            {'name': 'age', 'type': 'INTEGER'}
        ],
        'row_count': 100
    }
    """
    engine = _get_engine(db_path)
    _validate_table_exists(engine, table_name)
    
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    
    # Get row count
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = result.scalar()
    
    return {
        'columns': [{'name': col['name'], 'type': str(col['type'])} for col in columns],
        'row_count': row_count
    }


class CRUDManager:
    """
    A class-based interface for CRUD operations on a database.
    
    This provides a convenient object-oriented interface for database operations.
    
    Parameters
    ----------
    db_path : str or Path
        Path to the SQLite database.
    
    Examples
    --------
    >>> manager = CRUDManager("data/health.db")
    >>> manager.create("patients", {"id": 1, "name": "John", "age": 30})
    >>> patients = manager.read("patients", where="age > 25")
    >>> manager.update("patients", {"age": 31}, where="id=1")
    >>> manager.delete("patients", where="id=1")
    """
    
    def __init__(self, db_path: Union[str, Path]):
        """Initialize the CRUD manager with a database path."""
        self.db_path = Path(db_path)
        self.engine = _get_engine(db_path)
    
    def create(self, table_name: str, record: Dict[str, Any]) -> bool:
        """Create a single record. See create_record() for details."""
        return create_record(self.db_path, table_name, record)
    
    def create_many(self, table_name: str, records: List[Dict[str, Any]]) -> bool:
        """Create multiple records. See create_records() for details."""
        return create_records(self.db_path, table_name, records)
    
    def read(self, table_name: str, **kwargs) -> pd.DataFrame:
        """Read records. See read_records() for details."""
        return read_records(self.db_path, table_name, **kwargs)
    
    def read_by_id(self, table_name: str, id_column: str, id_value: Any) -> Optional[Dict[str, Any]]:
        """Read a single record by ID. See read_record_by_id() for details."""
        return read_record_by_id(self.db_path, table_name, id_column, id_value)
    
    def update(self, table_name: str, updates: Dict[str, Any], where: str) -> int:
        """Update records. See update_record() for details."""
        return update_record(self.db_path, table_name, updates, where=where)
    
    def update_by_id(self, table_name: str, id_column: str, id_value: Any, updates: Dict[str, Any]) -> int:
        """Update a record by ID. See update_records() for details."""
        return update_records(self.db_path, table_name, id_column, id_value, updates)
    
    def delete(self, table_name: str, where: str) -> int:
        """Delete records. See delete_record() for details."""
        return delete_record(self.db_path, table_name, where=where)
    
    def delete_by_id(self, table_name: str, id_column: str, id_value: Any) -> int:
        """Delete a record by ID. See delete_records() for details."""
        return delete_records(self.db_path, table_name, id_column, id_value)
    
    def get_tables(self) -> List[str]:
        """List all tables. See list_tables() for details."""
        return list_tables(self.db_path)
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists. See table_exists() for details."""
        return table_exists(self.db_path, table_name)
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information. See get_table_info() for details."""
        return get_table_info(self.db_path, table_name)

