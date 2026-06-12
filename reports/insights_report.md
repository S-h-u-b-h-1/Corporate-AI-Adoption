# Corporate AI Adoption Insights Report

## Dataset Description

This project analyzes the local Kaggle corporate AI adoption dataset. The cleaned dataset contains 200,000 rows, 23 columns, 8,000 unique company IDs, 10 industries, 15 countries, and years 2015 to 2035.

Years after 2026 are treated as future/projected observations, not confirmed historical results.

## Cleaning Steps

- Standardized column names to snake_case.
- Validated the dataset schema before analysis.
- Corrected numeric fields and integer year/deployment fields.
- Checked missing values and full duplicate rows.
- Added region from country.
- Added adoption_stage and maturity_stage buckets.
- Added total_financial_impact, roi_proxy, investment_per_deployment, and impact_per_deployment.
- Added company_scale_proxy from deployment_count quartiles because no direct company-size column exists.
- Detected IQR outliers for review; outliers were not removed.

## Data Quality Snapshot

- Missing values: 0
- Full duplicate rows: 0
- Negative revenue impact records: 7,440 (3.7%)
- Average AI adoption level: 52.8%
- Average AI maturity score: 6.27/10
- Average productivity gain: 39.5%

## Top 10 Insights

1. Average AI adoption rises from 19.1% in 2015 to 85.8% in 2035. Years after 2026 should be read as future/projected observations in this dataset.
2. Energy has the highest average AI adoption by industry at 53.2%, with an average maturity score of 6.30.
3. Technology has the strongest average ROI proxy (1.31x), indicating the best combined cost-savings and revenue-impact return per dollar invested.
4. United States leads countries with average adoption of 54.7% and an advanced-adoption share of 36.6%.
5. North America is the strongest region on average adoption (54.4%) and maturity (6.55).
6. The Enterprise company-scale proxy averages 83.3% adoption compared with 23.2% for the Focused proxy. This proxy is based on deployment_count because no true company-size column exists.
7. The strongest numeric adoption driver is productivity_gain with correlation 0.953. Productivity gain, maturity, training hours, automation, and deployment count are all strongly associated with adoption.
8. Optimized maturity records average 85.4% adoption and $9.06M average financial impact, versus 15.0% and $1.01M for Foundation maturity records.
9. 7,440 records (3.7%) show negative revenue impact, so not every AI investment is immediately revenue-accretive.
10. Energy ranks highest on the future-readiness score (90.6/100), based on adoption, maturity, productivity, training, deployment scale, and ROI proxy.

## Industry Comparison

| industry | records | avg_adoption | avg_maturity | avg_productivity_gain | avg_roi_proxy |
| --- | --- | --- | --- | --- | --- |
| Energy | 14,080 | 53.2% | 6.30 | 42.7% | 0.68 |
| Agriculture | 9,934 | 53.0% | 6.29 | 40.6% | 0.58 |
| Financial Services | 27,927 | 52.9% | 6.28 | 40.6% | 0.79 |
| Healthcare | 24,026 | 52.9% | 6.28 | 34.9% | 0.66 |
| Retail | 20,048 | 52.8% | 6.27 | 36.8% | 0.83 |
| Manufacturing | 29,884 | 52.8% | 6.28 | 44.2% | 0.64 |
| Logistics | 16,021 | 52.7% | 6.26 | 43.3% | 0.72 |
| Telecom | 14,128 | 52.7% | 6.27 | 38.5% | 0.77 |
| Technology | 35,994 | 52.6% | 6.25 | 38.5% | 1.31 |
| Education | 7,958 | 52.1% | 6.22 | 30.7% | 0.48 |

## Country Comparison

