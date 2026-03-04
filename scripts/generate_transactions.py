import csv
import random
from datetime import datetime, timedelta

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

def random_timestamp(days_back=180):
    start = datetime.now() - timedelta(days=days_back)
    delta = datetime.now() - start
    sec = random.randint(0, int(delta.total_seconds()))
    dt = start + timedelta(seconds=sec)
    hour = weighted_choice(list(range(6, 24)), [2 if 18 <= h <= 22 else 1 for h in range(6, 24)])
    dt = dt.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59), microsecond=0)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def gen_amount(cat, ttype):
    if ttype == 'income':
        if cat in ['Ride Platform Payout', 'Food Delivery Payout']:
            return round(random.uniform(300, 2000), 2)
        if cat in ['E-commerce Marketplace', 'Freelance Platform']:
            return round(random.uniform(800, 5000), 2)
        if cat == 'Tips':
            return round(random.uniform(20, 300), 2)
        if cat == 'Bonus':
            return round(random.uniform(200, 800), 2)
        return round(random.uniform(200, 2500), 2)
    else:
        if cat == 'Fuel':
            return round(random.uniform(200, 1200), 2)
        if cat == 'Groceries':
            return round(random.uniform(100, 800), 2)
        if cat in ['Mobile/Data', 'Utilities']:
            return round(random.uniform(100, 1500), 2)
        if cat == 'Food & Drink':
            return round(random.uniform(50, 600), 2)
        if cat == 'Transport':
            return round(random.uniform(50, 300), 2)
        if cat == 'Rent':
            return round(random.uniform(2500, 10000), 2)
        if cat in ['Subscription', 'EMI/Loan']:
            return round(random.uniform(300, 5000), 2)
        if cat == 'Healthcare':
            return round(random.uniform(300, 5000), 2)
        return round(random.uniform(50, 1000), 2)

def gen_payment_method(ttype, cat):
    if ttype == 'income':
        if cat in ['Ride Platform Payout', 'Food Delivery Payout', 'E-commerce Marketplace', 'Freelance Platform', 'Bonus']:
            return weighted_choice(['bank_transfer', 'upi', 'wallet'], [6, 3, 1])
        if cat == 'Tips':
            return weighted_choice(['upi', 'cash'], [7, 3])
    else:
        if cat in ['Groceries', 'Food & Drink', 'Transport', 'Subscription']:
            return weighted_choice(['upi', 'card', 'cash'], [6, 2, 2])
        if cat in ['Fuel', 'Utilities', 'EMI/Loan', 'Rent', 'Healthcare']:
            return weighted_choice(['bank_transfer', 'card', 'upi', 'cash'], [4, 2, 3, 1])
    return weighted_choice(['upi', 'bank_transfer', 'card', 'cash'], [5, 3, 1, 1])

def main(out_path='transactions.csv', rows=1000):
    random.seed(42)
    users = [f'GW{str(i).zfill(3)}' for i in range(1, 61)]
    income_cats = ['Ride Platform Payout', 'Food Delivery Payout', 'E-commerce Marketplace', 'Freelance Platform', 'Tips', 'Bonus']
    expense_cats = ['Fuel', 'Groceries', 'Mobile/Data', 'Food & Drink', 'Transport', 'Rent', 'Utilities', 'Subscription', 'EMI/Loan', 'Healthcare']
    locations = ['Bengaluru', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']
    devices = ['android', 'ios']
    rows_data = []
    for _ in range(rows):
        user_id = weighted_choice(users, [1 for _ in users])
        ttype = weighted_choice(['income', 'expense'], [3, 7])
        cat = weighted_choice(income_cats if ttype == 'income' else expense_cats,
                              [3, 3, 2, 2, 2, 1] if ttype == 'income' else [2, 3, 2, 3, 2, 1, 2, 2, 2, 1])
        amount = gen_amount(cat, ttype)
        ts = random_timestamp(180)
        pm = gen_payment_method(ttype, cat)
        loc = weighted_choice(locations, [4, 4, 3, 3, 3, 3, 2, 2, 2, 2])
        device = weighted_choice(devices, [7, 3])
        rows_data.append({
            'user_id': user_id,
            'transaction_amount': amount,
            'transaction_type': ttype,
            'timestamp': ts,
            'merchant_category': cat,
            'payment_method': pm,
            'location': loc,
            'device_type': device
        })
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['user_id', 'transaction_amount', 'transaction_type', 'timestamp', 'merchant_category', 'payment_method', 'location', 'device_type'])
        w.writeheader()
        for r in rows_data:
            w.writerow(r)

if __name__ == '__main__':
    main()
