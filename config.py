import os

MODEL_DIR = "models"

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEATHER_OPTIONS = ["Clear", "Cloudy", "Light Rain", "Heavy Rain", "Fog"]

CONGESTION_COLORS = {"Low": "green", "Moderate": "orange", "High": "red", "Very High": "darkred"}
RISK_COLORS       = {"Low": "green", "Moderate": "orange", "High": "red", "Very High": "darkred"}

AREA_ROADS = {
    "Edappally": [
        "NH 66 Bypass Edappally", "Edappally Junction Road", "Edappally-Pulinchode Road",
        "Seaport-Airport Road (Edappally)", "Kaloor-Edappally Road", "Vyttila-Edappally Road",
        "NH 544 Edappally Stretch", "Edappally Toll Road"
    ],
    "Kakkanad": [
        "Kakkanad-Kalamaserry Road", "Infopark Road", "Kakkanad Junction Road",
        "Seaport-Airport Road (Kakkanad)", "Rajagiri Road", "High Court Road Kakkanad",
        "Thrikkakara Road", "Cusat Road", "Kakkanad-Edappally Link Road"
    ],
    "Fort Kochi": [
        "Beach Road Fort Kochi", "Calvathy Road", "River Road Fort Kochi",
        "Princess Street", "Napier Street", "Fort Kochi-Mattancherry Road",
        "Parade Ground Road", "KB Jacob Road", "Burger Street"
    ],
    "Mattancherry": [
        "Mattancherry Palace Road", "Jew Town Road", "Bazaar Road Mattancherry",
        "Mattancherry-Willingdon Island Road", "Dutch Cemetery Road",
        "Harbour Road Mattancherry", "Jos Junction Road", "Marine Drive Mattancherry"
    ],
    "Vyttila": [
        "Vyttila Hub Road", "NH 66 Vyttila Stretch", "Vyttila-Kalamassery Road",
        "Vyttila-Kakkanad Road", "SA Road Vyttila", "Vyttila-Palarivattom Road",
        "Petta Road Vyttila", "SRM Road Vyttila"
    ],
    "Palarivattom": [
        "Palarivattom Junction Road", "MG Road Palarivattom", "NH 544 Palarivattom",
        "Palarivattom-Edappally Road", "Palarivattom-Vyttila Road",
        "Chembumukku Road", "Banerji Road Palarivattom", "Foreshore Road Palarivattom"
    ],
    "Kadavanthra": [
        "Kadavanthra Junction Road", "MG Road Kadavanthra", "Convent Road Kadavanthra",
        "Kadavanthra-Vyttila Road", "South Janatha Road", "Ravipuram Road",
        "Foreshore Road Kadavanthra", "Sreekandath Road"
    ]
}

