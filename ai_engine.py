import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

print("🧠 Abhedya AI Engine v2.1 starting...\n")

df = pd.read_csv('transactions.csv')
print(f"📊 Loaded {len(df)} transactions")

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour

# Feature engineering
df['amount_log'] = np.log1p(df['amount'])
df['is_late_night'] = ((df['hour'] >= 1) & (df['hour'] <= 5)).astype(int)
df['is_high_value'] = (df['amount'] > 40000).astype(int)

features = df[['amount_log', 'hour', 'is_late_night', 'is_high_value']]

# Train model
model = IsolationForest(
    contamination=0.12,   # Increased from 0.06
    random_state=42,
    n_estimators=100
)
model.fit(features)

# FIXED risk score calculation
scores = model.decision_function(features)   # Lower = more anomalous
neg_scores = -scores                          # Higher = more anomalous

# Normalize to 0-100
min_s, max_s = neg_scores.min(), neg_scores.max()
df['risk_score'] = ((neg_scores - min_s) / (max_s - min_s) * 100).round(0).astype(int)

# Verdict
def get_verdict(score):
    if score >= 70: return '🚨 CRITICAL'
    elif score >= 45: return '⚠️ SUSPICIOUS'
    else: return '✅ SAFE'

df['verdict'] = df['risk_score'].apply(get_verdict)

# Pattern detection
def detect_pattern(row):
    reasons = []
    if row['amount'] > 40000: reasons.append('High amount')
    if 1 <= row['hour'] <= 5: reasons.append('Late-night')
    if row['is_high_value'] == 1 and row['is_late_night'] == 1:
        reasons.append('High-value + late-night')
    return ' | '.join(reasons) if reasons else 'Normal pattern'

df['pattern'] = df.apply(detect_pattern, axis=1)

df.to_csv('transactions_with_risk.csv', index=False)

critical = df[df['risk_score'] >= 70]
suspicious = df[(df['risk_score'] >= 45) & (df['risk_score'] < 70)]

print("=" * 60)
print(f"🚨 Critical: {len(critical)}")
print(f"⚠️  Suspicious: {len(suspicious)}")
print(f"✅ Safe: {len(df[df['risk_score'] < 45])}")
print("=" * 60)
print(f"\n💰 At-risk amount: ₹{critical['amount'].sum():,}")

if len(critical) > 0:
    print("\n🚨 Top 5 CRITICAL:")
    for _, row in critical.nlargest(5, 'amount').iterrows():
        print(f"  {row['txn_id']} | ₹{row['amount']:,} | {row['city']} | Risk: {row['risk_score']} | {row['pattern']}")