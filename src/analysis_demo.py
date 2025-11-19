"""
Data Filtering and Analysis Demonstration Script - Step 3

This script demonstrates all filtering and analysis capabilities:
- Filtering by column values, date ranges, numeric ranges
- Summary statistics (mean, min, max, count, std)
- Grouping and aggregation
- Trend analysis over time
- Growth rates and moving averages
- Chained operations with DataAnalyzer class
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

from src.main import load_dataset, load_json_dataset
from src.cleaning import DataCleaner
from src.analysis import (
    filter_by_column,
    filter_by_date_range,
    filter_by_numeric_range,
    filter_by_multiple_criteria,
    calculate_summary_stats,
    get_column_statistics,
    group_and_aggregate,
    calculate_trends,
    calculate_growth_rate,
    calculate_moving_average,
    DataAnalyzer
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def demonstrate_basic_filtering():
    """Demonstrate basic filtering operations."""
    print_section("1. BASIC FILTERING OPERATIONS")
    
    # Load vaccination data
    df = load_dataset("data/sample_vaccination_data.csv")
    print(f"Original dataset: {len(df)} records\n")
    
    # Filter by country
    print("a) Filter by single country (UK):")
    uk_data = filter_by_column(df, 'country', 'United Kingdom')
    print(f"   UK records: {len(uk_data)}")
    print(f"   Months: {sorted(uk_data['month'].unique())}\n")
    
    # Filter by multiple countries
    print("b) Filter by multiple countries (UK, USA):")
    multi_country = filter_by_column(df, 'country', ['United Kingdom', 'United States'])
    print(f"   Records: {len(multi_country)}")
    print(f"   Countries: {sorted(multi_country['country'].unique())}\n")
    
    # Filter by numeric range
    print("c) Filter by vaccination rate (>= 0.05):")
    high_rate = filter_by_numeric_range(df, 'vaccination_rate', min_value=0.05)
    print(f"   High vaccination rate records: {len(high_rate)}")
    print(f"   Rate range: {high_rate['vaccination_rate'].min():.4f} - {high_rate['vaccination_rate'].max():.4f}")
    
    return df


def demonstrate_date_filtering():
    """Demonstrate date range filtering."""
    print_section("2. DATE RANGE FILTERING")
    
    # Load and convert dates
    df = load_dataset("data/sample_vaccination_data.csv")
    
    # Create a date column (year-month)
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-01')
    
    print(f"Date range: {df['date'].min()} to {df['date'].max()}\n")
    
    # Filter by date range
    print("a) Filter for year 2021:")
    year_2021 = filter_by_date_range(
        df, 'date',
        start_date=datetime(2021, 1, 1),
        end_date=datetime(2021, 12, 31)
    )
    print(f"   2021 records: {len(year_2021)}")
    print(f"   Countries with data: {len(year_2021['country'].unique())}\n")
    
    # Filter from specific date
    print("b) Filter from February 2021 onwards:")
    from_feb = filter_by_date_range(df, 'date', start_date=datetime(2021, 2, 1))
    print(f"   Records from Feb 2021: {len(from_feb)}")
    
    return df


def demonstrate_multiple_criteria():
    """Demonstrate filtering with multiple criteria."""
    print_section("3. MULTIPLE CRITERIA FILTERING")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    print("Filtering for: UK or USA, year 2021, vaccination rate >= 0.05\n")
    
    criteria = {
        'country': ['United Kingdom', 'United States'],
        'year': 2021
    }
    
    filtered = filter_by_multiple_criteria(df, criteria)
    filtered = filter_by_numeric_range(filtered, 'vaccination_rate', min_value=0.05)
    
    print(f"Matching records: {len(filtered)}")
    print("\nFiltered data:")
    print(filtered[['country', 'year', 'month', 'vaccination_rate']].to_string(index=False))
    
    return filtered


def demonstrate_summary_statistics():
    """Demonstrate summary statistics calculation."""
    print_section("4. SUMMARY STATISTICS")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    print("a) Summary for 'doses_administered' column:\n")
    stats = calculate_summary_stats(df, 'doses_administered')
    
    for key, value in stats.items():
        print(f"   {key:12s}: {value:,.0f}")
    
    print("\nb) Statistics for all numeric columns:\n")
    all_stats = get_column_statistics(df)
    
    print(f"   Analyzed {len(all_stats)} numeric columns:")
    for col in all_stats.keys():
        print(f"   - {col}: mean = {all_stats[col]['mean']:,.0f}, "
              f"min = {all_stats[col]['min']:,.0f}, "
              f"max = {all_stats[col]['max']:,.0f}")
    
    return df


def demonstrate_grouping():
    """Demonstrate grouping and aggregation."""
    print_section("5. GROUPING AND AGGREGATION")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    print("a) Total doses by country:\n")
    by_country = group_and_aggregate(
        df,
        group_by='country',
        agg_column='doses_administered',
        agg_func='sum',
        sort_by='doses_administered',
        ascending=False
    )
    
    print(by_country.to_string())
    
    print("\n\nb) Average vaccination rate by country and year:\n")
    by_country_year = group_and_aggregate(
        df,
        group_by=['country', 'year'],
        agg_column='vaccination_rate',
        agg_func='mean'
    )
    
    print(by_country_year.head(10).to_string())
    
    return by_country


def demonstrate_trend_analysis():
    """Demonstrate trend analysis over time."""
    print_section("6. TREND ANALYSIS")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    # Analyze UK vaccination trends
    uk_data = filter_by_column(df, 'country', 'United Kingdom')
    uk_data = uk_data.sort_values(['year', 'month'])
    
    print("UK Vaccination Trend Analysis:\n")
    
    # Calculate trends
    uk_data['date'] = pd.to_datetime(
        uk_data['year'].astype(str) + '-' + uk_data['month'].astype(str).str.zfill(2) + '-01'
    )
    trends = calculate_trends(uk_data, 'date', 'doses_administered')
    
    for key, value in trends.items():
        if isinstance(value, float):
            print(f"   {key:20s}: {value:,.2f}")
        else:
            print(f"   {key:20s}: {value}")
    
    print("\n\nWith growth rate:")
    uk_with_growth = calculate_growth_rate(uk_data, 'doses_administered')
    print(uk_with_growth[['year', 'month', 'doses_administered', 'growth_rate']].to_string(index=False))
    
    return uk_with_growth


def demonstrate_moving_average():
    """Demonstrate moving average calculation."""
    print_section("7. MOVING AVERAGES")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    # Focus on USA data
    usa_data = filter_by_column(df, 'country', 'United States')
    usa_data = usa_data.sort_values(['year', 'month']).reset_index(drop=True)
    
    print("USA vaccination doses with 3-month moving average:\n")
    
    usa_with_ma = calculate_moving_average(usa_data, 'doses_administered', window=3)
    
    print(usa_with_ma[['year', 'month', 'doses_administered', 'doses_administered_ma_3']].to_string(index=False))
    
    return usa_with_ma


def demonstrate_data_analyzer():
    """Demonstrate DataAnalyzer class with chained operations."""
    print_section("8. DATA ANALYZER CLASS - CHAINED OPERATIONS")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    print("Original dataset:")
    print(f"   Total records: {len(df)}")
    print(f"   Countries: {len(df['country'].unique())}")
    print(f"   Years: {sorted(df['year'].unique())}\n")
    
    print("Applying chained analysis:")
    print("1. Filter for year 2021")
    print("2. Filter for vaccination rate >= 0.05")
    print("3. Calculate summary statistics")
    print()
    
    analyzer = DataAnalyzer(df)
    
    # Chain filtering operations
    filtered_analyzer = (analyzer
                        .filter_by('year', 2021)
                        .filter_numeric_range('vaccination_rate', min_value=0.05))
    
    # Get summary
    summary = filtered_analyzer.summarize('doses_administered')
    
    print("Summary statistics for filtered data:")
    for key, value in summary.items():
        print(f"   {key:12s}: {value:,.2f}")
    
    # Get analysis report
    print("\n\nComprehensive analysis report:")
    report = filtered_analyzer.get_analysis_report()
    
    print(f"   Original records: {report['original_records']}")
    print(f"   Filtered records: {report['total_records']}")
    print(f"   Records removed: {report['records_filtered']}")
    print(f"   Numeric columns: {len(report['numeric_columns'])}")
    print(f"   Operations: {len(report['operations'])}")
    
    for i, op in enumerate(report['operations'], 1):
        print(f"      {i}. {op}")
    
    return filtered_analyzer


def demonstrate_grouped_analysis():
    """Demonstrate grouped analysis with DataAnalyzer."""
    print_section("9. GROUPED ANALYSIS WITH DATA ANALYZER")
    
    df = load_dataset("data/sample_vaccination_data.csv")
    
    print("Total vaccination doses by country (using DataAnalyzer):\n")
    
    analyzer = DataAnalyzer(df)
    result = analyzer.group_by('country').aggregate('doses_administered', 'sum')
    
    print(result.to_string())
    
    print("\n\nMultiple aggregations:")
    result_multi = analyzer.group_by('country').aggregate('doses_administered', ['sum', 'mean', 'count'])
    print(result_multi.to_string())
    
    return result


def demonstrate_comprehensive_workflow():
    """Demonstrate a comprehensive analysis workflow."""
    print_section("10. COMPREHENSIVE ANALYSIS WORKFLOW")
    
    print("Scenario: Analyze UK vaccination progress in 2021\n")
    
    # Load data
    df = load_dataset("data/sample_vaccination_data.csv")
    
    # Create analyzer
    analyzer = DataAnalyzer(df)
    
    # Step 1: Filter for UK, year 2021
    print("Step 1: Filter for UK, year 2021")
    uk_2021 = (analyzer
               .filter_by('country', 'United Kingdom')
               .filter_by('year', 2021)
               .get_data())
    print(f"   Records found: {len(uk_2021)}\n")
    
    # Step 2: Calculate summary statistics
    print("Step 2: Summary statistics")
    uk_analyzer = DataAnalyzer(uk_2021)
    summary = uk_analyzer.summarize('doses_administered')
    print(f"   Mean doses: {summary['mean']:,.0f}")
    print(f"   Total doses: {summary['sum']:,.0f}")
    print(f"   Max in single month: {summary['max']:,.0f}\n")
    
    # Step 3: Add trend analysis
    print("Step 3: Trend analysis")
    uk_2021_sorted = uk_2021.sort_values('month')
    uk_2021_sorted['date'] = pd.to_datetime(
        uk_2021_sorted['year'].astype(str) + '-' + uk_2021_sorted['month'].astype(str).str.zfill(2) + '-01'
    )
    
    trends = calculate_trends(uk_2021_sorted, 'date', 'doses_administered')
    print(f"   Total change: {trends['total_change']:,.0f}")
    print(f"   Percent change: {trends['percent_change']:.1f}%")
    print(f"   Average monthly change: {trends['average_change']:,.0f}\n")
    
    # Step 4: Calculate growth rates
    print("Step 4: Month-over-month growth rates")
    uk_with_growth = calculate_growth_rate(uk_2021_sorted, 'doses_administered')
    print(uk_with_growth[['month', 'doses_administered', 'growth_rate']].to_string(index=False))
    
    return uk_with_growth


def main():
    """Run all analysis demonstrations."""
    print("\n" + "="*70)
    print(" PUBLIC HEALTH DATA DASHBOARD - FILTERING & ANALYSIS DEMONSTRATION")
    print(" Step 3: Filtering and Summary Views")
    print("="*70)
    
    # Run all demonstrations
    demonstrate_basic_filtering()
    demonstrate_date_filtering()
    demonstrate_multiple_criteria()
    demonstrate_summary_statistics()
    demonstrate_grouping()
    demonstrate_trend_analysis()
    demonstrate_moving_average()
    demonstrate_data_analyzer()
    demonstrate_grouped_analysis()
    demonstrate_comprehensive_workflow()
    
    # Final summary
    print_section("SUMMARY")
    print("[SUCCESS] Data filtering and analysis demonstration completed!")
    print("\nCapabilities demonstrated:")
    print("  1. [OK] Filter by column values (single and multiple)")
    print("  2. [OK] Filter by date ranges")
    print("  3. [OK] Filter by numeric ranges")
    print("  4. [OK] Multiple criteria filtering")
    print("  5. [OK] Summary statistics (mean, min, max, count, std)")
    print("  6. [OK] Grouping and aggregation")
    print("  7. [OK] Trend analysis over time")
    print("  8. [OK] Growth rate calculations")
    print("  9. [OK] Moving averages")
    print("  10. [OK] Chained operations with DataAnalyzer class")
    print("\nReady for Step 4: Presentation Layer (CLI)")
    print()


if __name__ == "__main__":
    main()
