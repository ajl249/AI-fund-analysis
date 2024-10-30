# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from streamlit_tags import st_tags_sidebar
import plotly.express as px
import yfinance as yf
from io import BytesIO
import xlsxwriter

from finance_data import get_stock_data
from explanations import metric_explanations

# Define color coding functions for each metric
def color_pe_ratio(val):
    if pd.isnull(val):
        return ''
    elif val < 20:
        color = 'green'
    elif 20 <= val <= 25:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_peg_ratio(val):
    if pd.isnull(val):
        return ''
    elif val < 1:
        color = 'green'
    elif 1 <= val <= 1.25:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_ps_ratio(val):
    if pd.isnull(val):
        return ''
    elif val < 1:
        color = 'green'
    elif 1 <= val <= 3:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_roe(val):
    if pd.isnull(val):
        return ''
    elif val > 15:
        color = 'green'
    elif 10 <= val <= 15:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_de_ratio(val):
    if pd.isnull(val):
        return ''
    elif val < 1:
        color = 'green'
    elif 1 <= val <= 2:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_profit_margin(val):
    if pd.isnull(val):
        return ''
    elif val > 20:
        color = 'green'
    elif 10 <= val <= 20:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_ev_ebitda(val):
    if pd.isnull(val):
        return ''
    elif val < 10:
        color = 'green'
    elif 10 <= val <= 14:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_forward_pe(val):
    if pd.isnull(val):
        return ''
    elif val < 20:
        color = 'green'
    elif 20 <= val <= 25:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_pb_ratio(val):
    if pd.isnull(val):
        return ''
    elif val < 1:
        color = 'green'
    elif 1 <= val <= 3:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_dividend_yield(val):
    if pd.isnull(val):
        return ''
    elif val > 3:
        color = 'green'
    elif 1 <= val <= 3:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_eps(val):
    if pd.isnull(val):
        return ''
    elif val > 0:
        color = 'green'
    else:
        color = 'red'
    return f'background-color: {color}'

