"""
Command-Line Interface (CLI) Presentation Layer - Step 4

This module provides CLI functions for presenting data:
- Format tables and statistics for console display
- Create visualizations (bar charts, line charts)
- Interactive CLI for data exploration
- Export functionality
"""

from typing import Union, Optional, Dict, Any, List
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from src.main import load_dataset, load_json_dataset
from src.cleaning import DataCleaner
from src.analysis import DataAnalyzer, calculate_summary_stats, group_and_aggregate


def format_table(
    df: pd.DataFrame,
    max_rows: Optional[int] = None,
    max_cols: Optional[int] = None
) -> str:
    """
    Format DataFrame as a string table for console display.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to format
    max_rows : int, optional
        Maximum rows to display
    max_cols : int, optional
        Maximum columns to display

    Returns
    -------
    str
        Formatted table string
    """
    if df.empty:
        return "No data available (empty DataFrame)"
    
    # Configure pandas display options temporarily
    with pd.option_context(
        'display.max_rows', max_rows,
        'display.max_columns', max_cols,
        'display.width', 120
    ):
        return df.to_string()


def format_summary_stats(
    stats: Dict[str, float],
    title: Optional[str] = None
) -> str:
    """
    Format summary statistics for console display.

    Parameters
    ----------
    stats : dict
        Dictionary of statistics
    title : str, optional
        Title for the statistics

    Returns
    -------
    str
        Formatted statistics string
    """
    lines = []
    
    if title:
        lines.append("=" * 50)
        lines.append(f" {title}")
        lines.append("=" * 50)
    
    for key, value in stats.items():
        if isinstance(value, float):
            lines.append(f"  {key:15s}: {value:,.2f}")
        else:
            lines.append(f"  {key:15s}: {value}")
    
    return "\n".join(lines)


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Bar Chart",
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    sort_by: Optional[str] = None,
    ascending: bool = True,
    figsize: tuple = (10, 6)
) -> plt.Figure:
    """
    Create a bar chart.

    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x : str
        Column for x-axis
    y : str
        Column for y-axis (values)
    title : str
        Chart title
    xlabel : str, optional
        X-axis label
    ylabel : str, optional
        Y-axis label
    sort_by : str, optional
        Column to sort by
    ascending : bool
        Sort order
    figsize : tuple
        Figure size

    Returns
    -------
    matplotlib.figure.Figure
        Created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Sort if requested
    plot_df = df.copy()
    if sort_by and sort_by in plot_df.columns:
        plot_df = plot_df.sort_values(sort_by, ascending=ascending)
    
    # Create bar chart
    ax.bar(plot_df[x], plot_df[y], color='steelblue', alpha=0.8)
    
    # Labels and title
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=45, ha='right')
    
    # Add grid
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Line Chart",
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: tuple = (10, 6)
) -> plt.Figure:
    """
    Create a line chart.

    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x : str
        Column for x-axis
    y : str
        Column for y-axis
    title : str
        Chart title
    xlabel : str, optional
        X-axis label
    ylabel : str, optional
        Y-axis label
    figsize : tuple
        Figure size

    Returns
    -------
    matplotlib.figure.Figure
        Created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create line chart
    ax.plot(df[x], df[y], marker='o', linewidth=2, markersize=6, color='steelblue')
    
    # Labels and title
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Add grid
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def create_comparison_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    group_by: str,
    title: str = "Comparison Chart",
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: tuple = (12, 6)
) -> plt.Figure:
    """
    Create a comparison chart with multiple series.

    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x : str
        Column for x-axis
    y : str
        Column for y-axis
    group_by : str
        Column to group by (creates separate lines/bars)
    title : str
        Chart title
    xlabel : str, optional
        X-axis label
    ylabel : str, optional
        Y-axis label
    figsize : tuple
        Figure size

    Returns
    -------
    matplotlib.figure.Figure
        Created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each group
    for group_name, group_data in df.groupby(group_by):
        ax.plot(group_data[x], group_data[y], marker='o', label=str(group_name), linewidth=2)
    
    # Labels and title
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Legend
    ax.legend()
    
    # Grid
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def save_chart(
    fig: plt.Figure,
    output_path: Union[str, Path],
    dpi: int = 300
) -> bool:
    """
    Save a chart to file.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save
    output_path : str or Path
        Output file path
    dpi : int
        Resolution (dots per inch)

    Returns
    -------
    bool
        True if successful
    """
    try:
        output_path = Path(output_path)
        
        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save figure
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        
        return True
    except Exception as e:
        print(f"Error saving chart: {e}")
        return False


class HealthDataCLI:
    """
    Command-line interface for health data exploration.
    
    Provides methods for loading data, applying filters, showing summaries,
    creating visualizations, and exporting results.
    
    Examples
    --------
    >>> cli = HealthDataCLI()
    >>> cli.load_data("data/vaccination_data.csv")
    >>> cli.apply_filter('country', 'UK')
    >>> cli.show_summary('cases')
    >>> cli.create_visualization('bar', 'country', 'cases')
    """
    
    def __init__(self):
        """Initialize the CLI."""
        self.df = None
        self.original_df = None
        self.filters_applied = []
        self.data_source = None
    
    def load_data(self, file_path: Union[str, Path]) -> bool:
        """
        Load data from a file.
        
        Parameters
        ----------
        file_path : str or Path
            Path to CSV or JSON file
        
        Returns
        -------
        bool
            True if successful
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"Error: File not found: {file_path}")
                return False
            
            # Load based on extension
            if file_path.suffix == '.csv':
                self.df = load_dataset(file_path)
            elif file_path.suffix == '.json':
                self.df = load_json_dataset(file_path)
            else:
                print(f"Error: Unsupported file type: {file_path.suffix}")
                return False
            
            self.original_df = self.df.copy()
            self.data_source = str(file_path)
            self.filters_applied = []
            
            print(f"Successfully loaded {len(self.df)} records from {file_path.name}")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def apply_filter(
        self,
        column: str,
        value: Union[Any, List[Any]]
    ) -> bool:
        """
        Apply a filter to the data.
        
        Parameters
        ----------
        column : str
            Column to filter on
        value : any or list
            Value(s) to filter by
        
        Returns
        -------
        bool
            True if successful
        """
        if self.df is None:
            print("Error: No data loaded")
            return False
        
        try:
            if isinstance(value, list):
                self.df = self.df[self.df[column].isin(value)]
            else:
                self.df = self.df[self.df[column] == value]
            
            self.filters_applied.append(f"{column} = {value}")
            print(f"Filter applied: {column} = {value}")
            print(f"Records remaining: {len(self.df)}")
            
            return True
            
        except Exception as e:
            print(f"Error applying filter: {e}")
            return False
    
    def reset_filters(self) -> bool:
        """
        Reset all filters and restore original data.
        
        Returns
        -------
        bool
            True if successful
        """
        if self.original_df is None:
            print("Error: No original data available")
            return False
        
        self.df = self.original_df.copy()
        self.filters_applied = []
        print(f"Filters reset. Records: {len(self.df)}")
        
        return True
    
    def show_data(self, max_rows: int = 10) -> None:
        """
        Display current data.
        
        Parameters
        ----------
        max_rows : int
            Maximum rows to display
        """
        if self.df is None:
            print("No data loaded")
            return
        
        print(f"\nShowing {min(max_rows, len(self.df))} of {len(self.df)} records:")
        print(format_table(self.df.head(max_rows)))
    
    def show_summary(self, column: str) -> None:
        """
        Display summary statistics for a column.
        
        Parameters
        ----------
        column : str
            Column to summarize
        """
        if self.df is None:
            print("No data loaded")
            return
        
        if column not in self.df.columns:
            print(f"Error: Column '{column}' not found")
            return
        
        try:
            stats = calculate_summary_stats(self.df, column)
            print(format_summary_stats(stats, title=f"Summary Statistics: {column}"))
        except Exception as e:
            print(f"Error calculating summary: {e}")
    
    def show_grouped_data(
        self,
        group_by: str,
        agg_column: str,
        agg_func: str = 'sum'
    ) -> None:
        """
        Display grouped and aggregated data.
        
        Parameters
        ----------
        group_by : str
            Column to group by
        agg_column : str
            Column to aggregate
        agg_func : str
            Aggregation function
        """
        if self.df is None:
            print("No data loaded")
            return
        
        try:
            result = group_and_aggregate(
                self.df,
                group_by=group_by,
                agg_column=agg_column,
                agg_func=agg_func
            )
            
            print(f"\n{agg_func.capitalize()} of {agg_column} by {group_by}:")
            print(format_table(result))
            
        except Exception as e:
            print(f"Error grouping data: {e}")
    
    def export_data(self, output_path: Union[str, Path]) -> bool:
        """
        Export current (filtered) data to CSV.
        
        Parameters
        ----------
        output_path : str or Path
            Output file path
        
        Returns
        -------
        bool
            True if successful
        """
        if self.df is None:
            print("No data loaded")
            return False
        
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.df.to_csv(output_path, index=False)
            print(f"Exported {len(self.df)} records to {output_path}")
            
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def create_visualization(
        self,
        chart_type: str,
        x: str,
        y: str,
        title: Optional[str] = None,
        output_path: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> bool:
        """
        Create and optionally save a visualization.
        
        Parameters
        ----------
        chart_type : str
            Type of chart: 'bar', 'line', or 'comparison'
        x : str
            Column for x-axis
        y : str
            Column for y-axis
        title : str, optional
            Chart title
        output_path : str or Path, optional
            Path to save chart
        **kwargs
            Additional arguments for chart creation
        
        Returns
        -------
        bool
            True if successful
        """
        if self.df is None:
            print("No data loaded")
            return False
        
        try:
            # Generate title if not provided
            if title is None:
                title = f"{y} by {x}"
            
            # Create chart based on type
            if chart_type == 'bar':
                fig = create_bar_chart(self.df, x, y, title, **kwargs)
            elif chart_type == 'line':
                fig = create_line_chart(self.df, x, y, title, **kwargs)
            elif chart_type == 'comparison':
                if 'group_by' not in kwargs:
                    print("Error: 'group_by' required for comparison chart")
                    return False
                fig = create_comparison_chart(self.df, x, y, title=title, **kwargs)
            else:
                print(f"Error: Unknown chart type: {chart_type}")
                return False
            
            # Save if output path provided
            if output_path:
                return save_chart(fig, output_path)
            else:
                # Just close the figure
                plt.close(fig)
                print("Chart created successfully")
                return True
                
        except Exception as e:
            print(f"Error creating visualization: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current CLI status.
        
        Returns
        -------
        dict
            Status information
        """
        status = {
            'data_loaded': self.df is not None,
            'data_source': self.data_source,
            'record_count': len(self.df) if self.df is not None else 0,
            'column_count': len(self.df.columns) if self.df is not None else 0,
            'filters_applied': len(self.filters_applied),
            'filters': self.filters_applied
        }
        
        return status
    
    def get_columns(self) -> List[str]:
        """
        Get list of available columns.
        
        Returns
        -------
        list
            Column names
        """
        if self.df is None:
            return []
        return self.df.columns.tolist()

