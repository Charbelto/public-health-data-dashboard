"""
Command-Line Interface Module - Step 4

This module provides CLI functions for user interaction:
- Menu display and navigation
- User input handling
- Data display (tables, summaries)
- Visualizations (charts with matplotlib)
- Integration with data loading, cleaning, and analysis
"""

from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from src.main import load_dataset, load_json_dataset, load_to_database, read_from_database
from src.cleaning import DataCleaner
from src.analysis import DataAnalyzer


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def print_menu(title: str, options: List[str]):
    """
    Print a menu with numbered options.
    
    Parameters
    ----------
    title : str
        Menu title
    options : list of str
        List of menu options
    """
    print_header(title)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print(f"  0. Back/Exit")
    print()


def get_user_choice(max_choice: int) -> int:
    """
    Get and validate user's menu choice.
    
    Parameters
    ----------
    max_choice : int
        Maximum valid choice number
    
    Returns
    -------
    int
        User's validated choice
    """
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 0 <= choice <= max_choice:
                return choice
            else:
                print(f"Please enter a number between 0 and {max_choice}")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return 0


def get_user_input(prompt: str, input_type: str = "string") -> Any:
    """
    Get user input with type validation.
    
    Parameters
    ----------
    prompt : str
        Input prompt message
    input_type : str
        Expected input type: 'string', 'int', 'float', 'date'
    
    Returns
    -------
    any
        User's input in the specified type
    """
    while True:
        try:
            user_input = input(f"{prompt}: ").strip()
            
            if not user_input:
                return None
            
            if input_type == "int":
                return int(user_input)
            elif input_type == "float":
                return float(user_input)
            elif input_type == "date":
                return datetime.strptime(user_input, "%Y-%m-%d")
            else:
                return user_input
        except ValueError:
            print(f"Invalid {input_type}. Please try again.")
        except KeyboardInterrupt:
            print("\n")
            return None


def display_dataframe(df: pd.DataFrame, title: str = "Data", max_rows: int = 20):
    """
    Display a DataFrame in a formatted way.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to display
    title : str
        Title for the display
    max_rows : int
        Maximum number of rows to display
    """
    print_header(title)
    
    if df.empty:
        print("No data available.\n")
        return
    
    print(f"Total records: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}\n")
    
    if len(df) > max_rows:
        print(f"Showing first {max_rows} rows:\n")
        print(df.head(max_rows).to_string(index=False))
        print(f"\n... and {len(df) - max_rows} more rows")
    else:
        print(df.to_string(index=False))
    
    print()


def display_summary_stats(stats: Dict[str, float], title: str = "Summary Statistics"):
    """
    Display summary statistics in a formatted way.
    
    Parameters
    ----------
    stats : dict
        Dictionary of statistics
    title : str
        Title for the display
    """
    print_header(title)
    
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key:20s}: {value:,.2f}")
        else:
            print(f"  {key:20s}: {value}")
    
    print()


def display_grouped_data(df: pd.DataFrame, title: str = "Grouped Results"):
    """
    Display grouped/aggregated data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Grouped DataFrame
    title : str
        Title for the display
    """
    print_header(title)
    print(df.to_string())
    print()


def plot_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "Bar Chart",
    xlabel: str = "",
    ylabel: str = ""
):
    """
    Create and display a bar chart.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x_column : str
        Column for x-axis
    y_column : str
        Column for y-axis
    title : str
        Chart title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    """
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_column], df[y_column])
    plt.title(title)
    plt.xlabel(xlabel or x_column)
    plt.ylabel(ylabel or y_column)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "Line Chart",
    xlabel: str = "",
    ylabel: str = ""
):
    """
    Create and display a line chart.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x_column : str
        Column for x-axis
    y_column : str
        Column for y-axis
    title : str
        Chart title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_column], df[y_column], marker='o')
    plt.title(title)
    plt.xlabel(xlabel or x_column)
    plt.ylabel(ylabel or y_column)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_grouped_bar_chart(
    df: pd.DataFrame,
    title: str = "Grouped Bar Chart",
    ylabel: str = "Value"
):
    """
    Create and display a bar chart from grouped data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Grouped DataFrame with index as x-axis
    title : str
        Chart title
    ylabel : str
        Y-axis label
    """
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar', figsize=(10, 6))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()


def confirm_action(message: str = "Continue?") -> bool:
    """
    Ask user for confirmation.
    
    Parameters
    ----------
    message : str
        Confirmation message
    
    Returns
    -------
    bool
        True if user confirms, False otherwise
    """
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'")


def pause():
    """Pause and wait for user to press Enter."""
    input("\nPress Enter to continue...")


class CLISession:
    """
    Manages a CLI session with loaded data.
    
    This class maintains the current dataset and provides methods
    for interacting with it through the CLI.
    """
    
    def __init__(self):
        """Initialize a new CLI session."""
        self.df: Optional[pd.DataFrame] = None
        self.df_filtered: Optional[pd.DataFrame] = None
        self.data_name: str = "No data loaded"
        self.filters_applied: List[str] = []
    
    def load_data(self, df: pd.DataFrame, name: str):
        """
        Load data into the session.
        
        Parameters
        ----------
        df : pd.DataFrame
            Data to load
        name : str
            Name/description of the data
        """
        self.df = df.copy()
        self.df_filtered = df.copy()
        self.data_name = name
        self.filters_applied = []
    
    def has_data(self) -> bool:
        """Check if data is loaded."""
        return self.df is not None and not self.df.empty
    
    def apply_filter(self, filtered_df: pd.DataFrame, filter_description: str):
        """
        Apply a filter to the current data.
        
        Parameters
        ----------
        filtered_df : pd.DataFrame
            Filtered DataFrame
        filter_description : str
            Description of the filter applied
        """
        self.df_filtered = filtered_df
        self.filters_applied.append(filter_description)
    
    def reset_filters(self):
        """Reset all filters to original data."""
        if self.df is not None:
            self.df_filtered = self.df.copy()
            self.filters_applied = []
    
    def get_current_data(self) -> pd.DataFrame:
        """Get the current (filtered) data."""
        return self.df_filtered if self.df_filtered is not None else pd.DataFrame()
    
    def get_status(self) -> str:
        """
        Get current session status.
        
        Returns
        -------
        str
            Formatted status message
        """
        if not self.has_data():
            return "No data loaded"
        
        status = f"Data: {self.data_name}\n"
        status += f"Total records: {len(self.df)}\n"
        status += f"Current view: {len(self.df_filtered)} records"
        
        if self.filters_applied:
            status += f"\nFilters applied: {len(self.filters_applied)}"
            for filter_desc in self.filters_applied:
                status += f"\n  - {filter_desc}"
        
        return status


def export_to_csv(df: pd.DataFrame, default_filename: str = "export.csv"):
    """
    Export DataFrame to CSV file.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to export
    default_filename : str
        Default filename
    """
    filename = get_user_input(
        f"Enter filename (default: {default_filename})",
        "string"
    )
    
    if not filename:
        filename = default_filename
    
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    try:
        df.to_csv(filename, index=False)
        print(f"\n[SUCCESS] Data exported to {filename}")
    except Exception as e:
        print(f"\n[ERROR] Failed to export: {e}")


def format_number(value: float, decimals: int = 2) -> str:
    """
    Format a number with thousands separators.
    
    Parameters
    ----------
    value : float
        Number to format
    decimals : int
        Number of decimal places
    
    Returns
    -------
    str
        Formatted number string
    """
    return f"{value:,.{decimals}f}"
