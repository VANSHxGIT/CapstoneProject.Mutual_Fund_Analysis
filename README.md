# ETL.BlueStock
An end-to-end Mutual Fund Analytics project featuring ETL pipelines, API integration, SQL analysis, and interactive Power BI dashboards for investment insights.
# 📊 Mutual Fund Analytics

An end-to-end Mutual Fund Analytics platform that automates data ingestion, validation, analysis, and visualization using Python, SQL, APIs, and Power BI. The project combines historical mutual fund datasets with live NAV data to generate meaningful investment insights through interactive dashboards.

---

##  Project Overview

The objective of this project is to build a complete data analytics pipeline for mutual funds by:

- Ingesting and validating historical mutual fund datasets
- Fetching live NAV (Net Asset Value) data using the MFAPI API
- Performing data cleaning and quality checks
- Storing and querying data using SQL
- Building interactive Power BI dashboards
- Generating actionable investment insights

---

##  Project Architecture

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

##  Project Structure

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

##  Technologies Used

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

##  Features

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

##  Key Performance Indicators (KPIs)

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

##  Project Roadmap

###  Phase 1 – Data Engineering

- Project setup
- Data ingestion
- API integration
- Data validation
- Data quality report

###  Phase 2 – Database

- Database schema
- SQL table creation
- Data loading
- Query optimization

###  Phase 3 – Analytics

- Exploratory Data Analysis
- Performance comparison
- Risk analysis
- Business insights

###  Phase 4 – Dashboard

- Power BI dashboard
- KPI cards
- Interactive filters
- Trend analysis
- Report generation

---

##  Installation

Clone the repository

```bash
git clone https://github.com/your-username/MutualFundAnalytics.git
```

Move into the project directory

```bash
cd MutualFundAnalytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Usage

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

##  Future Improvements

- Machine Learning-based fund performance prediction
- Automated ETL scheduling
- Streamlit web dashboard
- Portfolio recommendation system
- Real-time market alerts
- Cloud deployment (AWS/Azure)

---

##  Team

- Vansh Rawat
- Alam Sarfaraz
- Riya Raghav

---

##  License

This project was developed as part of an internship/capstone program for educational purposes.

---

##  Acknowledgements

- MFAPI for providing mutual fund NAV data
- Pandas Community
- Power BI
- Python Open Source Community

---

**If you find this project useful, consider giving it a ⭐ on GitHub!**
