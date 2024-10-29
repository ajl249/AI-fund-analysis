# finance_data.py

import yfinance as yf
import numpy as np

def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    # Fetch info
    try:
        info = stock.info
    except Exception as e:
        raise Exception(f"Error fetching data for {ticker_symbol}: {e}")

    # Extract financial metrics with default values
    current_price = info.get('currentPrice', np.nan)
    pe_ratio = info.get('trailingPE', np.nan)
    forward_pe = info.get('forwardPE', np.nan)
    peg_ratio = info.get('pegRatio', np.nan)
    pb_ratio = info.get('priceToBook', np.nan)
    ps_ratio = info.get('priceToSalesTrailing12Months', np.nan)
    dividend_yield = info.get('dividendYield', np.nan)
    roe = info.get('returnOnEquity', np.nan)
    eps = info.get('trailingEps', np.nan)
    debt_to_equity = info.get('debtToEquity', np.nan)
    profit_margin = info.get('profitMargins', np.nan)
    beta = info.get('beta', np.nan)
    enterprise_value = info.get('enterpriseValue', np.nan)
    ebitda = info.get('ebitda', np.nan)
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')

    # Convert percentages
    dividend_yield_percentage = dividend_yield * 100 if not np.isnan(dividend_yield) else np.nan
    roe_percentage = roe * 100 if not np.isnan(roe) else np.nan
    profit_margin_percentage = profit_margin * 100 if not np.isnan(profit_margin) else np.nan

    # Calculate EV/EBITDA Ratio
    if not np.isnan(enterprise_value) and not np.isnan(ebitda) and ebitda != 0:
        ev_ebitda_ratio = enterprise_value / ebitda
    else:
        ev_ebitda_ratio = np.nan

    # Store numerical values in the metrics dictionary
    metrics = {
        'Current Price ($)': current_price,
        'PE Ratio': pe_ratio,
        'PEG Ratio': peg_ratio,
        'Price-to-Sales Ratio': ps_ratio,
        'Forward PE': forward_pe,
        'Price-to-Book Ratio': pb_ratio,
        'EV/EBITDA Ratio': ev_ebitda_ratio,
        'Dividend Yield (%)': dividend_yield_percentage,
        'Return on Equity (%)': roe_percentage,
        'Earnings Per Share ($)': eps,
        'Debt-to-Equity Ratio': debt_to_equity,
        'Profit Margin (%)': profit_margin_percentage,
        'Beta': beta,
        'Sector': sector,
        'Industry': industry
    }

    return stock, metrics, sector, industry
