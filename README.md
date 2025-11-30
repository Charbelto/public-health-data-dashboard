# Public Health Data Insights Dashboard

This project is a comprehensive Python tool to explore public health datasets
(e.g. vaccination rates, disease outbreaks, or mental health reports).

## 🚀 Quick Start (TL;DR)

**Want to run the app right now?** Here's the fastest way:

```powershell
# 1. Install dependencies (first time only)
pip install -r requirements.txt

# 2. Run the GUI Dashboard (recommended)
$env:PYTHONPATH="$PWD"; python src/gui_dashboard.py
```

That's it! The GUI opens with all features ready to use. 🎉

**Alternative:** For command-line interface, run `python src/dashboard.py` instead.

---

## Project Overview

**Aim**: Build a Python-based data insights tool for researchers analyzing public health data.

**Scope**: Support data access, filtering, cleaning, summarization, and presentation (not predictive modeling).

## Core Features

### ✅ Completed - Step 1: Data Access & Loading

- **CSV Loading**: Read vaccination and health data from CSV files
- **JSON Loading**: Import disease outbreak data from JSON files
- **API Integration**: Framework for loading data from public APIs (WHO, UK Gov, etc.)
- **Database Storage**: Store data in SQLite database for efficient querying
- **Data Retrieval**: Query and filter data from database with SQL support

### ✅ Completed - Step 2: Data Cleaning & Structuring

- **Missing Value Detection**: Identify and summarize missing data
- **Missing Value Handling**: 5 strategies (drop, mean, median, constant, forward/backward fill)
- **Duplicate Detection and Removal**: Find and remove duplicate records
- **Type Conversion**: Convert strings to datetime and numeric types
- **Data Validation**: Range checking and invalid data detection
- **Outlier Detection**: IQR and Z-score methods for anomaly identification
- **Text Standardization**: Clean and normalize text data
- **DataCleaner Class**: Fluent interface for chaining cleaning operations

### ✅ Completed - Step 3: Filtering and Summary Views

- **Column Filtering**: Filter by single or multiple column values
- **Date Range Filtering**: Filter by start/end dates with flexible ranges
- **Numeric Range Filtering**: Filter by min/max numeric values
- **Multiple Criteria Filtering**: Combine multiple filters simultaneously
- **Summary Statistics**: Calculate mean, median, min, max, count, sum, std
- **Grouping and Aggregation**: Group by columns with aggregate functions
- **Trend Analysis**: Calculate trends over time with growth rates
- **Moving Averages**: Calculate rolling averages for time series
- **DataAnalyzer Class**: Fluent interface for chaining analysis operations

### ✅ Completed - Step 4: Presentation Layer (CLI)

- **Interactive Dashboard**: Menu-driven command-line interface
- **Data Loading Menu**: Load CSV, JSON, or database with file browser
- **View Data Menu**: Display data, info, columns, and statistics
- **Filter Data Menu**: Interactive filtering with multiple criteria
- **Analyze Data Menu**: Calculate statistics, group data, analyze trends
- **Visualize Data Menu**: Create bar charts, line charts, grouped charts
- **Clean Data Menu**: Detect issues, handle missing values, remove duplicates
- **Export Data Menu**: Export to CSV or database
- **Session Management**: Track loaded data and applied filters
- **Error Handling**: Comprehensive error messages and validation

### ✅ Completed - Step 5: Extension Features

- **CRUD Operations**: Full Create, Read, Update, Delete functionality for database management
- **Activity Logging**: Comprehensive logging of all user activities to file
- **Database Management Menu**: Interactive CLI for database operations
- **Activity Log Viewer**: View, filter, and export activity logs
- **Export Activity Logs**: Export logs to CSV format

## Project Structure

