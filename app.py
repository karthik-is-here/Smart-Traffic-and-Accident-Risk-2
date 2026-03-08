import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import config
import predictor
import maps

st.set_page_config(
    page_title="Kochi Traffic — ML Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&family=Inter:wght@300;400;500;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* ── Off-white base ── */
.stApp { background: #F2F4F8 !important; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a2235 !important;
    border-right: 1px solid #263248 !important;
    min-width: 230px !important;
    max-width: 230px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

/* ── Sidebar section labels ── */
.sb-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    letter-spacing: 2.5px;
    color: #4a7a9b;
    text-transform: uppercase;
    margin: 0 0 7px 0;
    padding-bottom: 5px;
    border-bottom: 1px solid #263248;
}
.sb-section {
    padding: 12px 14px;
    border-bottom: 1px solid #1e2d42;
}

/* ── Day/Weather/Area toggle buttons ── */
.stButton > button {
    background: #0f1e30 !important;
    color: #6a8faa !important;
    border: 1px solid #1e3448 !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 6px 4px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #162840 !important;
    color: #c8dce8 !important;
    border-color: #2a5a7a !important;
}

/* Active state via special label prefix trick */
button[kind="secondary"] { /* fallback */ }

/* Predict button special style */
div[data-testid="stSidebar"] .stButton:last-of-type > button {
    background: linear-gradient(135deg, #004f72, #006a8a) !important;
    color: #00d4ff !important;
    border: 1px solid #00d4ff55 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    box-shadow: 0 0 14px #00d4ff18 !important;
    padding: 10px !important;
}
div[data-testid="stSidebar"] .stButton:last-of-type > button:hover {
    box-shadow: 0 0 22px #00d4ff33 !important;
    border-color: #00d4ff99 !important;
}

/* Slider dark styling */
[data-testid="stSidebar"] [data-testid="stSlider"] {
    padding: 0 4px;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background: #00d4ff !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #00d4ff !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 0 8px #00d4ff66 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #8aaec4 !important;
    font-size: 12px !important;
}

/* ── Topbar ── */
.topbar {
    background: #1a2235;
    padding: 11px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #263248;
    margin-bottom: 0;
}
.topbar-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    letter-spacing: 2.5px;
    color: #00d4ff;
    text-transform: uppercase;
    margin-bottom: 1px;
}
.topbar-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.topbar-title span { color: #00d4ff; }
.topbar-right {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #00ff88;
    letter-spacing: 1px;
}
.status-dot {
    width: 7px; height: 7px;
    background: #00ff88;
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes blink {
    0%,100% { opacity:1; box-shadow:0 0 5px #00ff88; }
    50%      { opacity:0.4; box-shadow:0 0 10px #00ff88; }
}

/* ── Main content area ── */
.main-wrap {
    padding: 14px 16px 0 16px;
}

/* ── Tab buttons in center ── */
.tab-row { display: flex; gap: 6px; margin-bottom: 10px; }
.tab-btn {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: #e6e9f0;
    color: #5a7a95;
    border: 1px solid #d0d8e8;
    border-radius: 6px;
    padding: 7px 16px;
    cursor: pointer;
    transition: all 0.15s;
}
.tab-btn.active {
    background: #1a2235;
    color: #00d4ff;
    border-color: #1a2235;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}

/* ── Map frame ── */
.map-frame {
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #d0d8e8;
    box-shadow: 0 4px 20px rgba(0,0,0,0.10);
    background: #e0e4ec;
}
.map-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1a2235;
    padding: 8px 14px;
    border-radius: 10px 10px 0 0;
}
.map-meta-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: #4a7a9b;
    text-transform: uppercase;
}
.map-meta-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #00d4ff;
}

/* ── Right stats panel ── */
.stats-wrap {
    background: #1a2235;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #263248;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}
.stats-section-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: #4a7a9b;
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #263248;
}
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
.stat-card {
    background: #111928;
    border: 1px solid #1e3248;
    border-radius: 8px;
    padding: 10px 12px;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.stat-card.cyan::after   { background: #00d4ff; }
.stat-card.green::after  { background: #00ff88; }
.stat-card.amber::after  { background: #ffaa00; }
.stat-card.red::after    { background: #ff4444; }
.stat-label { font-family:'Share Tech Mono',monospace; font-size:8px; letter-spacing:1.5px; color:#4a6a85; text-transform:uppercase; margin-bottom:4px; }
.stat-value { font-family:'Rajdhani',sans-serif; font-size:26px; font-weight:700; line-height:1; }
.stat-value.cyan  { color: #00d4ff; }
.stat-value.green { color: #00ff88; }
.stat-value.amber { color: #ffaa00; }
.stat-value.red   { color: #ff4444; }
.stat-unit { font-size:9px; color:#4a6a85; margin-top:2px; font-family:'Share Tech Mono',monospace; }

.meter-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px; }
.meter-box { background:#111928; border:1px solid #1e3248; border-radius:8px; padding:10px; }
.meter-title { font-family:'Share Tech Mono',monospace; font-size:8px; letter-spacing:1.5px; color:#4a6a85; text-transform:uppercase; margin-bottom:5px; }
.meter-val { font-family:'Rajdhani',sans-serif; font-size:20px; font-weight:700; }
.meter-bar-bg { background:#1e3248; border-radius:3px; height:3px; margin-top:5px; }
.meter-bar    { height:3px; border-radius:3px; }

.alert-box {
    background: #1a0c0c;
    border: 1px solid #ff444455;
    border-left: 3px solid #ff4444;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 10px;
}
.alert-title { font-family:'Share Tech Mono',monospace; font-size:9px; letter-spacing:1.5px; color:#ff4444; text-transform:uppercase; margin-bottom:6px; }
.alert-road  { font-size:11px; color:#ff8888; padding:2px 0; display:flex; align-items:center; gap:5px; border-bottom:1px solid #2a1010; }
.alert-road:last-child { border-bottom:none; }

.info-box { background:#111928; border:1px solid #1e3248; border-radius:8px; padding:10px 12px; }
.info-row { display:flex; justify-content:space-between; font-size:11px; padding:3px 0; border-bottom:1px solid #0f1820; }
.info-row:last-child { border-bottom:none; }
.info-key { color:#4a7a9b; }
.info-val { color:#c8dce8; font-weight:500; }
.info-val.cyan { color:#00d4ff; font-family:'Share Tech Mono',monospace; }

/* Road table */
.road-tbl { width:100%; border-collapse:collapse; font-size:11px; }
.road-tbl th { font-family:'Share Tech Mono',monospace; font-size:8px; letter-spacing:1.5px; color:#4a6a85; text-transform:uppercase; padding:5px 5px; border-bottom:1px solid #263248; text-align:left; }
.road-tbl td { color:#8aaab5; padding:5px 5px; border-bottom:1px solid #1a2a3a; }
.road-tbl tr:hover td { background:#0f1820; color:#c8dce8; }
.badge { display:inline-block; border-radius:4px; padding:1px 6px; font-size:9px; font-weight:600; font-family:'Share Tech Mono',monospace; }
.badge-low      { background:#012a14; color:#00ff88; border:1px solid #00ff8833; }
.badge-moderate { background:#2a1a00; color:#ffaa00; border:1px solid #ffaa0033; }
.badge-high     { background:#2a0808; color:#ff6666; border:1px solid #ff444433; }
.badge-veryhigh { background:#350505; color:#ff3333; border:1px solid #ff3333; }

/* Empty state */
.empty-map {
    height: 430px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #e6e9f0;
    border-radius: 0 0 10px 10px;
    color: #a0b0c0;
    gap: 10px;
}

/* Selected indicator labels */
.sel-indicator {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    color: #00d4ff;
    text-align: center;
    padding: 4px 0 8px 0;
    text-transform: uppercase;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Session defaults ───────────────────────────────────────────────────────────
for k, v in [("sel_day","Monday"), ("sel_weather","Clear"),
              ("sel_area","Fort Kochi"), ("sel_hour", 8),
              ("active_tab","congestion"), ("results", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Topbar (outside columns, full width) ──────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-eyebrow">Kochi Urban Intelligence &nbsp;▸&nbsp; Real ML Model</div>
        <div class="topbar-title">SMART <span>TRAFFIC</span> &amp; ACCIDENT RISK</div>
    </div>
    <div class="topbar-right">
        <div class="status-dot"></div>
        ML MODELS ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — all controls live here so Streamlit renders them correctly
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Day of week
    st.markdown('<div class="sb-section"><div class="sb-label">📅 Day of Week</div>', unsafe_allow_html=True)
    days_short = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    days_full  = config.DAYS_OF_WEEK
    cols_d = st.columns(3)
    for i, (short, full) in enumerate(zip(days_short, days_full)):
        label = f"✦ {short}" if st.session_state.sel_day == full else short
        with cols_d[i % 3]:
            if st.button(label, key=f"day_{full}", use_container_width=True):
                st.session_state.sel_day = full
                st.rerun()
    st.markdown(f'<div class="sel-indicator">▸ {st.session_state.sel_day.upper()}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Hour slider
    st.markdown('<div class="sb-section"><div class="sb-label">🕐 Hour of Day</div>', unsafe_allow_html=True)
    hour = st.slider("Hour", 0, 23, value=8, key="hour_slider",
                     format="%d:00", label_visibility="collapsed")
    period = "🌙 Night" if hour >= 22 or hour <= 5 else "🔆 Rush Hour" if (7 <= hour <= 9 or 17 <= hour <= 20) else "🕑 Off-Peak"
    st.markdown(f'<div class="sel-indicator">{hour:02d}:00 &nbsp;·&nbsp; {period}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Weather
    st.markdown('<div class="sb-section"><div class="sb-label">🌤️ Weather</div>', unsafe_allow_html=True)
    weather_icons = {"Clear":"☀️","Cloudy":"☁️","Light Rain":"🌦️","Heavy Rain":"🌧️","Fog":"🌫️"}
    wx_opts = config.WEATHER_OPTIONS
    cols_w = st.columns(2)
    for i, w in enumerate(wx_opts):
        label = f"✦ {weather_icons[w]} {w}" if st.session_state.sel_weather == w else f"{weather_icons[w]} {w}"
        with cols_w[i % 2]:
            if st.button(label, key=f"wx_{w}", use_container_width=True):
                st.session_state.sel_weather = w
                st.rerun()
    st.markdown(f'<div class="sel-indicator">▸ {st.session_state.sel_weather.upper()}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Area — 2-col grid
    st.markdown('<div class="sb-section"><div class="sb-label">📍 Location</div>', unsafe_allow_html=True)
    areas_list = list(config.AREA_ROADS.keys())
    cols_a = st.columns(2)
    for i, area_opt in enumerate(areas_list):
        lbl = f"✦ {area_opt}" if st.session_state.sel_area == area_opt else area_opt
        with cols_a[i % 2]:
            if st.button(lbl, key=f"area_{area_opt}", use_container_width=True):
                st.session_state.sel_area = area_opt
                st.rerun()
    st.markdown(f'<div class="sel-indicator">▸ {st.session_state.sel_area.upper()}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:12px 14px;">', unsafe_allow_html=True)
    predict_clicked = st.button("⚡  RUN PREDICTION", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Trigger prediction ─────────────────────────────────────────────────────────
if predict_clicked:
    with st.spinner("Analysing roads..."):
        try:
            results = predictor.predict_all_roads(
                st.session_state.sel_area,
                st.session_state.sel_day,
                st.session_state.get("hour_slider", 8),
                st.session_state.sel_weather
            )
            st.session_state.results = results
        except FileNotFoundError:
            st.error("❌ models/ folder not found next to app.py")
            st.stop()
        except Exception as e:
            st.error(f"❌ {e}")
            st.stop()
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AREA — map + stats side by side
# ═══════════════════════════════════════════════════════════════════════════════
results = st.session_state.results
area    = st.session_state.sel_area

center_col, right_col = st.columns([3.2, 1.4], gap="medium")

# ── Center: Map ───────────────────────────────────────────────────────────────
with center_col:
    st.markdown('<div style="padding: 10px 4px 0 4px;">', unsafe_allow_html=True)

    # Tab toggle
    tc, tr, _ = st.columns([1, 1, 3])
    with tc:
        if st.button("🗺️ Congestion", key="tab_cong", use_container_width=True):
            st.session_state.active_tab = "congestion"
            st.rerun()
    with tr:
        if st.button("⚠️ Risk", key="tab_risk", use_container_width=True):
            st.session_state.active_tab = "risk"
            st.rerun()

    tab_label = "CONGESTION MAP" if st.session_state.active_tab == "congestion" else "ACCIDENT RISK MAP"
    st.markdown(f"""
    <div class="map-meta" style="margin-top:8px;">
        <span class="map-meta-label">Zone Map — Kochi District</span>
        <span class="map-meta-value">📍 {area}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="border:2px solid #d0d8e8;border-top:none;border-radius:0 0 12px 12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.10);">', unsafe_allow_html=True)
    if results:
        m = maps.create_congestion_map(results, area) if st.session_state.active_tab == "congestion" else maps.create_risk_map(results, area)
        components.html(maps.map_to_html(m), height=440)
    else:
        st.markdown("""
        <div class="empty-map">
            <div style="font-size:44px;">🗺️</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#8aaac0;">
                SELECT PARAMETERS &amp; RUN PREDICTION
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Road table
    if results:
        df_key    = "congestion_level"   if st.session_state.active_tab == "congestion" else "accident_risk_level"
        score_key = "congestion_score"   if st.session_state.active_tab == "congestion" else "accident_risk_score"

        def badge(level):
            slug = level.lower().replace(" ", "")
            return f'<span class="badge badge-{slug}">{level}</span>'

        rows = "".join(
            f'<tr><td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{r["road_name"]}</td>'
            f'<td>{badge(r[df_key])}</td>'
            f'<td style="font-family:\'Share Tech Mono\',monospace;color:#00d4ff">{r[score_key]}%</td>'
            f'<td style="color:#5a7a95">{r["peak_time"]}</td></tr>'
            for r in sorted(results, key=lambda x: x[score_key], reverse=True)
        )
        label = "Congestion" if st.session_state.active_tab == "congestion" else "Accident Risk"
        st.markdown(f"""
        <div style="margin-top:10px;background:#1a2235;border:1px solid #263248;border-radius:10px;
                    padding:10px 14px;max-height:170px;overflow-y:auto;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;
                        color:#00d4ff;margin-bottom:8px;text-transform:uppercase;">{label} — {area}</div>
            <table class="road-tbl">
                <thead><tr><th>Road</th><th>Level</th><th>Score</th><th>Peak</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Right: Stats ───────────────────────────────────────────────────────────────
with right_col:
    st.markdown('<div style="padding: 10px 4px 0 0;">', unsafe_allow_html=True)
    st.markdown('<div class="stats-wrap">', unsafe_allow_html=True)

    if results:
        high_cong  = [r for r in results if r["congestion_level"] in ["High","Very High"]]
        high_risk  = [r for r in results if r["accident_risk_level"] in ["High","Very High"]]
        avg_cong   = round(sum(r["congestion_score"]   for r in results) / len(results), 1)
        avg_risk   = round(sum(r["accident_risk_score"] for r in results) / len(results), 1)
        cong_col   = "red" if len(high_cong) >= 3 else "amber" if len(high_cong) >= 1 else "green"
        risk_col   = "red" if len(high_risk) >= 3 else "amber" if len(high_risk) >= 1 else "green"
        risk_color = "#ff4444" if avg_risk > 50 else "#ffaa00" if avg_risk > 30 else "#00ff88"

        st.markdown(f"""
        <div class="stats-section-label">📊 Summary</div>
        <div class="stat-grid">
            <div class="stat-card {cong_col}">
                <div class="stat-label">High Cong.</div>
                <div class="stat-value {cong_col}">{len(high_cong)}</div>
                <div class="stat-unit">roads</div>
            </div>
            <div class="stat-card amber">
                <div class="stat-label">Avg Cong.</div>
                <div class="stat-value amber">{avg_cong}%</div>
                <div class="stat-unit">score</div>
            </div>
            <div class="stat-card cyan">
                <div class="stat-label">Checked</div>
                <div class="stat-value cyan">{len(results)}</div>
                <div class="stat-unit">roads</div>
            </div>
            <div class="stat-card {risk_col}">
                <div class="stat-label">High Risk</div>
                <div class="stat-value {risk_col}">{len(high_risk)}</div>
                <div class="stat-unit">roads</div>
            </div>
        </div>

        <div class="meter-row">
            <div class="meter-box">
                <div class="meter-title">Congestion</div>
                <div class="meter-val" style="color:#00d4ff">{avg_cong}%</div>
                <div class="meter-bar-bg"><div class="meter-bar" style="width:{min(avg_cong,100)}%;background:#00d4ff;"></div></div>
                <div style="font-size:9px;color:#4a6a85;margin-top:3px;">avg</div>
            </div>
            <div class="meter-box">
                <div class="meter-title">Risk</div>
                <div class="meter-val" style="color:{risk_color}">{avg_risk}%</div>
                <div class="meter-bar-bg"><div class="meter-bar" style="width:{min(avg_risk,100)}%;background:{risk_color};"></div></div>
                <div style="font-size:9px;color:#4a6a85;margin-top:3px;">avg</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Danger alert
        all_danger = list({r["road_name"] for r in high_cong + high_risk})
        if all_danger:
            road_rows = "".join(f'<div class="alert-road"><span>▸</span>{r}</div>' for r in all_danger)
            st.markdown(f"""
            <div class="alert-box">
                <div class="alert-title">⚠ Dangerous Roads</div>
                {road_rows}
            </div>
            """, unsafe_allow_html=True)

        # Session info
        st.markdown(f"""
        <div class="stats-section-label" style="margin-top:6px;">🔖 Session</div>
        <div class="info-box">
            <div class="info-row"><span class="info-key">Area</span><span class="info-val">{st.session_state.sel_area}</span></div>
            <div class="info-row"><span class="info-key">Day</span><span class="info-val">{st.session_state.sel_day}</span></div>
            <div class="info-row"><span class="info-key">Time</span><span class="info-val cyan">{st.session_state.get('hour_slider', 8):02d}:00</span></div>
            <div class="info-row"><span class="info-key">Weather</span><span class="info-val">{st.session_state.sel_weather}</span></div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="height:340px;display:flex;align-items:center;justify-content:center;
                    flex-direction:column;gap:12px;">
            <div style="font-size:38px;opacity:0.4;">📊</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;
                        color:#4a7a9b;text-align:center;line-height:2;">
                RUN A PREDICTION<br>TO SEE STATS
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
