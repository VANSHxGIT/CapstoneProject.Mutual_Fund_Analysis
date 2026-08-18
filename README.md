# ETL.BlueStock

An end-to-end Mutual Fund Analytics project featuring ETL pipelines, API integration, SQL analysis, and interactive Power BI dashboards for investment insights.

# 📊 Mutual Fund Analytics

An end-to-end Mutual Fund Analytics platform that automates data ingestion, validation, analysis, and visualization using Python, SQL, APIs, and Power BI. The project combines historical mutual fund datasets with live NAV data to generate meaningful investment insights through interactive dashboards.

---

## Project Overview

The objective of this project is to build a complete data analytics pipeline for mutual funds by:

- Ingesting and validating historical mutual fund datasets
- Fetching live NAV (Net Asset Value) data using the MFAPI API
- Performing data cleaning and quality checks
- Storing and querying data using SQL
- Building interactive Power BI dashboards
- Generating actionable investment insights

---

## Final deliverables

- `notebooks/EDA_Analysis.ipynb` — exploratory analysis
- `notebooks/Performance_Analytics.ipynb` — returns, CAGR, Sharpe, Sortino, Alpha/Beta and drawdown analysis
- `notebooks/Advanced_Analytics.ipynb` — VaR/CVaR, rolling Sharpe, investor cohorts, SIP continuity, recommender and sector HHI
- `reports/var_cvar_report.csv` — historical VaR/CVaR for 34 schemes
- `reports/alpha_beta.csv` — benchmark regression results for schemes with overlapping benchmark observations
- `reports/sector_hhi_report.csv` — sector concentration analysis
- `reports/sip_continuity_analysis.csv` — 6+ SIP transaction continuity analysis
- `Dashboard/Mutual Fund Analysis.pbix` — Power BI dashboard
- `reports/Final_Report.pdf` — final project report
- `reports/Bluestock_MF_Presentation.pptx` — 12-slide presentation

## Architecture

Historical CSVs → Python ingestion → cleaning/validation → live NAV API → processed datasets → SQLite → notebooks/analytics → Power BI dashboard → final report.

## Project structure

```text
Mutual Fund Analytics/
├── Data/
│   ├── Raw/
│   ├── Processed/
│   └── reports/
├── SQL/
│   ├── schema.sql
│   ├── queries.sql
│   └── mutual_fund.db
├── notebooks/
├── scripts/
├── Dashboard/
└── reports/
```

## Setup

1. Create a Python 3 environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the complete ETL with `python scripts/run_pipeline.py`.
4. Open the notebooks in Jupyter and execute them in order as required.
5. Open `Dashboard/Mutual Fund Analysis.pbix` in Power BI Desktop.

## ETL

The master pipeline runs ingestion, live NAV fetching, preprocessing, validation and SQLite loading in sequence. It uses `pathlib.Path` for project-relative paths and exits with a non-zero status when a stage fails.

## Data notes

The analytical NAV universe contains 34 schemes with usable NAV observations. The metadata contains one additional scheme without usable NAV observations; it is retained in metadata but excluded from NAV-based calculations.

## Dashboard

The PBIX contains four pages: Executive Overview, Fund Performance, Investor Analysis, and Portfolio & Market. The report layout includes interactive slicers on the relevant pages.

## Git

Final release tag: `v1.0` (create locally with `git tag v1.0`; push with `git push origin v1.0`).

## Project Architecture

```
                 Historical CSV Files
                         │
                         ▼
                Data Ingestion (Python)
                         │
                         ▼
                 Data Cleaning & Validation
                         │
                         ▼
               Live NAV API Integration
                         │
                         ▼
                    Processed Dataset
                         │
                         ▼
                    SQL Database
                         │
                         ▼
                Data Analysis & KPIs
                         │
                         ▼
               Power BI Interactive Dashboard
```

---

## Project Structure

```
MutualFundAnalytics/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── live_nav/
│
├── scripts/
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── data_validation.py
│   └── utils.py
│
├── sql/
│   ├── create_tables.sql
│   ├── analysis_queries.sql
│   └── load_data.sql
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   └── 02_Analysis.ipynb
│
├── dashboard/
│   └── MutualFundAnalytics.pbix
│
├── reports/
│   ├── Data_Quality_Report.md
│   └── Final_Report.pdf
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies Used

### Programming

- Python 3.x

### Libraries

- Pandas
- NumPy
- Requests
- SQLAlchemy
- Matplotlib
- Seaborn
- Plotly
- SciPy
- Jupyter Notebook

### Database

- SQL (MySQL/PostgreSQL/SQLite)

### Visualization

- Power BI

### Version Control

- Git
- GitHub

---

## Features

- Historical mutual fund data ingestion
- Live NAV fetching through MFAPI
- Data quality validation
- Missing value detection
- Duplicate detection
- Data type validation
- Exploratory Data Analysis (EDA)
- SQL-based analytics
- Interactive Power BI dashboards
- Business insights and reporting

---

## Key Performance Indicators (KPIs)

- Total Mutual Funds
- Total Fund Houses
- Fund Categories
- Average NAV
- Highest Performing Funds
- Lowest Performing Funds
- Category-wise Performance
- Risk Distribution
- NAV Trends
- Top Investment Schemes

---

## Project Roadmap

### Phase 1 – Data Engineering

- Project setup
- Data ingestion
- API integration
- Data validation
- Data quality report

### Phase 2 – Database

- Database schema
- SQL table creation
- Data loading
- Query optimization

### Phase 3 – Analytics

- Exploratory Data Analysis
- Performance comparison
- Risk analysis
- Business insights

### Phase 4 – Dashboard

- Power BI dashboard
- KPI cards
- Interactive filters
- Trend analysis
- Report generation

---

## Installation

Clone the repository

```bash
git clone https://github.com/VANSHxGIT/CapstoneProject.Mutual_Fund_Analysis
```

Move into the project directory

```bash
cd CapstoneProject.Mutual_Fund_Analysis
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run data ingestion

```bash
python scripts/data_ingestion.py
```

Fetch live NAV data

```bash
python scripts/live_nav_fetch.py
```

Perform data validation

```bash
python scripts/data_validation.py
```

---

## Future Improvements

- Machine Learning-based fund performance prediction
- Automated ETL scheduling
- Streamlit web dashboard
- Portfolio recommendation system
- Real-time market alerts
- Cloud deployment (AWS/Azure)

---

## Team

- Vansh Rawat
- Alam Sarfaraz
- Riya Raghav

---

## License

This project was developed as part of an internship/capstone program for educational purposes.

---

## Acknowledgements

- MFAPI for providing mutual fund NAV data
- Pandas Community
- Power BI
- Python Open Source Community

---

**If you find this project useful, consider giving it a ⭐ on GitHub!**
