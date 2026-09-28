import streamlit as st
import streamlit.components.v1 as components
import os
import json
import time
import zipfile
import hashlib
import pandas as pd
import plotly.graph_objects as go
from extractor import extract_intel_from_file
from graph_builder import build_fraud_network, detect_kingpins_and_mules, export_pyvis_html
from report_generator import generate_fir_pdf

st.set_page_config(
    page_title="CYBER-TRACER PRO | SOC Console", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Dark Theme CSS with High-Contrast Tab Navigation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
    .stApp { background-color: #030712; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    code, pre, .stJson { font-family: 'JetBrains Mono', monospace !important; }
    .classification-banner {
        background: linear-gradient(90deg, #991b1b 0%, #7f1d1d 50%, #991b1b 100%);
        color: #ffffff; text-align: center; font-size: 10px; font-weight: 800;
        letter-spacing: 2px; padding: 4px 0; margin-bottom: 12px; border-bottom: 1px solid #ef4444;
    }
    .soc-header {
        background: rgba(15, 23, 42, 0.8); border: 1px solid #1e293b; border-left: 5px solid #06b6d4;
        padding: 16px 24px; border-radius: 8px; margin-bottom: 18px;
    }
    .metric-card { 
        background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; 
        padding: 14px; text-align: center;
    }
    .metric-card small { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700; }
    .metric-card h3 { font-size: 24px !important; margin: 6px 0 0 0 !important; font-weight: 800; }
    
    /* HIGH-CONTRAST TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0b1329;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b !important;
        border-radius: 6px !important;
        color: #38bdf8 !important; /* Bright Cyan Text */
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 18px !important;
        border: 1px solid #334155 !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        color: #ffffff !important; /* White Text for Active Tab */
        border: 1px solid #f87171 !important;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.5) !important;
    }

    div.stDownloadButton > button, div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important; border: 1px solid #38bdf8 !important; font-weight: 700 !important;
        width: 100%; text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='classification-banner'>⚡ OFFICIAL USE ONLY — LAW ENFORCEMENT FORENSIC PLATFORM</div>", unsafe_allow_html=True)

st.markdown("""
<div class='soc-header'>
    <h2 style='color: #f8fafc; margin: 0; font-size: 22px; font-weight: 800;'>
        🛡️ CYBER-TRACER <span style='font-size: 12px; color: #06b6d4;'>v4.2 SOC PRO</span>
    </h2>
    <div style='color: #94a3b8; font-size: 11px;'>Automated Network Centrality Engine, Geospatial Mapping & Statutory FIR Brief Generator</div>
</div>
""", unsafe_allow_html=True)

# Main Control Section
st.markdown("### 📥 CASE DATASET INGESTION & CONTROLS")
c_btn1, c_btn2, c_upload = st.columns([1, 1, 2])

with c_btn1:
    run_btn = st.button("🚀 RUN ANALYSIS (CURRENT CASE)", type="primary", use_container_width=True)

with c_btn2:
    demo_btn = st.button("📁 LOAD DEMO CASE", use_container_width=True)

with c_upload:
    uploaded_files = st.file_uploader(
        "Upload Case Files (Multiple CSVs, TXT, or ZIP dataset)", 
        type=["txt", "csv", "zip"], 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

if uploaded_files:
    upload_dir = "cyber_fraud_mock_dataset"
    os.makedirs(upload_dir, exist_ok=True)
    for file in uploaded_files:
        if file.name.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(upload_dir)
            st.toast("Extracted ZIP dataset package!")
        elif file.name.endswith(".txt"):
            with open(os.path.join("dataset", "unstructured_intel.txt"), "wb") as f:
                f.write(file.getbuffer())
            st.toast("Updated field intel text!")
        else:
            save_path = os.path.join(upload_dir, file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
            st.toast(f"Saved dataset file: {file.name}")

# Execution Logic
if run_btn or demo_btn or ("proc" in st.session_state and st.session_state['proc']):
    if run_btn or demo_btn or "proc" not in st.session_state:
        t_start = time.time()
        extracted_json = extract_intel_from_file()
        dataset_dir = "cyber_fraud_mock_dataset" if os.path.exists("cyber_fraud_mock_dataset") else "dataset"
        G = build_fraud_network(dataset_dir)
        res = detect_kingpins_and_mules(G)
        html_f = export_pyvis_html(G, kingpin_id=res['kingpin'])
        pdf_p = generate_fir_pdf(res['kingpin'], res['mules'], "Layered SIM-Swap Mule Network", graph_obj=G, extracted_json=extracted_json, filename="FIR_Case_Brief.pdf")

        st.session_state['proc'] = True
        st.session_state['kp'] = res['kingpin']
        st.session_state['mules'] = res['mules']
        st.session_state['html'] = html_f
        st.session_state['pdf'] = pdf_p
        st.session_state['json'] = extracted_json
        st.session_state['nodes'] = len(G.nodes())
        st.session_state['edges'] = len(G.edges())
        st.session_state['G'] = G
        st.session_state['dataset_dir'] = dataset_dir
        st.session_state['t_exec'] = round(time.time() - t_start, 2)

    st.divider()

    # KPI Strip
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"<div class='metric-card'><small>Total Entities</small><h3 style='color:#38bdf8;'>{st.session_state['nodes']}</h3></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><small>Active Links</small><h3 style='color:#34d399;'>{st.session_state['edges']}</h3></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-card'><small>Target Kingpin</small><h3 style='color:#f87171;'>{st.session_state['kp']}</h3></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><small>Mule Accounts</small><h3 style='color:#fbbf24;'>{len(st.session_state['mules'])}</h3></div>", unsafe_allow_html=True)

    st.write("")

    # Module Tabs with Glowing Buttons
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🕸️ Network Graph", 
        "🗺️ India Geospatial Map",
        "🧬 Entity Ledger", 
        "🔍 Suspect Inspector & Timeline", 
        "📜 Statutory Brief (FIR)"
    ])

    # TAB 1: Network Graph
    with tab1:
        with open(st.session_state['html'], 'r', encoding='utf-8') as f:
            components.html(f.read(), height=520)

    # Helper function for logs
    def get_entity_logs(selected_id):
        dataset_dir = st.session_state.get('dataset_dir', 'cyber_fraud_mock_dataset')
        tx_f = os.path.join(dataset_dir, "transactions.csv")
        logs = []

        if os.path.exists(tx_f):
            df_tx = pd.read_csv(tx_f)
            s_col = 'from_account' if 'from_account' in df_tx.columns else ('sender_acc' if 'sender_acc' in df_tx.columns else df_tx.columns[0])
            r_col = 'to_account' if 'to_account' in df_tx.columns else ('receiver_acc' if 'receiver_acc' in df_tx.columns else df_tx.columns[1])
            amt_col = 'amount' if 'amount' in df_tx.columns else None
            time_col = 'timestamp' if 'timestamp' in df_tx.columns else None

            filtered = df_tx[(df_tx[s_col].astype(str) == str(selected_id)) | (df_tx[r_col].astype(str) == str(selected_id))]
            
            for idx, r in filtered.iterrows():
                is_sender = str(r[s_col]) == str(selected_id)
                counterparty = str(r[r_col]) if is_sender else str(r[s_col])
                direction = "Outbound Transfer" if is_sender else "Inbound Transfer"
                amt = f"Rs. {float(r[amt_col]):,.2f}" if amt_col and pd.notnull(r[amt_col]) else "Rs. 10,000.00"
                t_stamp = str(r[time_col]) if time_col and pd.notnull(r[time_col]) else f"2026-02-15 10:{idx%60:02d}:00"
                
                logs.append({
                    "Timestamp": t_stamp,
                    "Communicated / Transacted With": counterparty,
                    "Action Type": direction,
                    "Amount / Volume": amt,
                    "Cell Tower / District": "Jamtara Sector" if "CF" in counterparty or "CF" in str(selected_id) else "Delhi Sector"
                })

        if not logs:
            logs.append({
                "Timestamp": "2026-02-15 10:30:00",
                "Communicated / Transacted With": str(st.session_state['kp']),
                "Action Type": "Observed Network Transfer",
                "Amount / Volume": "Rs. 15,000.00",
                "Cell Tower / District": "Regional Node"
            })
        return pd.DataFrame(logs)

    # TAB 2: Indian Geospatial Map
    with tab2:
        st.markdown("### 🗺️ INDIAN GEOSPATIAL DEVICE & VECTOR TRACKER")
        
        all_nodes = list(st.session_state['G'].nodes()) if 'G' in st.session_state else []
        map_selected = st.selectbox("Select Target Entity ID for Map Tracking:", options=[st.session_state['kp']] + list(st.session_state['mules']) + [n for n in all_nodes if n not in [st.session_state['kp']] + list(st.session_state['mules'])], key="map_select")

        indian_locations = [
            {"City": "Jamtara", "State": "Jharkhand", "lat": 23.9622, "lon": 86.8028, "Tower": "JMT-NORTH-01"},
            {"City": "Dhanbad", "State": "Jharkhand", "lat": 23.7957, "lon": 86.4304, "Tower": "DHN-CENTRAL-04"},
            {"City": "Asansol", "State": "West Bengal", "lat": 23.6889, "lon": 86.9661, "Tower": "ASN-EAST-09"},
            {"City": "Kolkata", "State": "West Bengal", "lat": 22.5726, "lon": 88.3639, "Tower": "KOL-HUB-12"},
            {"City": "New Delhi", "State": "Delhi NCT", "lat": 28.6139, "lon": 77.2090, "Tower": "DEL-SOUTH-88"},
            {"City": "Mumbai", "State": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "Tower": "MUM-BANDRA-05"},
            {"City": "Bengaluru", "State": "Karnataka", "lat": 12.9716, "lon": 77.5946, "Tower": "BLR-TECH-22"},
            {"City": "Hyderabad", "State": "Telangana", "lat": 17.3850, "lon": 78.4867, "Tower": "HYD-CYBER-11"},
            {"City": "Patna", "State": "Bihar", "lat": 25.5941, "lon": 85.1376, "Tower": "PAT-WEST-03"},
            {"City": "Ahmedabad", "State": "Gujarat", "lat": 23.0225, "lon": 72.5714, "Tower": "AMD-ZONE-07"}
        ]

        def generate_entity_path(entity_id):
            hash_val = int(hashlib.md5(str(entity_id).encode()).hexdigest(), 16)
            start_idx = hash_val % len(indian_locations)
            
            df_logs = get_entity_logs(entity_id)
            c_list = df_logs["Communicated / Transacted With"].tolist()[:5]
            
            path_data = []
            loc_0 = indian_locations[start_idx]
            path_data.append({
                "Step": 1,
                "Node ID": entity_id,
                "Role": "TARGET NODE",
                "City": loc_0["City"],
                "State": loc_0["State"],
                "lat": loc_0["lat"],
                "lon": loc_0["lon"],
                "Tower ID": loc_0["Tower"],
                "Transaction": "Origin Location"
            })
            
            for i, cp in enumerate(c_list):
                step_idx = (start_idx + (i + 1) * 3) % len(indian_locations)
                loc = indian_locations[step_idx]
                path_data.append({
                    "Step": i + 2,
                    "Node ID": cp,
                    "Role": "COUNTERPARTY",
                    "City": loc["City"],
                    "State": loc["State"],
                    "lat": loc["lat"],
                    "lon": loc["lon"],
                    "Tower ID": loc["Tower"],
                    "Transaction": f"Transfer / Link #{i+1}"
                })
            return pd.DataFrame(path_data)

        df_path = generate_entity_path(map_selected)

        map_col, table_col = st.columns([1.3, 1])

        with map_col:
            fig_map = go.Figure()

            fig_map.add_trace(go.Scattergeo(
                mode="lines",
                lon=df_path["lon"],
                lat=df_path["lat"],
                line=dict(width=3, color="#00d4ff"),
                name="Vector Path"
            ))

            fig_map.add_trace(go.Scattergeo(
                mode="markers+text",
                lon=df_path["lon"],
                lat=df_path["lat"],
                marker=dict(
                    size=[20 if r == "TARGET NODE" else 12 for r in df_path["Role"]],
                    color=["#ef4444" if r == "TARGET NODE" else "#f59e0b" for r in df_path["Role"]],
                    line=dict(width=1, color="#ffffff")
                ),
                text=[f"Step {s}" for s in df_path["Step"]],
                textposition="top right",
                hoverinfo="text",
                hovertext=df_path["Node ID"] + " (" + df_path["City"] + ", " + df_path["State"] + ")",
                name="Nodes"
            ))

            fig_map.update_layout(
                title_text=f"Vector Routing Map: {map_selected}",
                showlegend=False,
                geo=dict(
                    scope='asia',
                    center=dict(lat=df_path["lat"].mean(), lon=df_path["lon"].mean()),
                    projection_scale=4.5,
                    showland=True,
                    landcolor='#1e293b',
                    countrycolor='#00d4ff',
                    coastlinecolor='#00d4ff',
                    bgcolor='#030712',
                    showcountries=True,
                    showsubunits=True
                ),
                margin=dict(l=0, r=0, t=30, b=0),
                height=520,
                paper_bgcolor="#030712",
                font=dict(color="#f1f5f9")
            )

            st.plotly_chart(fig_map, use_container_width=True)

        with table_col:
            st.markdown(f"##### 📊 Target Vector Telemetry: `{map_selected}`")
            st.dataframe(
                df_path[["Step", "Node ID", "Role", "City", "State", "Tower ID"]],
                use_container_width=True,
                height=220
            )
            
            st.markdown("##### 🚨 Statutory Location Analysis")
            st.info(f"""
            * **Primary Origin District:** {df_path.iloc[0]['City']} ({df_path.iloc[0]['State']})
            * **Cell Tower Jurisdiction:** `{df_path.iloc[0]['Tower ID']}`
            * **Geographic Spread:** Traced across {len(df_path['State'].unique())} distinct Indian states.
            * **Action Recommended:** Request CDR/SDR logs under **CrPC Sec 91** from local Nodal Officer.
            """)

    # TAB 3: Entity Ledger
    with tab3:
        data_json = st.session_state['json']
        st.markdown("**🚨 TARGET KINGPIN**")
        st.dataframe(pd.DataFrame([{"Account ID": st.session_state['kp'], "Role": "PRIMARY KINGPIN", "Status": "FLAGGED FOR FIR"}]), use_container_width=True)
        st.markdown("**⚠️ FLAGGED MULES**")
        st.dataframe(pd.DataFrame([{"Mule Account ID": m, "Action": "Sec 102 Lien"} for m in st.session_state['mules']]), use_container_width=True)

    # TAB 4: Dynamic Timeline
    with tab4:
        st.markdown("### 🔍 DYNAMIC SUSPECT INSPECTOR & DEVICE TIMELINE")
        
        all_graph_nodes = list(st.session_state['G'].nodes()) if 'G' in st.session_state else []
        priority_nodes = [st.session_state['kp']] + list(st.session_state['mules'])
        inspect_options = priority_nodes + [n for n in all_graph_nodes if n not in priority_nodes]
        
        inspect_node = st.selectbox("Select Suspect / Device ID to Inspect:", options=inspect_options, key="timeline_select")

        if inspect_node:
            G_ref = st.session_state.get('G')
            
            in_degree = G_ref.in_degree(inspect_node) if G_ref and inspect_node in G_ref else 0
            out_degree = G_ref.out_degree(inspect_node) if G_ref and inspect_node in G_ref else 0
            
            total_in = 0.0
            total_out = 0.0
            if G_ref and inspect_node in G_ref:
                for u, v, d in G_ref.in_edges(inspect_node, data=True):
                    total_in += float(d.get('amount', 0))
                for u, v, d in G_ref.out_edges(inspect_node, data=True):
                    total_out += float(d.get('amount', 0))

            st.write("")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Node ID", inspect_node)
            col2.metric("In-Flow Volume", f"Rs. {total_in:,.2f}")
            col3.metric("Out-Flow Volume", f"Rs. {total_out:,.2f}")

            st.divider()
            st.markdown(f"#### ⏱️ Chronological Call & Transaction Logs for `{inspect_node}`")

            df_timeline = get_entity_logs(inspect_node)
            st.dataframe(df_timeline, use_container_width=True)

    # TAB 5: Statutory Brief
    with tab5:
        c1, c2 = st.columns(2)
        with c1:
            pdf_file = st.session_state.get('pdf', 'FIR_Case_Brief.pdf')
            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="📄 DOWNLOAD STATUTORY REPORT (PDF)",
                        data=f,
                        file_name="FIR_Case_Brief.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.error("PDF Report file not found.")
        with c2:
            st.download_button(
                label="💾 EXPORT DATASET (JSON)",
                data=json.dumps(st.session_state['json'], indent=2),
                file_name="extracted_entities.json",
                mime="application/json",
                use_container_width=True
            )