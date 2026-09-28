import os
import tempfile
import pandas as pd
import networkx as nx
from pyvis.network import Network

def build_fraud_network(dataset_dir="cyber_fraud_mock_dataset"):
    G = nx.DiGraph()

    # Fallback to standard dataset directory if mock dataset path is missing
    if not os.path.exists(dataset_dir) and os.path.exists("dataset"):
        dataset_dir = "dataset"

    tx_f = os.path.join(dataset_dir, "transactions.csv")
    dev_f = os.path.join(dataset_dir, "devices.csv")
    calls_f = os.path.join(dataset_dir, "calls.csv")
    if not os.path.exists(calls_f):
        calls_f = os.path.join(dataset_dir, "call_logs.csv")

    # 1. Parse Transactions CSV
    if os.path.exists(tx_f):
        df_tx = pd.read_csv(tx_f)
        s_col = 'from_account' if 'from_account' in df_tx.columns else ('sender_acc' if 'sender_acc' in df_tx.columns else df_tx.columns[0])
        r_col = 'to_account' if 'to_account' in df_tx.columns else ('receiver_acc' if 'receiver_acc' in df_tx.columns else df_tx.columns[1])
        amt_col = 'amount' if 'amount' in df_tx.columns else None

        for _, r in df_tx.iterrows():
            u, v = str(r[s_col]), str(r[r_col])
            amt = float(r[amt_col]) if amt_col and pd.notnull(r[amt_col]) else 1000.0
            G.add_node(u, type='account', label=f"Acc: {u}")
            G.add_node(v, type='account', label=f"Acc: {v}")
            G.add_edge(u, v, type='TRANSFERRED', amount=amt)

    # 2. Parse Devices / IMEI CSV
    if os.path.exists(dev_f):
        df_dev = pd.read_csv(dev_f)
        acc_col = 'account_id' if 'account_id' in df_dev.columns else df_dev.columns[0]
        imei_col = 'imei' if 'imei' in df_dev.columns else df_dev.columns[1]

        for _, r in df_dev.iterrows():
            dev_id = f"IMEI_{r[imei_col]}"
            acc_id = str(r[acc_col])
            G.add_node(dev_id, type='device', label=f"IMEI: {r[imei_col]}")
            G.add_node(acc_id, type='account', label=f"Acc: {acc_id}")
            G.add_edge(acc_id, dev_id, type='USED_ON')

    # 3. Parse Calls CSV
    if os.path.exists(calls_f):
        df_calls = pd.read_csv(calls_f)
        c_col = 'caller' if 'caller' in df_calls.columns else df_calls.columns[0]
        r_col = 'callee' if 'callee' in df_calls.columns else df_calls.columns[1]

        for _, r in df_calls.iterrows():
            u, v = str(r[c_col]), str(r[r_col])
            G.add_edge(u, v, type='CALLED')

    return G

def detect_kingpins_and_mules(G):
    if len(G) == 0: 
        return {"kingpin": "N/A", "mules": [], "suspect_scores": []}
    
    bw = nx.betweenness_centrality(G)
    deg = nx.in_degree_centrality(G)
    
    scores = {n: bw[n] * 0.6 + deg[n] * 0.4 for n in G.nodes()}
    sorted_s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    kingpin = sorted_s[0][0] if sorted_s else "N/A"
    mules = [n for n, s in sorted_s[1:6] if G.nodes[n].get('type') == 'account']
    
    return {
        "kingpin": kingpin,
        "mules": mules,
        "suspect_scores": sorted_s
    }

def export_pyvis_html(G, kingpin_id=None, output_filename="network.html"):
    net = Network(height="500px", width="100%", directed=True, bgcolor="#0b0f19", font_color="#ffffff")
    res = detect_kingpins_and_mules(G)
    
    for n, d in G.nodes(data=True):
        ntype = d.get('type', 'account')
        
        if str(n) == str(kingpin_id):
            color = '#ef4444'
            shape = 'diamond'
            size = 35
            role = "Target Kingpin"
        elif ntype == 'device' or 'IMEI' in str(n):
            color = '#9ca3af'
            shape = 'square'
            size = 18
            role = "Hardware Device (IMEI)"
        elif n in res['mules']:
            color = '#f59e0b'
            shape = 'dot'
            size = 22
            role = "Flagged Mule Account"
        else:
            color = '#3b82f6'
            shape = 'dot'
            size = 16
            role = "Network Account / Victim"

        tooltip = f"Role: {role}\nNode ID: {n}"
        net.add_node(str(n), label=str(n), color=color, size=size, shape=shape, title=tooltip)

    for u, v, d in G.edges(data=True):
        etype = d.get('type', 'TRANSFERRED')
        if etype == 'USED_ON':
            net.add_edge(str(u), str(v), title="Shared Hardware IMEI Link", color="#ef4444", dashes=True, width=2)
        else:
            amt = float(d.get('amount', 1000))
            thickness = max(1, min(6, int(amt / 15000)))
            net.add_edge(str(u), str(v), title=f"Transfer: Rs. {amt:,.2f}", color="#3b82f6", width=thickness)

    net.toggle_physics(True)
    
    # Safe HTML Generation to prevent PermissionError
    try:
        html_content = net.generate_html()
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
    except Exception:
        output_filename = os.path.join(tempfile.gettempdir(), "network_render.html")
        html_content = net.generate_html()
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

    return output_filename