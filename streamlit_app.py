# stock_analysis_app.py

import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px

def main():
    # Set Seaborn style
    sns.set(style="darkgrid")

    # Set the title of the app
    st.title("University of Exeter AI Fund Stock Analysis")

    # Sidebar for user input
    st.sidebar.header("Input Options")
    ticker_symbol = st.sidebar.text_input("Enter the stock ticker symbol:", value='AAPL').upper()

    # Download the stock data
    stock = yf.Ticker(ticker_symbol)

    # Get key financial metrics
    try:
        info = stock.info
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    # Extract financial metrics with default values
    current_price = info.get('currentPrice', None)
    pe_ratio = info.get('trailingPE', None)
    forward_pe = info.get('forwardPE', None)
    peg_ratio = info.get('pegRatio', None)
    pb_ratio = info.get('priceToBook', None)
    ps_ratio = info.get('priceToSalesTrailing12Months', None)
    dividend_yield = info.get('dividendYield', None)
    roe = info.get('returnOnEquity', None)
    eps = info.get('trailingEps', None)
    debt_to_equity = info.get('debtToEquity', None)
    profit_margin = info.get('profitMargins', None)
    beta = info.get('beta', None)
    enterprise_value = info.get('enterpriseValue', None)
    ebitda = info.get('ebitda', None)

    # Convert percentages
    if dividend_yield is not None:
        dividend_yield_percentage = dividend_yield * 100
    else:
        dividend_yield_percentage = None

    if roe is not None:
        roe_percentage = roe * 100
    else:
        roe_percentage = None

    if profit_margin is not None:
        profit_margin_percentage = profit_margin * 100
    else:
        profit_margin_percentage = None

    # Calculate EV/EBITDA Ratio
    if enterprise_value is not None and ebitda is not None and ebitda != 0:
        ev_ebitda_ratio = enterprise_value / ebitda
    else:
        ev_ebitda_ratio = None

    # Fetch industry and sector
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')

    # Placeholder for industry averages (In a real scenario, you would fetch this data from a financial API)
    # For this example, let's assume some industry average PE ratios
    industry_pe_ratio = get_industry_pe_ratio(industry)

    # Prepare data for table
    metrics = {
        'Metric': [
            'Current Price',
            'PE Ratio',
            'Forward PE',
            'PEG Ratio',
            'Price-to-Book Ratio',
            'Price-to-Sales Ratio',
            'EV/EBITDA Ratio',
            'Dividend Yield (%)',
            'Return on Equity (%)',
            'Earnings Per Share',
            'Debt-to-Equity Ratio',
            'Profit Margin (%)',
            'Beta',
            'Sector',
            'Industry'
        ],
        'Value': [
            current_price,
            pe_ratio,
            forward_pe,
            peg_ratio,
            pb_ratio,
            ps_ratio,
            ev_ebitda_ratio,
            dividend_yield_percentage,
            roe_percentage,
            eps,
            debt_to_equity,
            profit_margin_percentage,
            beta,
            sector,
            industry
        ]
    }

    df_metrics = pd.DataFrame(metrics)

    # Evaluation Functions (updated)
    def evaluate_pe_ratio(pe, industry_pe):
        if pe is None or industry_pe is None:
            return ("PE ratio is not available for comparison.", 0)
        elif pe < industry_pe:
            return ("Undervalued compared to industry average PE ratio.", 1)
        elif pe == industry_pe:
            return ("PE ratio is equal to industry average.", 0)
        else:
            return ("Overvalued compared to industry average PE ratio.", -1)

    def evaluate_roe(roe_value):
        if roe_value is None:
            return ("Return on Equity is not available.", 0)
        elif roe_value > 15:
            return ("High Return on Equity.", 1)
        elif 10 <= roe_value <= 15:
            return ("Moderate Return on Equity.", 0)
        else:
            return ("Low Return on Equity.", -1)

    def evaluate_debt_to_equity(de_ratio):
        if de_ratio is None:
            return ("Debt-to-Equity ratio is not available.", 0)
        elif de_ratio < 1:
            return ("Low Debt-to-Equity ratio.", 1)
        elif 1 <= de_ratio <= 2:
            return ("Moderate Debt-to-Equity ratio.", 0)
        else:
            return ("High Debt-to-Equity ratio.", -1)

    def evaluate_profit_margin(pm):
        if pm is None:
            return ("Profit Margin is not available.", 0)
        elif pm > 20:
            return ("High Profit Margin.", 1)
        elif 10 <= pm <= 20:
            return ("Moderate Profit Margin.", 0)
        else:
            return ("Low Profit Margin.", -1)

    def evaluate_ev_ebitda(ev_ebitda):
        if ev_ebitda is None:
            return ("EV/EBITDA ratio is not available.", 0)
        elif ev_ebitda < 10:
            return ("Potentially undervalued based on EV/EBITDA.", 1)
        elif 10 <= ev_ebitda <= 14:
            return ("Fairly valued based on EV/EBITDA.", 0)
        else:
            return ("Potentially overvalued based on EV/EBITDA.", -1)

    # Evaluate the metrics
    pe_message, pe_score = evaluate_pe_ratio(pe_ratio, industry_pe_ratio)
    roe_message, roe_score = evaluate_roe(roe_percentage)
    de_message, de_score = evaluate_debt_to_equity(debt_to_equity)
    pm_message, pm_score = evaluate_profit_margin(profit_margin_percentage)
    ev_message, ev_score = evaluate_ev_ebitda(ev_ebitda_ratio)

    # Sum the scores
    total_score = pe_score + roe_score + de_score + pm_score + ev_score

    # Determine overall valuation
    if total_score >= 3:
        overall_evaluation = "The stock appears to be **undervalued**."
    elif -2 <= total_score <= 2:
        overall_evaluation = "The stock appears to be **fairly valued**."
    else:
        overall_evaluation = "The stock appears to be **overvalued**."

    # Display the metrics in a table
    st.header(f"Financial Metrics for {ticker_symbol}")
    st.table(df_metrics.set_index('Metric'))

    # Display evaluations in a table
    evaluations = {
        'Metric': [
            'PE Ratio',
            'Return on Equity',
            'Debt-to-Equity',
            'Profit Margin',
            'EV/EBITDA Ratio'
        ],
        'Evaluation': [
            pe_message,
            roe_message,
            de_message,
            pm_message,
            ev_message
        ],
    }
    df_evaluations = pd.DataFrame(evaluations)
    st.header("Evaluations")
    st.table(df_evaluations.set_index('Metric'))

    st.header("Overall Evaluation")
    st.markdown(f"### {overall_evaluation}")

    st.info("Disclaimer: This evaluation is based on basic financial metrics and should not be considered as financial advice. Please conduct your own research advisor before making investment decisions.")

    # --- Data Visualization ---

    # Fetch historical market data (past 1 year)
    stock_hist = stock.history(period="1y")

    if stock_hist.empty:
        st.warning("No historical data available to plot.")
        return

    # Interactive Price Chart
    st.header("Historical Stock Price")
    fig = px.line(stock_hist, x=stock_hist.index, y='Close', title=f'{ticker_symbol} Closing Price Over the Last Year')
    st.plotly_chart(fig)

    # Revenue and Earnings (using Yahoo Financials API)
    st.header("Financial Statements")
    try:
        income_stmt = stock.financials
        income_stmt = income_stmt.T  # Transpose for readability
        st.subheader("Income Statement")
        st.dataframe(income_stmt)
    except Exception as e:
        st.warning("Income statement data is not available.")

    # Cash Flow Statement
    try:
        cashflow_stmt = stock.cashflow
        cashflow_stmt = cashflow_stmt.T
        st.subheader("Cash Flow Statement")
        st.dataframe(cashflow_stmt)
    except Exception as e:
        st.warning("Cash flow statement data is not available.")

    # Balance Sheet
    try:
        balance_sheet = stock.balance_sheet
        balance_sheet = balance_sheet.T
        st.subheader("Balance Sheet")
        st.dataframe(balance_sheet)
    except Exception as e:
        st.warning("Balance sheet data is not available.")

def get_industry_pe_ratio(industry):
    # Placeholder function to get industry average PE ratio
    # In a real application, fetch this data from a financial API or database
    industry_pe_ratios = {
        'Information Technology Services': 25,
        'Consumer Electronics': 20,
        'Software—Application': 30,
        # Add more industries and their average PE ratios
    }
    return industry_pe_ratios.get(industry, None)

if __name__ == "__main__":
    main()