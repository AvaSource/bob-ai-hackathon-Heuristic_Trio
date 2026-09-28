# Source Code

Run everything from this folder: `pip install -r requirements.txt` then `streamlit run app.py`.

## Layout

```
src/
├── app.py                      ← Streamlit SOC console (entry point, UI tabs, geospatial map, inspector)
├── extractor.py                ← LLM entity/relationship extraction from unstructured intel (Groq)
├── graph_builder.py            ← Builds the fraud graph, scores kingpin/mules, exports PyVis HTML
├── report_generator.py         ← Generates the FIR case brief PDF (ReportLab)
├── requirements.txt
├── .env.example                ← Copy to .env and set GROQ_API_KEY (optional)
├── dataset/                    ← Jamtara-pattern synthetic case: accounts, transactions, devices,
│                                 call logs, unstructured_intel.txt, ground_truth.json
├── cyber_fraud_mock_dataset/   ← Larger multi-case synthetic dataset (cases, persons, SIMs, devices,
│                                 bank accounts, transactions, calls, locations, relationships)
└── lib/                        ← vis.js / tom-select assets used by the PyVis graph
```

See each dataset folder's README for provenance. All data is synthetic.

Generated at runtime (not committed): `network.html`, `FIR_Case_Brief.pdf`.
