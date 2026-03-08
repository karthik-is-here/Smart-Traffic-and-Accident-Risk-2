import numpy as np
import config
import data_utils


def predict_all_roads(area, day_of_week, hour, weather_condition):
    models          = data_utils.load_models()
    cong_model      = models["congestion_model"]
    risk_model      = models["accident_risk_model"]
    class_orders    = models["class_orders"]
    congestion_order = class_orders["congestion_order"]
    risk_order       = class_orders["risk_order"]

    roads = config.AREA_ROADS.get(area, [])
    results = []

    for road in roads:
        try:
            X = data_utils.build_feature_row(area, road, day_of_week, hour, weather_condition)

            cong_idx   = int(cong_model.predict(X)[0])
            cong_proba = cong_model.predict_proba(X)[0]
            cong_level = congestion_order[cong_idx]
            cong_score = float(np.max(cong_proba))

            risk_idx   = int(risk_model.predict(X)[0])
            risk_proba = risk_model.predict_proba(X)[0]
            # risk model may have only 3 classes after dropping Very High
            available_risk = getattr(risk_model, "classes_", list(range(len(risk_proba))))
            risk_level = risk_order[available_risk[risk_idx]] if risk_idx < len(available_risk) else "Low"
            risk_score = float(np.max(risk_proba))

            props = config.ROAD_PROPERTIES.get(road, {})
            lat, lon = config.ROAD_COORDINATES.get(road, (10.0, 76.3))

            if 7 <= hour <= 9:
                peak = "7AM – 9AM"
            elif 17 <= hour <= 20:
                peak = "5PM – 8PM"
            elif 12 <= hour <= 14:
                peak = "12PM – 2PM"
            else:
                peak = f"{hour:02d}:00"

            results.append({
                "road_name":          road,
                "congestion_level":   cong_level,
                "congestion_score":   round(cong_score * 100, 1),
                "accident_risk_level": risk_level,
                "accident_risk_score": round(risk_score * 100, 1),
                "lat":                lat,
                "lon":                lon,
                "road_type":          props.get("road_type", "Local"),
                "speed_limit_kmph":   props.get("speed_limit_kmph", 40),
                "lanes":              props.get("lanes", 2),
                "peak_time":          peak,
                "weather_condition":  weather_condition,
            })
        except Exception as e:
            print(f"[predictor] Skipping {road}: {e}")

    return results
