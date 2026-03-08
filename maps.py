import folium
import config


def _add_legend(m, colors, title):
    items_html = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;margin:5px 0;">'
        f'<div style="width:13px;height:13px;border-radius:50%;background:{color};flex-shrink:0;"></div>'
        f'<span style="font-size:13px;color:#2d3561;">{label}</span></div>'
        for label, color in colors.items()
    )
    legend_html = (
        '<div style="position:absolute;bottom:30px;right:10px;z-index:9999;'
        'background:white;padding:14px 18px;border-radius:10px;'
        'box-shadow:0 2px 12px rgba(0,0,0,0.2);font-family:Arial;'
        'border:1px solid #e2e6f0;min-width:155px;pointer-events:none;">'
        f'<b style="font-size:13px;color:#1a1f36;display:block;margin-bottom:10px;">{title}</b>'
        f'{items_html}'
        '</div>'
    )
    m.get_root().html.add_child(folium.Element(legend_html))


def _center(predictions):
    lats = [r["lat"] for r in predictions]
    lons = [r["lon"] for r in predictions]
    return (sum(lats) / len(lats), sum(lons) / len(lons))


def create_congestion_map(predictions, area):
    center = _center(predictions)
    m = folium.Map(location=center, zoom_start=14, tiles="CartoDB positron")

    for r in predictions:
        color = config.CONGESTION_COLORS.get(r["congestion_level"], "gray")
        popup_html = (
            f'<div style="font-family:Arial;min-width:200px">'
            f'<b style="font-size:14px">{r["road_name"]}</b><br>'
            f'<hr style="margin:4px 0">'
            f'Congestion: <b>{r["congestion_level"]}</b><br>'
            f'Score: <b>{r["congestion_score"]}%</b><br>'
            f'Type: {r["road_type"]}<br>'
            f'Speed limit: {r["speed_limit_kmph"]} km/h<br>'
            f'Peak time: {r["peak_time"]}<br>'
            f'Weather: {r["weather_condition"]}'
            f'</div>'
        )
        folium.CircleMarker(
            location=[r["lat"], r["lon"]],
            radius=13,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f'{r["road_name"]} — {r["congestion_level"]}'
        ).add_to(m)

    _add_legend(m, config.CONGESTION_COLORS, "Congestion Level")
    return m


def create_risk_map(predictions, area):
    center = _center(predictions)
    m = folium.Map(location=center, zoom_start=14, tiles="CartoDB positron")

    for r in predictions:
        color = config.RISK_COLORS.get(r["accident_risk_level"], "gray")
        popup_html = (
            f'<div style="font-family:Arial;min-width:200px">'
            f'<b style="font-size:14px">{r["road_name"]}</b><br>'
            f'<hr style="margin:4px 0">'
            f'Risk Level: <b>{r["accident_risk_level"]}</b><br>'
            f'Score: <b>{r["accident_risk_score"]}%</b><br>'
            f'Type: {r["road_type"]}<br>'
            f'Speed limit: {r["speed_limit_kmph"]} km/h<br>'
            f'Peak time: {r["peak_time"]}<br>'
            f'Weather: {r["weather_condition"]}'
            f'</div>'
        )
        folium.CircleMarker(
            location=[r["lat"], r["lon"]],
            radius=13,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f'{r["road_name"]} — {r["accident_risk_level"]}'
        ).add_to(m)

    _add_legend(m, config.RISK_COLORS, "Accident Risk Level")
    return m


def map_to_html(folium_map):
    return folium_map._repr_html_()


# Area centres for the picker map
AREA_CENTRES = {
    "Edappally":    (10.0262, 76.3090),
    "Kakkanad":     (10.0215, 76.3435),
    "Fort Kochi":   (9.9658,  76.2448),
    "Mattancherry": (9.9578,  76.2595),
    "Vyttila":      (9.9725,  76.3075),
    "Palarivattom": (10.0005, 76.3025),
    "Kadavanthra":  (9.9825,  76.2965),
}


def create_area_picker_map(selected_area):
    """
    Returns raw HTML string of a Folium map showing all 7 area markers.
    Clicking a marker sets ?pick_area=<area> on the parent page URL so
    Streamlit can read it via st.query_params.
    """
    m = folium.Map(location=[9.9975, 76.2900], zoom_start=12,
                   tiles="CartoDB positron")

    for area_name, (lat, lon) in AREA_CENTRES.items():
        is_sel  = area_name == selected_area
        color   = "#00d4ff" if is_sel else "#4a7a9b"
        radius  = 18        if is_sel else 13
        opacity = 1.0       if is_sel else 0.75
        weight  = 3         if is_sel else 1.5

        popup_html = (
            f'<div style="font-family:Arial;text-align:center;padding:4px 8px;">'
            f'<b style="font-size:13px;color:#1a2235;">{area_name}</b><br>'
            f'<a href="?pick_area={area_name}" target="_parent" '
            f'style="display:inline-block;margin-top:6px;padding:4px 12px;'
            f'background:#1a2235;color:#00d4ff;border-radius:5px;'
            f'font-size:11px;text-decoration:none;font-weight:600;">'
            f'Select Area</a>'
            f'</div>'
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=opacity,
            weight=weight,
            popup=folium.Popup(popup_html, max_width=180),
            tooltip=f"{'✦ ' if is_sel else ''}{area_name}{'  ← selected' if is_sel else '  — click to select'}"
        ).add_to(m)

        # Label on map
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-family:Arial;font-size:10px;font-weight:700;'
                     f'color:{"#00d4ff" if is_sel else "#2d3561"};'
                     f'white-space:nowrap;margin-top:18px;margin-left:-20px;'
                     f'text-shadow:1px 1px 2px white,-1px -1px 2px white;">'
                     f'{area_name}</div>',
                icon_size=(120, 20),
                icon_anchor=(0, 0)
            )
        ).add_to(m)

    # Instruction banner
    banner = (
        '<div style="position:absolute;top:10px;left:50%;transform:translateX(-50%);'
        'z-index:9999;background:#1a2235;color:#00d4ff;padding:7px 16px;'
        'border-radius:8px;font-family:Arial;font-size:11px;font-weight:600;'
        'letter-spacing:1px;border:1px solid #00d4ff44;pointer-events:none;'
        'white-space:nowrap;">'
        '📍 Click a marker then SELECT AREA to choose location'
        '</div>'
    )
    m.get_root().html.add_child(folium.Element(banner))

    return m._repr_html_()
