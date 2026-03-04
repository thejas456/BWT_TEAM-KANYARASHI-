import sys
import os
import pandas as pd

def main():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.interpretable_scoring import apply_scores
    path = 'features_per_user.csv'
    cap_freq = 10.0
    for a in sys.argv[1:]:
        if a.startswith('--cap-freq='):
            try:
                cap_freq = float(a.split('=', 1)[1])
            except Exception:
                pass
        elif not a.startswith('--'):
            path = a
    df = pd.read_csv(path)
    out = apply_scores(df, cap_freq=cap_freq)
    out.to_csv('trust_scores_interpretable.csv', index=False)
    print(out.head(10).to_string(index=False))

if __name__ == '__main__':
    main()
