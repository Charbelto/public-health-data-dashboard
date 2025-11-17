"""
Entry point for the Public Health Data Insights Dashboard (Task 1).

For now this file only contains a minimal structure and a stub for load_dataset.
We will grow this step-by-step using TDD.
"""

from pathlib import Path
import pandas as pd


def load_dataset(path: str | Path) -> pd.DataFrame:
    """
    Load a public health dataset from a CSV file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the loaded data.

    Notes
    -----
    The actual implementation will be added later.
    For now the function deliberately raises NotImplementedError
    so that our first test will fail (TDD).
    """
    raise NotImplementedError("load_dataset() not implemented yet")


def main() -> None:
    """
    Placeholder CLI entry point.

    In later steps this will:
    - Load data
    - Ask the user for filters
    - Display tables and charts
    """
    print("Public Health Data Insights Dashboard (stub)")
    # Implementation will be added in later commits.


if __name__ == "__main__":
    main()
