import math

def safe_emi(monthly_income, rate=0.3):
    mi = float(monthly_income or 0.0)
    return float(max(0.0, mi * rate))

def recommend(score, monthly_income):
    s = float(score or 0.0)
    if s > 75.0:
        max_loan = 50000.0
        status = 'Eligible'
    elif s >= 50.0:
        max_loan = 20000.0
        status = 'Eligible'
    else:
        max_loan = 0.0
        status = 'Not eligible'
    emi = safe_emi(monthly_income)
    return {
        'status': status,
        'max_loan_amount': max_loan,
        'recommended_emi': emi
    }
