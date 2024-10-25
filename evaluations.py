# evaluations.py

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

def evaluate_metrics(metrics, industry_pe_ratio):
    pe_message, pe_score = evaluate_pe_ratio(metrics['PE Ratio'], industry_pe_ratio)
    roe_message, roe_score = evaluate_roe(metrics['Return on Equity (%)'])
    de_message, de_score = evaluate_debt_to_equity(metrics['Debt-to-Equity Ratio'])
    pm_message, pm_score = evaluate_profit_margin(metrics['Profit Margin (%)'])
    ev_message, ev_score = evaluate_ev_ebitda(metrics['EV/EBITDA Ratio'])

    total_score = pe_score + roe_score + de_score + pm_score + ev_score

    # Determine overall valuation
    if total_score >= 3:
        overall_evaluation = "The stock appears to be **undervalued**."
    elif -2 <= total_score <= 2:
        overall_evaluation = "The stock appears to be **fairly valued**."
    else:
        overall_evaluation = "The stock appears to be **overvalued**."

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

    return evaluations, overall_evaluation