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
    peg_ratio = info.get('pegRatio', None)            # Added PEG Ratio
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

    # Format numerical values as strings with appropriate formatting
    metrics = {
        'Current Price ($)': f"${current_price:,.2f}" if current_price is not None else 'N/A',
        'PE Ratio': f"{pe_ratio:.2f}" if pe_ratio is not None else 'N/A',
        'PEG Ratio': f"{peg_ratio:.2f}" if peg_ratio is not None else 'N/A',              # Added PEG Ratio
        'Price-to-Sales Ratio': f"{ps_ratio:.2f}" if ps_ratio is not None else 'N/A',      # Moved PS Ratio to third position
        'Forward PE': f"{forward_pe:.2f}" if forward_pe is not None else 'N/A',
        'Price-to-Book Ratio': f"{pb_ratio:.2f}" if pb_ratio is not None else 'N/A',
        'EV/EBITDA Ratio': f"{ev_ebitda_ratio:.2f}" if ev_ebitda_ratio is not None else 'N/A',
        'Dividend Yield (%)': f"{dividend_yield_percentage:.2f}%" if dividend_yield_percentage is not None else 'N/A',
        'Return on Equity (%)': f"{roe_percentage:.2f}%" if roe_percentage is not None else 'N/A',
        'Earnings Per Share ($)': f"${eps:,.2f}" if eps is not None else 'N/A',
        'Debt-to-Equity Ratio': f"{debt_to_equity:.2f}" if debt_to_equity is not None else 'N/A',
        'Profit Margin (%)': f"{profit_margin_percentage:.2f}%" if profit_margin_percentage is not None else 'N/A',
        'Beta': f"{beta:.2f}" if beta is not None else 'N/A',
        'Sector': sector,
        'Industry': industry
    }

    return stock, metrics, sector, industry