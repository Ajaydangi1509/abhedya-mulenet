import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import numpy as np

print("🕸️ Building criminal network graph...\n")

df = pd.read_csv('transactions_with_risk.csv')
print(f"📊 Loaded {len(df)} transactions")

# Take TOP risky accounts only
suspicious = df[df['risk_score'] >= 60].copy()
print(f"🚨 High-risk accounts: {len(suspicious)}")

# Build graph
G = nx.DiGraph()

for _, row in suspicious.iterrows():
    sender = str(row['sender_account'])
    receiver = str(row['receiver_account'])
    
    if 'ATM' in sender or 'Cash' in str(row['sender_name']):
        continue
    
    if G.has_edge(sender, receiver):
        G[sender][receiver]['weight'] += 1
        G[sender][receiver]['amount'] += row['amount']
    else:
        G.add_edge(sender, receiver, 
                   weight=1, 
                   amount=row['amount'],
                   risk=int(row['risk_score']))

# Keep only nodes with connections (degree >= 2)
connected_nodes = [n for n in G.nodes() if G.degree(n) >= 1]
G = G.subgraph(connected_nodes).copy()

# Take top 25 most connected
if G.number_of_nodes() > 25:
    top_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:25]
    top_node_ids = [n[0] for n in top_nodes]
    G = G.subgraph(top_node_ids).copy()

print(f"🔗 Nodes: {G.number_of_nodes()}")
print(f"🔗 Edges: {G.number_of_edges()}")

# Layout
pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

# ============ EDGES ============
edge_traces = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    
    # Line thickness based on amount
    amount = edge[2].get('amount', 1000)
    width = min(1 + amount / 30000, 6)
    
    edge_trace = go.Scatter(
        x=[x0, x1, None],
        y=[y0, y1, None],
        line=dict(width=width, color='rgba(255, 51, 85, 0.8)'),
        hoverinfo='none',
        mode='lines'
    )
    edge_traces.append(edge_trace)

# ============ NODES ============
node_x, node_y, node_color, node_size, node_text, node_labels = [], [], [], [], [], []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    
    degree = G.degree(node)
    risk = 60  # default
    total_amount = 0
    
    # Get max risk from edges
    for u, v in G.edges(node):
        if 'risk' in G[u][v]:
            risk = max(risk, G[u][v]['risk'])
            total_amount += G[u][v].get('amount', 0)
    
    node_color.append(risk)
    node_size.append(20 + degree * 8)  # Bigger = more connections
    node_labels.append(f"****{str(node)[-4:]}")
    
    node_text.append(
        f"<b>Account:</b> ****{str(node)[-4:]}<br>"
        f"<b>Risk Score:</b> <span style='color:#FF3355'>{risk}/100</span><br>"
        f"<b>Connections:</b> {degree}<br>"
        f"<b>Total Amount:</b> ₹{total_amount:,}<br>"
        f"<b>Status:</b> 🚨 UNDER INVESTIGATION"
    )

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_labels,
    textposition='top center',
    textfont=dict(size=9, color='#00FFAA', family='Consolas'),
    hoverinfo='text',
    hovertext=node_text,
    marker=dict(
        showscale=True,
        colorscale=[
            [0, '#00FFAA'],
            [0.3, '#FFAA00'],
            [0.7, '#FF6600'],
            [1, '#FF0044']
        ],
        color=node_color,
        cmin=60,
        cmax=100,
        size=node_size,
        colorbar=dict(
            thickness=18,
            title=dict(text='Risk Score', side='right', font=dict(color='white')),
            xanchor='left',
            tickfont=dict(color='white', size=11),
            bgcolor='#1a1f3a',
            bordercolor='#00FFAA',
            borderwidth=1
        ),
        line=dict(width=2, color='#00FFAA')
    )
)

# ============ FIGURE ============
fig = go.Figure(
    data=edge_traces + [node_trace],
    layout=go.Layout(
        title=dict(
            text='🕸️ Criminal Network — Connected Mule Accounts',
            font=dict(color='#00FFAA', size=20, family='Consolas'),
            x=0.5
        ),
        paper_bgcolor='#0a0e1a',
        plot_bgcolor='#0a0e1a',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=20, r=20, t=60),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showline=False),
        height=700,
        annotations=[
            dict(
                text=f"🔴 {G.number_of_nodes()} accounts | 🔗 {G.number_of_edges()} connections | ⚠️ AI-detected fraud network",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.05,
                font=dict(color='#8899aa', size=12, family='Consolas')
            )
        ]
    )
)

fig.write_html('network_graph.html')
print("\n✅ Graph saved to: network_graph.html")

# Stats
top_5 = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:5]
print("\n🚨 Top 5 mule hubs (most connected):")
for acc, deg in top_5:
    print(f"  ****{str(acc)[-4:]} → {deg} connections")

print("\n✅ Network graph ready!")