```
public-health-data-dashboard/
├── data/                                # Data directory
│   ├── sample_vaccination_data.csv      # Clean sample vaccination dataset
│   ├── sample_disease_outbreak.json     # Clean sample outbreak dataset
│   ├── dirty_vaccination_data.csv       # Dirty data for cleaning demo
│   ├── dirty_disease_outbreak.json      # Dirty data for cleaning demo
│   ├── health_data.db                   # SQLite database (generated)
│   └── health_data_cleaned.db           # Cleaned data database (generated)
├── docs/                                # Documentation
│   ├── API_REFERENCE.md                 # Function documentation
│   └── DATA_FLOW_DIAGRAM.md             # Architecture diagrams
├── src/                                 # Source code
│   ├── main.py                          # Core data loading functions
│   ├── data_loader.py                   # DataLoader class and demonstration
│   ├── cleaning.py                      # Data cleaning functions
│   ├── cleaning_demo.py                 # Cleaning demonstration script
│   ├── analysis.py                      # Data analysis and filtering
│   ├── cli.py                           # CLI presentation layer
│   ├── dashboard.py                     # Interactive dashboard (MAIN APP)
│   ├── crud.py                          # CRUD operations for databases
│   └── activity_logger.py               # Activity logging functionality
├── tests/                               # Test suite (TDD approach)
│   ├── test_main.py                     # 21 data loading tests
│   ├── test_cleaning.py                 # 28 data cleaning tests
│   ├── test_analysis.py                 # 29 data analysis tests
│   ├── test_crud.py                     # 27 CRUD operation tests
│   └── test_activity_logger.py          # 24 activity logging tests
├── logs/                                # Activity logs (generated)
├── requirements.txt                     # Python dependencies
├── README.md                            # This file
├── STEP1_SUMMARY.md                     # Step 1 implementation report
└── STEP2_SUMMARY.md                     # Step 2 implementation report
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd public-health-data-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - pandas >= 2.0.0
   - matplotlib >= 3.7.0
   - SQLAlchemy >= 2.0.0
   - pytest >= 7.4.0
   - requests >= 2.31.0
   - pytest-mock >= 3.11.0
   - scipy >= 1.11.0
   - numpy >= 1.24.0

## Usage

### 🚀 Quick Start - Running the Complete Application

This application has **two main interfaces** plus several demonstration scripts. Choose based on your preference:

#### **Option 1: GUI Dashboard (🎨 Recommended)**

The **full-featured graphical interface** with embedded visualizations - best for visual exploration and analysis.

**Windows PowerShell:**
```powershell
$env:PYTHONPATH="$PWD"; python src/gui_dashboard.py
```

**Windows CMD:**
```cmd
set PYTHONPATH=%CD%
python src/gui_dashboard.py
```

**Linux/Mac:**
```bash
export PYTHONPATH=$PWD && python src/gui_dashboard.py
```

**GUI Features:**
- ✅ **Beautiful Visual Interface** - Modern tkinter-based GUI
- ✅ **Embedded Visualizations** - 5 chart types (bar, line, histogram, pie, scatter) display inside the window
- ✅ **Interactive Data Tables** - Scrollable, sortable data views
- ✅ **All 5 Steps Accessible** - Complete functionality through organized button panels
- ✅ **Tab-Based Navigation** - Switch between Data Table, Visualizations, and Statistics
- ✅ **Real-Time Activity Logging** - See every action logged at the bottom
- ✅ **File Browser Integration** - Easy file selection for loading/exporting
- ✅ **Correlation Heatmaps** - Visual correlation analysis
- ✅ **Full Cleaning Pipeline** - One-click data cleaning
- ✅ **Group & Aggregate** - Interactive grouping and aggregation

**Perfect for:** Exploratory data analysis, presentations, and users who prefer visual interfaces.

---

#### **Option 2: CLI Dashboard (💻 Alternative)**

The **interactive command-line menu** - best for terminal users and automation.

**Windows PowerShell:**
```powershell
$env:PYTHONPATH="$PWD"; python src/dashboard.py
```

**Windows CMD:**
```cmd
set PYTHONPATH=%CD%
python src/dashboard.py
```

**Linux/Mac:**
```bash
export PYTHONPATH=$PWD && python src/dashboard.py
```

**CLI Features:**
- ✅ **Menu-Driven Interface** - Numbered menu options for all operations
- ✅ **Data Loading** - Load CSV, JSON, or database files
- ✅ **Interactive Filtering** - Filter by column, range, or multiple criteria
- ✅ **Statistical Analysis** - Calculate summary statistics, trends, moving averages
- ✅ **Visualizations** - Generate charts (displayed in separate matplotlib windows)
- ✅ **Data Cleaning** - Detect issues, remove duplicates, handle missing values
- ✅ **CRUD Operations** - Full database management (Create, Read, Update, Delete)
- ✅ **Export Options** - Export to CSV or SQLite database
- ✅ **Activity Logging** - View activity logs and statistics
- ✅ **Session Management** - Tracks your current dataset and applied filters

**Perfect for:** Command-line enthusiasts, scripting, and terminal-based workflows.

---

### 📚 Demo Scripts - Exploring Individual Features

Run these to see demonstrations of specific functionality:

#### **Step 1: Data Loading Demo**

Demonstrates loading data from CSV, JSON, and APIs, plus database operations.

```bash
# Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/data_loader.py

