# ============================================================
#  constants.py
#  All static data: appliance list, watts, ML features, recommendations
# ============================================================

WATT: dict[str, int] = {
    "Air_Conditioning": 900,
    "Fridge":           150,
    "TV":               100,
    "Computer":         150,
    "Lights":            60,
    "Heater":          2000,
    "Dishwasher":      1200,
    "Oven":            2000,
    "Microwave":       1000,
    "Washing_Machine":  500,
}

APPLIANCES: list[dict] = [
    {"id": "Air_Conditioning", "label": "Air Conditioner (AC)", "emoji": "❄️",  "watt_desc": "900 W"},
    {"id": "Fridge",           "label": "Refrigerator",         "emoji": "🧊",  "watt_desc": "150 W"},
    {"id": "TV",               "label": "Television",           "emoji": "📺",  "watt_desc": "100 W"},
    {"id": "Computer",         "label": "Computer / Laptop",    "emoji": "💻",  "watt_desc": "150 W"},
    {"id": "Lights",           "label": "Lights",               "emoji": "💡",  "watt_desc": "60 W"},
    {"id": "Heater",           "label": "Water Heater",         "emoji": "🔥",  "watt_desc": "2,000 W"},
    {"id": "Dishwasher",       "label": "Dishwasher",           "emoji": "🍽️", "watt_desc": "1,200 W"},
    {"id": "Oven",             "label": "Oven",                 "emoji": "🍞",  "watt_desc": "2,000 W"},
    {"id": "Microwave",        "label": "Microwave",            "emoji": "🍲",  "watt_desc": "1,000 W"},
    {"id": "Washing_Machine",  "label": "Washing Machine",      "emoji": "🧺",  "watt_desc": "500 W"},
]

# Order of columns MUST match training dataset
FITUR_ML: list[str] = [
    "total_kwh_tahun",
    "household_size",
    "avg_temp",
    "kwh_Air_Conditioning", "kwh_Computer",  "kwh_Dishwasher",
    "kwh_Fridge",           "kwh_Heater",    "kwh_Lights",
    "kwh_Microwave",        "kwh_Oven",      "kwh_TV",
    "kwh_Washing_Machine",
    "prop_Air_Conditioning","prop_Computer",  "prop_Dishwasher",
    "prop_Fridge",          "prop_Heater",    "prop_Lights",
    "prop_Microwave",       "prop_Oven",      "prop_TV",
    "prop_Washing_Machine",
    "kwh_per_orang",
]

# (emoji, title, HTML recommendation text)
RECO_DB: dict[str, tuple] = {
    "Air_Conditioning": ("❄️",  "Optimize AC temperature",       "Set to <b>24-26°C</b> — each 1°C increase saves ~6% energy. Use <i>sleep</i> mode at night."),
    "Heater":           ("🔥",  "Save on water heating",         "Consider <b>solar water heaters</b> or shower without heating during the day."),
    "Oven":             ("🍞",  "Cook smarter with oven",        "<b>Cook multiple items at once</b> and use residual heat after turning it off."),
    "Dishwasher":       ("🍽️", "Optimize dishwasher usage",    "Run only when <b>full</b> and choose energy-saving modes."),
    "Washing_Machine":  ("🧺",  "Wash smarter",                  "Wash with <b>cold water</b> — saves up to 90% energy per cycle."),
    "Fridge":           ("🧊",  "Maintain fridge efficiency",    "Set temp to <b>3-5°C</b>. Keep doors tightly closed, do not insert hot food."),
    "Computer":         ("💻",  "Save computer energy",          "Enable <b>auto-sleep</b> after 10-15 mins of inactivity and use power-saving modes."),
    "TV":               ("📺",  "Watch TV efficiently",          "Turn TV <b>completely off</b> (not standby). Standby mode still consumes electricity!"),
    "Lights":           ("💡",  "Maximize natural light",        "Switch to <b>LEDs</b> and use natural sunlight. Turn off lights in empty rooms."),
    "Microwave":        ("🍲",  "Microwave > stove",             "Microwaves are more <b>energy efficient</b> than stoves for heating small portions."),
}

# PLN electricity price per kWh (Rp)
TARIF_PLN: float = 1444.70

# Rata-rata realistis Indonesia (kWh/orang/BULAN) — acuan PLN ~150 kWh/rumah ÷ ~3 orang
AVG_KWH_ORANG_INDO: float = 45.0

# CO2 emission factor (kg per kWh) - hanya untuk menghitung emisi karbonnya saja (tidak berpengaruh terhadap model)
FAKTOR_CO2: float = 0.87

SKALA_MODEL: float = 1.0