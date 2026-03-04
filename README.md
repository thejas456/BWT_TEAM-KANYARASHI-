# BWT_TEAM-KANYARASHI-
This is a Trae AI project

## CredPulse AI
Alternative credit scoring for gig workers with interpretable, heuristic+unsupervised, and supervised TrustScore pipelines. Includes a Streamlit dashboard for CSV upload, scoring, explainability, and loan recommendation.

### Features
- Per-user feature engineering (income consistency, savings ratio, stability, frequency)
- Interpretable TrustScore with configurable weights
- IsolationForest component blended with heuristics
- Supervised pipeline (RandomForest / Logistic Regression)
- Explainability: contributions and feature importance
- Loan recommendation and safe EMI guidance
- Streamlit UI with gauge, health meter, risk badge, and sidebar controls

### Quickstart
1. Install
   - `pip install -r requirements.txt`
2. Run Dashboard
   - `streamlit run app.py`
3. Upload data
   - Use the sample: `sample_transactions.csv`

### CLI
- Feature engineering per user:
  - `python scripts/compute_user_features.py --income-threshold=1200 --relative=true --relative-factor=0.5 --freq=week`
- Interpretable scoring:
  - `python scripts/score_interpretable.py features_per_user.csv --cap-freq=12`
- Train supervised:
  - `python scripts/train_trust_model.py --model=rf`

### Repo Structure
- `app.py` Streamlit dashboard
- `src/` modules:
  - `data_loader.py`, `feature_engineering.py`, `user_features.py`
  - `scoring.py`, `interpretable_scoring.py`, `model.py`
  - `supervised_model.py`, `loan_recommender.py`
- `scripts/` CLI utilities
- `sample_transactions.csv` demo dataset

### GitHub
Initialize and push:
```
git init
git add .
git commit -m "Initial commit: CredPulse AI"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```
