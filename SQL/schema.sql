-- ==========================================================
-- Mutual Fund Analytics Database Schema
-- ==========================================================

DROP TABLE IF EXISTS fund_master;
DROP TABLE IF EXISTS nav_history;
DROP TABLE IF EXISTS aum_by_fund_house;
DROP TABLE IF EXISTS monthly_sip_inflows;
DROP TABLE IF EXISTS category_inflows;
DROP TABLE IF EXISTS industry_folio_count;
DROP TABLE IF EXISTS scheme_performance;
DROP TABLE IF EXISTS investor_transactions;
DROP TABLE IF EXISTS portfolio_holdings;
DROP TABLE IF EXISTS benchmark_indices;

--------------------------------------------------------------
-- 1. Fund Master
--------------------------------------------------------------

CREATE TABLE fund_master (

    amfi_code INTEGER PRIMARY KEY,

    scheme_name TEXT,

    fund_house TEXT,

    category TEXT,

    sub_category TEXT,

    benchmark TEXT,

    expense_ratio_pct REAL,

    fund_manager TEXT,

    risk_category TEXT

);

--------------------------------------------------------------
-- 2. NAV History
--------------------------------------------------------------

CREATE TABLE nav_history (

    amfi_code INTEGER,

    date DATE,

    nav REAL,

    FOREIGN KEY(amfi_code)
        REFERENCES fund_master(amfi_code)

);

--------------------------------------------------------------
-- 3. AUM
--------------------------------------------------------------

CREATE TABLE aum_by_fund_house (

    date DATE,

    fund_house TEXT,

    aum_lakh_crore REAL,

    aum_crore REAL,

    num_schemes INTEGER

);

--------------------------------------------------------------
-- 4. SIP
--------------------------------------------------------------

CREATE TABLE monthly_sip_inflows (

    month DATE,

    sip_inflow REAL,

    active_sip_accounts INTEGER,

    sip_aum REAL,

    yoy_growth REAL

);

--------------------------------------------------------------
-- 5. Category Inflows
--------------------------------------------------------------

CREATE TABLE category_inflows (

    month DATE,

    category TEXT,

    net_inflow REAL

);

--------------------------------------------------------------
-- 6. Industry Folios
--------------------------------------------------------------

CREATE TABLE industry_folio_count (

    date DATE,

    equity INTEGER,

    debt INTEGER,

    hybrid INTEGER,

    others INTEGER,

    total INTEGER

);

--------------------------------------------------------------
-- 7. Scheme Performance
--------------------------------------------------------------

CREATE TABLE scheme_performance (

    amfi_code INTEGER,

    return_1y REAL,

    return_3y REAL,

    return_5y REAL,

    alpha REAL,

    beta REAL,

    sharpe_ratio REAL,

    sortino_ratio REAL,

    FOREIGN KEY(amfi_code)
        REFERENCES fund_master(amfi_code)

);

--------------------------------------------------------------
-- 8. Investor Transactions
--------------------------------------------------------------

CREATE TABLE investor_transactions (

    investor_id INTEGER,

    amfi_code INTEGER,

    transaction_date DATE,

    amount REAL,

    payment_mode TEXT,

    city TEXT,

    state TEXT,

    FOREIGN KEY(amfi_code)
        REFERENCES fund_master(amfi_code)

);

--------------------------------------------------------------
-- 9. Portfolio Holdings
--------------------------------------------------------------

CREATE TABLE portfolio_holdings (

    amfi_code INTEGER,

    stock_name TEXT,

    sector TEXT,

    weight REAL,

    market_value REAL,

    FOREIGN KEY(amfi_code)
        REFERENCES fund_master(amfi_code)

);

--------------------------------------------------------------
-- 10. Benchmark
--------------------------------------------------------------

CREATE TABLE benchmark_indices (

    date DATE,

    index_name TEXT,

    close_value REAL

);