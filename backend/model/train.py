# model/train.py (metrics-enabled, no user-defined classes)
import os, re, json, joblib, numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

RANDOM_STATE = 42

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_dataset(csv_path, text_cols=("text","review","content","Review","Text"), label_cols=("label","target","is_fake","fake","Label")):
    if not os.path.exists(csv_path):
        raise FileNotFoundError("CSV not found: " + csv_path)
    df = pd.read_csv(csv_path)
    text_col  = next((x for x in text_cols if x in df.columns), None)
    label_col = next((x for x in label_cols if x in df.columns), None)
    if text_col is None or label_col is None:
        raise ValueError("Expected a text column and a label column (0/1). Found: " + str(list(df.columns)))
    df[label_col] = df[label_col].astype(int)
    df["text_clean"] = df[text_col].astype(str).apply(clean_text)
    return df, "text_clean", label_col

def compute_metrics(y_true, y_pred):
    prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
    acc = accuracy_score(y_true, y_pred)
    return {"precision": float(prec), "recall": float(rec), "f1": float(f1), "accuracy": float(acc)}

def save_metrics(artifacts_dir, info):
    os.makedirs(artifacts_dir, exist_ok=True)
    path = os.path.join(artifacts_dir, "metrics.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
    return path

def train_or_load(artifacts_dir, csv_path):
    os.makedirs(artifacts_dir, exist_ok=True)
    vec_path = os.path.join(artifacts_dir, "tfidf.joblib")
    mdl_path = os.path.join(artifacts_dir, "model.joblib")
    mtx_path = os.path.join(artifacts_dir, "metrics.json")

    if os.path.exists(vec_path) and os.path.exists(mdl_path) and os.path.exists(mtx_path):
        tfidf = joblib.load(vec_path)
        model = joblib.load(mdl_path)
        with open(mtx_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        return tfidf, model, {"status": "loaded", "metrics": metrics}

    df, text_col, label_col = load_dataset(csv_path)
    X = df[text_col].values
    y = df[label_col].values

    tfidf = TfidfVectorizer(lowercase=False, ngram_range=(1,2), min_df=1, max_df=0.95)
    Xv = tfidf.fit_transform(X)

    X_tr, X_te, y_tr, y_te = train_test_split(Xv, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    model = LogisticRegression(max_iter=300, random_state=RANDOM_STATE)
    model.fit(X_tr, y_tr)
    preds = model.predict(X_te)
    metrics = compute_metrics(y_te, preds)

    joblib.dump(tfidf, vec_path)
    joblib.dump(model, mdl_path)
    save_metrics(artifacts_dir, metrics)

    return tfidf, model, {"status": "trained", "metrics": metrics}

def predict_label(text, tfidf, model):
    X = tfidf.transform([text])
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0,1]
        label = int(proba >= 0.5)
        conf  = float(proba)
    else:
        score = model.decision_function(X)[0]
        conf  = 1 / (1 + np.exp(-score))
        label = int(conf >= 0.5)
    return {"label": label, "confidence": round(conf, 4)}
