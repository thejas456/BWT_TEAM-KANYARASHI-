import sys
import os
import pandas as pd

def main():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.user_features import engineer_user_features
    path = 'transactions.csv'
    income_threshold = 1000.0
    relative = False
    relative_factor = 0.6
    freq = 'week'
    for a in sys.argv[1:]:
        if a.startswith('--income-threshold='):
            try:
                income_threshold = float(a.split('=', 1)[1])
            except Exception:
                pass
        elif a.startswith('--relative='):
            v = a.split('=', 1)[1].strip().lower()
            relative = v in ['1', 'true', 'yes', 'y']
        elif a.startswith('--relative-factor='):
            try:
                relative_factor = float(a.split('=', 1)[1])
            except Exception:
                pass
        elif a.startswith('--freq='):
            v = a.split('=', 1)[1].strip().lower()
            if v in ['week', 'month']:
                freq = v
        elif not a.startswith('--'):
            path = a
    df = pd.read_csv(path)
    feats = engineer_user_features(
        df,
        income_threshold=income_threshold,
        weekly=(freq == 'week'),
        relative_threshold=relative,
        relative_factor=relative_factor
    )
    feats.to_csv('features_per_user.csv', index=False)
    print(feats.head(10).to_string(index=False))

if __name__ == '__main__':
    main()
