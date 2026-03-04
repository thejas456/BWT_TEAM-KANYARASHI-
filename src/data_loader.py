import pandas as pd
import numpy as np

def load_transactions(source):
    df = pd.read_csv(source)
    cols = {c: c.lower().strip() for c in df.columns}
    df = df.rename(columns=cols)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    elif 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    elif 'transaction_amount' in df.columns:
        df['amount'] = pd.to_numeric(df['transaction_amount'], errors='coerce')
    if 'type' in df.columns:
        df['type'] = df['type'].astype(str).str.lower().str.strip()
    elif 'transaction_type' in df.columns:
        tt = df['transaction_type'].astype(str).str.lower().str.strip()
        df['type'] = np.where(tt == 'income', 'credit', np.where(tt == 'expense', 'debit', tt))
    if 'merchant_category' in df.columns and 'category' not in df.columns:
        df['category'] = df['merchant_category'].astype(str)
    df = df.dropna(subset=['date', 'amount'])
    if 'type' not in df.columns:
        df['type'] = np.where(df['amount'] >= 0, 'credit', 'debit')
    return df
