import streamlit as st
import pandas as pd
import os
import joblib
import altair as alt
from src.data_loader import load_transactions
from src.feature_engineering import engineer_features
from src.user_features import engineer_user_features
from src.model import train_unsupervised, model_trust_component, predict_eligibility
from src.scoring import trust_score, risk_category, loan_recommendation
from src.interpretable_scoring import trust_score_row, risk_level, loan_eligibility, contributions as interp_contrib
from src.supervised_model import feature_columns
from src.loan_recommender import recommend as loan_recommend
from src.scoring import heuristic_contributions

st.set_page_config(page_title='CredPulse AI', page_icon='💳', layout='centered')
st.title('CredPulse AI')
st.subheader('AI-powered alternative credit scoring for gig workers')
method = st.sidebar.selectbox('Scoring Method', ['Interpretable', 'Heuristic+Unsupervised', 'Supervised'])

theme = st.sidebar.radio('Theme', ['Light', 'Dark'], index=0)
currency = st.sidebar.text_input('Currency symbol', value='₹')
cap_freq = st.sidebar.slider('Frequency cap (transactions/week)', 5, 20, 10)
g_inner = st.sidebar.slider('Gauge inner radius', 60, 120, 90)
g_outer = st.sidebar.slider('Gauge outer radius', 100, 160, 120)
wi_ic = st.sidebar.slider('Weight: Income Consistency', 0.0, 1.0, 0.35)
wi_sr = st.sidebar.slider('Weight: Savings Ratio', 0.0, 1.0, 0.25)
wi_ss = st.sidebar.slider('Weight: Spending Stability', 0.0, 1.0, 0.20)
wi_tf = st.sidebar.slider('Weight: Transaction Frequency', 0.0, 1.0, 0.20)
_sumw = max(wi_ic + wi_sr + wi_ss + wi_tf, 1e-6)
weights_interp = {
    'income_consistency': wi_ic / _sumw,
    'savings_ratio': wi_sr / _sumw,
    'spending_stability': wi_ss / _sumw,
    'transaction_frequency': wi_tf / _sumw
}

st.markdown(
    "<style>.dashboard-card{background:%s;padding:16px;border-radius:12px;border:1px solid %s} .badge{display:inline-block;padding:6px 10px;border-radius:8px;color:#fff;font-weight:600}</style>" % ("#1e1e1e" if theme=='Dark' else "#f8f9fb", "#3a3a3a" if theme=='Dark' else "#e6e8ee"),
    unsafe_allow_html=True
)

st.header('Upload transaction file')
uploaded = st.file_uploader('Upload transaction CSV', type=['csv'])

st.header('Generate TrustScore')
trigger = st.button('Generate TrustScore')

def risk_color(category):
    if category == 'Low Risk':
        return '#2ca02c'
    if category == 'Medium Risk':
        return '#f5a623'
    return '#d9534f'

def gauge_chart(score, color='#2ca02c'):
    v = float(max(min(score, 100.0), 0.0))
    data = pd.DataFrame({'part': ['score', 'remainder'], 'value': [v, 100.0 - v]})
    chart = alt.Chart(data).mark_arc(innerRadius=g_inner, outerRadius=g_outer).encode(
        theta='value',
        color=alt.Color('part', scale=alt.Scale(domain=['score', 'remainder'], range=[color, '#e6e6e6']), legend=None)
    ).properties(width=240, height=160)
    return chart

def health_meter(score, color='#2ca02c'):
    v = float(max(min(score, 100.0), 0.0))
    base = pd.DataFrame({'label': ['fill', 'bg'], 'value': [v, 100]})
    fill = alt.Chart(base[base['label'] == 'fill']).mark_bar(color=color).encode(x=alt.X('value', scale=alt.Scale(domain=[0, 100])), y=alt.Y('label', axis=None))
    bg = alt.Chart(base[base['label'] == 'bg']).mark_bar(color='#e6e6e6').encode(x=alt.X('value', scale=alt.Scale(domain=[0, 100])), y=alt.Y('label', axis=None))
    return bg.properties(width=300, height=24) + fill.properties(width=300, height=24)

