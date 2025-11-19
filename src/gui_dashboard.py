"""
Public Health Data Dashboard - Graphical User Interface (GUI)

A simple GUI version of the dashboard using tkinter.
Provides easy access to all features with buttons and visual elements.

Step 4: Presentation Layer - GUI Implementation
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

# Import our existing modules
from src.main import (
    load_dataset, load_json_dataset, load_to_database, read_from_database
)
from src.cleaning import DataCleaner, detect_missing_values
from src.analysis import (
    filter_by_column, filter_by_numeric_range,
    calculate_summary_stats, group_and_aggregate
)
from src.crud import CRUDManager, list_tables
from src.activity_logger import ActivityLogger, get_activity_stats


class HealthDashboardGUI:
    """
    Graphical User Interface for Public Health Data Dashboard.
    
    Provides easy access to all functionality through a visual interface:
    - Data loading (CSV, JSON, Database)
    - Data viewing and exploration
    - Filtering and analysis
    - Visualizations
    - Data cleaning
    - CRUD operations
    - Activity logging
    """
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Public Health Data Insights Dashboard")
        self.root.geometry("1200x800")
        
        # Data storage
        self.df = None
        self.df_original = None
        self.current_source = "No data loaded"
        
        # Initialize activity logger
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        self.logger = ActivityLogger(log_dir / "gui_activity.log", user="gui_user")
        
        # Setup GUI
        self.setup_ui()
        
        # Log session start
        self.logger.log("session_start", "GUI Dashboard started")
        self.add_log("Dashboard started. Welcome!")
    
    def setup_ui(self):
        """Setup the user interface."""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title = ttk.Label(
            main_frame, 
            text="🏥 Public Health Data Insights Dashboard",
            font=('Arial', 16, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Left panel - Controls
        self.setup_left_panel(main_frame)
        
        # Right panel - Data display and visualizations
        self.setup_right_panel(main_frame)
        
        # Bottom panel - Status and logs
        self.setup_bottom_panel(main_frame)
    
    def setup_left_panel(self, parent):
        """Setup the left control panel."""
        left_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Data Loading Section
        load_frame = ttk.LabelFrame(left_frame, text="📂 Data Loading (Step 1)", padding="5")
        load_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(load_frame, text="Load CSV File", 
                  command=self.load_csv).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load JSON File", 
                  command=self.load_json).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load Sample Vaccination Data", 
                  command=self.load_sample_vaccination).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load Sample Outbreak Data", 
                  command=self.load_sample_outbreak).pack(fill=tk.X, pady=2)
        
        # Data Viewing Section
        view_frame = ttk.LabelFrame(left_frame, text="👁️ View Data", padding="5")
        view_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(view_frame, text="View All Data", 
                  command=self.view_data).pack(fill=tk.X, pady=2)
        ttk.Button(view_frame, text="View Statistics", 
                  command=self.view_statistics).pack(fill=tk.X, pady=2)
        ttk.Button(view_frame, text="View Data Info", 
                  command=self.view_info).pack(fill=tk.X, pady=2)
        
        # Filtering Section (Step 3)
        filter_frame = ttk.LabelFrame(left_frame, text="🔍 Filter Data (Step 3)", padding="5")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame, text="Filter by Column", 
                  command=self.filter_by_column_gui).pack(fill=tk.X, pady=2)
        ttk.Button(filter_frame, text="Filter by Numeric Range", 
                  command=self.filter_by_range_gui).pack(fill=tk.X, pady=2)
        ttk.Button(filter_frame, text="Reset Filters", 
                  command=self.reset_filters).pack(fill=tk.X, pady=2)
        
        # Analysis Section (Step 3)
        analysis_frame = ttk.LabelFrame(left_frame, text="📊 Analyze (Step 3)", padding="5")
        analysis_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(analysis_frame, text="Summary Statistics", 
                  command=self.show_summary).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Group & Aggregate", 
                  command=self.group_aggregate_gui).pack(fill=tk.X, pady=2)
        
        # Visualization Section (Step 4)
        viz_frame = ttk.LabelFrame(left_frame, text="📈 Visualize (Step 4)", padding="5")
        viz_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(viz_frame, text="Create Bar Chart", 
                  command=self.create_bar_chart_gui).pack(fill=tk.X, pady=2)
        ttk.Button(viz_frame, text="Create Line Chart", 
                  command=self.create_line_chart_gui).pack(fill=tk.X, pady=2)
        
        # Cleaning Section (Step 2)
        clean_frame = ttk.LabelFrame(left_frame, text="🧹 Clean Data (Step 2)", padding="5")
        clean_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(clean_frame, text="Detect Quality Issues", 
                  command=self.detect_quality_issues).pack(fill=tk.X, pady=2)
        ttk.Button(clean_frame, text="Remove Duplicates", 
                  command=self.remove_duplicates).pack(fill=tk.X, pady=2)
        
        # CRUD Section (Step 5)
        crud_frame = ttk.LabelFrame(left_frame, text="💾 CRUD Operations (Step 5)", padding="5")
        crud_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(crud_frame, text="Manage Database", 
                  command=self.open_crud_window).pack(fill=tk.X, pady=2)
        ttk.Button(crud_frame, text="View Activity Log", 
                  command=self.view_activity_log).pack(fill=tk.X, pady=2)
        
        # Export Section
        export_frame = ttk.LabelFrame(left_frame, text="💾 Export", padding="5")
        export_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(export_frame, text="Export to CSV", 
                  command=self.export_csv).pack(fill=tk.X, pady=2)
        ttk.Button(export_frame, text="Export to Database", 
                  command=self.export_database).pack(fill=tk.X, pady=2)
    
    def setup_right_panel(self, parent):
        """Setup the right data display panel."""
        right_frame = ttk.LabelFrame(parent, text="Data Display", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Data Table
        self.table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="📋 Data Table")
        self.setup_table_tab()
        
        # Tab 2: Visualization
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="📊 Visualization")
        
        # Tab 3: Statistics
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📈 Statistics")
        self.setup_stats_tab()
    
    def setup_table_tab(self):
        """Setup the data table tab."""
        # Create Treeview for data display
        tree_scroll = ttk.Scrollbar(self.table_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            self.table_frame,
            yscrollcommand=tree_scroll.set,
            selectmode='browse'
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)
        
        # Info label
        self.data_info_label = ttk.Label(
            self.table_frame,
            text="No data loaded",
            font=('Arial', 10)
        )
        self.data_info_label.pack(side=tk.BOTTOM, pady=5)
    
    def setup_stats_tab(self):
        """Setup the statistics tab."""
        self.stats_text = scrolledtext.ScrolledText(
            self.stats_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=('Courier', 10)
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_bottom_panel(self, parent):
        """Setup the bottom status and log panel."""
        bottom_frame = ttk.LabelFrame(parent, text="Activity Log", padding="5")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(
            bottom_frame,
            wrap=tk.WORD,
            height=6,
            font=('Courier', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            bottom_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def add_log(self, message):
        """Add a message to the activity log display."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.status_var.set(message)
    
    def load_csv(self):
        """Load a CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.df = load_dataset(filename)
                self.df_original = self.df.copy()
                self.current_source = Path(filename).name
                self.logger.log("data_loaded", f"Loaded CSV: {filename}",
                              metadata={"file": filename, "rows": len(self.df)})
                self.add_log(f"✅ Loaded {len(self.df)} records from {Path(filename).name}")
                self.update_table()
            except Exception as e:
                self.logger.log("error", f"Failed to load CSV: {str(e)}", level="ERROR")
                messagebox.showerror("Error", f"Failed to load CSV:\n{str(e)}")
    
    def load_json(self):
        """Load a JSON file."""
        filename = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.df = load_json_dataset(filename)
                self.df_original = self.df.copy()
                self.current_source = Path(filename).name
                self.logger.log("data_loaded", f"Loaded JSON: {filename}",
                              metadata={"file": filename, "rows": len(self.df)})
                self.add_log(f"✅ Loaded {len(self.df)} records from {Path(filename).name}")
                self.update_table()
            except Exception as e:
                self.logger.log("error", f"Failed to load JSON: {str(e)}", level="ERROR")
                messagebox.showerror("Error", f"Failed to load JSON:\n{str(e)}")
    
    def load_sample_vaccination(self):
        """Load sample vaccination data."""
        try:
            self.df = load_dataset("data/sample_vaccination_data.csv")
            self.df_original = self.df.copy()
            self.current_source = "Sample Vaccination Data"
            self.logger.log("data_loaded", "Loaded sample vaccination data",
                          metadata={"rows": len(self.df)})
            self.add_log(f"✅ Loaded sample vaccination data ({len(self.df)} records)")
            self.update_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sample data:\n{str(e)}")
    
    def load_sample_outbreak(self):
        """Load sample outbreak data."""
        try:
            self.df = load_json_dataset("data/sample_disease_outbreak.json")
            self.df_original = self.df.copy()
            self.current_source = "Sample Outbreak Data"
            self.logger.log("data_loaded", "Loaded sample outbreak data",
                          metadata={"rows": len(self.df)})
            self.add_log(f"✅ Loaded sample outbreak data ({len(self.df)} records)")
            self.update_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sample data:\n{str(e)}")
    
    def update_table(self):
        """Update the data table display."""
        if self.df is None or self.df.empty:
            self.data_info_label.config(text="No data loaded")
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Setup columns
        self.tree['columns'] = list(self.df.columns)
        self.tree['show'] = 'headings'
        
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Add data (first 1000 rows for performance)
        for idx, row in self.df.head(1000).iterrows():
            self.tree.insert('', tk.END, values=list(row))
        
        # Update info
        info_text = f"Showing {min(len(self.df), 1000)} of {len(self.df)} records | "
        info_text += f"{len(self.df.columns)} columns | Source: {self.current_source}"
        self.data_info_label.config(text=info_text)
    
    def view_data(self):
        """Switch to data table view."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        self.notebook.select(self.table_frame)
        self.add_log(f"📋 Viewing {len(self.df)} records")
    
    def view_statistics(self):
        """Show summary statistics."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "📊 SUMMARY STATISTICS\n")
        self.stats_text.insert(tk.END, "="*60 + "\n\n")
        
        # Basic info
        self.stats_text.insert(tk.END, f"Dataset: {self.current_source}\n")
        self.stats_text.insert(tk.END, f"Records: {len(self.df)}\n")
        self.stats_text.insert(tk.END, f"Columns: {len(self.df.columns)}\n\n")
        
        # Describe numeric columns
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            self.stats_text.insert(tk.END, "Numeric Column Statistics:\n")
            self.stats_text.insert(tk.END, "-"*60 + "\n")
            self.stats_text.insert(tk.END, str(self.df[numeric_cols].describe()) + "\n\n")
        
        # Column types
        self.stats_text.insert(tk.END, "Column Data Types:\n")
        self.stats_text.insert(tk.END, "-"*60 + "\n")
        for col in self.df.columns:
            self.stats_text.insert(tk.END, f"{col}: {self.df[col].dtype}\n")
        
        self.notebook.select(self.stats_frame)
        self.logger.log("analysis", "Viewed summary statistics")
        self.add_log("📊 Summary statistics displayed")
    
    def view_info(self):
        """Show data info."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        info = f"Dataset Information\n{'='*50}\n\n"
        info += f"Source: {self.current_source}\n"
        info += f"Total Records: {len(self.df)}\n"
        info += f"Total Columns: {len(self.df.columns)}\n\n"
        info += f"Columns:\n"
        for col in self.df.columns:
            info += f"  • {col} ({self.df[col].dtype})\n"
        
        messagebox.showinfo("Data Information", info)
    
    def filter_by_column_gui(self):
        """Filter data by column value."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        # Create filter dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Filter by Column")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Select Column:").pack(pady=5)
        col_var = tk.StringVar()
        col_combo = ttk.Combobox(dialog, textvariable=col_var, values=list(self.df.columns))
        col_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Enter Value:").pack(pady=5)
        value_entry = ttk.Entry(dialog, width=30)
        value_entry.pack(pady=5)
        
        def apply_filter():
            col = col_var.get()
            value = value_entry.get()
            if col and value:
                try:
                    self.df = filter_by_column(self.df, col, value)
                    self.logger.log("data_filtered", f"Filtered by {col}={value}",
                                  metadata={"column": col, "value": value, "result_rows": len(self.df)})
                    self.add_log(f"🔍 Filtered by {col}={value} → {len(self.df)} records")
                    self.update_table()
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Apply Filter", command=apply_filter).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def filter_by_range_gui(self):
        """Filter data by numeric range."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            messagebox.showinfo("No Numeric Columns", "No numeric columns available for filtering.")
            return
        
        # Create filter dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Filter by Numeric Range")
        dialog.geometry("400x350")
        
        ttk.Label(dialog, text="Select Column:").pack(pady=5)
        col_var = tk.StringVar()
        col_combo = ttk.Combobox(dialog, textvariable=col_var, values=numeric_cols)
        col_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Minimum Value (optional):").pack(pady=5)
        min_entry = ttk.Entry(dialog, width=30)
        min_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Maximum Value (optional):").pack(pady=5)
        max_entry = ttk.Entry(dialog, width=30)
        max_entry.pack(pady=5)
        
        def apply_filter():
            col = col_var.get()
            min_val = min_entry.get()
            max_val = max_entry.get()
            
            if col:
                try:
                    min_v = float(min_val) if min_val else None
                    max_v = float(max_val) if max_val else None
                    self.df = filter_by_numeric_range(self.df, col, min_v, max_v)
                    self.logger.log("data_filtered", f"Filtered by range {col} [{min_v}, {max_v}]",
                                  metadata={"column": col, "min": min_v, "max": max_v, "result_rows": len(self.df)})
                    self.add_log(f"🔍 Filtered by range → {len(self.df)} records")
                    self.update_table()
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Apply Filter", command=apply_filter).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def reset_filters(self):
        """Reset all filters."""
        if self.df_original is not None:
            self.df = self.df_original.copy()
            self.logger.log("data_filtered", "Reset all filters")
            self.add_log("🔄 Filters reset - showing all records")
            self.update_table()
        else:
            messagebox.showinfo("No Data", "Please load data first.")
    
    def show_summary(self):
        """Show summary statistics in dialog."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        self.view_statistics()
    
    def group_aggregate_gui(self):
        """Group and aggregate data."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Group & Aggregate")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Group By Column:").pack(pady=5)
        group_var = tk.StringVar()
        group_combo = ttk.Combobox(dialog, textvariable=group_var, values=list(self.df.columns))
        group_combo.pack(pady=5)
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        ttk.Label(dialog, text="Aggregate Column:").pack(pady=5)
        agg_var = tk.StringVar()
        agg_combo = ttk.Combobox(dialog, textvariable=agg_var, values=numeric_cols)
        agg_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Function (sum, mean, count, min, max):").pack(pady=5)
        func_entry = ttk.Entry(dialog, width=30)
        func_entry.insert(0, "sum")
        func_entry.pack(pady=5)
        
        def apply_group():
            group_col = group_var.get()
            agg_col = agg_var.get()
            func = func_entry.get()
            
            if group_col and agg_col and func:
                try:
                    result = group_and_aggregate(self.df, group_col, agg_col, func)
                    
                    # Display result
                    result_text = f"Grouped by {group_col}, {func}({agg_col}):\n\n"
                    result_text += str(result)
                    
                    messagebox.showinfo("Aggregation Result", result_text)
                    self.logger.log("analysis", f"Grouped by {group_col}, {func}({agg_col})")
                    self.add_log(f"📊 Grouped by {group_col}")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Apply", command=apply_group).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def create_bar_chart_gui(self):
        """Create a bar chart."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Bar Chart")
        dialog.geometry("400x350")
        
        ttk.Label(dialog, text="X-axis (Category):").pack(pady=5)
        x_var = tk.StringVar()
        x_combo = ttk.Combobox(dialog, textvariable=x_var, values=list(self.df.columns))
        x_combo.pack(pady=5)
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        ttk.Label(dialog, text="Y-axis (Value):").pack(pady=5)
        y_var = tk.StringVar()
        y_combo = ttk.Combobox(dialog, textvariable=y_var, values=numeric_cols)
        y_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Chart Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=30)
        title_entry.pack(pady=5)
        
        def create_chart():
            x_col = x_var.get()
            y_col = y_var.get()
            title = title_entry.get() or f"{y_col} by {x_col}"
            
            if x_col and y_col:
                try:
                    # Create chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    data_to_plot = self.df.head(20)  # Limit to 20 bars
                    ax.bar(data_to_plot[x_col].astype(str), data_to_plot[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(title)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.show()
                    
                    self.logger.log("visualization", f"Created bar chart: {title}")
                    self.add_log(f"📊 Created bar chart: {title}")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Create Chart", command=create_chart).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def create_line_chart_gui(self):
        """Create a line chart."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        # Similar to bar chart but with line plot
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Line Chart")
        dialog.geometry("400x350")
        
        ttk.Label(dialog, text="X-axis:").pack(pady=5)
        x_var = tk.StringVar()
        x_combo = ttk.Combobox(dialog, textvariable=x_var, values=list(self.df.columns))
        x_combo.pack(pady=5)
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        ttk.Label(dialog, text="Y-axis:").pack(pady=5)
        y_var = tk.StringVar()
        y_combo = ttk.Combobox(dialog, textvariable=y_var, values=numeric_cols)
        y_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Chart Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=30)
        title_entry.pack(pady=5)
        
        def create_chart():
            x_col = x_var.get()
            y_col = y_var.get()
            title = title_entry.get() or f"{y_col} over {x_col}"
            
            if x_col and y_col:
                try:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(self.df[x_col], self.df[y_col], marker='o')
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(title)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.show()
                    
                    self.logger.log("visualization", f"Created line chart: {title}")
                    self.add_log(f"📈 Created line chart: {title}")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Create Chart", command=create_chart).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def detect_quality_issues(self):
        """Detect data quality issues."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        try:
            missing = detect_missing_values(self.df)
            duplicates = self.df.duplicated().sum()
            
            report = "📋 DATA QUALITY REPORT\n"
            report += "="*50 + "\n\n"
            report += f"Total Records: {len(self.df)}\n"
            report += f"Duplicate Rows: {duplicates}\n\n"
            
            missing_issues = missing[missing['missing_count'] > 0]
            if len(missing_issues) > 0:
                report += "Missing Values:\n"
                report += str(missing_issues.to_string(index=False)) + "\n\n"
            else:
                report += "✅ No missing values found\n\n"
            
            report += "Column Data Types:\n"
            for col in self.df.columns:
                report += f"  • {col}: {self.df[col].dtype}\n"
            
            messagebox.showinfo("Quality Report", report)
            self.logger.log("data_cleaned", "Detected data quality issues")
            self.add_log("🧹 Quality report generated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def remove_duplicates(self):
        """Remove duplicate rows."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        duplicates = self.df.duplicated().sum()
        if duplicates == 0:
            messagebox.showinfo("No Duplicates", "No duplicate rows found.")
            return
        
        if messagebox.askyesno("Confirm", f"Remove {duplicates} duplicate rows?"):
            self.df = self.df.drop_duplicates()
            self.logger.log("data_cleaned", f"Removed {duplicates} duplicates")
            self.add_log(f"🧹 Removed {duplicates} duplicate rows")
            self.update_table()
    
    def export_csv(self):
        """Export data to CSV."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.df.to_csv(filename, index=False)
                self.logger.log("data_exported", f"Exported to CSV: {filename}",
                              metadata={"file": filename, "rows": len(self.df)})
                self.add_log(f"💾 Exported {len(self.df)} records to {Path(filename).name}")
                messagebox.showinfo("Success", f"Data exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def export_database(self):
        """Export data to database."""
        if self.df is None:
            messagebox.showinfo("No Data", "Please load data first.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Export to Database")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Database Path:").pack(pady=5)
        db_entry = ttk.Entry(dialog, width=40)
        db_entry.pack(pady=5)
        
        def browse_db():
            filename = filedialog.asksaveasfilename(
                title="Select Database",
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            if filename:
                db_entry.delete(0, tk.END)
                db_entry.insert(0, filename)
        
        ttk.Button(dialog, text="Browse...", command=browse_db).pack(pady=5)
        
        ttk.Label(dialog, text="Table Name:").pack(pady=5)
        table_entry = ttk.Entry(dialog, width=40)
        table_entry.pack(pady=5)
        
        def export():
            db_path = db_entry.get()
            table_name = table_entry.get()
            
            if db_path and table_name:
                try:
                    load_to_database(self.df, db_path, table_name)
                    self.logger.log("data_exported", f"Exported to database: {table_name}",
                                  metadata={"db": db_path, "table": table_name, "rows": len(self.df)})
                    self.add_log(f"💾 Exported to database: {table_name}")
                    messagebox.showinfo("Success", f"Data exported to:\n{db_path}\nTable: {table_name}")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Export", command=export).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def open_crud_window(self):
        """Open CRUD management window."""
        messagebox.showinfo(
            "CRUD Operations",
            "CRUD Database Management\n\n"
            "Features:\n"
            "• Create records\n"
            "• Read/Query data\n"
            "• Update records\n"
            "• Delete records\n\n"
            "Use the CLI version (python src/dashboard.py)\n"
            "for full CRUD functionality."
        )
    
    def view_activity_log(self):
        """View activity log."""
        try:
            stats = get_activity_stats(self.logger.log_file)
            
            info = "📊 ACTIVITY LOG STATISTICS\n"
            info += "="*50 + "\n\n"
            info += f"Total Activities: {stats['total_activities']}\n\n"
            
            if stats['action_counts']:
                info += "Top Actions:\n"
                sorted_actions = sorted(stats['action_counts'].items(), 
                                      key=lambda x: x[1], reverse=True)
                for action, count in sorted_actions[:10]:
                    info += f"  • {action}: {count}\n"
                
                info += f"\nSeverity Levels:\n"
                for level, count in stats['level_counts'].items():
                    info += f"  • {level}: {count}\n"
            
            messagebox.showinfo("Activity Log", info)
            self.add_log("📊 Viewed activity log statistics")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def on_closing(self):
        """Handle window closing."""
        self.logger.log("session_end", "GUI Dashboard closed")
        self.root.destroy()


def main():
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = HealthDashboardGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

