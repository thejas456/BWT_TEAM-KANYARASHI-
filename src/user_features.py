import pandas as pd
import numpy as np

def engineer_user_features(
    df,
    income_threshold=1000.0,
    weekly=True,
    relative_threshold=False,
    relative_factor=0.6
):
    df = df.copy()
    cols = {c: c.lower().strip() for c in df.columns}
    df = df.rename(columns=cols)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
        df['month'] = df['timestamp'].dt.to_period('M').dt.to_timestamp()
        dt_col = df['timestamp']
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
        df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
        dt_col = df['date']
    else:
        dt_col = None
    if 'transaction_amount' in df.columns:
        df['transaction_amount'] = pd.to_numeric(df['transaction_amount'], errors='coerce')
    if 'amount' in df.columns and 'transaction_amount' not in df.columns:
        df['transaction_amount'] = pd.to_numeric(df['amount'], errors='coerce')
    if 'transaction_type' in df.columns:
        df['transaction_type'] = df['transaction_type'].astype(str).str.lower().str.strip()
    if 'type' in df.columns and 'transaction_type' not in df.columns:
        df['transaction_type'] = df['type'].astype(str).str.lower().str.strip()
    df = df.dropna(subset=['transaction_amount', 'month'])
    groups = []
    for uid, g in df.groupby('user_id'):
        incomes = g[g['transaction_type'] == 'income']
        expenses = g[g['transaction_type'] == 'expense']
        total_income = float(incomes['transaction_amount'].clip(lower=0).sum())
        total_expenses = float(expenses['transaction_amount'].abs().sum())
        months = g['month'].nunique()
        txn_count = len(g)
        if weekly and dt_col is not None:
            gd = g[dt_col.name]
            if len(gd) > 0:
                days = (gd.max() - gd.min()).days + 1
                weeks = int(np.ceil(max(days, 1) / 7))
            else:
                weeks = 1
            freq = float(txn_count / weeks) if weeks > 0 else float(txn_count)
        else:
            freq = float(txn_count / months) if months > 0 else float(txn_count)
        avg_val = float(g['transaction_amount'].abs().mean()) if txn_count else 0.0
        income_monthly = incomes.groupby('month')['transaction_amount'].sum()
        mean_income = float(income_monthly.mean()) if len(income_monthly) else 0.0
        std_income = float(income_monthly.std(ddof=0)) if len(income_monthly) else 0.0
        income_volatility = float(std_income / mean_income) if mean_income > 0 else 0.0
        if relative_threshold and len(income_monthly):
            base_thr = float(income_monthly.median()) * float(relative_factor)
            thr = base_thr if base_thr > 0 else float(income_threshold)
        else:
            thr = float(income_threshold)
        if months > 0 and len(income_monthly) > 0:
            consistent_months = int((income_monthly >= thr).sum())
            monthly_income_consistency = float(np.clip(consistent_months / months, 0.0, 1.0))
        else:
            monthly_income_consistency = 0.0
        spending_ratio = float(total_expenses / total_income) if total_income > 0 else 0.0
        savings_ratio = float(np.clip((total_income - total_expenses) / total_income, 0.0, 1.0)) if total_income > 0 else 0.0
        groups.append({
            'user_id': uid,
            'monthly_income_consistency': monthly_income_consistency,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'spending_ratio': spending_ratio,
            'transaction_frequency': freq,
            'avg_transaction_value': avg_val,
            'income_volatility': income_volatility,
            'savings_ratio': savings_ratio,
            'mean_monthly_income': mean_income
        })
    return pd.DataFrame(groups)
