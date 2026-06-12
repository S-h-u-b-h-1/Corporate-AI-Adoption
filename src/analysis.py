"""Reusable EDA and business-insight functions for Corporate AI Adoption."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:
    from src.data_cleaning import (
        PROCESSED_DATA_PATH,
        RAW_DATA_PATH,
        REFERENCE_YEAR,
        REPORTS_DIR,
        build_data_quality_summary,
        clean_data,
        detect_outliers_iqr,
        load_raw_data,
    )
except ModuleNotFoundError:
    from data_cleaning import (
        PROCESSED_DATA_PATH,
        RAW_DATA_PATH,
        REFERENCE_YEAR,
        REPORTS_DIR,
        build_data_quality_summary,
        clean_data,
        detect_outliers_iqr,
        load_raw_data,
    )


ANALYSIS_NUMERIC_COLUMNS = [
    "ai_adoption_level",
    "ai_investment_usd",
    "automation_rate",
    "cost_savings",
    "revenue_impact",
    "productivity_gain",
    "employee_ai_training_hours",
    "ai_maturity_score",
    "deployment_count",
    "total_financial_impact",
    "roi_proxy",
]


def ensure_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned/enriched DataFrame if derived columns are missing."""
    required = {"region", "total_financial_impact", "roi_proxy", "company_scale_proxy"}
    if required.issubset(df.columns):
        return df.copy()
    return clean_data(df)


def format_pct(value: float, decimals: int = 1) -> str:
    return f"{value * 100:.{decimals}f}%"


def format_money(value: float) -> str:
    abs_value = abs(value)
    sign = "-" if value < 0 else ""
    if abs_value >= 1_000_000_000:
        return f"{sign}${abs_value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{sign}${abs_value / 1_000_000:.2f}M"
    if abs_value >= 1_000:
        return f"{sign}${abs_value / 1_000:.1f}K"
    return f"{sign}${abs_value:.0f}"


def dataset_overview(df: pd.DataFrame) -> dict[str, object]:
    df = ensure_analysis_columns(df)
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "unique_companies": df["company_id"].nunique(),
        "industries": df["industry"].nunique(),
        "countries": df["country"].nunique(),
        "regions": df["region"].nunique(),
        "min_year": int(df["year"].min()),
        "max_year": int(df["year"].max()),
        "avg_adoption": df["ai_adoption_level"].mean(),
        "avg_maturity": df["ai_maturity_score"].mean(),
        "avg_productivity_gain": df["productivity_gain"].mean(),
        "total_investment": df["ai_investment_usd"].sum(),
        "total_financial_impact": df["total_financial_impact"].sum(),
        "negative_revenue_rows": int((df["revenue_impact"] < 0).sum()),
        "negative_revenue_pct": float((df["revenue_impact"] < 0).mean()),
    }


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_pct": df.isna().mean().values,
        }
    ).sort_values(["missing_count", "column"], ascending=[False, True])


def duplicate_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "full_duplicate_rows", "value": int(df.duplicated().sum())},
            {"metric": "unique_company_ids", "value": int(df["company_id"].nunique())},
            {
                "metric": "company_ids_with_multiple_records",
                "value": int((df["company_id"].value_counts() > 1).sum()),
            },
        ]
    )


def univariate_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    return df[ANALYSIS_NUMERIC_COLUMNS].describe().T.reset_index(names="metric")


