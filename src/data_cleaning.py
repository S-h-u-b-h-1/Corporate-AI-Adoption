"""Data loading, validation, cleaning, and feature engineering utilities.

This module is shared by the notebook, analysis scripts, and Streamlit
dashboard. It validates the real dataset columns before creating derived
features, so future dataset changes fail with a clear message instead of silent
wrong analysis.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "corporate_ai_adoption_dataset.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"

# The source data includes years beyond the current project date. Those rows are
# analyzed as projected/modelled observations, not confirmed historical outcomes.
REFERENCE_YEAR = 2026

EXPECTED_COLUMNS = [
    "company_id",
    "industry",
    "country",
    "year",
    "ai_adoption_level",
    "ai_investment_usd",
    "automation_rate",
    "cost_savings",
    "revenue_impact",
    "productivity_gain",
    "employee_ai_training_hours",
    "ai_maturity_score",
    "deployment_count",
]

NUMERIC_COLUMNS = [
    "year",
    "ai_adoption_level",
    "ai_investment_usd",
    "automation_rate",
    "cost_savings",
    "revenue_impact",
    "productivity_gain",
    "employee_ai_training_hours",
    "ai_maturity_score",
    "deployment_count",
]

COUNTRY_TO_REGION = {
    "United States": "North America",
    "Canada": "North America",
    "China": "Asia-Pacific",
    "Japan": "Asia-Pacific",
    "India": "Asia-Pacific",
    "South Korea": "Asia-Pacific",
    "Australia": "Asia-Pacific",
    "Singapore": "Asia-Pacific",
    "Germany": "Europe",
    "United Kingdom": "Europe",
    "France": "Europe",
    "Sweden": "Europe",
    "Netherlands": "Europe",
    "Brazil": "South America",
    "UAE": "Middle East",
}


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns.str.strip()
        .str.lower()
        .str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)
        .str.strip("_")
    )
    return cleaned


def validate_schema(df: pd.DataFrame, required_columns: Iterable[str] | None = None) -> None:
    """Raise a clear error if required source fields are missing."""
    required = list(required_columns or EXPECTED_COLUMNS)
    missing = [column for column in required if column not in df.columns]
    if missing:
        available = ", ".join(df.columns)
        raise ValueError(
            "Dataset schema mismatch. Missing columns: "
            f"{missing}. Available columns: {available}"
        )


def load_data(filepath: str | Path) -> pd.DataFrame:
    """Load a CSV file from disk.

    Kept for compatibility with the original project scaffold.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def load_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the raw CSV, clean column names, and validate expected fields."""
    data_path = Path(path) if path else RAW_DATA_PATH
    df = load_data(data_path)
    df = clean_column_names(df)
    validate_schema(df)
    return df


def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Apply practical data types without changing real values."""
    cleaned = clean_column_names(df)
    validate_schema(cleaned)

    for column in ["company_id", "industry", "country"]:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    for integer_column in ["year", "deployment_count"]:
        if cleaned[integer_column].isna().any():
            cleaned[integer_column] = cleaned[integer_column].astype("Int64")
        else:
            cleaned[integer_column] = cleaned[integer_column].astype(int)

    return cleaned


def create_company_scale_proxy(df: pd.DataFrame) -> pd.Series:
    """Create an AI operating-scale proxy from deployment_count quartiles.

    The dataset has no employee-count, revenue-band, or company-size column.
    This field should be read as AI deployment scale, not true company size.
    """
    labels = ["Focused", "Scaling", "Expanded", "Enterprise"]
    deployment_count = pd.to_numeric(df["deployment_count"], errors="coerce")
    quantiles = deployment_count.quantile([0.25, 0.50, 0.75]).tolist()
    bins = [-np.inf, *quantiles, np.inf]

    if len(set(bins)) == len(bins):
        return pd.cut(deployment_count, bins=bins, labels=labels, include_lowest=True)

    ranked = deployment_count.rank(method="first")
    return pd.qcut(ranked, q=4, labels=labels)


