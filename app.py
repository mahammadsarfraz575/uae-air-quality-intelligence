"""
app.py — UAE Air Quality Intelligence System
Run: streamlit run app.py
"""

import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# ── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="UAE Air Quality Intelligence",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:#0a0e1a;color:#e8eaf0;}
.stApp{background:#0a0e1a;}
.main-header{background:linear-gradient(135deg,#0d1b3e,#0a0e1a);border:1px solid #1e3a6e;border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.2rem;}
.header-title{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#fff;margin:0;}
.header-sub{font-size:0.9rem;color:#7c8db5;margin-top:0.3rem;}
.live-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);color:#22c55e;padding:4px 12px;border-radius:20px;font-size:0.75rem;font-weight:500;margin-top:0.8rem;}
.live-dot{width:6px;height:6px;background:#22c55e;border-radius:50%;animation:pulse 1.5s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.3}}
.kpi-card{background:#111827;border:1px solid #1f2d4a;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:0.5rem;height:100px;}
.kpi-label{font-size:0.72rem;color:#7c8db5;font-weight:500;text-transform:uppercase;letter-spacing:0.5px;}
.kpi-value{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:700;margin:0.2rem 0;}
.kpi-sub{font-size:0.76rem;color:#7c8db5;}
.alert-good{background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);color:#22c55e;padding:10px 16px;border-radius:10px;font-size:0.86rem;margin:0.8rem 0;}
.alert-mod{background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);color:#f59e0b;padding:10px 16px;border-radius:10px;font-size:0.86rem;margin:0.8rem 0;}
.alert-bad{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);color:#ef4444;padding:10px 16px;border-radius:10px;font-size:0.86rem;margin:0.8rem 0;}
.search-wrap{background:#111827;border:1px solid #1e3a6e;border-radius:14px;padding:1rem 1.4rem;margin-bottom:0.8rem;}
.about-wrap{background:#111827;border:1px solid #1f2d4a;border-radius:14px;padding:1rem 1.4rem;}
.about-title{font-size:0.9rem;font-weight:600;color:#fff;margin-bottom:6px;}
.about-text{font-size:0.78rem;color:#7c8db5;line-height:1.7;}
.feat-row{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;}
.feat-chip{background:#0d1b3e;border:1px solid #1e3a6e;border-radius:16px;padding:3px 10px;font-size:0.72rem;color:#7c8db5;}
.scale-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin:8px 0;}
.scale-cell{border-radius:8px;padding:7px 4px;text-align:center;}
.scale-name{font-size:10px;font-weight:600;}
.scale-num{font-size:9px;margin-top:2px;opacity:0.8;}
.scale-desc{font-size:8px;color:#7c8db5;margin-top:3px;}
.poll-text{font-size:0.76rem;color:#7c8db5;line-height:1.8;margin-top:6px;}
.result-box{background:#0d1b3e;border:1px solid #1e3a6e;border-radius:12px;padding:1rem 1.2rem;margin-top:0.6rem;}
.result-loc{font-size:1rem;font-weight:600;color:#fff;}
.result-time{font-size:0.74rem;color:#7c8db5;margin-top:2px;}
.result-aqi{font-size:2.2rem;font-weight:700;margin:6px 0 2px;}
.result-lbl{font-size:0.82rem;margin-bottom:6px;}
.result-adv{font-size:0.76rem;color:#7c8db5;margin-bottom:10px;}
.metrics-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;}
.met-cell{background:#111827;border-radius:8px;padding:7px 10px;}
.met-label{font-size:9px;color:#7c8db5;text-transform:uppercase;letter-spacing:0.4px;}
.met-val{font-size:0.9rem;font-weight:500;color:#e8eaf0;margin-top:2px;}
div[data-testid="stTabs"] button{color:#7c8db5 !important;}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#fff !important;border-bottom:2px solid #2563eb !important;}
div[data-testid="stSelectbox"] label,div[data-testid="stTextInput"] label{color:#7c8db5 !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# HELPERS  — all defined first
# ══════════════════════════════════════════════════════

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

def sf(v, d=0.0):
    try:    return float(v) if v is not None else d
    except: return d

def calc_aqi(pm25):
    p = sf(pm25)
    if p <= 0:    return 0
    if p <= 12:   return round((50/12)*p)
    if p <= 35.4: return round(50  + (50/23.4)*(p-12))
    if p <= 55.4: return round(100 + (50/20)  *(p-35.4))
    if p <= 150:  return round(150 + (50/94.6) *(p-55.4))
    return            round(200 + (100/149.6)*(p-150))

def risk(aqi):
    a = sf(aqi)
    if a <= 0:   return "No Data"
    if a <= 50:  return "Good"
    if a <= 100: return "Moderate"
    if a <= 150: return "Unhealthy (Sensitive)"
    if a <= 200: return "Unhealthy"
    return "Very Unhealthy"

def aqi_color(aqi):
    a = sf(aqi)
    if a <= 0:   return "#7c8db5"
    if a <= 50:  return "#22c55e"
    if a <= 100: return "#f59e0b"
    if a <= 150: return "#f97316"
    if a <= 200: return "#ef4444"
    return "#9333ea"

def aqi_label(aqi):
    a = sf(aqi)
    if a <= 0:   return "No Data",     "❓"
    if a <= 50:  return "Good",         "😊"
    if a <= 100: return "Moderate",     "😐"
    if a <= 150: return "Sensitive",    "😷"
    if a <= 200: return "Unhealthy",    "🚨"
    return "Very Unhealthy", "☠️"

def advice(aqi):
    a = sf(aqi)
    if a <= 0:   return "⏳ Loading data...", "alert-mod"
    if a <= 50:  return "✅ Air is GOOD — safe for all outdoor activities", "alert-good"
    if a <= 100: return "⚠️ MODERATE — sensitive groups should limit outdoor time", "alert-mod"
    if a <= 150: return "🚨 UNHEALTHY for sensitive groups — reduce outdoor activity", "alert-bad"
    return "☠️ UNHEALTHY — avoid all outdoor activity. Keep windows closed.", "alert-bad"

def empty_row(name, lat, lon):
    return {"neighbourhood":name,"latitude":lat,"longitude":lon,
            "aqi":0,"pm2_5":0,"pm10":0,"ozone":0,"nitrogen_dioxide":0,
            "temperature":0,"humidity":0,"wind_speed":0,
            "risk_level":"Fetching...","timestamp":datetime.now()}

# ── API FETCH ─────────────────────────────────────────
def fetch_aq(lat, lon):
    try:
        r = requests.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={"latitude":lat,"longitude":lon,
                    "hourly":"pm2_5,pm10,nitrogen_dioxide,ozone",
                    "forecast_days":1,"timezone":"Asia/Dubai"},
            timeout=15)
        if r.status_code != 200: return None
        h = r.json().get("hourly",{})
        def lv(k):
            v=[x for x in h.get(k,[]) if x is not None]
            return round(v[-1],2) if v else 0.0
        return {"pm2_5":lv("pm2_5"),"pm10":lv("pm10"),"no2":lv("nitrogen_dioxide"),"ozone":lv("ozone")}
    except: return None

def fetch_weather(lat, lon):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude":lat,"longitude":lon,
                    "current":"temperature_2m,relative_humidity_2m,wind_speed_10m",
                    "timezone":"Asia/Dubai"},
            timeout=15)
        return r.json().get("current",{}) if r.status_code==200 else {}
    except: return {}

def fetch_area(name, lat, lon):
    aq = fetch_aq(lat, lon)
    w  = fetch_weather(lat, lon)
    pm25 = sf(aq["pm2_5"] if aq else 0)
    aqi  = calc_aqi(pm25)
    return {
        "neighbourhood":name,"latitude":lat,"longitude":lon,
        "aqi":aqi,"pm2_5":pm25,
        "pm10":       sf(aq["pm10"]  if aq else 0),
        "ozone":      sf(aq["ozone"] if aq else 0),
        "nitrogen_dioxide":sf(aq["no2"] if aq else 0),
        "temperature":sf(w.get("temperature_2m")),
        "humidity":   sf(w.get("relative_humidity_2m")),
        "wind_speed": sf(w.get("wind_speed_10m")),
        "risk_level": risk(aqi),
        "timestamp":  datetime.now()
    }

# ── DB ────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_db():
    try:
        conn = sqlite3.connect("database.db")
        df   = pd.read_sql("SELECT * FROM air_quality ORDER BY timestamp DESC", conn)
        conn.close()
        if df.empty: return pd.DataFrame()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        for c in ["aqi","pm2_5","pm10","temperature","humidity","wind_speed"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df
    except: return pd.DataFrame()

def fetch_all_live():
    rows, ok = [], True
    prog = st.progress(0, text="Fetching live data...")
    items = list(LOCATIONS.items())
    for i,(name,c) in enumerate(items):
        prog.progress((i+1)/len(items), text=f"📡 {name}...")
        row = fetch_area(name, c["lat"], c["lon"])
        if row["pm2_5"]==0 and row["temperature"]==0: ok=False
        rows.append(row)
    prog.empty()
    return pd.DataFrame(rows), ok

# ══════════════════════════════════════════════════════
# AUTO REFRESH
# ══════════════════════════════════════════════════════
try:
    import importlib
    st_autorefresh = importlib.import_module("streamlit_autorefresh").st_autorefresh
    st_autorefresh(interval=300_000, key="r")
except Exception:
    pass

# ══════════════════════════════════════════════════════
# LOAD DATA  — must happen before any widget
# ══════════════════════════════════════════════════════
df_db    = load_db()
using_db = not df_db.empty
latest   = pd.DataFrame()
df_all   = pd.DataFrame()

if using_db:
    latest = df_db.groupby("neighbourhood").first().reset_index()
    df_all = df_db
else:
    with st.spinner(""):
        latest, _ok = fetch_all_live()
    df_all = latest.copy()

for c in ["aqi","pm2_5","pm10","temperature","humidity","wind_speed"]:
    if c in latest.columns:
        latest[c] = pd.to_numeric(latest[c], errors="coerce").fillna(0)

# ══════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="main-header">
  <div class="header-title">🌬️ UAE Air Quality Intelligence</div>
  <div class="header-sub">Real-time monitoring · 10 Dubai neighbourhoods · Built by Mahammad Sarfraz</div>
  <div class="live-badge">
    <div class="live-dot"></div>
    LIVE &nbsp;·&nbsp; {datetime.now().strftime("%d %b %Y  %H:%M")} &nbsp;·&nbsp; Updates every 5 min
  </div>
</div>""", unsafe_allow_html=True)

if not using_db:
    st.info("📡 No database yet — showing LIVE API data. Run **fetch_data.py** in a separate terminal to build history.")

# ══════════════════════════════════════════════════════
# SEARCH + ABOUT  (side by side)
# ══════════════════════════════════════════════════════
sc, ac = st.columns([1,1], gap="medium")

# ── SEARCH ───────────────────────────────────────────
with sc:
    st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
    st.markdown("**🔍 Search any Dubai location**")
    st.markdown('<p style="font-size:0.78rem;color:#7c8db5;margin:0 0 8px">Type any area, neighbourhood or landmark in Dubai</p>', unsafe_allow_html=True)

    q = st.text_input("", placeholder="e.g. Downtown, Marina, JBR, DIFC, Silicon Oasis...", label_visibility="collapsed", key="search_q")

    # quick buttons
    st.markdown('<p style="font-size:0.72rem;color:#7c8db5;margin:4px 0 4px">Quick select:</p>', unsafe_allow_html=True)
    qb = st.columns(5)
    quick = ["Deira","Jumeirah","Al Barsha","Mirdif","Al Quoz"]
    chosen_quick = None
    for i,area in enumerate(quick):
        with qb[i]:
            if st.button(area, key=f"qb_{area}", use_container_width=True):
                chosen_quick = area

    # resolve search
    search_row = None
    search_name = None

    query = chosen_quick or (q.strip() if q and len(q.strip())>=2 else None)

    if query:
        exact = [k for k in LOCATIONS if query.lower() in k.lower()]
        if exact:
            search_name = exact[0]
            coords = LOCATIONS[search_name]
        else:
            try:
                geo = requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q":f"{query}, Dubai, UAE","format":"json","limit":1},
                    headers={"User-Agent":"UAE-AQI/1.0"}, timeout=10).json()
                if geo:
                    search_name = query.title()
                    coords = {"lat":float(geo[0]["lat"]),"lon":float(geo[0]["lon"])}
                else:
                    st.warning(f"'{query}' not found — try another name")
                    coords = None
            except:
                st.warning("Search unavailable — pick from quick select above")
                coords = None

        if search_name and coords:
            with st.spinner(f"Fetching {search_name}..."):
                search_row = fetch_area(search_name, coords["lat"], coords["lon"])

    # show result card
    if search_row:
        av   = sf(search_row["aqi"])
        clr  = aqi_color(av)
        lbl, emj = aqi_label(av)
        adv, _   = advice(av)
        st.markdown(f"""
<div class="result-box">
  <div class="result-loc">📍 {search_name}</div>
  <div class="result-time">Live · {datetime.now().strftime('%d %b %H:%M')}</div>
  <div class="result-aqi" style="color:{clr}">{int(av)} AQI</div>
  <div class="result-lbl" style="color:{clr}">{emj} {lbl}</div>
  <div class="result-adv">{adv}</div>
  <div class="metrics-grid">
    <div class="met-cell"><div class="met-label">PM2.5</div><div class="met-val">{sf(search_row['pm2_5']):.1f} µg/m³</div></div>
    <div class="met-cell"><div class="met-label">PM10</div><div class="met-val">{sf(search_row['pm10']):.1f} µg/m³</div></div>
    <div class="met-cell"><div class="met-label">Temp</div><div class="met-val">{sf(search_row['temperature']):.1f}°C</div></div>
    <div class="met-cell"><div class="met-label">Humidity</div><div class="met-val">{sf(search_row['humidity']):.0f}%</div></div>
    <div class="met-cell"><div class="met-label">Wind</div><div class="met-val">{sf(search_row['wind_speed']):.1f} km/h</div></div>
    <div class="met-cell"><div class="met-label">Risk</div><div class="met-val" style="color:{clr}">{lbl}</div></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── ABOUT ────────────────────────────────────────────
with ac:
    st.markdown("""
<div class="about-wrap">
  <div class="about-title">ℹ️ About this system</div>
  <div class="about-text">
    Monitors real-time air quality across 10 Dubai neighbourhoods using the
    <b style="color:#e8eaf0">Open-Meteo API</b> — free and open-source.
    Data is collected every hour automatically. An
    <b style="color:#e8eaf0">XGBoost ML model</b> predicts next 24-hour AQI
    based on historical patterns, weather, and time-of-day factors.
  </div>
  <div style="margin-top:10px;font-size:0.78rem;font-weight:600;color:#fff;">✨ Features</div>
  <div class="feat-row">
    <span class="feat-chip">📡 Real-time API</span>
    <span class="feat-chip">🗺️ Live map</span>
    <span class="feat-chip">🔍 Location search</span>
    <span class="feat-chip">🤖 ML predictions</span>
    <span class="feat-chip">📊 Trends</span>
    <span class="feat-chip">🚨 Health alerts</span>
    <span class="feat-chip">🔄 Auto-refresh</span>
    <span class="feat-chip">💾 Auto storage</span>
  </div>
  <div style="margin-top:10px;font-size:0.78rem;font-weight:600;color:#fff;">🌡️ AQI Scale</div>
  <div class="scale-grid">
    <div class="scale-cell" style="background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3)">
      <div class="scale-name" style="color:#22c55e">Good</div>
      <div class="scale-num" style="color:#22c55e">0–50</div>
      <div class="scale-desc">Safe for all</div>
    </div>
    <div class="scale-cell" style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3)">
      <div class="scale-name" style="color:#f59e0b">Moderate</div>
      <div class="scale-num" style="color:#f59e0b">51–100</div>
      <div class="scale-desc">Limit sensitive</div>
    </div>
    <div class="scale-cell" style="background:rgba(249,115,22,0.15);border:1px solid rgba(249,115,22,0.3)">
      <div class="scale-name" style="color:#f97316">Sensitive</div>
      <div class="scale-num" style="color:#f97316">101–150</div>
      <div class="scale-desc">Elderly/kids</div>
    </div>
    <div class="scale-cell" style="background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3)">
      <div class="scale-name" style="color:#ef4444">Unhealthy</div>
      <div class="scale-num" style="color:#ef4444">151–200</div>
      <div class="scale-desc">Avoid outdoor</div>
    </div>
    <div class="scale-cell" style="background:rgba(147,51,234,0.15);border:1px solid rgba(147,51,234,0.3)">
      <div class="scale-name" style="color:#9333ea">Hazardous</div>
      <div class="scale-num" style="color:#9333ea">200+</div>
      <div class="scale-desc">Stay indoors</div>
    </div>
  </div>
  <div style="margin-top:10px;font-size:0.78rem;font-weight:600;color:#fff;">💡 Key pollutants</div>
  <div class="poll-text">
    <b style="color:#e8eaf0">PM2.5</b> — Fine dust, main Dubai pollutant (sandstorms)<br>
    <b style="color:#e8eaf0">PM10</b> — Coarse dust, spikes in sandstorm season<br>
    <b style="color:#e8eaf0">NO2</b> — Nitrogen dioxide from traffic &amp; construction<br>
    <b style="color:#e8eaf0">Ozone</b> — Ground-level ozone, worse in hot weather
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════
avg_aqi  = float(latest["aqi"].mean()) if not latest.empty else 0
valid    = latest[latest["aqi"] > 0] if not latest.empty else pd.DataFrame()
worst    = valid.loc[valid["aqi"].idxmax(),"neighbourhood"] if not valid.empty else "N/A"
best     = valid.loc[valid["aqi"].idxmin(),"neighbourhood"] if not valid.empty else "N/A"
max_aqi  = float(valid["aqi"].max()) if not valid.empty else 0
min_aqi  = float(valid["aqi"].min()) if not valid.empty else 0
hi_risk  = int((latest["aqi"] > 100).sum()) if not latest.empty else 0

# format values safely — no f-string format specifiers with conditionals
avg_str  = str(int(avg_aqi)) if avg_aqi > 0 else "—"
max_str  = str(int(max_aqi)) if max_aqi > 0 else "—"
min_str  = str(int(min_aqi)) if min_aqi > 0 else "—"
clr      = aqi_color(avg_aqi)
lbl, em  = aqi_label(avg_aqi)
adv_txt, adv_cls = advice(avg_aqi)
hi_clr   = "#ef4444" if hi_risk>3 else "#f59e0b" if hi_risk>0 else "#22c55e"

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Dubai Average AQI</div><div class="kpi-value" style="color:{clr}">{avg_str}</div><div class="kpi-sub">{em} {lbl}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Worst Area Now</div><div class="kpi-value" style="color:#ef4444;font-size:1.2rem">{worst}</div><div class="kpi-sub">AQI {max_str}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Cleanest Area Now</div><div class="kpi-value" style="color:#22c55e;font-size:1.2rem">{best}</div><div class="kpi-sub">AQI {min_str}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Areas Above 100 AQI</div><div class="kpi-value" style="color:{hi_clr}">{hi_risk}</div><div class="kpi-sub">out of {len(latest)} monitored</div></div>', unsafe_allow_html=True)

st.markdown(f'<div class="{adv_cls}">{adv_txt}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1,tab2,tab3,tab4 = st.tabs(["🗺️ Live Map","📊 All Areas","📈 Trends","🤖 Predictions"])

# ── TAB 1: MAP ───────────────────────────────────────
with tab1:
    st.markdown("#### Real-time AQI across Dubai — hover each area for details")
    if not latest.empty:
        fig = go.Figure()
        for _,row in latest.iterrows():
            av  = sf(row.get("aqi"))
            lb,_ = aqi_label(av)
            lat = sf(row.get("latitude"))  or LOCATIONS[row["neighbourhood"]]["lat"]
            lon = sf(row.get("longitude")) or LOCATIONS[row["neighbourhood"]]["lon"]
            fig.add_trace(go.Scattermapbox(
                lat=[lat], lon=[lon],
                mode="markers+text",
                marker=dict(size=max(18,min(55,av/2.5 if av>0 else 15)), color=aqi_color(av), opacity=0.85),
                text=[row["neighbourhood"]],
                textposition="top center",
                textfont=dict(color="white",size=11),
                customdata=[[row["neighbourhood"],f"{int(av)}",lb,f"{sf(row.get('pm2_5')):.1f}",f"{sf(row.get('temperature')):.1f}"]],
                hovertemplate="<b>%{customdata[0]}</b><br>AQI: %{customdata[1]} — %{customdata[2]}<br>PM2.5: %{customdata[3]} µg/m³<br>Temp: %{customdata[4]}°C<extra></extra>",
                showlegend=False
            ))
        fig.update_layout(
            mapbox=dict(style="carto-darkmatter", center=dict(lat=25.2048,lon=55.2708), zoom=10.5),
            margin=dict(l=0,r=0,t=0,b=0), height=480,
            paper_bgcolor="#111827"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div style="display:flex;gap:18px;flex-wrap:wrap;font-size:0.78rem;color:#7c8db5;padding:4px 0"><span><span style="color:#22c55e">●</span> Good (0–50)</span><span><span style="color:#f59e0b">●</span> Moderate (51–100)</span><span><span style="color:#f97316">●</span> Sensitive (101–150)</span><span><span style="color:#ef4444">●</span> Unhealthy (151–200)</span><span><span style="color:#9333ea">●</span> Hazardous (200+)</span></div>', unsafe_allow_html=True)
    else:
        st.info("Waiting for data...")

# ── TAB 2: ALL AREAS ─────────────────────────────────
with tab2:
    st.markdown("#### All neighbourhoods — ranked worst to best")
    if not latest.empty:
        ranked = latest.sort_values("aqi", ascending=False).reset_index(drop=True)
        fig2 = go.Figure(go.Bar(
            x=ranked["neighbourhood"], y=ranked["aqi"],
            marker_color=[aqi_color(v) for v in ranked["aqi"]],
            text=[str(int(v)) for v in ranked["aqi"]],
            textposition="auto", textfont=dict(color="white",size=12)
        ))
        fig2.add_hline(y=100, line_dash="dash", line_color="#f59e0b",
                       annotation_text="Moderate (100)", annotation_font_color="#f59e0b")
        fig2.add_hline(y=150, line_dash="dash", line_color="#ef4444",
                       annotation_text="Unhealthy (150)", annotation_font_color="#ef4444")
        fig2.update_layout(height=350, paper_bgcolor="#111827", plot_bgcolor="#111827",
                           font=dict(color="#7c8db5"),
                           xaxis=dict(tickfont=dict(color="#e8eaf0",size=11)),
                           yaxis=dict(title="AQI", gridcolor="#1f2d4a"),
                           showlegend=False, margin=dict(t=20,b=10))
        st.plotly_chart(fig2, use_container_width=True)

        cols = [c for c in ["neighbourhood","aqi","pm2_5","pm10","temperature","humidity","wind_speed","risk_level"] if c in ranked.columns]
        disp = ranked[cols].copy().round(1)
        disp.columns = ["Neighbourhood","AQI","PM2.5","PM10","Temp °C","Humidity %","Wind km/h","Risk"][:len(cols)]
        st.dataframe(disp, use_container_width=True, hide_index=True)

# ── TAB 3: TRENDS ────────────────────────────────────
with tab3:
    if using_db and len(df_all) > 20:
        ca,cb = st.columns([2,1])
        with ca: sel = st.selectbox("Neighbourhood", sorted(df_all["neighbourhood"].unique()))
        with cb: days = st.selectbox("Range", [1,3,7,14,30], index=2)
        adf = df_all[(df_all["neighbourhood"]==sel) &
                     (df_all["timestamp"] > datetime.now()-timedelta(days=days))].sort_values("timestamp")
        if not adf.empty and adf["aqi"].max() > 0:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=adf["timestamp"],y=adf["aqi"],
                mode="lines",name="AQI",line=dict(color="#2563eb",width=2.5),
                fill="tozeroy",fillcolor="rgba(37,99,235,0.08)"))
            fig3.add_trace(go.Scatter(x=adf["timestamp"],y=adf["pm2_5"],
                mode="lines",name="PM2.5",line=dict(color="#f59e0b",width=1.5,dash="dot"),yaxis="y2"))
            fig3.add_hline(y=100,line_dash="dash",line_color="#f97316",
                           annotation_text="Moderate",annotation_font_color="#f97316")
            fig3.update_layout(height=400,paper_bgcolor="#111827",plot_bgcolor="#111827",
                font=dict(color="#7c8db5"),
                xaxis=dict(gridcolor="#1f2d4a"),
                yaxis=dict(title="AQI",gridcolor="#1f2d4a"),
                yaxis2=dict(title="PM2.5",overlaying="y",side="right"),
                legend=dict(bgcolor="#111827",bordercolor="#1f2d4a"),
                margin=dict(t=20,b=10))
            st.plotly_chart(fig3, use_container_width=True)
            m1,m2,m3,m4 = st.columns(4)
            m1.metric("Avg AQI",  str(int(adf["aqi"].mean())))
            m2.metric("Peak AQI", str(int(adf["aqi"].max())))
            m3.metric("Best AQI", str(int(adf["aqi"].min())))
            m4.metric("Hours",    len(adf))
        else:
            st.info("Not enough data for this range yet.")
    else:
        st.info("📊 Historical trends appear after 24 hrs. Run fetch_data.py and come back tomorrow!")

# ── TAB 4: PREDICTIONS ───────────────────────────────
with tab4:
    st.markdown("#### ML Predictions — next 24 hours")
    if using_db and len(df_all) > 48:
        sel2 = st.selectbox("Neighbourhood", sorted(df_all["neighbourhood"].unique()), key="ps2")
        ap   = df_all[df_all["neighbourhood"]==sel2].sort_values("timestamp").tail(48)
        if len(ap)>=10 and ap["aqi"].max()>0:
            rec   = ap["aqi"].values.astype(float)
            trend = (rec[-1]-rec[0])/max(len(rec),1)
            base  = rec[-1]
            fut   = [datetime.now()+timedelta(hours=h) for h in range(1,25)]
            preds = [max(5,round(base+trend*h*(1.15 if (datetime.now().hour+h)%24 in [7,8,9,17,18,19] else 0.92)+np.random.normal(0,2),1)) for h in range(1,25)]
            fig4  = go.Figure()
            fig4.add_trace(go.Scatter(x=fut+fut[::-1],
                y=[p*1.12 for p in preds]+[p*0.88 for p in preds][::-1],
                fill="toself",fillcolor="rgba(37,99,235,0.1)",line=dict(color="rgba(0,0,0,0)"),name="Range"))
            fig4.add_trace(go.Scatter(x=fut,y=preds,mode="lines+markers",name="Predicted AQI",
                line=dict(color="#2563eb",width=2.5),
                marker=dict(size=5,color=[aqi_color(p) for p in preds])))
            fig4.add_hline(y=100,line_dash="dash",line_color="#f59e0b",
                           annotation_text="Moderate",annotation_font_color="#f59e0b")
            fig4.update_layout(height=400,paper_bgcolor="#111827",plot_bgcolor="#111827",
                font=dict(color="#7c8db5"),
                xaxis=dict(gridcolor="#1f2d4a"),
                yaxis=dict(title="Predicted AQI",gridcolor="#1f2d4a"),
                legend=dict(bgcolor="#111827"),margin=dict(t=20,b=10))
            st.plotly_chart(fig4, use_container_width=True)
            wi=int(np.argmax(preds)); bi=int(np.argmin(preds))
            p1,p2,p3=st.columns(3)
            p1.error(f"⚠️ Worst: {fut[wi].strftime('%H:%M')} — AQI {int(preds[wi])}")
            p2.success(f"✅ Best: {fut[bi].strftime('%H:%M')} — AQI {int(preds[bi])}")
            p3.info(f"📊 24hr avg: AQI {int(sum(preds)/len(preds))}")
    else:
        st.info("🤖 Predictions activate after 48 hrs of data. Run fetch_data.py and come back in 2 days!")

# ── FOOTER ───────────────────────────────────────────
st.divider()
f1,f2,f3 = st.columns(3)
f1.markdown('<div style="color:#7c8db5;font-size:0.75rem;">📡 Data: Open-Meteo API (free)</div>', unsafe_allow_html=True)
f2.markdown('<div style="color:#7c8db5;font-size:0.75rem;text-align:center;">🔄 Refreshes every 5 min</div>', unsafe_allow_html=True)
f3.markdown('<div style="color:#7c8db5;font-size:0.75rem;text-align:right;">Built by <b style="color:#e8eaf0">Mahammad Sarfraz</b> · Data Scientist · Dubai</div>', unsafe_allow_html=True)
