# Public Health Data Insights Dashboard

This project is a command-line Python tool to explore public health datasets
(e.g. vaccination rates, disease outbreaks, or mental health reports).

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

### 🔄 Planned Features

- Command-line interface (CLI) for user interaction
- Data visualizations with Matplotlib
- CRUD operations on database
- Export filtered data as CSV
- Activity logging

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
│   └── cleaning_demo.py                 # Cleaning demonstration script
├── tests/                               # Test suite (TDD approach)
│   ├── test_main.py                     # 21 data loading tests
│   └── test_cleaning.py                 # 28 data cleaning tests
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

### Running the Demonstrations

**Step 1: Data Loading Demo**

To see all data loading functionality in action:

```bash
# On Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/data_loader.py

# On Linux/Mac:
export PYTHONPATH=$PWD && python src/data_loader.py
```

This will:
1. Load vaccination data from CSV
2. Load outbreak data from JSON
3. Store both datasets in SQLite database
4. Query and display data from the database
5. Show a summary of all loaded data

**Step 2: Data Cleaning Demo**

To see all data cleaning functionality in action:

```bash
# On Windows PowerShell:
$env:PYTHONPATH="$PWD"; python src/cleaning_demo.py

# On Linux/Mac:
export PYTHONPATH=$PWD && python src/cleaning_demo.py
```

This will:
1. Demonstrate missing value detection and handling
2. Show duplicate detection and removal
3. Perform type conversions (datetime, numeric)
4. Validate data ranges and detect outliers
5. Standardize text data
6. Show chained cleaning operations with DataCleaner class
7. Generate cleaning reports
8. Save cleaned data to database

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
- **Total**: 78 tests, all passing ✅

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

## License

This project is for educational purposes as part of a university coursework assignment.

## Authors

- Developed following TDD and software engineering best practices
- Version control with Git

## Implementation Progress

- ✅ **Step 1**: Data Access & Loading - **COMPLETE** (21 tests)
- ✅ **Step 2**: Data Cleaning & Structuring - **COMPLETE** (28 tests)
- ✅ **Step 3**: Filtering and Summary Views - **COMPLETE** (29 tests)
- ⏳ **Step 4**: Presentation Layer (CLI)
- ⏳ **Step 5**: Extension Features (CRUD, Export, Logging)
