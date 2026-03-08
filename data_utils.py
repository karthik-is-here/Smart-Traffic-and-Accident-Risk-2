import numpy as np
import pandas as pd
import joblib
import os
import config

_model_cache = {}

def load_models():
    global _model_cache
    if _model_cache:
        return _model_cache
    d = config.MODEL_DIR
    _model_cache = {
        "congestion_model":     joblib.load(os.path.join(d, "congestion_model.pkl")),
        "accident_risk_model":  joblib.load(os.path.join(d, "accident_risk_model.pkl")),
        "label_encoders":       joblib.load(os.path.join(d, "label_encoders.pkl")),
        "feature_columns":      joblib.load(os.path.join(d, "feature_columns.pkl")),
        "class_orders":         joblib.load(os.path.join(d, "class_orders.pkl")),
    }
    return _model_cache


DAY_INDEX = {d: i for i, d in enumerate(config.DAYS_OF_WEEK)}


def build_feature_row(area, road_name, day_of_week, hour, weather_condition,
                      vehicle_volume=None, avg_speed_kmph=None):
    models  = load_models()
    le_dict = models["label_encoders"]
    feat_cols = models["feature_columns"]

    props = config.ROAD_PROPERTIES.get(road_name, {"road_type": "Local", "lanes": 2, "speed_limit_kmph": 40})
    road_type       = props["road_type"]
    lanes           = props["lanes"]
    speed_limit     = props["speed_limit_kmph"]

    is_rush_hour = int(7 <= hour <= 9 or 17 <= hour <= 20)
    is_weekend   = int(day_of_week in ["Saturday", "Sunday"])
    is_night     = int(hour >= 22 or hour <= 5)

    if vehicle_volume is None:
        base = {"Highway": 2000, "Arterial": 1000, "Local": 500}[road_type] * lanes
        vehicle_volume = int(base * (1.5 if is_rush_hour else 1.0))

    if avg_speed_kmph is None:
        factor = 0.55 if is_rush_hour else 0.85
        if weather_condition in ["Heavy Rain", "Fog"]:
            factor -= 0.15
        avg_speed_kmph = round(speed_limit * factor, 1)

    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)
    day_idx  = DAY_INDEX.get(day_of_week, 0)
    day_sin  = np.sin(2 * np.pi * day_idx / 7)
    day_cos  = np.cos(2 * np.pi * day_idx / 7)

    def safe_encode(le, val):
        try:
            return int(le.transform([val])[0])
        except Exception:
            return 0

    row = {
        "hour":                  hour,
        "hour_sin":              hour_sin,
        "hour_cos":              hour_cos,
        "day_sin":               day_sin,
        "day_cos":               day_cos,
        "lanes":                 lanes,
        "speed_limit_kmph":      speed_limit,
        "vehicle_volume":        vehicle_volume,
        "avg_speed_kmph":        avg_speed_kmph,
        "is_rush_hour":          is_rush_hour,
        "is_weekend":            is_weekend,
        "is_night":              is_night,
        "area_enc":              safe_encode(le_dict["area"], area),
        "road_name_enc":         safe_encode(le_dict["road_name"], road_name),
        "road_type_enc":         safe_encode(le_dict["road_type"], road_type),
        "weather_condition_enc": safe_encode(le_dict["weather_condition"], weather_condition),
        "day_of_week_enc":       safe_encode(le_dict["day_of_week"], day_of_week),
    }

    return pd.DataFrame([row])[feat_cols]
