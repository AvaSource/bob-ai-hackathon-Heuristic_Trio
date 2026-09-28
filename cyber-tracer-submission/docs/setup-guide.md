# Setup Guide

> **This file is read by the automated evaluation pipeline. Be precise and complete.**

## Prerequisites

Before you begin, ensure you have the following installed:

- [ ] Python 3.10+ (tested with 3.13)
- [ ] pip
- [ ] (Optional) A free Groq API key from https://console.groq.com/keys — without it, extraction uses the bundled ground-truth file and everything else works the same

## Environment Variables

Copy `src/.env.example` to `src/.env` and fill in the values:

```bash
cd src
cp .env.example .env
```

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key used for LLM entity extraction | No (falls back to `dataset/ground_truth.json`) |

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/src

# 2. (Recommended) create a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the Application

Run from inside `src/` (the app uses relative paths to `dataset/` and `cyber_fraud_mock_dataset/`):

```bash
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

## Running Tests

There is no automated test suite. To verify the pipeline headlessly:

```bash
python -c "from graph_builder import build_fraud_network, detect_kingpins_and_mules; G=build_fraud_network('cyber_fraud_mock_dataset'); print(len(G), detect_kingpins_and_mules(G)['kingpin'])"
```

## Quick Demo

1. Start the app with `streamlit run app.py`.
2. Click **📁 LOAD DEMO CASE**.
3. Explore the tabs: **Network Graph** → **India Geospatial Map** → **Entity Ledger** → **Suspect Inspector & Timeline**.
4. In **Statutory Brief (FIR)**, download the PDF case brief and the JSON entity export.

A sample generated brief is in [`demo/sample-output/FIR_Case_Brief.pdf`](../demo/sample-output/FIR_Case_Brief.pdf).

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your activated virtual environment |
| `FileNotFoundError` for dataset files | Make sure you run `streamlit run app.py` from inside the `src/` folder |
| `[Extractor Warning] Failed with model ...` in the console | Check `GROQ_API_KEY` in `src/.env`; the app automatically falls back to `ground_truth.json` |
| Network graph tab is blank | Refresh the page and click **RUN ANALYSIS** again; ensure the browser allows iframes/JavaScript |
