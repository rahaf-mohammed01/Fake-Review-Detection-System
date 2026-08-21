const API_BASE = (location.hostname === 'localhost' || location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:8000'
  : 'http://127.0.0.1:8000'; // change if deploying elsewhere

async function predict(text) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  if (!res.ok) throw new Error('Network response was not ok');
  return res.json();
}

async function fetchMetrics() {
  const res = await fetch(`${API_BASE}/metrics`);
  if (!res.ok) throw new Error('Failed to fetch metrics');
  return res.json();
}

document.addEventListener('DOMContentLoaded', () => {
  const textarea = document.getElementById('review');
  const btn = document.getElementById('predictBtn');
  const status = document.getElementById('status');
  const result = document.getElementById('result');
  const metricsBtn = document.getElementById('metricsBtn');
  const metricsBox = document.getElementById('metrics');

  btn.addEventListener('click', async () => {
    const text = textarea.value.trim();
    result.innerHTML = '';
    if (!text) {
      result.textContent = 'Please paste a review first.';
      return;
    }
    status.textContent = 'Predicting...';
    try {
      const data = await predict(text);
      status.textContent = '';
      if (data && data.ok && data.result) {
        const { label, confidence } = data.result;
        const labelText = label === 1 ? 'REAL (1)' : 'FAKE (0)';
        result.innerHTML = `<div><span class="k">Prediction:</span> <span class="v">${labelText}</span></div>
                            <div><span class="k">Confidence:</span> <span class="v">${(confidence*100).toFixed(1)}%</span></div>`;
      } else {
        result.textContent = 'Unexpected response.';
      }
    } catch (err) {
      status.textContent = '';
      result.textContent = 'Error: ' + err.message;
    }
  });

  metricsBtn.addEventListener('click', async () => {
    metricsBox.textContent = 'Loading metrics...';
    try {
      const data = await fetchMetrics();
      if (data && data.ok && data.metrics) {
        const m = data.metrics;
        metricsBox.innerHTML = `<div><span class="k">F1:</span> <span class="v">${m.f1.toFixed(3)}</span></div>
                                <div><span class="k">Precision:</span> <span class="v">${m.precision.toFixed(3)}</span></div>
                                <div><span class="k">Recall:</span> <span class="v">${m.recall.toFixed(3)}</span></div>
                                <div><span class="k">Accuracy:</span> <span class="v">${m.accuracy.toFixed(3)}</span></div>`;
      } else {
        metricsBox.textContent = 'Metrics not available.';
      }
    } catch (err) {
      metricsBox.textContent = 'Error: ' + err.message;
    }
  });
});
