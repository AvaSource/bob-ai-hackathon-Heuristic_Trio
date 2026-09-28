# 🚀 Cyber-Tracer Pro — Cyber Fraud Network Analyzer

> AI-assisted forensic console that turns raw fraud case data (transactions, devices, call logs and free-text field intel) into a mule-network graph, a ranked kingpin/mule list, a geospatial trace and a ready-to-file FIR case brief.

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | Heuristic Trio |
| **Track** | AI |
| **Team Lead** | Kaavya Desai | avanco140@gmail.com |
| **Members** | Lil Drashti, Kaavya Desai |

---

## 🎯 Problem Statement

Cyber-crime cells investigating SIM-swap / OTP-vishing fraud (the "Jamtara pattern") receive case evidence as scattered bank transaction dumps, telecom call records, device/IMEI lists and unstructured field reports. Investigators manually cross-reference these sources in spreadsheets to work out who the coordinator is and which accounts are mules — a slow process that lets funds get layered and cashed out before accounts can be frozen.

---

## 💡 Solution

Cyber-Tracer Pro ingests case files (CSV / TXT / ZIP), uses an LLM to extract entities and relationships from unstructured intel, and fuses everything into a single directed graph of accounts, devices and phones. Graph-centrality scoring (betweenness + in-degree) surfaces the likely kingpin and the top mule accounts, which are then visualised interactively, traced on an India map, and written up automatically as a statutory FIR case brief PDF.

---

## ✨ Key Features

- **LLM entity extraction:** Unstructured field-intel text is converted into structured entities/relationships (person, account, device, SIM) via Groq-hosted Llama models, with multi-model fallback and an offline ground-truth fallback.
- **Fraud network graph + kingpin detection:** Transactions, IMEI links and call logs are fused into a NetworkX graph; a weighted betweenness/in-degree score ranks the kingpin and mule accounts.
- **Interactive network visualisation:** PyVis graph with role-based colouring (kingpin, mule, device, victim), shared-IMEI links and amount-weighted transfer edges.
- **Geospatial trace & suspect inspector:** Plotly map of each entity's routing across Indian cities/cell towers plus per-entity in/out flow volumes and chronological transaction timeline.
- **Automated FIR case brief:** One-click ReportLab PDF with case metadata, accused/mule tables and recommended statutory actions, plus JSON export of extracted entities.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python |
| **Frameworks** | Streamlit, NetworkX, PyVis, Plotly, Pandas, ReportLab |
| **IBM Technologies** | TODO — list IBM Bob / watsonx usage if applicable |
| **AI / LLM** | Groq API (Llama 3.3 70B, Mixtral 8x7B, Gemma2 9B fallback chain) |
| **Databases** | None — CSV case files |
| **Other** | Synthetic dataset modelled on public I4C / NCRP fraud typologies |

---

## 📁 Repository Structure

```
├── src/                         # All source code
│   ├── app.py                   # Streamlit SOC console (entry point)
│   ├── extractor.py             # LLM entity/relationship extraction (Groq)
│   ├── graph_builder.py         # Graph construction, kingpin/mule scoring, PyVis export
│   ├── report_generator.py      # FIR case brief PDF generator
│   ├── requirements.txt
│   ├── .env.example
│   ├── dataset/                 # Jamtara-pattern synthetic case + ground_truth.json
│   ├── cyber_fraud_mock_dataset/# Larger multi-case synthetic dataset
│   └── lib/                     # PyVis front-end assets
├── docs/                        # Written documentation
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/                        # Demo artifacts
│   ├── screenshots/
│   ├── sample-output/           # Example generated FIR brief
│   └── demo-video-link.txt
├── presentation/                # Slide deck
└── submission.yaml              # Structured submission metadata
```

---

## ⚡ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/src

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment (optional — without a key the app uses dataset/ground_truth.json)
cp .env.example .env
# Edit .env and set GROQ_API_KEY

# 4. Run the project
streamlit run app.py
```

Open `http://localhost:8501` and click **📁 LOAD DEMO CASE**.

---

## 🖥️ Demo

artifacts:
  source_code: "."
  setup_guide: "README.md"
  architecture_doc: "README.md"
  demo_video: "https://youtube.com" # Replace with your YouTube/Loom video link
  live_demo: "http://localhost:8501" # Replace with your deployed URL or keep default
  screenshots: "demo/screenshots/"
  presentation: "presentation/"

---

## ⚠️ Known Limitations

- All data is **synthetic** — modelled on public fraud typologies, not real case records.
- Geospatial routing is illustrative: locations are assigned deterministically per entity (hash-based) rather than read from real cell-tower/CDR data.
- Kingpin/mule detection is a centrality heuristic, not a trained classifier; the top-scoring node may be a device or a high-traffic victim in noisy data.
- Uploaded files overwrite the local dataset folder; there is no per-case workspace or authentication.

---

## 🏅 What We're Most Proud Of

The end-to-end pipeline: one click takes raw, messy multi-source evidence to a ranked suspect list, an explorable network graph and a filed-ready FIR brief. Look at `graph_builder.py` (schema-tolerant fusion of transactions, IMEI and call data into one graph) and `report_generator.py` (the generated statutory brief).
