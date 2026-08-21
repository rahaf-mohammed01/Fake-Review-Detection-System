# backend/app.py
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import os, json
from model.train import train_or_load, predict_label, clean_text

ARTIFACTS = os.path.join(os.path.dirname(__file__), "model", "artifacts")
DATA_CSV = os.path.join(os.path.dirname(__file__), "data", "fake_reviews_sample.csv")
METRICS_JSON = os.path.join(ARTIFACTS, "metrics.json")

app = FastAPI(title="Fake Review Detector", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TFIDF = None
MODEL = None
INFO  = None

def ensure_model_ready():
    global TFIDF, MODEL, INFO
    if TFIDF is None or MODEL is None:
        TFIDF, MODEL, INFO = train_or_load(ARTIFACTS, DATA_CSV)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/metrics")
def get_metrics():
    ensure_model_ready()
    if os.path.exists(METRICS_JSON):
        with open(METRICS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"ok": True, "metrics": data}
    return {"ok": False, "error": "metrics not found"}

@app.post("/predict")
def predict(payload: dict = Body(...)):
    ensure_model_ready()
    text = payload.get("text", "")
    text_clean = clean_text(text)
    out = predict_label(text_clean, TFIDF, MODEL)
    return {"ok": True, "result": out}

@app.post("/reload")
def reload_model(payload: dict = Body(None)):
    csv_path = DATA_CSV
    if payload and "csv_path" in payload and os.path.exists(payload["csv_path"]):
        csv_path = payload["csv_path"]
    global TFIDF, MODEL, INFO
    TFIDF = MODEL = INFO = None
    TFIDF, MODEL, INFO = train_or_load(ARTIFACTS, csv_path)
    return {"ok": True, "info": INFO}
