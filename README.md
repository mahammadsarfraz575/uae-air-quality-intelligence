# 🌬️ UAE Air Quality Intelligence System

**Real-time air quality monitoring across 10 Dubai neighbourhoods — powered by ML predictions**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://your-link.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🎯 What This Project Does

This system automatically collects real-time air quality data for 10 Dubai neighbourhoods every hour, stores it in a growing database, and displays it on a live interactive dashboard. An ML model predicts the next 24 hours of air quality based on historical patterns.

**Live link:** [https://your-link.streamlit.app](https://your-link.streamlit.app)

---

## 🏙️ Neighbourhoods Monitored

| Neighbourhood | Latitude | Longitude |
|---|---|---|
| Al Rashidiya | 25.2245 | 55.3890 |
| Al Warqa | 25.1913 | 55.4087 |
| Abu Hail | 25.2859 | 55.3282 |
| Deira | 25.2788 | 55.3271 |
| Bur Dubai | 25.2146 | 55.3033 |
| Al Quoz | 25.1542 | 55.2561 |
| Jumeirah | 25.2028 | 55.2413 |
| Al Barsha | 25.1076 | 55.2044 |
| Mirdif | 25.2194 | 55.4249 |
| Al Nahda | 25.2893 | 55.3641 |

---

## 🏗️ System Architecture

```
Open-Meteo API (free)
        ↓
  fetch_data.py          ← runs every hour automatically
        ↓
   SQLite database        ← grows continuously
        ↓
   app.py (Streamlit)     ← live dashboard, auto-refreshes every 5 min
        ↓
  Live web link           ← share in CV + LinkedIn
```

---

## 📊 Features

- **Live map** — AQI bubble map of all Dubai areas colour-coded by risk
- **All areas ranking** — bar chart + table sorted worst to best
- **Historical trends** — AQI and PM2.5 over time per neighbourhood
- **ML predictions** — 24-hour AQI forecast with confidence bands
- **Health alerts** — automatic advice based on current AQI
- **Auto-refresh** — dashboard updates every 5 minutes automatically

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data source | Open-Meteo API (free, no key needed) |
| Auto-fetch | Python + schedule library |
| Storage | SQLite (grows automatically) |
| ML model | XGBoost regressor |
| Dashboard | Streamlit + Plotly |
| Deployment | Streamlit Cloud (free) |

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/mahammadsarfraz/uae-air-quality.git
cd uae-air-quality

# 2. Install libraries
pip install -r requirements.txt

# 3. Start data collection (leave running in background)
python fetch_data.py

# 4. Open the dashboard (new terminal)
streamlit run app.py
```

---

## 📈 What the Data Shows

- **AQI (Air Quality Index)** — 0–50 Good, 51–100 Moderate, 101–150 Sensitive, 151+ Unhealthy
- **PM2.5** — Fine particulate matter (main pollutant in Dubai)
- **PM10** — Coarse dust (common during sandstorms)
- **NO2** — Nitrogen dioxide from traffic
- **Ozone** — Ground-level ozone

---

## 👨‍💻 About

Built by **Mahammad Sarfraz** — Data Scientist based in Dubai, UAE.

- 📧 mahammadsarfraz575@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/mahammad-sarfraz)
- 🐙 [GitHub](https://github.com/mahammadsarfraz)

---

*Data source: [Open-Meteo](https://open-meteo.com/) — free, open-source weather and air quality API*
