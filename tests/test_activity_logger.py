"""
Tests for activity logging functionality.

Following TDD, these tests are written before implementation.
Step 5: Extension Features - Activity Logging
"""

import pytest
from pathlib import Path
from datetime import datetime
import json

from src.activity_logger import (
    ActivityLogger,
    log_activity,
    read_activity_log,
    get_activity_stats,
    filter_activities,
    clear_activity_log,
    export_log_to_csv
)


# ==============================================================================
# Tests for Basic Logging Operations
# ==============================================================================

def test_activity_logger_initialization(tmp_path: Path) -> None:
    """
    Test ActivityLogger initialization.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    assert logger.log_file == log_file
    assert log_file.exists()


def test_log_simple_activity(tmp_path: Path) -> None:
    """
    Test logging a simple activity.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("data_loaded", "Loaded vaccination data from CSV")
    
    # Read log file
    activities = read_activity_log(log_file)
    
    assert len(activities) == 1
    assert activities[0]['action'] == 'data_loaded'
    assert 'Loaded vaccination data' in activities[0]['description']
    assert 'timestamp' in activities[0]


def test_log_activity_with_metadata(tmp_path: Path) -> None:
    """
    Test logging activity with additional metadata.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    metadata = {
        'file_path': 'data/vaccination.csv',
        'rows': 100,
        'columns': 5
    }
    logger.log("data_loaded", "Loaded CSV file", metadata=metadata)
    
    activities = read_activity_log(log_file)
    
    assert len(activities) == 1
    assert activities[0]['metadata']['file_path'] == 'data/vaccination.csv'
    assert activities[0]['metadata']['rows'] == 100


def test_log_multiple_activities(tmp_path: Path) -> None:
    """
    Test logging multiple activities in sequence.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("data_loaded", "Loaded data")
    logger.log("data_filtered", "Filtered by country=UK")
    logger.log("data_exported", "Exported to CSV")
    
    activities = read_activity_log(log_file)
    
    assert len(activities) == 3
    assert activities[0]['action'] == 'data_loaded'
    assert activities[1]['action'] == 'data_filtered'
    assert activities[2]['action'] == 'data_exported'


def test_log_activity_with_user(tmp_path: Path) -> None:
    """
    Test logging activity with user information.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file, user="john_doe")
    
    logger.log("data_loaded", "Loaded data")
    
    activities = read_activity_log(log_file)
    
    assert activities[0]['user'] == 'john_doe'


def test_log_activity_with_level(tmp_path: Path) -> None:
    """
    Test logging activities with different severity levels.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("info_action", "Info message", level="INFO")
    logger.log("warning_action", "Warning message", level="WARNING")
    logger.log("error_action", "Error message", level="ERROR")
    
    activities = read_activity_log(log_file)
    
    assert len(activities) == 3
    assert activities[0]['level'] == 'INFO'
    assert activities[1]['level'] == 'WARNING'
    assert activities[2]['level'] == 'ERROR'


# ==============================================================================
# Tests for Reading and Filtering Logs
# ==============================================================================

def test_read_activity_log_returns_chronological_order(tmp_path: Path) -> None:
    """
    Test that activities are returned in chronological order.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("first", "First action")
    logger.log("second", "Second action")
    logger.log("third", "Third action")
    
    activities = read_activity_log(log_file)
    
    assert activities[0]['action'] == 'first'
    assert activities[2]['action'] == 'third'


def test_filter_activities_by_action(tmp_path: Path) -> None:
    """
    Test filtering activities by action type.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("data_loaded", "Action 1")
    logger.log("data_filtered", "Action 2")
    logger.log("data_loaded", "Action 3")
    logger.log("data_exported", "Action 4")
    
    filtered = filter_activities(log_file, action="data_loaded")
    
    assert len(filtered) == 2
    assert all(a['action'] == 'data_loaded' for a in filtered)


def test_filter_activities_by_date_range(tmp_path: Path) -> None:
    """
    Test filtering activities by date range.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("action1", "Description 1")
    
    activities = read_activity_log(log_file)
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.now().replace(hour=23, minute=59, second=59)
    
    filtered = filter_activities(log_file, start_date=start_date, end_date=end_date)
    
    assert len(filtered) >= 1


def test_filter_activities_by_level(tmp_path: Path) -> None:
    """
    Test filtering activities by severity level.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("action1", "Info", level="INFO")
    logger.log("action2", "Warning", level="WARNING")
    logger.log("action3", "Error", level="ERROR")
    logger.log("action4", "Another info", level="INFO")
    
    filtered = filter_activities(log_file, level="INFO")
    
    assert len(filtered) == 2
    assert all(a['level'] == 'INFO' for a in filtered)


def test_filter_activities_by_user(tmp_path: Path) -> None:
    """
    Test filtering activities by user.
    """
    log_file = tmp_path / "activity.log"
    
    logger1 = ActivityLogger(log_file, user="alice")
    logger1.log("action1", "Alice's action")
    
    logger2 = ActivityLogger(log_file, user="bob")
    logger2.log("action2", "Bob's action")
    
    logger1.log("action3", "Another Alice action")
    
    filtered = filter_activities(log_file, user="alice")
    
    assert len(filtered) == 2
    assert all(a['user'] == 'alice' for a in filtered)


# ==============================================================================
# Tests for Activity Statistics
# ==============================================================================

