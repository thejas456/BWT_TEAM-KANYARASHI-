import pandas as pd
import numpy as np

def engineer_features(df):
    df = df.copy()
    if 'date' not in df.columns:
        return pd.Series(dtype=float)
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    credits = df[df['type'] == 'credit']
    debits = df[df['type'] == 'debit']
    total_income = credits['amount'].clip(lower=0).sum()
    total_expense = debits['amount'].abs().sum()
    net_cashflow = total_income - total_expense
    txn_count = len(df)
    credit_count = len(credits)
    debit_count = len(debits)
    avg_txn_amount = df['amount'].abs().mean() if txn_count else 0.0
    income_monthly = credits.groupby('month')['amount'].sum()
    expense_monthly = debits.groupby('month')['amount'].abs().sum()
    income_std = income_monthly.std(ddof=0) if len(income_monthly) else 0.0
    expense_std = expense_monthly.std(ddof=0) if len(expense_monthly) else 0.0
    income_mean = income_monthly.mean() if len(income_monthly) else 0.0
    expense_mean = expense_monthly.mean() if len(expense_monthly) else 0.0
    savings_rate = (net_cashflow / total_income) if total_income > 0 else 0.0
    df_sorted = df.sort_values('date')
    gaps = df_sorted['date'].diff().dt.days.dropna()
    median_gap_days = gaps.median() if len(gaps) else 0.0
    diversity_cols = [c for c in ['merchant', 'category'] if c in df.columns]
    if diversity_cols:
        uniq = pd.concat([df[c].astype(str) for c in diversity_cols], axis=1).agg('-'.join, axis=1).nunique()
        merchant_diversity = uniq / txn_count if txn_count else 0.0
    else:
        merchant_diversity = 0.0
    return pd.Series({
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'net_cashflow': float(net_cashflow),
        'txn_count': float(txn_count),
        'credit_count': float(credit_count),
        'debit_count': float(debit_count),
        'avg_txn_amount': float(avg_txn_amount),
        'income_std': float(income_std),
        'expense_std': float(expense_std),
        'income_mean': float(income_mean),
        'expense_mean': float(expense_mean),
        'savings_rate': float(np.clip(savings_rate, 0, 1)),
        'median_gap_days': float(median_gap_days),
        'merchant_diversity': float(merchant_diversity)
    })

def monthly_feature_matrix(df):
    df = df.copy()
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    credits = df[df['type'] == 'credit']
    debits = df[df['type'] == 'debit']
    income = credits.groupby('month')['amount'].sum().rename('income')
    expense = debits.groupby('month')['amount'].abs().sum().rename('expense')
    counts_c = credits.groupby('month').size().rename('credit_count')
    counts_d = debits.groupby('month').size().rename('debit_count')
    X = pd.concat([income, expense, counts_c, counts_d], axis=1).fillna(0)
    X['net'] = X['income'] - X['expense']
    return X.reset_index(drop=True)
