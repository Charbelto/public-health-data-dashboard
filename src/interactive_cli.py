"""
Interactive Command-Line Interface for Public Health Data Dashboard

This module provides an interactive menu-driven CLI for exploring health data.
Users can load data, apply filters, view summaries, create visualizations, and export results.
"""

from pathlib import Path
from typing import Optional
import sys

from src.cli import HealthDataCLI


class InteractiveCLI:
    """
    Interactive command-line interface with menu system.
    
    Provides a user-friendly menu for data exploration without programming.
    """
    
    def __init__(self):
        """Initialize the interactive CLI."""
        self.cli = HealthDataCLI()
        self.running = True
    
    def print_header(self):
        """Print application header."""
        print("\n" + "="*70)
        print(" PUBLIC HEALTH DATA DASHBOARD - Interactive CLI")
        print("="*70)
    
    def print_menu(self):
        """Print main menu."""
        print("\n" + "-"*70)
        print(" MAIN MENU")
        print("-"*70)
        print(" 1. Load Data")
        print(" 2. View Data")
        print(" 3. Apply Filter")
        print(" 4. Reset Filters")
        print(" 5. Show Summary Statistics")
        print(" 6. Show Grouped Data")
        print(" 7. Create Visualization")
        print(" 8. Export Data")
        print(" 9. Show Status")
        print(" 0. Exit")
        print("-"*70)
    
    def get_input(self, prompt: str, default: Optional[str] = None) -> str:
        """
        Get user input with optional default value.
        
        Parameters
        ----------
        prompt : str
            Input prompt
        default : str, optional
            Default value
        
        Returns
        -------
        str
            User input
        """
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        
        value = input(prompt).strip()
        return value if value else (default or '')
    
    def load_data_menu(self):
        """Handle data loading."""
        print("\n" + "="*70)
        print(" LOAD DATA")
        print("="*70)
        print("\nAvailable sample files:")
        print("  1. data/sample_vaccination_data.csv")
        print("  2. data/sample_disease_outbreak.json")
        print("  3. Custom file path")
        
        choice = self.get_input("\nSelect option (1-3)", "1")
        
        if choice == "1":
            file_path = "data/sample_vaccination_data.csv"
        elif choice == "2":
            file_path = "data/sample_disease_outbreak.json"
        elif choice == "3":
            file_path = self.get_input("Enter file path")
        else:
            print("Invalid choice")
            return
        
        self.cli.load_data(file_path)
        
        if self.cli.df is not None:
            print(f"\nColumns available: {', '.join(self.cli.get_columns())}")
    
    def view_data_menu(self):
        """Handle data viewing."""
        if self.cli.df is None:
            print("\nNo data loaded. Please load data first.")
            return
        
        print("\n" + "="*70)
        print(" VIEW DATA")
        print("="*70)
        
        max_rows_str = self.get_input("Number of rows to display", "10")
        try:
            max_rows = int(max_rows_str)
        except ValueError:
            max_rows = 10
        
        self.cli.show_data(max_rows)
    
    def apply_filter_menu(self):
        """Handle filter application."""
        if self.cli.df is None:
            print("\nNo data loaded. Please load data first.")
            return
        
        print("\n" + "="*70)
        print(" APPLY FILTER")
        print("="*70)
        print(f"\nAvailable columns: {', '.join(self.cli.get_columns())}")
        
        column = self.get_input("\nColumn to filter by")
        
        if column not in self.cli.get_columns():
            print(f"Error: Column '{column}' not found")
            return
        
        # Show unique values
        unique_vals = self.cli.df[column].unique()
        if len(unique_vals) <= 20:
            print(f"\nUnique values: {', '.join(map(str, unique_vals))}")
        else:
            print(f"\n{len(unique_vals)} unique values found")
        
        value = self.get_input("Value to filter by")
        
        # Try to convert to appropriate type
        try:
            if self.cli.df[column].dtype in ['int64', 'float64']:
                value = float(value)
        except:
            pass
        
        self.cli.apply_filter(column, value)
    
    def show_summary_menu(self):
        """Handle summary statistics display."""
        if self.cli.df is None:
            print("\nNo data loaded. Please load data first.")
            return
        
        print("\n" + "="*70)
        print(" SUMMARY STATISTICS")
        print("="*70)
        
        # Show numeric columns
        numeric_cols = self.cli.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        print(f"\nNumeric columns: {', '.join(numeric_cols)}")
        
        column = self.get_input("\nColumn to summarize")
        
        if column not in numeric_cols:
            print(f"Error: '{column}' is not a numeric column")
            return
        
        self.cli.show_summary(column)
    
    def show_grouped_menu(self):
        """Handle grouped data display."""
        if self.cli.df is None:
            print("\nNo data loaded. Please load data first.")
            return
        
        print("\n" + "="*70)
        print(" GROUPED DATA")
        print("="*70)
        print(f"\nAvailable columns: {', '.join(self.cli.get_columns())}")
        
        group_by = self.get_input("\nGroup by column")
        
        if group_by not in self.cli.get_columns():
            print(f"Error: Column '{group_by}' not found")
            return
        
        numeric_cols = self.cli.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        print(f"\nNumeric columns: {', '.join(numeric_cols)}")
        
        agg_column = self.get_input("Column to aggregate")
        
        if agg_column not in numeric_cols:
            print(f"Error: '{agg_column}' is not a numeric column")
            return
        
        print("\nAggregation functions: sum, mean, count, min, max")
        agg_func = self.get_input("Aggregation function", "sum")
        
        self.cli.show_grouped_data(group_by, agg_column, agg_func)
    
    def create_visualization_menu(self):
        """Handle visualization creation."""
        if self.cli.df is None:
            print("\nNo data loaded. Please load data first.")
            return
        
        print("\n" + "="*70)
        print(" CREATE VISUALIZATION")
        print("="*70)
        print("\nChart types:")
        print("  1. Bar Chart")
        print("  2. Line Chart")
        print("  3. Comparison Chart (multiple series)")
        
        chart_choice = self.get_input("\nSelect chart type (1-3)", "1")
        
        chart_types = {"1": "bar", "2": "line", "3": "comparison"}
        chart_type = chart_types.get(chart_choice, "bar")
        
        print(f"\nAvailable columns: {', '.join(self.cli.get_columns())}")
        
        x = self.get_input("X-axis column")
        y = self.get_input("Y-axis column")
        title = self.get_input("Chart title (optional)")
        
        if x not in self.cli.get_columns() or y not in self.cli.get_columns():
            print("Error: Invalid column names")
            return
        
        kwargs = {}
        if chart_type == "comparison":
            group_by = self.get_input("Group by column")
            if group_by in self.cli.get_columns():
                kwargs['group_by'] = group_by
            else:
                print("Error: Invalid group_by column")
                return
        
        save = self.get_input("Save to file? (yes/no)", "yes").lower()
        
        output_path = None
        if save in ['yes', 'y']:
            filename = self.get_input("Output filename", "chart.png")
            output_path = Path("outputs") / filename
        
        self.cli.create_visualization(
            chart_type=chart_type,
            x=x,
            y=y,
            title=title if title else None,
            output_path=output_path,
            **kwargs
        )
    
    def export_data_menu(self):
        """Handle data export."""
        if self.cli.df is None:
            print("\nNo data loaded. Please load data first.")
            return
        
        print("\n" + "="*70)
        print(" EXPORT DATA")
        print("="*70)
        
        filename = self.get_input("\nOutput filename", "exported_data.csv")
        output_path = Path("outputs") / filename
        
        self.cli.export_data(output_path)
    
    def show_status_menu(self):
        """Handle status display."""
        print("\n" + "="*70)
        print(" SYSTEM STATUS")
        print("="*70)
        
        status = self.cli.get_status()
        
        print(f"\nData Loaded: {'Yes' if status['data_loaded'] else 'No'}")
        
        if status['data_loaded']:
            print(f"Data Source: {status['data_source']}")
            print(f"Records: {status['record_count']}")
            print(f"Columns: {status['column_count']}")
            print(f"Filters Applied: {status['filters_applied']}")
            
            if status['filters']:
                print("\nActive Filters:")
                for i, filter_desc in enumerate(status['filters'], 1):
                    print(f"  {i}. {filter_desc}")
    
    def run(self):
        """Run the interactive CLI."""
        self.print_header()
        print("\nWelcome! This tool helps you explore public health data.")
        
        while self.running:
            try:
                self.print_menu()
                choice = self.get_input("\nEnter choice (0-9)")
                
                if choice == "1":
                    self.load_data_menu()
                elif choice == "2":
                    self.view_data_menu()
                elif choice == "3":
                    self.apply_filter_menu()
                elif choice == "4":
                    self.cli.reset_filters()
                elif choice == "5":
                    self.show_summary_menu()
                elif choice == "6":
                    self.show_grouped_menu()
                elif choice == "7":
                    self.create_visualization_menu()
                elif choice == "8":
                    self.export_data_menu()
                elif choice == "9":
                    self.show_status_menu()
                elif choice == "0":
                    print("\nThank you for using the Public Health Data Dashboard!")
                    self.running = False
                else:
                    print("\nInvalid choice. Please try again.")
                
                if self.running and choice != "0":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point for interactive CLI."""
    app = InteractiveCLI()
    app.run()


if __name__ == "__main__":
    main()

