# Data Flow Diagram - Step 1: Data Access & Loading

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Public Health Data Dashboard                         │
│                         Step 1: Data Loading                             │
└─────────────────────────────────────────────────────────────────────────┘

                           DATA SOURCES
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │   CSV Files  │    │  JSON Files  │    │  Public APIs │
    │              │    │              │    │              │
    │  Vaccination │    │   Disease    │    │  WHO, CDC,   │
    │     Data     │    │  Outbreaks   │    │   UK Gov     │
    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
           │                   │                    │
           └───────────────────┼────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   LOADING LAYER     │
                    │  (src/main.py)      │
                    │                     │
                    │  • load_dataset()   │
                    │  • load_json_ds()   │
                    │  • load_from_api()  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  pandas DataFrame   │
                    │                     │
                    │  • Structured data  │
                    │  • Type inference   │
                    │  • Data validation  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  DATABASE LAYER     │
                    │                     │
                    │  • load_to_db()     │
                    │  • read_from_db()   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  SQLite Database    │
                    │  (health_data.db)   │
                    │                     │
                    │  Tables:            │
                    │  • vaccinations     │
                    │  • outbreaks        │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   QUERY LAYER       │
                    │                     │
                    │  • SQL queries      │
                    │  • Filtering        │
                    │  • Aggregation      │
                    └─────────────────────┘
                               │
                               ▼
                      [Ready for Step 2]
                    (Cleaning & Filtering)
```

---

## Detailed Component Flow

### 1. CSV Loading Flow

```
┌─────────────────────────────────────────────────────────────┐
│  CSV File (sample_vaccination_data.csv)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ country,year,month,vaccine_type,doses_administered... │  │
│  │ United Kingdom,2020,12,COVID-19,1000000,...          │  │
│  │ United States,2021,1,COVID-19,12000000,...           │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  load_dataset(path)  │
                 │                      │
                 │  1. Check file exists│
                 │  2. Read with pandas │
                 │  3. Infer types      │
                 │  4. Return DataFrame │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌─────────────────────────┐
                 │   pandas DataFrame      │
                 │   ┌─────────┬──────┬───┐│
                 │   │ country │ year │...││
                 │   ├─────────┼──────┼───┤│
                 │   │   UK    │ 2020 │...││
                 │   │   USA   │ 2021 │...││
                 │   └─────────┴──────┴───┘│
                 └──────────┬──────────────┘
                            │
                            ▼
              ┌───────────────────────────────┐
              │ load_to_database(df, path,    │
              │                  table_name)  │
              │                               │
              │  1. Validate DataFrame        │
              │  2. Create SQLAlchemy engine  │
              │  3. Write to SQLite           │
              │  4. Return engine             │
              └───────────────┬───────────────┘
                              │
                              ▼
                 ┌───────────────────────────┐
                 │  SQLite Database          │
                 │  ┌─────────────────────┐  │
                 │  │ Table: vaccinations │  │
                 │  │ 20 rows x 7 columns │  │
                 │  └─────────────────────┘  │
                 └───────────────────────────┘
```

### 2. JSON Loading Flow

```
┌──────────────────────────────────────────────────┐
│  JSON File (sample_disease_outbreak.json)       │
│  ┌────────────────────────────────────────────┐  │
│  │ [                                          │  │
│  │   {                                        │  │
│  │     "country": "United Kingdom",           │  │
│  │     "disease": "Influenza",                │  │
│  │     "year": 2020,                          │  │
│  │     "confirmed_cases": 45000,              │  │
│  │     ...                                    │  │
│  │   },                                       │  │
│  │   ...                                      │  │
│  │ ]                                          │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────┬────────────────────────────┘
                      │
                      ▼
           ┌────────────────────────┐
           │ load_json_dataset(path)│
           │                        │
           │  1. Check file exists  │
           │  2. Parse JSON         │
           │  3. Convert to DF      │
           │  4. Return DataFrame   │
           └───────────┬────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │   pandas DataFrame       │
           │   ┌────────┬─────────┬──┐│
           │   │country │ disease │..││
           │   ├────────┼─────────┼──┤│
           │   │   UK   │Influenza│..││
           │   │   USA  │Influenza│..││
           │   └────────┴─────────┴──┘│
           └──────────┬───────────────┘
                      │
                      ▼
           [Store in database: outbreaks table]
```

### 3. API Loading Flow

```
┌─────────────────────────────────────────────────────────┐
│               Public Health API                         │
│  https://api.example.com/health-data?country=UK&year=2021│
└──────────────────────────┬──────────────────────────────┘
                           │
                           │ HTTP GET Request
                           ▼
                ┌─────────────────────────┐
                │  load_from_api(url,     │
                │         params, key)    │
                │                         │
                │  1. Make HTTP request   │
                │  2. Check status        │
                │  3. Parse JSON response │
                │  4. Extract data        │
                │  5. Convert to DF       │
                │  6. Return DataFrame    │
                └───────────┬─────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  JSON Response      │
                 │  {                  │
                 │    "status": "ok",  │
                 │    "data": [        │
                 │      {...},         │
                 │      {...}          │
                 │    ]                │
                 │  }                  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Extract "data" key  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   pandas DataFrame   │
                 └──────────────────────┘