def categorical_summary(df: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    selected_columns = list(
        columns
        or ["industry", "country", "region", "adoption_stage", "maturity_stage", "company_scale_proxy"]
    )
    rows = []
    for column in selected_columns:
        counts = df[column].value_counts(dropna=False).head(10)
        for category, count in counts.items():
            rows.append(
                {
                    "column": column,
                    "category": str(category),
                    "records": int(count),
                    "record_pct": float(count / len(df)),
                }
            )
    return pd.DataFrame(rows)


def grouped_summary(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    return (
        df.groupby(group_col, observed=True)
        .agg(
            records=("company_id", "size"),
            unique_companies=("company_id", "nunique"),
            avg_adoption=("ai_adoption_level", "mean"),
            avg_maturity=("ai_maturity_score", "mean"),
            avg_productivity_gain=("productivity_gain", "mean"),
            avg_training_hours=("employee_ai_training_hours", "mean"),
            avg_automation_rate=("automation_rate", "mean"),
            avg_deployment_count=("deployment_count", "mean"),
            avg_investment=("ai_investment_usd", "mean"),
            avg_cost_savings=("cost_savings", "mean"),
            avg_revenue_impact=("revenue_impact", "mean"),
            avg_total_financial_impact=("total_financial_impact", "mean"),
            avg_roi_proxy=("roi_proxy", "mean"),
            advanced_share=("adoption_stage", lambda values: float((values == "Advanced").mean())),
            negative_revenue_share=("revenue_impact", lambda values: float((values < 0).mean())),
        )
        .reset_index()
        .sort_values("avg_adoption", ascending=False)
    )


def trend_by_year(df: pd.DataFrame) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    return (
        df.groupby("year")
        .agg(
            records=("company_id", "size"),
            avg_adoption=("ai_adoption_level", "mean"),
            avg_maturity=("ai_maturity_score", "mean"),
            avg_productivity_gain=("productivity_gain", "mean"),
            avg_automation_rate=("automation_rate", "mean"),
            avg_training_hours=("employee_ai_training_hours", "mean"),
            avg_total_financial_impact=("total_financial_impact", "mean"),
        )
        .reset_index()
        .sort_values("year")
    )


def correlation_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    return df[ANALYSIS_NUMERIC_COLUMNS].corr(numeric_only=True)


def adoption_driver_summary(df: pd.DataFrame) -> pd.DataFrame:
    corr = correlation_summary(df)["ai_adoption_level"].drop("ai_adoption_level")
    return (
        corr.sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "metric", "ai_adoption_level": "correlation_with_adoption"})
    )


def future_readiness_by_industry(df: pd.DataFrame) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    metrics = (
        df.groupby("industry")
        .agg(
            avg_adoption=("ai_adoption_level", "mean"),
            avg_maturity=("ai_maturity_score", "mean"),
            avg_productivity_gain=("productivity_gain", "mean"),
            avg_training_hours=("employee_ai_training_hours", "mean"),
            avg_deployment_count=("deployment_count", "mean"),
            avg_roi_proxy=("roi_proxy", "mean"),
        )
        .reset_index()
    )

    weights = {
        "avg_adoption": 0.25,
        "avg_maturity": 0.25,
        "avg_productivity_gain": 0.15,
        "avg_training_hours": 0.15,
        "avg_deployment_count": 0.10,
        "avg_roi_proxy": 0.10,
    }

    score = np.zeros(len(metrics), dtype=float)
    for column, weight in weights.items():
        minimum = metrics[column].min()
        maximum = metrics[column].max()
        normalized = np.zeros(len(metrics), dtype=float) if maximum == minimum else (
            metrics[column] - minimum
        ) / (maximum - minimum)
        score += normalized * weight

    metrics["future_readiness_score"] = score * 100
    return metrics.sort_values("future_readiness_score", ascending=False)


