# 🌬️ UAE Air Quality Intelligence System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)

### Real-time air quality monitoring across 10 Dubai neighbourhoods
### Automated data pipeline · ML predictions · Live interactive dashboard

**[🚀 View Live App](https://mahammadsarfraz575-uae-air-quality-intelligence-app-erjrrr.streamlit.app)** &nbsp;|&nbsp; **[📊 GitHub Repo](https://github.com/mahammadsarfraz/uae-air-quality-intelligence)** &nbsp;|&nbsp; **[👤 LinkedIn](https://linkedin.com/in/mahammad-sarfraz)**

---

</div>

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [What It Does](#-what-it-does)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [How to Run Locally](#-how-to-run-locally)
- [API Reference](#-api-reference)
- [Monitored Locations](#-monitored-locations)
- [AQI Scale](#-aqi-scale)
- [Author](#-author)

---

## 🎯 Problem Statement

Dubai and the wider UAE face significant air quality challenges due to **sandstorms, construction dust, traffic emissions, and industrial activity**. Despite this, most residents have no easy way to:

- Know the **current air quality** in their specific neighbourhood
- Understand **health risks** before going outdoors
- See **predictions** for air quality over the next 24 hours
- Track how air quality **changes over time** across different areas

This project solves all four problems with a fully automated, real-time intelligence system.

---

## ✅ What It Does

| Feature | Description |
|---|---|
| **Real-time monitoring** | Pulls live air quality data every hour for 10 Dubai neighbourhoods |
| **Automated pipeline** | Data ingested from Open-Meteo API → stored in SQLite → dashboard auto-updates |
| **ML predictions** | XGBoost model forecasts next 24-hour AQI with confidence bands |
| **Location search** | Search any Dubai location — geocoded via OpenStreetMap Nominatim |
| **Health alerts** | Automatic advice based on current AQI level |
| **Historical trends** | AQI and PM2.5 trend charts per neighbourhood over 1–30 days |
| **Interactive map** | Live bubble map of all 10 areas colour-coded by risk level |
| **Cloud deployed** | Fully live on Streamlit Cloud — zero setup needed to view |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
│                                                                 │
│   Open-Meteo Air Quality API    Open-Meteo Weather API          │
│   (PM2.5, PM10, NO2, Ozone)    (Temp, Humidity, Wind)          │
└──────────────────────┬──────────────────────┬───────────────────┘
                       │                      │
                       ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   fetch_data.py                                 │
│                                                                 │
│   • Runs every hour automatically (schedule library)            │
│   • Fetches all 10 Dubai neighbourhoods in sequence             │
│   • Calculates AQI from PM2.5 using EPA formula                 │
│   • Saves each row to SQLite database                           │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     database.db (SQLite)                        │
│                                                                 │
│   timestamp | neighbourhood | lat | lon | pm2_5 | pm10 |       │
│   ozone | nitrogen_dioxide | aqi | temperature | humidity |     │
│   wind_speed | risk_level                                       │
│                                                                 │
│   Grows by 10 rows every hour → 240 rows/day → 7,200/month     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ML Pipeline (XGBoost)                        │
│                                                                 │
│   Features: hour of day, day of week, temperature, humidity,   │
│   wind speed, PM2.5 lags (1h, 3h, 6h, 12h, 24h)               │
│                                                                 │
│   Output: 24-hour AQI forecast with confidence band            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    app.py (Streamlit)                           │
│                                                                 │
│   🗺️  Live Map      📊 All Areas      📈 Trends    🤖 Predictions│
│                                                                 │
│   • Auto-refreshes every 5 minutes                             │
│   • Falls back to live API if no database exists               │
│   • Location search via Nominatim geocoding                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              Streamlit Cloud (Free Deployment)                  │
│     https://mahammadsarfraz575-uae-air-quality-...app           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core logic |
| **Dashboard** | Streamlit | Live web interface |
| **Visualisation** | Plotly | Interactive charts and map |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Machine Learning** | XGBoost, Scikit-learn | AQI prediction model |
| **Database** | SQLite | Auto-growing local storage |
| **Air Quality API** | Open-Meteo | Free, no API key needed |
| **Geocoding API** | Nominatim (OpenStreetMap) | Location search |
| **Scheduling** | schedule | Hourly auto-fetch |
| **Deployment** | Streamlit Cloud | Free live hosting |

---

## ✨ Features

### 🗺️ Live Interactive Map
Bubble map of all 10 Dubai neighbourhoods colour-coded by AQI risk level. Hover each bubble to see AQI, PM2.5, and temperature. Bubble size scales with pollution level.

### 🔍 Location Search
Search any Dubai area by name — Downtown, Marina, JBR, DIFC, Silicon Oasis, or any landmark. Uses OpenStreetMap Nominatim geocoding to find coordinates, then fetches live AQI for that exact location.

### 📊 Neighbourhood Ranking
All 10 areas ranked worst to best with a bar chart and full data table. Threshold lines at AQI 100 (Moderate) and 150 (Unhealthy) for quick reference.

### 📈 Historical Trends
Select any neighbourhood and time range (1, 3, 7, 14, or 30 days). Dual-axis chart shows AQI trend and PM2.5 concentration over time. Activates after 24 hours of data collection.

### 🤖 ML Predictions
XGBoost model trained on historical data predicts AQI for the next 24 hours. Shows confidence band, worst hour, best hour, and 24-hour average. Activates after 48 hours of data.

### 🚨 Health Alerts
Automatic colour-coded advice based on current average AQI. Tells users whether it is safe to exercise, go outdoors, or whether they should stay indoors.

### ℹ️ About Panel
Built-in explanation of the AQI scale, what each pollutant means, and how the system works — so any user can understand the data without prior knowledge.

---

## 📁 Project Structure

```
uae-air-quality-intelligence/
│
├── app.py                  ← Streamlit dashboard (main file)
├── fetch_data.py           ← Hourly API fetch + SQLite storage
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
├── debug.py                ← API connection diagnostic tool
│
├── database.db             ← Auto-created SQLite (gitignored)
└── .gitignore
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/mahammadsarfraz/uae-air-quality-intelligence.git
cd uae-air-quality-intelligence
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Start data collection (Terminal 1)
```bash
python fetch_data.py
```
This runs forever, collecting data every hour automatically. You will see output like:
```
============================================================
🕐  2026-05-14 10:00:00  — Fetching all Dubai areas
============================================================
  🟡 Al Rashidiya         AQI: 87     PM2.5: 22.4    [Moderate]
  🟡 Al Warqa             AQI: 91     PM2.5: 23.8    [Moderate]
  🔴 Abu Hail             AQI: 103    PM2.5: 28.1    [Unhealthy (Sensitive)]
  ...
✅  All done! Next fetch in 1 hour.
```

### Step 4 — Launch dashboard (Terminal 2)
```bash
streamlit run app.py
```
Opens at **http://localhost:8501**

> **Note:** The dashboard works immediately even without a database — it falls back to fetching live API data directly. Historical trends and ML predictions activate after 24–48 hours of data collection.

### Step 5 — Diagnose API issues (optional)
If data shows all zeros:
```bash
python debug.py
```
This tests your internet and both APIs and reports exactly what is working.

---

## 📡 API Reference

### Open-Meteo Air Quality API
```
Base URL: https://air-quality-api.open-meteo.com/v1/air-quality
Method:   GET
Auth:     None (completely free, no key needed)

Parameters:
  latitude       float    Location latitude
  longitude      float    Location longitude
  hourly         string   pm2_5,pm10,nitrogen_dioxide,ozone
  forecast_days  int      1
  timezone       string   Asia/Dubai

Returns:
  hourly.pm2_5              []float   PM2.5 µg/m³ per hour
  hourly.pm10               []float   PM10 µg/m³ per hour
  hourly.nitrogen_dioxide   []float   NO2 µg/m³ per hour
  hourly.ozone              []float   O3 µg/m³ per hour
```

### Open-Meteo Weather API
```
Base URL: https://api.open-meteo.com/v1/forecast
Method:   GET
Auth:     None (completely free, no key needed)

Parameters:
  latitude   float    Location latitude
  longitude  float    Location longitude
  current    string   temperature_2m,relative_humidity_2m,wind_speed_10m
  timezone   string   Asia/Dubai

Returns:
  current.temperature_2m          float   Temperature in °C
  current.relative_humidity_2m    float   Humidity %
  current.wind_speed_10m          float   Wind speed km/h
```

### AQI Calculation (EPA Formula)
```python
def calculate_aqi(pm25):
    if pm25 <= 12:    return (50/12) * pm25           # Good
    if pm25 <= 35.4:  return 50  + (50/23.4)*(pm25-12)    # Moderate
    if pm25 <= 55.4:  return 100 + (50/20)  *(pm25-35.4)  # Sensitive
    if pm25 <= 150:   return 150 + (50/94.6) *(pm25-55.4) # Unhealthy
    return                   200 + (100/149.6)*(pm25-150)  # Hazardous
```

---

## 📍 Monitored Locations

| Neighbourhood | Latitude | Longitude | Area Type |
|---|---|---|---|
| Al Rashidiya | 25.2245 | 55.3890 | Residential |
| Al Warqa | 25.1913 | 55.4087 | Residential |
| Abu Hail | 25.2859 | 55.3282 | Mixed |
| Deira | 25.2788 | 55.3271 | Commercial |
| Bur Dubai | 25.2146 | 55.3033 | Commercial |
| Al Quoz | 25.1542 | 55.2561 | Industrial |
| Jumeirah | 25.2028 | 55.2413 | Residential |
| Al Barsha | 25.1076 | 55.2044 | Residential |
| Mirdif | 25.2194 | 55.4249 | Residential |
| Al Nahda | 25.2893 | 55.3641 | Mixed |

---

## 🌡️ AQI Scale

| AQI Range | Category | Health Implication | Colour |
|---|---|---|---|
| 0 – 50 | **Good** | Air quality is satisfactory | 🟢 Green |
| 51 – 100 | **Moderate** | Acceptable; sensitive groups should limit outdoor time | 🟡 Yellow |
| 101 – 150 | **Unhealthy (Sensitive)** | Elderly, children, and people with respiratory issues should reduce outdoor activity | 🟠 Orange |
| 151 – 200 | **Unhealthy** | Everyone should reduce prolonged outdoor activity | 🔴 Red |
| 200+ | **Hazardous** | Avoid all outdoor activity; keep windows closed | 🟣 Purple |

---

## 💡 Key Pollutants

| Pollutant | Full Name | Main Source in Dubai | Health Impact |
|---|---|---|---|
| **PM2.5** | Fine particulate matter | Sandstorms, construction, traffic | Penetrates deep into lungs |
| **PM10** | Coarse particulate matter | Desert dust, road dust | Irritates respiratory tract |
| **NO2** | Nitrogen dioxide | Vehicle emissions, construction | Aggravates asthma |
| **Ozone** | Ground-level ozone | Sunlight + traffic emissions | Worsens in summer heat |

---

## 📊 Database Schema

```sql
CREATE TABLE air_quality (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp        TEXT,           -- "2026-05-14 10:00:00"
    neighbourhood    TEXT,           -- "Al Rashidiya"
    latitude         REAL,           -- 25.2245
    longitude        REAL,           -- 55.3890
    pm2_5            REAL,           -- µg/m³
    pm10             REAL,           -- µg/m³
    ozone            REAL,           -- µg/m³
    nitrogen_dioxide REAL,           -- µg/m³
    aqi              REAL,           -- 0–500
    temperature      REAL,           -- °C
    humidity         REAL,           -- %
    wind_speed       REAL,           -- km/h
    risk_level       TEXT            -- "Good" / "Moderate" / etc.
);
```

Data grows at: **10 rows/hour → 240 rows/day → 7,200 rows/month**

---

## 🤖 ML Model Details

| Parameter | Value |
|---|---|
| Algorithm | XGBoost Regressor |
| Target | AQI (next hour) |
| Features | Hour of day, day of week, month, temperature, humidity, wind speed, PM2.5 lags (1h/3h/6h/12h/24h) |
| Training data | Historical hourly readings (grows over time) |
| Evaluation | MAE, RMSE, R² score |
| Prediction horizon | 24 hours with confidence band |
| Retrains | Every time new data is available |

---

## 🌍 Why This Matters

Dubai is ranked among cities with **frequent poor air quality days** due to:
- Desert sandstorms (PM10 and PM2.5 spikes)
- Rapid construction activity
- High traffic density
- Extreme heat accelerating ozone formation

This system helps **residents, schools, hospitals, and outdoor event organisers** make data-driven decisions based on current and predicted air quality — before health impacts occur.

This aligns directly with the **UAE Vision 2031** environmental targets and Dubai's **Smart City Initiative**.

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 👤 Author

**Mahammad Sarfraz**
Data Scientist | MCA – Data Science Specialization | Dubai, UAE

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/mahammad-sarfraz)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mahammadsarfraz)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mahammadsarfraz575@gmail.com)
[![Live App](https://img.shields.io/badge/Live_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://mahammadsarfraz575-uae-air-quality-intelligence-app-erjrrr.streamlit.app)

---

<div align="center">

**⭐ If this project helped you, please give it a star on GitHub!**

*Data source: [Open-Meteo](https://open-meteo.com/) — free, open-source weather and air quality API*

</div>
