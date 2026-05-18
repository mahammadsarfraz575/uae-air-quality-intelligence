"""
test_api.py — Run this to verify API is working
Command: python test_api.py
"""
import requests

print("\n" + "="*55)
print("  UAE Air Quality — API Connection Test")
print("="*55)

# ── 1. Internet ──────────────────────────────────────────
try:
    requests.get("https://www.google.com", timeout=5)
    print("✅ Internet:        Connected")
except Exception as e:
    print(f"❌ Internet:        FAILED — {e}")
    print("   Fix: Check your WiFi or network connection")
    exit()

# ── 2. Air Quality API (hourly) ──────────────────────────
print("\n── Air Quality API (Dubai center) ─────────────────")
try:
    r = requests.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        params={
            "latitude":      25.2048,
            "longitude":     55.2708,
            "hourly":        ["pm10","pm2_5","nitrogen_dioxide","ozone"],
            "forecast_days": 1,
            "timezone":      "Asia/Dubai"
        },
        timeout=15
    )
    print(f"✅ Status code:     {r.status_code}")
    data   = r.json()
    hourly = data.get("hourly", {})

    def latest(key):
        vals  = hourly.get(key, [])
        valid = [v for v in vals if v is not None]
        return round(valid[-1], 2) if valid else "N/A"

    print(f"✅ PM2.5:           {latest('pm2_5')} µg/m³")
    print(f"✅ PM10:            {latest('pm10')} µg/m³")
    print(f"✅ NO2:             {latest('nitrogen_dioxide')} µg/m³")
    print(f"✅ Ozone:           {latest('ozone')} µg/m³")
    print(f"   Hours returned:  {len(hourly.get('time', []))}")
except Exception as e:
    print(f"❌ Air Quality API: FAILED — {e}")

# ── 3. Weather API ───────────────────────────────────────
print("\n── Weather API (Dubai center) ──────────────────────")
try:
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude":  25.2048,
            "longitude": 55.2708,
            "current":   ["temperature_2m","relative_humidity_2m","wind_speed_10m"],
            "timezone":  "Asia/Dubai"
        },
        timeout=15
    )
    print(f"✅ Status code:     {r.status_code}")
    cur = r.json().get("current", {})
    print(f"✅ Temperature:     {cur.get('temperature_2m')}°C")
    print(f"✅ Humidity:        {cur.get('relative_humidity_2m')}%")
    print(f"✅ Wind speed:      {cur.get('wind_speed_10m')} km/h")
except Exception as e:
    print(f"❌ Weather API:     FAILED — {e}")

print("\n" + "="*55)
print("  If all ✅ — run:  streamlit run app.py")
print("="*55 + "\n")