def markdown_table(df: pd.DataFrame, columns: list[str], max_rows: int = 10) -> str:
    table = df.loc[:, columns].head(max_rows).copy()
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in table.iterrows():
        values = []
        for column in columns:
            value = row[column]
            if isinstance(value, float):
                if column in {"year", "records", "outlier_count"}:
                    values.append(f"{int(round(value)):,}")
                elif "correlation" in column:
                    values.append(f"{value:.3f}")
                elif "pct" in column or "share" in column or "adoption" in column or "rate" in column or "gain" in column:
                    values.append(format_pct(value))
                elif "investment" in column or "impact" in column or "savings" in column or "revenue" in column:
                    values.append(format_money(value))
                else:
                    values.append(f"{value:.2f}")
            elif isinstance(value, (int, np.integer)) and column in {"year", "records", "outlier_count"}:
                values.append(f"{int(value):,}")
            else:
                values.append(str(value))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def build_top_insights(df: pd.DataFrame) -> list[str]:
    df = ensure_analysis_columns(df)
    overview = dataset_overview(df)
    industry = grouped_summary(df, "industry")
    country = grouped_summary(df, "country")
    region = grouped_summary(df, "region")
    scale = grouped_summary(df, "company_scale_proxy")
    maturity = grouped_summary(df, "maturity_stage")
    trend = trend_by_year(df)
    drivers = adoption_driver_summary(df)
    readiness = future_readiness_by_industry(df)

    first_year = trend.iloc[0]
    last_year = trend.iloc[-1]
    top_industry = industry.iloc[0]
    top_roi_industry = industry.sort_values("avg_roi_proxy", ascending=False).iloc[0]
    top_country = country.iloc[0]
    top_region = region.iloc[0]
    enterprise = scale.loc[scale["company_scale_proxy"].astype(str) == "Enterprise"].iloc[0]
    focused = scale.loc[scale["company_scale_proxy"].astype(str) == "Focused"].iloc[0]
    optimized = maturity.loc[maturity["maturity_stage"].astype(str) == "Optimized"].iloc[0]
    foundation = maturity.loc[maturity["maturity_stage"].astype(str) == "Foundation"].iloc[0]
    top_driver = drivers.iloc[0]
    top_readiness = readiness.iloc[0]

    return [
        (
            f"Average AI adoption rises from {format_pct(first_year['avg_adoption'])} in "
            f"{int(first_year['year'])} to {format_pct(last_year['avg_adoption'])} in "
            f"{int(last_year['year'])}. Years after {REFERENCE_YEAR} should be read as "
            "future/projected observations in this dataset."
        ),
        (
            f"{top_industry['industry']} has the highest average AI adoption by industry "
            f"at {format_pct(top_industry['avg_adoption'])}, with an average maturity score "
            f"of {top_industry['avg_maturity']:.2f}."
        ),
        (
            f"{top_roi_industry['industry']} has the strongest average ROI proxy "
            f"({top_roi_industry['avg_roi_proxy']:.2f}x), indicating the best combined "
            "cost-savings and revenue-impact return per dollar invested."
        ),
        (
            f"{top_country['country']} leads countries with average adoption of "
            f"{format_pct(top_country['avg_adoption'])} and an advanced-adoption share of "
            f"{format_pct(top_country['advanced_share'])}."
        ),
        (
            f"{top_region['region']} is the strongest region on average adoption "
            f"({format_pct(top_region['avg_adoption'])}) and maturity "
            f"({top_region['avg_maturity']:.2f})."
        ),
        (
            f"The Enterprise company-scale proxy averages {format_pct(enterprise['avg_adoption'])} "
            f"adoption compared with {format_pct(focused['avg_adoption'])} for the Focused proxy. "
            "This proxy is based on deployment_count because no true company-size column exists."
        ),
        (
            f"The strongest numeric adoption driver is {top_driver['metric']} with correlation "
            f"{top_driver['correlation_with_adoption']:.3f}. Productivity gain, maturity, "
            "training hours, automation, and deployment count are all strongly associated with adoption."
        ),
        (
            f"Optimized maturity records average {format_pct(optimized['avg_adoption'])} adoption and "
            f"{format_money(optimized['avg_total_financial_impact'])} average financial impact, versus "
            f"{format_pct(foundation['avg_adoption'])} and {format_money(foundation['avg_total_financial_impact'])} "
            "for Foundation maturity records."
        ),
        (
            f"{overview['negative_revenue_rows']:,} records ({format_pct(overview['negative_revenue_pct'])}) "
            "show negative revenue impact, so not every AI investment is immediately revenue-accretive."
        ),
        (
            f"{top_readiness['industry']} ranks highest on the future-readiness score "
            f"({top_readiness['future_readiness_score']:.1f}/100), based on adoption, maturity, "
            "productivity, training, deployment scale, and ROI proxy."
        ),
    ]


