"""
CLI Demonstration Script - Step 4

This script demonstrates all presentation layer capabilities programmatically:
- Table formatting and display
- Summary statistics presentation
- Grouped data views
- Chart creation (bar, line, comparison)
- Data export
- Complete workflow examples
"""

from pathlib import Path
import pandas as pd

from src.cli import (
    HealthDataCLI,
    format_table,
    format_summary_stats,
    create_bar_chart,
    create_line_chart,
    create_comparison_chart,
    save_chart
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def demonstrate_table_formatting():
    """Demonstrate table formatting."""
    print_section("1. TABLE FORMATTING")
    
    # Load sample data
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    print("First 5 records:")
    cli.show_data(max_rows=5)


def demonstrate_summary_statistics():
    """Demonstrate summary statistics display."""
    print_section("2. SUMMARY STATISTICS")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    print("Summary for 'doses_administered' column:\n")
    cli.show_summary('doses_administered')


def demonstrate_grouped_data():
    """Demonstrate grouped data views."""
    print_section("3. GROUPED DATA VIEWS")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    print("Total doses by country:\n")
    cli.show_grouped_data('country', 'doses_administered', 'sum')
    
    print("\n\nAverage vaccination rate by country:\n")
    cli.show_grouped_data('country', 'vaccination_rate', 'mean')


def demonstrate_bar_charts():
    """Demonstrate bar chart creation."""
    print_section("4. BAR CHARTS")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    # Create grouped data
    from src.analysis import group_and_aggregate
    grouped = group_and_aggregate(
        cli.df,
        group_by='country',
        agg_column='doses_administered',
        agg_func='sum',
        sort_by='doses_administered',
        ascending=False
    )
    
    # Reset index for plotting
    plot_df = grouped.reset_index()
    
    print("Creating bar chart: Total doses by country")
    
    # Create and save chart
    output_path = Path("outputs") / "bar_chart_demo.png"
    cli.create_visualization(
        chart_type='bar',
        x='country',
        y='doses_administered',
        title='Total Vaccination Doses by Country',
        output_path=output_path,
        sort_by='doses_administered',
        ascending=False
    )
    
    print(f"Chart saved to: {output_path}")


def demonstrate_line_charts():
    """Demonstrate line chart creation."""
    print_section("5. LINE CHARTS")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    # Filter for UK data and create trend
    cli.apply_filter('country', 'United Kingdom')
    
    # Sort by month
    cli.df = cli.df.sort_values('month')
    
    print("Creating line chart: UK vaccination trend\n")
    
    output_path = Path("outputs") / "line_chart_demo.png"
    cli.create_visualization(
        chart_type='line',
        x='month',
        y='doses_administered',
        title='UK Vaccination Doses Over Time',
        output_path=output_path
    )
    
    print(f"Chart saved to: {output_path}")


def demonstrate_comparison_charts():
    """Demonstrate comparison charts with multiple series."""
    print_section("6. COMPARISON CHARTS")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    # Filter for a few countries
    cli.apply_filter('country', ['United Kingdom', 'United States', 'France'])
    
    # Sort by month
    cli.df = cli.df.sort_values(['country', 'month'])
    
    print("Creating comparison chart: Multiple countries over time\n")
    
    output_path = Path("outputs") / "comparison_chart_demo.png"
    cli.create_visualization(
        chart_type='comparison',
        x='month',
        y='vaccination_rate',
        title='Vaccination Rates: UK, USA, and France',
        output_path=output_path,
        group_by='country'
    )
    
    print(f"Chart saved to: {output_path}")


def demonstrate_filtering_workflow():
    """Demonstrate filtering workflow."""
    print_section("7. FILTERING WORKFLOW")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    print("Original data:")
    print(f"  Records: {len(cli.df)}")
    print(f"  Countries: {cli.df['country'].nunique()}")
    
    print("\nApplying filter: year = 2021")
    cli.apply_filter('year', 2021)
    
    print(f"\nAfter filter:")
    print(f"  Records: {len(cli.df)}")
    
    print("\nApplying filter: vaccination_rate >= 0.05")
    cli.df = cli.df[cli.df['vaccination_rate'] >= 0.05]
    
    print(f"\nAfter second filter:")
    print(f"  Records: {len(cli.df)}")
    
    cli.show_data(max_rows=5)


def demonstrate_export():
    """Demonstrate data export."""
    print_section("8. DATA EXPORT")
    
    cli = HealthDataCLI()
    cli.load_data("data/sample_vaccination_data.csv")
    
    # Apply some filters
    cli.apply_filter('country', ['United Kingdom', 'United States'])
    cli.apply_filter('year', 2021)
    
    print(f"Exporting {len(cli.df)} filtered records\n")
    
    output_path = Path("outputs") / "filtered_data_export.csv"
    cli.export_data(output_path)


def demonstrate_comprehensive_workflow():
    """Demonstrate a complete analysis workflow."""
    print_section("9. COMPREHENSIVE WORKFLOW")
    
    print("Scenario: Analyze vaccination progress in 2021\n")
    
    # Initialize CLI
    cli = HealthDataCLI()
    
    # Step 1: Load data
    print("Step 1: Load data")
    cli.load_data("data/sample_vaccination_data.csv")
    
    # Step 2: Filter for 2021
    print("\nStep 2: Filter for year 2021")
    cli.apply_filter('year', 2021)
    
    # Step 3: Show summary
    print("\nStep 3: Summary statistics")
    cli.show_summary('doses_administered')
    
    # Step 4: Show grouped data
    print("\n\nStep 4: Total doses by country")
    cli.show_grouped_data('country', 'doses_administered', 'sum')
    
    # Step 5: Create visualization
    print("\n\nStep 5: Create visualization")
    
    from src.analysis import group_and_aggregate
    grouped = group_and_aggregate(
        cli.df,
        group_by='country',
        agg_column='doses_administered',
        agg_func='sum',
        sort_by='doses_administered',
        ascending=False
    )
    
    plot_df = grouped.reset_index()
    
    output_path = Path("outputs") / "2021_summary_chart.png"
    
    fig = create_bar_chart(
        plot_df,
        x='country',
        y='doses_administered',
        title='2021 Vaccination Doses by Country',
        ylabel='Total Doses',
        sort_by='doses_administered',
        ascending=False
    )
    
    save_chart(fig, output_path)
    print(f"Visualization saved: {output_path}")
    
    # Step 6: Export results
    print("\nStep 6: Export results")
    export_path = Path("outputs") / "2021_analysis_results.csv"
    cli.export_data(export_path)


def demonstrate_status_tracking():
    """Demonstrate status tracking."""
    print_section("10. STATUS TRACKING")
    
    cli = HealthDataCLI()
    
    print("Initial status:")
    status = cli.get_status()
    print(f"  Data loaded: {status['data_loaded']}")
    
    cli.load_data("data/sample_vaccination_data.csv")
    cli.apply_filter('country', 'United Kingdom')
    cli.apply_filter('year', 2021)
    
    print("\nAfter loading and filtering:")
    status = cli.get_status()
    print(f"  Data loaded: {status['data_loaded']}")
    print(f"  Data source: {status['data_source']}")
    print(f"  Records: {status['record_count']}")
    print(f"  Columns: {status['column_count']}")
    print(f"  Filters applied: {status['filters_applied']}")
    print(f"  Active filters:")
    for i, filter_desc in enumerate(status['filters'], 1):
        print(f"    {i}. {filter_desc}")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print(" PUBLIC HEALTH DATA DASHBOARD - CLI PRESENTATION LAYER DEMO")
    print(" Step 4: Presentation Layer (CLI)")
    print("="*70)
    
    # Create outputs directory
    Path("outputs").mkdir(exist_ok=True)
    
    # Run all demonstrations
    demonstrate_table_formatting()
    demonstrate_summary_statistics()
    demonstrate_grouped_data()
    demonstrate_bar_charts()
    demonstrate_line_charts()
    demonstrate_comparison_charts()
    demonstrate_filtering_workflow()
    demonstrate_export()
    demonstrate_comprehensive_workflow()
    demonstrate_status_tracking()
    
    # Final summary
    print_section("SUMMARY")
    print("[SUCCESS] CLI presentation layer demonstration completed!")
    print("\nCapabilities demonstrated:")
    print("  1. [OK] Table formatting and display")
    print("  2. [OK] Summary statistics presentation")
    print("  3. [OK] Grouped data views")
    print("  4. [OK] Bar chart creation")
    print("  5. [OK] Line chart creation")
    print("  6. [OK] Comparison charts (multiple series)")
    print("  7. [OK] Filtering workflows")
    print("  8. [OK] Data export")
    print("  9. [OK] Comprehensive analysis workflow")
    print("  10. [OK] Status tracking")
    print("\nAll visualizations saved to: outputs/")
    print("\nReady for Step 5: Extension Features")
    print()


if __name__ == "__main__":
    main()

