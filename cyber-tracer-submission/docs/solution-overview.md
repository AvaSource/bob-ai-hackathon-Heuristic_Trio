# Solution Overview

## What We Built

Cyber-Tracer Pro is a Streamlit "SOC console" for fraud investigators. You drop in the case files you have — transaction CSVs, device/IMEI lists, call logs and a free-text intel report — and it builds a single picture of the fraud network: who moved money to whom, which accounts share handsets, and who is at the centre. It then ranks the likely kingpin and mule accounts and writes the FIR case brief for you.

## How It Works

1. **Ingest** — The user uploads CSV / TXT / ZIP files or loads the built-in demo case (`app.py`).
2. **Extract** — The free-text field intel is sent to an LLM (Groq, Llama 3.3 70B, with Mixtral / Gemma fallbacks) with a strict JSON schema prompt, returning entities (person, account, device, SIM) and relationships (TRANSFERRED_TO, REGISTERED_TO, USED_ON, CALLED) (`extractor.py`). If no API key is configured or all models fail, it falls back to `dataset/ground_truth.json` so the demo always runs.
3. **Build graph** — Transactions, device/IMEI registrations and call logs are fused into a NetworkX directed graph. Column names are detected flexibly so different dataset schemas work (`graph_builder.py`).
4. **Score** — Each node gets `0.6 × betweenness centrality + 0.4 × in-degree centrality`. The top node is flagged as the kingpin; the next top-ranked account nodes are flagged as mules.
5. **Visualise & investigate** — An interactive PyVis graph, an India geospatial trace, an entity ledger and a per-suspect inspector (in/out flow, transaction timeline) are shown in tabs.
6. **Report** — A ReportLab FIR case brief PDF and a JSON export of extracted entities are generated for download (`report_generator.py`).

## Architecture Diagram

> See [`architecture.md`](architecture.md) for the detailed diagram.

```
[Case files: CSV/TXT/ZIP] → [Streamlit app.py]
        │                        │
        ├─ intel .txt ─→ [extractor.py → Groq LLM] ─→ entities JSON
        └─ CSVs ──────→ [graph_builder.py → NetworkX] ─→ kingpin / mules
                                 │
               [PyVis graph · Plotly map · Ledger · Inspector]
                                 │
                     [report_generator.py → FIR PDF]
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Graph centrality (betweenness + in-degree) for kingpin/mule detection | Mule networks are defined by structure — fan-in and brokerage — which centrality captures directly and explainably, without needing labelled training data. |
| LLM with strict JSON output for unstructured intel | Field reports are free prose; an LLM reliably pulls out names, numbers and IMEIs into a schema the graph can use. |
| Multi-model fallback + ground-truth fallback | Keeps the demo and field use working when a model is deprecated, rate-limited or offline. |
| Schema-tolerant CSV parsing | Real data from banks/telcos arrives with inconsistent column names; the builder adapts instead of requiring a fixed format. |
| Synthetic dataset modelled on public typologies | Real FIRs, SARs and CDRs are confidential; synthetic data preserves the structure (mule fan-in, shared IMEIs, layering) without privacy risk. |

## IBM Technologies Used

- **TODO:** Describe specifically how IBM Bob (or other IBM tech) was used in building or running this project. The judging rubric awards 10 points for IBM Bob integration.
