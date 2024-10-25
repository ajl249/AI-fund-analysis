# evaluations.py

def evaluate_pe_ratio(pe):
    try:
        pe_value = float(pe)
    except:
        return ("PE ratio is not available for comparison.", 0, "black")
    # Define fixed ranges for PE Ratio
    if pe_value < 20:
        return (f"Undervalued based on PE Ratio (<20). PE Ratio = {pe_value}.", 1, "green")
    elif 20 <= pe_value <= 25:
        return (f"Fairly valued based on PE Ratio (20 - 25). PE Ratio = {pe_value}.", 0, "orange")
    else:
        return (f"Overvalued based on PE Ratio (>25). PE Ratio = {pe_value}.", -1, "red")

def evaluate_peg_ratio(peg):
    try:
        peg_value = float(peg)
    except:
        return ("PEG ratio is not available for comparison.", 0, "black")
    # Define fixed ranges for PEG Ratio
    if peg_value < 1:
        return (f"Undervalued based on PEG Ratio (<1). PEG Ratio = {peg_value}.", 1, "green")
    elif 1 <= peg_value <= 1.5:
        return (f"Fairly valued based on PEG Ratio (1 - 1.5). PEG Ratio = {peg_value}.", 0, "orange")
    else:
        return (f"Overvalued based on PEG Ratio (>1.5). PEG Ratio = {peg_value}.", -1, "red")

def evaluate_price_to_sales(ps_ratio):
    try:
        ps_value = float(ps_ratio)
    except:
        return ("Price-to-Sales ratio is not available.", 0, "black")
    # Define expected ranges for Price-to-Sales Ratio
    # These ranges can vary by industry; adjust as necessary
    if ps_value < 1:
        return (f"Undervalued based on Price-to-Sales Ratio (<1). Price-to-Sales Ratio = {ps_value}.", 1, "green")
    elif 1 <= ps_value <= 3:
        return (f"Fairly valued based on Price-to-Sales Ratio (1 - 3). Price-to-Sales Ratio = {ps_value}.", 0, "orange")
    else:
        return (f"Overvalued based on Price-to-Sales Ratio (>3). Price-to-Sales Ratio = {ps_value}.", -1, "red")

def evaluate_roe(roe_value):
    try:
        roe_value = float(roe_value.replace('%', ''))
    except:
        return ("Return on Equity is not available.", 0, "black")
    if roe_value > 15:
        return (f"High Return on Equity (>15%). ROE = {roe_value}%.", 1, "green")
    elif 10 <= roe_value <= 15:
        return (f"Moderate Return on Equity (10% - 15%). ROE = {roe_value}%.", 0, "orange")
    else:
        return (f"Low Return on Equity (<10%). ROE = {roe_value}%.", -1, "red")

def evaluate_debt_to_equity(de_ratio):
    try:
        de_value = float(de_ratio)
    except:
        return ("Debt-to-Equity ratio is not available.", 0, "black")
    if de_value < 1:
        return (f"Low Debt-to-Equity ratio (<1). Debt-to-Equity = {de_value}.", 1, "green")
    elif 1 <= de_value <= 2:
        return (f"Moderate Debt-to-Equity ratio (1 - 2). Debt-to-Equity = {de_value}.", 0, "orange")
    else:
        return (f"High Debt-to-Equity ratio (>2). Debt-to-Equity = {de_value}.", -1, "red")

def evaluate_profit_margin(pm):
    try:
        pm_value = float(pm.replace('%', ''))
    except:
        return ("Profit Margin is not available.", 0, "black")
    if pm_value > 20:
        return (f"High Profit Margin (>20%). Profit Margin = {pm_value}%.", 1, "green")
    elif 10 <= pm_value <= 20:
        return (f"Moderate Profit Margin (10% - 20%). Profit Margin = {pm_value}%.", 0, "orange")
    else:
        return (f"Low Profit Margin (<10%). Profit Margin = {pm_value}%.", -1, "red")

def evaluate_ev_ebitda(ev_ebitda):
    try:
        ev_ebitda_value = float(ev_ebitda)
    except:
        return ("EV/EBITDA ratio is not available.", 0, "black")
    if ev_ebitda_value < 10:
        return (f"Potentially undervalued based on EV/EBITDA (<10). EV/EBITDA = {ev_ebitda_value}.", 1, "green")
    elif 10 <= ev_ebitda_value <= 14:
        return (f"Fairly valued based on EV/EBITDA (10 - 14). EV/EBITDA = {ev_ebitda_value}.", 0, "orange")
    else:
        return (f"Potentially overvalued based on EV/EBITDA (>14). EV/EBITDA = {ev_ebitda_value}.", -1, "red")

def evaluate_metrics(metrics):
    pe_message, pe_score, pe_color = evaluate_pe_ratio(metrics['PE Ratio'])
    peg_message, peg_score, peg_color = evaluate_peg_ratio(metrics['PEG Ratio'])           # Added PEG Ratio
    ps_message, ps_score, ps_color = evaluate_price_to_sales(metrics['Price-to-Sales Ratio'])  # Moved PS Ratio to third position
    roe_message, roe_score, roe_color = evaluate_roe(metrics['Return on Equity (%)'])
    de_message, de_score, de_color = evaluate_debt_to_equity(metrics['Debt-to-Equity Ratio'])
    pm_message, pm_score, pm_color = evaluate_profit_margin(metrics['Profit Margin (%)'])
    ev_message, ev_score, ev_color = evaluate_ev_ebitda(metrics['EV/EBITDA Ratio'])

    total_score = pe_score + peg_score + ps_score + roe_score + de_score + pm_score + ev_score

    # Determine overall valuation without color
    # As per your instruction, the overall evaluation statement is removed

    # Create evaluation dictionary with color-coded messages
    evaluations = {
        'Metric': [
            'PE Ratio',
            'PEG Ratio',                   # Added PEG Ratio
            'Price-to-Sales Ratio',        # Moved PS Ratio to third position
            'Return on Equity',
            'Debt-to-Equity',
            'Profit Margin',
            'EV/EBITDA Ratio'
        ],
        'Evaluation': [
            pe_message,
            peg_message,                   # Added PEG Ratio
            ps_message,                    # Moved PS Ratio to third position
            roe_message,
            de_message,
            pm_message,
            ev_message
        ],
        'Color': [
            pe_color,
            peg_color,                     # Added PEG Ratio
            ps_color,                      # Moved PS Ratio to third position
            roe_color,
            de_color,
            pm_color,
            ev_color
        ]
    }

    return evaluations, None  # Removed overall_evaluation