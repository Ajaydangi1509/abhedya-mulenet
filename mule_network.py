import networkx as nx
import plotly.graph_objects as go
import random

print("🕸️ Building REAL mule network...\n")

# ============================================
# CREATE A REAL CRIMINAL NETWORK
# Mastermind → Layer 1 → Layer 2 → Cash Out
# ============================================

random.seed(42)

# Mastermind account
mastermind = "90001234567"

# Layer 1 mules (directly receive from mastermind)
layer1 = [f"7000{random.randint(1000000, 9999999)}" for _ in range(5)]

# Layer 2 mules (receive from layer 1)
layer2 = []
for _ in range(8):
    layer2.append(f"8000{random.randint(1000000, 9999999)}")

# Layer 3 - cash out accounts (receive from layer 2)
layer3 = [f"6000{random.randint(1000000, 9999999)}" for _ in range(10)]

# Build graph
G = nx.DiGraph()

# Mastermind → Layer 1 (large transfers)
for l1 in layer1:
    G.add_edge(mastermind, l1, amount=random.randint(80000, 150000), risk=98)

# Layer 1 → Layer 2 (medium transfers)
for l1 in layer1:
    targets = random.sample(layer2, k=2)
    for t in targets:
        G.add_edge(l1, t, amount=random.randint(40000, 70000), risk=92)

# Layer 2 → Layer 3 (smaller, cash out)
for l2 in layer2:
    targets = random.sample(layer3, k=2)
    for t in targets:
        G.add_edge(l2, t, amount=random.randint(15000, 35000), risk=85)

# Some cross-connections (mule rings often have complex links)
for _ in range(5):
    src = random.choice(layer1)
    dst = random.choice(layer2)
    if src != dst and not G.has_edge(src, dst):
        G.add_edge(src, dst, amount=random.randint(30000, 50000), risk=88)

print(f"✅ Network created!")
print(f"   Nodes: {G.number_of_nodes()}")
print(f"   Edges: {G.number_of_edges()}")

# Layout - hierarchical look
pos = nx.spring_layout(G, k=2.0, iterations=100, seed=42)

# ============================================
# EDGES (with arrows!)
# ============================================
edge_traces = []

for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    
    amount = edge[2].get('amount', 1000)
    width = max(1, min(amount / 20000, 8))
    
    # Main line
    edge_traces.append(go.Scatter(
        x=[x0, x1, None],
        y=[y0, y1, None],
        line=dict(width=width, color='rgba(255, 51, 85, 0.7)'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Arrow head (small triangle at end)
    arrow_x = x0 + (x1 - x0) * 0.85
    arrow_y = y0 + (y1 - y0) * 0.85
    
    edge_traces.append(go.Scatter(
        x=[arrow_x],
        y=[arrow_y],
        mode='markers',
        marker=dict(
            size=8,
            color='#FF3355',
            symbol='triangle-right',
            angle=0
        ),
        hoverinfo='none',
        showlegend=False
    ))

# ============================================
# NODES (grouped by layer)
# ============================================
node_x, node_y, node_color, node_size, node_text = [], [], [], [], []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    
    if node == mastermind:
        color = '#FF0044'  # Bright red
        size = 45
        role = "🎯 MASTERMIND"
        risk = 100
    elif node in layer1:
        color = '#FF3355'  # Red
        size = 35
        role = "💰 Layer 1 Mule"
        risk = 95
    elif node in layer2:
        color = '#FF8800'  # Orange
        size = 25
        role = "💵 Layer 2 Mule"
        risk = 88
    else:
        color = '#FFAA00'  # Yellow
        size = 18
        role = "💸 Cash Out"
        risk = 80
    
    node_color.append(color)
    node_size.append(size)
    
    inbound = sum([G[u][node].get('amount', 0) for u in G.predecessors(node)])
    outbound = sum([G[node][v].get('amount', 0) for v in G.successors(node)])
    
    node_text.append(
        f"<b>Account:</b> ****{str(node)[-4:]}<br>"
        f"<b>Role:</b> {role}<br>"
        f"<b>Risk Score:</b> {risk}/100<br>"
        f"<b>Money In:</b> ₹{inbound:,}<br>"
        f"<b>Money Out:</b> ₹{outbound:,}<br>"
        f"<b>Connections:</b> {G.degree(node)}"
    )

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[f"****{str(n)[-4:]}" for n in G.nodes()],
    textposition='bottom center',
    textfont=dict(size=9, color='#FFFFFF', family='Consolas'),
    hoverinfo='text',
    hovertext=node_text,
    marker=dict(
        color=node_color,
        size=node_size,
        line=dict(width=2, color='white')
    )
)

# ============================================
# FIGURE
# ============================================
fig = go.Figure(
    data=edge_traces + [node_trace],
    layout=go.Layout(
        title=dict(
            text='🕸️ MULE NETWORK — Money Flow Chain',
            font=dict(color='#00FFAA', size=20, family='Consolas'),
            x=0.5
        ),
        paper_bgcolor='#0a0e1a',
        plot_bgcolor='#0a0e1a',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=60, l=20, r=20, t=60),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=700,
        annotations=[
            dict(
                text="🎯 Mastermind → 💰 Layer 1 → 💵 Layer 2 → 💸 Cash Out",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.08,
                font=dict(color='#FF3355', size=14, family='Consolas')
            ),
            dict(
                text=f"Total Nodes: {G.number_of_nodes()} | Total Transfers: {G.number_of_edges()}",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.13,
                font=dict(color='#8899aa', size=11, family='Consolas')
            )
        ]
    )
)

fig.write_html('network_graph.html')
print("\n✅ Saved to: network_graph.html")

print("\n🚨 TOP 5 MULE HUBS:")
for node, degree in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:5]:
    if node == mastermind:
        label = "MASTERMIND"
    elif node in layer1:
        label = "Layer 1"
    elif node in layer2:
        label = "Layer 2"
    else:
        label = "Cash Out"
    print(f"  ****{str(node)[-4:]} → {degree} connections [{label}]")