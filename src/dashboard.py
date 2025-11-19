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
from src.crud import (
    CRUDManager, list_tables, get_table_info, create_record,
    read_records, update_record, delete_record
)
from src.activity_logger import (
    ActivityLogger, log_data_operation, log_crud_operation, log_error,
    get_activity_stats, export_log_to_csv as export_activity_log
)


class HealthDashboard:
    """Main dashboard application class."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.session = CLISession()
        self.running = True
        
        # Initialize activity logger
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        self.logger = ActivityLogger(log_dir / "dashboard_activity.log", user="dashboard_user")
    
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
            "Export Data",
            "Database Management (CRUD)",
            "View Activity Log"
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
        elif choice == 8:
            self.database_management_menu()
        elif choice == 9:
            self.view_activity_log_menu()
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
            log_data_operation(self.logger, "load", 
                             "Loaded sample vaccination data from CSV",
                             file_path="data/sample_vaccination_data.csv",
                             records=len(df), columns=len(df.columns))
            print("\n[SUCCESS] Loaded vaccination data")
            print(f"Records: {len(df)}, Columns: {len(df.columns)}")
        except Exception as e:
            log_error(self.logger, "load_data", str(e), 
                     file_path="data/sample_vaccination_data.csv")
            print(f"\n[ERROR] Failed to load data: {e}")
        pause()
    
    def load_sample_outbreak_data(self):
        """Load sample outbreak data."""
        try:
            df = load_json_dataset("data/sample_disease_outbreak.json")
            self.session.load_data(df, "Sample Disease Outbreak Data")
            log_data_operation(self.logger, "load",
                             "Loaded sample disease outbreak data from JSON",
                             file_path="data/sample_disease_outbreak.json",
                             records=len(df), columns=len(df.columns))
            print("\n[SUCCESS] Loaded outbreak data")
            print(f"Records: {len(df)}, Columns: {len(df.columns)}")
        except Exception as e:
            log_error(self.logger, "load_data", str(e),
                     file_path="data/sample_disease_outbreak.json")
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
            log_data_operation(self.logger, "load",
                             f"Loaded custom CSV file: {filename}",
                             file_path=filepath, records=len(df), columns=len(df.columns))
            print(f"\n[SUCCESS] Loaded {filename}")
            print(f"Records: {len(df)}, Columns: {len(df.columns)}")
        except Exception as e:
            log_error(self.logger, "load_data", str(e), file_path=filepath)
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
        
        log_data_operation(self.logger, "filter",
                         f"Filtered by {col_name} = {value}",
                         original_records=len(df), filtered_records=len(filtered))
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
            log_data_operation(self.logger, "export", 
                             f"Exported {len(df)} records to database",
                             db_path=str(db_path), table=table_name, records=len(df))
            print(f"\n[SUCCESS] Exported {len(df)} records to {table_name}")
        except Exception as e:
            log_error(self.logger, "export", str(e), db_path=str(db_path))
            print(f"\n[ERROR] Failed to export: {e}")
        
        pause()
    
    def database_management_menu(self):
        """Handle database CRUD operations menu."""
        clear_screen()
        options = [
            "List All Tables in Database",
            "View Table Information",
            "Create New Record",
            "Read Records",
            "Update Record",
            "Delete Record",
            "Execute Custom Query"
        ]
        
        print_menu("Database Management (CRUD)", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.list_tables_menu()
        elif choice == 2:
            self.view_table_info_menu()
        elif choice == 3:
            self.create_record_menu()
        elif choice == 4:
            self.read_records_menu()
        elif choice == 5:
            self.update_record_menu()
        elif choice == 6:
            self.delete_record_menu()
        elif choice == 7:
            self.custom_query_menu()
    
    def list_tables_menu(self):
        """List all tables in a database."""
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        try:
            tables = list_tables(db_path)
            print_header("Tables in Database")
            if tables:
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table}")
            else:
                print("No tables found in database")
            
            log_crud_operation(self.logger, "read", "database", 
                             f"Listed {len(tables)} tables",
                             db_path=str(db_path))
        except Exception as e:
            log_error(self.logger, "list_tables", str(e), db_path=str(db_path))
            print(f"\n[ERROR] {e}")
        
        print()
        pause()
    
    def view_table_info_menu(self):
        """View information about a table."""
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        try:
            info = get_table_info(db_path, table_name)
            print_header(f"Table Information: {table_name}")
            print(f"Row Count: {info['row_count']}")
            print(f"\nColumns:")
            for col in info['columns']:
                print(f"  - {col['name']} ({col['type']})")
            
            log_crud_operation(self.logger, "read", table_name, 
                             "Viewed table information",
                             db_path=str(db_path))
        except Exception as e:
            log_error(self.logger, "table_info", str(e), 
                     db_path=str(db_path), table=table_name)
            print(f"\n[ERROR] {e}")
        
        print()
        pause()
    
    def create_record_menu(self):
        """Create a new record in a database table."""
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        try:
            # Get table info to know what columns to fill
            info = get_table_info(db_path, table_name)
            print("\nColumns in table:")
            for col in info['columns']:
                print(f"  - {col['name']} ({col['type']})")
            
            print("\nEnter values for each column (press Enter to skip):")
            record = {}
            for col in info['columns']:
                value = get_user_input(f"{col['name']}", "string")
                if value:
                    # Try to convert to appropriate type
                    if 'INT' in col['type'].upper():
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                    elif 'REAL' in col['type'].upper() or 'FLOAT' in col['type'].upper():
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    record[col['name']] = value
            
            if not record:
                print("\n[INFO] No data entered")
                pause()
                return
            
            if confirm_action(f"Create record with {len(record)} fields?"):
                create_record(db_path, table_name, record)
                log_crud_operation(self.logger, "create", table_name,
                                 f"Created new record with {len(record)} fields",
                                 db_path=str(db_path), record=str(record))
                print("\n[SUCCESS] Record created")
        except Exception as e:
            log_error(self.logger, "create_record", str(e),
                     db_path=str(db_path), table=table_name)
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def read_records_menu(self):
        """Read records from a database table."""
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        where_clause = get_user_input("Enter WHERE clause (optional, e.g., 'id=1')", "string")
        limit = get_user_input("Enter limit (optional)", "int")
        
        try:
            df = read_records(db_path, table_name, where=where_clause if where_clause else None, 
                            limit=limit)
            
            display_dataframe(df, f"Records from {table_name}", max_rows=50)
            
            # Optionally load into session
            if len(df) > 0 and confirm_action("\nLoad these records into current session?"):
                self.session.load_data(df, f"{table_name} (from database)")
                print("[SUCCESS] Data loaded into session")
            
            log_crud_operation(self.logger, "read", table_name,
                             f"Read {len(df)} records",
                             db_path=str(db_path), where=where_clause or "all")
        except Exception as e:
            log_error(self.logger, "read_records", str(e),
                     db_path=str(db_path), table=table_name)
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def update_record_menu(self):
        """Update records in a database table."""
        print("\n[WARNING] Update operations modify the database directly.")
        if not confirm_action("Continue?"):
            return
        
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        where_clause = get_user_input("Enter WHERE clause (REQUIRED, e.g., 'id=1')", "string")
        if not where_clause:
            print("\n[ERROR] WHERE clause is required for safety")
            pause()
            return
        
        try:
            print("\nEnter updates as 'column=value' (press Enter when done):")
            updates = {}
            while True:
                update_str = get_user_input("Update (or Enter to finish)", "string")
                if not update_str:
                    break
                
                if '=' in update_str:
                    col, val = update_str.split('=', 1)
                    updates[col.strip()] = val.strip()
            
            if not updates:
                print("\n[INFO] No updates specified")
                pause()
                return
            
            if confirm_action(f"Update records where {where_clause}?"):
                rows_affected = update_record(db_path, table_name, updates, where=where_clause)
                log_crud_operation(self.logger, "update", table_name,
                                 f"Updated {rows_affected} records",
                                 db_path=str(db_path), where=where_clause, 
                                 updates=str(updates))
                print(f"\n[SUCCESS] Updated {rows_affected} record(s)")
        except Exception as e:
            log_error(self.logger, "update_record", str(e),
                     db_path=str(db_path), table=table_name)
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def delete_record_menu(self):
        """Delete records from a database table."""
        print("\n[WARNING] Delete operations are irreversible!")
        if not confirm_action("Continue?"):
            return
        
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        where_clause = get_user_input("Enter WHERE clause (REQUIRED, e.g., 'id=1')", "string")
        if not where_clause:
            print("\n[ERROR] WHERE clause is required for safety")
            pause()
            return
        
        try:
            # Show records that will be deleted
            print("\n[INFO] Records matching the WHERE clause:")
            df = read_records(db_path, table_name, where=where_clause, limit=10)
            display_dataframe(df, "Records to Delete", max_rows=10)
            
            if confirm_action(f"\nDelete {len(df)} record(s)?"):
                rows_affected = delete_record(db_path, table_name, where=where_clause)
                log_crud_operation(self.logger, "delete", table_name,
                                 f"Deleted {rows_affected} records",
                                 db_path=str(db_path), where=where_clause)
                print(f"\n[SUCCESS] Deleted {rows_affected} record(s)")
        except Exception as e:
            log_error(self.logger, "delete_record", str(e),
                     db_path=str(db_path), table=table_name)
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def custom_query_menu(self):
        """Execute a custom SQL query."""
        print("\n[INFO] Execute custom SQL query on database.")
        db_path = get_user_input("Enter database path", "string")
        if not db_path:
            return
        
        table_name = get_user_input("Enter table name", "string")
        if not table_name:
            return
        
        query = get_user_input("Enter SQL query (SELECT only)", "string")
        if not query or not query.strip().upper().startswith('SELECT'):
            print("\n[ERROR] Only SELECT queries are allowed for safety")
            pause()
            return
        
        try:
            from src.main import read_from_database
            df = read_from_database(db_path, table_name, query=query)
            display_dataframe(df, "Query Results", max_rows=50)
            
            log_crud_operation(self.logger, "read", table_name,
                             "Executed custom query",
                             db_path=str(db_path), query=query)
        except Exception as e:
            log_error(self.logger, "custom_query", str(e),
                     db_path=str(db_path), query=query)
            print(f"\n[ERROR] {e}")
        
        pause()
    
    def view_activity_log_menu(self):
        """View activity log menu."""
        clear_screen()
        options = [
            "View Recent Activities",
            "View Activity Statistics",
            "Filter Activities",
            "Export Activity Log to CSV"
        ]
        
        print_menu("Activity Log", options)
        choice = get_user_choice(len(options))
        
        if choice == 1:
            self.view_recent_activities()
        elif choice == 2:
            self.view_activity_statistics()
        elif choice == 3:
            self.filter_activities_menu()
        elif choice == 4:
            self.export_activity_log_menu()
    
    def view_recent_activities(self):
        """View recent activities from the log."""
        try:
            from src.activity_logger import read_activity_log
            activities = read_activity_log(self.logger.log_file)
            
            # Show last 20 activities
            recent = activities[-20:] if len(activities) > 20 else activities
            recent.reverse()  # Most recent first
            
            print_header("Recent Activities")
            for i, activity in enumerate(recent, 1):
                timestamp = activity.get('timestamp', 'N/A')
                action = activity.get('action', 'N/A')
                desc = activity.get('description', 'N/A')
                level = activity.get('level', 'INFO')
                
                print(f"\n{i}. [{level}] {timestamp[:19]}")
                print(f"   Action: {action}")
                print(f"   Details: {desc}")
        except Exception as e:
            print(f"\n[ERROR] Failed to read activity log: {e}")
        
        print()
        pause()
    
    def view_activity_statistics(self):
        """View activity statistics."""
        try:
            stats = get_activity_stats(self.logger.log_file)
            
            print_header("Activity Statistics")
            print(f"Total Activities: {stats['total_activities']}")
            
            if stats['date_range']:
                print(f"\nDate Range:")
                print(f"  First: {stats['date_range']['first'][:19]}")
                print(f"  Last:  {stats['date_range']['last'][:19]}")
            
            print(f"\nTop Actions:")
            sorted_actions = sorted(stats['action_counts'].items(), 
                                  key=lambda x: x[1], reverse=True)
            for action, count in sorted_actions[:10]:
                print(f"  {action}: {count}")
            
            print(f"\nSeverity Levels:")
            for level, count in stats['level_counts'].items():
                print(f"  {level}: {count}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        print()
        pause()
    
    def filter_activities_menu(self):
        """Filter and view activities."""
        from src.activity_logger import filter_activities
        
        action_type = get_user_input("Filter by action (optional)", "string")
        level = get_user_input("Filter by level (optional, e.g., ERROR)", "string")
        
        try:
            filtered = filter_activities(
                self.logger.log_file,
                action=action_type if action_type else None,
                level=level.upper() if level else None
            )
            
            print_header(f"Filtered Activities ({len(filtered)} found)")
            for i, activity in enumerate(filtered[-20:], 1):  # Show last 20
                timestamp = activity.get('timestamp', 'N/A')
                action = activity.get('action', 'N/A')
                desc = activity.get('description', 'N/A')
                
                print(f"\n{i}. {timestamp[:19]} - {action}")
                print(f"   {desc}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
        print()
        pause()
    
    def export_activity_log_menu(self):
        """Export activity log to CSV."""
        output_path = get_user_input("Enter output CSV path", "string")
        if not output_path:
            output_path = "logs/activity_export.csv"
        
        try:
            export_activity_log(self.logger.log_file, output_path)
            print(f"\n[SUCCESS] Activity log exported to {output_path}")
            log_data_operation(self.logger, "export",
                             f"Exported activity log to CSV",
                             output_path=output_path)
        except Exception as e:
            print(f"\n[ERROR] {e}")
        
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

