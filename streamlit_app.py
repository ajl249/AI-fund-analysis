# stock_analysis_app.py

import yfinance as yf
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px

def main():
    # Set Streamlit page configuration to wide layout
    st.set_page_config(
        page_title="University of Exeter AI Fund Stock Analysis",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Set Seaborn style
    sns.set(style="darkgrid")

    # Set the title of the app
    st.title("University of Exeter AI Fund Stock Analysis")

    # Sidebar for user input
    st.sidebar.header("Input Options")
    ticker_symbol = st.sidebar.text_input("Enter the stock ticker symbol:", value='AAPL').upper()

    st.sidebar.markdown("""
    ---
    **Instructions:**
    - Enter the stock ticker symbol (e.g., AAPL for Apple Inc.).
    - The app will display financial metrics, evaluations, and visualizations.
    """)

    # Display the currently selected ticker
    st.sidebar.markdown(f"**Currently Selected:** {ticker_symbol}")

    st.divider()

    # Download the stock data
    stock = yf.Ticker(ticker_symbol)

    # Get key financial metrics
    try:
        info = stock.info
    except Exception as e:
        st.error(f"Error fetching data for {ticker_symbol}: {e}")
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
    dividend_yield_percentage = round(dividend_yield * 100, 2) if dividend_yield is not None else None
    roe_percentage = round(roe * 100, 2) if roe is not None else None
    profit_margin_percentage = round(profit_margin * 100, 2) if profit_margin is not None else None

    # Calculate EV/EBITDA Ratio
    if enterprise_value is not None and ebitda is not None and ebitda != 0:
        ev_ebitda_ratio = round(enterprise_value / ebitda, 2)
    else:
        ev_ebitda_ratio = None

    # Fetch industry and sector
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')

    # Placeholder for industry averages (In a real scenario, you would fetch this data from a financial API)
    # For this example, let's assume some industry average PE ratios
    industry_pe_ratio = get_industry_pe_ratio(industry)

    # Prepare data for table without forcing two decimal places
    metrics = {
        'Metric': [
            'Current Price ($)',
            'PE Ratio',
            'Forward PE',
            'PEG Ratio',
            'Price-to-Book Ratio',
            'Price-to-Sales Ratio',
            'EV/EBITDA Ratio',
            'Dividend Yield (%)',
            'Return on Equity (%)',
            'Earnings Per Share ($)',
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
    st.dataframe(
        df_metrics.set_index('Metric').style
        .hide(axis="index")  # Correct method to hide index
    )

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

    st.info("Disclaimer: This evaluation is based on basic financial metrics and should not be considered as financial advice. Please conduct your own research or consult with a financial advisor before making investment decisions.")

    # --- Data Visualization ---

    # Fetch historical market data (past 1 year) and reset index to include 'Date' as a column
    stock_hist = stock.history(period="1y").reset_index()

    if stock_hist.empty:
        st.warning("No historical data available to plot.")
        return

    # Layout using columns
    col1, col2 = st.columns(2)

    with col1:
        # Interactive Price Chart with Plotly
        st.subheader("Historical Stock Price")
        fig_price = px.line(
            stock_hist, 
            x='Date', 
            y='Close', 
            title=f'{ticker_symbol} Closing Price Over the Last Year',
            labels={'Close': 'Closing Price ($)', 'Date': 'Date'}
        )
        fig_price.update_layout(xaxis_title='Date', yaxis_title='Closing Price ($)')
        st.plotly_chart(fig_price, use_container_width=True)

    with col2:
        # Moving Averages
        stock_hist['MA50'] = stock_hist['Close'].rolling(window=50).mean()
        stock_hist['MA200'] = stock_hist['Close'].rolling(window=200).mean()

        st.subheader("Closing Price with Moving Averages")
        fig_ma = px.line(
            stock_hist, 
            x='Date', 
            y=['Close', 'MA50', 'MA200'],
            title=f"{ticker_symbol} Closing Price with 50-Day and 200-Day Moving Averages",
            labels={'value': 'Price ($)', 'Date': 'Date'},
            hover_data={'Date': '|%B %d, %Y'}
        )
        fig_ma.update_layout(xaxis_title='Date', yaxis_title='Price ($)')
        st.plotly_chart(fig_ma, use_container_width=True)

    # Trading Volume
    st.subheader("Trading Volume")
    fig_volume = px.bar(
        stock_hist, 
        x='Date', 
        y='Volume', 
        title=f'{ticker_symbol} Trading Volume Over the Last Year',
        labels={'Volume': 'Volume', 'Date': 'Date'}
    )
    fig_volume.update_layout(xaxis_title='Date', yaxis_title='Volume')
    st.plotly_chart(fig_volume, use_container_width=True)

    # Additional Visualizations: Revenue and Net Income Trends
    st.header("Revenue and Net Income Trends")
    try:
        # Fetch quarterly data for better trend visualization
        quarterly_financials = stock.quarterly_financials.T
        if quarterly_financials.empty:
            st.warning("Quarterly financial data is not available.")
        else:
            if 'Total Revenue' in quarterly_financials.columns and 'Net Income' in quarterly_financials.columns:
                quarterly_financials = quarterly_financials[['Total Revenue', 'Net Income']].dropna()
                quarterly_financials = quarterly_financials.reset_index()

                fig_financials = px.bar(
                    quarterly_financials, 
                    x='index', 
                    y=['Total Revenue', 'Net Income'],
                    barmode='group',
                    title=f'{ticker_symbol} Quarterly Revenue and Net Income',
                    labels={'index': 'Quarter', 'value': 'Amount ($)'},
                    hover_data={'index': '|%B %d, %Y'}
                )
                fig_financials.update_layout(xaxis_title='Quarter', yaxis_title='Amount ($)')
                st.plotly_chart(fig_financials, use_container_width=True)
            else:
                st.warning("Required financial metrics are not available for quarterly trends.")
    except Exception as e:
        st.warning("Financial trends data is not available.")

def get_industry_pe_ratio(industry):
    # Placeholder function to get industry average PE ratio
    # In a real application, fetch this data from a financial API or database
    industry_pe_ratios = {
        'Information Technology Services': 25,
        'Consumer Electronics': 20,
        'Software—Application': 30,
        'Financial Services': 15,
        'Healthcare': 22,
        'Energy': 18,
        'Retail': 18,
        # Add more industries and their average PE ratios as needed
    }
    return industry_pe_ratios.get(industry, None)

if __name__ == "__main__":
    main()