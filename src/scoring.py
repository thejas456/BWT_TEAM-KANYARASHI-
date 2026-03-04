import numpy as np

def normalize(value, min_v, max_v):
    if max_v == min_v:
        return 0.0
    v = (value - min_v) / (max_v - min_v)
    return float(np.clip(v, 0, 1))

def heuristic_score(features):
    income_score = normalize(features.get('income_mean', 0.0), 0.0, max(features.get('income_mean', 0.0), 1.0))
    savings_score = features.get('savings_rate', 0.0)
    stability_score = 1.0 - normalize(features.get('income_std', 0.0), 0.0, max(features.get('income_mean', 0.0), 1.0))
    diversity_score = features.get('merchant_diversity', 0.0)
    activity_score = normalize(features.get('txn_count', 0.0), 0.0, max(features.get('txn_count', 0.0), 1.0))
    score = 0.35 * income_score + 0.25 * savings_score + 0.2 * stability_score + 0.1 * diversity_score + 0.1 * activity_score
    return float(np.clip(score * 100, 0, 100))

def blended_score(features, model_score=None):
    base = heuristic_score(features)
    if model_score is None:
        return base
    return float(np.clip(0.6 * base + 0.4 * model_score, 0, 100))

def trust_score(features, model_score=None):
    return blended_score(features, model_score)

def risk_category(score):
    if score >= 70:
        return 'Low Risk'
    if score >= 45:
        return 'Medium Risk'
    return 'High Risk'

def loan_recommendation(features, score):
    monthly_net = features.get('income_mean', 0.0) - features.get('expense_mean', 0.0)
    if monthly_net < 0:
        monthly_net = 0.0
    if score >= 75:
        amount = monthly_net * 3.0
        tenure = 12
        return f'Recommend approval up to {amount:.2f} with {tenure} months'
    if score >= 55:
        amount = monthly_net * 1.5
        tenure = 9
        return f'Consider approval up to {amount:.2f} with {tenure} months'
    return 'Not recommended currently; increase savings and stabilize income'

def heuristic_contributions(features, model_score=None):
    income_score = normalize(features.get('income_mean', 0.0), 0.0, max(features.get('income_mean', 0.0), 1.0))
    savings_score = features.get('savings_rate', 0.0)
    stability_score = 1.0 - normalize(features.get('income_std', 0.0), 0.0, max(features.get('income_mean', 0.0), 1.0))
    diversity_score = features.get('merchant_diversity', 0.0)
    activity_score = normalize(features.get('txn_count', 0.0), 0.0, max(features.get('txn_count', 0.0), 1.0))
    parts = {
        'Income Strength': 0.6 * 100.0 * 0.35 * income_score,
        'Savings Rate': 0.6 * 100.0 * 0.25 * savings_score,
        'Income Stability': 0.6 * 100.0 * 0.20 * stability_score,
        'Merchant Diversity': 0.6 * 100.0 * 0.10 * diversity_score,
        'Activity': 0.6 * 100.0 * 0.10 * activity_score
    }
    if model_score is not None:
        parts['Model Component'] = float(np.clip(0.4 * model_score, 0.0, 40.0))
    return parts
