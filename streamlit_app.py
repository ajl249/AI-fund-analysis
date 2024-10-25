import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def main():
    # Set Seaborn style
    sns.set(style="darkgrid")

    # Set the title of the app
    st.title("University of Exeter AI Fund Stock Analysis")

    # Sidebar for user input
    st.sidebar.header("Input Options")
    ticker_symbol = st.sidebar.text_input("Enter the stock ticker symbol:", value='AAPL').upper()

    # Define S&P 500 ticker symbol
    sp500_symbol = "^GSPC"

    # Download the stock data
    stock = yf.Ticker(ticker_symbol)
    sp500 = yf.Ticker(sp500_symbol)

    # Get key financial metrics
    try:
        info = stock.info
        sp500_info = sp500.info
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    # Extract financial metrics with default values
    current_price = info.get('currentPrice', None)
    pe_ratio = info.get('trailingPE', None)
    forward_pe = info.get('forwardPE', None)
    peg_ratio = info.get('pegRatio', None)
    pb_ratio = info.get('priceToBook', None)
    dividend_yield = info.get('dividendYield', None)
    roe = info.get('returnOnEquity', None)
    eps = info.get('trailingEps', None)
    debt_to_equity = info.get('debtToEquity', None)
    profit_margin = info.get('profitMargins', None)
    free_cash_flow = info.get('freeCashflow', None)
    beta = info.get('beta', None)

    # S&P 500 Metrics
    sp500_pe_ratio = sp500_info.get('trailingPE', None)

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

    # Prepare data for table
    metrics = {
        'Metric': [
            'Current Price',
            'PE Ratio',
            'Forward PE',
            'PEG Ratio',
            'Price-to-Book Ratio',
            'Dividend Yield (%)',
            'Return on Equity (%)',
            'Earnings Per Share',
            'Debt-to-Equity Ratio',
            'Profit Margin (%)',
            'Free Cash Flow',
            'Beta'
        ],
        'Value': [
            current_price,
            pe_ratio,
            forward_pe,
            peg_ratio,
            pb_ratio,
            dividend_yield_percentage,
            roe_percentage,
            eps,
            debt_to_equity,
            profit_margin_percentage,
            free_cash_flow,
            beta
        ]
    }

    df_metrics = pd.DataFrame(metrics)

    # Evaluation Functions (updated)
    def evaluate_pe_ratio(pe, sp_pe):
        if pe is None or sp_pe is None:
            return ("PE ratio is not available for comparison.", 0)
        elif pe < sp_pe:
            return ("Undervalued compared to S&P 500 based on PE ratio.", 1)
        elif pe == sp_pe:
            return ("PE ratio is equal to S&P 500.", 0)
        else:
            return ("Overvalued compared to S&P 500 based on PE ratio.", -1)

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

    # Evaluate the metrics
    pe_message, pe_score = evaluate_pe_ratio(pe_ratio, sp500_pe_ratio)
    roe_message, roe_score = evaluate_roe(roe_percentage)
    de_message, de_score = evaluate_debt_to_equity(debt_to_equity)
    pm_message, pm_score = evaluate_profit_margin(profit_margin_percentage)

    # Sum the scores
    total_score = pe_score + roe_score + de_score + pm_score

    # Determine overall valuation
    if total_score >= 2:
        overall_evaluation = "The stock appears to be **undervalued**."
    elif -1 <= total_score <= 1:
        overall_evaluation = "The stock appears to be **fairly valued**."
    else:
        overall_evaluation = "The stock appears to be **overvalued**."

    # Display the metrics in a table
    st.header(f"Financial Metrics for {ticker_symbol}")
    st.table(df_metrics.set_index('Metric'))

    # Display evaluations in a table
    evaluations = {
        'Metric': ['PE Ratio', 'Return on Equity', 'Debt-to-Equity', 'Profit Margin'],
        'Evaluation': [pe_message, roe_message, de_message, pm_message],
    }
    df_evaluations = pd.DataFrame(evaluations)
    st.header("Evaluations")
    st.table(df_evaluations.set_index('Metric'))

    st.header("Overall Evaluation")
    st.markdown(f"### {overall_evaluation}")

    st.info("Disclaimer: This evaluation is based on basic financial metrics and should not be considered as financial advice. Please conduct your own research or consult with a financial advisor before making investment decisions.")

    # --- Data Visualization ---

    # Fetch historical market data (past 1 year)
    stock_hist = stock.history(period="1y")
    sp500_hist = sp500.history(period="1y")

    if stock_hist.empty or sp500_hist.empty:
        st.warning("No historical data available to plot.")
        return

    # Normalize the prices for comparison
    stock_hist['Normalized'] = stock_hist['Close'] / stock_hist['Close'].iloc[0]
    sp500_hist['Normalized'] = sp500_hist['Close'] / sp500_hist['Close'].iloc[0]

    # Plot comparison of stock vs S&P 500
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(stock_hist.index, stock_hist['Normalized'], label=f"{ticker_symbol} Stock Price")
    ax.plot(sp500_hist.index, sp500_hist['Normalized'], label="S&P 500 Index", linestyle='--')
    ax.set_title(f"{ticker_symbol} vs S&P 500 - Last 1 Year Performance")
    ax.set_ylabel('Normalized Price')
    ax.set_xlabel('Date')
    ax.legend()
    st.pyplot(fig)

    # Additional Visualizations
    # Plot Closing Price and Moving Averages
    stock_hist['MA50'] = stock_hist['Close'].rolling(window=50).mean()
    stock_hist['MA200'] = stock_hist['Close'].rolling(window=200).mean()

    fig2, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(stock_hist.index, stock_hist['Close'], label='Closing Price', color='blue')
    ax1.plot(stock_hist.index, stock_hist['MA50'], label='50-Day MA', color='red', linestyle='--')
    ax1.plot(stock_hist.index, stock_hist['MA200'], label='200-Day MA', color='green', linestyle='--')
    ax1.set_title(f"{ticker_symbol} Stock Price with Moving Averages")
    ax1.set_ylabel('Price ($)')
    ax1.set_xlabel('Date')
    ax1.legend()
    st.pyplot(fig2)

    # Plot Volume
    fig3, ax2 = plt.subplots(figsize=(12, 3))
    ax2.bar(stock_hist.index, stock_hist['Volume'], color='gray')
    ax2.set_title('Trading Volume')
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Date')
    st.pyplot(fig3)

if __name__ == "__main__":
    main()