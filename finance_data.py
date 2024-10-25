# finance_data.py

import yfinance as yf

def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    # Fetch info
    try:
        info = stock.info
    except Exception as e:
        raise Exception(f"Error fetching data for {ticker_symbol}: {e}")

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
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')

    # Convert percentages
    dividend_yield_percentage = round(dividend_yield * 100, 2) if dividend_yield is not None else None
    roe_percentage = round(roe * 100, 2) if roe is not None else None
    profit_margin_percentage = round(profit_margin * 100, 2) if profit_margin is not None else None

    # Calculate EV/EBITDA Ratio
    if enterprise_value is not None and ebitda is not None and ebitda != 0:
        ev_ebitda_ratio = round(enterprise_value / ebitda, 2)
    else:
        ev_ebitda_ratio = None

    # Create a dictionary of metrics
    metrics = {
        'Current Price ($)': current_price,
        'PE Ratio': pe_ratio,
        'Forward PE': forward_pe,
        'PEG Ratio': peg_ratio,
        'Price-to-Book Ratio': pb_ratio,
        'Price-to-Sales Ratio': ps_ratio,
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