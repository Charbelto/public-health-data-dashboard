# API Reference - Data Loading Functions

Quick reference guide for all data loading functions in the Public Health Data Insights Dashboard.

---

## CSV Loading

### `load_dataset(path)`

Load a CSV file into a pandas DataFrame.

**Parameters:**
- `path` (str | Path): Path to the CSV file

**Returns:**
- `pd.DataFrame`: Loaded data

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file cannot be parsed as CSV

**Example:**
```python
from src.main import load_dataset

df = load_dataset("data/sample_vaccination_data.csv")
print(f"Loaded {len(df)} records")
```

---

## JSON Loading

### `load_json_dataset(path)`

Load a JSON file into a pandas DataFrame.

**Parameters:**
- `path` (str | Path): Path to the JSON file

**Returns:**
- `pd.DataFrame`: Loaded data

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file cannot be parsed as JSON

**Example:**
```python
from src.main import load_json_dataset

df = load_json_dataset("data/sample_disease_outbreak.json")
print(df.head())
```

---

## API Loading

### `load_from_api(url, params=None, data_key=None)`

Load data from a public API endpoint.

**Parameters:**
- `url` (str): API endpoint URL
- `params` (dict, optional): Query parameters for the API request
- `data_key` (str, optional): Key to extract nested data from JSON response

**Returns:**
- `pd.DataFrame`: Loaded data

**Raises:**
- `requests.RequestException`: If the API request fails
- `ValueError`: If response cannot be converted to DataFrame

**Example 1: Simple API call**
```python
from src.main import load_from_api

df = load_from_api("https://api.example.com/health-data")
```

**Example 2: With query parameters**
```python
df = load_from_api(
    "https://api.example.com/health-data",
    params={"country": "UK", "year": 2021}
)
```

**Example 3: Nested JSON data**
```python
# API returns: {"status": "ok", "data": [{"country": "UK", ...}]}
df = load_from_api(
    "https://api.example.com/health-data",
    data_key="data"
)
```

---

## Database Operations

### `load_to_database(df, db_path, table_name, if_exists='replace')`

Load a DataFrame into a SQLite database.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to load
- `db_path` (str | Path): Path to the SQLite database file
- `table_name` (str): Name of the table to create/update
- `if_exists` (str): How to behave if table exists:
  - `'replace'`: Drop and recreate table (default)
  - `'append'`: Add rows to existing table
  - `'fail'`: Raise error if table exists

**Returns:**
- `sqlalchemy.engine.Engine`: Database engine for further operations

**Raises:**
- `ValueError`: If DataFrame is empty or table_name is invalid

**Example 1: Create new table**
```python
from src.main import load_dataset, load_to_database

df = load_dataset("data/sample_vaccination_data.csv")
engine = load_to_database(df, "data/my_data.db", "vaccinations")
```

**Example 2: Append to existing table**
```python
new_df = load_dataset("data/new_vaccinations.csv")
load_to_database(new_df, "data/my_data.db", "vaccinations", if_exists="append")
```

---

### `read_from_database(db_path, table_name, query=None)`

Read data from a SQLite database table.

**Parameters:**
- `db_path` (str | Path): Path to the SQLite database file
- `table_name` (str): Name of the table to read from
- `query` (str, optional): SQL query to execute. If None, reads entire table

**Returns:**
- `pd.DataFrame`: Queried data

**Raises:**
- `FileNotFoundError`: If database doesn't exist
- `ValueError`: If table doesn't exist or query is invalid

**Example 1: Read entire table**
```python
from src.main import read_from_database

df = read_from_database("data/health_data.db", "vaccinations")
```

**Example 2: SQL query**
```python
query = """
    SELECT country, SUM(doses_administered) as total_doses
    FROM vaccinations
    WHERE year = 2021
    GROUP BY country
    ORDER BY total_doses DESC
"""
df = read_from_database("data/health_data.db", "vaccinations", query=query)
```