def generate_markdown_report(df: pd.DataFrame) -> str:
    df = ensure_analysis_columns(df)
    raw_df = load_raw_data(RAW_DATA_PATH)
    overview = dataset_overview(df)
    outliers = detect_outliers_iqr(df)
    industry = grouped_summary(df, "industry")
    country = grouped_summary(df, "country")
    region = grouped_summary(df, "region")
    scale = grouped_summary(df, "company_scale_proxy")
    trend = trend_by_year(df)
    drivers = adoption_driver_summary(df)
    readiness = future_readiness_by_industry(df)
    insights = build_top_insights(df)

    lines = [
        "# Corporate AI Adoption Insights Report",
        "",
        "## Dataset Description",
        "",
        (
            "This project analyzes the local Kaggle corporate AI adoption dataset. "
            f"The cleaned dataset contains {overview['rows']:,} rows, {overview['columns']:,} columns, "
            f"{overview['unique_companies']:,} unique company IDs, {overview['industries']} industries, "
            f"{overview['countries']} countries, and years {overview['min_year']} to {overview['max_year']}."
        ),
        "",
        (
            f"Years after {REFERENCE_YEAR} are treated as future/projected observations, "
            "not confirmed historical results."
        ),
        "",
        "## Cleaning Steps",
        "",
        "- Standardized column names to snake_case.",
        "- Validated the dataset schema before analysis.",
        "- Corrected numeric fields and integer year/deployment fields.",
        "- Checked missing values and full duplicate rows.",
        "- Added region from country.",
        "- Added adoption_stage and maturity_stage buckets.",
        "- Added total_financial_impact, roi_proxy, investment_per_deployment, and impact_per_deployment.",
        "- Added company_scale_proxy from deployment_count quartiles because no direct company-size column exists.",
        "- Detected IQR outliers for review; outliers were not removed.",
        "",
        "## Data Quality Snapshot",
        "",
        f"- Missing values: {int(raw_df.isna().sum().sum()):,}",
        f"- Full duplicate rows: {int(raw_df.duplicated().sum()):,}",
        f"- Negative revenue impact records: {overview['negative_revenue_rows']:,} ({format_pct(overview['negative_revenue_pct'])})",
        f"- Average AI adoption level: {format_pct(overview['avg_adoption'])}",
        f"- Average AI maturity score: {overview['avg_maturity']:.2f}/10",
        f"- Average productivity gain: {format_pct(overview['avg_productivity_gain'])}",
        "",
        "## Top 10 Insights",
        "",
    ]
    lines.extend([f"{index}. {insight}" for index, insight in enumerate(insights, start=1)])
    lines.extend(
        [
            "",
            "## Industry Comparison",
            "",
            markdown_table(
                industry,
                ["industry", "records", "avg_adoption", "avg_maturity", "avg_productivity_gain", "avg_roi_proxy"],
            ),
            "",
            "## Country Comparison",
            "",
            markdown_table(
                country,
                ["country", "records", "avg_adoption", "avg_maturity", "advanced_share", "avg_total_financial_impact"],
                max_rows=15,
            ),
            "",
            "## Region Comparison",
            "",
            markdown_table(
                region,
                ["region", "records", "avg_adoption", "avg_maturity", "avg_productivity_gain", "advanced_share"],
            ),
            "",
            "## Company-Scale Proxy Comparison",
            "",
            "The dataset does not include true company size, so this uses deployment_count quartiles as an AI operating-scale proxy.",
            "",
            markdown_table(
                scale,
                ["company_scale_proxy", "records", "avg_adoption", "avg_maturity", "avg_total_financial_impact", "advanced_share"],
            ),
            "",
            "## Adoption Trend",
            "",
            markdown_table(
                trend,
                ["year", "records", "avg_adoption", "avg_maturity", "avg_productivity_gain", "avg_total_financial_impact"],
                max_rows=25,
            ),
            "",
            "## Drivers and Barriers",
            "",
            "The dataset has no explicit survey fields for adoption drivers or barriers. The items below are inferred from numeric relationships and low-performing segments.",
            "",
            markdown_table(drivers, ["metric", "correlation_with_adoption"], max_rows=10),
            "",
            "Likely adoption drivers supported by the data:",
            "",
            "- Higher productivity gains.",
            "- Higher AI maturity scores.",
            "- More employee AI training hours.",
            "- Higher automation rates.",
            "- More AI deployments.",
            "",
            "Likely barriers inferred from the data:",
            "",
            "- Lower training intensity.",
            "- Lower automation readiness.",
            "- Fewer deployments and lower maturity.",
            "- Financial uncertainty, shown by records with negative revenue impact.",
            "",
            "## Future AI Readiness by Industry",
            "",
            markdown_table(
                readiness,
                ["industry", "future_readiness_score", "avg_adoption", "avg_maturity", "avg_productivity_gain", "avg_roi_proxy"],
            ),
            "",
            "## Outlier Review",
            "",
            markdown_table(outliers, ["column", "outlier_count", "outlier_pct"], max_rows=12),
            "",
            "## Business Implications",
            "",
            "- AI maturity is strongly linked with adoption and value creation.",
            "- Employee training appears central to scaling AI adoption.",
            "- Deployment scale matters: broader deployment footprints show much higher adoption maturity.",
            "- Financial outcomes vary, so cost savings and revenue impact should be tracked separately.",
            "- Regional and industry differences make peer benchmarking more useful than universal targets.",
            "",
            "## Recommendations",
            "",
            "- Build a practical AI maturity roadmap from pilots to scaled deployments.",
            "- Pair AI investments with employee training and change-management programs.",
            "- Track AI ROI using cost savings, revenue impact, productivity gain, and deployment count.",
            "- Investigate negative revenue-impact cases to identify implementation or measurement issues.",
            "- Benchmark adoption by industry and region before setting targets.",
            "",
            "## Dataset Limitations",
            "",
            "- No direct company-size column exists; company_scale_proxy is based on deployment count.",
            "- No explicit barrier or driver survey fields exist; barriers are inferred from available metrics.",
            "- Future years through 2035 should be interpreted as projected/modelled observations.",
            "- Company IDs repeat across records, so the dataset appears panel-like rather than one row per company.",
            "- Correlation does not prove causation.",
            "- The dataset source file is local, so this project references the Kaggle dataset provided in the project folder rather than a specific URL.",
            "",
        ]
    )
    return "\n".join(lines)


