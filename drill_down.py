import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Account Investigation | Abhedya MuleNet",
    page_icon="🔍",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; }
    h1, h2, h3 { color: #00FFAA; font-family: 'Consolas', monospace; }
    .account-card {
        background: linear-gradient(135deg, #1a1f3a, #131829);
        border: 2px solid #FF3355;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    .info-box {
        background: #131829;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00FFAA;
        margin: 8px 0;
        font-family: 'Consolas', monospace;
    }
    .txn-row {
        background: #0a0e1a;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-family: 'Consolas', monospace;
        border-left: 3px solid #2a3050;
    }
    .txn-row.fraud {
        border-left: 3px solid #FF3355;
        background: linear-gradient(90deg, #1a0000, #0a0e1a);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔍 ACCOUNT INVESTIGATION TOOL")
st.markdown("<p style='color:#8899aa;'>Click any account to view complete investigation report</p>", unsafe_allow_html=True)
st.markdown("---")

# Load data
df = pd.read_csv('transactions_with_risk.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# High-risk accounts
high_risk = df[df['risk_score'] >= 60]

# Group by receiver account
account_summary = high_risk.groupby('receiver_account').agg({
    'amount': ['sum', 'count', 'mean'],
    'risk_score': 'max',
    'timestamp': ['min', 'max'],
    'city': lambda x: x.mode()[0] if len(x) > 0 else 'Unknown',
    'bank': lambda x: x.mode()[0] if len(x) > 0 else 'Unknown'
}).reset_index()

account_summary.columns = ['account', 'total_amount', 'txn_count', 'avg_amount', 
                            'max_risk', 'first_seen', 'last_seen', 'city', 'bank']
account_summary = account_summary.sort_values('max_risk', ascending=False).head(20)

# ============================================
# SIDEBAR - Account Selector
# ============================================
st.sidebar.markdown("### 🎯 Flagged Accounts")
st.sidebar.markdown(f"<p style='color:#8899aa; font-size:12px;'>{len(account_summary)} accounts under investigation</p>", unsafe_allow_html=True)

selected = st.sidebar.radio(
    "Select account to investigate:",
    options=account_summary['account'].tolist(),
    format_func=lambda x: f"****{str(x)[-4:]} (Risk: {int(account_summary[account_summary['account']==x]['max_risk'].values[0])})"
)

# ============================================
# MAIN AREA - Investigation Report
# ============================================
if selected:
    acc_data = account_summary[account_summary['account'] == selected].iloc[0]
    acc_txns = df[df['receiver_account'] == selected].sort_values('timestamp', ascending=False)
    acc_sent = df[df['sender_account'] == selected].sort_values('timestamp', ascending=False)
    
    # Header
    st.markdown(f"""
    <div class="account-card">
        <p style="color: #8899aa; margin: 0; font-size: 13px;">🚨 UNDER INVESTIGATION</p>
        <h2 style="color: #FF3355; margin: 5px 0; font-family: Consolas;">ACCOUNT ****{str(selected)[-4:]}</h2>
        <p style="color: #FFFFFF; margin: 5px 0;">Full ID: <b>{selected}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🚨 Risk Score", f"{int(acc_data['max_risk'])}/100", delta="CRITICAL", delta_color="inverse")
    col2.metric("💰 Total Amount", f"₹{int(acc_data['total_amount']):,}")
    col3.metric("📊 Transactions", int(acc_data['txn_count']))
    col4.metric("📍 Primary City", acc_data['city'])
    
    st.markdown("---")
    
    # Two columns
    left, right = st.columns([1, 1])
    
    with left:
        st.markdown("### 🏦 Account Details")
        st.markdown(f"""
        <div class="info-box">
            <b style="color:#00FFAA;">Bank:</b> {acc_data['bank']}<br>
            <b style="color:#00FFAA;">City:</b> {acc_data['city']}<br>
            <b style="color:#00FFAA;">First Flagged:</b> {acc_data['first_seen'].strftime('%d %b %Y, %H:%M')}<br>
            <b style="color:#00FFAA;">Last Activity:</b> {acc_data['last_seen'].strftime('%d %b %Y, %H:%M')}<br>
            <b style="color:#00FFAA;">Avg Transaction:</b> ₹{int(acc_data['avg_amount']):,}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚠️ AI Detection Reasons")
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #FF3355;">
            🚩 High-value transactions (>₹40,000)<br>
            🚩 Late-night activity (1 AM - 4 AM)<br>
            🚩 Rapid in-and-out money flow<br>
            🚩 Connected to {int(acc_data['txn_count'])} suspicious transfers<br>
            🚩 Geographic anomaly detected
        </div>
        """, unsafe_allow_html=True)
        
        # Freeze button
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚨 FREEZE ACCOUNT", type="primary", use_container_width=True):
                st.success("✅ Account frozen. Alert sent to Cyber Cell.")
        with col_b:
            if st.button("📤 Report to I4C", use_container_width=True):
                st.info("📡 Reported to Indian Cyber Crime Coordination Centre")
    
    with right:
        st.markdown(f"### 📥 Incoming Transactions ({len(acc_txns)})")
        for _, row in acc_txns.head(8).iterrows():
            fraud_class = "txn-row fraud" if row['risk_score'] >= 60 else "txn-row"
            st.markdown(f"""
            <div class="{fraud_class}">
                <span style="color:#00FFAA;">{row['txn_id']}</span>
                <span style="color:#8899aa; float:right;">{row['timestamp'].strftime('%d %b %H:%M')}</span><br>
                <span style="color:#FFFFFF;">₹<b>{row['amount']:,}</b> from {str(row['sender_name'])[:20]}</span><br>
                <span style="color:#8899aa; font-size:12px;">
                Risk: <b style="color:#FF3355;">{row['risk_score']}/100</b> | 
                {row['channel']} | 📍 {row['city']}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"### 📤 Outgoing Transactions ({len(acc_sent)})")
        for _, row in acc_sent.head(5).iterrows():
            st.markdown(f"""
            <div class="txn-row">
                <span style="color:#00FFAA;">{row['txn_id']}</span>
                <span style="color:#8899aa; float:right;">{row['timestamp'].strftime('%d %b %H:%M')}</span><br>
                <span style="color:#FFFFFF;">₹<b>{row['amount']:,}</b> to {str(row['receiver_name'])[:20]}</span><br>
                <span style="color:#8899aa; font-size:12px;">
                {row['channel']} | 📍 {row['city']}
                </span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Abhedya MuleNet | Account Investigation Tool | Void Hacks() 8.0")