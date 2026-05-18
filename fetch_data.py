"""
fetch_data.py
UAE Air Quality Intelligence System
Fetches real-time air quality data for 10 Dubai neighbourhoods every hour
Run this file first: python fetch_data.py
"""

import requests
import sqlite3
from datetime import datetime
import schedule
import time

# ── 10 DUBAI NEIGHBOURHOODS ──────────────────────────────
LOCATIONS = {
    "Al Rashidiya": {"lat": 25.2245, "lon": 55.3890},
    "Al Warqa":     {"lat": 25.1913, "lon": 55.4087},
    "Abu Hail":     {"lat": 25.2859, "lon": 55.3282},
    "Deira":        {"lat": 25.2788, "lon": 55.3271},
    "Bur Dubai":    {"lat": 25.2146, "lon": 55.3033},
    "Al Quoz":      {"lat": 25.1542, "lon": 55.2561},
    "Jumeirah":     {"lat": 25.2028, "lon": 55.2413},
    "Al Barsha":    {"lat": 25.1076, "lon": 55.2044},
    "Mirdif":       {"lat": 25.2194, "lon": 55.4249},
    "Al Nahda":     {"lat": 25.2893, "lon": 55.3641},
}

# ── DATABASE SETUP ───────────────────────────────────────
def setup_database():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS air_quality (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp        TEXT,
            neighbourhood    TEXT,
            latitude         REAL,
            longitude        REAL,
            pm2_5            REAL,
            pm10             REAL,
            ozone            REAL,
            nitrogen_dioxide REAL,
            aqi              REAL,
            temperature      REAL,
            humidity         REAL,
            wind_speed       REAL,
            risk_level       TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database ready — database.db created")

# ── AQI CALCULATION ──────────────────────────────────────
def calculate_aqi(pm25):
    if not pm25: return None
    if pm25 <= 12:     return round((50 / 12) * pm25)
    elif pm25 <= 35.4: return round(50 + (50 / 23.4) * (pm25 - 12))
    elif pm25 <= 55.4: return round(100 + (50 / 20) * (pm25 - 35.4))
    elif pm25 <= 150.4:return round(150 + (50 / 94.6) * (pm25 - 55.4))
    else:              return round(200 + (100 / 149.6) * (pm25 - 150.4))

def get_risk_level(aqi):
    if not aqi:    return "Unknown"
    if aqi <= 50:  return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy (Sensitive)"
    if aqi <= 200: return "Unhealthy"
    return "Very Unhealthy"

# ── FETCH ONE NEIGHBOURHOOD ──────────────────────────────
def fetch_one(name, lat, lon):
    try:
        # ── Air Quality — use hourly, take latest valid value ──
        aq_resp = requests.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={
                "latitude":      lat,
                "longitude":     lon,
                "hourly":        ["pm10","pm2_5","nitrogen_dioxide","ozone"],
                "forecast_days": 1,
                "timezone":      "Asia/Dubai"
            },
            timeout=10
        ).json()

        hourly = aq_resp.get("hourly", {})

        def latest_val(key):
            vals  = hourly.get(key, [])
            valid = [v for v in vals if v is not None]
            return valid[-1] if valid else 0.0

        pm25 = latest_val("pm2_5")
        pm10 = latest_val("pm10")
        no2  = latest_val("nitrogen_dioxide")
        oz   = latest_val("ozone")

        # ── Weather — current works fine ──
        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude":  lat,
                "longitude": lon,
                "current":   ["temperature_2m","relative_humidity_2m","wind_speed_10m"],
                "timezone":  "Asia/Dubai"
            },
            timeout=10
        ).json().get("current", {})

        aqi  = calculate_aqi(pm25)
        risk = get_risk_level(aqi)

        conn = sqlite3.connect("database.db")
        conn.execute("""
            INSERT INTO air_quality
            (timestamp, neighbourhood, latitude, longitude,
             pm2_5, pm10, ozone, nitrogen_dioxide, aqi,
             temperature, humidity, wind_speed, risk_level)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name, lat, lon,
            pm25, pm10, oz, no2, aqi,
            w.get("temperature_2m"),
            w.get("relative_humidity_2m"),
            w.get("wind_speed_10m"),
            risk
        ))
        conn.commit()
        conn.close()

        icon = "🟢" if aqi <= 50 else "🟡" if aqi <= 100 else "🔴"
        print(f"  {icon} {name:<22} AQI: {str(aqi):<6} PM2.5: {str(round(pm25,1)):<8} [{risk}]")

    except Exception as e:
        print(f"  ❌ {name:<22} Error: {e}")

# ── FETCH ALL 10 AREAS ───────────────────────────────────
def fetch_all():
    print(f"\n{'='*60}")
    print(f"🕐  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  — Fetching all Dubai areas")
    print(f"{'='*60}")
    for name, coords in LOCATIONS.items():
        fetch_one(name, coords["lat"], coords["lon"])
    print(f"{'='*60}")
    print(f"✅  All 10 areas saved. Next auto-fetch in 1 hour.\n")

# ── RUN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🌬️  UAE Air Quality Intelligence System")
    print("━" * 60)
    setup_database()
    fetch_all()
    schedule.every().hour.do(fetch_all)
    print("🚀  Running... auto-fetching every hour. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(60)
