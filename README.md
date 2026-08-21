# 🕵️ Fake Review Detection System

> A full-stack NLP application that analyzes product reviews and predicts whether a review is **genuine or fake** using machine learning.

<p align="center">
  <img src="fake-review-home.png" alt="Fake Review Detection System" width="850">
</p>

---

##  Overview

The **Fake Review Detection System** is a machine learning-powered web application designed to identify potentially deceptive product reviews.

The system processes review text using **TF-IDF feature extraction** and classifies it using a **Logistic Regression** model.

A **FastAPI REST API** provides real-time predictions and model performance metrics, while a lightweight HTML, CSS, and JavaScript frontend provides an interactive interface for users.

---

## ✨ Key Features

* 🔍 Detect fake and genuine product reviews
* ⚡ Real-time review classification
* 📊 Prediction confidence score
* 📈 View model performance metrics
* 🔄 Reload and retrain the model using another CSV dataset
* 🌐 FastAPI REST API
* 💻 Interactive web interface
* 🐳 Docker and Docker Compose support
* 🔗 CORS-enabled frontend/backend communication

---

The application also exposes model evaluation metrics including:

* Accuracy
* Precision
* Recall
* F1 Score

---

## Machine Learning Pipeline

```text
Product Review
      │
      ▼
Text Cleaning
      │
      ▼
TF-IDF Vectorization
Unigrams + Bigrams
      │
      ▼
Logistic Regression
      │
      ▼
Fake / Genuine Prediction
      │
      ▼
Confidence Score
```

The text vectorizer uses:

```text
TF-IDF
ngram_range = (1, 2)
max_df = 0.95
```

The classifier is implemented using:

```text
Logistic Regression
max_iter = 300
random_state = 42
```

The dataset is divided using an **80/20 train-test split** with stratification.

---

##  Tech Stack

| Area             | Technologies            |
| ---------------- | ----------------------- |
| Machine Learning | Scikit-learn            |
| NLP              | TF-IDF Vectorization    |
| Model            | Logistic Regression     |
| Backend          | Python, FastAPI         |
| Data Processing  | Pandas, NumPy           |
| Frontend         | HTML5, CSS3, JavaScript |
| API              | REST                    |
| Deployment       | Docker, Docker Compose  |
| Web Server       | Nginx                   |

---

## System Architecture

```text
┌──────────────────────────┐
│       User Browser       │
│   HTML / CSS / JavaScript│
└─────────────┬────────────┘
              │
              │ REST API
              ▼
┌──────────────────────────┐
│        FastAPI API       │
│                          │
│  /predict                │
│  /metrics                │
│  /healthz                │
│  /reload                 │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     NLP / ML Pipeline    │
│                          │
│ Text Cleaning            │
│       ↓                  │
│ TF-IDF                   │
│       ↓                  │
│ Logistic Regression      │
└──────────────────────────┘
```

---

## Project Structure

```text
Fake-Review-Detection-System/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── data/
│   │   └── fake_reviews_sample.csv
│   │
│   └── model/
│       └── train.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── nginx/
│   ├── default.conf
│   └── Dockerfile
│   
│ 
│
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

### Health Check

```http
GET /healthz
```

Example response:

```json
{
  "ok": true
}
```

### Predict Review

```http
POST /predict
```

Request:

```json
{
  "text": "This product is absolutely amazing!"
}
```

Example response:

```json
{
  "ok": true,
  "result": {
    "label": 1,
    "confidence": 0.87
  }
}
```

### Model Metrics

```http
GET /metrics
```

Returns:

```text
Accuracy
Precision
Recall
F1 Score
```

### Reload / Retrain Model

```http
POST /reload
```

The endpoint can load another CSV dataset and retrain the model.

---

## 🚀 Running the Project

### Backend

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

---

### Frontend

Open:

```text
frontend/index.html
```

in your browser.

The frontend communicates with the FastAPI backend through JavaScript.

---



## 📊 Dataset Format

The model accepts CSV datasets containing:

### Review text

Supported column names include:

```text
text
review
content
Review
Text
```

### Label

Supported label columns include:

```text
label
target
is_fake
fake
Label
```

Labels must be binary:

```text
0 / 1
```

---

## What I Learned

Through this project, I gained hands-on experience with:

* Natural Language Processing
* Text preprocessing
* TF-IDF feature extraction
* Machine learning classification
* Model evaluation
* REST API development with FastAPI
* Frontend-to-backend API integration
* Docker-based application deployment
* Structuring a full-stack machine learning application

---


