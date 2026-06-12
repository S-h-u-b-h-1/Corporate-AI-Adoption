# Corporate AI Adoption Analysis + Dashboard

A portfolio-ready Python data analysis project exploring corporate AI adoption, maturity, investment, productivity, and financial impact across industries, countries, and years.

## Objective

Analyze corporate AI adoption trends and turn the results into reusable analysis code, an exploratory notebook, an evidence-backed insights report, and an interactive Streamlit dashboard.

## Dataset Source

The dataset is a Kaggle Corporate AI Adoption dataset already provided in this project folder:

`data/raw/corporate_ai_adoption_dataset.csv`

The data includes 200,000 records, 8,000 unique company IDs, 10 industries, 15 countries, and years from 2015 to 2035. Years after 2026 are treated as future/projected observations.

## Tech Stack

- Python
- Pandas and NumPy
- Matplotlib and Seaborn for notebook EDA
- Plotly for interactive visualizations
- Streamlit for the dashboard
- Jupyter Notebook

## Folder Structure

```text
corporate-ai-adoption-analysis/
├── data/
│   ├── raw/
│   │   └── corporate_ai_adoption_dataset.csv
│   └── processed/
│       └── cleaned_data.csv
├── notebooks/
│   └── exploratory_analysis.ipynb
├── src/
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualizations.py
├── dashboard/
│   └── app.py
├── reports/
│   ├── insights_report.md
│   ├── industry_summary.csv
│   ├── country_summary.csv
│   ├── region_summary.csv
│   ├── company_scale_proxy_summary.csv
│   ├── year_trend.csv
│   ├── adoption_driver_correlations.csv
│   ├── future_readiness_by_industry.csv
│   ├── data_quality_summary.csv
│   └── outlier_summary.csv
├── requirements.txt
└── README.md
```

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the cleaned dataset:

```bash
python src/data_cleaning.py
```

Generate summaries and the markdown insights report:

```bash
python src/analysis.py
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Key Insights

- Average AI adoption rises from 19.1% in 2015 to 85.8% in 2035. Future years after 2026 should be interpreted as projected records.
- Energy has the highest average industry adoption at 53.2%.
- Technology has the strongest average ROI proxy at 1.31x.
- The United States leads countries with 54.7% average adoption and a 36.6% advanced-adoption share.
- North America is the strongest region by adoption at 54.4% and maturity score at 6.55.
- Productivity gain is the strongest numeric adoption driver, with a 0.953 correlation to AI adoption level.
- The dataset has no true company-size column, so company-scale analysis uses a transparent deployment-count proxy.

## Dashboard Features

- KPI cards for record count, adoption, maturity, productivity, investment, and financial impact.
- Sidebar filters for industry, region, country, year, maturity stage, adoption stage, and company-scale proxy.
- Interactive Plotly charts for trends, industry comparison, regional comparison, correlations, ROI, and financial impact.
- Insight cards and recommendations based on the currently filtered data.
- Download option for filtered records.

## Important Data Notes

- There are no missing values and no full duplicate rows in the raw dataset.
- Company IDs repeat across records, so the dataset appears panel-like rather than one row per company.
- The dataset does not include employee count, revenue band, or direct company size. `company_scale_proxy` is derived from deployment-count quartiles.
- The dataset does not include explicit survey fields for adoption barriers. Barriers are inferred from available metrics such as training, automation, maturity, deployments, and revenue impact.
- Correlations are useful for insight generation but do not prove causation.

## Future Improvements

- Add predictive modeling for adoption maturity or financial impact.
- Add clustering to segment companies by AI behavior and value profile.
- Add model explainability for drivers of adoption and ROI.
- Compare projected future years against real updated observations if a newer dataset becomes available.