# Linux/Mac:
export PYTHONPATH=$PWD && python src/data_loader.py
```

**What it shows:**
- Loading vaccination data from CSV
- Loading disease outbreak data from JSON
- Storing data in SQLite database
- Querying data with SQL
- All with sample output and timing

#### **Step 2: Data Cleaning Demo**

Demonstrates all data cleaning capabilities with before/after comparisons.

```bash
# Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/cleaning_demo.py

# Linux/Mac:
export PYTHONPATH=$PWD && python src/cleaning_demo.py
```

**What it shows:**
- Detecting data quality issues (missing values, duplicates, outliers)
- Multiple missing value handling strategies
- Duplicate removal
- Type conversions (dates, numerics)
- Data validation and range filtering
- Text standardization
- Complete cleaning pipeline with reports

#### **Step 3: Analysis Demo**

Demonstrates filtering, statistics, and trend analysis features.

```bash
# Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/analysis_demo.py

# Linux/Mac:
export PYTHONPATH=$PWD && python src/analysis_demo.py
```

**What it shows:**
- Filtering by columns, dates, and numeric ranges
- Summary statistics (mean, median, std, etc.)
- Grouping and aggregation
- Trend analysis over time
- Moving averages
- Multiple filter combinations
- Export to CSV

#### **Step 4: CLI Demo**

Quick command-line interface demonstration.

```bash
# Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/cli.py

# Linux/Mac:
export PYTHONPATH=$PWD && python src/cli.py
```

**What it shows:**
- Basic CLI table formatting
- Data display and presentation

#### **Step 5: Interactive CLI (Advanced)**

Full-featured interactive command-line with all CRUD operations.

```bash
# Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/interactive_cli.py

# Linux/Mac:
export PYTHONPATH=$PWD && python src/interactive_cli.py
```

**What it shows:**
- Complete CRUD menu
- Database management
- Activity log viewing
- All interactive features

---

### 🎯 Which One Should You Run?

| **Use Case** | **Recommended** | **Command** |
|--------------|----------------|-------------|
| **General use** | 🎨 GUI Dashboard | `$env:PYTHONPATH="$PWD"; python src/gui_dashboard.py` |
| **Visual analysis** | 🎨 GUI Dashboard | `$env:PYTHONPATH="$PWD"; python src/gui_dashboard.py` |
| **Presentations** | 🎨 GUI Dashboard | `$env:PYTHONPATH="$PWD"; python src/gui_dashboard.py` |
| **Terminal users** | 💻 CLI Dashboard | `$env:PYTHONPATH="$PWD"; python src/dashboard.py` |
| **Learn features** | 📚 Demo Scripts | Run any `*_demo.py` script |
| **Automated testing** | 🧪 Test Suite | `pytest tests/ -v` |

---

### ⚙️ Prerequisites Check

Before running, ensure you have:

1. **Python 3.10 or higher**
   ```bash
   python --version  # Should show 3.10+
   ```

2. **All dependencies installed**
   ```bash
   pip install -r requirements.txt
   ```

3. **In the project directory**
   ```bash
   cd C:\Users\Charbel\Desktop\public-health-data-dashboard
   ```

---

### 🔧 Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'src'`
- **Solution:** Make sure you set `PYTHONPATH` before running:
  ```powershell
  $env:PYTHONPATH="$PWD"
  python src/gui_dashboard.py
  ```