ROAD_COORDINATES = {
    # Edappally
    "NH 66 Bypass Edappally":           (10.0269, 76.3083),
    "Edappally Junction Road":          (10.0250, 76.3070),
    "Edappally-Pulinchode Road":        (10.0290, 76.3110),
    "Seaport-Airport Road (Edappally)": (10.0310, 76.3150),
    "Kaloor-Edappally Road":            (10.0230, 76.3020),
    "Vyttila-Edappally Road":           (10.0200, 76.3060),
    "NH 544 Edappally Stretch":         (10.0260, 76.3095),
    "Edappally Toll Road":              (10.0275, 76.3105),
    # Kakkanad
    "Kakkanad-Kalamaserry Road":        (10.0210, 76.3410),
    "Infopark Road":                    (10.0230, 76.3450),
    "Kakkanad Junction Road":           (10.0200, 76.3390),
    "Seaport-Airport Road (Kakkanad)":  (10.0250, 76.3480),
    "Rajagiri Road":                    (10.0180, 76.3430),
    "High Court Road Kakkanad":         (10.0160, 76.3400),
    "Thrikkakara Road":                 (10.0240, 76.3500),
    "Cusat Road":                       (10.0270, 76.3520),
    "Kakkanad-Edappally Link Road":     (10.0220, 76.3350),
    # Fort Kochi
    "Beach Road Fort Kochi":            (9.9670,  76.2430),
    "Calvathy Road":                    (9.9650,  76.2450),
    "River Road Fort Kochi":            (9.9640,  76.2410),
    "Princess Street":                  (9.9660,  76.2460),
    "Napier Street":                    (9.9655,  76.2440),
    "Fort Kochi-Mattancherry Road":     (9.9620,  76.2480),
    "Parade Ground Road":               (9.9680,  76.2420),
    "KB Jacob Road":                    (9.9645,  76.2470),
    "Burger Street":                    (9.9635,  76.2455),
    # Mattancherry
    "Mattancherry Palace Road":         (9.9570,  76.2590),
    "Jew Town Road":                    (9.9555,  76.2600),
    "Bazaar Road Mattancherry":         (9.9580,  76.2580),
    "Mattancherry-Willingdon Island Road": (9.9600, 76.2620),
    "Dutch Cemetery Road":              (9.9545,  76.2570),
    "Harbour Road Mattancherry":        (9.9610,  76.2640),
    "Jos Junction Road":                (9.9565,  76.2610),
    "Marine Drive Mattancherry":        (9.9590,  76.2560),
    # Vyttila
    "Vyttila Hub Road":                 (9.9720,  76.3080),
    "NH 66 Vyttila Stretch":            (9.9710,  76.3060),
    "Vyttila-Kalamassery Road":         (9.9740,  76.3100),
    "Vyttila-Kakkanad Road":            (9.9750,  76.3130),
    "SA Road Vyttila":                  (9.9700,  76.3050),
    "Vyttila-Palarivattom Road":        (9.9730,  76.3020),
    "Petta Road Vyttila":               (9.9695,  76.3090),
    "SRM Road Vyttila":                 (9.9760,  76.3070),
    # Palarivattom
    "Palarivattom Junction Road":       (10.0010, 76.3030),
    "MG Road Palarivattom":             (10.0000, 76.3010),
    "NH 544 Palarivattom":              (10.0020, 76.3050),
    "Palarivattom-Edappally Road":      (10.0040, 76.3070),
    "Palarivattom-Vyttila Road":        (9.9990,  76.3020),
    "Chembumukku Road":                 (10.0060, 76.3090),
    "Banerji Road Palarivattom":        (9.9980,  76.3000),
    "Foreshore Road Palarivattom":      (9.9970,  76.2980),
    # Kadavanthra
    "Kadavanthra Junction Road":        (9.9820,  76.2970),
    "MG Road Kadavanthra":              (9.9810,  76.2950),
    "Convent Road Kadavanthra":         (9.9830,  76.2990),
    "Kadavanthra-Vyttila Road":         (9.9800,  76.3010),
    "South Janatha Road":               (9.9840,  76.2960),
    "Ravipuram Road":                   (9.9850,  76.2940),
    "Foreshore Road Kadavanthra":       (9.9790,  76.2930),
    "Sreekandath Road":                 (9.9860,  76.2980),
}

ROAD_PROPERTIES = {}
for area, road_list in AREA_ROADS.items():
    for road in road_list:
        if any(k in road for k in ["NH", "Bypass", "Seaport-Airport", "Toll Road"]):
            ROAD_PROPERTIES[road] = {"road_type": "Highway",  "lanes": 4, "speed_limit_kmph": 70}
        elif any(k in road for k in ["Junction", "MG Road", "Hub", "Infopark"]):
            ROAD_PROPERTIES[road] = {"road_type": "Arterial", "lanes": 4, "speed_limit_kmph": 50}
        else:
            ROAD_PROPERTIES[road] = {"road_type": "Local",    "lanes": 2, "speed_limit_kmph": 40}
