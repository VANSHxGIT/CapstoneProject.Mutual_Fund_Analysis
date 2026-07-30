-- ==========================================
-- EXECUTIVE KPI QUERIES
-- ==========================================

-- 1. Total Number of Schemes
SELECT COUNT(*) AS total_schemes
FROM fund_metadata;

-- 2. Total Fund Houses
SELECT COUNT(DISTINCT fund_house) AS total_fund_houses
FROM fund_metadata;

-- 3. Total Investors
SELECT COUNT(DISTINCT investor_id) AS total_investors
FROM investor_transactions;

-- 4. Total Transactions
SELECT COUNT(*) AS total_transactions
FROM investor_transactions;

-- 5. Total Investment Amount
SELECT SUM(amount_inr) AS total_investment
FROM investor_transactions;

-- ==========================================
-- FUND ANALYSIS
-- ==========================================

-- Schemes by Fund House
SELECT
    fund_house,
    COUNT(*) AS total_schemes
FROM fund_metadata
GROUP BY fund_house
ORDER BY total_schemes DESC;

-- Schemes by Category
SELECT
    scheme_category,
    COUNT(*) AS total_schemes
FROM fund_metadata
GROUP BY scheme_category
ORDER BY total_schemes DESC;

-- Schemes by Type
SELECT
    scheme_type,
    COUNT(*) AS total_schemes
FROM fund_metadata
GROUP BY scheme_type;

-- ==========================================
-- NAV ANALYSIS
-- ==========================================

-- Latest NAV Date
SELECT MAX(date) AS latest_date
FROM nav_history;

-- Highest NAV
SELECT
    scheme_code,
    MAX(nav) AS highest_nav
FROM nav_history
GROUP BY scheme_code
ORDER BY highest_nav DESC;

-- Average NAV
SELECT
    scheme_code,
    AVG(nav) AS average_nav
FROM nav_history
GROUP BY scheme_code
ORDER BY average_nav DESC;

-- NAV History
SELECT
    date,
    scheme_code,
    nav
FROM nav_history
ORDER BY date;

-- ==========================================
-- AUM ANALYSIS
-- ==========================================

-- Latest AUM by Fund House
SELECT
    fund_house,
    MAX(aum_crore) AS latest_aum
FROM aum_by_fund_house
GROUP BY fund_house
ORDER BY latest_aum DESC;

-- Number of Schemes per Fund House
SELECT
    fund_house,
    MAX(num_schemes) AS schemes
FROM aum_by_fund_house
GROUP BY fund_house
ORDER BY schemes DESC;

-- ==========================================
-- SIP ANALYSIS
-- ==========================================

SELECT
    month,
    sip_inflow_crore
FROM monthly_sip_inflows
ORDER BY month;

SELECT
    month,
    yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;

SELECT
    month,
    active_sip_accounts_crore
FROM monthly_sip_inflows;

-- ==========================================
-- CATEGORY INFLOWS
-- ==========================================

SELECT
    category,
    SUM(net_inflow_crore) AS total_inflow
FROM category_inflows
GROUP BY category
ORDER BY total_inflow DESC;

-- ==========================================
-- INVESTOR ANALYTICS
-- ==========================================

-- State-wise Investment
SELECT
    state,
    SUM(amount_inr) AS investment
FROM investor_transactions
GROUP BY state
ORDER BY investment DESC;

-- Gender Distribution
SELECT
    gender,
    COUNT(*) AS investors
FROM investor_transactions
GROUP BY gender;

-- Age Group Distribution
SELECT
    age_group,
    COUNT(*) AS investors
FROM investor_transactions
GROUP BY age_group;

-- Payment Mode
SELECT
    payment_mode,
    COUNT(*) AS transactions
FROM investor_transactions
GROUP BY payment_mode;

-- KYC Status
SELECT
    kyc_status,
    COUNT(*) AS investors
FROM investor_transactions
GROUP BY kyc_status;

-- ==========================================
-- PORTFOLIO ANALYSIS
-- ==========================================

-- Top Holdings
SELECT
    stock_name,
    SUM(weight_pct) AS weight
FROM portfolio_holdings
GROUP BY stock_name
ORDER BY weight DESC
LIMIT 15;

-- Sector Allocation
SELECT
    sector,
    SUM(weight_pct) AS weight
FROM portfolio_holdings
GROUP BY sector
ORDER BY weight DESC;

-- ==========================================
-- BENCHMARK ANALYSIS
-- ==========================================

-- Latest Close Value
SELECT
    index_name,
    MAX(close_value) AS latest_close
FROM benchmark_indices
GROUP BY index_name;

-- Benchmark Trend
SELECT
    date,
    index_name,
    close_value
FROM benchmark_indices
ORDER BY date;