if uploaded and trigger:
    df = load_transactions(uploaded)
    if method == 'Interpretable':
        ufeats = engineer_user_features(df)
        row = ufeats.iloc[0] if len(ufeats) else pd.Series({})
        score = trust_score_row(row, weights=weights_interp, cap_freq=cap_freq)
        category = risk_level(score)
        eligible = loan_eligibility(score)
        color = risk_color(category)
        st.header('Trust Overview')
        top = st.container()
        c1, c2 = top.columns([1, 1])
        with c1:
            st.altair_chart(gauge_chart(score, color), use_container_width=False)
            st.altair_chart(health_meter(score, color), use_container_width=False)
        with c2:
            card = st.container()
            with card:
                st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
                st.metric('TrustScore', f'{score:.1f}')
                st.markdown(f"<div class='badge' style='background:{color}'> {category} </div>", unsafe_allow_html=True)
                st.metric('Loan Eligibility', 'Yes' if eligible else 'No')
                st.markdown("</div>", unsafe_allow_html=True)
        st.header('Financial health indicator')
        if category == 'Low Risk':
            st.success('Healthy')
        elif category == 'Medium Risk':
            st.warning('Needs attention')
        else:
            st.error('Fragile')
        st.caption('Per-user features')
        st.dataframe(ufeats)
        if len(ufeats):
            mi = float(ufeats.iloc[0].get('mean_monthly_income', 0.0))
            lr = loan_recommend(score, mi)
            st.caption('Loan recommendation')
            st.write(f"Status: {lr['status']} | Max Loan: {currency}{lr['max_loan_amount']:,.0f} | Safe EMI: {currency}{lr['recommended_emi']:,.0f}")
        st.subheader('Feature Contributions')
        cdf = interp_contrib(row, weights=weights_interp, cap_freq=cap_freq)
        b = alt.Chart(cdf).mark_bar().encode(x='contribution', y=alt.Y('feature', sort='-x'))
        st.altair_chart(b, use_container_width=True)
    elif method == 'Heuristic+Unsupervised':
        feats = engineer_features(df)
        model, X = train_unsupervised(df)
        mscore = model_trust_component(model, X)
        score = trust_score(feats, mscore)
        category = risk_category(score)
        eligible = predict_eligibility(score)
        rec = loan_recommendation(feats, score)
        color = risk_color(category)
        st.header('Trust Overview')
        top = st.container()
        c1, c2 = top.columns([1, 1])
        with c1:
            st.altair_chart(gauge_chart(score, color), use_container_width=False)
            st.altair_chart(health_meter(score, color), use_container_width=False)
        with c2:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.metric('TrustScore', f'{score:.1f}')
            st.markdown(f"<div class='badge' style='background:{color}'> {category} </div>", unsafe_allow_html=True)
            st.metric('Loan Eligibility', 'Yes' if eligible else 'No')
            st.markdown("</div>", unsafe_allow_html=True)
        st.header('Financial health indicator')
        if category == 'Low Risk':
            st.success('Healthy')
        elif category == 'Medium Risk':
            st.warning('Needs attention')
        else:
            st.error('Fragile')
        st.caption('Feature Summary')
        st.dataframe(pd.DataFrame(feats, index=['value']).T)
        st.caption('Loan recommendation')
        st.write(rec)
        mi = float(feats.get('income_mean', 0.0))
        lr = loan_recommend(score, mi)
        st.write(f"Status: {lr['status']} | Max Loan: {currency}{lr['max_loan_amount']:,.0f} | Safe EMI: {currency}{lr['recommended_emi']:,.0f}")
        st.subheader('Feature Contributions')
        parts = heuristic_contributions(feats, mscore)
        cdf = pd.DataFrame({'feature': list(parts.keys()), 'contribution': list(parts.values())})
        b = alt.Chart(cdf).mark_bar().encode(x='contribution', y=alt.Y('feature', sort='-x'))
        st.altair_chart(b, use_container_width=True)
    else:
        ufeats = engineer_user_features(df)
        cols = feature_columns(ufeats)
        X = ufeats[cols].fillna(0.0)
        model_path = 'model_rf.pkl' if os.path.exists('model_rf.pkl') else ('model_logreg.pkl' if os.path.exists('model_logreg.pkl') else None)
        if not model_path:
            st.warning('No trained supervised model found. Train via scripts/train_trust_model.py')
        else:
            model = joblib.load(model_path)
            proba = model.predict_proba(X)[:, 1]
            score = float(min(max(proba[0] * 100.0, 0.0), 100.0))
            category = risk_category(score)
            eligible = predict_eligibility(score)
            color = risk_color(category)
            st.header('Trust Overview')
            top = st.container()
            c1, c2 = top.columns([1, 1])
            with c1:
                st.altair_chart(gauge_chart(score, color), use_container_width=False)
                st.altair_chart(health_meter(score, color), use_container_width=False)
            with c2:
                st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
                st.metric('TrustScore', f'{score:.1f}')
                st.markdown(f"<div class='badge' style='background:{color}'> {category} </div>", unsafe_allow_html=True)
                st.metric('Loan Eligibility', 'Yes' if eligible else 'No')
                st.markdown("</div>", unsafe_allow_html=True)
            st.header('Financial health indicator')
            if category == 'Low Risk':
                st.success('Healthy')
            elif category == 'Medium Risk':
                st.warning('Needs attention')
            else:
                st.error('Fragile')
            st.caption('Per-user features')
            st.dataframe(ufeats)
            if len(ufeats):
                mi = float(ufeats.iloc[0].get('mean_monthly_income', 0.0))
                lr = loan_recommend(score, mi)
                st.caption('Loan recommendation')
                st.write(f"Status: {lr['status']} | Max Loan: {currency}{lr['max_loan_amount']:,.0f} | Safe EMI: {currency}{lr['recommended_emi']:,.0f}")
            st.subheader('Feature Importance')
            if hasattr(model, 'named_steps') and 'clf' in model.named_steps:
                clf = model.named_steps['clf']
                if hasattr(clf, 'feature_importances_'):
                    imp = clf.feature_importances_
                    cdf = pd.DataFrame({'feature': cols, 'importance': imp})
                elif hasattr(clf, 'coef_'):
                    imp = abs(clf.coef_[0])
                    cdf = pd.DataFrame({'feature': cols, 'importance': imp})
                else:
                    cdf = pd.DataFrame({'feature': cols, 'importance': [0.0 for _ in cols]})
                b = alt.Chart(cdf).mark_bar().encode(x='importance', y=alt.Y('feature', sort='-x'))
                st.altair_chart(b, use_container_width=True)
            if hasattr(model, 'named_steps') and 'clf' in model.named_steps:
                clf = model.named_steps['clf']
                if hasattr(clf, 'coef_'):
                    xrow = X.iloc[0:1]
                    if 'scaler' in model.named_steps:
                        xscaled = model.named_steps['scaler'].transform(xrow)
                    else:
                        xscaled = xrow.values
                    contrib = abs(clf.coef_[0] * xscaled[0])
                    cdf_local = pd.DataFrame({'feature': cols, 'contribution': contrib})
                    st.subheader('Local Contributions (LogReg)')
                    b2 = alt.Chart(cdf_local).mark_bar().encode(x='contribution', y=alt.Y('feature', sort='-x'))
                    st.altair_chart(b2, use_container_width=True)