def color_beta(val):
    if pd.isnull(val):
        return ''
    elif val < 1:
        color = 'green'
    elif 1 <= val <= 1.5:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def main():
    # Set Streamlit page configuration to wide layout
    st.set_page_config(
        page_title="University of Exeter AI Fund Stock Comparison",
        page_icon="AI_fund_logo.jpg",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.logo('AI_fund_logo.jpg', size = 'large')

    # Initialize session state for storing tickers and data
    if 'tickers' not in st.session_state:
        # List of 20 AI stock tickers
        st.session_state.tickers = [
            'NVDA', 'GOOGL', 'MSFT', 'AMZN', 'IBM', 'TSLA', 'META', 'BIDU',
            'AMD', 'CRM', 'INTC', 'ORCL', 'TWLO', 'PLTR', 'AI', 'PATH',
            'CGNX'
        ]
    if 'metrics_df' not in st.session_state:
        st.session_state.metrics_df = pd.DataFrame()
    if 'prev_tickers' not in st.session_state:
        st.session_state.prev_tickers = []

    # Set Seaborn style
    sns.set(style="darkgrid")

    # Set the title of the app
    st.title("University of Exeter AI Fund Stock Comparison")

    # Sidebar for user input
    st.sidebar.header("Manage Ticker Symbols")

    # Use st_tags_sidebar to allow users to add/remove tickers
    ticker_tags = st_tags_sidebar(
        label='**Enter Stock Ticker Symbols:**',
        text='Add or remove tickers (e.g., AAPL)',
        value=st.session_state.tickers,
        suggestions=[],
        maxtags=-1,
        key='ticker_tags'
    )

    # Update the tickers in session state based on tag input
    st.session_state.tickers = [ticker.upper() for ticker in ticker_tags]

    # Check if tickers have changed
    if set(st.session_state.tickers) != set(st.session_state.prev_tickers):
        # Ticker list has changed; set a flag to indicate data needs to be refreshed
        st.session_state.data_needs_refresh = True
        st.session_state.prev_tickers = st.session_state.tickers.copy()
    else:
        if 'data_needs_refresh' not in st.session_state:
            st.session_state.data_needs_refresh = False

    # Define a function to fetch data
    def fetch_data():
        if st.session_state.tickers:
            refreshed_data = pd.DataFrame()
            failed_tickers = []
            for ticker in st.session_state.tickers:
                try:
                    stock, metrics, sector, industry = get_stock_data(ticker)
                    metrics_row = {'Ticker': ticker}
                    metrics_row.update(metrics)
                    refreshed_data = pd.concat(
                        [refreshed_data, pd.DataFrame([metrics_row])],
                        ignore_index=True
                    )
                except Exception as e:
                    failed_tickers.append(ticker)
                    st.sidebar.error(f"Error fetching data for {ticker}: {e}")
            # Update the session state DataFrame
            st.session_state.metrics_df = refreshed_data
            if failed_tickers:
                st.sidebar.warning(f"Failed to fetch data for: {', '.join(failed_tickers)}")
            else:
                st.sidebar.success("Data fetched successfully.")
            # Reset the refresh flag
            st.session_state.data_needs_refresh = False

    # Fetch data if needed
    if st.session_state.data_needs_refresh:
        fetch_data()

    # Ensure numerical columns are of numeric data types
    numerical_columns = [
        'PE Ratio',
        'PEG Ratio',
        'Price-to-Sales Ratio',
        'Forward PE',
        'Price-to-Book Ratio',
        'EV/EBITDA Ratio',
        'Dividend Yield (%)',
        'Return on Equity (%)',
        'Earnings Per Share ($)',
        'Debt-to-Equity Ratio',
        'Profit Margin (%)',
        'Beta'
    ]

    if not st.session_state.metrics_df.empty:
        for col in numerical_columns:
            st.session_state.metrics_df[col] = pd.to_numeric(st.session_state.metrics_df[col], errors='coerce')

        # Proceed to create the Styler object and apply conditional formatting
        metrics_df = st.session_state.metrics_df.set_index('Ticker')

        # Define formatting for columns
        format_dict = {
            'Current Price ($)': '${:,.2f}',
            'PE Ratio': '{:.2f}',
            'PEG Ratio': '{:.2f}',
            'Price-to-Sales Ratio': '{:.2f}',
            'Forward PE': '{:.2f}',
            'Price-to-Book Ratio': '{:.2f}',
            'EV/EBITDA Ratio': '{:.2f}',
            'Dividend Yield (%)': '{:.2f}%',
            'Return on Equity (%)': '{:.2f}%',
            'Earnings Per Share ($)': '${:,.2f}',
            'Debt-to-Equity Ratio': '{:.2f}',
            'Profit Margin (%)': '{:.2f}%',
            'Beta': '{:.2f}',
        }

        # Create a Styler object with formatting
        styled_df = metrics_df.style.format(format_dict, na_rep='N/A')

        # Apply conditional formatting
        styled_df = styled_df.applymap(color_pe_ratio, subset=['PE Ratio'])
        styled_df = styled_df.applymap(color_forward_pe, subset=['Forward PE'])
        styled_df = styled_df.applymap(color_peg_ratio, subset=['PEG Ratio'])
        styled_df = styled_df.applymap(color_pb_ratio, subset=['Price-to-Book Ratio'])
        styled_df = styled_df.applymap(color_ps_ratio, subset=['Price-to-Sales Ratio'])
        styled_df = styled_df.applymap(color_ev_ebitda, subset=['EV/EBITDA Ratio'])
        styled_df = styled_df.applymap(color_dividend_yield, subset=['Dividend Yield (%)'])
        styled_df = styled_df.applymap(color_roe, subset=['Return on Equity (%)'])
        styled_df = styled_df.applymap(color_eps, subset=['Earnings Per Share ($)'])
        styled_df = styled_df.applymap(color_de_ratio, subset=['Debt-to-Equity Ratio'])
        styled_df = styled_df.applymap(color_profit_margin, subset=['Profit Margin (%)'])
        styled_df = styled_df.applymap(color_beta, subset=['Beta'])

        # --- 1. Display Comparison Table ---
        st.header("Stock Comparison Table")
        st.write(styled_df)

        # --- 2. Export to Excel Button ---
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Stock Metrics')
            processed_data = output.getvalue()
            return processed_data

        excel_data = to_excel(st.session_state.metrics_df)

        st.download_button(
            label="📥 Export data to Excel",
            data=excel_data,
            file_name='stock_metrics.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # --- 3. Refresh Data Button ---
        if st.button("Refresh Data"):
            fetch_data()
            st.success("Data refreshed successfully.")

        st.divider()

        # --- 4. Metrics Explained ---
        st.header("Metrics Explained")
        metric_list = list(metric_explanations.keys())
        choice = st.selectbox(
            "Select a Metric to Explain",
            metric_list,
        )
        st.write(f"**{choice}:** {metric_explanations[choice]}")

        st.divider()

        # --- 5. Visualization 1: Stock Price Chart ---
        st.header("Stock Price Over the Last Year")

        # Dropdown to select a ticker
        selected_ticker = st.selectbox(
            "Select a Ticker to View Price Chart",
            st.session_state.tickers
        )

        # Fetch historical data for the selected ticker
        stock_obj = yf.Ticker(selected_ticker)
        hist_data = stock_obj.history(period="1y")

        if not hist_data.empty:
            hist_data.reset_index(inplace=True)
            fig_price = px.line(
                hist_data,
                x='Date',
                y='Close',
                title=f"{selected_ticker} Closing Price Over the Last Year",
                labels={'Close': 'Closing Price ($)', 'Date': 'Date'}
            )
            st.plotly_chart(fig_price, use_container_width=True)
        else:
            st.warning(f"No historical data available for {selected_ticker}.")

        st.divider()

        # --- 5. Visualization 2: Metric Comparison Chart ---
        st.header("Metric Comparison Among Selected Stocks")

        # Dropdown to select a metric
        metric_options = [
            'PE Ratio',
            'PEG Ratio',
            'Price-to-Sales Ratio',
            'Forward PE',
            'Price-to-Book Ratio',
            'EV/EBITDA Ratio',
            'Dividend Yield (%)',
            'Return on Equity (%)',
            'Earnings Per Share ($)',
            'Debt-to-Equity Ratio',
            'Profit Margin (%)',
            'Beta'
        ]

        selected_metric = st.selectbox(
            "Select a Metric to Compare Across Stocks",
            metric_options
        )

        # Filter data for the selected metric
        metric_data = st.session_state.metrics_df[['Ticker', selected_metric]].dropna()

        if not metric_data.empty:
            # Create a bar chart using Plotly
            fig_metric = px.bar(
                metric_data,
                x='Ticker',
                y=selected_metric,
                title=f"Comparison of {selected_metric} Across Selected Stocks",
                labels={'Ticker': 'Ticker', selected_metric: selected_metric}
            )
            st.plotly_chart(fig_metric, use_container_width=True)
        else:
            st.warning(f"No data available for {selected_metric}.")

    else:
        st.info("No data available to display. Please add tickers and click 'Refresh Data'.")

   

    # Instructions 
    st.sidebar.markdown("""
    ---
    **Instructions:**
    - Use the tag input above to add or remove stock ticker symbols.
    - Click the "Refresh Data" button to update all metrics for the selected tickers.
    - You can add as many tickers as you'd like to compare.
    - Examples: AAPL, MSFT, TSLA, etc.
    """)

if __name__ == "__main__":
    main()
