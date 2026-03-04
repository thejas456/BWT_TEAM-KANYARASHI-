import sys
import os
import pandas as pd
import joblib

def main():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.supervised_model import train
    path = 'features_per_user.csv'
    model_type = 'rf'
    for a in sys.argv[1:]:
        if a.startswith('--model='):
            v = a.split('=', 1)[1].strip().lower()
            if v in ['rf', 'logreg']:
                model_type = v
        elif not a.startswith('--'):
            path = a
    df = pd.read_csv(path)
    model, scores_df, report = train(df, model_type=model_type)
    joblib.dump(model, f'model_{model_type}.pkl')
    scores_df.to_csv('trust_scores.csv', index=False)
    print(report)
    print(scores_df.head(10).to_string(index=False))

if __name__ == '__main__':
    main()
