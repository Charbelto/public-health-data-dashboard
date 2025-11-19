"""
Activity Logger for tracking user activities in the dashboard.

Part 5: Extension Features - Activity Logging
Logs all user activities to a file for audit and analysis purposes.
"""

import json
from pathlib import Path
from typing import Union, Optional, Dict, List, Any
from datetime import datetime
import pandas as pd


class ActivityLogger:
    """
    Logger class for tracking user activities in the health data dashboard.
    
    This logger records all user actions including data loading, filtering,
    analysis, exports, and CRUD operations.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file where activities will be recorded.
    user : str, optional
        Username or identifier for the current user.
    auto_log_session : bool, default False
        If True, automatically logs session start and end when using
        as a context manager.
    
    Examples
    --------
    >>> logger = ActivityLogger("logs/activity.log", user="analyst1")
    >>> logger.log("data_loaded", "Loaded vaccination data from CSV")
    
    # Using as context manager
    >>> with ActivityLogger("logs/activity.log", auto_log_session=True) as logger:
    ...     logger.log("analysis", "Calculated summary statistics")
    """
    
    def __init__(self, 
                 log_file: Union[str, Path],
                 user: Optional[str] = None,
                 auto_log_session: bool = False):
        """Initialize the activity logger."""
        self.log_file = Path(log_file)
        self.user = user or "unknown"
        self.auto_log_session = auto_log_session
        
        # Create log file if it doesn't exist
        if not self.log_file.exists():
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            self.log_file.touch()
    
    def log(self, 
            action: str, 
            description: str,
            level: str = "INFO",
            metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a user activity.
        
        Parameters
        ----------
        action : str
            Type of action performed (e.g., 'data_loaded', 'data_filtered').
        description : str
            Human-readable description of the action.
        level : str, default 'INFO'
            Severity level: 'INFO', 'WARNING', 'ERROR'.
        metadata : dict, optional
            Additional metadata about the action (e.g., file paths, parameters).
        
        Examples
        --------
        >>> logger.log("data_filtered", "Filtered by country=UK")
        >>> logger.log("error", "Failed to load file", level="ERROR",
        ...            metadata={"file": "data.csv", "error": "File not found"})
        """
        activity = {
            'timestamp': datetime.now().isoformat(),
            'user': self.user,
            'action': action,
            'description': description,
            'level': level
        }
        
        if metadata:
            activity['metadata'] = metadata
        
        # Append to log file as JSON lines
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(activity) + '\n')
    
    def __enter__(self):
        """Context manager entry - log session start if enabled."""
        if self.auto_log_session:
            self.log('session_start', 'User session started')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - log session end if enabled."""
        if self.auto_log_session:
            if exc_type is not None:
                self.log('session_end', f'Session ended with error: {exc_type.__name__}',
                        level='ERROR')
            else:
                self.log('session_end', 'User session ended')
        return False


def log_activity(log_file: Union[str, Path],
                 action: str,
                 description: str,
                 user: Optional[str] = None,
                 level: str = "INFO",
                 metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Standalone function to log a single activity.
    
    Convenience function for one-off logging without creating a logger instance.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file.
    action : str
        Type of action performed.
    description : str
        Description of the action.
    user : str, optional
        Username or identifier.
    level : str, default 'INFO'
        Severity level.
    metadata : dict, optional
        Additional metadata.
    
    Examples
    --------
    >>> log_activity("logs/activity.log", "data_loaded", "Loaded CSV file")
    """
    logger = ActivityLogger(log_file, user=user)
    logger.log(action, description, level=level, metadata=metadata)


def read_activity_log(log_file: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Read all activities from the log file.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file.
    
    Returns
    -------
    list of dict
        List of activity records in chronological order.
    
    Examples
    --------
    >>> activities = read_activity_log("logs/activity.log")
    >>> print(f"Total activities: {len(activities)}")
    """
    log_file = Path(log_file)
    
    if not log_file.exists():
        return []
    
    activities = []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        activity = json.loads(line)
                        activities.append(activity)
                    except json.JSONDecodeError:
                        # Skip malformed lines
                        continue
    except Exception:
        return []
    
    return activities


def filter_activities(log_file: Union[str, Path],
                     action: Optional[str] = None,
                     user: Optional[str] = None,
                     level: Optional[str] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Filter activities based on various criteria.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file.
    action : str, optional
        Filter by action type.
    user : str, optional
        Filter by user.
    level : str, optional
        Filter by severity level.
    start_date : datetime, optional
        Filter activities after this date/time.
    end_date : datetime, optional
        Filter activities before this date/time.
    
    Returns
    -------
    list of dict
        Filtered list of activities.
    
    Examples
    --------
    >>> # Get all data loading activities
    >>> activities = filter_activities("logs/activity.log", action="data_loaded")
    >>> 
    >>> # Get all ERROR level activities
    >>> errors = filter_activities("logs/activity.log", level="ERROR")
    >>> 
    >>> # Get activities for a specific user
    >>> user_activities = filter_activities("logs/activity.log", user="analyst1")
    """
    activities = read_activity_log(log_file)
    filtered = activities
    
    if action:
        filtered = [a for a in filtered if a.get('action') == action]
    
    if user:
        filtered = [a for a in filtered if a.get('user') == user]
    
    if level:
        filtered = [a for a in filtered if a.get('level') == level]
    
    if start_date:
        filtered = [a for a in filtered 
                   if datetime.fromisoformat(a['timestamp']) >= start_date]
    
    if end_date:
        filtered = [a for a in filtered 
                   if datetime.fromisoformat(a['timestamp']) <= end_date]
    
    return filtered


def get_activity_stats(log_file: Union[str, Path]) -> Dict[str, Any]:
    """
    Get statistics about logged activities.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file.
    
    Returns
    -------
    dict
        Dictionary containing statistics:
        - total_activities: Total number of logged activities
        - action_counts: Count of each action type
        - level_counts: Count of each severity level
        - user_counts: Count of activities per user
        - date_range: First and last activity timestamps
    
    Examples
    --------
    >>> stats = get_activity_stats("logs/activity.log")
    >>> print(f"Total activities: {stats['total_activities']}")
    >>> print(f"Most common action: {max(stats['action_counts'].items())}")
    """
    activities = read_activity_log(log_file)
    
    if not activities:
        return {
            'total_activities': 0,
            'action_counts': {},
            'level_counts': {},
            'user_counts': {},
            'date_range': None
        }
    
    # Count actions
    action_counts = {}
    for activity in activities:
        action = activity.get('action', 'unknown')
        action_counts[action] = action_counts.get(action, 0) + 1
    
    # Count levels
    level_counts = {}
    for activity in activities:
        level = activity.get('level', 'INFO')
        level_counts[level] = level_counts.get(level, 0) + 1
    
    # Count users
    user_counts = {}
    for activity in activities:
        user = activity.get('user', 'unknown')
        user_counts[user] = user_counts.get(user, 0) + 1
    
    # Get date range
    timestamps = [datetime.fromisoformat(a['timestamp']) for a in activities]
    date_range = {
        'first': min(timestamps).isoformat(),
        'last': max(timestamps).isoformat()
    }
    
    return {
        'total_activities': len(activities),
        'action_counts': action_counts,
        'level_counts': level_counts,
        'user_counts': user_counts,
        'date_range': date_range
    }


def clear_activity_log(log_file: Union[str, Path]) -> None:
    """
    Clear all activities from the log file.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file.
    
    Warning
    -------
    This operation is irreversible. Consider backing up the log first.
    
    Examples
    --------
    >>> clear_activity_log("logs/activity.log")
    """
    log_file = Path(log_file)
    
    if log_file.exists():
        # Clear the file by opening in write mode
        with open(log_file, 'w', encoding='utf-8') as f:
            pass  # Empty file


def export_log_to_csv(log_file: Union[str, Path],
                     output_file: Union[str, Path],
                     include_metadata: bool = False) -> None:
    """
    Export activity log to CSV format.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the log file.
    output_file : str or Path
        Path to the output CSV file.
    include_metadata : bool, default False
        If True, includes metadata as a JSON string column.
    
    Examples
    --------
    >>> export_log_to_csv("logs/activity.log", "reports/activities.csv")
    """
    activities = read_activity_log(log_file)
    
    if not activities:
        # Create empty CSV with headers
        df = pd.DataFrame(columns=['timestamp', 'user', 'action', 'description', 'level'])
    else:
        # Convert to DataFrame
        df = pd.DataFrame(activities)
        
        # Handle metadata
        if include_metadata and 'metadata' in df.columns:
            # Convert metadata dict to JSON string
            df['metadata'] = df['metadata'].apply(
                lambda x: json.dumps(x) if isinstance(x, dict) else ''
            )
        elif 'metadata' in df.columns and not include_metadata:
            # Drop metadata column
            df = df.drop(columns=['metadata'])
    
    # Ensure standard columns exist
    standard_cols = ['timestamp', 'user', 'action', 'description', 'level']
    for col in standard_cols:
        if col not in df.columns:
            df[col] = ''
    
    # Reorder columns
    cols = [c for c in standard_cols if c in df.columns]
    if include_metadata and 'metadata' in df.columns:
        cols.append('metadata')
    
    df = df[cols]
    
    # Export to CSV
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)


# ==============================================================================
# Convenience functions for common activities
# ==============================================================================

def log_data_operation(logger: ActivityLogger, 
                       operation: str,
                       details: str,
                       **metadata) -> None:
    """
    Log a data operation with standardized format.
    
    Parameters
    ----------
    logger : ActivityLogger
        Logger instance.
    operation : str
        Operation type: 'load', 'filter', 'clean', 'export', 'analyze'.
    details : str
        Operation details.
    **metadata : dict
        Additional metadata about the operation.
    """
    action_map = {
        'load': 'data_loaded',
        'filter': 'data_filtered',
        'clean': 'data_cleaned',
        'export': 'data_exported',
        'analyze': 'data_analyzed'
    }
    
    action = action_map.get(operation, f'data_{operation}')
    logger.log(action, details, metadata=metadata if metadata else None)


def log_crud_operation(logger: ActivityLogger,
                      operation: str,
                      table: str,
                      details: str,
                      **metadata) -> None:
    """
    Log a CRUD operation with standardized format.
    
    Parameters
    ----------
    logger : ActivityLogger
        Logger instance.
    operation : str
        CRUD operation: 'create', 'read', 'update', 'delete'.
    table : str
        Table name.
    details : str
        Operation details.
    **metadata : dict
        Additional metadata.
    """
    action = f'crud_{operation}'
    full_details = f"[{table}] {details}"
    metadata['table'] = table
    logger.log(action, full_details, metadata=metadata if metadata else None)


def log_error(logger: ActivityLogger, 
              error_type: str,
              error_message: str,
              **metadata) -> None:
    """
    Log an error with standardized format.
    
    Parameters
    ----------
    logger : ActivityLogger
        Logger instance.
    error_type : str
        Type of error.
    error_message : str
        Error message.
    **metadata : dict
        Additional error context.
    """
    logger.log(f'error_{error_type}', error_message, level='ERROR',
              metadata=metadata if metadata else None)

