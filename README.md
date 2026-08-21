# Fake Review Detection — Full Stack (FastAPI + Vanilla JS) — v2

**No user-defined classes.** Backend in Python (FastAPI), frontend in HTML/CSS/JS.  
**Now with:** `/metrics` endpoint + Docker + docker-compose.

## Quickstart (Local, no Docker)

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend
Open `frontend/index.html` directly in the browser, or serve statically.  
By default, it calls `http://127.0.0.1:8000`—change `API_BASE` in `frontend/script.js` if needed.

## Endpoints
- `GET /healthz` → `{"ok": true}`
- `GET /metrics` → training metrics `{"f1", "precision", "recall", "accuracy"}`
- `POST /predict` → `{"ok": true, "result": { "label": 0|1, "confidence": 0..1 } }`
- `POST /reload` → retrain/load; body `{"csv_path": "/abs/path/to.csv"}`

## Use your Kaggle dataset
```
curl -X POST http://127.0.0.1:8000/reload   -H "Content-Type: application/json"   -d '{"csv_path":"C:/path/to/your.csv"}'
```

Your CSV should include a text column (e.g., `text`, `review`) and a binary label (`label`, `fake`, `is_fake`).

## Docker

Build and run both services (backend + nginx serving the frontend) with:
```bash
docker compose up --build
```
- Frontend: http://127.0.0.1:5173
- Backend:  http://127.0.0.1:8000

### Re-train with your CSV inside Docker
- Mount or copy your CSV to a reachable path in the backend container, or expose a host path via `volumes`.  
- Then call `POST /reload` with that internal path.

## Notes
- Metrics are stored at `backend/model/artifacts/metrics.json`.
- All code uses **functions only**—no user-defined `class` anywhere.