```

### 4. Database Query Flow

```
┌─────────────────────────────────────────────────────────┐
│                 Application Request                     │
│  "Show me UK vaccination data from 2021"                │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
                ┌──────────────────────────┐
                │  read_from_database(     │
                │      db_path,            │
                │      table_name,         │
                │      query)              │
                │                          │
                │  1. Check DB exists      │
                │  2. Check table exists   │
                │  3. Execute SQL query    │
                │  4. Return DataFrame     │
                └───────────┬──────────────┘
                            │
                            ▼
                 ┌─────────────────────────────────────┐
                 │  SQL Query                          │
                 │  SELECT * FROM vaccinations         │
                 │  WHERE country = 'United Kingdom'   │
                 │    AND year = 2021                  │
                 └──────────────┬──────────────────────┘
                                │
                                ▼
                 ┌────────────────────────────────────┐
                 │  SQLite Database                   │
                 │  ┌──────────────────────────────┐  │
                 │  │ Execute query on table       │  │
                 │  │ vaccinations                 │  │
                 │  └──────────────────────────────┘  │
                 └─────────────┬──────────────────────┘
                               │
                               ▼
                 ┌────────────────────────────────────┐
                 │  Result Set                        │
                 │  ┌──────────┬──────┬────┬────────┐ │
                 │  │  country │ year │... │ doses  │ │
                 │  ├──────────┼──────┼────┼────────┤ │
                 │  │    UK    │ 2021 │... │3500000 │ │
                 │  │    UK    │ 2021 │... │7000000 │ │
                 │  │    UK    │ 2021 │... │12000000│ │
                 │  └──────────┴──────┴────┴────────┘ │
                 └─────────────┬──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Return DataFrame to │
                    │     Application      │
                    └──────────────────────┘
```

---

## Error Handling Flow

```
┌──────────────────┐
│  User Request    │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────┐
│  Try to load data       │
└────────┬────────────────┘
         │
         ▼
    ┌────────┐
    │ Success?│
    └────┬───┘
         │
    ┌────┼────┐
    │ Yes     │ No
    │         │
    ▼         ▼
┌───────┐  ┌─────────────────────┐
│Return │  │  Error Type?        │
│DF     │  └──────┬──────────────┘
└───────┘         │
            ┌─────┼─────┬────────┬────────┐
            │           │        │        │
            ▼           ▼        ▼        ▼
    ┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐
    │FileNotFnd│ │ValueError│ │Network │ │Other   │
    │          │ │          │ │Error   │ │        │
    └─────┬────┘ └────┬─────┘ └───┬────┘ └───┬────┘
          │           │           │           │
          └───────────┴───────────┴───────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Raise exception│
              │ with meaningful│
              │ error message  │
              └───────┬────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Log error      │
              │ Return to user │
              └────────────────┘
```

---

## Data Transformation Pipeline

```
RAW DATA → VALIDATION → LOADING → STORAGE → RETRIEVAL

   CSV        Check        Read        Store      Query
   JSON    ──► exists  ──► with    ──► in     ──► from
   API         Format      pandas      SQLite     DB
               Valid       Convert     Tables     Filter
                          to DF                  Aggregate
```

---

## Class Relationships

```
┌────────────────────────────────────────────────────┐
│                   DataLoader                       │
│  ┌──────────────────────────────────────────────┐ │
│  │  - db_path: Path                             │ │
│  │                                              │ │
│  │  + load_vaccination_data()                   │ │
│  │  + load_outbreak_data()                      │ │
│  │  + get_data_from_db()                        │ │
│  │  + display_summary()                         │ │
│  └──────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────┘
                 │ uses
                 ▼
┌────────────────────────────────────────────────────┐
│                   main.py                          │
│  ┌──────────────────────────────────────────────┐ │
│  │  Functions:                                  │ │
│  │                                              │ │
│  │  + load_dataset(path)                        │ │
│  │  + load_json_dataset(path)                   │ │
│  │  + load_from_api(url, params, key)           │ │
│  │  + load_to_database(df, path, table)         │ │
│  │  + read_from_database(path, table, query)    │ │
│  └──────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────┘
                 │ uses
        ┌────────┼────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────┐
│    pandas    │  │  SQLAlchemy  │
│  DataFrame   │  │    Engine    │
└──────────────┘  └──────────────┘
```

---

## Test Coverage Map

```
┌─────────────────────────────────────────────────┐
│              test_main.py (21 tests)            │
├─────────────────────────────────────────────────┤
│                                                 │
│  CSV Tests (4)           JSON Tests (4)        │
│  ├─ Normal load          ├─ Normal load        │
│  ├─ Missing file         ├─ Missing file       │
│  ├─ Empty CSV            ├─ Invalid JSON       │
│  └─ Type handling        └─ Empty array        │
│                                                 │
│  API Tests (5)           Database Tests (8)    │
│  ├─ Success              ├─ Write success      │
│  ├─ Nested data          ├─ Read success       │
│  ├─ With params          ├─ SQL query          │
│  ├─ Error handling       ├─ Empty DF error     │
│  └─ Dict response        ├─ Invalid table      │
│                          ├─ Missing DB          │
│                          ├─ Missing table       │
│                          └─ Append mode         │
└─────────────────────────────────────────────────┘
```

---

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────────┐
│                    PRODUCTION (Future)                  │
│                                                         │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Web UI    │───▶│  Flask API   │───▶│PostgreSQL │ │
│  │  (React)    │    │  (REST)      │    │           │ │
│  └─────────────┘    └──────────────┘    └───────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘

                         Current:
                     Local SQLite DB
                    Command Line Only
```

---

**Document Version**: 1.0  
**Last Updated**: November 17, 2025  
**Related**: STEP1_SUMMARY.md, API_REFERENCE.md