| country | records | avg_adoption | avg_maturity | advanced_share | avg_total_financial_impact |
| --- | --- | --- | --- | --- | --- |
| United States | 50,080 | 54.7% | 6.60 | 36.6% | $5.98M |
| Singapore | 3,958 | 53.5% | 6.42 | 35.0% | $5.10M |
| United Kingdom | 13,989 | 53.4% | 6.42 | 35.1% | $4.73M |
| Canada | 10,114 | 53.1% | 6.28 | 34.8% | $4.59M |
| China | 35,906 | 52.9% | 6.28 | 34.4% | $5.04M |
| Sweden | 4,057 | 52.9% | 6.28 | 35.3% | $4.70M |
| Germany | 16,040 | 52.2% | 6.23 | 33.4% | $4.49M |
| Australia | 5,960 | 51.8% | 6.09 | 32.3% | $4.08M |
| South Korea | 8,033 | 51.7% | 6.09 | 32.5% | $4.16M |
| Netherlands | 4,032 | 51.7% | 6.09 | 32.8% | $4.04M |
| Japan | 14,125 | 51.6% | 6.08 | 32.8% | $4.09M |
| France | 9,896 | 51.6% | 6.08 | 32.4% | $4.19M |
| India | 13,911 | 51.1% | 5.94 | 31.5% | $2.92M |
| UAE | 1,968 | 50.4% | 5.80 | 32.0% | $3.58M |
| Brazil | 7,931 | 48.7% | 5.57 | 28.5% | $2.41M |

## Region Comparison

| region | records | avg_adoption | avg_maturity | avg_productivity_gain | advanced_share |
| --- | --- | --- | --- | --- | --- |
| North America | 60,194 | 54.4% | 6.55 | 41.2% | 36.3% |
| Europe | 48,014 | 52.4% | 6.24 | 39.2% | 33.8% |
| Asia-Pacific | 81,893 | 52.2% | 6.16 | 38.9% | 33.3% |
| Middle East | 1,968 | 50.4% | 5.80 | 36.8% | 32.0% |
| South America | 7,931 | 48.7% | 5.57 | 35.5% | 28.5% |

## Company-Scale Proxy Comparison

The dataset does not include true company size, so this uses deployment_count quartiles as an AI operating-scale proxy.

| company_scale_proxy | records | avg_adoption | avg_maturity | avg_total_financial_impact | advanced_share |
| --- | --- | --- | --- | --- | --- |
| Enterprise | 47,380 | 83.3% | 8.76 | $8.68M | 91.7% |
| Expanded | 50,073 | 63.1% | 7.13 | $5.53M | 43.9% |
| Scaling | 50,287 | 44.6% | 5.58 | $3.41M | 5.5% |
| Focused | 52,260 | 23.2% | 3.87 | $1.61M | 0.1% |

## Adoption Trend

| year | records | avg_adoption | avg_maturity | avg_productivity_gain | avg_total_financial_impact |
| --- | --- | --- | --- | --- | --- |
| 2,015 | 9,419 | 19.1% | 3.41 | 15.1% | $1.38M |
| 2,016 | 9,517 | 22.0% | 3.67 | 17.3% | $1.58M |
| 2,017 | 9,542 | 25.2% | 3.95 | 19.6% | $1.87M |
| 2,018 | 9,680 | 28.8% | 4.25 | 22.1% | $2.12M |
| 2,019 | 9,695 | 32.0% | 4.54 | 24.5% | $2.36M |
| 2,020 | 9,455 | 35.4% | 4.82 | 26.9% | $2.67M |
| 2,021 | 9,600 | 39.1% | 5.11 | 29.5% | $3.01M |
| 2,022 | 9,365 | 42.6% | 5.41 | 32.2% | $3.31M |
| 2,023 | 9,522 | 45.6% | 5.68 | 34.3% | $3.61M |
| 2,024 | 9,532 | 49.5% | 5.99 | 37.1% | $4.02M |
| 2,025 | 9,518 | 53.0% | 6.29 | 39.6% | $4.42M |
| 2,026 | 9,653 | 56.7% | 6.59 | 42.3% | $4.91M |
| 2,027 | 9,355 | 59.8% | 6.86 | 44.7% | $5.27M |
| 2,028 | 9,647 | 63.1% | 7.14 | 47.0% | $5.56M |
| 2,029 | 9,421 | 66.9% | 7.45 | 49.9% | $6.12M |
| 2,030 | 9,473 | 70.1% | 7.73 | 52.1% | $6.63M |
| 2,031 | 9,555 | 73.8% | 8.03 | 54.8% | $7.07M |
| 2,032 | 9,581 | 76.9% | 8.31 | 57.1% | $7.56M |
| 2,033 | 9,540 | 80.2% | 8.58 | 59.4% | $8.21M |
| 2,034 | 9,617 | 83.4% | 8.85 | 61.6% | $8.64M |
| 2,035 | 9,313 | 85.8% | 9.08 | 63.5% | $8.87M |

