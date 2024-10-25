# main.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

from finance_data import get_stock_data, get_industry_pe_ratio
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

    st.sidebar.markdown("""
    ---
    **Instructions:**
    - Enter the stock ticker symbol (e.g., AAPL for Apple Inc.).
    - The app will display financial metrics, evaluations, and visualizations.
    """)

    # Display the currently selected ticker
    st.sidebar.markdown(f"**Currently Selected:** {ticker_symbol}")

    st.divider()

    # Fetch stock data
    try:
        stock, metrics, sector, industry = get_stock_data(ticker_symbol)
    except Exception as e:
        st.error(str(e))
        return

    # Fetch industry average PE ratio
    industry_pe_ratio = get_industry_pe_ratio(industry)

    # Prepare data for table
    df_metrics = pd.DataFrame({
        'Metric': list(metrics.keys()),
        'Value': list(metrics.values())
    })

    # Evaluate the metrics
    evaluations_dict, overall_evaluation = evaluate_metrics(metrics, industry_pe_ratio)
    df_evaluations = pd.DataFrame(evaluations_dict).set_index('Metric')

    col1, col2 = st.columns(2)

    with col1:
        # Display the metrics in a table
        st.header(f"Financial Metrics for {ticker_symbol}")
        st.dataframe(
            df_metrics.set_index('Metric')
        )

    with col2:
        # Explanations
        st.header("Metrics Explained")
        metric_list = list(metric_explanations.keys())
        choice = st.selectbox(
            "Select a Metric to Explain",
            metric_list,
        )
        st.write(f"**{choice}:** {metric_explanations[choice]}")

    # Display evaluations in a table
    st.header("Evaluations")
    st.table(df_evaluations)

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


if __name__ == "__main__":
    main()