**Problem:** `ModuleNotFoundError: No module named 'pandas'` (or matplotlib, etc.)
- **Solution:** Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

**Problem:** Charts don't appear in GUI
- **Solution:** They appear in the **Visualization tab** - click the tab to see them!

**Problem:** "No such file or directory" errors
- **Solution:** Make sure you're in the project root directory:
  ```bash
  cd C:\Users\Charbel\Desktop\public-health-data-dashboard
  ```

**Problem:** PowerShell execution policy errors
- **Solution:** Run PowerShell as Administrator, or use CMD instead:
  ```cmd
  set PYTHONPATH=%CD%
  python src/gui_dashboard.py
  ```

### Running Tests

**Run All Tests**

```bash
# Run all tests (49 tests total)
pytest tests/ -v

# Run data loading tests only (21 tests)
pytest tests/test_main.py -v

# Run data cleaning tests only (28 tests)
pytest tests/test_cleaning.py -v
```

**Test Coverage Report**

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Using CRUD Operations

**Database CRUD (Step 5)**

```python
from src.crud import CRUDManager

# Initialize CRUD manager
crud = CRUDManager("data/health_data.db")

# List all tables
tables = crud.get_tables()

# Create a new record
crud.create("patients", {"id": 1, "name": "John Doe", "age": 30})

# Read records with filter
patients = crud.read("patients", where="age > 25")

# Update a record
crud.update("patients", {"age": 31}, where="id=1")

# Delete a record
crud.delete("patients", where="id=1")

# Get table information
info = crud.get_table_info("patients")
```

**Activity Logging (Step 5)**

```python
from src.activity_logger import ActivityLogger, get_activity_stats

# Initialize logger
logger = ActivityLogger("logs/activity.log", user="analyst1")

# Log activities
logger.log("data_loaded", "Loaded vaccination data from CSV")
logger.log("data_filtered", "Filtered by country=UK", 
          metadata={"records": 100})

# View activity statistics
stats = get_activity_stats("logs/activity.log")
print(f"Total activities: {stats['total_activities']}")

# Export logs to CSV
from src.activity_logger import export_log_to_csv
export_log_to_csv("logs/activity.log", "reports/activity_report.csv")
```

### Using the Core Functions

**Data Loading (Step 1)**

```python
from src.main import (
    load_dataset,
    load_json_dataset,
    load_to_database,
    read_from_database
)

# Load CSV data
df = load_dataset("data/sample_vaccination_data.csv")

# Load JSON data
df_json = load_json_dataset("data/sample_disease_outbreak.json")

# Store in database
load_to_database(df, "data/my_data.db", "vaccinations")

# Query from database
result = read_from_database(
    "data/my_data.db", 
    "vaccinations",
    query="SELECT * FROM vaccinations WHERE country='United Kingdom'"
)
```

**Data Cleaning (Step 2)**

```python
from src.cleaning import DataCleaner

# Load dirty data
df = load_dataset("data/dirty_vaccination_data.csv")

# Apply comprehensive cleaning
cleaner = DataCleaner(df)
clean_df = (cleaner
            .remove_duplicates()
            .handle_missing(strategy='drop')
            .convert_column_type('year', 'numeric', errors='coerce')
            .standardize_column('country', strip=True)
            .filter_by_range('vaccination_rate', 0, 1)
            .get_cleaned_data())

# Get cleaning report
report = cleaner.get_cleaning_report()
print(f"Removed {report['rows_removed']} invalid records")
```

## Development Approach

### Test-Driven Development (TDD)

This project follows TDD principles:

1. ✅ **Write tests first** - Tests were written before implementation
2. ✅ **Red-Green-Refactor** - Tests fail initially, then implementation makes them pass
3. ✅ **Comprehensive coverage** - 49 tests covering normal cases, edge cases, and error handling
4. ✅ **Automated testing** - All tests can be run with a single pytest command

**Test Statistics:**
- Step 1 (Data Loading): 21 tests
- Step 2 (Data Cleaning): 28 tests
- Step 3 (Filtering & Analysis): 29 tests
- Step 5 (CRUD Operations): 27 tests
- Step 5 (Activity Logging): 24 tests
- **Total**: 129 tests, all passing ✅