def run_full_analysis(output_dir: str | Path | None = None) -> dict[str, Path]:
    reports_dir = Path(output_dir) if output_dir else REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    raw_df = load_raw_data(RAW_DATA_PATH)
    df = clean_data(raw_df)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    outputs = {
        "cleaned_data": PROCESSED_DATA_PATH,
        "data_quality": reports_dir / "data_quality_summary.csv",
        "outliers": reports_dir / "outlier_summary.csv",
        "industry_summary": reports_dir / "industry_summary.csv",
        "country_summary": reports_dir / "country_summary.csv",
        "region_summary": reports_dir / "region_summary.csv",
        "scale_summary": reports_dir / "company_scale_proxy_summary.csv",
        "year_trend": reports_dir / "year_trend.csv",
        "adoption_drivers": reports_dir / "adoption_driver_correlations.csv",
        "future_readiness": reports_dir / "future_readiness_by_industry.csv",
        "report": reports_dir / "insights_report.md",
    }

    build_data_quality_summary(raw_df, df).to_csv(outputs["data_quality"], index=False)
    detect_outliers_iqr(df).to_csv(outputs["outliers"], index=False)
    grouped_summary(df, "industry").to_csv(outputs["industry_summary"], index=False)
    grouped_summary(df, "country").to_csv(outputs["country_summary"], index=False)
    grouped_summary(df, "region").to_csv(outputs["region_summary"], index=False)
    grouped_summary(df, "company_scale_proxy").to_csv(outputs["scale_summary"], index=False)
    trend_by_year(df).to_csv(outputs["year_trend"], index=False)
    adoption_driver_summary(df).to_csv(outputs["adoption_drivers"], index=False)
    future_readiness_by_industry(df).to_csv(outputs["future_readiness"], index=False)
    outputs["report"].write_text(generate_markdown_report(df), encoding="utf-8")
    return outputs


# Compatibility functions from the first scaffold.
def get_industry_adoption(df: pd.DataFrame) -> pd.DataFrame:
    return grouped_summary(df, "industry")


def get_regional_adoption(df: pd.DataFrame) -> pd.DataFrame:
    return grouped_summary(df, "country")


def get_company_size_adoption(df: pd.DataFrame) -> pd.DataFrame:
    return grouped_summary(df, "company_scale_proxy")


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return correlation_summary(df)


def get_impact_analysis(df: pd.DataFrame) -> pd.DataFrame:
    df = ensure_analysis_columns(df)
    cols = [
        "ai_adoption_level",
        "cost_savings",
        "revenue_impact",
        "productivity_gain",
        "ai_investment_usd",
        "total_financial_impact",
        "roi_proxy",
    ]
    return df[cols].corr(numeric_only=True)


def main() -> None:
    outputs = run_full_analysis()
    print("Analysis complete. Generated files:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
