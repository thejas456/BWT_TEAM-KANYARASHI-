import numpy as np
import pandas as pd

def _clip01(x):
    return float(np.clip(x, 0.0, 1.0))

def spending_stability(spending_ratio):
    return _clip01(1.0 / (1.0 + float(spending_ratio)))

def freq_score(transaction_frequency, cap=10.0):
    return _clip01(float(transaction_frequency) / float(cap))

def trust_score_row(row, weights=None, cap_freq=10.0):
    w = weights or {'income_consistency': 0.35, 'savings_ratio': 0.25, 'spending_stability': 0.20, 'transaction_frequency': 0.20}
    ic = _clip01(row.get('monthly_income_consistency', 0.0))
    sr = _clip01(row.get('savings_ratio', 0.0))
    ss = spending_stability(row.get('spending_ratio', 0.0))
    tf = freq_score(row.get('transaction_frequency', 0.0), cap=cap_freq)
    s = w['income_consistency'] * ic + w['savings_ratio'] * sr + w['spending_stability'] * ss + w['transaction_frequency'] * tf
    return float(np.clip(s * 100.0, 0.0, 100.0))

def risk_level(score):
    if score >= 70.0:
        return 'Low Risk'
    if score >= 45.0:
        return 'Medium Risk'
    return 'High Risk'

def loan_eligibility(score):
    return bool(score >= 60.0)

def apply_scores(df, weights=None, cap_freq=10.0):
    scores = []
    for _, r in df.iterrows():
        ts = trust_score_row(r, weights=weights, cap_freq=cap_freq)
        risk = risk_level(ts)
        elig = 'Yes' if loan_eligibility(ts) else 'No'
        scores.append({'user_id': r.get('user_id', None), 'TrustScore': ts, 'Risk': risk, 'LoanEligibility': elig})
    return pd.DataFrame(scores)

def contributions(row, weights=None, cap_freq=10.0):
    w = weights or {'income_consistency': 0.35, 'savings_ratio': 0.25, 'spending_stability': 0.20, 'transaction_frequency': 0.20}
    ic = _clip01(row.get('monthly_income_consistency', 0.0))
    sr = _clip01(row.get('savings_ratio', 0.0))
    ss = spending_stability(row.get('spending_ratio', 0.0))
    tf = freq_score(row.get('transaction_frequency', 0.0), cap=cap_freq)
    parts = {
        'Income Consistency': w['income_consistency'] * ic * 100.0,
        'Savings Ratio': w['savings_ratio'] * sr * 100.0,
        'Spending Stability': w['spending_stability'] * ss * 100.0,
        'Transaction Frequency': w['transaction_frequency'] * tf * 100.0
    }
    return pd.DataFrame({'feature': list(parts.keys()), 'contribution': list(parts.values())})
