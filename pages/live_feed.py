import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

st.set_page_config(
    page_title="Live Feed | Abhedya MuleNet",
    page_icon="📡",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; }
    h1, h2, h3 { color: #00FFAA; font-family: 'Consolas', monospace; }
    .live-txn {
        background: #131829;
        border-left: 4px solid #00FFAA;
        padding: 12px;
        border-radius: 5px;
        margin: 8px 0;
        font-family: 'Consolas', monospace;
        animation: slideIn 0.5s ease-out;
    }
    .live-txn.fraud {
        background: linear-gradient(90deg, #2a0000, #1a0000);
        border-left: 4px solid #FF3355;
        animation: pulse 1s infinite;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 51, 85, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 51, 85, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 51, 85, 0); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📡 LIVE TRANSACTION FEED")
st.markdown("<p style='color:#8899aa;'>Real-time monitoring | Indore Police Cyber Cell</p>", unsafe_allow_html=True)
st.markdown("---")

# Names
NAMES = ['Rahul Sharma', 'Priya Verma', 'Amit Patel', 'Sneha Gupta', 'Vikram Singh',
         'Pooja Jain', 'Arjun Reddy', 'Neha Agarwal', 'Rohit Kumar', 'Anjali Mishra']
CITIES = ['Indore', 'Bhopal', 'Delhi', 'Mumbai', 'Jaipur', 'Pune', 'Bangalore']
CHANNELS = ['UPI', 'IMPS', 'NEFT', 'ATM']

# Session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'stats' not in st.session_state:
    st.session_state.stats = {'total': 0, 'fraud': 0, 'safe': 0, 'amount_saved': 0}

# Controls
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("▶️ Start Live Feed", type="primary"):
        st.session_state.running = True
with col2:
    if st.button("⏹️ Stop"):
        st.session_state.running = False
with col3:
    st.markdown("<p style='color:#8899aa; text-align:right;'>Refresh rate: 2 seconds</p>", unsafe_allow_html=True)

# Stats
st.markdown("---")
s1, s2, s3, s4 = st.columns(4)
stats_placeholder = st.empty()

with stats_placeholder.container():
    s1.metric("📊 Total Txns", st.session_state.stats['total'])
    s2.metric("🚨 Fraud Blocked", st.session_state.stats['fraud'])
    s3.metric("✅ Legitimate", st.session_state.stats['safe'])
    s4.metric("💰 Money Saved", f"₹{st.session_state.stats['amount_saved']:,}")

st.markdown("---")
st.markdown("### 🔴 Live Feed")

feed_container = st.container()

# Simulate transactions
def generate_transaction():
    is_fraud = random.random() < 0.15  # 15% fraud
    
    if is_fraud:
        amount = random.randint(45000, 95000)
        hour = random.choice([1, 2, 3, 4])  # Late night
        city = random.choice(['Indore', 'Bhopal', 'Jaipur', 'Delhi'])
        risk = random.randint(85, 99)
        return {
            'txn_id': f"TXN{random.randint(100000, 999999)}",
            'sender': random.choice(NAMES),
            'receiver': random.choice(NAMES),
            'amount': amount,
            'city': city,
            'channel': random.choice(['IMPS', 'UPI']),
            'time': datetime.now().strftime('%H:%M:%S'),
            'risk': risk,
            'is_fraud': True
        }
    else:
        amount = random.randint(100, 25000)
        return {
            'txn_id': f"TXN{random.randint(100000, 999999)}",
            'sender': random.choice(NAMES),
            'receiver': random.choice(NAMES),
            'amount': amount,
            'city': random.choice(CITIES),
            'channel': random.choice(CHANNELS),
            'time': datetime.now().strftime('%H:%M:%S'),
            'risk': random.randint(15, 40),
            'is_fraud': False
        }

# Render feed
with feed_container:
    if st.session_state.running:
        # Generate new transaction
        txn = generate_transaction()
        st.session_state.transactions.insert(0, txn)
        
        # Update stats
        st.session_state.stats['total'] += 1
        if txn['is_fraud']:
            st.session_state.stats['fraud'] += 1
            st.session_state.stats['amount_saved'] += txn['amount']
        else:
            st.session_state.stats['safe'] += 1
        
        # Keep only last 15
        st.session_state.transactions = st.session_state.transactions[:15]
        
        # Display
        for txn in st.session_state.transactions:
            css_class = "live-txn fraud" if txn['is_fraud'] else "live-txn"
            icon = "🚨" if txn['is_fraud'] else "✅"
            label = "FRAUD BLOCKED" if txn['is_fraud'] else "APPROVED"
            color = "#FF3355" if txn['is_fraud'] else "#00FFAA"
            
            st.markdown(f"""
            <div class="{css_class}">
                <span style="color: {color}; font-weight: bold;">{icon} {label}</span>
                <span style="color: #8899aa; float: right;">{txn['time']}</span><br>
                <span style="color: #FFFFFF;">
                <b>{txn['txn_id']}</b> | ₹<b>{txn['amount']:,}</b> via {txn['channel']}<br>
                <span style="color: #8899aa; font-size: 13px;">
                {txn['sender'][:20]} → {txn['receiver'][:20]} | 📍 {txn['city']}
                | Risk: <b style="color:{color};">{txn['risk']}/100</b>
                </span>
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Auto refresh
        time.sleep(2)
        st.rerun()
    else:
        if not st.session_state.transactions:
            st.info("👆 Click 'Start Live Feed' to begin monitoring")
        else:
            for txn in st.session_state.transactions:
                css_class = "live-txn fraud" if txn['is_fraud'] else "live-txn"
                icon = "🚨" if txn['is_fraud'] else "✅"
                label = "FRAUD BLOCKED" if txn['is_fraud'] else "APPROVED"
                color = "#FF3355" if txn['is_fraud'] else "#00FFAA"
                
                st.markdown(f"""
                <div class="{css_class}">
                    <span style="color: {color}; font-weight: bold;">{icon} {label}</span>
                    <span style="color: #8899aa; float: right;">{txn['time']}</span><br>
                    <span style="color: #FFFFFF;">
                    <b>{txn['txn_id']}</b> | ₹<b>{txn['amount']:,}</b> via {txn['channel']}<br>
                    <span style="color: #8899aa; font-size: 13px;">
                    {txn['sender'][:20]} → {txn['receiver'][:20]} | 📍 {txn['city']}
                    | Risk: <b style="color:{color};">{txn['risk']}/100</b>
                    </span>
                    </span>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Abhedya MuleNet | Live Monitoring System | Void Hacks() 8.0")