### Software Engineering Best Practices

- **Modular design**: Separate concerns (data loading, database operations, presentation)
- **Type hints**: All functions use Python type annotations for clarity
- **Documentation**: Comprehensive docstrings following NumPy style
- **Error handling**: Proper exception handling with meaningful error messages
- **Code quality**: No linter errors, follows PEP 8 style guidelines

## Data Sources

### Sample Datasets Included

1. **Vaccination Data** (`sample_vaccination_data.csv`):
   - Countries: UK, USA, France, Germany, Canada
   - Timeframe: December 2020 - March 2021
   - Metrics: doses administered, population, vaccination rate

2. **Disease Outbreak Data** (`sample_disease_outbreak.json`):
   - Diseases: Influenza, Measles, Tuberculosis
   - Metrics: confirmed cases, deaths, recovered, active cases

### Extensibility for Real APIs

The `load_from_api()` function supports integration with real public health APIs:

- WHO COVID-19 API
- UK Government Health Data API
- CDC Data API
- European CDC API
- Our World in Data API

## Testing Strategy

The test suite covers:

### CSV Loading Tests (4 tests)
- Normal loading
- Missing file handling
- Empty CSV handling
- Various data types

### JSON Loading Tests (4 tests)
- Normal loading
- Missing file handling
- Invalid JSON handling
- Empty data handling

### API Loading Tests (5 tests)
- Successful API calls
- Nested data extraction
- Query parameters
- Error handling
- Various response formats

### Database Tests (8 tests)
- Loading to database
- Reading from database
- SQL queries
- Empty DataFrame handling
- Invalid table names
- Missing database handling
- Missing table handling
- Append mode

## 📁 Source Files Reference

Understanding what each file does and when to run it:

### 🎯 Main Application Files (Run These!)

| **File** | **Purpose** | **When to Use** | **Command** |
|----------|------------|----------------|------------|
| **`src/gui_dashboard.py`** | **Full GUI Application** | Best for visual analysis, presentations, general use | `$env:PYTHONPATH="$PWD"; python src/gui_dashboard.py` |
| **`src/dashboard.py`** | **Full CLI Application** | Best for terminal users, automation | `$env:PYTHONPATH="$PWD"; python src/dashboard.py` |
| **`src/interactive_cli.py`** | **Advanced CLI with CRUD** | Complete command-line experience with database operations | `$env:PYTHONPATH="$PWD"; python src/interactive_cli.py` |

### 📚 Demonstration Files (Run These to Learn!)

| **File** | **Purpose** | **What it Demonstrates** |
|----------|------------|-------------------------|
| **`src/data_loader.py`** | Step 1 Demo | Loading CSV, JSON, API data; database storage and queries |
| **`src/cleaning_demo.py`** | Step 2 Demo | Data cleaning: missing values, duplicates, outliers, validation |
| **`src/analysis_demo.py`** | Step 3 Demo | Filtering, statistics, grouping, trends, moving averages |
| **`src/cli_demo.py`** | Step 4 Demo | Command-line table display and formatting |

### 🛠️ Core Library Files (Import These!)

These are the building blocks used by the main applications:

| **File** | **Purpose** | **Key Functions/Classes** |
|----------|------------|---------------------------|
| **`src/main.py`** | Data Loading Core | `load_dataset()`, `load_json_dataset()`, `load_from_api()`, `load_to_database()`, `read_from_database()` |
| **`src/cleaning.py`** | Data Cleaning Core | `DataCleaner` class, `detect_missing_values()`, `remove_duplicates()`, `handle_missing()`, `detect_outliers()` |
| **`src/analysis.py`** | Analysis & Filtering Core | `DataAnalyzer` class, `filter_by_column()`, `filter_by_date_range()`, `calculate_summary()`, `group_and_aggregate()` |
| **`src/cli.py`** | CLI Display Functions | `display_dataframe()`, `display_statistics()`, `display_table()` |
| **`src/crud.py`** | Database CRUD Operations | `CRUDManager` class, `create()`, `read()`, `update()`, `delete()` |
| **`src/activity_logger.py`** | Activity Logging | `ActivityLogger` class, `log()`, `get_activity_stats()`, `export_log_to_csv()` |