def add_business_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add reusable business analysis fields."""
    featured = df.copy()
    featured["region"] = featured["country"].map(COUNTRY_TO_REGION).fillna("Other")
    featured["total_financial_impact"] = featured["cost_savings"] + featured["revenue_impact"]

    featured["roi_proxy"] = np.where(
        featured["ai_investment_usd"] > 0,
        featured["total_financial_impact"] / featured["ai_investment_usd"],
        np.nan,
    )
    featured["investment_per_deployment"] = np.where(
        featured["deployment_count"] > 0,
        featured["ai_investment_usd"] / featured["deployment_count"],
        np.nan,
    )
    featured["impact_per_deployment"] = np.where(
        featured["deployment_count"] > 0,
        featured["total_financial_impact"] / featured["deployment_count"],
        np.nan,
    )

    featured["adoption_stage"] = pd.cut(
        featured["ai_adoption_level"],
        bins=[-np.inf, 0.35, 0.65, np.inf],
        labels=["Emerging", "Scaling", "Advanced"],
    )
    featured["maturity_stage"] = pd.cut(
        featured["ai_maturity_score"],
        bins=[-np.inf, 4, 6, 8, np.inf],
        labels=["Foundation", "Developing", "Scaling", "Optimized"],
    )
    featured["time_period"] = np.where(
        featured["year"] <= REFERENCE_YEAR,
        "Observed/current period",
        "Future/projected period",
    )
    featured["company_scale_proxy"] = create_company_scale_proxy(featured)

    # Compatibility column for first-version notebook/dashboard code. It is a
    # proxy, not true employee-count company size.
    featured["company_size"] = featured["company_scale_proxy"].astype("string")
    return featured


def clean_data(data: pd.DataFrame | str | Path | None = None) -> pd.DataFrame:
    """Clean and enrich data from a DataFrame or CSV path.

    This flexible signature keeps the original scaffold usable:
    clean_data(df) and clean_data("path.csv") both work.
    """
    if data is None:
        raw_df = load_raw_data()
    elif isinstance(data, pd.DataFrame):
        raw_df = clean_column_names(data)
        validate_schema(raw_df)
    else:
        raw_df = load_raw_data(data)

    typed_df = correct_data_types(raw_df)
    cleaned_df = typed_df.drop_duplicates().copy()
    return add_business_features(cleaned_df)


def save_data(df: pd.DataFrame, output_path: str | Path) -> None:
    """Save a DataFrame to CSV, creating folders as needed."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Data saved to {path}")


def save_clean_dataset(
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Create the cleaned dataset used by the notebook and dashboard."""
    output = Path(output_path) if output_path else PROCESSED_DATA_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df = clean_data(input_path or RAW_DATA_PATH)
    cleaned_df.to_csv(output, index=False)
    return output


def detect_outliers_iqr(
    df: pd.DataFrame, columns: Iterable[str] | None = None
) -> pd.DataFrame:
    """Detect IQR outliers for reporting; values are not removed."""
    numeric_columns = list(columns) if columns else [
        column for column in df.select_dtypes(include=[np.number]).columns if column != "year"
    ]

    rows = []
    for column in numeric_columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        mask = (df[column] < lower_bound) | (df[column] > upper_bound)
        rows.append(
            {
                "column": column,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outlier_count": int(mask.sum()),
                "outlier_pct": float(mask.mean()),
            }
        )

    return pd.DataFrame(rows).sort_values("outlier_pct", ascending=False)


def build_data_quality_summary(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Create a compact data-quality table for reports."""
    return pd.DataFrame(
        [
            {"check": "raw_rows", "value": len(raw_df)},
            {"check": "raw_columns", "value": raw_df.shape[1]},
            {"check": "missing_values_total", "value": int(raw_df.isna().sum().sum())},
            {"check": "full_duplicate_rows", "value": int(raw_df.duplicated().sum())},
            {"check": "unique_companies", "value": int(cleaned_df["company_id"].nunique())},
            {"check": "unique_industries", "value": int(cleaned_df["industry"].nunique())},
            {"check": "unique_countries", "value": int(cleaned_df["country"].nunique())},
            {"check": "min_year", "value": int(cleaned_df["year"].min())},
            {"check": "max_year", "value": int(cleaned_df["year"].max())},
            {
                "check": "negative_revenue_impact_rows",
                "value": int((cleaned_df["revenue_impact"] < 0).sum()),
            },
        ]
    )


def main() -> None:
    raw_df = load_raw_data(RAW_DATA_PATH)
    cleaned_df = clean_data(raw_df)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_df.to_csv(PROCESSED_DATA_PATH, index=False)
    build_data_quality_summary(raw_df, cleaned_df).to_csv(
        REPORTS_DIR / "data_quality_summary.csv", index=False
    )
    detect_outliers_iqr(cleaned_df).to_csv(REPORTS_DIR / "outlier_summary.csv", index=False)

    print(f"Cleaned dataset saved to {PROCESSED_DATA_PATH}")
    print(f"Rows: {len(cleaned_df):,} | Columns: {cleaned_df.shape[1]:,}")


if __name__ == "__main__":
    main()

