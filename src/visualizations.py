"""Plotly visualization functions used by the dashboard and notebook."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Premium Neon Color Palette
COLOR_SEQUENCE = [
    "#00f2fe",  # Cyan
    "#4facfe",  # Light Blue
    "#f093fb",  # Pink
    "#f5576c",  # Red-Pink
    "#43e97b",  # Green
    "#38f9d7",  # Mint
    "#fa709a",  # Salmon
    "#fee140",  # Yellow
    "#a18cd1",  # Lavender
    "#fbc2eb",  # Light Pink
]

TEMPLATE = "plotly_dark"
FONT_FAMILY = "'Inter', 'Outfit', 'Segoe UI', sans-serif"

def _apply_layout(fig: go.Figure, title: str, height: int = 450) -> go.Figure:
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=22, color="#ffffff", family=FONT_FAMILY),
            x=0.02
        ),
        template=TEMPLATE,
        height=height,
        margin=dict(l=40, r=40, t=80, b=40),
        font=dict(family=FONT_FAMILY, size=14, color="#cbd5e1"),
        legend_title_text="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False, zeroline=False, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, zeroline=False, gridcolor="rgba(255,255,255,0.1)")
    return fig

def _sample_for_plot(df: pd.DataFrame, max_rows: int = 5_000) -> pd.DataFrame:
    """Keep scatter plots responsive on the 200k-row dataset."""
    if len(df) <= max_rows:
        return df
    return df.sample(max_rows, random_state=42)

def adoption_by_industry(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("industry", observed=True)
        .agg(avg_adoption=("ai_adoption_level", "mean"), records=("company_id", "size"))
        .reset_index()
        .sort_values("avg_adoption", ascending=True)
    )
    fig = px.bar(
        summary,
        x="avg_adoption",
        y="industry",
        orientation="h",
        color="avg_adoption",
        color_continuous_scale="Tealgrn",
        text=summary["avg_adoption"].map(lambda value: f"{value:.1%}"),
        hover_data={"avg_adoption": ":.1%", "records": ":,"},
    )
    fig.update_yaxes(title="")
    fig.update_xaxes(title="Average AI Adoption", tickformat=".0%")
    fig.update_traces(textfont_color="#ffffff", textposition="outside")
    return _apply_layout(fig, "Industry AI Adoption Rates")

def adoption_by_country(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    summary = (
        df.groupby("country", observed=True)
        .agg(avg_adoption=("ai_adoption_level", "mean"), records=("company_id", "size"))
        .reset_index()
        .sort_values("avg_adoption", ascending=False)
        .head(top_n)
    )
    fig = px.bar(
        summary,
        x="country",
        y="avg_adoption",
        color="avg_adoption",
        color_continuous_scale="Purpor",
        text=summary["avg_adoption"].map(lambda value: f"{value:.1%}"),
        hover_data={"avg_adoption": ":.1%", "records": ":,"},
    )
    fig.update_xaxes(title="", tickangle=-35)
    fig.update_yaxes(title="Adoption %", tickformat=".0%")
    fig.update_traces(textfont_color="#ffffff", textposition="outside")
    return _apply_layout(fig, "Top 15 Countries by Adoption")

def adoption_by_region(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("region", observed=True)
        .agg(
            avg_adoption=("ai_adoption_level", "mean"),
            avg_maturity=("ai_maturity_score", "mean"),
            records=("company_id", "size"),
        )
        .reset_index()
        .sort_values("avg_adoption", ascending=False)
    )
    fig = px.bar(
        summary,
        x="region",
        y="avg_adoption",
        color="avg_maturity",
        color_continuous_scale="Plasma",
        text=summary["avg_adoption"].map(lambda value: f"{value:.1%}"),
        hover_data={"avg_adoption": ":.1%", "avg_maturity": ":.2f", "records": ":,"},
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Adoption %", tickformat=".0%")
    fig.update_traces(textfont_color="#ffffff", textposition="outside")
    return _apply_layout(fig, "Regional Adoption & Maturity")

def trend_by_year(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("year")
        .agg(
            avg_adoption=("ai_adoption_level", "mean"),
            avg_productivity_gain=("productivity_gain", "mean"),
        )
        .reset_index()
        .sort_values("year")
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=summary["year"], y=summary["avg_adoption"],
        mode="lines", fill="tozeroy", name="AI Adoption",
        line=dict(color="#00f2fe", width=3),
        hovertemplate="<b>Year: %{x}</b><br>Adoption: %{y:.1%}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=summary["year"], y=summary["avg_productivity_gain"],
        mode="lines", name="Productivity Gain",
        line=dict(color="#f093fb", width=3, dash="dot"),
        hovertemplate="<b>Year: %{x}</b><br>Productivity: %{y:.1%}<extra></extra>"
    ))
    fig.update_yaxes(title="Average Rate", tickformat=".0%")
    fig.update_xaxes(title="")
    return _apply_layout(fig, "Evolution of AI Adoption & Productivity")

def maturity_comparison(df: pd.DataFrame) -> go.Figure:
    order = ["Foundation", "Developing", "Scaling", "Optimized"]
    summary = (
        df.groupby("maturity_stage", observed=True)
        .agg(
            avg_adoption=("ai_adoption_level", "mean"),
            avg_financial_impact=("total_financial_impact", "mean"),
            records=("company_id", "size"),
        )
        .reindex(order)
        .reset_index()
        .dropna(subset=["avg_adoption"])
    )
    fig = px.bar(
        summary,
        x="maturity_stage",
        y="avg_adoption",
        color="avg_financial_impact",
        color_continuous_scale="Sunset",
        text=summary["avg_adoption"].map(lambda value: f"{value:.1%}"),
        hover_data={"avg_adoption": ":.1%", "avg_financial_impact": ":$,.0f", "records": ":,"},
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Adoption %", tickformat=".0%")
    fig.update_traces(textfont_color="#ffffff", textposition="outside")
    return _apply_layout(fig, "Adoption Level by Maturity Stage")

def company_scale_comparison(df: pd.DataFrame) -> go.Figure:
    order = ["Focused", "Scaling", "Expanded", "Enterprise"]
    summary = (
        df.groupby("company_scale_proxy", observed=True)
        .agg(
            avg_adoption=("ai_adoption_level", "mean"),
            avg_maturity=("ai_maturity_score", "mean"),
            avg_financial_impact=("total_financial_impact", "mean"),
            records=("company_id", "size"),
        )
        .reindex(order)
        .reset_index()
        .dropna(subset=["avg_adoption"])
    )
    fig = px.bar(
        summary,
        x="company_scale_proxy",
        y="avg_adoption",
        color="avg_maturity",
        color_continuous_scale="Magma",
        text=summary["avg_adoption"].map(lambda value: f"{value:.1%}"),
        hover_data={
            "avg_adoption": ":.1%",
            "avg_maturity": ":.2f",
            "avg_financial_impact": ":$,.0f",
            "records": ":,",
        },
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Adoption %", tickformat=".0%")
    fig.update_traces(textfont_color="#ffffff", textposition="outside")
    return _apply_layout(fig, "Impact by Scale Proxy")

def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    numeric_columns = [
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
    corr = df[numeric_columns].corr(numeric_only=True)
    fig = px.imshow(
        corr,
        color_continuous_scale="Tropic",
        zmin=-1,
        zmax=1,
        text_auto=".2f",
        aspect="auto",
    )
    return _apply_layout(fig, "Metric Correlation Matrix", height=600)

def industry_region_heatmap(df: pd.DataFrame) -> go.Figure:
    pivot = df.pivot_table(
        index="industry",
        columns="region",
        values="ai_adoption_level",
        aggfunc="mean",
        observed=True,
    ).sort_index()
    fig = px.imshow(
        pivot,
        color_continuous_scale="Electric",
        text_auto=".1%",
        aspect="auto",
    )
    return _apply_layout(fig, "Global Adoption Heatmap", height=560)

def financial_impact_scatter(df: pd.DataFrame) -> go.Figure:
    sample = _sample_for_plot(df)
    fig = px.scatter(
        sample,
        x="ai_investment_usd",
        y="total_financial_impact",
        color="industry",
        size="deployment_count",
        size_max=25,
        opacity=0.7,
        color_discrete_sequence=COLOR_SEQUENCE,
        hover_data={
            "company_id": True,
            "country": True,
            "year": True,
            "ai_adoption_level": ":.1%",
            "ai_investment_usd": ":$,.0f",
            "total_financial_impact": ":$,.0f",
            "deployment_count": ":,",
        },
    )
    fig.update_xaxes(title="AI Investment ($)", separatethousands=True)
    fig.update_yaxes(title="Total Financial Impact ($)", separatethousands=True)
    return _apply_layout(fig, "Investment vs Returns Scaled by Deployment Count", height=600)

def roi_by_industry(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("industry", observed=True)
        .agg(avg_roi_proxy=("roi_proxy", "mean"), records=("company_id", "size"))
        .reset_index()
        .sort_values("avg_roi_proxy", ascending=True)
    )
    # Using a dot/lollipop plot design
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=summary["avg_roi_proxy"],
        y=summary["industry"],
        mode="markers",
        marker=dict(size=18, color="#00f2fe", line=dict(width=2, color="white")),
        text=summary["avg_roi_proxy"].map(lambda value: f"{value:.2f}x"),
        textposition="middle right",
        hovertemplate="Industry: %{y}<br>ROI Proxy: %{x:.2f}x<extra></extra>"
    ))
    # Add lollipop stems
    for i, row in summary.iterrows():
        fig.add_shape(
            type="line",
            x0=0, y0=row["industry"],
            x1=row["avg_roi_proxy"], y1=row["industry"],
            line=dict(color="#4facfe", width=3, dash="dot")
        )

    fig.update_xaxes(title="Average ROI Multiplier (Impact / Investment)", range=[0, summary["avg_roi_proxy"].max() * 1.1])
    fig.update_yaxes(title="")
    return _apply_layout(fig, "ROI Proxy by Industry")

def adoption_distribution(df: pd.DataFrame) -> go.Figure:
    # Changed to violin plot for a more premium look
    fig = px.violin(
        df,
        y="ai_adoption_level",
        x="adoption_stage",
        color="adoption_stage",
        box=True,
        points="all",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_yaxes(title="AI Adoption %", tickformat=".0%")
    fig.update_xaxes(title="")
    return _apply_layout(fig, "AI Adoption Density")

def automation_vs_productivity(df: pd.DataFrame) -> go.Figure:
    sample = _sample_for_plot(df)
    fig = px.scatter(
        sample,
        x="automation_rate",
        y="productivity_gain",
        color="maturity_stage",
        opacity=0.7,
        color_discrete_sequence=COLOR_SEQUENCE,
        hover_data={"industry": True, "automation_rate": ":.1%", "productivity_gain": ":.1%"},
    )
    fig.update_xaxes(title="Automation Rate", tickformat=".0%")
    fig.update_yaxes(title="Productivity Gain", tickformat=".0%")
    return _apply_layout(fig, "Automation vs Productivity by Maturity")

def training_impact(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby("maturity_stage", observed=True)
        .agg(avg_training=("employee_ai_training_hours", "mean"))
        .reset_index()
        .dropna()
    )
    fig = px.bar(
        summary,
        x="maturity_stage",
        y="avg_training",
        color="maturity_stage",
        color_discrete_sequence=COLOR_SEQUENCE,
        text=summary["avg_training"].map(lambda v: f"{v:.1f} hrs")
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Avg Training Hours")
    fig.update_traces(textfont_color="#ffffff", textposition="outside")
    return _apply_layout(fig, "Training Hours by Maturity Stage")

def cost_vs_revenue(df: pd.DataFrame) -> go.Figure:
    sample = _sample_for_plot(df)
    fig = px.scatter(
        sample,
        x="cost_savings",
        y="revenue_impact",
        color="region",
        opacity=0.7,
        color_discrete_sequence=COLOR_SEQUENCE,
        hover_data={"industry": True, "cost_savings": ":$,.0f", "revenue_impact": ":$,.0f"},
    )
    # Add a diagonal line for y=x to show where revenue impact > cost savings
    max_val = max(sample["cost_savings"].max(), sample["revenue_impact"].max())
    min_val = min(sample["cost_savings"].min(), sample["revenue_impact"].min())
    fig.add_shape(type="line", x0=min_val, y0=min_val, x1=max_val, y1=max_val, line=dict(color="rgba(255,255,255,0.2)", dash="dash"))
    
    fig.update_xaxes(title="Cost Savings ($)", separatethousands=True)
    fig.update_yaxes(title="Revenue Impact ($)", separatethousands=True)
    return _apply_layout(fig, "Cost Savings vs Revenue Impact")
