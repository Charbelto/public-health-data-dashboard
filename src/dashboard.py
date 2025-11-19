"""
Public Health Data Dashboard - Interactive CLI Application

Main entry point for the command-line interface.
Provides menu-driven access to all functionality.
"""

from pathlib import Path
import pandas as pd

from src.cli import (
    clear_screen, print_header, print_menu, get_user_choice, get_user_input,
    display_dataframe, display_summary_stats, display_grouped_data,
    plot_bar_chart, plot_line_chart, plot_grouped_bar_chart,
    confirm_action, pause, CLISession, export_to_csv
)
from src.main import load_dataset, load_json_dataset, load_to_database, read_from_database
from src.cleaning import DataCleaner, detect_missing_values
from src.analysis import (
    filter_by_column, filter_by_numeric_range, filter_by_date_range,
    calculate_summary_stats, get_column_statistics, group_and_aggregate,
    calculate_trends, DataAnalyzer
)


class HealthDashboard:
    """Main dashboard application class."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.session = CLISession()
        self.running = True
    
    def run(self):
        """Run the main dashboard loop."""
        while self.running:
            self.show_main_menu()
    
    def show_main_menu(self):
        """Display and handle the main menu."""
        clear_screen()
        print_header("PUBLIC HEALTH DATA INSIGHTS DASHBOARD")
        print(self.session.get_status())
        
        options = [
            "Load Data",
            "View Data",
            "Filter Data",
            "Analyze Data",
            "Visualize Data",
            "Clean Data",
            "Export Data"
        ]
        
        print_menu("Main Menu", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.load_data_menu()
        elif choice == 2:
            self.view_data_menu()
        elif choice == 3:
            self.filter_data_menu()
        elif choice == 4:
            self.analyze_data_menu()
        elif choice == 5:
            self.visualize_data_menu()
        elif choice == 6:
            self.clean_data_menu()
        elif choice == 7:
            self.export_data_menu()
        elif choice == 0:
            self.exit_dashboard()
    
    def load_data_menu(self):
        """Handle data loading menu."""
        clear_screen()
        options = [
            "Load Sample Vaccination Data (CSV)",
            "Load Sample Outbreak Data (JSON)",
            "Load Custom CSV File",
            "Load from Database"
        ]
        
        print_menu("Load Data", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.load_sample_vaccination_data()
        elif choice == 2:
            self.load_sample_outbreak_data()
        elif choice == 3:
            self.load_custom_csv()
        elif choice == 4:
            self.load_from_database()
    
    def load_sample_vaccination_data(self):
        """Load sample vaccination data."""
        try:
            df = load_dataset("data/sample_vaccination_data.csv")
            self.session.load_data(df, "Sample Vaccination Data")
            print("\n[SUCCESS] Loaded vaccination data")
            print(f"Records: {len(df)}, Columns: {len(df.columns)}")
        except Exception as e:
            print(f"\n[ERROR] Failed to load data: {e}")
        pause()
    
    def load_sample_outbreak_data(self):
        """Load sample outbreak data."""
        try:
            df = load_json_dataset("data/sample_disease_outbreak.json")
            self.session.load_data(df, "Sample Disease Outbreak Data")
            print("\n[SUCCESS] Loaded outbreak data")
            print(f"Records: {len(df)}, Columns: {len(df.columns)}")
        except Exception as e:
            print(f"\n[ERROR] Failed to load data: {e}")
        pause()
    
    def load_custom_csv(self):
        """Load a custom CSV file."""
        filepath = get_user_input("Enter CSV file path", "string")
        if not filepath:
            return
        
        try:
            df = load_dataset(filepath)
            filename = Path(filepath).name
            self.session.load_data(df, filename)
            print(f"\n[SUCCESS] Loaded {filename}")
            print(f"Records: {len(df)}, Columns: {len(df.columns)}")
        except Exception as e:
            print(f"\n[ERROR] Failed to load data: {e}")
        pause()
    
    def load_from_database(self):
        """Load data from database."""
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        try:
            df = read_from_database(db_path, table_name)
            self.session.load_data(df, f"{table_name} (from database)")
            print(f"\n[SUCCESS] Loaded {len(df)} records from {table_name}")
        except Exception as e:
            print(f"\n[ERROR] Failed to load from database: {e}")
        pause()
    
    def view_data_menu(self):
        """Handle data viewing menu."""
        if not self.session.has_data():
            print("\n[INFO] No data loaded. Please load data first.")
            pause()
            return
        
        clear_screen()
        options = [
            "View All Data",
            "View First 10 Rows",
            "View Last 10 Rows",
            "View Data Info",
            "View Column Names",
            "View Summary Statistics"
        ]
        
        print_menu("View Data", options)
        choice = get_user_choice(len(options))
        
        df = self.session.get_current_data()
        
        if choice == 1:
            display_dataframe(df, "All Data", max_rows=50)
        elif choice == 2:
            display_dataframe(df.head(10), "First 10 Rows")
        elif choice == 3:
            display_dataframe(df.tail(10), "Last 10 Rows")
        elif choice == 4:
            self.view_data_info(df)
        elif choice == 5:
            self.view_column_names(df)
        elif choice == 6:
            self.view_summary_statistics(df)
        
        if choice != 0:
            pause()
    
    def view_data_info(self, df: pd.DataFrame):
        """Display data information."""
        print_header("Data Information")
        print(f"Total Records: {len(df)}")
        print(f"Total Columns: {len(df.columns)}")
        print(f"\nColumn Details:")
        print(df.dtypes.to_string())
        print()
    
    def view_column_names(self, df: pd.DataFrame):
        """Display column names."""
        print_header("Column Names")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col} ({df[col].dtype})")
        print()
    
    def view_summary_statistics(self, df: pd.DataFrame):
        """Display summary statistics for all numeric columns."""
        stats = get_column_statistics(df)
        if not stats:
            print("\n[INFO] No numeric columns found.")
            return
        
        for col, col_stats in stats.items():
            display_summary_stats(col_stats, f"Statistics: {col}")
    
    def filter_data_menu(self):
        """Handle data filtering menu."""
        if not self.session.has_data():
            print("\n[INFO] No data loaded. Please load data first.")
            pause()
            return
        
        clear_screen()
        options = [
            "Filter by Column Value",
            "Filter by Numeric Range",
            "Filter by Date Range (if applicable)",
            "Reset All Filters",
            "Show Current Filters"
        ]
        
        print_menu("Filter Data", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.filter_by_column_value()
        elif choice == 2:
            self.filter_by_numeric_range_menu()
        elif choice == 3:
            self.filter_by_date_range_menu()
        elif choice == 4:
            self.reset_filters()
        elif choice == 5:
            self.show_current_filters()
    
    def filter_by_column_value(self):
        """Filter data by column value."""
        df = self.session.get_current_data()
        
        print("\nAvailable columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        col_name = get_user_input("\nEnter column name", "string")
        if not col_name or col_name not in df.columns:
            print("[ERROR] Invalid column name")
            pause()
            return
        
        print(f"\nUnique values in '{col_name}':")
        unique_values = df[col_name].unique()
        for i, val in enumerate(unique_values[:20], 1):
            print(f"  {i}. {val}")
        if len(unique_values) > 20:
            print(f"  ... and {len(unique_values) - 20} more")
        
        value = get_user_input(f"\nEnter value to filter by", "string")
        if not value:
            pause()
            return
        
        filtered = filter_by_column(df, col_name, value)
        self.session.apply_filter(filtered, f"{col_name} = {value}")
        
        print(f"\n[SUCCESS] Filtered to {len(filtered)} records")
        pause()
    
    def filter_by_numeric_range_menu(self):
        """Filter by numeric range."""
        df = self.session.get_current_data()
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            print("\n[INFO] No numeric columns available")
            pause()
            return
        
        print("\nNumeric columns:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"  {i}. {col}")
        
        col_name = get_user_input("\nEnter column name", "string")
        if not col_name or col_name not in numeric_cols:
            print("[ERROR] Invalid column name")
            pause()
            return
        
        print(f"\nCurrent range: {df[col_name].min()} to {df[col_name].max()}")
        
        min_val = get_user_input("Enter minimum value (or press Enter to skip)", "float")
        max_val = get_user_input("Enter maximum value (or press Enter to skip)", "float")
        
        if min_val is None and max_val is None:
            pause()
            return
        
        filtered = filter_by_numeric_range(df, col_name, min_val, max_val)
        filter_desc = f"{col_name}: "
        if min_val is not None:
            filter_desc += f">= {min_val}"
        if max_val is not None:
            if min_val is not None:
                filter_desc += " and "
            filter_desc += f"<= {max_val}"
        
        self.session.apply_filter(filtered, filter_desc)
        print(f"\n[SUCCESS] Filtered to {len(filtered)} records")
        pause()
    
    def filter_by_date_range_menu(self):
        """Filter by date range."""
        print("\n[INFO] Date filtering requires a datetime column.")
        print("Format: YYYY-MM-DD")
        pause()
    
    def reset_filters(self):
        """Reset all filters."""
        self.session.reset_filters()
        print("\n[SUCCESS] All filters reset")
        pause()
    
    def show_current_filters(self):
        """Show currently applied filters."""
        print_header("Current Filters")
        if not self.session.filters_applied:
            print("No filters applied")
        else:
            for i, filter_desc in enumerate(self.session.filters_applied, 1):
                print(f"  {i}. {filter_desc}")
        print()
        pause()
    
    def analyze_data_menu(self):
        """Handle data analysis menu."""
        if not self.session.has_data():
            print("\n[INFO] No data loaded. Please load data first.")
            pause()
            return
        
        clear_screen()
        options = [
            "Summary Statistics for Column",
            "Summary for All Numeric Columns",
            "Group and Aggregate",
            "Trend Analysis"
        ]
        
        print_menu("Analyze Data", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.analyze_column()
        elif choice == 2:
            self.analyze_all_numeric()
        elif choice == 3:
            self.group_and_aggregate_menu()
        elif choice == 4:
            self.trend_analysis_menu()
    
    def analyze_column(self):
        """Analyze a specific column."""
        df = self.session.get_current_data()
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            print("\n[INFO] No numeric columns available")
            pause()
            return
        
        print("\nNumeric columns:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"  {i}. {col}")
        
        col_name = get_user_input("\nEnter column name", "string")
        if not col_name or col_name not in numeric_cols:
            print("[ERROR] Invalid column name")
            pause()
            return
        
        stats = calculate_summary_stats(df, col_name)
        display_summary_stats(stats, f"Statistics: {col_name}")
        pause()
    
    def analyze_all_numeric(self):
        """Analyze all numeric columns."""
        df = self.session.get_current_data()
        stats = get_column_statistics(df)
        
        if not stats:
            print("\n[INFO] No numeric columns found")
            pause()
            return
        
        for col, col_stats in stats.items():
            display_summary_stats(col_stats, f"Statistics: {col}")
        
        pause()
    
    def group_and_aggregate_menu(self):
        """Group and aggregate data."""
        df = self.session.get_current_data()
        
        print("\nAvailable columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        group_col = get_user_input("\nEnter column to group by", "string")
        if not group_col or group_col not in df.columns:
            print("[ERROR] Invalid column name")
            pause()
            return
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        print("\nNumeric columns:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"  {i}. {col}")
        
        agg_col = get_user_input("\nEnter column to aggregate", "string")
        if not agg_col or agg_col not in numeric_cols:
            print("[ERROR] Invalid column name")
            pause()
            return
        
        print("\nAggregation functions: sum, mean, count, min, max")
        agg_func = get_user_input("Enter function (default: sum)", "string")
        if not agg_func:
            agg_func = "sum"
        
        try:
            result = group_and_aggregate(df, group_col, agg_col, agg_func)
            display_grouped_data(result, f"Grouped by {group_col}")
            
            if confirm_action("Visualize this grouped data?"):
                plot_grouped_bar_chart(result, f"{agg_col} by {group_col}", agg_col)
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def trend_analysis_menu(self):
        """Analyze trends over time."""
        print("\n[INFO] Trend analysis requires time-series data with date column.")
        pause()
    
    def visualize_data_menu(self):
        """Handle data visualization menu."""
        if not self.session.has_data():
            print("\n[INFO] No data loaded. Please load data first.")
            pause()
            return
        
        clear_screen()
        options = [
            "Bar Chart",
            "Line Chart",
            "Grouped Bar Chart"
        ]
        
        print_menu("Visualize Data", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.create_bar_chart()
        elif choice == 2:
            self.create_line_chart()
        elif choice == 3:
            self.create_grouped_bar_chart()
    
    def create_bar_chart(self):
        """Create a bar chart."""
        df = self.session.get_current_data()
        
        if len(df) > 50:
            print("\n[WARNING] Too many records for bar chart. Showing first 50.")
            df = df.head(50)
        
        print("\nAvailable columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        x_col = get_user_input("\nEnter X-axis column", "string")
        y_col = get_user_input("Enter Y-axis column", "string")
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            print("[ERROR] Invalid column names")
            pause()
            return
        
        title = get_user_input("Enter chart title (optional)", "string")
        if not title:
            title = f"{y_col} by {x_col}"
        
        try:
            plot_bar_chart(df, x_col, y_col, title)
        except Exception as e:
            print(f"\n[ERROR] Failed to create chart: {e}")
        
        pause()
    
    def create_line_chart(self):
        """Create a line chart."""
        df = self.session.get_current_data()
        
        print("\nAvailable columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        x_col = get_user_input("\nEnter X-axis column", "string")
        y_col = get_user_input("Enter Y-axis column", "string")
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            print("[ERROR] Invalid column names")
            pause()
            return
        
        title = get_user_input("Enter chart title (optional)", "string")
        if not title:
            title = f"{y_col} over {x_col}"
        
        try:
            plot_line_chart(df, x_col, y_col, title)
        except Exception as e:
            print(f"\n[ERROR] Failed to create chart: {e}")
        
        pause()
    
    def create_grouped_bar_chart(self):
        """Create a grouped bar chart."""
        print("\n[INFO] Please use 'Group and Aggregate' in Analyze Data menu first.")
        pause()
    
    def clean_data_menu(self):
        """Handle data cleaning menu."""
        if not self.session.has_data():
            print("\n[INFO] No data loaded. Please load data first.")
            pause()
            return
        
        clear_screen()
        options = [
            "Detect Data Quality Issues",
            "Handle Missing Values",
            "Remove Duplicates",
            "Apply Full Cleaning Pipeline"
        ]
        
        print_menu("Clean Data", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.detect_quality_issues()
        elif choice == 2:
            self.handle_missing_values_menu()
        elif choice == 3:
            self.remove_duplicates_menu()
        elif choice == 4:
            self.apply_cleaning_pipeline()
    
    def detect_quality_issues(self):
        """Detect data quality issues."""
        df = self.session.get_current_data()
        
        print_header("Data Quality Report")
        
        # Missing values
        missing = detect_missing_values(df)
        missing_with_issues = missing[missing['missing_count'] > 0]
        
        if len(missing_with_issues) > 0:
            print("Missing Values Found:")
            print(missing_with_issues.to_string(index=False))
        else:
            print("No missing values found")
        
        # Duplicates
        duplicates = df.duplicated().sum()
        print(f"\nDuplicate Rows: {duplicates}")
        
        # Data types
        print("\nData Types:")
        print(df.dtypes.to_string())
        
        print()
        pause()
    
    def handle_missing_values_menu(self):
        """Handle missing values."""
        print("\n[INFO] Missing value handling will modify the current data.")
        if not confirm_action("Continue"):
            return
        
        print("\nStrategies: drop, mean, median")
        strategy = get_user_input("Enter strategy", "string")
        
        if strategy not in ['drop', 'mean', 'median']:
            print("[ERROR] Invalid strategy")
            pause()
            return
        
        from src.cleaning import handle_missing_values
        df = self.session.get_current_data()
        
        try:
            cleaned = handle_missing_values(df, strategy=strategy)
            self.session.df_filtered = cleaned
            print(f"\n[SUCCESS] Applied {strategy} strategy")
            print(f"Records after cleaning: {len(cleaned)}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def remove_duplicates_menu(self):
        """Remove duplicate rows."""
        df = self.session.get_current_data()
        duplicates = df.duplicated().sum()
        
        print(f"\nFound {duplicates} duplicate rows")
        
        if duplicates == 0:
            print("[INFO] No duplicates to remove")
            pause()
            return
        
        if confirm_action("Remove duplicates?"):
            from src.cleaning import remove_duplicates
            cleaned = remove_duplicates(df)
            self.session.df_filtered = cleaned
            print(f"\n[SUCCESS] Removed {len(df) - len(cleaned)} duplicates")
            print(f"Records remaining: {len(cleaned)}")
        
        pause()
    
    def apply_cleaning_pipeline(self):
        """Apply full cleaning pipeline."""
        print("\n[INFO] This will apply a comprehensive cleaning pipeline.")
        if not confirm_action("Continue"):
            return
        
        df = self.session.get_current_data()
        
        try:
            cleaner = DataCleaner(df)
            cleaned = (cleaner
                      .remove_duplicates()
                      .handle_missing(strategy='drop')
                      .get_cleaned_data())
            
            report = cleaner.get_cleaning_report()
            self.session.df_filtered = cleaned
            
            print("\n[SUCCESS] Cleaning completed")
            print(f"Original records: {report['original_rows']}")
            print(f"Cleaned records: {report['cleaned_rows']}")
            print(f"Rows removed: {report['rows_removed']}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def export_data_menu(self):
        """Handle data export menu."""
        if not self.session.has_data():
            print("\n[INFO] No data loaded. Please load data first.")
            pause()
            return
        
        clear_screen()
        options = [
            "Export Current View to CSV",
            "Export to Database"
        ]
        
        print_menu("Export Data", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.export_to_csv_menu()
        elif choice == 2:
            self.export_to_database_menu()
    
    def export_to_csv_menu(self):
        """Export current data to CSV."""
        df = self.session.get_current_data()
        export_to_csv(df)
        pause()
    
    def export_to_database_menu(self):
        """Export to database."""
        df = self.session.get_current_data()
        
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        try:
            load_to_database(df, db_path, table_name)
            print(f"\n[SUCCESS] Exported {len(df)} records to {table_name}")
        except Exception as e:
            print(f"\n[ERROR] Failed to export: {e}")
        
        pause()
    
    def exit_dashboard(self):
        """Exit the dashboard."""
        clear_screen()
        print_header("Thank You for Using Public Health Data Dashboard!")
        print("\nGoodbye!\n")
        self.running = False


def main():
    """Main entry point for the dashboard."""
    dashboard = HealthDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()