### 🧪 Test Files (Run with pytest!)

| **File** | **Tests** | **Coverage** |
|----------|-----------|-------------|
| **`tests/test_main.py`** | 21 tests | Data loading, JSON/CSV parsing, API calls, database operations |
| **`tests/test_cleaning.py`** | 28 tests | Missing values, duplicates, outliers, validation, text cleaning |
| **`tests/test_analysis.py`** | 29 tests | Filtering, statistics, grouping, trends, moving averages |
| **`tests/test_cli.py`** | Various | CLI display and formatting functions |
| **`tests/test_crud.py`** | 27 tests | Create, Read, Update, Delete database operations |
| **`tests/test_activity_logger.py`** | 24 tests | Activity logging, statistics, export functionality |

### 📊 Data Files

| **File** | **Purpose** |
|----------|------------|
| **`data/sample_vaccination_data.csv`** | Clean sample vaccination dataset (15 records) |
| **`data/sample_disease_outbreak.json`** | Clean sample outbreak dataset |
| **`data/dirty_vaccination_data.csv`** | Dirty data with missing values, duplicates (for cleaning demos) |
| **`data/dirty_disease_outbreak.json`** | Dirty outbreak data (for cleaning demos) |
| **`data/health_data.db`** | SQLite database (auto-generated when you load data) |
| **`data/health_data_cleaned.db`** | Cleaned data database (auto-generated) |

### 📝 Documentation Files

| **File** | **Content** |
|----------|------------|
| **`README.md`** | This file - complete project documentation |
| **`GUI_QUICK_START.md`** | Detailed GUI usage guide with screenshots and workflows |
| **`GUI_USER_GUIDE.md`** | Comprehensive GUI documentation |
| **`docs/API_REFERENCE.md`** | Function and API documentation |
| **`docs/DATA_FLOW_DIAGRAM.md`** | Architecture and data flow diagrams |
| **`STEP1_SUMMARY.md`** | Step 1 implementation report |
| **`STEP2_SUMMARY.md`** | Step 2 implementation report |
| **`STEP3_SUMMARY.md`** | Step 3 implementation report |
| **`STEP4_SUMMARY.md`** | Step 4 implementation report |
| **`STEP5_SUMMARY.md`** | Step 5 implementation report |

### 📂 Output Directories

| **Directory** | **Contains** |
|--------------|-------------|
| **`outputs/`** | Generated charts (PNG files), exported CSV files, analysis results |
| **`logs/`** | Activity logs: `dashboard_activity.log`, `gui_activity.log` |

---

## 🎓 Learning Path

**New to the project?** Follow this path:

1. **Start here:** Run `python src/gui_dashboard.py` - explore the interface
2. **Load sample data:** Click "Load Sample Vaccination Data"
3. **Try features:** Filter, analyze, visualize - get comfortable
4. **Learn Step 1:** Run `python src/data_loader.py` - see data loading
5. **Learn Step 2:** Run `python src/cleaning_demo.py` - see data cleaning
6. **Learn Step 3:** Run `python src/analysis_demo.py` - see analysis
7. **Try CLI:** Run `python src/dashboard.py` - command-line interface
8. **Run tests:** Run `pytest tests/ -v` - see comprehensive testing
9. **Read code:** Check `src/*.py` files to understand implementation
10. **Build something:** Use the core functions in your own scripts!

---

## License

This project is for educational purposes as part of a university coursework assignment.

## Authors

- Developed following TDD and software engineering best practices
- Version control with Git

## Implementation Progress

- ✅ **Step 1**: Data Access & Loading - **COMPLETE** (21 tests)
- ✅ **Step 2**: Data Cleaning & Structuring - **COMPLETE** (28 tests)
- ✅ **Step 3**: Filtering and Summary Views - **COMPLETE** (29 tests)
- ✅ **Step 4**: Presentation Layer (CLI) - **COMPLETE**
- ✅ **Step 5**: Extension Features - **COMPLETE** (51 tests: 27 CRUD + 24 Logging)
