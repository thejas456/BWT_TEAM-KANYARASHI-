import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from .scoring import risk_category

def generate_labels(df):
    y = (
        (df['savings_ratio'].fillna(0) >= 0.2).astype(int)
        & (df['monthly_income_consistency'].fillna(0) >= 0.5).astype(int)
        & (df['spending_ratio'].replace([np.inf, -np.inf], np.nan).fillna(0) <= 1.2).astype(int)
    ).astype(int)
    return y

def feature_columns(df):
    cols = [
        'monthly_income_consistency',
        'total_income',
        'total_expenses',
        'spending_ratio',
        'transaction_frequency',
        'avg_transaction_value',
        'income_volatility',
        'savings_ratio'
    ]
    return [c for c in cols if c in df.columns]

def build_pipeline(model_type='rf', random_state=42):
    if model_type == 'logreg':
        clf = LogisticRegression(max_iter=1000, random_state=random_state)
        pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)])
    else:
        clf = RandomForestClassifier(n_estimators=200, random_state=random_state)
        pipe = Pipeline([('clf', clf)])
    return pipe

def train(df, model_type='rf', test_size=0.2, random_state=42):
    df = df.copy()
    X_cols = feature_columns(df)
    X = df[X_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    if 'label' in df.columns:
        y = df['label'].astype(int)
    else:
        y = generate_labels(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    pipe = build_pipeline(model_type=model_type, random_state=random_state)
    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]
    trust = np.clip(proba * 100.0, 0, 100)
    risks = [risk_category(s) for s in trust]
    report = classification_report(y_test, pipe.predict(X_test), output_dict=False)
    out = pd.DataFrame({
        'user_id': df.loc[X_test.index, 'user_id'] if 'user_id' in df.columns else X_test.index,
        'TrustScore': trust,
        'Risk': risks
    })
    return pipe, out, report
