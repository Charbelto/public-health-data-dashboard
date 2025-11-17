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

### 🔄 Planned Features

- Data cleaning and structuring (handle missing values, type conversions)
- Filtering by user-selected criteria (country, date range, age group)
- Summary statistics (mean, min, max, counts, trends)
- Command-line interface (CLI) for user interaction
- Data visualizations with Matplotlib
- CRUD operations on database
- Export filtered data as CSV
- Activity logging

## Project Structure

```
public-health-data-dashboard/
├── data/                           # Data directory
│   ├── sample_vaccination_data.csv # Sample vaccination dataset
│   ├── sample_disease_outbreak.json# Sample outbreak dataset
│   └── health_data.db             # SQLite database (generated)
├── src/                           # Source code
│   ├── main.py                    # Core data loading functions
│   └── data_loader.py             # DataLoader class and demonstration
├── tests/                         # Test suite (TDD approach)
│   └── test_main.py               # 21 comprehensive tests
├── requirements.txt               # Python dependencies
└── README.md                      # This file
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

## Usage

### Running the Demonstration

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

### Running Tests

Run the comprehensive test suite (21 tests covering all functionality):

```bash
pytest tests/test_main.py -v
```

For test coverage report:

```bash
pytest tests/test_main.py -v --cov=src --cov-report=html
```

### Using the Data Loading Functions

Here's a quick example of how to use the core functions:

```python
from pathlib import Path
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

## Development Approach

### Test-Driven Development (TDD)

This project follows TDD principles:

1. ✅ **Write tests first** - Tests were written before implementation
2. ✅ **Red-Green-Refactor** - Tests fail initially, then implementation makes them pass
3. ✅ **Comprehensive coverage** - 21 tests covering normal cases, edge cases, and error handling
4. ✅ **Automated testing** - All tests can be run with a single pytest command

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

## Next Steps

- **Step 2**: Data Cleaning & Structuring
- **Step 3**: Filtering and Summary Views
- **Step 4**: Presentation Layer (CLI)
- **Step 5**: Extension Features (CRUD, Export, Logging)
