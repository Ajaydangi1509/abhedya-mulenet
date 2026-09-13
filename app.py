import streamlit as st

# ==================== LOGO ====================
st.set_page_config(
    page_title="Abhedya MuleNet | Cyber Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================== ULTRA CYBER CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@300;400;600&display=swap');
    
    /* Global */
    .stApp { 
        background: #05070f;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 255, 170, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 51, 85, 0.05) 0%, transparent 50%),
            linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, h4 { 
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
    }
    p, div, span, li { font-family: 'JetBrains Mono', monospace; }
    
    /* HERO SECTION */
    .hero-container {
    position: relative;
    text-align: center;
    padding: 5px 20px 30px 20px;
    border-bottom: 1px solid rgba(0, 255, 170, 0.2);
    margin-bottom: 30px;
}
    
    .hero-badge {
        display: inline-block;
        background: rgba(0, 255, 170, 0.1);
        border: 1px solid #00FFAA;
        color: #00FFAA;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 20px;
        font-family: 'JetBrains Mono', monospace;
        animation: pulse-glow 2s infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 170, 0.3); }
        50% { box-shadow: 0 0 25px rgba(0, 255, 170, 0.6); }
    }
    
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 64px;
        font-weight: 900;
        background: linear-gradient(135deg, #00FFAA 0%, #00D4FF 50%, #FF3355 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 10px 0;
        letter-spacing: 4px;
        text-shadow: 0 0 40px rgba(0, 255, 170, 0.3);
    }
    
    .hero-subtitle {
        color: #8899aa;
        font-size: 16px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 10px 0 20px 0;
    }
    
    .hero-tagline {
        color: #FF3355;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        letter-spacing: 2px;
    }
    
    /* LIVE STATUS BAR */
    .status-bar {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 25px 0;
        padding: 15px;
        background: rgba(19, 24, 41, 0.6);
        border: 1px solid rgba(0, 255, 170, 0.2);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #8899aa;
        font-size: 13px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00FFAA;
        box-shadow: 0 0 10px #00FFAA;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* GLASS CARDS */
    .glass-card {
        background: linear-gradient(135deg, rgba(19, 24, 41, 0.8), rgba(10, 14, 26, 0.6));
        border: 1px solid rgba(0, 255, 170, 0.2);
        border-radius: 16px;
        padding: 28px;
        backdrop-filter: blur(20px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00FFAA, transparent);
        transition: left 0.6s ease;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        border-color: #00FFAA;
        box-shadow: 0 0 40px rgba(0, 255, 170, 0.2);
        transform: translateY(-4px);
    }
    
    /* STAT CARDS */
    .stat-card {
        background: linear-gradient(135deg, rgba(255, 51, 85, 0.1), rgba(19, 24, 41, 0.9));
        border-left: 3px solid #FF3355;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .stat-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        font-weight: 900;
        color: #FF3355;
        margin: 5px 0;
        text-shadow: 0 0 20px rgba(255, 51, 85, 0.4);
    }
    
    .stat-label {
        color: #8899aa;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* NODE VISUALIZATION */
    .node-grid {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .node {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #FF3355;
        box-shadow: 0 0 15px #FF3355;
        animation: node-pulse 2s infinite;
    }
    
    @keyframes node-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    /* TERMINAL */
    .terminal-box {
        background: #0a0e1a;
        border: 1px solid rgba(0, 255, 170, 0.3);
        border-radius: 10px;
        padding: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #00FFAA;
        position: relative;
    }
    
    .terminal-header {
        display: flex;
        gap: 6px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(0, 255, 170, 0.2);
    }
    
    .terminal-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    
    .terminal-line {
        color: #8899aa;
        margin: 5px 0;
    }
    
    .terminal-line .cmd {
        color: #00FFAA;
    }
    
    .terminal-line .output {
        color: #FF3355;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.15), rgba(0, 200, 150, 0.05));
        border: 1px solid #00FFAA;
        color: #00FFAA;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 2px;
        padding: 16px 24px;
        border-radius: 10px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.3), rgba(0, 200, 150, 0.15));
        box-shadow: 0 0 30px rgba(0, 255, 170, 0.5);
        color: #FFFFFF;
        transform: translateY(-2px);
    }
    
    /* SECTION HEADERS */
    .section-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin: 40px 0 20px 0;
    }
    
    .section-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #00FFAA, transparent);
    }
    
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        color: #00FFAA;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* THREAT BAR */
    .threat-bar {
        background: #0a0e1a;
        border: 1px solid rgba(255, 51, 85, 0.3);
        border-radius: 8px;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin: 10px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }
    
    .threat-level {
        padding: 4px 12px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 1px;
    }
    
    .threat-critical { background: #FF0044; color: white; }
    .threat-high { background: #FF3355; color: white; }
    .threat-medium { background: #FF8800; color: white; }
</style>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⬤ SYSTEM ONLINE | MONITORING ACTIVE</div>
    <h1 class="hero-title">ABHEDYA MULENET</h1>
    <p class="hero-subtitle">Real-Time Mule Account Detection & Network Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Live status bar
st.markdown("""
<div class="status-bar">
    <div class="status-item"><span class="status-dot"></span> AI ENGINE: ACTIVE</div>
    <div class="status-item"><span class="status-dot"></span> TRANSACTIONS: LIVE</div>
    <div class="status-item"><span class="status-dot"></span> NETWORK MAP: TRACKING</div>
    <div class="status-item"><span class="status-dot"></span> POLICE LINK: CONNECTED</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== THREAT METRICS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Mule Accounts (India)</div>
        <div class="stat-value">32L+</div>
        <div class="stat-label">Flagged 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Financial Loss</div>
        <div class="stat-value">₹22K Cr</div>
        <div class="stat-label">Pan India 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Indore Complaints</div>
        <div class="stat-value">7,000+</div>
        <div class="stat-label">Jan-Aug 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Detection Speed</div>
        <div class="stat-value">0.3s</div>
        <div class="stat-label">AI Response</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== WHAT ARE MULE ACCOUNTS ====================
st.markdown("""
<div class="section-header">
    <span class="section-title">🧐 What are Mule Accounts?</span>
    <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div class="glass-card">
        <p style="color: #E0E0E0; line-height: 1.8; font-size: 15px;">
        A <b style="color: #00FFAA;">mule account</b> is a bank account used by criminals to 
        <b style="color: #FF3355;">receive, transfer, or launder money</b> obtained through 
        illegal activities — cyber fraud, digital arrest scams, and phishing attacks.
        </p>
        <p style="color: #8899aa; line-height: 1.8; font-size: 14px;">
        Criminals rent these accounts from ordinary citizens — students, daily wage workers, 
        vulnerable individuals — by offering small commissions. The account holder often 
        doesn't even realize their account is being used for fraud.
        </p>
        <div style="margin-top: 20px; padding: 15px; background: rgba(255, 51, 85, 0.1); border-left: 3px solid #FF3355; border-radius: 6px;">
        <p style="color: #FF3355; font-weight: bold; margin: 0;">⚡ The Money Trail:</p>
        <p style="color: #E0E0E0; margin: 8px 0 0 0; font-family: 'JetBrains Mono', monospace; font-size: 13px;">
        Victim → Layer-1 Mule → Layer-2 Mule → Layer-3 Mule → Cash Out (ATM/Crypto)
        </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="terminal-box">
        <div class="terminal-header">
            <span class="terminal-dot" style="background:#FF3355;"></span>
            <span class="terminal-dot" style="background:#FFAA00;"></span>
            <span class="terminal-dot" style="background:#00FFAA;"></span>
            <span style="color: #8899aa; margin-left: 10px; font-size: 11px;">abhedya@soc:~$</span>
        </div>
        <div class="terminal-line"><span class="cmd">$ scan --mode=live</span></div>
        <div class="terminal-line"><span class="output">[✓] 1,070 transactions loaded</span></div>
        <div class="terminal-line"><span class="cmd">$ detect --ai=isolation_forest</span></div>
        <div class="terminal-line"><span class="output">[!] 184 anomalies detected</span></div>
        <div class="terminal-line"><span class="cmd">$ map --network=graph</span></div>
        <div class="terminal-line"><span class="output">[!] 24 mule accounts traced</span></div>
        <div class="terminal-line"><span class="cmd">$ status</span></div>
        <div class="terminal-line"><span class="output">[✓] Network FROZEN</span></div>
        <div class="terminal-line" style="margin-top: 15px;"><span class="cmd">$ </span><span style="animation: blink 1s infinite;">█</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== LIVE THREAT FEED PREVIEW ====================
st.markdown("""
<div class="section-header">
    <span class="section-title">📡 Live Threat Feed</span>
    <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="threat-bar">
    <span class="threat-level threat-critical">CRITICAL</span>
    <span style="color: #E0E0E0;">₹95,000 IMPS transfer detected from unknown device</span>
    <span style="color: #8899aa; margin-left: auto;">2 sec ago</span>
</div>

<div class="threat-bar">
    <span class="threat-level threat-high">HIGH</span>
    <span style="color: #E0E0E0;">Account ****4521 linked to 12 pending complaints</span>
    <span style="color: #8899aa; margin-left: auto;">14 sec ago</span>
</div>

<div class="threat-bar">
    <span class="threat-level threat-medium">MEDIUM</span>
    <span style="color: #E0E0E0;">Late-night transaction spike in Indore region</span>
    <span style="color: #8899aa; margin-left: auto;">1 min ago</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== LAUNCH CENTER ====================
st.markdown("""
<div class="section-header">
    <span class="section-title">🚀 Launch Center</span>
    <span class="section-line"></span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h3 style="color: #00FFAA; font-size: 18px;">🛡️ MAIN DASHBOARD</h3>
        <p style="color: #8899aa; font-size: 13px; margin: 15px 0;">
        AI-powered anomaly detection with real-time threat metrics & analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶ LAUNCH DASHBOARD", key="dash_btn"):
        st.switch_page("pages/dashboard.py")

with col2:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h3 style="color: #00FFAA; font-size: 18px;">📡 LIVE FEED</h3>
        <p style="color: #8899aa; font-size: 13px; margin: 15px 0;">
        Real-time transaction stream with fraud alerts and impact counters
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶ LAUNCH LIVE FEED", key="live_btn"):
        st.switch_page("pages/live_feed.py")

with col3:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h3 style="color: #00FFAA; font-size: 18px;">🔍 INVESTIGATION</h3>
        <p style="color: #8899aa; font-size: 13px; margin: 15px 0;">
        Drill down into accounts, view history, and freeze entire networks
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶ LAUNCH INVESTIGATION", key="inv_btn"):
        st.switch_page("pages/drill_down.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div style="text-align: center; padding: 30px 20px; border-top: 1px solid rgba(0, 255, 170, 0.2); margin-top: 40px;">
    <p style="color: #00FFAA; font-family: 'Orbitron', sans-serif; letter-spacing: 3px; font-size: 14px; margin: 5px 0;">
    🛡️ ABHEDYA MULENET v2.0
    </p>
    <p style="color: #8899aa; font-size: 12px; letter-spacing: 1px; margin: 5px 0;">
    Void Hacks() 8.0 | Indore Police Cyber Cell | Build. Defend. Break.
    </p>
</div>
""", unsafe_allow_html=True)