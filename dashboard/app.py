import streamlit as st
import pandas as pd
import sys
import os

# Add src to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis import (
    build_top_insights,
    ensure_analysis_columns
)
from src.visualizations import (
    adoption_by_country,
    adoption_by_industry,
    adoption_by_region,
    adoption_distribution,
    company_scale_comparison,
    correlation_heatmap,
    financial_impact_scatter,
    industry_region_heatmap,
    maturity_comparison,
    roi_by_industry,
    trend_by_year,
    automation_vs_productivity,
    training_impact,
    cost_vs_revenue
)

# Page configuration
st.set_page_config(
    page_title="Corporate AI Adoption Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Executive Dark Mode & Glassmorphism CSS ---
st.markdown("""
<style>
    /* Global Font Settings */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@400;700;900&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* App Background */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f8fafc;
    }

    /* Main Header */
    .main-header {
        font-family: 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: -10px;
        text-align: center;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 30px;
        text-align: center;
        font-weight: 300;
    }

    /* Built By Badge */
    .built-by {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #38bdf8 !important;
        padding: 8px 20px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 50px;
        display: inline-block;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        text-decoration: none !important;
        transition: all 0.3s ease;
    }
    .built-by:hover {
        background: rgba(56, 189, 248, 0.2);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        color: #fff !important;
        transform: translateY(-2px);
    }
    .built-by-container {
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
    }

    /* Control Panel Box Styling */
    .control-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
    }
    .control-panel-title {
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }

    /* Glassmorphism KPI Cards */
    .metric-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 242, 254, 0.5);
    }
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        white-space: nowrap;
    }
    .metric-value {
        color: #f8fafc;
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
        white-space: nowrap;
    }

    /* Strategic Insight Cards */
    .insight-card {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 8px;
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .insight-card h4 {
        color: #10b981;
        font-family: 'Outfit', sans-serif;
        margin-top: 0;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
    }

    /* Tabs Styling Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(255,255,255,0.02);
        padding: 10px 20px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for currency formatting
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

@st.cache_data
def load_dashboard_data():
    path = "data/processed/cleaned_data.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        return ensure_analysis_columns(df)
    
    raw_path = "data/raw/corporate_ai_adoption_dataset.csv"
    if os.path.exists(raw_path):
        from src.data_cleaning import clean_data
        return clean_data(pd.read_csv(raw_path))
    return pd.DataFrame()

df = load_dashboard_data()

if df.empty:
    st.error("No data found! Please ensure data is loaded into data/processed/.")
    st.stop()

# --- Header & Branding ---
st.markdown('<div class="main-header">Corporate AI Adoption Matrix</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive Overview of AI Maturity, Operational Readiness & Financial Impact</div>', unsafe_allow_html=True)

# Floating LinkedIn Badge
st.markdown(
    '<div class="built-by-container">'
    '<a href="https://www.linkedin.com/in/shubhaangkataruka/" target="_blank" class="built-by">'
    'Built by Shubhaang Kataruka</a></div>', 
    unsafe_allow_html=True
)

# --- Top Level Control Panel ---
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown('<div class="control-panel-title">🎛️ Command Center Parameters</div>', unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

def get_options(col):
    return sorted(df[col].dropna().unique().tolist())

with filter_col1:
    selected_industry = st.multiselect("Industry Sector", get_options('industry'))
with filter_col2:
    selected_region = st.multiselect("Geographic Region", get_options('region'))
with filter_col3:
    selected_maturity = st.multiselect("Maturity Stage", get_options('maturity_stage'))
with filter_col4:
    selected_scale = st.multiselect("Scale Proxy", get_options('company_scale_proxy'))

year_min, year_max = int(df['year'].min()), int(df['year'].max())
selected_years = st.slider("Timeline Horizon", year_min, year_max, (year_min, year_max))
st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()

if selected_industry:
    filtered_df = filtered_df[filtered_df['industry'].isin(selected_industry)]
if selected_region:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_region)]
if selected_maturity:
    filtered_df = filtered_df[filtered_df['maturity_stage'].isin(selected_maturity)]
if selected_scale:
    filtered_df = filtered_df[filtered_df['company_scale_proxy'].isin(selected_scale)]

filtered_df = filtered_df[filtered_df['year'].between(selected_years[0], selected_years[1])]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your Command Center parameters.")
    st.stop()

# --- Glassmorphism KPI Section ---
total_records = len(filtered_df)
avg_adoption = filtered_df["ai_adoption_level"].mean()
avg_maturity = filtered_df["ai_maturity_score"].mean()
avg_productivity = filtered_df["productivity_gain"].mean()
total_investment = filtered_df["ai_investment_usd"].sum()
total_impact = filtered_df["total_financial_impact"].sum()

cols = st.columns(6)
kpis = [
    ("Companies", f"{total_records:,}"),
    ("Adoption Rate", f"{avg_adoption:.1%}"),
    ("Maturity Index", f"{avg_maturity:.2f}"),
    ("Productivity", f"+{avg_productivity:.1%}"),
    ("Total CAPEX", format_money(total_investment)),
    ("Financial ROI", format_money(total_impact))
]

for i, col in enumerate(cols):
    title, value = kpis[i]
    col.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# --- Multi-Tab Navigation ---
tab_insights, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💡 Strategic Insights",
    "📈 Trajectory & Correlations", 
    "🌍 Global Distribution", 
    "💰 Financial Economics", 
    "⚙️ Operational Impact", 
    "📋 Raw Data Matrix"
])

with tab_insights:
    is_filtered = bool(selected_industry or selected_region or selected_maturity or selected_scale or (selected_years[0] > year_min or selected_years[1] < year_max))
    
    if not is_filtered:
        st.markdown("### 📊 About the Corporate AI Adoption Dataset")
        st.markdown("""
        <div class="insight-card" style="border-left-color: #00f2fe; background: rgba(0, 242, 254, 0.05);">
            <h4 style="color: #00f2fe;">The Global Benchmark</h4>
            This dataset encompasses <strong>200,000</strong> corporate entities globally, tracking their journey through AI adoption. It measures maturity levels, financial investments, productivity gains, and total revenue impacts across different industries and regions.
        </div>
        <div class="insight-card" style="border-left-color: #f093fb; background: rgba(240, 147, 251, 0.05);">
            <h4 style="color: #f093fb;">How to Use This Dashboard</h4>
            The visualizations and KPIs on this dashboard are completely interactive. <strong>Use the Command Center Parameters above</strong> to filter by specific industries, regions, or maturity stages. As you apply filters, this insights page and all charts will automatically recalculate to reveal hidden trends and ROI metrics specific to your selection.
        </div>
        """, unsafe_allow_html=True)
    else:
        col_l, col_r = st.columns([1, 1])
        
        with col_l:
            st.markdown("### Executive Summary")
            st.markdown("""
            <div class="insight-card">
                <h4>1. Maturity Drives Value</h4>
                AI maturity is strongly linked with adoption and value creation. Organizations in the 'Optimized' stage 
                report significantly higher financial impact and productivity gains compared to those in 'Foundation' stages.
            </div>
            <div class="insight-card">
                <h4>2. Training is the Catalyst</h4>
                Employee training appears central to scaling AI adoption. Higher AI training hours correlate strongly 
                with elevated maturity scores and improved automation rates.
            </div>
            <div class="insight-card">
                <h4>3. Scale Matters</h4>
                Deployment scale is highly influential: broader deployment footprints show much higher adoption maturity. 
                Companies scaling from isolated pilots to enterprise-wide integration experience exponential ROI growth.
            </div>
            """, unsafe_allow_html=True)
    
        with col_r:
            st.markdown("### Dynamic Filtered Insights")
            try:
                insights = build_top_insights(filtered_df)
                if insights:
                    for i in range(min(3, len(insights))):
                        st.markdown(f"""
                        <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-left: 4px solid #00f2fe; padding: 1.2rem; border-radius: 8px; color: #e2e8f0; margin-bottom: 1rem;">
                            <strong style="color: #00f2fe;">Dynamic Observation {i+1}</strong><br>
                            {insights[i]}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Not enough data to generate insights for this specific filter slice.")
            except Exception as e:
                st.info("Adjust filters to generate automated insights.")

with tab1:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.plotly_chart(trend_by_year(filtered_df), use_container_width=True)
    with col2:
        st.plotly_chart(adoption_distribution(filtered_df), use_container_width=True)
    st.plotly_chart(correlation_heatmap(filtered_df), use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(adoption_by_industry(filtered_df), use_container_width=True)
    with col2:
        st.plotly_chart(adoption_by_region(filtered_df), use_container_width=True)
    
    st.plotly_chart(industry_region_heatmap(filtered_df), use_container_width=True)
    st.plotly_chart(adoption_by_country(filtered_df), use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(roi_by_industry(filtered_df), use_container_width=True)
    with col2:
        st.plotly_chart(cost_vs_revenue(filtered_df), use_container_width=True)
    st.plotly_chart(financial_impact_scatter(filtered_df), use_container_width=True)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(automation_vs_productivity(filtered_df), use_container_width=True)
    with col2:
        st.plotly_chart(training_impact(filtered_df), use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(maturity_comparison(filtered_df), use_container_width=True)
    with col4:
        st.plotly_chart(company_scale_comparison(filtered_df), use_container_width=True)

with tab5:
    st.markdown("#### Interactive Dataset Explorer")
    st.dataframe(filtered_df, use_container_width=True, height=500)
    st.download_button(
        "📥 Download Current View (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="corporate_ai_filtered_matrix.csv",
        mime="text/csv",
    )

# Force reload
