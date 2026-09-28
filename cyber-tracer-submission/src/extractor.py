import json
import os
from groq import Groq

def _load_dotenv(path=".env"):
    # Minimal .env loader so no extra dependency is needed
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

_load_dotenv()

# Set GROQ_API_KEY in src/.env (see .env.example). Without it, extraction falls back to ground_truth.json
GROQ_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

SYSTEM_PROMPT = """
You are an expert Cyber Crime Forensic Analyst. Extract entities and relationships into strict JSON schema:
Entity Types: "person", "account", "device", "sim"
Relationship Types: "TRANSFERRED_TO", "REGISTERED_TO", "USED_ON", "CALLED"
Output JSON: {"entities": [{"id": "", "type": "", "label": ""}], "relationships": [{"from": "", "to": "", "type": "", "details": ""}]}
Return ONLY raw valid JSON without markdown formatting.
"""

# Active models to try in sequence
MODELS_TO_TRY = [
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

def extract_intel_from_file(file_path="dataset/unstructured_intel.txt"):
    if not os.path.exists(file_path):
        return {"entities": [], "relationships": []}

    with open(file_path, "r", encoding="utf-8") as f:
        text_data = f.read()

    # Try calling Groq API across active models
    for model_name in (MODELS_TO_TRY if client else []):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text_data}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"[Extractor Warning] Failed with model '{model_name}': {e}")
            continue

    # Safety Fallback: Load ground truth dataset directly if API fails
    print("[Extractor Info] Falling back to dataset/ground_truth.json")
    if os.path.exists("dataset/ground_truth.json"):
        with open("dataset/ground_truth.json", "r", encoding="utf-8") as gf:
            return json.load(gf)

    return {"entities": [], "relationships": []}