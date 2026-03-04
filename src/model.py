import numpy as np
from sklearn.ensemble import IsolationForest
from .feature_engineering import monthly_feature_matrix

def train_unsupervised(df):
    X = monthly_feature_matrix(df)
    if len(X) < 2:
        return None, None
    model = IsolationForest(random_state=42, contamination=0.1)
    model.fit(X.values)
    return model, X

def model_trust_component(model, X):
    if model is None or X is None or len(X) == 0:
        return None
    s = model.decision_function(X.values)
    s = np.clip(s, -1.0, 1.0)
    s = (s - s.min()) / (s.max() - s.min() + 1e-9)
    return float(np.clip(100.0 * s.mean(), 0, 100))

def predict_eligibility(score):
    return bool(score >= 60.0)