def test_get_activity_stats_basic(tmp_path: Path) -> None:
    """
    Test getting basic activity statistics.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("data_loaded", "Action 1")
    logger.log("data_loaded", "Action 2")
    logger.log("data_filtered", "Action 3")
    logger.log("data_exported", "Action 4")
    
    stats = get_activity_stats(log_file)
    
    assert stats['total_activities'] == 4
    assert 'action_counts' in stats
    assert stats['action_counts']['data_loaded'] == 2
    assert stats['action_counts']['data_filtered'] == 1


def test_get_activity_stats_with_levels(tmp_path: Path) -> None:
    """
    Test activity statistics including severity levels.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("action1", "Info", level="INFO")
    logger.log("action2", "Warning", level="WARNING")
    logger.log("action3", "Error", level="ERROR")
    logger.log("action4", "Another info", level="INFO")
    
    stats = get_activity_stats(log_file)
    
    assert stats['level_counts']['INFO'] == 2
    assert stats['level_counts']['WARNING'] == 1
    assert stats['level_counts']['ERROR'] == 1


def test_get_activity_stats_empty_log(tmp_path: Path) -> None:
    """
    Test getting statistics from an empty log.
    """
    log_file = tmp_path / "activity.log"
    ActivityLogger(log_file)  # Create empty log
    
    stats = get_activity_stats(log_file)
    
    assert stats['total_activities'] == 0
    assert stats['action_counts'] == {}


# ==============================================================================
# Tests for Log Management
# ==============================================================================

def test_clear_activity_log(tmp_path: Path) -> None:
    """
    Test clearing the activity log.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("action1", "Description 1")
    logger.log("action2", "Description 2")
    
    # Verify log has activities
    activities = read_activity_log(log_file)
    assert len(activities) == 2
    
    # Clear log
    clear_activity_log(log_file)
    
    # Verify log is empty
    activities = read_activity_log(log_file)
    assert len(activities) == 0


def test_log_rotation_when_file_too_large(tmp_path: Path) -> None:
    """
    Test that log file can handle many entries without issues.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    # Log many activities
    for i in range(100):
        logger.log(f"action_{i}", f"Description {i}")
    
    activities = read_activity_log(log_file)
    
    assert len(activities) == 100


def test_export_log_to_csv(tmp_path: Path) -> None:
    """
    Test exporting activity log to CSV format.
    """
    log_file = tmp_path / "activity.log"
    logger = ActivityLogger(log_file)
    
    logger.log("data_loaded", "Loaded data", metadata={'file': 'test.csv'})
    logger.log("data_filtered", "Filtered data")
    logger.log("data_exported", "Exported results")
    
    csv_file = tmp_path / "activity_export.csv"
    export_log_to_csv(log_file, csv_file)
    
    assert csv_file.exists()
    
    # Verify CSV content
    import pandas as pd
    df = pd.read_csv(csv_file)
    
    assert len(df) == 3
    assert 'timestamp' in df.columns
    assert 'action' in df.columns
    assert 'description' in df.columns


# ==============================================================================
# Tests for Standalone log_activity Function
# ==============================================================================

def test_standalone_log_activity_function(tmp_path: Path) -> None:
    """
    Test the standalone log_activity convenience function.
    """
    log_file = tmp_path / "activity.log"
    
    log_activity(log_file, "test_action", "Test description")
    
    activities = read_activity_log(log_file)
    
    assert len(activities) == 1
    assert activities[0]['action'] == 'test_action'


def test_log_activity_creates_file_if_not_exists(tmp_path: Path) -> None:
    """
    Test that log_activity creates the log file if it doesn't exist.
    """
    log_file = tmp_path / "new_activity.log"
    
    assert not log_file.exists()
    
    log_activity(log_file, "action", "description")
    
    assert log_file.exists()


# ==============================================================================
# Tests for Error Handling
# ==============================================================================

def test_read_nonexistent_log_returns_empty_list(tmp_path: Path) -> None:
    """
    Test reading from a non-existent log file returns empty list.
    """
    log_file = tmp_path / "nonexistent.log"
    
    activities = read_activity_log(log_file)
    
    assert activities == []


def test_filter_nonexistent_log_returns_empty_list(tmp_path: Path) -> None:
    """
    Test filtering a non-existent log file returns empty list.
    """
    log_file = tmp_path / "nonexistent.log"
    
    filtered = filter_activities(log_file, action="test")
    
    assert filtered == []


def test_get_stats_nonexistent_log_returns_default(tmp_path: Path) -> None:
    """
    Test getting stats from non-existent log returns default values.
    """
    log_file = tmp_path / "nonexistent.log"
    
    stats = get_activity_stats(log_file)
    
    assert stats['total_activities'] == 0
    assert stats['action_counts'] == {}


# ==============================================================================
# Tests for Context Manager Support
# ==============================================================================

def test_activity_logger_context_manager(tmp_path: Path) -> None:
    """
    Test using ActivityLogger as a context manager.
    """
    log_file = tmp_path / "activity.log"
    
    with ActivityLogger(log_file) as logger:
        logger.log("action_in_context", "Action inside context manager")
    
    activities = read_activity_log(log_file)
    
    assert len(activities) == 1
    assert activities[0]['action'] == 'action_in_context'


def test_activity_logger_auto_log_session(tmp_path: Path) -> None:
    """
    Test automatic session logging when using context manager.
    """
    log_file = tmp_path / "activity.log"
    
    with ActivityLogger(log_file, auto_log_session=True) as logger:
        logger.log("user_action", "User performed action")
    
    activities = read_activity_log(log_file)
    
    # Should have: session_start, user_action, session_end
    assert len(activities) == 3
    assert activities[0]['action'] == 'session_start'
    assert activities[1]['action'] == 'user_action'
    assert activities[2]['action'] == 'session_end'

