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
2. Select a star TIC ID to fetch its live JWST spectrum profiles.
3. Hover over the graphs to read telemetry values.
4. Open the **AI COPILOT** chat window to consult your AI space assistant for data analyzing.


I used Google Gemini 3.1 Pro Extended to design the code(both frontend and backend) and Claude Code(Sonnet 5 Extended) to identify bugs and errors for 90% of the project. 