## Drivers and Barriers

The dataset has no explicit survey fields for adoption drivers or barriers. The items below are inferred from numeric relationships and low-performing segments.

| metric | correlation_with_adoption |
| --- | --- |
| productivity_gain | 0.953 |
| ai_maturity_score | 0.943 |
| employee_ai_training_hours | 0.933 |
| automation_rate | 0.931 |
| deployment_count | 0.897 |
| roi_proxy | 0.537 |
| cost_savings | 0.511 |
| ai_investment_usd | 0.501 |
| total_financial_impact | 0.500 |
| revenue_impact | 0.434 |

Likely adoption drivers supported by the data:

- Higher productivity gains.
- Higher AI maturity scores.
- More employee AI training hours.
- Higher automation rates.
- More AI deployments.

Likely barriers inferred from the data:

- Lower training intensity.
- Lower automation readiness.
- Fewer deployments and lower maturity.
- Financial uncertainty, shown by records with negative revenue impact.

## Future AI Readiness by Industry

| industry | future_readiness_score | avg_adoption | avg_maturity | avg_productivity_gain | avg_roi_proxy |
| --- | --- | --- | --- | --- | --- |
| Energy | 90.62 | 53.2% | 6.30 | 42.7% | 0.68 |
| Agriculture | 73.97 | 53.0% | 6.29 | 40.6% | 0.58 |
| Financial Services | 72.08 | 52.9% | 6.28 | 40.6% | 0.79 |
| Manufacturing | 68.58 | 52.8% | 6.28 | 44.2% | 0.64 |
| Healthcare | 63.98 | 52.9% | 6.28 | 34.9% | 0.66 |
| Retail | 61.06 | 52.8% | 6.27 | 36.8% | 0.83 |
| Logistics | 60.99 | 52.7% | 6.26 | 43.3% | 0.72 |
| Telecom | 52.05 | 52.7% | 6.27 | 38.5% | 0.77 |
| Technology | 47.26 | 52.6% | 6.25 | 38.5% | 1.31 |
| Education | 0.00 | 52.1% | 6.22 | 30.7% | 0.48 |

## Outlier Review

| column | outlier_count | outlier_pct |
| --- | --- | --- |
| revenue_impact | 15,869 | 7.9% |
| total_financial_impact | 14,297 | 7.1% |
| cost_savings | 13,386 | 6.7% |
| impact_per_deployment | 12,861 | 6.4% |
| roi_proxy | 9,059 | 4.5% |
| ai_investment_usd | 7,476 | 3.7% |
| investment_per_deployment | 7,097 | 3.5% |
| employee_ai_training_hours | 6 | 0.0% |
| ai_adoption_level | 0 | 0.0% |
| automation_rate | 0 | 0.0% |
| productivity_gain | 0 | 0.0% |
| ai_maturity_score | 0 | 0.0% |

## Business Implications

- AI maturity is strongly linked with adoption and value creation.
- Employee training appears central to scaling AI adoption.
- Deployment scale matters: broader deployment footprints show much higher adoption maturity.
- Financial outcomes vary, so cost savings and revenue impact should be tracked separately.
- Regional and industry differences make peer benchmarking more useful than universal targets.

## Recommendations

- Build a practical AI maturity roadmap from pilots to scaled deployments.
- Pair AI investments with employee training and change-management programs.
- Track AI ROI using cost savings, revenue impact, productivity gain, and deployment count.
- Investigate negative revenue-impact cases to identify implementation or measurement issues.
- Benchmark adoption by industry and region before setting targets.

## Dataset Limitations

- No direct company-size column exists; company_scale_proxy is based on deployment count.
- No explicit barrier or driver survey fields exist; barriers are inferred from available metrics.
- Future years through 2035 should be interpreted as projected/modelled observations.
- Company IDs repeat across records, so the dataset appears panel-like rather than one row per company.
- Correlation does not prove causation.
- The dataset source file is local, so this project references the Kaggle dataset provided in the project folder rather than a specific URL.
