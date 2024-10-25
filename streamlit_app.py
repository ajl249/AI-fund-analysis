# main.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

from finance_data import get_stock_data
from evaluations import evaluate_metrics
from explanations import metric_explanations

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

    # Display the currently selected ticker
    st.sidebar.markdown(f"**Currently Selected:** {ticker_symbol}")

    st.sidebar.markdown("""
    ---
    **Instructions:**
    - Enter the stock ticker symbol (e.g., AAPL for Apple Inc.).
    - The app will display financial metrics, evaluations, and visualizations.
    """)

    # List of 20 Publicly Traded AI Stocks as Examples
    st.sidebar.markdown("""
    ---
    ### **AI Stocks Examples:**
    - **NVIDIA Corporation (NVDA)**
    - **Alphabet Inc. (GOOGL)**
    - **Microsoft Corporation (MSFT)**
    - **Amazon.com, Inc. (AMZN)**
    - **International Business Machines Corporation (IBM)**
    - **Tesla, Inc. (TSLA)**
    - **Meta Platforms, Inc. (META)**
    - **Baidu, Inc. (BIDU)**
    - **Advanced Micro Devices, Inc. (AMD)**
    - **Salesforce.com, Inc. (CRM)**
    - **Intel Corporation (INTC)**
    - **Oracle Corporation (ORCL)**
    - **Twilio Inc. (TWLO)**
    - **Palantir Technologies Inc. (PLTR)**
    - **C3.ai, Inc. (AI)**
    - **UiPath Inc. (PATH)**
    - **Veritone, Inc. (VERI)**
    - **Cognex Corporation (CGNX)**
    - **Nuance Communications, Inc. (NUAN)**
    """)

    

    st.divider()

    # Fetch stock data
    try:
        stock, metrics, sector, industry = get_stock_data(ticker_symbol)
    except Exception as e:
        st.error(str(e))
        return

    # Separate Numerical and Categorical Metrics
    numerical_metrics = {
        'Metric': [
            'Current Price ($)',
            'PE Ratio',
            'PEG Ratio',             # Added PEG Ratio
            'Price-to-Sales Ratio',  # Moved PS Ratio to third position
            'Forward PE',
            'Price-to-Book Ratio',
            'EV/EBITDA Ratio',
            'Dividend Yield (%)',
            'Return on Equity (%)',
            'Earnings Per Share ($)',
            'Debt-to-Equity Ratio',
            'Profit Margin (%)',
            'Beta'
        ],
        'Value': [
            metrics['Current Price ($)'],
            metrics['PE Ratio'],
            metrics['PEG Ratio'],             # Added PEG Ratio
            metrics['Price-to-Sales Ratio'],  # Moved PS Ratio to third position
            metrics['Forward PE'],
            metrics['Price-to-Book Ratio'],
            metrics['EV/EBITDA Ratio'],
            metrics['Dividend Yield (%)'],
            metrics['Return on Equity (%)'],
            metrics['Earnings Per Share ($)'],
            metrics['Debt-to-Equity Ratio'],
            metrics['Profit Margin (%)'],
            metrics['Beta']
        ]
    }

    categorical_metrics = {
        'Metric': [
            'Sector',
            'Industry'
        ],
        'Value': [
            sector,
            industry
        ]
    }

    df_numerical = pd.DataFrame(numerical_metrics)
    df_categorical = pd.DataFrame(categorical_metrics)

    # Evaluate the metrics
    evaluations_dict, _ = evaluate_metrics(metrics)

    # Layout using columns
    col1, col2 = st.columns(2)

    with col1:
        # Display Numerical Metrics in a DataFrame
        st.header(f"Financial Metrics for {ticker_symbol}")
        st.dataframe(
            df_numerical.set_index('Metric'),
            use_container_width=True  # Widen the table
        )

    with col2:
        # Display Categorical Metrics in a Table
        st.header("Company Classification")
        st.table(
            df_categorical.set_index('Metric')
        )

    # Metrics Explained
    st.header("Metrics Explained")
    metric_list = list(metric_explanations.keys())
    choice = st.selectbox(
        "Select a Metric to Explain",
        metric_list,
    )
    st.write(f"**{choice}:** {metric_explanations[choice]}")

    # Display evaluations in a table with color-coded text
    st.header("Evaluations")

    # Build the markdown table manually
    evaluations = evaluations_dict['Evaluation']
    metrics_list = evaluations_dict['Metric']
    colors = evaluations_dict['Color']

    # Start the markdown table
    table_md = "| Metric | Evaluation |\n|---|---|\n"
    for metric, evaluation, color in zip(metrics_list, evaluations, colors):
        table_md += f"| {metric} | <span style='color:{color}'>{evaluation}</span> |\n"

    st.markdown(table_md, unsafe_allow_html=True)

    # Note: The Final Overall Evaluation section has been removed as per your instruction.

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

    # Note: The Revenue and Net Income Trends section has been removed as per your instruction.

if __name__ == "__main__":
    main()