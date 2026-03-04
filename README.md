# BWT_TEAM-KANYARASHI-
Future Finance Platforms:


Problem Statement B : The Invisible 400 Million 
This is a Trae AI project

# CredPulse AI

### Behavioral Credit Identity for the Invisible Workforce

CredPulse AI is an AI-powered alternative credit scoring system designed to help gig workers and financially underserved individuals access credit without traditional financial records.

The system analyzes digital transaction behavior and converts it into a **TrustScore**, enabling fair and inclusive access to micro-loans and financial services.

---

## Problem Statement

Millions of gig workers earn consistently through digital payments such as UPI but lack formal financial records like salary slips or credit history.

Traditional credit scoring systems rely on banking data and formal employment records, which excludes this large population from accessing loans, insurance, and financial growth opportunities.

---

## Our Solution

CredPulse AI analyzes transaction behavior and generates a **behavior-based credit identity**.

Instead of relying on traditional credit history, the system evaluates:

* Income consistency
* Spending patterns
* Savings behavior
* Transaction frequency
* Cash flow stability

Using these behavioral signals, the system generates a **TrustScore (0–100)** and recommends appropriate financial opportunities.

---

## Key Features

### Behavioral TrustScore

Generates a credit score based on financial behavior patterns instead of traditional credit reports.

### Loan Recommendation Engine

Suggests safe loan amounts and EMI plans based on the generated TrustScore.

### Financial Health Dashboard

Provides a visual overview of the user's financial stability.

### Explainable AI

Displays which behavioral factors influenced the TrustScore to ensure transparency.

### Future Financial Simulation

Allows users to simulate income or expense changes and see how their TrustScore changes.

---


## System Architecture

```
User Transaction Data
        │
        ▼
Feature Engineering Layer
(income stability, spending ratio, etc.)
        │
        ▼
Machine Learning Model
(Random Forest Classifier)
        │
        ▼
TrustScore Engine
(Score generation)
        │
        ▼
Recommendation Engine
(Loan eligibility + EMI suggestion)
        │
        ▼
Explainability Layer
(Feature importance insights)
        │
        ▼
Streamlit Dashboard
(User Interface)
```

---

## Tech Stack

**Frontend / UI**

* Streamlit

**Backend**

* Python

**Machine Learning**

* Scikit-learn
* Random Forest Classifier

**Data Processing**

* Pandas
* NumPy

**Visualization**

* Plotly
* Matplotlib

---

## Project Structure

```
credpulse-ai
│
├── data
│   └── transactions.csv
│
├── utils
│   └── feature_engineering.py
│
├── models
│   └── train_model.py
│
├── app
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
```

---

## How to Run the Project

### 1. Clone the repository

```
git clone https://github.com/yourusername/credpulse-ai.git
cd credpulsee-ai
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the application

```
streamlit run app/streamlit_app.py
```

Open the browser and navigate to

```
http://localhost:8501
```

---

## Demo Workflow

1. Upload transaction dataset
2. System analyzes financial behavior
3. TrustScore is generated
4. Dashboard displays risk level and loan eligibility
5. Simulation tool shows how financial changes affect the score

---

## Future Improvements

* Integration with real UPI transaction APIs
* Federated learning for privacy-preserving credit scoring
* Mobile application for gig workers
* Integration with microfinance institutions

---

## Impact

CredPulse AI promotes **financial inclusion** by enabling access to credit for millions of individuals who are invisible to traditional banking systems.

By converting financial behavior into a digital credit identity, this system can empower gig workers and underserved communities worldwide.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

Built for a fintech hackathon to explore AI-driven solutions for financial inclusion.
