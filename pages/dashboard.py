import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Abhedya MuleNet | Cyber Cell",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Professional dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@300;400;600&display=swap');
    
    .stApp { 
        background: #05070f;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 255, 170, 0.05) 0%, transparent 50%),
            linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 { 
        font-family: 'Orbitron', sans-serif !important; 
        color: #00FFAA;
        letter-spacing: 1px;
    }
    p, div, span { font-family: 'JetBrains Mono', monospace; }
    
    [data-testid="stMetricValue"] {
        color: #00FFAA !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 32px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8899aa !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .alert-card {
        background: linear-gradient(90deg, rgba(255, 51, 85, 0.15), rgba(19, 24, 41, 0.6));
        border-left: 4px solid #FF3355;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 8px 0;
        backdrop-filter: blur(10px);
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; color: #00FFAA;">🛡️ ABHEDYA MULENET</h1>
    <p style="color: #8899aa; margin: 5px 0 0 0; font-family: Consolas;">
        Real-Time Mule Account Detection System | Indore Police Cyber Cell
    </p>
</div>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv('transactions_with_risk.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Refresh button
col_refresh, col_time = st.columns([1, 4])
with col_refresh:
    if st.button("🔄 Refresh Feed"):
        st.rerun()
with col_time:
    st.markdown(f"<p style='color:#8899aa; text-align:right; font-family:Consolas;'>Last updated: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# Top KPIs
critical = df[df['risk_score'] >= 70]
suspicious = df[(df['risk_score'] >= 45) & (df['risk_score'] < 70)]
safe = df[df['risk_score'] < 45]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📊 Total Txns", f"{len(df):,}")
col2.metric("🚨 Critical", f"{len(critical)}", delta=f"{len(critical)}", delta_color="inverse")
col3.metric("⚠️ Suspicious", f"{len(suspicious)}")
col4.metric("✅ Safe", f"{len(safe):,}")
col5.metric("💰 At Risk", f"₹{critical['amount'].sum()/100000:.1f}L", delta_color="inverse")

st.markdown("---")

# Main layout
left, right = st.columns([3, 2])

with left:
    st.markdown("### 🚨 Live Threat Feed")
    st.markdown("<p style='color:#8899aa; font-size:13px;'>Real-time detection of mule account activity</p>", unsafe_allow_html=True)
    
    for _, row in critical.nlargest(8, 'amount').iterrows():
        st.markdown(f"""
        <div class="alert-card">
            <span style="color:#FF3355; font-weight:bold;">⚠️ {row['verdict']}</span>
            <span style="color:#8899aa; float:right;">{row['timestamp'].strftime('%d %b, %H:%M')}</span><br>
            <span style="color:#FFFFFF;">
            <b>{row['txn_id']}</b> | ₹<b>{row['amount']:,}</b> via {row['channel']}<br>
            <span style="color:#8899aa; font-size:13px;">
            From: {row['sender_name'][:25]} | To: {row['receiver_name'][:25]}<br>
            📍 {row['city']} | 🏦 {row['bank']} | Risk: <b style="color:#FF3355;">{row['risk_score']}/100</b><br>
            🔍 Pattern: <i>{row['pattern']}</i>
            </span>
            </span>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("### 📊 Attack Analytics")
    
    # Attack locations
    loc_data = critical.groupby('city').size().reset_index(name='count').sort_values('count', ascending=True)
    fig1 = px.bar(loc_data, x='count', y='city', orientation='h',
                   color='count', color_continuous_scale=['#00FFAA', '#FFAA00', '#FF3355'],
                   title="Fraud Hotspots")
    fig1.update_layout(
        paper_bgcolor='#0a0e1a', plot_bgcolor='#131829',
        font=dict(color='#FFFFFF', family='Consolas'),
        showlegend=False, height=280,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Hourly pattern
    hour_data = critical.groupby(critical['timestamp'].dt.hour).size().reset_index(name='count')
    fig2 = px.area(hour_data, x='timestamp', y='count',
                    color_discrete_sequence=['#FF3355'],
                    title="Attack Timing (Hourly)")
    fig2.update_layout(
        paper_bgcolor='#0a0e1a', plot_bgcolor='#131829',
        font=dict(color='#FFFFFF', family='Consolas'),
        showlegend=False, height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Hour of Day", yaxis_title="Alerts"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Bottom - Network graph preview
st.markdown("### 🕸️ Network Graph Preview (Sample)")
st.markdown("<p style='color:#8899aa; font-size:13px;'>Connected accounts identified by AI</p>", unsafe_allow_html=True)

# Top 3 dangerous accounts
top_accounts = critical.groupby('receiver_account').agg({
    'amount': 'sum',
    'risk_score': 'max',
    'txn_id': 'count'
}).sort_values('risk_score', ascending=False).head(3)

cols = st.columns(3)
for i, (acc_id, data) in enumerate(top_accounts.iterrows()):
    with cols[i]:
        st.markdown(f"""
        <div class="metric-box">
            <p style="color:#FF3355; margin:0; font-size:12px;">🚨 FLAGGED ACCOUNT</p>
            <h4 style="color:#00FFAA; margin:8px 0; font-family:Consolas;">****{str(acc_id)[-4:]}</h4>
            <p style="color:#FFFFFF; margin:5px 0;"><b>{int(data['txn_id'])}</b> transactions linked</p>
            <p style="color:#FFFFFF; margin:5px 0;">₹<b>{int(data['amount']):,}</b> moved</p>
            <p style="color:#FF3355; margin:5px 0;">Risk: <b>{int(data['risk_score'])}/100</b></p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Footer
col_a, col_b, col_c = st.columns(3)
col_a.success("✅ AI Engine: Active")
col_b.success("🛡️ Protection: Online")
col_c.success(f"📡 Monitoring: {len(df):,} transactions")

st.markdown("<p style='text-align:center; color:#556677; font-family:Consolas; font-size:12px;'>Abhedya MuleNet v2.0 | Void Hacks() 8.0 | Built for Indore Police Cyber Cell</p>", unsafe_allow_html=True)



st.markdown("---")

# ==================== NETWORK GRAPH SECTION ====================
st.markdown("### 🕸️ Criminal Network Graph")
st.markdown("<p style='color:#8899aa; font-size:13px;'>Click on any node to see account details. Node size = connections. Color = risk score.</p>", unsafe_allow_html=True)

# Load the network graph HTML in an iframe
import streamlit.components.v1 as components

try:
    with open('network_graph.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=650, scrolling=True)
except FileNotFoundError:
    st.warning("⚠️ Run `python network_graph.py` first to generate the network graph.")