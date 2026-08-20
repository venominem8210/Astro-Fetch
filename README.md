# 🌌 Astro-Fetch: Live JWST Exoplanet Analyzer

**Astro-Fetch** is an interactive web platform that hooks directly into NASA's public data archives to analyze atmospheric chemical signatures from the James Webb Space Telescope (JWST). 

---

## ⚡ Core Interactive Features

### 📊 Hover-Responsive Light Curves
* **Precision Tracking:** Move your cursor across any data point on the graph to instantly view exact relative brightness and timing telemetry.
* **No Raw Text Dumps:** Data points automatically round to clear, readable values with tracking guide crosshairs.

### 🤖 AI Astrophysicist Chatbot
* **Context-Aware Assistance:** The built-in AI chatbot acts like an expert astronomer. It dynamically reads the current planet's data so it knows exactly what you are looking at.
* **Instant Explanations:** Click the suggested prompt chips or type your own questions to understand what the transmission spectra dips mean (e.g., *"Is there methane here?"*).

---

## 🛠️ How It Works Under the Hood

* **`aperture_jwst/`** — Connects directly to NASA's MAST API to pull real-time telescope datasets.
* **`astro/`** — Cleans and processes raw telescope signal noise into clean planetary atmospheric profiles.
* **`main.py`** — The engine running your Python data server that feeds data to your responsive Tailwind frontend dashboard.

---

## 🌐 Quick Start (For Reviewers)

1. Open the live deployment link in your browser.
2. Select an exoplanet to fetch its live JWST spectrum profiles.
3. Hover over the graphs to read telemetry values.
4. Open the **Team Radio** chat window to consult your AI space assistant.


## 📂 Project Structure

```text
Astro-Fetch/
│
├── aperture_jwst/          # JWST aperture and data fetching module
│   ├── fetcher.py          # Handles data retrieval routines
│   └── .gitignore
│
├── astro/                  # Core astronomy and calculation algorithms
│   └── algorithms.py       # Math and pipeline computation logic
│
├── main.py                 # Main execution entry point
└── README.md