**Example 3: Filter by condition**
```python
query = "SELECT * FROM vaccinations WHERE country = 'United Kingdom' AND year >= 2021"
uk_data = read_from_database("data/health_data.db", "vaccinations", query=query)
```

---

## DataLoader Class

### `DataLoader(db_path=None)`

High-level interface for loading and managing health data.

**Parameters:**
- `db_path` (Path, optional): Path to database. Defaults to `data/health_data.db`

**Methods:**

#### `load_vaccination_data(csv_path=None)`
Load vaccination data from CSV and store in database.

**Returns:** `pd.DataFrame`

#### `load_outbreak_data(json_path=None)`
Load outbreak data from JSON and store in database.

**Returns:** `pd.DataFrame`

#### `get_data_from_db(table_name, query=None)`
Retrieve data from database.

**Returns:** `pd.DataFrame`

#### `display_summary()`
Display summary of all data in the database.

**Example: Using DataLoader**
```python
from src.data_loader import DataLoader

# Initialize
loader = DataLoader()

# Load data
vaccination_df = loader.load_vaccination_data()
outbreak_df = loader.load_outbreak_data()

# Query data
uk_vaccinations = loader.get_data_from_db(
    "vaccinations",
    query="SELECT * FROM vaccinations WHERE country = 'United Kingdom'"
)

# Display summary
loader.display_summary()
```

---

## Common Patterns

### Pattern 1: Load CSV to Database
```python
from src.main import load_dataset, load_to_database

df = load_dataset("my_data.csv")
load_to_database(df, "my_database.db", "my_table")
```

### Pattern 2: Query and Export
```python
from src.main import read_from_database

df = read_from_database("my_database.db", "my_table", 
                       query="SELECT * FROM my_table WHERE year >= 2020")
df.to_csv("filtered_data.csv", index=False)
```

### Pattern 3: Combine Multiple Sources
```python
from src.main import load_dataset, load_json_dataset, load_to_database
import pandas as pd

# Load from different sources
csv_data = load_dataset("vaccinations.csv")
json_data = load_json_dataset("outbreaks.json")

# Combine if schemas match
combined = pd.concat([csv_data, json_data], ignore_index=True)

# Store in database
load_to_database(combined, "health_data.db", "combined_data")
```

### Pattern 4: Incremental Updates
```python
from src.main import load_dataset, load_to_database, read_from_database

# Load new data
new_data = load_dataset("new_records.csv")

# Append to existing table
load_to_database(new_data, "health_data.db", "vaccinations", if_exists="append")

# Verify
total_records = read_from_database("health_data.db", "vaccinations")
print(f"Total records now: {len(total_records)}")
```

---

## Error Handling

All functions raise meaningful exceptions that should be caught and handled:

```python
from src.main import load_dataset, load_to_database
import logging

try:
    df = load_dataset("data.csv")
    load_to_database(df, "db.db", "table")
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
except ValueError as e:
    logging.error(f"Invalid data: {e}")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
```

---

## Performance Tips

1. **Large CSV files**: Use pandas chunking
```python
import pandas as pd
from src.main import load_to_database

for chunk in pd.read_csv("large_file.csv", chunksize=10000):
    load_to_database(chunk, "db.db", "large_table", if_exists="append")
```

2. **Database queries**: Use indexes for faster queries
```python
from sqlalchemy import create_engine

engine = create_engine('sqlite:///health_data.db')
with engine.connect() as conn:
    conn.execute("CREATE INDEX idx_country ON vaccinations(country)")
    conn.execute("CREATE INDEX idx_year ON vaccinations(year)")
```

3. **API calls**: Implement caching for repeated requests
```python
from functools import lru_cache
from src.main import load_from_api

@lru_cache(maxsize=100)
def cached_api_call(url, params_tuple):
    params = dict(params_tuple)  # Convert tuple back to dict
    return load_from_api(url, params)
```

---

**Last Updated**: November 17, 2025  
**Version**: 1.0.0 (Step 1 Complete)

